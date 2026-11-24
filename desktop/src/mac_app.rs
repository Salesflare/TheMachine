//! What is macOS' own in the dashboard's window: what a page asks (alert, confirm, prompt), links and frames, finding in the
//! page, the title bar in the page's color, and starting at login and notifications.
use crate::{dash, login, notify};
use block2::{Block, RcBlock};
use objc2::rc::Retained;
use objc2::runtime::{AnyClass, AnyObject, Bool, ClassBuilder, NSObject, NSObjectProtocol, ProtocolObject, Sel};
use objc2::{class, define_class, msg_send, sel, AnyThread, DefinedClass, MainThreadMarker, MainThreadOnly, Message};
use objc2_app_kit::{
    NSAlert, NSAlertFirstButtonReturn, NSApplication, NSAutoresizingMaskOptions, NSButton, NSColor, NSEventModifierFlags, NSModalResponse, NSTextField, NSTitlebarSeparatorStyle, NSView, NSWindow,
    NSWindowTitleVisibility,
};
use objc2_foundation::{ns_string, NSArray, NSData, NSDictionary, NSError, NSObjectNSKeyValueObserverRegistration, NSPoint, NSRect, NSSize, NSString};
use objc2_user_notifications::{
    UNAuthorizationOptions, UNAuthorizationStatus, UNMutableNotificationContent, UNNotification, UNNotificationPresentationOptions, UNNotificationRequest, UNNotificationResponse,
    UNUserNotificationCenter, UNUserNotificationCenterDelegate,
};
use std::cell::RefCell;
use std::path::Path;
use std::sync::atomic::{AtomicU8, Ordering};
use std::sync::OnceLock;
use tauri::WebviewWindow;

/// The dashboard's window, or one with a file.
pub fn prepare(window: &WebviewWindow) {
    let dashboard = window.label() == dash::LABEL;
    let _ = window.with_webview(move |page| {
        let Some(mtm) = MainThreadMarker::new() else { return };
        // SAFETY: the page's own view and its window, on the main thread.
        unsafe {
            let (Some(view), Some(ns)) = (page.inner().cast::<NSView>().as_ref(), page.ns_window().cast::<NSWindow>().as_ref()) else { return };
            subclass(view, sel!(navigationDelegate), sel!(setNavigationDelegate:), c"TheMachineFrames", |class| {
                class.add_method(sel!(webView:decidePolicyForNavigationAction:decisionHandler:), decide as extern "C-unwind" fn(_, _, _, _, _));
                keeps(class);
            });
            ns.setTabbingMode(objc2_app_kit::NSWindowTabbingMode::Disallowed);
            ns.setTitlebarAppearsTransparent(dashboard);
            if dashboard {
                asks(view);
                shade(view, ns);
                find(view, mtm);
            }
        }
    });
}

/// wry's own object for this, made a kind of itself that has more methods. It holds nothing more. WebKit is given it again, as
/// it only looks then which methods there are.
///
/// # Safety
/// On the main thread, for a WKWebView; the methods fit their names.
pub unsafe fn subclass(view: &NSView, which: Sel, set: Sel, name: &std::ffi::CStr, methods: impl FnOnce(&mut ClassBuilder)) {
    let delegate: Option<Retained<AnyObject>> = msg_send![view, performSelector: which];
    let Some(delegate) = delegate else { return };
    let class = AnyClass::get(name).unwrap_or_else(|| {
        let mut class = ClassBuilder::new(name, delegate.class()).expect("a name of its own");
        methods(&mut class);
        class.register()
    });
    if class.superclass() == Some(delegate.class()) {
        AnyObject::set_class(&delegate, class);
        let none: Option<&AnyObject> = None;
        let () = msg_send![view, performSelectorOnMainThread: set, withObject: none, waitUntilDone: true];
        let () = msg_send![view, performSelectorOnMainThread: set, withObject: &*delegate, waitUntilDone: true];
    }
}

