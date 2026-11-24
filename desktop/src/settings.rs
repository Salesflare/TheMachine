//! Settings, a small window of the app's own: the robot, starting at login, what closing the dashboard's window does, and
//! notifications when there is no robot. What the Machine itself does is set in the dashboard.
use crate::{away, later, login, notify, speak, windows, Shared};
use serde::Serialize;
use std::sync::atomic::Ordering;
use tauri::{AppHandle, Emitter, LogicalSize, Manager, WebviewUrl, WebviewWindowBuilder};

const LABEL: &str = "settings";
const WIDTH: f64 = 420.0;

#[derive(Serialize)]
pub struct Settings {
    robot: bool,
    login: login::State,
    quits: bool,
    notify: bool,
    /// The system has them here.
    can_notify: bool,
    /// They are on, and the system doesn't let the app.
    blocked: bool,
    /// Nothing is said here: a browser here may tell (speak.rs).
    browser: bool,
    machine: Option<String>,
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
                .visible(false) // until its page says how tall it is
                .additional_browser_args(&windows::browser())
                .on_navigation(|url| url.scheme() == "tauri" || url.host_str() == Some("tauri.localhost"));
            #[cfg(target_os = "macos")]
            let built = built.title_bar_style(tauri::TitleBarStyle::Transparent);
            match built.build() {
                #[cfg(windows)]
                Ok(window) => {
                    windows::no_menu(&window);
                    return;
                }
                #[cfg(not(windows))]
                Ok(_) => return,
                Err(error) => return eprintln!("could not open settings: {error}"),
            }
        }
    };
    let _ = window.show();
    let _ = window.set_focus();
}

#[tauri::command]
pub fn settings_fit(app: AppHandle, height: f64) {
    later(&app, move |app| {
        let Some(window) = app.get_webview_window(LABEL) else { return };
        let _ = window.set_size(LogicalSize::new(WIDTH, height.clamp(120.0, 700.0)));
        if !window.is_visible().unwrap_or(true) {
            let _ = window.center();
            let _ = window.show();
            let _ = window.set_focus();
        }
    });
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
            can_notify: notify::there(),
            blocked: saved.notify == Some(true) && notices == notify::Lets::No,
            browser: shared.browser.load(Ordering::Relaxed) > 0 && (!saved.no_robot || saved.notify == Some(true) && notices == notify::Lets::Yes),
            machine: saved.machine.clone(),
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
            let tells = !on && notify::there() && saved.notify != Some(false);
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
