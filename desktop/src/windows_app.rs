//! What the dashboard's window has on Windows besides what it has everywhere: the keys a menu has elsewhere, its zoom, a
//! page that ended, how many wait on its icon in the taskbar, and Windows' own notifications.
use crate::keys::{self, Held};
use crate::{dash, later, notify};
use ::windows::core::{Error, HSTRING};
use ::windows::Data::Xml::Dom::XmlDocument;
use ::windows::Foundation::TypedEventHandler;
use ::windows::UI::Notifications::{NotificationSetting, ToastNotification, ToastNotificationManager};
use std::path::Path;
use std::sync::Mutex;
use tauri::{AppHandle, Manager, WebviewWindow};
use webview2_com::Microsoft::Web::WebView2::Win32::{
    COREWEBVIEW2_KEY_EVENT_KIND_KEY_DOWN, COREWEBVIEW2_KEY_EVENT_KIND_SYSTEM_KEY_DOWN, COREWEBVIEW2_PROCESS_FAILED_KIND_RENDER_PROCESS_EXITED,
};
use webview2_com::{AcceleratorKeyPressedEventHandler, ProcessFailedEventHandler, ZoomFactorChangedEventHandler};
use windows_sys::Win32::UI::Input::KeyboardAndMouse::{GetKeyState, VK_CONTROL, VK_F11, VK_F5, VK_MENU, VK_SHIFT};

/// Windows' number of a key, as keys.rs has it.
fn key(code: u32) -> &'static str {
    match code {
        0xBB | 0x6B => "+",
        0xBD | 0x6D => "-",
        0x30 | 0x60 => "0",
        0x52 => "r",
        0x53 => "s",
        0x57 => "w",
        0xBC => ",",
        k if k == u32::from(VK_F11) => "F11",
        k if k == u32::from(VK_F5) => "F5",
        _ => "",
    }
}

/// A page that ends is there again.
pub fn lives(window: &WebviewWindow) {
    let (app, label) = (window.app_handle().clone(), window.label().to_string());
    let _ = window.with_webview(move |page| {
        let failed = ProcessFailedEventHandler::create(Box::new(move |_, args| {
            let mut kind = Default::default();
            // SAFETY: the event's own arguments, and a valid place.
            if let Some(Ok(())) = args.map(|a| unsafe { a.ProcessFailedKind(&mut kind) }) {
                if kind == COREWEBVIEW2_PROCESS_FAILED_KIND_RENDER_PROCESS_EXITED {
                    let label = label.clone();
                    later(&app, move |app| dash::died(app, &label));
                }
            }
            Ok(())
        }));
        // SAFETY: the window's own page, on its own thread.
        let _ = unsafe { page.controller().CoreWebView2().and_then(|page| page.add_ProcessFailed(&failed, &mut 0)) };
    });
}

pub fn prepare(window: &WebviewWindow) {
    crate::windows::no_menu(window);
    lives(window);
    let (app, label) = (window.app_handle().clone(), window.label().to_string());
    let _ = window.with_webview(move |page| {
        let controller = page.controller();
        let mut token = 0;
        let (here, of) = (app.clone(), label.clone());
        let pressed = AcceleratorKeyPressedEventHandler::create(Box::new(move |_, args| {
            let Some(args) = args else { return Ok(()) };
            let (mut kind, mut code) = (COREWEBVIEW2_KEY_EVENT_KIND_KEY_DOWN, 0);
            // SAFETY: the arguments are this event's; the two places are valid.
            let found = unsafe {
                args.KeyEventKind(&mut kind)?;
                args.VirtualKey(&mut code)?;
                let held = |k: u16| GetKeyState(k.into()) < 0;
                keys::does(&of, key(code), Held { ctrl: held(VK_CONTROL), shift: held(VK_SHIFT), alt: held(VK_MENU) })
            };
            if let (Some(what), COREWEBVIEW2_KEY_EVENT_KIND_KEY_DOWN | COREWEBVIEW2_KEY_EVENT_KIND_SYSTEM_KEY_DOWN) = (found, kind) {
                // SAFETY: as above.
                unsafe { args.SetHandled(true)? };
                let of = of.clone();
                later(&here, move |app| keys::run(app, &of, what));
            }
            Ok(())
        }));
        let zooms = app.clone();
        let zoomed = ZoomFactorChangedEventHandler::create(Box::new(move |controller, _| {
            let mut zoom = 0.0;
            // SAFETY: the event's own controller, and a valid place.
            if let Some(Ok(())) = controller.map(|c| unsafe { c.ZoomFactor(&mut zoom) }) {
                later(&zooms, move |app| dash::zoomed_by_hand(app, zoom));
            }
            Ok(())
        }));

        // SAFETY: the window's own controller, on its own thread.
        unsafe {
            let _ = controller.add_AcceleratorKeyPressed(&pressed, &mut token);
            if label == dash::LABEL {
                let _ = controller.add_ZoomFactorChanged(&zoomed, &mut token);
            }
        }
    });
}

