//! Without a robot, what it would say comes as the system's own notification (speak.rs decides what and when, as for a
//! bubble). A tap opens its to-do. So far on a Mac.
use crate::{dash, later, Shared};
use std::sync::OnceLock;
use tauri::{AppHandle, Manager};

static APP: OnceLock<AppHandle> = OnceLock::new();

/// Whether this system has them here.
pub fn there() -> bool {
    cfg!(target_os = "macos")
}

pub fn start(app: &AppHandle) {
    let _ = APP.set(app.clone());
    #[cfg(target_os = "macos")]
    crate::mac_app::notices_start();
    follow(app);
}

/// The person wants them, instead of a robot.
fn wanted(shared: &Shared) -> bool {
    let saved = shared.saved.lock().unwrap();
    saved.no_robot && saved.notify && saved.machine.is_some()
}

/// Settings changed.
pub fn follow(app: &AppHandle) {
    #[cfg(target_os = "macos")]
    later(app, |app| crate::mac_app::awake(wanted(&app.state::<Shared>())));
    let _ = app;
}

/// It may tell now: the person wants it, the system lets it, and the dashboard isn't in front.
pub fn may(app: &AppHandle) -> bool {
    #[cfg(target_os = "macos")]
    crate::mac_app::notices_look(|_| {}); // as it is at the next look
    wanted(&app.state::<Shared>()) && allowed() && !dash::front()
}

pub fn allowed() -> bool {
    #[cfg(target_os = "macos")]
    return crate::mac_app::notices_allowed();
    #[cfg(not(target_os = "macos"))]
    false
}

/// The system asks the person, when it hasn't.
pub fn ask(told: impl Fn(bool) + Send + 'static) {
    #[cfg(target_os = "macos")]
    crate::mac_app::notices_ask(told);
    #[cfg(not(target_os = "macos"))]
    told(false);
}

pub fn show(id: &str, title: &str, line: &str) {
    #[cfg(target_os = "macos")]
    crate::mac_app::notice(id, title, line);
    #[cfg(not(target_os = "macos"))]
    let _ = (id, title, line);
}

/// Decided elsewhere: it needs no telling any more.
pub fn gone(id: &str) {
    #[cfg(target_os = "macos")]
    crate::mac_app::notice_gone(id);
    #[cfg(not(target_os = "macos"))]
    let _ = id;
}

/// One was tapped.
#[cfg_attr(not(target_os = "macos"), allow(dead_code))]
pub fn opened(id: &str) {
    if let (Some(app), Ok(())) = (APP.get(), crate::todo_id(id)) {
        let path = format!("#card={id}");
        later(app, move |app| {
            if app.state::<Shared>().machine().is_some() {
                dash::show(app, &path);
            }
        });
    }
}
