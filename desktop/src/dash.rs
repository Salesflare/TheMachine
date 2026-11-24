//! The dashboard in a window of its own: the Machine's own page, as a browser shows it, with what a browser has around it
//! (links, files, downloads, zoom, a place of its own). It gets none of the app's commands: those are only for the app's own
//! page in this window (ui/app.html), that signs in and says when the Machine can't be reached. Its session is the one the
//! app keeps, set each time the dashboard is loaded; a to-do in the box has the same one, in a store of its own (card.rs).
use crate::machine::Machine;
use crate::place::Rect;
use crate::{address, card, files, later, quit, signin, windows, Shared};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::time::Duration;
use tauri::webview::{DownloadEvent, NewWindowResponse, PageLoadEvent, PermissionKind, PermissionResponse};
use tauri::{AppHandle, Emitter, LogicalPosition, LogicalSize, Manager, PhysicalPosition, PhysicalSize, WebviewUrl, WebviewWindow, WebviewWindowBuilder};
use url::Url;

pub const LABEL: &str = "app";
const SMALLEST: (f64, f64) = (380.0, 480.0);
const USUAL: (f64, f64) = (1280.0, 860.0);
const ZOOMS: [f64; 13] = [0.5, 0.67, 0.75, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0];

/// How the dashboard knows where it is: it is the same page, but nothing to install, and downloads say where they landed.
const SCRIPT: &str = "Object.defineProperty(window,'machineDesktop',{value:Object.freeze({version:1})});";

/// The window, or one with a file, is in front.
static FRONT: AtomicBool = AtomicBool::new(false);

/// What the app's own page says.
#[derive(Clone, Copy, Debug, Default, PartialEq, serde::Serialize)]
#[serde(rename_all = "lowercase")]
pub enum View {
    #[default]
    Blank,
    SignIn,
    /// The Machine doesn't take the session any more.
    SignedOut,
    /// The Machine's address is another one now.
    Moved,
    Offline,
}

#[derive(Debug, PartialEq)]
enum At {
    Own(View),
    /// This Machine's dashboard, and whether its page came.
    Machine(String, bool),
}

pub struct Dash {
    at: At,
    /// The place in the dashboard that is asked for, until it is there.
    path: String,
    loads: u64,
    #[cfg(target_os = "macos")]
    died: Option<std::time::Instant>,
}

impl Default for Dash {
    fn default() -> Self {
        Dash {
            at: At::Own(View::Blank),
            path: String::new(),
            loads: 0,
            #[cfg(target_os = "macos")]
            died: None,
        }
    }
}

/// Whether the app has this window. So far on a Mac; elsewhere the dashboard opens in its installed app or the browser.
pub fn here() -> bool {
    cfg!(target_os = "macos") || cfg!(feature = "sandbox") && std::env::var_os("MACHINE_SANDBOX_WINDOW").is_some()
}

pub fn front() -> bool {
    FRONT.load(Ordering::Relaxed)
}

pub fn label(label: &str) -> bool {
    label == LABEL || label.starts_with("file-")
}

pub fn window(app: &AppHandle) -> Option<WebviewWindow> {
    app.get_webview_window(LABEL)
}

pub fn visible(app: &AppHandle) -> bool {
    window(app).is_some_and(|w| w.is_visible().unwrap_or(false))
}

// Where a page may go

#[derive(Debug, PartialEq)]
enum Goes {
    /// On in the window.
    Here,
    /// The app's own page.
    Own,
    SignedOut,
    Moved,
    /// To the browser, or the mail app.
    Out,
    No,
}

/// A place the dashboard goes to. `account`: where the person signs in.
fn goes(machine: &str, account: &str, url: &Url) -> Goes {
    if matches!(url.as_str(), "about:blank" | "about:srcdoc") {
        return Goes::Here;
    }
    if url.scheme() == "tauri" || url.host_str() == Some("tauri.localhost") {
        return Goes::Own;
    }
    if own(machine, url) {
        return Goes::Here;
    }
    match url.scheme() {
        "http" | "https" => {}
        "mailto" => return Goes::Out,
        _ => return Goes::No,
    }
    if Url::parse(account).is_ok_and(|a| a.origin() == url.origin()) {
        return if url.path() == "/open" { Goes::SignedOut } else { Goes::Out };
    }
    // A hosted Machine whose name was changed sends its own address on to the new one
    let hosted = |u: &Url| u.scheme() == "https" && u.port().is_none() && u.host_str().is_some_and(address::hosted_host);
    if hosted(url) && url.path() == "/" && Url::parse(machine).is_ok_and(|m| hosted(&m)) {
        return Goes::Moved;
    }
    Goes::Out
}