// The taskbar

/// How many wait, on its icon there: 1 to 99, and 99+, as the dashboard installed as an app has it. Windows forgets it when
/// the window goes.
pub fn badge(app: &AppHandle, count: usize) {
    let Some(window) = dash::window(app).filter(|w| w.is_visible().unwrap_or(false)) else { return };
    let _ = window.set_overlay_icon(if count == 0 { None } else { number(count) });
}

/// Badge n of icons/badges.png (tools/badges.py draws them): ten in a row, ten rows, the last 99+.
fn number(count: usize) -> Option<tauri::image::Image<'static>> {
    const SIDE: usize = 32;
    let mut read = png::Decoder::new(std::io::Cursor::new(include_bytes!("../icons/badges.png"))).read_info().ok()?;
    let mut all = vec![0; read.output_buffer_size()?];
    let info = read.next_frame(&mut all).ok()?;
    if (info.width as usize, info.height as usize, info.line_size) != (10 * SIDE, 10 * SIDE, 40 * SIDE) || count == 0 {
        return None;
    }
    let (row, column) = ((count.min(100) - 1) / 10, (count.min(100) - 1) % 10);
    let from = column * SIDE * 4;
    let rows = all.chunks_exact(info.line_size).skip(row * SIDE).take(SIDE);
    let one = rows.flat_map(|line| line[from..from + SIDE * 4].to_vec()).collect();
    Some(tauri::image::Image::new_owned(one, SIDE as u32, SIDE as u32))
}

/// Windows' own mark of a file from the internet, as a browser's download has it.
pub fn from_the_internet(file: &Path) {
    let mut name = file.as_os_str().to_owned();
    name.push(":Zone.Identifier");
    let _ = std::fs::write(name, "[ZoneTransfer]\r\nZoneId=3\r\n");
}

// Notifications

/// What Windows knows the app's notifications by, in the person's own part of the registry while they are on.
const ID: &str = "computer.themachine.desktop";
const GROUP: &str = "todo";

/// Those that are there: Windows tells the program of a click as long as it keeps them.
static SHOWN: Mutex<Vec<(String, ToastNotification)>> = Mutex::new(Vec::new());

fn place() -> String {
    format!("Software\\Classes\\AppUserModelId\\{ID}")
}

/// On: Windows knows its name and icon. Off: nothing of it is left there.
pub fn notices_on(app: &AppHandle, on: bool) {
    if !on {
        if windows_registry::CURRENT_USER.open(place()).is_ok() {
            notices_clear();
            let _ = windows_registry::CURRENT_USER.remove_tree(place());
        }
        return;
    }
    let Ok(folder) = app.path().app_local_data_dir() else { return };
    let icon = folder.join("notifications.png");
    let _ = std::fs::create_dir_all(&folder).and_then(|()| std::fs::write(&icon, include_bytes!("../icons/icon.png")));
    if let Ok(key) = windows_registry::CURRENT_USER.create(place()) {
        let _ = key.set_string("DisplayName", "The Machine");
        let _ = key.set_string("IconUri", icon.to_string_lossy());
    }
}