/// wry asks `on_navigation` about frames too, which are no place to go: they load as in a browser. And a link to a new window
/// goes to `on_new_window` only.
extern "C-unwind" fn decide(this: &AnyObject, _: Sel, view: &AnyObject, action: &AnyObject, answer: &Block<dyn Fn(isize)>) {
    const ALLOW: isize = 1;
    // SAFETY: WebKit's own arguments to this method, and the class it was added to has wry's as its super class.
    unsafe {
        let frame: Option<Retained<AnyObject>> = msg_send![action, targetFrame];
        let request: Retained<AnyObject> = msg_send![action, request];
        let address: Option<Retained<AnyObject>> = msg_send![&request, URL];
        let file: bool = msg_send![action, shouldPerformDownload];
        if let (Some(address), false) = (address, file) {
            let scheme: Option<Retained<NSString>> = msg_send![&address, scheme];
            let web = scheme.is_some_and(|s| matches!(s.to_string().to_lowercase().as_str(), "https" | "http" | "about" | "blob" | "data"));
            let main = frame.as_ref().is_some_and(|f| msg_send![f, isMainFrame]);
            if frame.is_none() || web && !main {
                return answer.call((ALLOW,));
            }
        }
        if let Some(wry) = AnyClass::get(c"TheMachineFrames").and_then(AnyClass::superclass) {
            let () = msg_send![super(this, wry), webView: view, decidePolicyForNavigationAction: action, decisionHandler: answer];
        }
    }
}

// The pages' keys. The dashboard encrypts what it keeps here with a key of its own, and WebKit keeps that under one in the
// login keychain: up to macOS 15 it asks for it on the main thread, and as long as macOS asks the person about the keychain
// (it is locked, or another build made the key) nothing here answers. So it gets one that is kept beside the session.

static KEY: OnceLock<[u8; 16]> = OnceLock::new();

pub fn own_key(hex: &str) {
    if let Some(key) = key(hex) {
        let _ = KEY.set(key);
    }
}

pub fn key(hex: &str) -> Option<[u8; 16]> {
    u128::from_str_radix(hex, 16).ok().filter(|_| hex.len() == 32).map(u128::to_be_bytes)
}

/// Without a key it answers none, and then the page keeps nothing.
pub fn keeps(class: &mut ClassBuilder) {
    if cfg!(feature = "sandbox") && std::env::var_os("MACHINE_SANDBOX_KEYCHAIN").is_some() {
        return; // as it was, for smoke/hangs.py
    }
    // SAFETY: the method takes the view and gives an NSData or nothing.
    unsafe { class.add_method(sel!(_webCryptoMasterKeyForWebView:), master_key as extern "C-unwind" fn(_, _, _) -> _) };
}

extern "C-unwind" fn master_key(_: &AnyObject, _: Sel, _: &AnyObject) -> *mut NSData {
    KEY.get().map_or(std::ptr::null_mut(), |key| Retained::autorelease_return(NSData::with_bytes(key)))
}

/// The process of a window's page, where macOS tells.
pub fn process(window: &WebviewWindow) -> Option<u32> {
    let (tell, told) = std::sync::mpsc::channel();
    let _ = window.with_webview(move |page| {
        // SAFETY: the page's own view, asked for what it has: a pid_t.
        let pid = unsafe {
            page.inner().cast::<NSView>().as_ref().filter(|v| v.respondsToSelector(sel!(_webProcessIdentifier))).map(|view| {
                let pid: i32 = msg_send![view, _webProcessIdentifier];
                pid
            })
        };
        let _ = tell.send(pid);
    });
    told.recv_timeout(std::time::Duration::from_secs(5)).ok().flatten().and_then(|pid| u32::try_from(pid).ok()).filter(|pid| *pid > 0)
}

/// A session's cookies, for the page at this host. wry's own waits for each, on the main thread.
pub fn cookies(window: &WebviewWindow, cookies: Vec<(String, String)>, host: String, secure: bool, done: impl Fn() + Send + 'static) {
    let _ = window.with_webview(move |page| {
        // SAFETY: the page's own view, on the main thread; a cookie's properties are texts by these names.
        unsafe {
            let Some(view) = page.inner().cast::<NSView>().as_ref() else { return };
            let configuration: Retained<AnyObject> = msg_send![view, configuration];
            let data: Retained<AnyObject> = msg_send![&configuration, websiteDataStore];
            let store: Retained<AnyObject> = msg_send![&data, httpCookieStore];
            let left = std::rc::Rc::new((std::cell::Cell::new(cookies.len()), done));
            for (name, value) in cookies {
                let mut of = vec![("Name", name), ("Value", value), ("Domain", host.clone()), ("Path", "/".into()), ("HttpOnly", "TRUE".into())];
                if secure {
                    of.push(("Secure", "TRUE".into()));
                }
                let names: Vec<_> = of.iter().map(|(n, _)| NSString::from_str(n)).collect();
                let values: Vec<_> = of.iter().map(|(_, v)| NSString::from_str(v)).collect();
                let names: Vec<&NSString> = names.iter().map(|n| &**n).collect();
                let of = NSDictionary::<NSString, NSString>::from_retained_objects(&names, &values);
                let cookie: Option<Retained<AnyObject>> = msg_send![class!(NSHTTPCookie), cookieWithProperties: &*of];
                let left = left.clone();
                let one = move || {
                    left.0.set(left.0.get() - 1);
                    if left.0.get() == 0 {
                        (left.1)();
                    }
                };
                match cookie {
                    Some(cookie) => {
                        let one = RcBlock::new(one);
                        let () = msg_send![&store, setCookie: &*cookie, completionHandler: &*one];
                    }
                    None => one(),
                }
            }
        }
    });
}

