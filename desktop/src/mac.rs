//! What is macOS' own in the windows: panels that take the keys without the program coming to the front, on every Space and
//! beside a full-screen app; places in the Mac's own points; the menu that gives the box its Command keys.
use crate::place::Rect;
use crate::{later, windows, Shared};
use block2::RcBlock;
use objc2::rc::Retained;
use objc2::runtime::{AnyObject, NSObjectProtocol, ProtocolObject};
use objc2::{class, define_class, msg_send, sel, AnyThread, ClassType, MainThreadMarker};
use objc2_app_kit::{
    NSApplication, NSApplicationActivationOptions, NSApplicationDidChangeScreenParametersNotification, 
    NSEvent, NSPanel, NSResponder, NSRunningApplication, NSScreen, NSTrackingArea, NSTrackingAreaOptions, NSView, NSWindow,
    NSWindowAnimationBehavior, NSWindowCollectionBehavior, NSWindowDidBecomeKeyNotification, NSWindowDidChangeOcclusionStateNotification,
    NSWindowDidResignKeyNotification, NSWindowStyleMask, NSWorkspace, NSWorkspaceDidActivateApplicationNotification,
};
use objc2_foundation::{NSArray, NSBundle, NSDictionary, NSNotification, NSNotificationCenter, NSNotificationName, NSNumber, NSPoint, NSRect, NSSize, NSString, NSURL};
use std::cell::RefCell;
use std::ptr::NonNull;
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::Duration;
use tauri::menu::{Menu, MenuItem, PredefinedMenuItem, Submenu};
use tauri::{AppHandle, Emitter, Manager, WebviewWindow};

// Neither holds anything of its own: Tauri's window becomes one, as it is.
define_class!(
    /// The robot and its bubble: a click on them leaves the keys where they are.
    #[unsafe(super(NSPanel, NSWindow, NSResponder))]
    #[name = "TheMachineRobot"]
    struct Robot;

    impl Robot {
        #[unsafe(method(canBecomeKeyWindow))]
        fn can_become_key(&self) -> bool {
            false
        }

        #[unsafe(method(canBecomeMainWindow))]
        fn can_become_main(&self) -> bool {
            false
        }

        #[unsafe(method(mouseEntered:))]
        fn entered(&self, _event: &NSEvent) {
            over(true);
        }

        #[unsafe(method(mouseExited:))]
        fn exited(&self, _event: &NSEvent) {
            over(false);
        }
    }
);

define_class!(
    /// The box and the to-do in it: written in, while the program that was in front stays so.
    #[unsafe(super(NSPanel, NSWindow, NSResponder))]
    #[name = "TheMachineBox"]
    struct Panel;

    impl Panel {
        #[unsafe(method(canBecomeKeyWindow))]
        fn can_become_key(&self) -> bool {
            true
        }

        #[unsafe(method(canBecomeMainWindow))]
        fn can_become_main(&self) -> bool {
            false
        }
    }
);

thread_local! {
    static BUBBLE: RefCell<Option<WebviewWindow>> = const { RefCell::new(None) };
}

/// The pointer came over the bubble, or left it. Its page doesn't know: WebKit follows the pointer only where the keys are.
fn over(on: bool) {
    BUBBLE.with_borrow(|bubble| {
        if let Some(bubble) = bubble {
            let _ = bubble.emit_to("bubble", "over", on);
        }
    });
}

fn native(window: &WebviewWindow) -> Option<Retained<NSWindow>> {
    MainThreadMarker::new()?;
    // SAFETY: Tauri's window is there as long as its handle, and this is the main thread.
    unsafe { Retained::retain(window.ns_window().ok()?.cast()) }
}

