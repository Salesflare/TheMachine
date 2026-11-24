//! The robot speaks up: a small bubble above it when a to-do's notification would buzz on this computer, with the
//! notification's own buttons. Whether it does, and in what words, is the Machine's (its machine/delivery/desk.py): the
//! robot only says that it is there and may speak, with the look it takes anyway, and gets what waits for it. Then this
//! computer's browser doesn't get it too. A meeting with a briefing that starts in a few minutes is the Machine's word too.
use crate::machine::{Machine, Quick};
use crate::{later, windows, Shared};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::{BTreeSet, VecDeque};
use std::sync::atomic::Ordering;
use tauri::{AppHandle, Manager};

/// At most this many after another; the dot says there is more.
const QUEUE: usize = 3;

/// A meeting about to start, for the page to put in words.
#[derive(Clone, Serialize, Debug, Default, PartialEq)]
pub struct Meeting {
    pub at: String,
    /// The first guest's first name, or the meeting's own; empty when notifications hide what they are about.
    pub who: String,
    pub others: u64,
    pub join: bool,
}

/// One bubble. A meeting's is of its briefing to-do.
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
    pub meeting: Option<Meeting>,
    /// What Join opens: the page names no address.
    #[serde(skip)]
    pub link: Option<String>,
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
    /// The meetings it said.
    told: BTreeSet<String>,
}

/// When it speaks, as the person chose. That notifications are switched off on this computer says nothing of it: the
/// robot is something the person put there, and its bubble makes no sound.
#[derive(Clone, Copy, Debug, Default, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Speak {
    #[default]
    Always,
    /// Not in Do Not Disturb.
    Calm,
    Never,
}

impl Speak {
    fn now(self, disturb: impl FnOnce() -> bool) -> bool {
        match self {
            Speak::Always => true,
            Speak::Calm => !disturb(),
            Speak::Never => false,
        }
    }
}

/// It may speak: the person sees the robot, nothing is full screen or presented, the screen isn't locked, and they want it.
pub fn up(app: &AppHandle) -> bool {
    let shared = app.state::<Shared>();
    let may = showing(&shared) && !crate::front::full() && !quiet::away() && wants(&shared);
    #[cfg(feature = "sandbox")]
    if !may {
        eprintln!("doesn't speak: showing {}, full screen {}, away {}, do not disturb {}", showing(&shared), crate::front::full(), quiet::away(), quiet::disturb());
    }
    may
}

fn wants(shared: &Shared) -> bool {
    let when = shared.saved.lock().unwrap().speak;
    when.now(quiet::disturb)
}

fn showing(shared: &Shared) -> bool {
    let off = [&shared.hidden, &shared.away, &shared.full, &shared.picking].iter().any(|f| f.load(Ordering::Relaxed));
    !off && shared.saved.lock().unwrap().speak != Speak::Never
}