// What a page asks

/// alert(), confirm() and prompt(): WebKit leaves those to the app, and without it answers no at once.
///
/// # Safety
/// On the main thread, for a WKWebView.
pub unsafe fn asks(view: &NSView) {
    subclass(view, sel!(UIDelegate), sel!(setUIDelegate:), c"TheMachineAsks", |class| {
        class.add_method(sel!(webView:runJavaScriptAlertPanelWithMessage:initiatedByFrame:completionHandler:), alert as extern "C-unwind" fn(_, _, _, _, _, _));
        class.add_method(sel!(webView:runJavaScriptConfirmPanelWithMessage:initiatedByFrame:completionHandler:), confirm as extern "C-unwind" fn(_, _, _, _, _, _));
        class.add_method(
            sel!(webView:runJavaScriptTextInputPanelWithPrompt:defaultText:initiatedByFrame:completionHandler:),
            prompt as extern "C-unwind" fn(_, _, _, _, _, _, _),
        );
    });
}

extern "C-unwind" fn alert(_: &AnyObject, _: Sel, view: &NSView, message: &NSString, _: &AnyObject, answer: &Block<dyn Fn()>) {
    let answer = answer.copy();
    ask(view, message, None, false, move |_, _| answer.call(()));
}

extern "C-unwind" fn confirm(_: &AnyObject, _: Sel, view: &NSView, message: &NSString, _: &AnyObject, answer: &Block<dyn Fn(Bool)>) {
    let answer = answer.copy();
    ask(view, message, None, true, move |yes, _| answer.call((Bool::new(yes),)));
}

extern "C-unwind" fn prompt(_: &AnyObject, _: Sel, view: &NSView, message: &NSString, usual: Option<&NSString>, _: &AnyObject, answer: &Block<dyn Fn(*mut NSString)>) {
    let answer = answer.copy();
    let usual = usual.map(|u| u.to_string()).unwrap_or_default();
    ask(view, message, Some(usual), true, move |yes, text| {
        let text = text.filter(|_| yes);
        answer.call((text.as_ref().map_or(std::ptr::null_mut(), |t| Retained::as_ptr(t).cast_mut()),));
    });
}

/// A sheet on the page's window. WebKit waits for the answer, which has to come.
fn ask(view: &NSView, message: &NSString, field: Option<String>, cancel: bool, done: impl Fn(bool, Option<Retained<NSString>>) + 'static) {
    let (Some(mtm), Some(window)) = (MainThreadMarker::new(), view.window()) else { return done(false, None) };
    if !window.isVisible() || window.attachedSheet().is_some() {
        return done(false, None);
    }
    let alert = NSAlert::new(mtm);
    let message = message.to_string();
    let (head, rest) = message.trim().split_once('\n').unwrap_or((message.trim(), ""));
    // A long one reads better as the smaller text
    let (head, rest) = if head.chars().count() > 120 { ("", message.trim()) } else { (head, rest.trim()) };
    alert.setMessageText(&NSString::from_str(if head.is_empty() { "The Machine" } else { head }));
    alert.setInformativeText(&NSString::from_str(rest));
    alert.addButtonWithTitle(ns_string!("OK"));
    if cancel {
        alert.addButtonWithTitle(ns_string!("Cancel")); // Escape is its key
    }
    let text = field.map(|usual| {
        let text = NSTextField::textFieldWithString(&NSString::from_str(&usual), mtm);
        text.setFrame(NSRect::new(NSPoint::ZERO, NSSize::new(260.0, 24.0)));
        alert.setAccessoryView(Some(&text));
        alert.window().setInitialFirstResponder(Some(&text));
        text
    });
    let kept = alert.clone();
    let ended = RcBlock::new(move |button: NSModalResponse| {
        let _ = &kept;
        done(button == NSAlertFirstButtonReturn, text.as_ref().map(|t| t.stringValue()));
    });
    alert.beginSheetModalForWindow_completionHandler(&window, Some(&ended));
}

