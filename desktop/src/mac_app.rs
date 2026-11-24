//! What is macOS' own in the dashboard's window: what a page asks (alert, confirm, prompt), links and frames, finding in the
//! page, the title bar in the page's color, and starting at login and notifications.
use crate::{dash, login, notify};
use block2::{Block, RcBlock};
use objc2::rc::Retained;
use objc2::runtime::{AnyClass, AnyObject, Bool, ClassBuilder, NSObject, NSObjectProtocol, ProtocolObject, Sel};
use objc2::{define_class, msg_send, sel, AnyThread, DefinedClass, MainThreadMarker, MainThreadOnly, Message};
use objc2_app_kit::{
    NSAlert, NSAlertFirstButtonReturn, NSAutoresizingMaskOptions, NSColor, NSModalResponse, NSTextField, NSTextFinder, NSTextFinderAction, NSTextFinderBarContainer, NSTitlebarSeparatorStyle, NSView, NSWindow,
    NSWindowTitleVisibility,
};
use objc2_foundation::{ns_string, NSArray, NSDictionary, NSError, NSObjectNSKeyValueObserverRegistration, NSPoint, NSRect, NSSize, NSString};
use objc2_user_notifications::{
    UNAuthorizationOptions, UNAuthorizationStatus, UNMutableNotificationContent, UNNotification, UNNotificationPresentationOptions, UNNotificationRequest, UNNotificationResponse,
    UNUserNotificationCenter, UNUserNotificationCenterDelegate,
};
use std::cell::{Cell, RefCell};
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};
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
            });
            ns.setTabbingMode(objc2_app_kit::NSWindowTabbingMode::Disallowed);
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
unsafe fn subclass(view: &NSView, which: Sel, set: Sel, name: &std::ffi::CStr, methods: impl FnOnce(&mut ClassBuilder)) {
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
    window.setTitlebarAppearsTransparent(true);
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
    bar: RefCell<Option<Retained<NSView>>>,
    shown: Cell<bool>,
}

define_class!(
    // SAFETY: NSObject asks nothing of what is made from it.
    #[unsafe(super(NSObject))]
    #[thread_kind = MainThreadOnly]
    #[name = "TheMachineFind"]
    #[ivars = Bar]
    struct Find;

    unsafe impl NSObjectProtocol for Find {}

    unsafe impl NSTextFinderBarContainer for Find {
        #[unsafe(method_id(findBarView))]
        fn bar(&self) -> Option<Retained<NSView>> {
            self.ivars().bar.borrow().clone()
        }

        #[unsafe(method(setFindBarView:))]
        fn set_bar(&self, bar: Option<&NSView>) {
            self.put(false);
            *self.ivars().bar.borrow_mut() = bar.map(|b| b.retain());
        }

        #[unsafe(method(isFindBarVisible))]
        fn shown(&self) -> bool {
            self.ivars().shown.get()
        }

        #[unsafe(method(setFindBarVisible:))]
        fn set_shown(&self, shown: bool) {
            self.put(shown);
        }

        #[unsafe(method(findBarViewDidChangeHeight))]
        fn resized(&self) {
            self.lay_out();
        }

        #[unsafe(method_id(contentView))]
        fn content(&self) -> Option<Retained<NSView>> {
            Some(self.ivars().page.clone())
        }
    }
);

impl Find {
    fn put(&self, shown: bool) {
        self.ivars().shown.set(shown);
        let Some(bar) = self.ivars().bar.borrow().clone() else { return };
        let page = &self.ivars().page;
        if !shown {
            bar.removeFromSuperview();
            if let Some(window) = page.window() {
                window.makeFirstResponder(Some(page));
            }
        } else if let Some(around) = unsafe { page.superview() } { // SAFETY: on the main thread
            around.addSubview(&bar);
        }
        self.lay_out();
    }

