//! Whether the Machine's installed app is the window in front: then the robot goes away (README.md). Asked of the window
//! system when another window comes to the front, and only which program's window that is: the id its browser gave the
//! app, as webapp.rs knows it. Never its title or what is in it. A dashboard in a browser's tab is the browser's.
use crate::{dash, later, looked, webapp, windows, Shared};
use std::sync::atomic::Ordering;
use std::sync::mpsc::{Receiver, Sender};
use std::time::Duration;
use tauri::{AppHandle, Manager};

/// What is in front has to stay there this long, so nothing flickers.
const SETTLE: Duration = Duration::from_millis(300);

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Front {
    App,
    /// The robot or its box, or a file opened from there or from the dashboard.
    Own,
    Other,
    #[cfg_attr(not(target_os = "linux"), allow(dead_code))]
    /// No window has the keys: they are in the robot's box, or in nothing.
    Nothing,
}

/// What a change of the window in front does: the robot goes (true) or comes back (false). None: it stays as it is, so
/// that a click on the robot or its box is never the app being left.
fn change(was: Front, now: Front) -> Option<bool> {
    match (was, now) {
        (a, b) if a == b => None,
        (_, Front::App) => Some(true),
        (_, Front::Own) => None,
        (_, Front::Other | Front::Nothing) => Some(false),
    }
}

/// Whether what is in front is full screen, where the window system tells (on Windows: windows::full_screen).
pub fn full() -> bool {
    system::full()
}

pub fn watch(app: &AppHandle) {
    let (changed, changes) = std::sync::mpsc::channel();
    if system::listen(changed) {
        let app = app.clone();
        std::thread::spawn(move || follow(&app, &changes));
    }
}

fn follow(app: &AppHandle, changes: &Receiver<()>) {
    let mut was = if app.state::<Shared>().away.load(Ordering::Relaxed) { Front::App } else { Front::Other };
    loop {
        // Now and then without being told, for what isn't: the app was installed, or the sign-in changed
        let _ = changes.recv_timeout(Duration::from_secs(5));
        while changes.recv_timeout(SETTLE).is_ok() {}
        let shared = app.state::<Shared>();
        let now = shared.signed_in().map_or(Front::Other, |(machine, alone)| system::front(&webapp::ids(&machine, alone)));
        let now = if dash::file_front() { Front::Own } else if dash::front() { Front::App } else if now == Front::Nothing && windows::box_open(app) { Front::Own } else { now };
        let todo = change(was, now);
        was = now;
        if let Some(gone) = todo {
            if shared.away.swap(gone, Ordering::Relaxed) && !gone {
                shared.look_soon(); // what was done there
            }
            later(app, move |app| {
                if gone {
                    app.state::<Shared>().look_soon(); // it doesn't speak now
                    looked(app);
                    windows::close_box(app);
                }
                windows::show_or_not(app);
            });
        }
    }
}

#[cfg(windows)]
mod system {
    use super::{Front, Sender};
    use std::sync::OnceLock;
    use ::windows::core::PCWSTR;
    use ::windows::Win32::Foundation::{HWND, PROPERTYKEY};
    use ::windows::Win32::System::Com::{CoInitializeEx, COINIT_MULTITHREADED};
    use ::windows::Win32::System::Com::StructuredStorage::PropVariantToStringAlloc;
    use ::windows::Win32::System::Threading::GetCurrentProcessId;
    use ::windows::Win32::UI::Accessibility::{SetWinEventHook, HWINEVENTHOOK};
    use ::windows::Win32::UI::Shell::PropertiesSystem::{IPropertyStore, SHGetPropertyStoreForWindow};
    use ::windows::Win32::UI::WindowsAndMessaging::{
        DispatchMessageW, GetForegroundWindow, GetMessageW, GetWindowThreadProcessId, EVENT_SYSTEM_FOREGROUND, EVENT_SYSTEM_MINIMIZEEND, EVENT_SYSTEM_MINIMIZESTART, MSG,
        WINEVENT_OUTOFCONTEXT,
    };

    static CHANGED: OnceLock<std::sync::Mutex<Sender<()>>> = OnceLock::new();

    unsafe extern "system" fn changed(_: HWINEVENTHOOK, _: u32, _: HWND, _: i32, _: i32, _: u32, _: u32) {
        if let Some(to) = CHANGED.get() {
            let _ = to.lock().map(|to| to.send(()));
        }
    }

