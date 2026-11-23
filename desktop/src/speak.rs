//! The robot speaks up: a small bubble above it when a to-do's notification would buzz on this computer, with the
//! notification's own buttons. Whether it does, and in what words, is the Machine's (its machine/delivery/desk.py): the
//! robot only says that it is there and may speak, with the look it takes anyway, and gets what waits for it. Then this
//! computer's browser doesn't get it too.
use crate::machine::{Machine, Quick};
use crate::{later, windows, Shared};
use serde::Serialize;
use serde_json::Value;
use std::collections::VecDeque;
use std::sync::atomic::Ordering;
use tauri::{AppHandle, Manager};

/// At most this many after another; the dot says there is more.
const QUEUE: usize = 3;

/// One bubble.
#[derive(Clone, Serialize, Debug, Default, PartialEq)]
pub struct Say {
    pub id: String,
    pub title: String,
    pub line: String,
    /// The name of the button that opens it, in the Machine's words: Open, Open draft, Answer, Sign in.
    pub opens: String,
    pub quick: Vec<Quick>,
    /// What Snooze offers: each with its name, as the dashboard's.
    pub snooze: Vec<(String, String)>,
    /// It was in For you since: gone from there, it goes too.
    #[serde(skip)]
    pub listed: bool,
    /// A button of it was tapped: it says what happened first.
    #[serde(skip)]
    pub held: bool,
}

#[derive(Default)]
pub struct Speaking {
    queue: VecDeque<Say>,
    now: Option<Say>,
    /// The notifications it has (the Machine's keys of them), until the Machine no longer offers them: an answer can be
    /// lost on the way, so the Machine keeps each until a look names it.
    got: Vec<String>,
}

/// It may speak: the person sees the robot, and nothing says not to disturb them.
pub fn up(app: &AppHandle) -> bool {
    let shared = app.state::<Shared>();
    let may = showing(&shared) && !crate::front::full() && !quiet::now();
    #[cfg(feature = "sandbox")]
    if !may {
        eprintln!("doesn't speak: showing {}, full screen {}, quiet {}", showing(&shared), crate::front::full(), quiet::now());
    }
    may
}

fn showing(shared: &Shared) -> bool {
    let off = [&shared.hidden, &shared.away, &shared.full, &shared.picking].iter().any(|f| f.load(Ordering::Relaxed));
    !off && !shared.saved.lock().unwrap().quiet
}

/// What came with a look. Asked of the Machine once more, as the phone app does: its words, and its buttons now.
pub fn came(app: &AppHandle, machine: &Machine, notices: &Value) {
    if notices.is_null() || !up(app) {
        return;
    }
    let shared = app.state::<Shared>();
    let (mut got, fresh) = sort(&got(&shared), notices);
    let before = got.len();
    let mut said = Vec::new();
    for (i, n) in fresh.iter().rev().enumerate() {
        if i < QUEUE {
            match machine.notice(n["id"].as_str().unwrap_or_default(), n["kind"].as_str().unwrap_or_default()) {
                Ok(Some(say)) => said.push(Say { snooze: serde_json::from_value(n["snooze"].clone()).unwrap_or_default(), ..say }),
                Ok(None) => {}
                Err(_) => continue, // the next look gets it again
            }
        }
        got.extend(n["key"].as_str().map(String::from));
    }
    let told = got.len() > before;
    shared.speaking.lock().unwrap().got = got;
    {
        let mut speaking = shared.speaking.lock().unwrap();
        for say in said.into_iter().rev() {
            speaking.queue.retain(|s| s.id != say.id);
            speaking.queue.push_back(say);
            while speaking.queue.len() > QUEUE {
                speaking.queue.pop_front();
            }
        }
    }
    if told {
        shared.look_soon(); // it says so right away: then the browser doesn't get it too when the computer sleeps meanwhile
    }
    later(app, next);
}

pub fn got(shared: &Shared) -> Vec<String> {
    shared.speaking.lock().unwrap().got.clone()
}