/// The Machine's own: what is under its address, its sign-in's (/_machine/), and files its page made.
fn own(machine: &str, url: &Url) -> bool {
    let Ok(machine) = Url::parse(machine) else { return false };
    if url.scheme() == "blob" {
        return url.origin() == machine.origin();
    }
    url.origin() == machine.origin() && (url.path().starts_with(machine.path()) || url.path().starts_with("/_machine/"))
}

/// A place in the dashboard: what comes after its address.
fn place(machine: &str, url: &Url) -> Option<String> {
    let path = url.as_str().strip_prefix(machine).filter(|_| own(machine, url))?;
    (path.is_empty() || path.starts_with('#')).then(|| path.to_string())
}

fn machine_url(app: &AppHandle) -> Option<String> {
    app.state::<Shared>().machine().map(|m| m.url)
}

/// What a page asks to open in a window of its own.
fn open_link(app: &AppHandle, url: &Url) {
    let Some(machine) = machine_url(app) else { return };
    if let Some(path) = place(&machine, url) {
        show(app, &path);
    } else if own(&machine, url) && url.scheme() != "blob" {
        open_file(app, url);
    } else {
        card::web(app, url);
    }
}

// The window

fn build(app: &AppHandle) -> tauri::Result<WebviewWindow> {
    let (goes_to, opens, loads, saves) = (app.clone(), app.clone(), app.clone(), app.clone());
    let at = frame(app);
    let window = WebviewWindowBuilder::new(app, LABEL, WebviewUrl::App("app.html".into()))
        .title("The Machine")
        .inner_size(USUAL.0, USUAL.1)
        .min_inner_size(SMALLEST.0, SMALLEST.1)
        .visible(false)
        .disable_drag_drop_handler() // the page takes dropped files itself
        .zoom_hotkeys_enabled(cfg!(windows))
        .additional_browser_args(&windows::browser())
        .initialization_script(SCRIPT)
        .on_navigation(move |url| navigation(&goes_to, url))
        .on_new_window(move |url, _| {
            later(&opens, move |app| open_link(app, &url));
            NewWindowResponse::Deny
        })
        .on_download(move |_, event| files::download(&saves, event))
        .on_permission_request(|_, kind| match kind {
            PermissionKind::Microphone => PermissionResponse::Allow, // the system asks; Talk and dictation
            PermissionKind::Camera | PermissionKind::Geolocation | PermissionKind::Notifications => PermissionResponse::Deny,
            _ => PermissionResponse::Default,
        })
        .on_page_load(move |_, page| {
            // Elsewhere a page has only started to load by then
            if page.event() == PageLoadEvent::Finished || cfg!(target_os = "macos") {
                loaded(&loads, page.url());
            }
        });
    let window = window.build()?;
    #[cfg(target_os = "macos")]
    crate::mac_app::prepare(&window);
    #[cfg(windows)]
    windows::no_menu(&window);
    put(&window, at);
    if app.state::<Shared>().saved.lock().unwrap().wide && !cfg!(target_os = "macos") {
        let _ = window.maximize();
    }
    let zoom = app.state::<Shared>().saved.lock().unwrap().zoom;
    if zoom > 0.0 {
        let _ = window.set_zoom(zoom);
    }
    Ok(window)
}

fn navigation(app: &AppHandle, url: &Url) -> bool {
    let shared = app.state::<Shared>();
    let machine = machine_url(app).unwrap_or_default();
    let (own_page, there) = match &shared.dash.lock().unwrap().at {
        At::Own(_) => (true, false),
        At::Machine(_, there) => (false, *there),
    };
    let to = match goes(&machine, &signin::account(), url) {
        Goes::Here => return true,
        Goes::Own => return own_page,
        Goes::Out if !there && url.scheme() != "mailto" => View::SignedOut, // a sign-in of its own, in front of it
        Goes::Out => {
            let url = url.clone();
            later(app, move |app| card::web(app, &url));
            return false;
        }
        Goes::SignedOut => View::SignedOut,
        Goes::Moved => View::Moved,
        Goes::No => return false,
    };
    later(app, move |app| view(app, to));
    false
}