    pub fn listen(to: Sender<()>) -> bool {
        if CHANGED.set(std::sync::Mutex::new(to)).is_err() {
            return false;
        }
        std::thread::spawn(|| {
            // SAFETY: the callback is a function of the program's; this thread's messages are where Windows runs it.
            unsafe {
                for (from, to) in [(EVENT_SYSTEM_FOREGROUND, EVENT_SYSTEM_FOREGROUND), (EVENT_SYSTEM_MINIMIZESTART, EVENT_SYSTEM_MINIMIZEEND)] {
                    let _ = SetWinEventHook(from, to, None, Some(changed), 0, 0, WINEVENT_OUTOFCONTEXT);
                }
                let mut message = MSG::default();
                while GetMessageW(&mut message, None, 0, 0).as_bool() {
                    DispatchMessageW(&message);
                }
            }
        });
        true
    }

    /// Two of the taskbar's facts on a window: the id it is grouped by, and how it is started again.
    const TASKBAR: ::windows::core::GUID = ::windows::core::GUID::from_u128(0x9F4C2855_9F79_4B39_A8D0_E1D42DE1D5F3);
    const RELAUNCH: PROPERTYKEY = PROPERTYKEY { fmtid: TASKBAR, pid: 2 };
    const ID: PROPERTYKEY = PROPERTYKEY { fmtid: TASKBAR, pid: 5 };

    pub fn full() -> bool {
        false
    }

    pub fn front(ids: &[String]) -> Front {
        // SAFETY: plain calls; what they give back is checked, and freed by its own types.
        unsafe {
            let _ = CoInitializeEx(None, COINIT_MULTITHREADED);
            let window = GetForegroundWindow();
            let mut process = 0;
            GetWindowThreadProcessId(window, Some(&mut process));
            if process == GetCurrentProcessId() {
                return Front::Own;
            }
            let Ok(store) = SHGetPropertyStoreForWindow::<IPropertyStore>(window) else { return Front::Other };
            let read = |key: &PROPERTYKEY| {
                let value = store.GetValue(key).ok()?;
                let text = PropVariantToStringAlloc(&value).ok()?;
                let copy = PCWSTR(text.0).to_string().ok();
                ::windows::Win32::System::Com::CoTaskMemFree(Some(text.0.cast()));
                copy
            };
            let (group, start) = (read(&ID).unwrap_or_default(), read(&RELAUNCH).unwrap_or_default());
            if ids.iter().any(|id| super::is_app(&group, &start, id)) { Front::App } else { Front::Other }
        }
    }
}

/// On Windows: the window's group is "Chrome._crx_<id>", each part cut in its middle to fit 64 characters in all
/// (ShellUtil::BuildAppUserModelId), and the app is started again with its id.
#[cfg_attr(not(windows), allow(dead_code))]
fn is_app(group: &str, start: &str, id: &str) -> bool {
    let name = format!("_crx_{id}");
    let cut = |most: usize| if name.len() > most { format!("{}{}", &name[..most / 2], &name[name.len() - (most + 1) / 2..]) } else { name.clone() };
    let parts: Vec<&str> = group.split('.').collect();
    let given = [2, 3].iter().any(|n| parts.contains(&cut((64 - (n - 1)) / n).as_str())) || parts.contains(&name.as_str());
    let flag = format!("--app-id={id}");
    given || start.split_whitespace().any(|a| a.trim_matches('"') == flag)
}

/// The class in Hyprland's event of another window in front ("activewindow>>class,title"). No other event, and no title.
#[cfg(target_os = "linux")]
fn active(line: &[u8]) -> Option<String> {
    let rest = line.strip_prefix(b"activewindow>>")?;
    let class = rest.split(|b| *b == b',').next()?;
    Some(String::from_utf8_lossy(&class[..class.len().min(200)]).into_owned())
}

/// On Wayland an installed app's class is "<browser>-<id>-<profile>".
#[cfg(target_os = "linux")]
fn is_class(class: &str, ids: &[String]) -> bool {
    class.split('-').skip(1).any(|part| ids.iter().any(|id| part == id))
}