pub fn prepare(window: &WebviewWindow) {
    let Some(ns) = native(window) else { return };
    let keys = matches!(window.label(), "box" | "card");
    let class = if keys { Panel::class() } else { Robot::class() };
    if class.instance_size() == NSWindow::class().instance_size() {
        // SAFETY: a panel is a window that holds nothing more than one, as was just compared, so nothing of what Tauri's
        // own holds is in its way; and the window is never destroyed.
        unsafe { AnyObject::set_class(&ns, class) };
        ns.setStyleMask(ns.styleMask() | NSWindowStyleMask::NonactivatingPanel);
        // The window system only hears of that when a window is made so: else a click still brings the program to the front
        let prevents = sel!(_setPreventsActivation:);
        if ns.respondsToSelector(prevents) {
            // SAFETY: it has this method, which takes a BOOL.
            let () = unsafe { msg_send![&ns, _setPreventsActivation: true] };
        }
    }
    ns.setHidesOnDeactivate(false);
    ns.setLevel(if window.label() == "card" { 4 } else { 3 }); // floating, and a to-do over its box
    ns.setCollectionBehavior(
        NSWindowCollectionBehavior::CanJoinAllSpaces | NSWindowCollectionBehavior::FullScreenAuxiliary
            | NSWindowCollectionBehavior::Stationary | NSWindowCollectionBehavior::IgnoresCycle,
    );
    ns.setAnimationBehavior(NSWindowAnimationBehavior::None);
    let speaks = window.label() == "bubble";
    if speaks {
        BUBBLE.set(Some(window.clone()));
    }
    let _ = window.with_webview(move |page| {
        // SAFETY: the page's own view, and what it has. WebKit has the setting since macOS 10.12.3: the Tab key goes to
        // buttons too.
        unsafe {
            let Some(view) = page.inner().cast::<NSView>().as_ref() else { return };
            let configuration: Retained<AnyObject> = msg_send![view, configuration];
            let preferences: Retained<AnyObject> = msg_send![&configuration, preferences];
            let () = msg_send![&preferences, setTabFocusesLinks: true];
            if let (true, Some(bubble)) = (speaks, page.ns_window().cast::<AnyObject>().as_ref()) {
                let told = NSTrackingAreaOptions::MouseEnteredAndExited | NSTrackingAreaOptions::ActiveAlways | NSTrackingAreaOptions::InVisibleRect;
                let area = NSTrackingArea::initWithRect_options_owner_userInfo(NSTrackingArea::alloc(), NSRect::ZERO, told, Some(bubble), None);
                view.addTrackingArea(&area);
            }
        }
    });
}

/// Shows it, the keys stay where they are.
pub fn show(window: &WebviewWindow) {
    if let Some(ns) = native(window) {
        ns.orderFrontRegardless();
    }
}

/// Something is full screen, beside the robot: then it doesn't speak.
pub static FULL: AtomicBool = AtomicBool::new(false);

/// A window of the program in front covers a whole screen (beside the notch, where there is one), its menu bar too. Where
/// windows are macOS tells without a permission; only what they are called needs one.
fn covers(program: i32, mtm: MainThreadMarker) -> bool {
    #[link(name = "CoreGraphics", kind = "framework")]
    extern "C" {
        fn CGWindowListCopyWindowInfo(which: u32, beside: u32) -> *mut NSArray<NSDictionary<NSString, AnyObject>>;
    }
    // SAFETY: a plain call: those on the screen, without the desktop's own; the list is this one's own, or nothing.
    let Some(windows) = (unsafe { Retained::from_raw(CGWindowListCopyWindowInfo(1 | 16, 0)) }) else { return false };
    let number = |of: &NSDictionary<NSString, AnyObject>, name: &str| {
        let found = of.objectForKey(&NSString::from_str(name))?;
        found.downcast_ref::<NSNumber>().map(|n| n.doubleValue())
    };
    let at = |w: &NSDictionary<NSString, AnyObject>| {
        let found = w.objectForKey(&NSString::from_str("kCGWindowBounds"))?;
        // SAFETY: the bounds are a dictionary of numbers, by their names.
        let of = unsafe { &*Retained::as_ptr(&found).cast::<NSDictionary<NSString, AnyObject>>() };
        Some(Rect { x: number(of, "X")?, y: number(of, "Y")?, w: number(of, "Width")?, h: number(of, "Height")? })
    };
    let of = |layer: f64| windows.iter().filter(move |w| number(w, "kCGWindowLayer") == Some(layer));
    let bars: Vec<Rect> = of(24.0).filter_map(|w| at(&w)).collect(); // kCGMainMenuWindowLevel
    let mine: Vec<Rect> = of(0.0).filter(|w| number(w, "kCGWindowOwnerPID") == Some(f64::from(program))).filter_map(|w| at(&w)).collect();
    let top = top(mtm);
    NSScreen::screens(mtm).iter().any(|screen| {
        let f = screen.frame();
        let (x, y, notch) = (f.origin.x, top - f.origin.y - f.size.height, screen.safeAreaInsets().top);
        let covered = mine.iter().any(|w| {
            let end = y + f.size.height;
            w.x <= x && w.x + w.w >= x + f.size.width && w.y <= y + notch && w.y + w.h >= end
        });
        covered && !bars.iter().any(|b| b.x < x + f.size.width && b.x + b.w > x && b.y < y + 1.0 && b.y + b.h > y)
    })
}

