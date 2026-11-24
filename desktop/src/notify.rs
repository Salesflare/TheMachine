//! Without a robot, what it would say comes as the system's own notification (speak.rs decides what and when, as for a
//! bubble). A tap opens its to-do.
use crate::{dash, later, Shared};
use std::sync::OnceLock;
use tauri::{AppHandle, Manager};

#[cfg(target_os = "linux")]
use crate::linux_app as system;
#[cfg(target_os = "macos")]
use crate::mac_app as system;
#[cfg(windows)]
use crate::windows_app as system;

static APP: OnceLock<AppHandle> = OnceLock::new();

/// The notification that asks whether a browser here tells too (speak.rs). A tap opens Settings.
pub const ASKS: &str = "browser";

/// Whether the system lets the app.
#[derive(Clone, Copy, Debug, PartialEq)]
#[cfg_attr(not(target_os = "macos"), allow(dead_code))]
pub enum Lets {
    /// It hasn't asked the person.
    Unasked,
    Yes,
    No,
}

pub fn start(app: &AppHandle) {
    let _ = APP.set(app.clone());
    #[cfg(target_os = "macos")]
    system::notices_start();
    follow(app);
}

/// The person wants them, instead of a robot.
fn wanted(shared: &Shared) -> bool {
    let saved = shared.saved.lock().unwrap();
    saved.no_robot && saved.notify == Some(true) && saved.machine.is_some()
}

/// Settings changed, or who is signed in.
pub fn follow(app: &AppHandle) {
    #[cfg(target_os = "macos")]
    later(app, |app| system::awake(wanted(&app.state::<Shared>())));
    #[cfg(not(target_os = "macos"))]
    system::notices_on(app, wanted(&app.state::<Shared>()));
}

/// It may tell now: the person wants it, the system lets it, and the dashboard isn't in front.
pub fn may(app: &AppHandle) -> bool {
    #[cfg(target_os = "macos")]
    system::notices_look(|| {}); // as it is at the next look
    wanted(&app.state::<Shared>()) && system::notices_lets() == Lets::Yes && !dash::front()
}

/// As it is now. Not on the main thread.
pub fn look() -> Lets {
    #[cfg(target_os = "macos")]
    {
        let (tell, told) = std::sync::mpsc::channel();
        system::notices_look(move || { let _ = tell.send(()); });
        let _ = told.recv_timeout(std::time::Duration::from_secs(1));
    }
    system::notices_lets()
}

/// The system asks the person, when it hasn't: only a Mac's does.
pub fn ask(told: impl Fn() + Send + 'static) {
    #[cfg(target_os = "macos")]
    system::notices_ask(told);
    #[cfg(not(target_os = "macos"))]
    told();
}

pub fn show(id: &str, title: &str, line: &str) {
    system::notice(id, title, line);
}

/// Decided elsewhere: it needs no telling any more.
pub fn gone(id: &str) {
    system::notice_gone(id);
}

/// The app quits. A Mac starts it again for a tap; elsewhere nothing would answer one.
pub fn quits() {
    #[cfg(not(target_os = "macos"))]
    system::notices_clear();
}

/// One was tapped.
pub fn opened(id: &str) {
    if let (Some(app), ASKS) = (APP.get(), id) {
        return later(app, crate::settings::open);
    }
    if let (Some(app), Ok(())) = (APP.get(), crate::todo_id(id)) {
        let path = format!("#card={id}");
        later(app, move |app| {
            if app.state::<Shared>().machine().is_some() {
                dash::show(app, &path);
            }
        });
    }
}