fn loaded(app: &AppHandle, url: &Url) {
    let shared = app.state::<Shared>();
    let mut dash = shared.dash.lock().unwrap();
    if let At::Machine(of, there) = &mut dash.at {
        if own(of, url) && !*there {
            *there = true;
            dash.path.clear();
        }
    }
}

/// Opens it, at a place in the dashboard ("" or "#card=..."): where it was when none is asked for.
pub fn show(app: &AppHandle, path: &str) {
    let window = match window(app) {
        Some(w) => w,
        None => match build(app) {
            Ok(w) => w,
            Err(error) => return eprintln!("could not open the window: {error}"),
        },
    };
    let shared = app.state::<Shared>();
    match shared.machine() {
        None => view(app, View::SignIn),
        Some(machine) => {
            let step = {
                let mut dash = shared.dash.lock().unwrap();
                if !path.is_empty() {
                    dash.path = path.into();
                }
                match &dash.at {
                    At::Own(View::SignedOut | View::Moved) => None, // signing in comes first
                    At::Machine(url, _) if *url == machine.url && path.is_empty() => None,
                    At::Machine(url, true) if *url == machine.url => Some(true),
                    _ => Some(false),
                }
            };
            match step {
                Some(true) => {
                    shared.dash.lock().unwrap().path.clear();
                    step_to(&window, &machine.url, path);
                }
                Some(false) => load(app, &window, &machine),
                None => {}
            }
        }
    }
    let _ = window.unminimize();
    let _ = window.show();
    let _ = window.set_focus();
    shared.over_dash.store(true, Ordering::Relaxed);
    windows::close_box(app);
}

/// A place within the page that is there, as the dashboard takes an address that was opened again.
fn step_to(window: &WebviewWindow, machine: &str, path: &str) {
    let inside = window.url().is_ok_and(|now| place(machine, &now).is_some() || now.query().is_some() && own(machine, &now) && Url::parse(machine).is_ok_and(|m| m.path() == now.path()));
    if inside {
        let hash = serde_json::to_string(path).unwrap_or_default();
        let _ = window.eval(format!("location.hash==={hash}?dispatchEvent(new HashChangeEvent('hashchange')):location.hash={hash}"));
    } else if let Ok(url) = Url::parse(&format!("{machine}{path}")) {
        let _ = window.navigate(url);
    }
}

fn load(app: &AppHandle, window: &WebviewWindow, machine: &Machine) {
    let shared = app.state::<Shared>();
    let (path, load) = {
        let mut dash = shared.dash.lock().unwrap();
        dash.at = At::Machine(machine.url.clone(), false);
        dash.loads += 1;
        (dash.path.clone(), dash.loads)
    };
    let Ok(url) = Url::parse(&format!("{}{path}", machine.url)) else { return };
    card::session(window, machine, &url);
    let _ = window.navigate(url);
    let (app, machine) = (app.clone(), machine.clone());
    std::thread::spawn(move || {
        let reached = machine.check();
        if matches!(reached.as_ref().map_err(String::as_str), Err("unreachable" | "notmachine")) {
            std::thread::sleep(Duration::from_millis(1500)); // the page its service worker keeps comes first
            later(&app, move |app| unreached(app, load));
        }
    });
}

/// Nothing answered: the page that is there is the dashboard's own kept one, or it is none of the Machine's.
fn unreached(app: &AppHandle, load: u64) {
    let Some(window) = window(app) else { return };
    let here = app.clone();
    let _ = window.eval_with_callback("!!document.querySelector('link[rel=manifest]')", move |kept| {
        later(&here, move |app| {
            let this = app.state::<Shared>().dash.lock().unwrap().loads == load;
            if this && kept.trim() != "true" {
                view(app, View::Offline);
            }
        });
    });
}

/// The app's own page takes the place of the dashboard.
fn view(app: &AppHandle, view: View) {
    let was = {
        let shared = app.state::<Shared>();
        let mut dash = shared.dash.lock().unwrap();
        dash.loads += 1; // what was loading isn't any more
        std::mem::replace(&mut dash.at, At::Own(view))
    };
    let Some(window) = window(app) else { return };
    match was {
        At::Own(_) => {
            let _ = window.emit_to(LABEL, "view", ());
        }
        At::Machine(..) => {
            let page = if cfg!(windows) { "http://tauri.localhost/app.html" } else { "tauri://localhost/app.html" };
            let _ = window.navigate(page.parse().unwrap());
        }
    }
}