    /// The bar over the page, in the room of its window.
    fn lay_out(&self) {
        let Bar { page, bar, shown } = self.ivars();
        let Some(around) = (unsafe { page.superview() }) else { return };
        let room = around.bounds();
        let tall = match &*bar.borrow() {
            Some(bar) if shown.get() => {
                let tall = bar.frame().size.height;
                let top = if around.isFlipped() { 0.0 } else { room.size.height - tall };
                bar.setFrame(NSRect::new(NSPoint::new(0.0, top), NSSize::new(room.size.width, tall)));
                let edge = if around.isFlipped() { NSAutoresizingMaskOptions::ViewMaxYMargin } else { NSAutoresizingMaskOptions::ViewMinYMargin };
                bar.setAutoresizingMask(NSAutoresizingMaskOptions::ViewWidthSizable | edge);
                tall
            }
            _ => 0.0,
        };
        let top = if around.isFlipped() { tall } else { 0.0 };
        page.setFrame(NSRect::new(NSPoint::new(0.0, top), NSSize::new(room.size.width, room.size.height - tall)));
    }
}

thread_local! {
    static FINDER: RefCell<Option<Retained<NSTextFinder>>> = const { RefCell::new(None) };
}

/// macOS' own find bar, as Safari's: WKWebView answers it, where it has that.
///
/// # Safety
/// On the main thread, for a WKWebView, which is there as long as the program.
unsafe fn find(view: &NSView, mtm: MainThreadMarker) {
    if !view.respondsToSelector(sel!(findMatchesForString:relativeToMatch:findOptions:maxResults:resultCollector:)) {
        return;
    }
    let own = mtm.alloc::<Find>().set_ivars(Bar { page: view.retain(), bar: RefCell::new(None), shown: Cell::new(false) });
    let own: Retained<Find> = msg_send![super(own), init];
    let finder = NSTextFinder::new();
    let () = msg_send![&finder, setClient: view];
    finder.setFindBarContainer(Some(ProtocolObject::from_ref(&*own)));
    finder.setIncrementalSearchingEnabled(true);
    finder.setIncrementalSearchingShouldDimContentView(false);
    std::mem::forget(own);
    FINDER.set(Some(finder));
}

/// 0: the bar, 1: the next one, -1: the one before.
pub fn find_next(step: i8) {
    FINDER.with_borrow(|finder| {
        let Some(finder) = finder else { return };
        let action = match step {
            0 => NSTextFinderAction::ShowFindInterface,
            1.. => NSTextFinderAction::NextMatch,
            _ => NSTextFinderAction::PreviousMatch,
        };
        if finder.validateAction(action) {
            finder.performAction(action);
        }
    });
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

static ALLOWED: AtomicBool = AtomicBool::new(false);

pub fn notices_start() {
    let Some(center) = center() else { return };
    let own: Retained<Notices> = {
        let own = Notices::alloc().set_ivars(());
        // SAFETY: NSObject's own.
        unsafe { msg_send![super(own), init] }
    };
    center.setDelegate(Some(ProtocolObject::from_ref(&*own)));
    std::mem::forget(own); // the center doesn't keep it
    notices_look(|_| {});
}

/// Whether macOS lets it, which the person can change at any time.
pub fn notices_look(told: impl Fn(bool) + 'static + Send) {
    let Some(center) = center() else { return told(false) };
    let answer = RcBlock::new(move |settings: std::ptr::NonNull<objc2_user_notifications::UNNotificationSettings>| {
        // SAFETY: macOS gives it for as long as the block runs.
        let status = unsafe { settings.as_ref() }.authorizationStatus();
        let allowed = status == UNAuthorizationStatus::Authorized || status == UNAuthorizationStatus::Provisional;
        ALLOWED.store(allowed, Ordering::Relaxed);
        told(allowed);
    });
    center.getNotificationSettingsWithCompletionHandler(&answer);
}

pub fn notices_allowed() -> bool {
    ALLOWED.load(Ordering::Relaxed)
}

/// macOS asks the person, the first time; after a no, its settings open.
pub fn notices_ask(told: impl Fn(bool) + 'static + Send) {
    let Some(center) = center() else { return told(false) };
    let answer = RcBlock::new(move |granted: Bool, _: *mut NSError| {
        ALLOWED.store(granted.as_bool(), Ordering::Relaxed);
        told(granted.as_bool());
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