/// Whether that changed.
pub fn full_screen() -> bool {
    let Some(mtm) = MainThreadMarker::new() else { return false };
    let full = NSWorkspace::sharedWorkspace().frontmostApplication().is_some_and(|front| {
        // SAFETY: it has this method, which gives a pid_t.
        covers(unsafe { msg_send![&front, processIdentifier] }, mtm)
    });
    FULL.swap(full, Ordering::Relaxed) != full
}

/// Shows it, with the keys in its page. Tauri's own also brings the program to the front.
pub fn focus(window: &WebviewWindow) {
    let Some(ns) = native(window) else { return };
    ns.orderFrontRegardless();
    ns.makeKeyWindow();
    let _ = window.with_webview(move |page| {
        // SAFETY: the page's own view, and the window it is in.
        unsafe {
            let (view, ns) = (page.inner().cast::<NSView>().as_ref(), page.ns_window().cast::<NSWindow>().as_ref());
            if let Some(ns) = ns {
                ns.makeFirstResponder(view.map(|v| v.as_super()));
            }
        }
    });
}

/// The main screen's height: macOS counts from its bottom left corner, the rest of the program from its top left.
fn top(mtm: MainThreadMarker) -> f64 {
    NSScreen::screens(mtm).firstObject().map_or(0.0, |s| s.frame().size.height)
}

pub fn put(window: &WebviewWindow, at: Rect) {
    let (Some(ns), Some(mtm)) = (native(window), MainThreadMarker::new()) else { return };
    let to = NSRect::new(NSPoint::new(at.x.round(), (top(mtm) - at.y - at.h).round()), NSSize::new(at.w.round(), at.h.round()));
    if ns.frame() != to {
        ns.setFrame_display(to, true);
    }
}

/// Each screen's name and what the menu bar and the Dock leave of it, the main one first.
pub fn screens() -> Vec<(String, Rect)> {
    let Some(mtm) = MainThreadMarker::new() else { return Vec::new() };
    let top = top(mtm);
    let of = |s: Retained<NSScreen>| {
        let free = s.visibleFrame();
        let area = Rect { x: free.origin.x, y: top - free.origin.y - free.size.height, w: free.size.width, h: free.size.height };
        (s.localizedName().to_string(), area)
    };
    NSScreen::screens(mtm).iter().map(of).collect()
}

pub fn pointer() -> Option<(f64, f64)> {
    let mtm = MainThreadMarker::new()?;
    let at = NSEvent::mouseLocation();
    Some((at.x, top(mtm) - at.y))
}