pub fn now(app: &AppHandle) -> View {
    match app.state::<Shared>().dash.lock().unwrap().at {
        At::Own(view) => view,
        At::Machine(..) => View::Blank,
    }
}

/// Try again.
pub fn retry(app: &AppHandle) {
    let shared = app.state::<Shared>();
    if let (Some(window), Some(machine), true) = (window(app), shared.machine(), now(app) == View::Offline) {
        load(app, &window, &machine);
    }
}

/// The app's own look (main.rs) got an answer: the Machine is there again.
pub fn answered(app: &AppHandle) {
    if now(app) == View::Offline {
        later(app, retry);
    }
}

/// Signed in, in the box or here.
pub fn signed_in(app: &AppHandle) {
    if let (Some(window), Some(machine)) = (window(app), app.state::<Shared>().machine()) {
        if visible(app) {
            load(app, &window, &machine);
        } else {
            view(app, View::Blank); // it loads when it is opened
        }
    }
}

/// Signed out: nothing of it is left on this computer.
pub fn forget(app: &AppHandle) {
    for (label, file) in app.webview_windows() {
        if label.starts_with("file-") {
            let _ = file.destroy();
        }
    }
    app.state::<Shared>().dash.lock().unwrap().path.clear();
    view(app, View::SignIn);
    if here() {
        if let Some(any) = app.get_webview_window("robot") {
            let _ = any.clear_all_browsing_data(); // the windows have one store
        }
    }
}

/// Tells the dashboard what the app did. One that doesn't know of it does nothing.
pub fn tell(app: &AppHandle, what: &serde_json::Value) {
    let there = matches!(app.state::<Shared>().dash.lock().unwrap().at, At::Machine(_, true));
    if let (Some(window), true) = (window(app), there) {
        let _ = window.eval(format!("dispatchEvent(new CustomEvent('machinedesktop',{{detail:{what}}}))"));
    }
}

/// Its page's process ended, as macOS ends one that takes too much memory: a fresh one, unless that ends too.
#[cfg(target_os = "macos")]
pub fn died(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let again = {
        let mut dash = shared.dash.lock().unwrap();
        let again = dash.died.is_none_or(|last| last.elapsed() > Duration::from_secs(20));
        dash.died = Some(std::time::Instant::now());
        again
    };
    match window(app) {
        Some(window) if again => { let _ = window.reload(); }
        Some(_) if shared.machine().is_some() => view(app, View::Offline),
        _ => {}
    }
}

/// The close button, as Settings has it. Hidden, not gone: it is there again at once.
pub fn close(app: &AppHandle) {
    keep(app);
    if app.state::<Shared>().saved.lock().unwrap().quits {
        return quit::quit(app);
    }
    let Some(window) = window(app) else { return };
    if !window.is_fullscreen().unwrap_or(false) {
        let _ = window.hide();
        return;
    }
    // A full screen that is hidden stays as an empty one
    let _ = window.set_fullscreen(false);
    let app = app.clone();
    std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(1200));
        later(&app, move |_| { let _ = window.hide(); });
    });
}

pub fn focused(app: &AppHandle, of: &str, on: bool) {
    FRONT.store(on || in_front(app).is_some_and(|w| w.label() != of), Ordering::Relaxed);
    if on {
        crate::looked(app);
        crate::speak::hush(app, true);
    } else {
        keep(app);
    }
    app.state::<Shared>().look_soon(); // whether it speaks
}

// Its place and size

/// Points on macOS, pixels elsewhere: what the window system counts in.
fn unit(window: &WebviewWindow) -> f64 {
    if cfg!(target_os = "macos") { window.scale_factor().unwrap_or(1.0) } else { 1.0 }
}

/// It was moved or got another size.
pub fn moved(app: &AppHandle) {
    let Some(window) = window(app) else { return };
    let odd = [window.is_fullscreen(), window.is_minimized()].into_iter().any(|is| is.unwrap_or(true));
    if odd || !window.is_visible().unwrap_or(false) {
        return;
    }
    let shared = app.state::<Shared>();
    let mut saved = shared.saved.lock().unwrap();
    saved.wide = window.is_maximized().unwrap_or(false) && !cfg!(target_os = "macos");
    if let (Ok(at), Ok(size), false) = (window.outer_position(), window.inner_size(), saved.wide) {
        let unit = unit(&window);
        saved.window = Some([at.x.into(), at.y.into(), size.width.into(), size.height.into()].map(|n: f64| n / unit));
    }
}