/// Of what the Machine offers: the keys of what the robot has already, and the rest.
fn sort(got: &[String], offered: &Value) -> (Vec<String>, Vec<Value>) {
    let key = |n: &Value| n["key"].as_str().filter(|k| !k.is_empty() && k.len() <= 32 && k.bytes().all(|b| b.is_ascii_alphanumeric())).map(String::from);
    let (mut kept, mut fresh) = (Vec::new(), Vec::new());
    for n in offered.as_array().into_iter().flatten().take(50) {
        match key(n) {
            Some(k) if got.contains(&k) => kept.push(k),
            Some(_) => fresh.push(n.clone()),
            None => {}
        }
    }
    (kept, fresh)
}

/// The next one, when none is there. While the box is open it waits: what is among the box's rows needs no bubble after.
fn next(app: &AppHandle) {
    let shared = app.state::<Shared>();
    {
        let mut speaking = shared.speaking.lock().unwrap();
        if speaking.now.is_some() || windows::box_open(app) || !showing(&shared) {
            return;
        }
        let Some(say) = speaking.queue.pop_front() else { return };
        speaking.now = Some(say);
    }
    windows::open_bubble(app);
}

/// What the bubble says now.
pub fn now(shared: &Shared) -> Option<Say> {
    shared.speaking.lock().unwrap().now.clone()
}

/// A button of it was tapped.
pub fn hold(shared: &Shared) {
    if let Some(say) = &mut shared.speaking.lock().unwrap().now {
        say.held = true;
    }
}

/// The bubble's done; another may wait.
pub fn done(app: &AppHandle) {
    if app.state::<Shared>().speaking.lock().unwrap().now.take().is_some() {
        windows::close_bubble(app);
        let app = app.clone();
        std::thread::spawn(move || {
            std::thread::sleep(std::time::Duration::from_millis(600));
            later(&app, next);
        });
    }
}

/// The box opened: what is said now, it says. Or the robot goes: nothing more is said. The dot still tells.
pub fn hush(app: &AppHandle, all: bool) {
    let shared = app.state::<Shared>();
    let there = {
        let mut speaking = shared.speaking.lock().unwrap();
        if all {
            speaking.queue.clear();
        }
        speaking.now.take().is_some()
    };
    if there {
        windows::close_bubble(app);
    }
}

/// The box closed: its rows were seen.
pub fn closed(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let rows: Vec<String> = shared.waiting.lock().unwrap().todos.iter().filter_map(|t| t.id.clone()).collect();
    shared.speaking.lock().unwrap().queue.retain(|s| !rows.contains(&s.id));
    later(app, next);
}

/// What is in For you now: one that was there and went (decided here or on another device) isn't said any more.
pub fn follow(app: &AppHandle, marks: &[crate::seen::Mark]) {
    let there = |id: &str| marks.iter().any(|(name, _)| name.split('@').next() == Some(id));
    let gone = {
        let shared = app.state::<Shared>();
        let mut speaking = shared.speaking.lock().unwrap();
        let mut stays = |say: &mut Say| {
            let here = there(&say.id);
            let stays = here || !say.listed;
            say.listed |= here;
            stays
        };
        speaking.queue.retain_mut(&mut stays);
        speaking.now.as_mut().is_some_and(|say| !stays(say) && !say.held)
    };
    if gone {
        done(app);
    }
}

