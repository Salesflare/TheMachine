//! Settings, a small window of the app's own: the robot, starting at login, what closing the dashboard's window does,
//! notifications when there is no robot, and whether the Machine's browser may go out through this computer. What the
//! Machine itself does is set in the dashboard.
use crate::{away, later, login, notify, speak, updates, windows, Shared};
use serde::Serialize;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;
use tauri::{AppHandle, Emitter, Manager, WebviewUrl, WebviewWindow, WebviewWindowBuilder};

const LABEL: &str = "settings";
const WIDTH: f64 = 420.0;

/// Shown once its page says how tall it is; a page that is only read again says so too.
static OPENING: AtomicBool = AtomicBool::new(false);
/// How tall its page said it is.
static HEIGHT: Mutex<f64> = Mutex::new(300.0);

#[derive(Serialize)]
pub struct Settings {
    robot: bool,
    login: login::State,
    quits: bool,
    notify: bool,
    /// They are on, and the system doesn't let the app.
    blocked: bool,
    /// Nothing is said here: a browser here may tell (speak.rs).
    browser: bool,
    machine: Option<String>,
    /// The Machine's browser goes out through this computer; None where the Machine has no such thing (exit.rs).
    exit: Option<bool>,
    /// A release's (crate::version).
    version: String,
    /// The version that is fetched and waits for a restart (updates.rs).
    update: Option<String>,
    /// A newer version that the package manager puts in place.
    out: Option<updates::Out>,
}

pub fn open(app: &AppHandle) {
    app.state::<Shared>().over_dash.store(true, Ordering::Relaxed); // the box closes to it
    windows::close_box(app);
    let window = match app.get_webview_window(LABEL) {
        Some(window) => {
            let _ = window.emit_to(LABEL, "settings", ());
            window
        }
        None => {
            let built = WebviewWindowBuilder::new(app, LABEL, WebviewUrl::App("settings.html".into()))
                .title("Settings")
                .inner_size(WIDTH, 300.0)
                .resizable(false)
                .maximizable(false)
                .minimizable(false)
                .center()
                .visible(false)
                .additional_browser_args(&windows::browser())
                .on_navigation(|url| url.scheme() == "tauri" || url.host_str() == Some("tauri.localhost"));
            #[cfg(target_os = "macos")]
            let built = built.title_bar_style(tauri::TitleBarStyle::Transparent);
            OPENING.store(true, Ordering::Relaxed);
            match built.build() {
                #[cfg(windows)]
                Ok(window) => return crate::windows_app::prepare(&window),
                #[cfg(target_os = "linux")]
                Ok(window) => return crate::linux_app::prepare(&window),
                #[cfg(target_os = "macos")]
                Ok(_) => return,
                Err(error) => return eprintln!("could not open settings: {error}"),
            }
        }
    };
    let _ = window.show();
    windows::front(&window);
}

#[tauri::command]
pub fn settings_fit(app: AppHandle, height: f64) {
    later(&app, move |app| {
        let Some(window) = app.get_webview_window(LABEL) else { return };
        let height = height.clamp(120.0, 700.0);
        *HEIGHT.lock().unwrap() = height;
        size(&window, height);
        if OPENING.swap(false, Ordering::Relaxed) {
            let _ = window.center();
            let _ = window.show();
            windows::front(&window);
        }
    });
}

#[cfg(target_os = "macos")]
fn size(window: &WebviewWindow, height: f64) {
    let _ = window.set_size(tauri::LogicalSize::new(WIDTH, height));
}

#[cfg(target_os = "linux")]
fn size(window: &WebviewWindow, height: f64) {
    windows::linux::size(window, crate::place::Rect { x: 0.0, y: 0.0, w: WIDTH, h: height });
}

