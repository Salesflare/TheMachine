//! What is macOS' own in the windows: panels that take the keys without the program coming to the front, on every Space and
//! beside a full-screen app; places in the Mac's own points; the menu that gives the box its Command keys.
use crate::place::Rect;
use crate::{dash, later, mac_app, windows, Shared};
use block2::{Block, RcBlock};
use objc2::rc::Retained;
use objc2::runtime::{AnyClass, AnyObject, NSObjectProtocol, ProtocolObject, Sel};
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
use std::sync::Mutex;
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
    if let Some(bubble) = BUBBLE.with_borrow(Clone::clone) {
        let _ = bubble.emit_to("bubble", "over", on);
    }
}

fn native(window: &WebviewWindow) -> Option<Retained<NSWindow>> {
    MainThreadMarker::new()?;
    // SAFETY: Tauri's window is there as long as its handle, and this is the main thread.
    unsafe { Retained::retain(window.ns_window().ok()?.cast()) }
}

/// What Tauri made the windows, before they became panels.
#[cfg(feature = "store")]
static WAS: std::sync::OnceLock<&'static AnyClass> = std::sync::OnceLock::new();

/// A window that goes is Tauri's own again first (windows.rs, `again`: only in the Mac App Store's build).
#[cfg(feature = "store")]
pub fn unprepare(window: &WebviewWindow) {
    let (Some(ns), Some(was)) = (native(window), WAS.get()) else { return };
    let ours: &AnyObject = &ns;
    if ours.class() == Panel::class() || ours.class() == Robot::class() {
        // SAFETY: the class it had, which holds as much as a panel (`prepare`).
        unsafe { AnyObject::set_class(&ns, was) };
    }
}

/// What a window of the app's own becomes: the box and its to-do take the keys, the robot and its bubble don't.
fn kind(label: &str) -> &'static AnyClass {
    if matches!(label, "box" | "card") { Panel::class() } else { Robot::class() }
}

/// AppKit's own way to make a window.
#[cfg(feature = "store")]
type Init = unsafe extern "C-unwind" fn(*mut AnyObject, Sel, NSRect, NSWindowStyleMask, usize, objc2::runtime::Bool) -> *mut AnyObject;

/// What AppKit made windows with, before `panel`.
#[cfg(feature = "store")]
static INIT: std::sync::OnceLock<Init> = std::sync::OnceLock::new();

#[cfg(feature = "store")]
thread_local! {
    /// What the next window Tauri makes is (`panel`).
    static NEXT: std::cell::Cell<Option<&'static AnyClass>> = const { std::cell::Cell::new(None) };
}

/// The Mac App Store's build: one of the app's own windows (`make`, Tauri's) is a panel from the moment it is made, the
/// only moment the window system hears that a click on it leaves the program in front where it is. The other builds tell it
/// later, with a private method (`prepare`), which the store's may not use (App Review; desktop.yml checks its program).
#[cfg(feature = "store")]
pub fn panel<T>(label: &str, make: impl FnOnce() -> T) -> T {
    static ONCE: std::sync::Once = std::sync::Once::new();
    if MainThreadMarker::new().is_none() {
        return make(); // Tauri makes it on the main thread: `prepare` does what it can
    }
    ONCE.call_once(|| {
        let Some(method) = NSWindow::class().instance_method(sel!(initWithContentRect:styleMask:backing:defer:)) else { return };
        // SAFETY: AppKit's method takes and answers these, as `made` does, which calls it as it was for any other window.
        unsafe {
            let _ = INIT.set(std::mem::transmute::<objc2::runtime::Imp, Init>(method.implementation()));
            let _ = method.set_implementation(std::mem::transmute::<Init, objc2::runtime::Imp>(made));
        }
    });
    NEXT.set(Some(kind(label)));
    let window = make();
    NEXT.set(None);
    window
}