pub fn notices_lets() -> notify::Lets {
    let setting = ToastNotificationManager::CreateToastNotifierWithId(&ID.into()).and_then(|n| n.Setting());
    match setting {
        Ok(NotificationSetting::Enabled) | Err(_) => notify::Lets::Yes, // it doesn't know the app yet
        Ok(_) => notify::Lets::No,
    }
}

pub fn notice(id: &str, title: &str, line: &str) {
    if let Err(error) = toast(id, title, line) {
        eprintln!("could not notify: {error}");
    }
}

fn toast(id: &str, title: &str, line: &str) -> Result<(), Error> {
    let page = XmlDocument::new()?;
    page.LoadXml(&HSTRING::from(xml(title, line)))?;
    let toast = ToastNotification::CreateToastNotification(&page)?;
    toast.SetTag(&id.into())?;
    toast.SetGroup(&GROUP.into())?;
    let todo = id.to_string();
    toast.Activated(&TypedEventHandler::new(move |_, _| {
        notify::opened(&todo);
        Ok(())
    }))?;
    ToastNotificationManager::CreateToastNotifierWithId(&ID.into())?.Show(&toast)?;
    let mut shown = SHOWN.lock().unwrap();
    shown.retain(|(of, _)| of != id);
    shown.push((id.into(), toast));
    if shown.len() > 40 {
        shown.remove(0);
    }
    Ok(())
}

fn xml(title: &str, line: &str) -> String {
    let plain = |text: &str| -> String {
        let text = text.chars().filter(|c| !c.is_control());
        text.map(|c| match c {
            '&' => "&amp;".into(),
            '<' => "&lt;".into(),
            '>' => "&gt;".into(),
            c => c.to_string(),
        }).collect()
    };
    let (title, line) = (plain(title), plain(line));
    format!("<toast><visual><binding template=\"ToastGeneric\"><text>{title}</text><text>{line}</text></binding></visual><audio silent=\"true\"/></toast>")
}

pub fn notice_gone(id: &str) {
    SHOWN.lock().unwrap().retain(|(of, _)| of != id);
    let _ = ToastNotificationManager::History().and_then(|h| h.RemoveGroupedTagWithId(&id.into(), &GROUP.into(), &ID.into()));
}

/// Without the program nothing answers a click on them.
pub fn notices_clear() {
    SHOWN.lock().unwrap().clear();
    let _ = ToastNotificationManager::History().and_then(|h| h.ClearWithId(&ID.into()));
}

#[cfg(test)]
mod tests {
    use super::*;


    #[test]
    fn its_words_are_only_words() {
        assert!(xml("a <b> & \"c\"\u{0}", "</text>").contains("<text>a &lt;b&gt; &amp; \"c\"</text><text>&lt;/text&gt;</text>"));
    }

    #[test]
    fn its_number_is_the_installed_apps() {
        let pixels = |n| number(n).map(|i| i.rgba().to_vec()).unwrap();
        assert!(number(0).is_none() && number(1).is_some_and(|i| (i.width(), i.height()) == (32, 32)));
        // Each its own up to 99, then 99+ for all above
        let all: Vec<_> = (1..=100).map(pixels).collect();
        assert!((1..all.len()).all(|i| all[i] != all[i - 1]));
        assert_eq!(pixels(250), all[99]);
        // A dark circle, as Windows' own badges are, around white
        let at = |p: &[u8], x: usize, y: usize| p[(y * 32 + x) * 4..(y * 32 + x) * 4 + 4].to_vec();
        for one in &all {
            assert_eq!(at(&one[..], 0, 0)[3], 0);
            assert_eq!(at(&one[..], 16, 2), vec![0x26, 0x25, 0x2D, 255]);
            assert!(one.chunks_exact(4).any(|p| p[..3].iter().all(|&c| c > 240) && p[3] == 255));
        }
    }
}