/// Also as large as the person's Text size, while its monitor has room, and all of it there.
#[cfg(windows)]
fn size(window: &WebviewWindow, height: f64) {
    let Some(m) = window.current_monitor().ok().flatten().or(window.primary_monitor().ok().flatten()) else { return };
    let (work, plain) = (m.work_area(), m.scale_factor());
    let (wide, high) = (f64::from(work.size.width), f64::from(work.size.height));
    const TITLE: f64 = 48.0; // its title bar and edges
    let scale = windows::with_text(plain, wide, high).min((high - TITLE * plain) / height).max(plain);
    windows::draw_at(window, scale);
    let _ = window.set_size(tauri::PhysicalSize::new((WIDTH * scale).round(), (height * scale).round()));
    if let (Ok(at), Ok(outer)) = (window.outer_position(), window.outer_size()) {
        let inside = |at: i32, from: i32, size: u32, most: u32| at.min(from + most as i32 - size as i32).max(from);
        let to = tauri::PhysicalPosition::new(inside(at.x, work.position.x, outer.width, work.size.width), inside(at.y, work.position.y, outer.height, work.size.height));
        if to != at {
            let _ = window.set_position(to);
        }
    }
}

/// The text, the scale or a monitor is another one.
#[cfg(windows)]
pub fn again(app: &AppHandle) {
    if let Some(window) = app.get_webview_window(LABEL) {
        size(&window, *HEIGHT.lock().unwrap());
    }
}

#[tauri::command]
pub async fn settings_state(app: AppHandle) -> Result<Settings, String> {
    away(move || {
        let (login, notices) = (login::state(), notify::look());
        let shared = app.state::<Shared>();
        let saved = shared.saved.lock().unwrap();
        Ok(Settings {
            robot: !saved.no_robot,
            login,
            quits: saved.quits,
            notify: saved.notify == Some(true) && notices != notify::Lets::No,
            blocked: saved.notify == Some(true) && notices == notify::Lets::No,
            browser: shared.browser.load(Ordering::Relaxed) > 0 && (!saved.no_robot || saved.notify == Some(true) && notices == notify::Lets::Yes),
            machine: saved.machine.clone(),
            exit: (saved.machine.is_some() && saved.exit_at == saved.machine).then_some(!saved.no_exit),
            version: crate::version().to_string(),
            update: updates::ready(),
            out: updates::out(),
        })
    }).await
}

#[tauri::command]
pub async fn settings_set(app: AppHandle, id: String, on: bool) -> Result<(), String> {
    let shared = app.state::<Shared>();
    match id.as_str() {
        "robot" => {
            let mut saved = shared.saved.lock().unwrap();
            saved.no_robot = !on;
            // What it said is told another way, unless the person turned that off
            let tells = !on && saved.notify != Some(false);
            if tells {
                saved.notify = Some(true);
            }
            drop(saved);
            later(&app, robot);
            if tells {
                asks(&app);
            }
        }
        "login" => {
            if !away(move || Ok(login::set(on))).await? {
                return Err("login".into());
            }
        }
        "quits" => shared.saved.lock().unwrap().quits = on,
        // Off tells the Machine at once, so it doesn't ask for this computer
        "exit" => {
            shared.saved.lock().unwrap().no_exit = !on;
            crate::exit::set(on);
        }
        // The browser tells the Machine that it is here, as it opens; or none is
        "browser" if on => {
            let (machine, alone) = shared.signed_in().ok_or("notowner")?;
            return crate::open_outside(&app, &machine, alone, "");
        }
        "browser" => {
            let browser = shared.browser.swap(0, Ordering::Relaxed);
            let mut saved = shared.saved.lock().unwrap();
            saved.none = saved.none.max(browser);
        }
        "notify" => {
            shared.saved.lock().unwrap().notify = Some(on);
            if on {
                asks(&app);
            }
        }
        _ => return Err("failed".into()),
    }
    shared.save();
    shared.look_soon(); // whether it speaks
    notify::follow(&app);
    Ok(())
}

/// The system asks the person, when it hasn't before. The page shows what came of it.
fn asks(app: &AppHandle) {
    let app = app.clone();
    notify::ask(move || {
        app.state::<Shared>().look_soon();
        let _ = app.emit_to(LABEL, "settings", ());
    });
}

/// With the robot, or without one: then the app is its window only.
fn robot(app: &AppHandle) {
    let off = app.state::<Shared>().saved.lock().unwrap().no_robot;
    if off {
        windows::close_box(app);
        speak::hush(app, true);
        windows::show_or_not(app);
    } else {
        crate::show(app);
        windows::show_or_not(app); // not over the dashboard in front
    }
    crate::follow_tray(app);
}