/// A window is made: Tauri's next one (`panel`) as a panel that doesn't bring the program to the front. Any other as it was.
#[cfg(feature = "store")]
unsafe extern "C-unwind" fn made(this: *mut AnyObject, cmd: Sel, frame: NSRect, style: NSWindowStyleMask, backing: usize, defer: objc2::runtime::Bool) -> *mut AnyObject {
    let Some(&init) = INIT.get() else { return std::ptr::null_mut() }; // never: it is set first
    // SAFETY: a window that is being made, of the class it was made of. A panel holds nothing more than the window Tauri
    // makes, as is compared; so all of Tauri's is there, as with `prepare`. And `unprepare` gives it Tauri's class back
    // before it goes.
    unsafe {
        let Some(was) = this.as_ref().map(AnyObject::class) else { return init(this, cmd, frame, style, backing, defer) };
        match NEXT.take() {
            Some(class) if was.name() == c"TaoWindow" && class.instance_size() <= was.instance_size() => {
                let _ = WAS.set(was);
                AnyObject::set_class(&*this, class);
                let style = style | NSWindowStyleMask::NonactivatingPanel;
                // NSPanel's own, if it has one: it comes back here, now as any other, for NSWindow's
                let theirs = class.instance_method(cmd).map_or(init, |m| std::mem::transmute::<objc2::runtime::Imp, Init>(m.implementation()));
                theirs(this, cmd, frame, style, backing, defer)
            }
            next => {
                NEXT.set(next);
                init(this, cmd, frame, style, backing, defer)
            }
        }
    }
}

pub fn prepare(window: &WebviewWindow) {
    let Some(ns) = native(window) else { return };
    let class = kind(window.label());
    if class.instance_size() == NSWindow::class().instance_size() {
        #[cfg(feature = "store")]
        if let Some(was) = Some((&*ns as &AnyObject).class()).filter(|c| *c != Panel::class() && *c != Robot::class()) {
            let _ = WAS.set(was);
        }
        // SAFETY: a panel is a window that holds nothing more than one, as was just compared, so nothing of what Tauri's
        // own holds is in its way; and the window is never destroyed (but in the Mac App Store's build, where it is
        // Tauri's own again first: `unprepare`).
        unsafe { AnyObject::set_class(&ns, class) };
        ns.setStyleMask(ns.styleMask() | NSWindowStyleMask::NonactivatingPanel);
        // The window system only hears of that when a window is made so: else a click still brings the program to the front.
        // Not in the Mac App Store's build, where it is a panel as it is made (`panel`): it uses no private method.
        #[cfg(not(feature = "store"))]
        {
            let prevents = sel!(_setPreventsActivation:);
            if ns.respondsToSelector(prevents) {
                // SAFETY: it has this method, which takes a BOOL.
                let () = unsafe { msg_send![&ns, _setPreventsActivation: true] };
            }
        }
    }
    ns.setHidesOnDeactivate(false);
    ns.setCanHide(false); // Hide is about the dashboard's window
    ns.setLevel(if window.label() == "card" { 4 } else { 3 }); // floating, and a to-do over its box
    ns.setCollectionBehavior(
        NSWindowCollectionBehavior::CanJoinAllSpaces | NSWindowCollectionBehavior::FullScreenAuxiliary
            | NSWindowCollectionBehavior::Stationary | NSWindowCollectionBehavior::IgnoresCycle,
    );
    ns.setAnimationBehavior(NSWindowAnimationBehavior::None);
    let (speaks, leaves) = (window.label() == "bubble", window.label() == "card");
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
            if leaves {
                mac_app::subclass(view, sel!(navigationDelegate), sel!(setNavigationDelegate:), LEAVES, |class| {
                    class.add_method(sel!(webView:decidePolicyForNavigationAction:decisionHandler:), decide as extern "C-unwind" fn(_, _, _, _, _));
                    mac_app::keeps(class);
                });
                mac_app::asks(view);
            }
            if let (true, Some(bubble)) = (speaks, page.ns_window().cast::<AnyObject>().as_ref()) {
                let told = NSTrackingAreaOptions::MouseEnteredAndExited | NSTrackingAreaOptions::ActiveAlways | NSTrackingAreaOptions::InVisibleRect;
                let area = NSTrackingArea::initWithRect_options_owner_userInfo(NSTrackingArea::alloc(), NSRect::ZERO, told, Some(bubble), None);
                view.addTrackingArea(&area);
            }
        }
    });
}