/// What came with a look. Asked of the Machine once more, as the phone app does: its words, and its buttons now.
pub fn came(app: &AppHandle, machine: &Machine, notices: &Value, meeting: &Value) {
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
        let soon = about(meeting).filter(|(key, _)| speaking.told.insert(key.clone())).map(|(_, say)| say);
        for say in said.into_iter().rev().chain(soon) {
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

/// The meeting that starts soon, and what it is told once by: one that is moved is told again.
fn about(meeting: &Value) -> Option<(String, Say)> {
    let words = |key: &str| meeting[key].as_str().unwrap_or_default().split_whitespace().collect::<Vec<_>>().join(" ").chars().filter(|c| !c.is_control()).take(60).collect::<String>();
    let id = meeting["id"].as_str().filter(|id| crate::todo_id(id).is_ok())?.to_string();
    let (at, link) = (words("at"), meeting["join"].as_str().filter(|l| crate::address::call(l)).map(String::from));
    let of = Meeting { who: words("who"), others: meeting["others"].as_u64().unwrap_or(0), join: link.is_some(), at: at.clone() };
    (!at.is_empty()).then(|| (format!("{} {at}", meeting["event"]), Say { id, meeting: Some(of), link, ..Say::default() }))
}

/// Join was tapped: that meeting's link.
pub fn link(shared: &Shared, todo: &str) -> Option<String> {
    shared.speaking.lock().unwrap().now.as_ref().filter(|say| say.id == todo)?.link.clone()
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
    shared.speaking.lock().unwrap().queue.retain(|s| s.meeting.is_some() || !rows.contains(&s.id));
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

/// What the system tells without asking for a permission. `away`: the screen is locked, something is presented, or nobody
/// is there; it never speaks then. `disturb`: the person switched Do Not Disturb on.
mod quiet {
    #[cfg(target_os = "linux")]
    mod bus {
        use zbus::blocking::{connection::Builder, fdo::DBusProxy, Connection, Proxy};

        /// One that hangs doesn't hold up the look.
        fn soon(builder: zbus::Result<Builder<'static>>) -> Option<Connection> {
            builder.and_then(|b| b.method_timeout(std::time::Duration::from_secs(2)).build()).ok()
        }

        fn read(bus: &Connection, service: &'static str, path: &'static str, interface: &'static str, name: &'static str) -> bool {
            Proxy::new(bus, service, path, interface).ok().and_then(|p| p.get_property::<bool>(name).ok()).unwrap_or(false)
        }

        /// The sign-in manager says (GNOME, KDE, and lockers that tell it).
        pub fn locked() -> bool {
            soon(Builder::system()).is_some_and(|bus| read(&bus, "org.freedesktop.login1", "/org/freedesktop/login1/session/auto", "org.freedesktop.login1.Session", "LockedHint"))
        }

        /// KDE, then dunst, then mako. None of them running tells nothing.
        pub fn disturb() -> bool {
            const SHOWS: &str = "org.freedesktop.Notifications";
            let Some(bus) = soon(Builder::session()) else { return false };
            let there = DBusProxy::new(&bus).ok().and_then(|d| d.name_has_owner(SHOWS.try_into().ok()?).ok()).unwrap_or(false); // never started by this
            there
                && (read(&bus, SHOWS, "/org/freedesktop/Notifications", SHOWS, "Inhibited")
                    || read(&bus, SHOWS, "/org/freedesktop/Notifications", "org.dunstproject.cmd0", "paused")
                    || Proxy::new(&bus, SHOWS, "/fr/emersion/Mako", "fr.emersion.Mako").ok()
                        .and_then(|p| p.call::<_, _, Vec<String>>("ListModes", &()).ok())
                        .is_some_and(|modes| modes.iter().any(|m| m == "do-not-disturb" || m == "dnd")))
        }
    }

    #[cfg(target_os = "linux")]
    pub fn away() -> bool {
        bus::locked()
    }

    #[cfg(target_os = "linux")]
    pub fn disturb() -> bool {
        bus::disturb() || gnome()
    }

    /// Its Do Not Disturb. That an app's own notifications are off is elsewhere, and not read.
    #[cfg(target_os = "linux")]
    fn gnome() -> bool {
        use gtk::gio::{prelude::*, Settings, SettingsSchemaSource};
        const SCHEMA: &str = "org.gnome.desktop.notifications";
        std::env::var("XDG_CURRENT_DESKTOP").is_ok_and(|d| d.to_uppercase().contains("GNOME"))
            && SettingsSchemaSource::default().and_then(|s| s.lookup(SCHEMA, true)).is_some_and(|s| s.has_key("show-banners"))
            && !Settings::new(SCHEMA).boolean("show-banners")
    }

    /// Locked or the screen saver (1), an app or a game in full screen (2, 3), a presentation (4), the screen shown twice; or
    /// nothing was touched for five minutes. That the screen is shared in a call Windows doesn't tell.
    #[cfg(windows)]
    pub fn away() -> bool {
        use windows_sys::Win32::System::SystemInformation::GetTickCount;
        use windows_sys::Win32::UI::Input::KeyboardAndMouse::{GetLastInputInfo, LASTINPUTINFO};
        let mut last = LASTINPUTINFO { cbSize: std::mem::size_of::<LASTINPUTINFO>() as u32, dwTime: 0 };
        // SAFETY: the one argument is a valid place for the answer.
        let idle = unsafe { GetLastInputInfo(&mut last) != 0 && GetTickCount().wrapping_sub(last.dwTime) > 5 * 60 * 1000 };
        let (state, _, doubled) = says();
        idle || doubled || (1..=4).contains(&state)
    }

    /// Do Not Disturb (Windows 11; Focus turns it on too): only priority notifications, or only alarms. Not the switch that
    /// turns notifications off: that one changes neither answer. Also a new person's first hour, which Windows keeps quiet.
    #[cfg(windows)]
    pub fn disturb() -> bool {
        let (state, mode, _) = says();
        state == 6 || mode != 0
    }

    /// Windows' word: SHQueryUserNotificationState, the notification mode (0 where it has none: Windows 10), and whether the
    /// displays are duplicated.
    #[cfg(windows)]
    fn says() -> (i32, i32, bool) {
        use windows::UI::Notifications::ToastNotificationManager;
        use windows_sys::Win32::UI::Shell::{SHQueryUserNotificationState, QUNS_ACCEPTS_NOTIFICATIONS};
        #[cfg(feature = "sandbox")]
        if let Some(said) = std::env::var("MACHINE_SANDBOX_STATE").ok().and_then(|f| std::fs::read_to_string(f).ok()) {
            let mut said = said.split_whitespace().filter_map(|n| n.parse().ok());
            return (said.next().unwrap_or(5), said.next().unwrap_or(0), said.next() == Some(1));
        }
        let mut state = QUNS_ACCEPTS_NOTIFICATIONS;
        // SAFETY: the one argument is a valid place for the answer.
        if unsafe { SHQueryUserNotificationState(&mut state) } != 0 {
            state = QUNS_ACCEPTS_NOTIFICATIONS;
        }
        let mode = ToastNotificationManager::GetDefault().and_then(|m| m.NotificationMode()).map_or(0, |m| m.0);
        (state, mode, doubled())
    }

    #[cfg(windows)]
    fn doubled() -> bool {
        use windows_sys::Win32::Devices::Display::{
            GetDisplayConfigBufferSizes, QueryDisplayConfig, DISPLAYCONFIG_MODE_INFO, DISPLAYCONFIG_PATH_INFO, DISPLAYCONFIG_TOPOLOGY_CLONE, QDC_DATABASE_CURRENT,
        };
        let (mut paths, mut modes, mut how) = (0, 0, 0);
        // SAFETY: plain numbers and structs of numbers, in buffers of the sizes asked for.
        unsafe {
            if GetDisplayConfigBufferSizes(QDC_DATABASE_CURRENT, &mut paths, &mut modes) != 0 {
                return false;
            }
            let mut path: Vec<DISPLAYCONFIG_PATH_INFO> = vec![std::mem::zeroed(); paths as usize];
            let mut mode: Vec<DISPLAYCONFIG_MODE_INFO> = vec![std::mem::zeroed(); modes as usize];
            QueryDisplayConfig(QDC_DATABASE_CURRENT, &mut paths, path.as_mut_ptr(), &mut modes, mode.as_mut_ptr(), &mut how) == 0 && how == DISPLAYCONFIG_TOPOLOGY_CLONE
        }
    }

    /// Locked, the screen shown twice, or nothing was touched for five minutes. Full screen is front::full.
    #[cfg(target_os = "macos")]
    pub fn away() -> bool {
        use objc2_foundation::{ns_string, NSDictionary, NSNumber, NSString};
        #[link(name = "CoreGraphics", kind = "framework")]
        extern "C" {
            fn CGEventSourceSecondsSinceLastEventType(source: i32, event: u32) -> f64;
            fn CGSessionCopyCurrentDictionary() -> *mut NSDictionary<NSString>;
            fn CGGetOnlineDisplayList(most: u32, displays: *mut u32, count: *mut u32) -> i32;
            fn CGDisplayIsInMirrorSet(display: u32) -> u32;
        }
        let (mut displays, mut count) = ([0; 16], 0);
        // SAFETY: plain calls, the list with its own size; the dictionary is this one's own, or nothing.
        unsafe {
            let locked = objc2::rc::Retained::from_raw(CGSessionCopyCurrentDictionary())
                .and_then(|s| s.objectForKey(ns_string!("CGSSessionScreenIsLocked")))
                .and_then(|v| v.downcast::<NSNumber>().ok())
                .is_some_and(|v| v.boolValue());
            let told = CGGetOnlineDisplayList(16, displays.as_mut_ptr(), &mut count) == 0;
            let twice = told && displays.iter().take(count as usize).any(|d| CGDisplayIsInMirrorSet(*d) != 0);
            locked || twice || CGEventSourceSecondsSinceLastEventType(0, u32::MAX) > 5.0 * 60.0
        }
    }

    /// Whether a Focus is on, macOS only tells with a permission: the box doesn't offer the choice there.
    #[cfg(target_os = "macos")]
    pub fn disturb() -> bool {
        false
    }

    #[cfg(not(any(windows, target_os = "linux", target_os = "macos")))]
    pub fn away() -> bool {
        false
    }

    #[cfg(not(any(windows, target_os = "linux", target_os = "macos")))]
    pub fn disturb() -> bool {
        false
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn it_speaks_as_chosen() {
        let says = |when: &str, disturb: bool| serde_json::from_value::<Speak>(json!(when)).unwrap().now(|| disturb);
        assert!(says("always", true) && says("always", false));
        assert!(!says("calm", true) && says("calm", false));
        assert!(!says("never", true) && !says("never", false));
        assert_eq!(Speak::default(), Speak::Always);
    }

    #[test]
    fn what_it_has_already_is_not_said_again() {
        let offered = json!([{"key": "a1", "id": "x"}, {"key": "b2", "id": "x"}, {"id": "no-key"}, {"key": "&up=0", "id": "x"}]);
        let (kept, fresh) = sort(&["a1".into(), "gone".into()], &offered);
        assert_eq!((kept, fresh), (vec!["a1".to_string()], vec![json!({"key": "b2", "id": "x"})]));
        assert_eq!(sort(&["a1".into()], &json!([])), (vec![], vec![]));
    }

    #[test]
    fn a_meeting_and_its_link() {
        let meeting = json!({"id": "aa01", "event": 7, "at": "2026-11-24T10:00:00+00:00", "who": " Dana\n", "others": 2, "join": "https://zoom.us/j/1"});
        let (key, say) = about(&meeting).unwrap();
        assert_eq!(key, "7 2026-11-24T10:00:00+00:00");
        assert_eq!(say.meeting, Some(Meeting { at: "2026-11-24T10:00:00+00:00".into(), who: "Dana".into(), others: 2, join: true }));
        assert_eq!(say.link.as_deref(), Some("https://zoom.us/j/1"));
        let with = |key: &str, value: Value| { let mut m = meeting.clone(); m[key] = value; about(&m) };
        let (_, other) = with("join", json!("https://zoom.us.example.com/j/1")).unwrap();
        assert!(other.link.is_none() && !other.meeting.unwrap().join);
        assert!(with("id", json!("../x")).is_none() && with("at", Value::Null).is_none() && about(&Value::Null).is_none());
    }
}