// The title bar

struct Shaded {
    window: Retained<NSWindow>,
    view: Retained<NSView>,
}

define_class!(
    // SAFETY: NSObject asks nothing of what is made from it.
    #[unsafe(super(NSObject))]
    #[thread_kind = MainThreadOnly]
    #[name = "TheMachineShade"]
    #[ivars = Shaded]
    struct Shade;

    unsafe impl NSObjectProtocol for Shade {}

    impl Shade {
        #[unsafe(method(observeValueForKeyPath:ofObject:change:context:))]
        fn changed(&self, _key: Option<&NSString>, _of: Option<&AnyObject>, _change: Option<&NSDictionary>, _context: *mut std::ffi::c_void) {
            self.follow();
        }
    }
);

impl Shade {
    fn follow(&self) {
        let Shaded { window, view } = self.ivars();
        // SAFETY: WKWebView has it since macOS 12.
        let color: Option<Retained<NSColor>> = unsafe { msg_send![view, underPageBackgroundColor] };
        if let Some(color) = color.filter(|c| c.alphaComponent() > 0.9) {
            window.setBackgroundColor(Some(&color));
        }
    }
}

/// The title bar has the page's own color, in light and dark, also when the dashboard's theme isn't the system's.
///
/// # Safety
/// On the main thread, for a WKWebView in this window, which is there as long as the program.
unsafe fn shade(view: &NSView, window: &NSWindow) {
    window.setTitleVisibility(NSWindowTitleVisibility::Hidden);
    window.setTitlebarSeparatorStyle(NSTitlebarSeparatorStyle::None);
    let Some(mtm) = MainThreadMarker::new() else { return };
    let own = mtm.alloc::<Shade>().set_ivars(Shaded { window: window.retain(), view: view.retain() });
    let own: Retained<Shade> = msg_send![super(own), init];
    let key = ns_string!("underPageBackgroundColor");
    view.addObserver_forKeyPath_options_context(&own, key, objc2_foundation::NSKeyValueObservingOptions::empty(), std::ptr::null_mut());
    own.follow();
    std::mem::forget(own);
}

// Find

struct Bar {
    page: Retained<NSView>,
    bar: Retained<NSView>,
    field: Retained<NSTextField>,
}

define_class!(
    // SAFETY: NSObject asks nothing of what is made from it.
    #[unsafe(super(NSObject))]
    #[thread_kind = MainThreadOnly]
    #[name = "TheMachineFind"]
    #[ivars = Bar]
    struct Find;

    unsafe impl NSObjectProtocol for Find {}

    // The field's
    impl Find {
        #[unsafe(method(controlTextDidChange:))]
        fn typed(&self, _note: &AnyObject) {
            self.look(0);
        }

        #[unsafe(method(control:textView:doCommandBySelector:))]
        fn command(&self, _field: &AnyObject, _text: &AnyObject, what: Sel) -> Bool {
            if what == sel!(insertNewline:) {
                let shift = NSApplication::sharedApplication(self.mtm()).currentEvent().is_some_and(|e| e.modifierFlags().contains(NSEventModifierFlags::Shift));
                self.look(if shift { -1 } else { 1 });
            } else if what == sel!(cancelOperation:) {
                self.put(false);
            } else {
                return Bool::NO;
            }
            Bool::YES
        }

        #[unsafe(method(next:))]
        fn next(&self, _button: &AnyObject) {
            self.look(1);
        }

        #[unsafe(method(before:))]
        fn before(&self, _button: &AnyObject) {
            self.look(-1);
        }

        #[unsafe(method(done:))]
        fn done(&self, _button: &AnyObject) {
            self.put(false);
        }
    }
);

impl Find {
    fn shown(&self) -> bool {
        // SAFETY: on the main thread.
        unsafe { self.ivars().bar.superview() }.is_some()
    }