/// Written once it is left.
fn keep(app: &AppHandle) {
    moved(app);
    app.state::<Shared>().save();
}

fn frame(app: &AppHandle) -> Rect {
    let saved = app.state::<Shared>().saved.lock().unwrap().window;
    fit(saved, &windows::areas(app))
}

/// Where it was, when enough of that is on a screen still; else in the middle of the main one. Never larger than its screen.
fn fit(saved: Option<[f64; 4]>, screens: &[(Rect, f64)]) -> Rect {
    let Some((main, scale)) = screens.first().copied() else { return Rect { x: 0.0, y: 0.0, w: USUAL.0, h: USUAL.1 } };
    if let Some([x, y, w, h]) = saved.filter(|s| s.iter().all(|n| n.is_finite())) {
        // Its title bar has to be there, to move it by
        let there = screens.iter().find(|(a, s)| {
            let across = (x + w).min(a.x + a.w) - x.max(a.x);
            across >= 120.0 * s && y >= a.y - 1.0 && y <= a.y + a.h - 60.0 * s
        });
        if let Some((a, s)) = there {
            let (w, h) = (w.clamp(SMALLEST.0 * s, a.w.max(SMALLEST.0 * s)), h.clamp(SMALLEST.1 * s, a.h.max(SMALLEST.1 * s)));
            return Rect { x, y, w, h };
        }
    }
    let (w, h) = ((USUAL.0 * scale).min(main.w - 80.0 * scale), (USUAL.1 * scale).min(main.h - 60.0 * scale));
    Rect { x: main.x + (main.w - w) / 2.0, y: main.y + (main.h - h) / 3.0, w, h }
}

fn put(window: &WebviewWindow, at: Rect) {
    if cfg!(target_os = "macos") {
        let _ = window.set_size(LogicalSize::new(at.w, at.h));
        let _ = window.set_position(LogicalPosition::new(at.x, at.y));
    } else {
        let _ = window.set_position(PhysicalPosition::new(at.x.round(), at.y.round()));
        let _ = window.set_size(PhysicalSize::new(at.w.round(), at.h.round()));
    }
}

// The menu's

/// The window it is about: the dashboard's, or one with a file, when that is in front.
pub fn in_front(app: &AppHandle) -> Option<WebviewWindow> {
    app.webview_windows().into_values().find(|w| label(w.label()) && w.is_focused().unwrap_or(false))
}

/// 0: as made.
#[cfg_attr(not(target_os = "macos"), allow(dead_code))] // as the three after it: so far a menu's
pub fn zoom(app: &AppHandle, step: i8) {
    let Some(window) = window(app) else { return };
    let shared = app.state::<Shared>();
    let zoom = {
        let mut saved = shared.saved.lock().unwrap();
        saved.zoom = zoomed(saved.zoom, step);
        saved.zoom
    };
    let _ = window.set_zoom(zoom);
    shared.save();
}

fn zoomed(now: f64, step: i8) -> f64 {
    let now = if now > 0.0 { now } else { 1.0 };
    match step {
        0 => 1.0,
        1.. => ZOOMS.into_iter().find(|z| *z > now + 0.01).unwrap_or(3.0),
        _ => ZOOMS.into_iter().rev().find(|z| *z < now - 0.01).unwrap_or(0.5),
    }
}

#[cfg_attr(not(target_os = "macos"), allow(dead_code))]
pub fn reload(app: &AppHandle) {
    let Some(window) = in_front(app) else { return };
    if window.label() == LABEL && now(app) != View::Blank {
        return retry(app);
    }
    let _ = window.reload();
}

#[cfg_attr(not(target_os = "macos"), allow(dead_code))]
pub fn back(app: &AppHandle, forward: bool) {
    if let Some(window) = in_front(app) {
        let _ = window.eval(if forward { "history.forward()" } else { "history.back()" });
    }
}

/// Save a copy of the file in front.
#[cfg_attr(not(target_os = "macos"), allow(dead_code))]
pub fn save_copy(app: &AppHandle) {
    if let Some(url) = in_front(app).filter(|w| w.label() != LABEL).and_then(|w| w.url().ok()) {
        files::save(app, url);
    }
}

// Files