/// Runs this on the main thread when it is told so, as long as the program runs.
pub fn on(center: &NSNotificationCenter, name: &NSNotificationName, run: impl Fn() + 'static) {
    let block = RcBlock::new(move |_: NonNull<NSNotification>| run());
    // SAFETY: nothing but this thread runs the block, as the notices asked for come on the main thread.
    let told: Retained<ProtocolObject<dyn NSObjectProtocol>> = unsafe { center.addObserverForName_object_queue_usingBlock(Some(name), None, None, &block) };
    std::mem::forget(told);
}

thread_local! {
    /// The program that was in front before this one.
    static BEFORE: RefCell<Option<Retained<NSRunningApplication>>> = const { RefCell::new(None) };
}

/// macOS brings the program to the front when it is opened again or a sign-in comes back, and choosing a file needs that.
/// Once nothing here has the keys, the program that was in front is again.
pub fn follow_front(app: &AppHandle) {
    let seen = || {
        let front = NSWorkspace::sharedWorkspace().frontmostApplication();
        if let Some(front) = front.filter(|p| *p != NSRunningApplication::currentApplication()) {
            BEFORE.set(Some(front));
        }
    };
    seen();
    // SAFETY: constants of AppKit's.
    let (program, names) = unsafe {
        (NSWorkspaceDidActivateApplicationNotification,
         [NSWindowDidChangeOcclusionStateNotification, NSWindowDidBecomeKeyNotification, NSWindowDidResignKeyNotification])
    };
    on(&NSWorkspace::sharedWorkspace().notificationCenter(), program, seen);
    for name in names {
        let app = app.clone();
        on(&NSNotificationCenter::defaultCenter(), name, move || choosing(&app));
    }
}

/// macOS' own window to choose a file: it gets the keys while it is there, and then the box has them again.
fn choosing(app: &AppHandle) {
    static CHOOSING: AtomicBool = AtomicBool::new(false);
    let Some(mtm) = MainThreadMarker::new() else { return };
    let here = NSApplication::sharedApplication(mtm);
    let panel = here.windows().iter().find(|w| w.isVisible() && w.isKindOfClass(class!(NSSavePanel)));
    if CHOOSING.swap(panel.is_some(), Ordering::Relaxed) == panel.is_some() {
        return;
    }
    if let Some(panel) = panel {
        #[allow(deprecated)] // the newer one only asks, and it may be told no
        here.activateIgnoringOtherApps(true);
        panel.makeKeyAndOrderFront(None);
    } else if let (true, Some(window)) = (windows::box_open(app), app.get_webview_window("box")) {
        focus(&window);
    }
}

thread_local! {
    /// The program the sign-in's links went to before.
    static LINKS: RefCell<Option<Retained<NSURL>>> = const { RefCell::new(None) };
}

fn links_go_to(program: &NSURL) {
    let scheme = NSString::from_str(crate::signin::SCHEME);
    NSWorkspace::sharedWorkspace().setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler(program, &scheme, None);
}

/// The program's Info.plist names the sign-in's links, but the phone's app on this Mac does too. While it signs in they
/// come here.
pub fn take_links() {
    let Some(link) = NSURL::URLWithString(&NSString::from_str(&format!("{}://", crate::signin::SCHEME))) else { return };
    let own = NSBundle::mainBundle().bundleURL();
    let now = NSWorkspace::sharedWorkspace().URLForApplicationToOpenURL(&link);
    if let Some(now) = now.filter(|now| now.path() != own.path()) {
        links_go_to(&own);
        LINKS.set(Some(now));
    }
}

pub fn give_links() {
    if let Some(before) = LINKS.take() {
        links_go_to(&before);
    }
}

pub fn give_back() {
    let Some(mtm) = MainThreadMarker::new() else { return };
    let app = NSApplication::sharedApplication(mtm);
    if !app.isActive() {
        return;
    }
    BEFORE.with_borrow(|before| match before.as_ref().filter(|p| !p.isTerminated()) {
        Some(before) => {
            if app.respondsToSelector(sel!(yieldActivationToApplication:)) { // since macOS 14
                app.yieldActivationToApplication(before);
            }
            before.activateWithOptions(NSApplicationActivationOptions::empty());
        }
        None => app.deactivate(),
    });
}