    /// Over the page, in the room of its window.
    fn put(&self, shown: bool) {
        let Bar { page, bar, field } = self.ivars();
        // SAFETY: on the main thread.
        let Some(around) = (unsafe { page.superview() }) else { return };
        let (room, flipped, tall) = (around.bounds(), around.isFlipped(), if shown { bar.frame().size.height } else { 0.0 });
        if shown {
            let (top, edge) = if flipped { (0.0, NSAutoresizingMaskOptions::ViewMaxYMargin) } else { (room.size.height - tall, NSAutoresizingMaskOptions::ViewMinYMargin) };
            bar.setFrame(NSRect::new(NSPoint::new(0.0, top), NSSize::new(room.size.width, tall)));
            bar.setAutoresizingMask(NSAutoresizingMaskOptions::ViewWidthSizable | edge);
            around.addSubview(bar);
        } else {
            bar.removeFromSuperview();
        }
        page.setFrame(NSRect::new(NSPoint::new(0.0, if flipped { tall } else { 0.0 }), NSSize::new(room.size.width, room.size.height - tall)));
        if let Some(window) = page.window() {
            window.makeFirstResponder(Some(if shown { field } else { page }));
        }
        if shown {
            // SAFETY: from no one, as it may be.
            unsafe { field.selectText(None) };
        }
    }

    /// 1: the next one, -1: the one before, 0: more was typed.
    fn look(&self, step: i8) {
        let Bar { page, field, .. } = self.ivars();
        let words = field.stringValue();
        field.setTextColor(Some(&NSColor::labelColor()));
        let Some(options) = AnyClass::get(c"WKFindConfiguration").filter(|_| words.length() > 0) else { return };
        // SAFETY: WebKit's own methods of the page's view, since macOS 11 as its options.
        unsafe {
            if step == 0 { // from where it is, not after it
                let told: Option<&Block<dyn Fn(*mut AnyObject, *mut NSError)>> = None;
                let () = msg_send![page, evaluateJavaScript: ns_string!("(s=>{if(s.rangeCount)s.collapseToStart()})(getSelection())"), completionHandler: told];
            }
            let options: Retained<AnyObject> = msg_send![options, new];
            let () = msg_send![&options, setBackwards: step < 0];
            let () = msg_send![&options, setWraps: true];
            let field = field.clone();
            let told = RcBlock::new(move |result: *mut AnyObject| {
                let found: bool = !result.is_null() && msg_send![result, matchFound];
                let color = if found { NSColor::labelColor() } else { NSColor::systemRedColor() };
                field.setTextColor(Some(&color));
            });
            let () = msg_send![page, findString: &*words, withConfiguration: &*options, completionHandler: &*told];
        }
    }
}

thread_local! {
    static FIND: RefCell<Option<Retained<Find>>> = const { RefCell::new(None) };
}

/// A bar over the page, as Safari's.
fn find(view: &NSView, mtm: MainThreadMarker) {
    const TALL: f64 = 40.0;
    let place = |x: f64, w: f64, h: f64| NSRect::new(NSPoint::new(x, (TALL - h) / 2.0), NSSize::new(w, h));
    let bar = NSView::initWithFrame(mtm.alloc(), place(0.0, 380.0, TALL));
    let field = NSTextField::textFieldWithString(ns_string!(""), mtm);
    field.setPlaceholderString(Some(ns_string!("Find")));
    let own = mtm.alloc::<Find>().set_ivars(Bar { page: view.retain(), bar: bar.clone(), field: field.clone() });
    // SAFETY: what they call is there, and stays as long as the program.
    let own: Retained<Find> = unsafe {
        let own: Retained<Find> = msg_send![super(own), init];
        let () = msg_send![&field, setDelegate: &*own];
        own
    };
    let button = |title: &NSString, label: &NSString, what: Sel, x: f64, w: f64| {
        // SAFETY: as above.
        let button = unsafe { NSButton::buttonWithTitle_target_action(title, Some(&own), Some(what), mtm) };
        button.setFrame(place(x, w, 28.0));
        // SAFETY: every view's.
        let () = unsafe { msg_send![&button, setAccessibilityLabel: label] };
        button
    };
    field.setFrame(place(12.0, 196.0, 24.0));
    let before = button(ns_string!("‹"), ns_string!("Find Previous"), sel!(before:), 214.0, 38.0);
    let next = button(ns_string!("›"), ns_string!("Find Next"), sel!(next:), 254.0, 38.0);
    let done = button(ns_string!("Done"), ns_string!("Done"), sel!(done:), 300.0, 68.0);
    for one in [&field as &NSView, &before, &next, &done] {
        one.setAutoresizingMask(NSAutoresizingMaskOptions::ViewMinXMargin); // on the right
        bar.addSubview(one);
    }
    FIND.set(Some(own));
}