/// A link to a new window, before WebKit asks for one: wry asks card.rs' `on_navigation` about it as if it took the place of
/// the page, which that refuses. It goes nowhere by itself: `on_new_window` follows it, as on the other systems.
extern "C-unwind" fn decide(this: &AnyObject, _: Sel, view: &AnyObject, action: &AnyObject, answer: &Block<dyn Fn(isize)>) {
    // SAFETY: WebKit's own arguments to this method, and the class it was added to has wry's as its super class.
    unsafe {
        let frame: Option<Retained<AnyObject>> = msg_send![action, targetFrame];
        let request: Retained<AnyObject> = msg_send![action, request];
        let address: Option<Retained<AnyObject>> = msg_send![&request, URL]; // without one wry refuses it
        let file: bool = msg_send![action, shouldPerformDownload];
        if frame.is_none() && address.is_some() && !file {
            return answer.call((1,)); // WKNavigationActionPolicyAllow
        }
        if let Some(wry) = AnyClass::get(LEAVES).and_then(AnyClass::superclass) {
            let () = msg_send![super(this, wry), webView: view, decidePolicyForNavigationAction: action, decisionHandler: answer];
        }
    }
}

const LEAVES: &std::ffi::CStr = c"TheMachineLinks";


/// Shows it, the keys stay where they are.
pub fn show(window: &WebviewWindow) {
    if let Some(ns) = native(window) {
        ns.orderFrontRegardless();
    }
}

/// Something is full screen, beside the robot: then it doesn't speak.
pub static FULL: AtomicBool = AtomicBool::new(false);

/// A window on the screen: its layer, whose it is, and where.
pub struct There {
    layer: f64,
    program: f64,
    at: Rect,
}

/// The windows on the screen. Where they are macOS tells without a permission; only what they are called needs one. Not on
/// the main thread: the window system answers when it can.
pub fn there() -> Vec<There> {
    #[link(name = "CoreGraphics", kind = "framework")]
    extern "C" {
        fn CGWindowListCopyWindowInfo(which: u32, beside: u32) -> *mut NSArray<NSDictionary<NSString, AnyObject>>;
    }
    // SAFETY: a plain call: those on the screen, without the desktop's own; the list is this one's own, or nothing.
    let Some(windows) = (unsafe { Retained::from_raw(CGWindowListCopyWindowInfo(1 | 16, 0)) }) else { return Vec::new() };
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
    windows.iter().filter_map(|w| Some(There { layer: number(&w, "kCGWindowLayer")?, program: number(&w, "kCGWindowOwnerPID")?, at: at(&w)? })).collect()
}