/// X11: the window manager says which window is in front, and that window which app's it is. XWayland too, as long as
/// the app is there as well. Wayland has no such question for a program, so there the robot stays, but Hyprland tells what
/// comes to the front on a socket of its own.
#[cfg(target_os = "linux")]
mod system {
    use super::{Front, Sender};
    use x11rb::connection::Connection;
    use x11rb::protocol::xproto::{AtomEnum, ChangeWindowAttributesAux, ConnectionExt, EventMask, Window};
    use x11rb::protocol::Event;
    use x11rb::rust_connection::RustConnection;

    fn x11() -> bool {
        use gtk::gdk::prelude::*;
        gtk::gdk::Display::default().is_some_and(|d| d.type_().name() == "GdkX11Display")
    }

    pub fn listen(to: Sender<()>) -> bool {
        if !x11() {
            return hyprland::listen(to);
        }
        X11.store(true, std::sync::atomic::Ordering::Relaxed);
        std::thread::spawn(move || {
            let Ok((x, screen)) = x11rb::connect(None) else { return };
            let root = x.setup().roots[screen].root;
            let told = ChangeWindowAttributesAux::new().event_mask(EventMask::PROPERTY_CHANGE);
            let Some(active) = atom(&x, "_NET_ACTIVE_WINDOW") else { return };
            if x.change_window_attributes(root, &told).is_err() || x.flush().is_err() {
                return;
            }
            while let Ok(event) = x.wait_for_event() {
                if matches!(event, Event::PropertyNotify(p) if p.atom == active) && to.send(()).is_err() {
                    return;
                }
            }
        });
        true
    }

    fn atom(x: &RustConnection, name: &str) -> Option<u32> {
        Some(x.intern_atom(false, name.as_bytes()).ok()?.reply().ok()?.atom)
    }

    pub fn front(ids: &[String]) -> Front {
        hyprland::front(ids).or_else(|| read(ids)).unwrap_or(Front::Other)
    }

    /// Known once listen() asked on the main thread, the only one GDK answers on.
    static X11: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

    pub fn full() -> bool {
        hyprland::full().unwrap_or_else(|| X11.load(std::sync::atomic::Ordering::Relaxed) && read_full().unwrap_or(false))
    }

    fn read_full() -> Option<bool> {
        let (x, screen) = x11rb::connect(None).ok()?;
        let first = |window: Window, name: &str, kind: AtomEnum, most: u32| -> Option<Vec<u32>> {
            let found = x.get_property(false, window, atom(&x, name)?, kind, 0, most).ok()?.reply().ok()?;
            let all = found.value32()?.collect();
            Some(all)
        };
        let window = *first(x.setup().roots[screen].root, "_NET_ACTIVE_WINDOW", AtomEnum::WINDOW, 1)?.first().filter(|w| **w != 0)?;
        let full = atom(&x, "_NET_WM_STATE_FULLSCREEN")?;
        Some(first(window, "_NET_WM_STATE", AtomEnum::ATOM, 32)?.contains(&full))
    }

    /// Only where Hyprland says it is there, and only the program's name (its class): the title after it is never kept.
    mod hyprland {
        use super::{Front, Sender};
        use std::io::{BufRead, BufReader, Read, Write};
        use std::os::unix::net::UnixStream;
        use std::sync::Mutex;

        /// The program in front; nothing is: an empty desktop, or the keys are in a layer (the robot's box, a launcher).
        static IN_FRONT: Mutex<Option<String>> = Mutex::new(None);

        fn connect(socket: &str) -> Option<UnixStream> {
            let (run, which) = (std::env::var_os("XDG_RUNTIME_DIR")?, std::env::var_os("HYPRLAND_INSTANCE_SIGNATURE")?);
            UnixStream::connect(std::path::Path::new(&run).join("hypr").join(which).join(socket)).ok()
        }

        /// One question on its other socket; of the answer only what T names is read.
        fn ask<T: serde::de::DeserializeOwned>(question: &str) -> Option<T> {
            let mut socket = connect(".socket.sock")?;
            let soon = Some(std::time::Duration::from_secs(2));
            socket.set_read_timeout(soon).ok()?;
            socket.write_all(question.as_bytes()).ok()?;
            let mut answer = Vec::new();
            socket.take(64 << 10).read_to_end(&mut answer).ok()?;
            serde_json::from_slice(&answer).ok()
        }

        #[derive(serde::Deserialize)]
        struct Window {
            fullscreen: serde_json::Value,
        }