/// 0: the bar, 1: the next one, -1: the one before.
pub fn find_next(step: i8) {
    let Some(find) = FIND.with_borrow(Clone::clone) else { return };
    if !find.ivars().page.window().is_some_and(|w| w.isKeyWindow()) {
        return;
    }
    if step == 0 || !find.shown() {
        find.put(true);
    } else {
        find.look(step);
    }
}

// Files

/// The Downloads folder in the Dock bounces, as for a browser's.
pub fn downloaded(file: &Path) {
    let Some(path) = file.to_str().map(NSString::from_str) else { return };
    // SAFETY: the name of the notice says what its object is: the file's path.
    unsafe {
        let center: Option<Retained<AnyObject>> = AnyClass::get(c"NSDistributedNotificationCenter").map(|c| msg_send![c, defaultCenter]);
        if let Some(center) = center {
            let () = msg_send![&center, postNotificationName: ns_string!("com.apple.DownloadFileFinished"), object: &*path];
        }
    }
}

// Starting at login

#[link(name = "ServiceManagement", kind = "framework")]
extern "C" {}

/// The app itself, as an item in System Settings, General, Login Items.
fn item() -> Option<Retained<AnyObject>> {
    let class = AnyClass::get(c"SMAppService")?; // since macOS 13, the oldest it runs on
    // SAFETY: a class method that gives an object.
    unsafe { msg_send![class, mainAppService] }
}

pub fn login_state() -> login::State {
    // SAFETY: it has this property, a number.
    let status: isize = item().map_or(0, |item| unsafe { msg_send![&item, status] });
    match status {
        1 => login::State::On,
        2 => login::State::Asks,
        _ => login::State::Off,
    }
}

pub fn set_login(on: bool) -> bool {
    let Some(item) = item() else { return false };
    let none = std::ptr::null_mut::<*mut NSError>();
    // SAFETY: it has these methods, which take a place for an error, or none.
    let done: bool = unsafe { if on { msg_send![&item, registerAndReturnError: none] } else { msg_send![&item, unregisterAndReturnError: none] } };
    if on && login_state() == login::State::Asks {
        // SAFETY: a class method without arguments.
        unsafe {
            let () = msg_send![item.class(), openSystemSettingsLoginItems];
        }
        return true;
    }
    done
}

/// Whether macOS started the program by itself, at login. Only asked while it starts.
pub fn at_login() -> bool {
    const fn code(name: &[u8; 4]) -> u32 {
        u32::from_be_bytes(*name)
    }
    // SAFETY: the manager is always there; the event is the one the program is started with, or none.
    unsafe {
        let Some(class) = AnyClass::get(c"NSAppleEventManager") else { return false };
        let manager: Retained<AnyObject> = msg_send![class, sharedAppleEventManager];
        let event: Option<Retained<AnyObject>> = msg_send![&manager, currentAppleEvent];
        let Some(event) = event else { return false };
        let id: u32 = msg_send![&event, eventID];
        let why: Option<Retained<AnyObject>> = msg_send![&event, paramDescriptorForKeyword: code(b"prdt")];
        let why: u32 = why.map_or(0, |w| msg_send![&w, enumCodeValue]);
        id == code(b"oapp") && why == code(b"lgit")
    }
}

// Notifications

define_class!(
    // SAFETY: NSObject asks nothing of what is made from it.
    #[unsafe(super(NSObject))]
    #[name = "TheMachineNotices"]
    struct Notices;

    unsafe impl NSObjectProtocol for Notices {}

    unsafe impl UNUserNotificationCenterDelegate for Notices {
        // While the program is in front, with its settings: the dashboard in front gets none (speak.rs)
        #[unsafe(method(userNotificationCenter:willPresentNotification:withCompletionHandler:))]
        fn shows(&self, _center: &UNUserNotificationCenter, _notice: &UNNotification, answer: &Block<dyn Fn(UNNotificationPresentationOptions)>) {
            answer.call((UNNotificationPresentationOptions::Banner | UNNotificationPresentationOptions::List,));
        }

        #[unsafe(method(userNotificationCenter:didReceiveNotificationResponse:withCompletionHandler:))]
        fn opened(&self, _center: &UNUserNotificationCenter, response: &UNNotificationResponse, answer: &Block<dyn Fn()>) {
            notify::opened(&response.notification().request().identifier().to_string());
            answer.call(());
        }
    }
);