/// A window of the program in front covers a whole screen (beside the notch, where there is one), its menu bar too.
fn covers(program: i32, there: &[There], mtm: MainThreadMarker) -> bool {
    let of = |layer: f64| there.iter().filter(move |w| w.layer == layer);
    let bars: Vec<Rect> = of(24.0).map(|w| w.at).collect(); // kCGMainMenuWindowLevel
    let mine: Vec<Rect> = of(0.0).filter(|w| w.program == f64::from(program)).map(|w| w.at).collect();
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
pub fn full_screen(there: &[There]) -> bool {
    let Some(mtm) = MainThreadMarker::new() else { return false };
    let full = NSWorkspace::sharedWorkspace().frontmostApplication().is_some_and(|front| {
        // SAFETY: it has this method, which gives a pid_t.
        covers(unsafe { msg_send![&front, processIdentifier] }, there, mtm)
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

/// The program comes to the front as macOS 14 lets it: not when the person went to another one since it was started, as
/// Tauri's own does (activateIgnoringOtherApps). A sandboxed start takes longer, and that was in time to take it back. Before
/// macOS 14 there is no such way, and it is Tauri's own.
pub fn offer_front(window: &WebviewWindow) {
    let Some(mtm) = MainThreadMarker::new() else { return };
    let here = NSApplication::sharedApplication(mtm);
    if !here.respondsToSelector(sel!(activate)) {
        let _ = window.set_focus();
        return;
    }
    // SAFETY: there since macOS 14, as just asked; it takes nothing and gives nothing.
    let () = unsafe { msg_send![&here, activate] };
    if let Some(ns) = native(window) {
        ns.makeKeyAndOrderFront(None); // in front of the program's own; of others' only once it is active
    }
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

/// The program the sign-in's links went to before: its address.
static LINKS: Mutex<Option<String>> = Mutex::new(None);

fn links_go_to(program: &NSURL) {
    let scheme = NSString::from_str(crate::signin::SCHEME);
    NSWorkspace::sharedWorkspace().setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler(program, &scheme, None);
}

/// The program's Info.plist names the sign-in's links, but the phone's app on this Mac does too. While it signs in they
/// come here. Not on the main thread: what knows the programs answers when it can. Not in the Mac App Store's build: in the
/// App Sandbox macOS keeps who gets a scheme as it is, so there the sign-in only comes back at its port (signin.rs).
pub fn take_links() {
    if cfg!(feature = "store") {
        return;
    }
    let Some(link) = NSURL::URLWithString(&NSString::from_str(&format!("{}://", crate::signin::SCHEME))) else { return };
    let own = NSBundle::mainBundle().bundleURL();
    let now = NSWorkspace::sharedWorkspace().URLForApplicationToOpenURL(&link);
    if let Some(now) = now.filter(|now| now.path() != own.path()) {
        links_go_to(&own);
        *LINKS.lock().unwrap() = now.absoluteString().map(|a| a.to_string());
    }
}

pub fn give_links() {
    let before = LINKS.lock().unwrap().take();
    if let Some(before) = before.and_then(|b| NSURL::URLWithString(&NSString::from_str(&b))) {
        links_go_to(&before);
    }
}

pub fn give_back() {
    let Some(mtm) = MainThreadMarker::new() else { return };
    let app = NSApplication::sharedApplication(mtm);
    if !app.isActive() {
        return;
    }
    let before = BEFORE.with_borrow(Clone::clone); // macOS may tell of another one meanwhile
    match before.filter(|p| !p.isTerminated()) {
        Some(before) => {
            if app.respondsToSelector(sel!(yieldActivationToApplication:)) { // since macOS 14
                app.yieldActivationToApplication(&before);
            }
            before.activateWithOptions(NSApplicationActivationOptions::empty());
        }
        None => app.deactivate(),
    }
}

/// On macOS 15 the pages of one program can wait for each other for good over their saved shaders (Metal's own lock): about
/// one start in fifty on the test runners, then the robot or the box never answers. Made anew at each start, they never did.
pub fn fresh_shaders(app: &AppHandle) {
    let Some(of) = std::env::temp_dir().parent().map(|user| user.join("C")) else { return };
    let pages = format!("com.apple.WebKit.WebContent+{}", app.config().identifier);
    let _ = std::fs::remove_dir_all(of.join(pages).join("com.apple.WebKit.WebContent/com.apple.metal"));
}

/// Once macOS has brought it to the front.
pub fn give_back_soon(app: &AppHandle) {
    let app = app.clone();
    std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(300));
        later(&app, |app| {
            if !windows::box_open(app) && !dash::visible(app) {
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

/// In the menu bar while the dashboard's window is in front; its Command keys are the box's too.
pub fn menu(app: &AppHandle) -> tauri::Result<()> {
    let item = |id, name, key| MenuItem::with_id(app, id, name, true, Some(key));
    let line = || PredefinedMenuItem::separator(app);
    // Settings and Quit are the tray's too, which hears them (main.rs)
    let own = Submenu::with_items(app, "The Machine", true, &[
        &PredefinedMenuItem::about(app, Some("About The Machine"), None)?,
        &line()?,
        &item("settings", "Settings…", "Cmd+,")?,
        &line()?,
        &PredefinedMenuItem::hide(app, Some("Hide The Machine"))?,
        &PredefinedMenuItem::hide_others(app, None)?,
        &PredefinedMenuItem::show_all(app, None)?,
        &line()?,
        &item("quit", "Quit The Machine", "Cmd+Q")?,
    ])?;
    let file = Submenu::with_items(app, "File", true, &[&item("close", "Close", "Cmd+W")?, &line()?, &item("save", "Save a Copy", "Cmd+S")?, &item("print", "Print…", "Cmd+P")?])?;
    let find = Submenu::with_items(app, "Find", true, &[&item("find", "Find…", "Cmd+F")?, &item("find-next", "Find Next", "Cmd+G")?, &item("find-before", "Find Previous", "Cmd+Shift+G")?])?;
    let edit = Submenu::with_items(app, "Edit", true, &[
        &PredefinedMenuItem::undo(app, None)?,
        &PredefinedMenuItem::redo(app, None)?,
        &line()?,
        &PredefinedMenuItem::cut(app, None)?,
        &PredefinedMenuItem::copy(app, None)?,
        &PredefinedMenuItem::paste(app, None)?,
        &PredefinedMenuItem::select_all(app, None)?,
        &line()?,
        &find,
    ])?;
    let view = Submenu::with_items(app, "View", true, &[
        &item("reload", "Reload", "Cmd+R")?,
        &item("back", "Back", "Cmd+[")?,
        &item("forward", "Forward", "Cmd+]")?,
        &line()?,
        &item("zoom", "Actual Size", "Cmd+0")?,
        &item("zoom-in", "Zoom In", "Cmd+=")?,
        &item("zoom-out", "Zoom Out", "Cmd+-")?,
        &line()?,
        &PredefinedMenuItem::fullscreen(app, None)?,
    ])?;
    let window = Submenu::with_items(app, "Window", true, &[
        &PredefinedMenuItem::minimize(app, None)?,
        &PredefinedMenuItem::maximize(app, Some("Zoom"))?,
        &line()?,
        &item("window", "The Machine", "Cmd+1")?,
    ])?;
    app.set_menu(Menu::with_items(app, &[&own, &file, &edit, &view, &window])?)?;
    app.on_menu_event(|app, event| {
        let id = event.id.as_ref().to_string();
        later(app, move |app| match id.as_str() {
            "close" => close(app),
            "save" => dash::save_copy(app),
            "print" => {
                if let Some(window) = dash::in_front(app) {
                    let _ = window.print();
                }
            }
            "find" => mac_app::find_next(0),
            "find-next" => mac_app::find_next(1),
            "find-before" => mac_app::find_next(-1),
            "reload" => dash::reload(app),
            "back" => dash::back(app, false),
            "forward" => dash::back(app, true),
            "zoom" => dash::zoom(app, 0),
            "zoom-in" => dash::zoom(app, 1),
            "zoom-out" => dash::zoom(app, -1),
            "window" => dash::show(app, ""),
            _ => {}
        });
    });
    Ok(())
}

/// Cmd+W: what has the keys. The box, else the window in front.
fn close(app: &AppHandle) {
    if windows::box_open(app) {
        return windows::close_box(app);
    }
    if let Some(window) = app.get_webview_window("settings").filter(|w| w.is_focused().unwrap_or(false)) {
        let _ = window.hide();
    } else if let Some(window) = dash::in_front(app) {
        if window.label() == dash::LABEL { dash::close(app) } else { dash::close_file(app, window.label()) }
    }
}