        #[derive(serde::Deserialize)]
        struct Locked {
            locked: bool,
        }

        /// The window in front is full screen (2 and up; 1 is only maximized), or the screen is locked. None: not Hyprland.
        pub fn full() -> Option<bool> {
            connect(".socket.sock")?;
            let window = ask::<Window>("j/activewindow").is_some_and(|w| w.fullscreen == true || w.fullscreen.as_i64().is_some_and(|f| f >= 2));
            Some(window || ask::<Locked>("j/locked").is_some_and(|l| l.locked))
        }

        pub fn listen(to: Sender<()>) -> bool {
            let Some(stream) = connect(".socket2.sock") else { return false };
            *IN_FRONT.lock().unwrap() = Some(String::new());
            std::thread::spawn(move || {
                for line in BufReader::new(stream).split(b'\n') {
                    let Ok(line) = line else { break };
                    let Some(class) = super::super::active(&line) else { continue };
                    *IN_FRONT.lock().unwrap() = Some(class);
                    if to.send(()).is_err() {
                        break;
                    }
                }
                *IN_FRONT.lock().unwrap() = Some(String::new()); // Hyprland went: so does what was in front
                let _ = to.send(());
            });
            true
        }

        pub fn front(ids: &[String]) -> Option<Front> {
            let class = IN_FRONT.lock().unwrap().clone()?;
            Some(match class.as_str() {
                "" => Front::Nothing,
                class if super::super::is_class(class, ids) => Front::App,
                _ => Front::Other,
            })
        }
    }

    fn read(ids: &[String]) -> Option<Front> {
        let (x, screen) = x11rb::connect(None).ok()?;
        let root = x.setup().roots[screen].root;
        let number = |window: Window, name: &str, kind: AtomEnum| -> Option<u32> {
            let found = x.get_property(false, window, atom(&x, name)?, kind, 0, 1).ok()?.reply().ok()?;
            let first = found.value32()?.next();
            first
        };
        let window = number(root, "_NET_ACTIVE_WINDOW", AtomEnum::WINDOW).filter(|w| *w != 0)?;
        if number(window, "_NET_WM_PID", AtomEnum::CARDINAL) == Some(std::process::id()) {
            return Some(Front::Own);
        }
        // Two names, each ended by a 0: an installed app's first is crx_<id>
        let class = x.get_property(false, window, AtomEnum::WM_CLASS, AtomEnum::STRING, 0, 64).ok()?.reply().ok()?.value;
        let first = class.split(|b| *b == 0).next()?;
        let app = ids.iter().any(|id| first == format!("crx_{id}").as_bytes());
        Some(if app { Front::App } else { Front::Other })
    }
}

/// macOS says which program is in front, and its id: an installed app's is its browser's with ".app.<id>" after it. The
/// robot's box takes the keys without coming to the front (mac.rs), so that is kept here.
#[cfg(target_os = "macos")]
mod system {
    use super::{Front, Sender};
    use crate::mac::on;
    use objc2_app_kit::{NSRunningApplication, NSWindowDidBecomeKeyNotification, NSWindowDidResignKeyNotification, NSWorkspace, NSWorkspaceDidActivateApplicationNotification};
    use objc2_foundation::NSNotificationCenter;
    use std::sync::atomic::{AtomicBool, Ordering};

    static KEYS: AtomicBool = AtomicBool::new(false);

    pub fn full() -> bool {
        crate::mac::FULL.load(Ordering::Relaxed)
    }

    pub fn listen(to: Sender<()>) -> bool {
        // SAFETY: constants of AppKit's.
        let (program, got, lost) = unsafe { (NSWorkspaceDidActivateApplicationNotification, NSWindowDidBecomeKeyNotification, NSWindowDidResignKeyNotification) };
        let tell = to.clone();
        on(&NSWorkspace::sharedWorkspace().notificationCenter(), program, move || { let _ = tell.send(()); });
        for (name, keys) in [(got, true), (lost, false)] {
            let tell = to.clone();
            on(&NSNotificationCenter::defaultCenter(), name, move || {
                KEYS.store(keys, Ordering::Relaxed);
                let _ = tell.send(());
            });
        }
        true
    }