/// macOS only knows a program that is in an app's folder.
fn center() -> Option<Retained<UNUserNotificationCenter>> {
    let own = objc2_foundation::NSBundle::mainBundle().bundleIdentifier();
    own.map(|_| UNUserNotificationCenter::currentNotificationCenter())
}

static LETS: AtomicU8 = AtomicU8::new(0);

pub fn notices_start() {
    let Some(center) = center() else { return };
    let own: Retained<Notices> = {
        let own = Notices::alloc().set_ivars(());
        // SAFETY: NSObject's own.
        unsafe { msg_send![super(own), init] }
    };
    center.setDelegate(Some(ProtocolObject::from_ref(&*own)));
    std::mem::forget(own); // the center doesn't keep it
    notices_look(|| {});
}

/// Whether macOS lets it, which the person can change at any time.
pub fn notices_look(told: impl Fn() + 'static + Send) {
    let Some(center) = center() else { return told() };
    let answer = RcBlock::new(move |settings: std::ptr::NonNull<objc2_user_notifications::UNNotificationSettings>| {
        // SAFETY: macOS gives it for as long as the block runs.
        let status = unsafe { settings.as_ref() }.authorizationStatus();
        let lets = match status {
            UNAuthorizationStatus::NotDetermined => 0,
            UNAuthorizationStatus::Denied => 2,
            _ => 1,
        };
        LETS.store(lets, Ordering::Relaxed);
        told();
    });
    center.getNotificationSettingsWithCompletionHandler(&answer);
}

pub fn notices_lets() -> notify::Lets {
    match LETS.load(Ordering::Relaxed) {
        0 => notify::Lets::Unasked,
        1 => notify::Lets::Yes,
        _ => notify::Lets::No,
    }
}

/// macOS asks the person, the first time.
pub fn notices_ask(told: impl Fn() + 'static + Send) {
    let Some(center) = center() else { return told() };
    let answer = RcBlock::new(move |granted: Bool, _: *mut NSError| {
        LETS.store(if granted.as_bool() { 1 } else { 2 }, Ordering::Relaxed);
        told();
    });
    center.requestAuthorizationWithOptions_completionHandler(UNAuthorizationOptions::Alert | UNAuthorizationOptions::Badge, &answer);
}

pub fn notice(id: &str, title: &str, line: &str) {
    let Some(center) = center() else { return };
    let content = UNMutableNotificationContent::new();
    content.setTitle(&NSString::from_str(title));
    content.setBody(&NSString::from_str(line));
    let request = UNNotificationRequest::requestWithIdentifier_content_trigger(&NSString::from_str(id), &content, None);
    center.addNotificationRequest_withCompletionHandler(&request, None);
}

pub fn notice_gone(id: &str) {
    if let Some(center) = center() {
        center.removeDeliveredNotificationsWithIdentifiers(&NSArray::from_retained_slice(&[NSString::from_str(id)]));
    }
}

/// The system doesn't slow the program down while it is out of sight: what is new is told in time.
pub fn awake(on: bool) {
    thread_local! {
        static KEPT: RefCell<Option<Retained<AnyObject>>> = const { RefCell::new(None) };
    }
    KEPT.with_borrow_mut(|kept| {
        // SAFETY: the process' own info; what it gives to begin is what it takes to end. The option is
        // NSActivityUserInitiatedAllowingIdleSystemSleep: the computer sleeps as ever.
        unsafe {
            let Some(class) = AnyClass::get(c"NSProcessInfo") else { return };
            let info: Retained<AnyObject> = msg_send![class, processInfo];
            if !on {
                if let Some(activity) = kept.take() {
                    let () = msg_send![&info, endActivity: &*activity];
                }
            } else if kept.is_none() {
                *kept = Some(msg_send![&info, beginActivityWithOptions: 0x00EF_FFFF_u64, reason: ns_string!("Tells what is new")]);
            }
        }
    });
}