/// Whether the system says not to disturb, or nobody is there, where it tells without asking for a permission.
mod quiet {
    #[cfg(target_os = "linux")]
    pub fn now() -> bool {
        use zbus::blocking::{connection::Builder, fdo::DBusProxy, Connection, Proxy};
        let read = |bus: &Connection, service: &'static str, path: &'static str, interface: &'static str, name: &'static str| {
            Proxy::new(bus, service, path, interface).ok().and_then(|p| p.get_property::<bool>(name).ok()).unwrap_or(false)
        };
        let soon = std::time::Duration::from_secs(2); // one that hangs doesn't hold up the look
        // Locked: the sign-in manager says (GNOME, KDE, and lockers that tell it)
        if Builder::system().and_then(|b| b.method_timeout(soon).build()).is_ok_and(|bus| read(&bus, "org.freedesktop.login1", "/org/freedesktop/login1/session/auto", "org.freedesktop.login1.Session", "LockedHint")) {
            return true;
        }
        const SHOWS: &str = "org.freedesktop.Notifications";
        if let Ok(bus) = Builder::session().and_then(|b| b.method_timeout(soon).build()) {
            let there = DBusProxy::new(&bus).ok().and_then(|d| d.name_has_owner(SHOWS.try_into().ok()?).ok()).unwrap_or(false); // never started by this
            // KDE, then dunst, then mako
            if there
                && (read(&bus, SHOWS, "/org/freedesktop/Notifications", SHOWS, "Inhibited")
                    || read(&bus, SHOWS, "/org/freedesktop/Notifications", "org.dunstproject.cmd0", "paused")
                    || Proxy::new(&bus, SHOWS, "/fr/emersion/Mako", "fr.emersion.Mako").ok()
                        .and_then(|p| p.call::<_, _, Vec<String>>("ListModes", &()).ok())
                        .is_some_and(|modes| modes.iter().any(|m| m == "do-not-disturb" || m == "dnd")))
            {
                return true;
            }
        }
        gnome()
    }

    #[cfg(target_os = "linux")]
    fn gnome() -> bool {
        use gtk::gio::{prelude::*, Settings, SettingsSchemaSource};
        const SCHEMA: &str = "org.gnome.desktop.notifications";
        std::env::var("XDG_CURRENT_DESKTOP").is_ok_and(|d| d.to_uppercase().contains("GNOME"))
            && SettingsSchemaSource::default().and_then(|s| s.lookup(SCHEMA, true)).is_some_and(|s| s.has_key("show-banners"))
            && !Settings::new(SCHEMA).boolean("show-banners")
    }

    /// Locked, the screen saver, a game, a presentation, or quiet time; or nothing was touched for five minutes.
    #[cfg(windows)]
    pub fn now() -> bool {
        use windows_sys::Win32::System::SystemInformation::GetTickCount;
        use windows_sys::Win32::UI::Input::KeyboardAndMouse::{GetLastInputInfo, LASTINPUTINFO};
        use windows_sys::Win32::UI::Shell::{SHQueryUserNotificationState, QUNS_ACCEPTS_NOTIFICATIONS};
        let mut state = QUNS_ACCEPTS_NOTIFICATIONS;
        #[cfg(feature = "sandbox")]
        if let Some(said) = std::env::var("MACHINE_SANDBOX_STATE").ok().and_then(|f| std::fs::read_to_string(f).ok()?.trim().parse::<i32>().ok()) {
            return quiet(said);
        }
        let mut last = LASTINPUTINFO { cbSize: std::mem::size_of::<LASTINPUTINFO>() as u32, dwTime: 0 };
        // SAFETY: the one argument of each is a valid place for the answer.
        unsafe {
            let told = SHQueryUserNotificationState(&mut state) == 0;
            let idle = GetLastInputInfo(&mut last) != 0 && GetTickCount().wrapping_sub(last.dwTime) > 5 * 60 * 1000;
            told && quiet(state) || idle
        }
    }

    #[cfg(windows)]
    fn quiet(state: i32) -> bool {
        use windows_sys::Win32::UI::Shell::{QUNS_ACCEPTS_NOTIFICATIONS, QUNS_APP};
        state != QUNS_ACCEPTS_NOTIFICATIONS && state != QUNS_APP
    }

    #[cfg(not(any(windows, target_os = "linux")))]
    pub fn now() -> bool {
        false
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn what_it_has_already_is_not_said_again() {
        let offered = json!([{"key": "a1", "id": "x"}, {"key": "b2", "id": "x"}, {"id": "no-key"}, {"key": "&up=0", "id": "x"}]);
        let (kept, fresh) = sort(&["a1".into(), "gone".into()], &offered);
        assert_eq!((kept, fresh), (vec!["a1".to_string()], vec![json!({"key": "b2", "id": "x"})]));
        assert_eq!(sort(&["a1".into()], &json!([])), (vec![], vec![]));
    }
}