    pub fn front(ids: &[String]) -> Front {
        if KEYS.load(Ordering::Relaxed) {
            return Front::Own;
        }
        let Some(program) = NSWorkspace::sharedWorkspace().frontmostApplication() else { return Front::Other };
        if program == NSRunningApplication::currentApplication() {
            return Front::Nothing; // its window was closed
        }
        let name = program.bundleIdentifier().map(|b| b.to_string()).unwrap_or_default();
        if ids.iter().any(|id| super::is_bundle(&name, id)) { Front::App } else { Front::Other }
    }
}

/// On macOS an installed app is a program of its own, "<browser's>.app.<id>".
#[cfg_attr(not(target_os = "macos"), allow(dead_code))]
fn is_bundle(name: &str, id: &str) -> bool {
    name.strip_suffix(id).is_some_and(|browser| browser.ends_with(".app."))
}

#[cfg(not(any(windows, target_os = "linux", target_os = "macos")))]
mod system {
    use super::{Front, Sender};

    pub fn listen(_: Sender<()>) -> bool {
        false
    }

    pub fn full() -> bool {
        false
    }

    pub fn front(_: &[String]) -> Front {
        Front::Other
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_goes_and_comes_back() {
        use Front::*;
        assert_eq!(change(Other, App), Some(true));
        assert_eq!(change(App, Other), Some(false));
        assert_eq!(change(App, App), None);
        // The box over the app: a click in it leaves things as they are, one in the app closes it again
        assert_eq!(change(App, Own), None);
        assert_eq!(change(Own, App), Some(true));
        assert_eq!(change(Own, Other), Some(false));
        assert_eq!(change(Other, Own), None);
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn hyprland_says_only_the_class() {
        let ids = ["fgbphkfplekcbajjgdeoaplmlccnhblm".to_string()];
        let class = |line: &str| active(line.as_bytes());
        assert_eq!(class("activewindow>>chrome-fgbphkfplekcbajjgdeoaplmlccnhblm-Default,The Machine, To-dos").unwrap(), "chrome-fgbphkfplekcbajjgdeoaplmlccnhblm-Default");
        assert_eq!(class("activewindow>>,").unwrap(), "");
        for other in ["activewindowv2>>5591", "openwindow>>a,1,chrome-fgbphkfplekcbajjgdeoaplmlccnhblm-Default,x", "workspace>>2", ""] {
            assert_eq!(class(other), None, "{other}");
        }
        for (class, app) in [("chrome-fgbphkfplekcbajjgdeoaplmlccnhblm-Default", true), ("brave-fgbphkfplekcbajjgdeoaplmlccnhblm-Profile_1", true),
            ("chromium-browser", false), ("chrome-aaaphkfplekcbajjgdeoaplmlccnhblm-Default", false), ("fgbphkfplekcbajjgdeoaplmlccnhblm", false)] {
            assert_eq!(is_class(class, &ids), app, "{class}");
        }
        assert_eq!(change(Front::App, Front::Nothing), Some(false));
    }

    #[test]
    fn only_the_machines_app() {
        let (id, other) = ("fgbphkfplekcbajjgdeoaplmlccnhblm", "aaaphkfplekcbajjgdeoaplmlccnhblm");
        for group in ["Chrome._crx_fgbphkfpleccnhblm", "x._crx_fgbphkfplekcbajjgdeoaplmlccnhblm"] {
            assert_eq!(is_app(group, "", id), group.starts_with('x'), "{group}");
        }
        let two = format!("Chrome.{}{}", &format!("_crx_{id}")[..15], &format!("_crx_{id}")[21..]);
        let three = format!("Chrome.{}{}.Profile_1", &format!("_crx_{id}")[..10], &format!("_crx_{id}")[27..]);
        assert!(is_app(&two, "", id) && is_app(&three, "", id));
        assert!(!is_app(&two, "", other) && !is_app(&three, "", other));
        let start = format!("\"C:\\a b\\chrome_proxy.exe\" --profile-directory=Default --app-id={id}");
        assert!(is_bundle(&format!("com.google.Chrome.app.{id}"), id) && !is_bundle(&format!("com.google.Chrome.app.{other}"), id));
        assert!(!is_bundle("com.google.Chrome", id) && !is_bundle(id, id));
        assert!(is_app("Chrome", &start, id) && !is_app("Chrome", &start, other) && !is_app("Chrome", "", id));
    }
}