/// A file of the Machine's, in a window of its own: a PDF, a picture, text. One that can't be shown is downloaded, and the
/// window goes.
pub fn open_file(app: &AppHandle, url: &Url) {
    static FILES: AtomicU64 = AtomicU64::new(0);
    app.state::<Shared>().over_dash.store(true, Ordering::Relaxed);
    let name = format!("file-{}", FILES.fetch_add(1, Ordering::Relaxed));
    let (goes_to, opens, saves, titled) = (app.clone(), app.clone(), app.clone(), name.clone());
    let shown = std::sync::Arc::new(AtomicBool::new(false));
    let came = shown.clone();
    let area = windows::areas(app).first().map_or((900.0, 900.0), |(a, s)| (a.w / s, a.h / s));
    let window = WebviewWindowBuilder::new(app, &name, WebviewUrl::External("about:blank".parse().unwrap()))
        .title(title(url))
        .inner_size(920.0_f64.min(area.0 - 80.0), 1000.0_f64.min(area.1 - 80.0))
        .min_inner_size(320.0, 240.0)
        .disable_drag_drop_handler()
        .additional_browser_args(&windows::browser())
        .on_navigation(move |url| {
            let machine = machine_url(&goes_to).unwrap_or_default();
            let to = goes(&machine, &signin::account(), url);
            if to == Goes::Out {
                let url = url.clone();
                later(&goes_to, move |app| card::web(app, &url));
            }
            to == Goes::Here
        })
        .on_new_window(move |url, _| {
            later(&opens, move |app| open_link(app, &url));
            NewWindowResponse::Deny
        })
        .on_download(move |_, event| {
            let (name, over) = (titled.clone(), matches!(event, DownloadEvent::Finished { .. }));
            let saved = files::download(&saves, event);
            if !shown.load(Ordering::Relaxed) {
                later(&saves, move |app| gone(app, &name, over));
            }
            saved
        })
        .on_page_load(move |_, page| {
            if page.url().as_str() != "about:blank" && (page.event() == PageLoadEvent::Finished || cfg!(target_os = "macos")) {
                came.store(true, Ordering::Relaxed);
            }
        })
        .on_permission_request(|_, _| PermissionResponse::Deny)
        .on_document_title_changed(|window, title| {
            if !title.trim().is_empty() {
                let _ = window.set_title(title.trim());
            }
        });
    match window.build() {
        Ok(window) => {
            #[cfg(target_os = "macos")]
            crate::mac_app::prepare(&window);
            if let Some(machine) = app.state::<Shared>().machine() {
                card::session(&window, &machine, url);
            }
            let _ = window.navigate(url.clone());
            let _ = window.set_focus();
        }
        Err(error) => eprintln!("could not open a file: {error}"),
    }
}

/// Nothing to show: it goes to Downloads. The window ends once it is there, as its page is what downloads it.
fn gone(app: &AppHandle, name: &str, over: bool) {
    if over {
        return close_file(app, name);
    }
    if let Some(window) = app.get_webview_window(name) {
        let _ = window.hide();
    }
}

/// A window with a file that was closed.
pub fn close_file(app: &AppHandle, label: &str) {
    if let Some(window) = app.get_webview_window(label) {
        let _ = window.destroy();
    }
}

/// The file's name, as its address has it.
fn title(url: &Url) -> String {
    let named = url.query_pairs().find(|(k, v)| k == "name" && !v.is_empty()).map(|(_, v)| v.into_owned());
    let last = url.path_segments().and_then(|mut s| s.next_back()).filter(|s| s.contains('.')).map(String::from);
    named.or(last).map_or("The Machine".into(), |n| n.chars().take(80).collect())
}

#[cfg(test)]
mod tests {
    use super::*;

    const OWN: &str = "https://name.app.themachine.computer/";
    const ACCOUNT: &str = "https://app.themachine.computer";