/// Once macOS has brought it to the front.
pub fn give_back_soon(app: &AppHandle) {
    let app = app.clone();
    std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(300));
        later(&app, |app| {
            if !windows::box_open(app) {
                give_back();
            }
        });
    });
}

/// A drop brings the program to the front too: what it came from is again, and the box keeps the keys.
pub fn dropped(app: &AppHandle) {
    let app = app.clone();
    std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(300));
        later(&app, |_| give_back());
        std::thread::sleep(Duration::from_millis(300));
        later(&app, |app| {
            if let (true, Some(window)) = (windows::box_open(app), app.get_webview_window("box")) {
                focus(&window);
            }
        });
    });
}

/// A screen that comes or goes, another resolution, the Dock elsewhere: the robot goes back to its corner.
pub fn follow_screens(app: &AppHandle) {
    let app = app.clone();
    // SAFETY: a constant of AppKit's.
    let changed = unsafe { NSApplicationDidChangeScreenParametersNotification };
    on(&NSNotificationCenter::defaultCenter(), changed, move || {
        let app = app.clone();
        std::thread::spawn(move || {
            for wait in [100, 1500] { // macOS moves windows too, meanwhile
                std::thread::sleep(Duration::from_millis(wait));
                later(&app, |app| {
                    if app.state::<Shared>().grab.lock().unwrap().is_none() {
                        windows::place(app);
                    }
                });
            }
        });
    });
}

/// Not in the menu bar while another program is in front, but its Command keys are the box's: Copy and Paste, Close, Quit.
pub fn menu(app: &AppHandle) -> tauri::Result<()> {
    let item = |id, name, key| MenuItem::with_id(app, id, name, true, Some(key)); // Quit is the tray's too, which hears it
    let own = Submenu::with_items(app, "The Machine", true, &[&item("close", "Close", "Cmd+W")?, &item("quit", "Quit The Machine", "Cmd+Q")?])?;
    let edit = Submenu::with_items(app, "Edit", true, &[
        &PredefinedMenuItem::undo(app, None)?,
        &PredefinedMenuItem::redo(app, None)?,
        &PredefinedMenuItem::separator(app)?,
        &PredefinedMenuItem::cut(app, None)?,
        &PredefinedMenuItem::copy(app, None)?,
        &PredefinedMenuItem::paste(app, None)?,
        &PredefinedMenuItem::select_all(app, None)?,
    ])?;
    app.set_menu(Menu::with_items(app, &[&own, &edit])?)?;
    app.on_menu_event(|app, event| {
        if event.id.as_ref() == "close" {
            later(app, windows::close_box);
        }
    });
    Ok(())
}

/// A sandbox build's pages, for smoke/mac.py: a page's label on the first line, what to ask it after. WebKit has nothing
/// like this of its own.
#[cfg(feature = "sandbox")]
pub fn debug(app: &AppHandle) {
    use std::io::{Read, Write};
    let Some(port) = std::env::var("MACHINE_SANDBOX_DEBUG").ok().and_then(|p| p.parse::<u16>().ok()) else { return };
    let Ok(listener) = std::net::TcpListener::bind(("127.0.0.1", port)) else { return };
    let app = app.clone();
    std::thread::spawn(move || {
        for mut stream in listener.incoming().flatten() {
            let mut asked = String::new();
            if stream.read_to_string(&mut asked).is_err() {
                continue;
            }
            let (label, script) = asked.split_once('\n').unwrap_or_default();
            let (tell, told) = std::sync::mpsc::channel();
            let found = app.get_webview_window(label).map(|w| w.eval_with_callback(script, move |answer| { let _ = tell.send(answer); }));
            let answer = match found {
                Some(Ok(())) => told.recv_timeout(Duration::from_secs(5)).unwrap_or_default(),
                _ => String::new(),
            };
            let _ = stream.write_all(answer.as_bytes());
        }
    });
}
