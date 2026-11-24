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
    /// The system has them and lets the app.
    can_notify: bool,
    allowed: bool,
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
                .on_navigation(|url| url.scheme() == "tauri" || url.host_str() == Some("tauri.localhost"))
                .build();
            match built {
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
        let login = login::state();
        let shared = app.state::<Shared>();
        let saved = shared.saved.lock().unwrap();
        Ok(Settings {
            robot: !saved.no_robot,
            login,
            quits: saved.quits,
            notify: saved.notify && notify::allowed(),
            can_notify: notify::there(),
            allowed: notify::allowed(),
            machine: saved.machine.clone(),
        })
    }).await
}

#[tauri::command]
pub async fn settings_set(app: AppHandle, id: String, on: bool) -> Result<(), String> {
    let shared = app.state::<Shared>();
    match id.as_str() {
        "robot" => {
            shared.saved.lock().unwrap().no_robot = !on;
            later(&app, robot);
        }
        "login" => {
            if !away(move || Ok(login::set(on))).await? {
                return Err("login".into());
            }
        }
        "quits" => shared.saved.lock().unwrap().quits = on,
        "notify" => {
            if on {
                let (tell, told) = std::sync::mpsc::channel();
                notify::ask(move |yes| { let _ = tell.send(yes); });
                if !away(move || told.recv().map_err(|_| "failed".to_string())).await? {
                    return Err("notify".into());
                }
            }
            shared.saved.lock().unwrap().notify = on;
        }
        _ => return Err("failed".into()),
    }
    shared.save();
    shared.look_soon(); // whether it speaks
    notify::follow(&app);
    Ok(())
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