    #[test]
    fn where_the_dashboard_may_go() {
        let to = |u: &str| goes(OWN, ACCOUNT, &u.parse().unwrap());
        for here in ["", "#card=aa01", "api/attachment?id=1", "_machine/account-hop", "?desk=x"] {
            assert_eq!(to(&format!("{OWN}{here}")), Goes::Here, "{here}");
        }
        assert_eq!([to("about:blank"), to("about:srcdoc"), to("blob:https://name.app.themachine.computer/1")], [Goes::Here, Goes::Here, Goes::Here]);
        assert_eq!([to("tauri://localhost/app.html"), to("http://tauri.localhost/app.html")], [Goes::Own, Goes::Own]);
        assert_eq!([to("https://app.themachine.computer/open"), to("https://app.themachine.computer/open?x=1")], [Goes::SignedOut, Goes::SignedOut]);
        assert_eq!([to("https://other.app.themachine.computer/"), to("https://other.app.themachine.computer/#card=aa01")], [Goes::Moved, Goes::Moved]);
        for out in ["https://app.themachine.computer/hop?t=x", "https://other.app.themachine.computer/s/1", "https://example.com/", "http://example.com/", "mailto:a@b.example",
            "https://name.app.themachine.computer.evil.example/", "http://name.app.themachine.computer/", "https://name.app.themachine.computer:8443/"] {
            assert_eq!(to(out), Goes::Out, "{out}");
        }
        for no in ["file:///etc/passwd", "data:text/html,x", "javascript:1", "blob:https://other.example/1", "ms-settings:x", "about:config"] {
            assert_eq!(to(no), Goes::No, "{no}");
        }
        // A self-hosted Machine under a path: what is beside it isn't its
        let mine = "https://my.example.com/assistant/";
        let to = |u: &str| goes(mine, ACCOUNT, &u.parse().unwrap());
        assert_eq!([to("https://my.example.com/assistant/#x"), to("https://my.example.com/other/"), to("https://name.app.themachine.computer/")], [Goes::Here, Goes::Out, Goes::Out]);
        assert_eq!(goes("", ACCOUNT, &"https://example.com/".parse().unwrap()), Goes::Out);
    }

    #[test]
    fn a_place_in_the_dashboard() {
        let at = |u: &str| place(OWN, &u.parse().unwrap());
        assert_eq!([at(OWN), at(&format!("{OWN}#card=aa01"))], [Some("".into()), Some("#card=aa01".into())]);
        assert_eq!([at(&format!("{OWN}api/attachment?id=1")), at(&format!("{OWN}?compact=1#card=a")), at("https://example.com/#x")], [None, None, None]);
    }

    #[test]
    fn it_opens_where_it_was() {
        let screen = |x: f64, w: f64, h: f64, scale: f64| (Rect { x, y: 25.0, w, h }, scale);
        let two = [screen(0.0, 1440.0, 815.0, 1.0), screen(1440.0, 1920.0, 1055.0, 1.0)];
        let was = [1500.0, 100.0, 1000.0, 700.0];
        assert_eq!(fit(Some(was), &two), Rect { x: 1500.0, y: 100.0, w: 1000.0, h: 700.0 });
        // That screen is gone; or only its edge shows; or its title bar doesn't
        let middle = fit(None, &two);
        assert_eq!(middle, Rect { x: 80.0, y: 25.0 + (815.0 - 755.0) / 3.0, w: 1280.0, h: 755.0 });
        for lost in [was, [-950.0, 100.0, 1000.0, 700.0], [100.0, 830.0, 1000.0, 700.0], [100.0, -300.0, 1000.0, 700.0], [f64::NAN, 1.0, 1.0, 1.0]] {
            assert_eq!(fit(Some(lost), &two[..1]), middle, "{lost:?}");
        }
        let large = fit(Some([0.0, 25.0, 3000.0, 2000.0]), &two[..1]);
        assert_eq!((large.w, large.h), (1440.0, 815.0));
        let small = fit(None, &[screen(0.0, 1024.0, 560.0, 1.0)]);
        assert_eq!((small.w, small.h), (944.0, 500.0));
        let twice = fit(None, &[screen(0.0, 3840.0, 2080.0, 2.0)]);
        assert_eq!((twice.w, twice.h), (2560.0, 1720.0));
        assert_eq!(fit(None, &[]).w, 1280.0);
    }

    #[test]
    fn zoom_steps() {
        assert_eq!([zoomed(0.0, 1), zoomed(1.1, 1), zoomed(3.0, 1), zoomed(1.0, -1), zoomed(0.5, -1), zoomed(2.0, 0)], [1.1, 1.25, 3.0, 0.9, 0.5, 1.0]);
    }

    #[test]
    fn a_files_name() {
        let of = |u: &str| title(&u.parse().unwrap());
        assert_eq!([of("https://x.example/api/attachment?id=1&name=Plan%20B.pdf"), of("https://x.example/api/a/plan.pdf"), of("https://x.example/api/attachment?id=1")], ["Plan B.pdf", "plan.pdf", "The Machine"]);
    }
}
