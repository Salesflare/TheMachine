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
use std::time::{Duration, Instant};
use tauri::{AppHandle, Emitter, Manager};

/// At most this many after another; the dot says there is more.
const QUEUE: usize = 3;
/// A bubble shows this long after the look the Machine offered it with, or after another look: not next to the browser's.
const FRESH: Duration = Duration::from_secs(5);
/// The bubble's page that hasn't shown it by then, or hasn't said it is there since, is made again.
const SLOW: Duration = Duration::from_secs(10);
const DEAD: Duration = Duration::from_secs(90);

/// A meeting about to start, for the page to put in words.
#[derive(Clone, Serialize, Debug, Default, PartialEq)]
pub struct Meeting {
    pub at: String,
    /// The first guest's first name; empty when none has one, or notifications hide what they are about.
    pub who: String,
    pub others: u64,
    /// The meeting's own name, '' as above. None from a Machine that says it in who.
    pub title: Option<String>,
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
    /// The Machine's key of the notification, or what its meeting is told once by.
    #[serde(skip)]
    pub key: Option<String>,
    #[serde(skip)]
    pub told: Option<String>,
}

#[derive(Default)]
pub struct Speaking {
    queue: VecDeque<Say>,
    now: Option<Say>,
    /// What is said now shows, and when its page last said it is there.
    shown: bool,
    alive: Option<Instant>,
    /// When the Machine last said what it offers.
    asked: Option<Instant>,
    /// Why it may not speak, as it was last noted.
    no: Option<Option<&'static str>>,
    /// The notifications that were shown or are gone (the Machine's keys of them), until the Machine no longer offers them: an answer can be
    /// lost on the way, so the Machine keeps each until a look names it.
    got: Vec<String>,
    /// What the system told (notify.rs), and whether it was in For you since.
    notices: Vec<(Say, bool)>,
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
    let no = why_not(app, &shared);
    let changed = std::mem::replace(&mut shared.speaking.lock().unwrap().no, Some(no)) != Some(no);
    if changed {
        note(&shared, &no.map_or("may speak".into(), |no| format!("may not speak: {no}")));
        #[cfg(feature = "sandbox")]
        eprintln!("speaks: {}", no.unwrap_or("yes"));
    }
    no.is_none()
}

fn why_not(app: &AppHandle, shared: &Shared) -> Option<&'static str> {
    let off = |flag: &std::sync::atomic::AtomicBool| flag.load(Ordering::Relaxed);
    if no_robot(shared) { // else the phone and the browser have it
        return if !crate::notify::may(app) { Some("no robot, and notifications are off") } else { quiet::away().then_some("locked, presented, mirrored or idle") };
    }
    let when = shared.saved.lock().unwrap().speak;
    Some(match () {
        _ if when == Speak::Never => "Speak up is off",
        _ if off(&shared.hidden) => "the robot is hidden",
        _ if off(&shared.away) || crate::dash::front() => "the dashboard's app is in front",
        _ if off(&shared.full) || crate::front::full() => "something is full screen",
        _ if off(&shared.picking) => "a screenshot is being taken",
        _ if quiet::away() => "locked, presented, mirrored or idle",
        _ if !when.now(quiet::disturb) => "Do Not Disturb",
        _ => return None,
    })
}

/// For the person who wonders why it said nothing (why.rs). Reasons only.
fn note(shared: &Shared, reason: &str) {
    crate::why::note(&shared.file.with_file_name(crate::why::NAME), reason);
}

fn no_robot(shared: &Shared) -> bool {
    shared.saved.lock().unwrap().no_robot
}

fn showing(shared: &Shared) -> bool {
    let off = [&shared.hidden, &shared.away, &shared.full, &shared.picking].iter().any(|f| f.load(Ordering::Relaxed));
    !off && !crate::dash::front() && shared.saved.lock().unwrap().speak != Speak::Never
}

impl Speaking {
    /// What the Machine offers with a look: what isn't here yet. What it no longer offers is the browser's now, or a newer
    /// one took its place: that isn't said any more. Also how many those are.
    fn offered(&mut self, notices: &Value, meeting: Option<&str>, at: Instant) -> (Vec<Value>, usize) {
        let before = self.queue.len();
        let (kept, mut fresh) = sort(&self.got, notices);
        let open = |key: &str| fresh.iter().any(|n| n["key"] == key);
        self.queue.retain(|s| s.key.as_deref().map_or(s.told.as_deref() == meeting, open));
        fresh.retain(|n| !self.queue.iter().chain(&self.now).any(|s| s.key.as_deref() == n["key"].as_str()));
        self.got = kept;
        self.asked = Some(at);
        (fresh, before - self.queue.len())
    }

    fn room(&self) -> usize {
        QUEUE.saturating_sub(self.queue.len())
    }

    fn add(&mut self, say: Say) {
        self.queue.retain(|s| s.id != say.id);
        self.queue.push_back(say);
    }

    /// It was shown, or it is really gone: the Machine hears so with the next look.
    fn had(&mut self, say: &Say) {
        self.got.extend(say.key.clone().filter(|k| !self.got.contains(k)));
        self.told.extend(say.told.clone());
    }

    /// The next one, if the Machine offered it a moment ago: else the browser may have it by now.
    fn pop(&mut self, at: Instant) -> Option<&Say> {
        if !self.asked.is_some_and(|asked| at.duration_since(asked) < FRESH) {
            return None;
        }
        self.now = self.queue.pop_front();
        (self.shown, self.alive) = (false, Some(at));
        self.now.as_ref()
    }

    /// The bubble's page is gone or never came: it says it is there every few seconds (ui/bubble.js).
    fn stuck(&self, at: Instant) -> bool {
        self.now.is_some() && self.alive.is_some_and(|alive| at.duration_since(alive) > if self.shown { DEAD } else { SLOW })
    }

    /// The rows of the box were seen, so these are. The rest waited for a while: it is asked for again first (pop).
    fn seen(&mut self, rows: &[String]) -> usize {
        self.asked = None;
        let before = self.queue.len();
        let (seen, rest) = std::mem::take(&mut self.queue).into_iter().partition::<Vec<_>, _>(|s| s.meeting.is_none() && rows.contains(&s.id));
        self.queue = rest.into();
        seen.iter().for_each(|s| self.had(s));
        before - self.queue.len()
    }

    /// What is decided elsewhere isn't said. Also whether that is what it says now.
    fn decided(&mut self, there: impl Fn(&str) -> bool) -> bool {
        let stays = |say: &mut Say| {
            let here = there(&say.id);
            let stays = here || !say.listed;
            say.listed |= here;
            stays
        };
        let (rest, gone) = std::mem::take(&mut self.queue).into_iter().map(|mut s| (stays(&mut s), s)).partition::<Vec<_>, _>(|(stays, _)| *stays);
        self.queue = rest.into_iter().map(|(_, s)| s).collect();
        gone.iter().for_each(|(_, s)| self.had(s));
        self.now.as_mut().is_some_and(|say| !stays(say) && !say.held)
    }
}

/// Whether the Machine keeps it quiet here because a browser that may be on this computer has notifications on (its
/// number of those, or 0). Settings asks the person. Without a robot a notification says so, once: nothing else would.
pub fn unsure(app: &AppHandle, browser: u64) {
    let shared = app.state::<Shared>();
    if shared.browser.swap(browser, Ordering::Relaxed) == browser {
        return;
    }
    let _ = app.emit_to("settings", "settings", ());
    if browser == 0 {
        return crate::notify::gone(crate::notify::ASKS);
    }
    note(&shared, "a browser that may be on this computer has notifications on");
    let asks = {
        let mut saved = shared.saved.lock().unwrap();
        saved.no_robot && std::mem::replace(&mut saved.asked, browser) != browser
    };
    if asks {
        shared.save();
        if app.get_webview_window("settings").is_none() {
            let _ = app.emit_to("robot", "asks", ()); // its page has the words
        }
    }
}

/// What came with a look. Asked of the Machine once more, as the phone app does: its words, and its buttons now. It isn't
/// given up as got here: only when it shows (shown), or when there is nothing to show any more.
pub fn came(app: &AppHandle, machine: &Machine, notices: &Value, meeting: &Value) {
    if notices.is_null() {
        return;
    }
    let (shared, may) = (app.state::<Shared>(), up(app));
    let about = about(meeting);
    let (fresh, lost, room, stuck) = {
        let (mut speaking, at) = (shared.speaking.lock().unwrap(), Instant::now());
        let (fresh, lost) = speaking.offered(notices, about.as_ref().and_then(|m| m.told.as_deref()), at);
        (fresh, lost, speaking.room(), speaking.stuck(at))
    };
    if lost > 0 {
        note(&shared, "a waiting one went: the Machine no longer offers it here (the browser's after 90 seconds, or replaced)");
    }
    if stuck {
        note(&shared, "the bubble's page doesn't answer: it is made again");
        later(app, windows::drop_bubble);
        return later(app, done);
    }
    if !may {
        return;
    }
    let (mut said, mut gone) = (Vec::new(), Vec::new());
    for n in fresh.iter().rev().filter(|n| n["key"].is_string()) {
        if said.len() >= room {
            note(&shared, "one waits: enough are waiting already");
            break;
        }
        let key = n["key"].as_str().map(String::from);
        match machine.notice(n["id"].as_str().unwrap_or_default(), n["kind"].as_str().unwrap_or_default()) {
            Ok(Some(say)) => said.push(Say { snooze: serde_json::from_value(n["snooze"].clone()).unwrap_or_default(), key, ..say }),
            Ok(None) => {
                note(&shared, "one had nothing to show any more");
                gone.push(Say { key, ..Say::default() });
            }
            Err(_) => note(&shared, "the Machine didn't say what one is: asked again with the next look"),
        }
    }
    let had = !gone.is_empty();
    let no_robot = no_robot(&shared);
    let mut tells = Vec::new();
    {
        let mut speaking = shared.speaking.lock().unwrap();
        gone.iter().for_each(|s| speaking.had(s));
        let soon = about.filter(|m| !m.told.as_ref().is_some_and(|t| speaking.told.contains(t)) && !speaking.queue.iter().chain(&speaking.now).any(|s| s.told == m.told));
        for say in said.into_iter().rev().chain(soon) {
            if no_robot {
                speaking.notices.retain(|n| n.0.id != say.id);
                speaking.notices.push((say.clone(), false));
                tells.push(say);
                continue;
            }
            speaking.add(say);
        }
    }
    for say in tells {
        let _ = app.emit_to("robot", "notify", say); // its page has the words
    }
    if had {
        shared.look_soon(); // it says so right away: then the browser doesn't get it too when the computer sleeps meanwhile
    }
    later(app, next);
}

/// The meeting that starts soon, and what it is told once by: one that is moved is told again.
fn about(meeting: &Value) -> Option<Say> {
    let words = |key: &str| meeting[key].as_str().unwrap_or_default().split_whitespace().collect::<Vec<_>>().join(" ").chars().filter(|c| !c.is_control()).take(60).collect::<String>();
    let id = meeting["id"].as_str().filter(|id| crate::todo_id(id).is_ok())?.to_string();
    let (at, link) = (words("at"), meeting["join"].as_str().filter(|l| crate::address::call(l)).map(String::from));
    let of = Meeting { who: words("who"), others: meeting["others"].as_u64().unwrap_or(0), title: meeting["title"].is_string().then(|| words("title")), join: link.is_some(), at: at.clone() };
    (!at.is_empty()).then(|| Say { id, meeting: Some(of), link, told: Some(format!("{} {at}", meeting["event"])), ..Say::default() })
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
    let (shows, open) = (showing(&shared), windows::box_open(app));
    let found = {
        let mut speaking = shared.speaking.lock().unwrap();
        if speaking.now.is_some() || speaking.queue.is_empty() || !shows {
            return;
        }
        (!open).then(|| speaking.pop(Instant::now()).is_some())
    };
    let Some(found) = found else { return note(&shared, "one waits: the box is open") };
    if found {
        windows::open_bubble(app);
    } else {
        shared.look_soon(); // whether it is still this robot's to say
    }
}

/// The bubble shows, or still does: now it is got.
pub fn shown(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let first = {
        let mut speaking = shared.speaking.lock().unwrap();
        speaking.alive = Some(Instant::now());
        let Some(say) = speaking.now.clone().filter(|_| !std::mem::replace(&mut speaking.shown, true)) else { return };
        speaking.had(&say);
        say
    };
    note(&shared, if first.meeting.is_some() { "showed a bubble, of a meeting" } else { "showed a bubble" });
    shared.look_soon(); // the Machine hears so right away: then the browser doesn't get it too
}

/// Without a robot: the system was asked to show it (notify.rs).
pub fn notified(app: &AppHandle, id: &str) {
    let shared = app.state::<Shared>();
    {
        let mut speaking = shared.speaking.lock().unwrap();
        let Some((say, _)) = speaking.notices.iter().find(|n| n.0.id == id).cloned() else { return };
        speaking.had(&say);
    }
    note(&shared, "gave one to the system's notifications");
    shared.look_soon();
}

/// What the bubble says now.
pub fn now(shared: &Shared) -> Option<Say> {
    shared.speaking.lock().unwrap().now.clone()
}

/// A button of it was tapped.
pub fn hold(shared: &Shared) {
    let mut speaking = shared.speaking.lock().unwrap();
    if let Some(say) = &mut speaking.now {
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

/// The box opened: what is said now, it says. Or the robot goes: nothing more is said. The dot still tells, and what wasn't
/// shown is still the Machine's: it comes again when the robot may speak, or goes to the browser.
pub fn hush(app: &AppHandle, all: bool) {
    let shared = app.state::<Shared>();
    let (there, waited) = {
        let mut speaking = shared.speaking.lock().unwrap();
        let waited = all && !speaking.queue.is_empty();
        if all {
            speaking.queue.clear();
        }
        (speaking.now.take().is_some(), waited)
    };
    if waited {
        note(&shared, "a waiting one is the Machine's again: the robot went");
    }
    if there {
        windows::close_bubble(app);
    }
}

/// The box closed: its rows were seen.
pub fn closed(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let rows: Vec<String> = shared.waiting.lock().unwrap().todos.iter().filter_map(|t| t.id.clone()).collect();
    if shared.speaking.lock().unwrap().seen(&rows) > 0 {
        note(&shared, "a waiting one isn't said: the box showed its row");
        shared.look_soon();
    }
    later(app, next);
}

/// What is in For you now: one that was there and went (decided here or on another device) isn't said any more.
pub fn follow(app: &AppHandle, marks: &[crate::seen::Mark]) {
    let there = |id: &str| marks.iter().any(|(name, _)| name.split('@').next() == Some(id));
    let mut went = Vec::new();
    let gone = {
        let shared = app.state::<Shared>();
        let mut speaking = shared.speaking.lock().unwrap();
        speaking.notices.retain_mut(|(say, listed)| {
            let here = there(&say.id);
            let stays = here || !*listed;
            *listed |= here;
            if !stays {
                went.push(say.id.clone());
            }
            stays
        });
        speaking.decided(there)
    };
    went.iter().for_each(|id| crate::notify::gone(id));
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

    fn say(id: &str, key: &str) -> Say {
        Say { id: id.into(), key: Some(key.into()), ..Say::default() }
    }

    fn keys(found: &[Value]) -> Vec<&str> {
        found.iter().filter_map(|n| n["key"].as_str()).collect()
    }

    #[test]
    fn it_is_got_when_it_shows_and_not_before() {
        let (mut s, at) = (Speaking::default(), Instant::now());
        let offered = json!([{"key": "a1", "id": "x"}]);
        assert_eq!(keys(&s.offered(&offered, None, at).0), ["a1"]);
        s.add(say("x", "a1"));
        assert_eq!((s.offered(&offered, None, at), s.got.len()), ((vec![], 0), 0), "it waits: not asked for again, not got");
        assert_eq!(s.pop(at).unwrap().id, "x");
        assert_eq!((s.offered(&offered, None, at), s.got.len()), ((vec![], 0), 0), "its page has it: not got either");
        let now = s.now.clone().unwrap();
        s.had(&now);
        assert_eq!((s.got.clone(), s.offered(&offered, None, at).0), (vec!["a1".to_string()], vec![]));
        s.offered(&json!([]), None, at);
        assert!(s.got.is_empty(), "the Machine knows");
    }

    #[test]
    fn one_the_machine_gave_to_the_browser_is_not_said_after() {
        let (mut s, at) = (Speaking::default(), Instant::now());
        let offered = json!([{"key": "a1", "id": "x"}, {"key": "b2", "id": "y"}]);
        s.offered(&offered, None, at);
        s.add(say("x", "a1"));
        s.add(say("y", "b2"));
        assert_eq!(s.offered(&json!([{"key": "b2", "id": "y"}]), None, at), (vec![], 1));
        assert!(s.pop(at + FRESH).is_none(), "the box closed a while after the look: another look first");
        assert_eq!(s.pop(at).unwrap().id, "y");
        assert!(s.got.is_empty());
    }

    #[test]
    fn a_cleared_one_comes_again() {
        let (mut s, at) = (Speaking::default(), Instant::now());
        let offered = json!([{"key": "a1", "id": "x"}]);
        s.offered(&offered, None, at);
        s.add(say("x", "a1"));
        s.queue.clear(); // hush: the robot went away
        assert_eq!(keys(&s.offered(&offered, None, at).0), ["a1"]);
    }

    #[test]
    fn the_box_said_what_its_rows_showed_and_nothing_else() {
        let mut s = Speaking::default();
        s.add(say("x", "a1"));
        s.add(say("y", "b2"));
        s.add(Say { id: "x2".into(), meeting: Some(Meeting::default()), told: Some("7 ten".into()), ..Say::default() });
        assert_eq!(s.seen(&["x".into(), "x2".into()]), 1);
        assert_eq!(s.got, ["a1"]);
        assert_eq!(s.queue.iter().map(|q| q.id.as_str()).collect::<Vec<_>>(), ["y", "x2"]);
        assert!(s.pop(Instant::now()).is_none(), "the browser may have them by now: another look first");
        s.offered(&json!([{"key": "b2", "id": "y"}]), Some("7 ten"), Instant::now());
        assert_eq!(s.pop(Instant::now()).unwrap().id, "y");
    }

    #[test]
    fn one_decided_elsewhere_is_got() {
        let mut s = Speaking::default();
        s.add(say("x", "a1"));
        assert!(!s.decided(|_| false), "not in the list yet");
        assert_eq!(s.queue.len(), 1);
        s.decided(|id| id == "x");
        s.decided(|_| false);
        assert_eq!((s.queue.len(), s.got.clone()), (0, vec!["a1".to_string()]));
    }

    #[test]
    fn a_page_that_died_is_made_again() {
        let (mut s, at) = (Speaking { asked: Some(Instant::now()), ..Speaking::default() }, Instant::now());
        assert!(!s.stuck(at + DEAD * 2), "nothing is said");
        s.add(say("x", "a1"));
        s.pop(at);
        assert!(!s.stuck(at + SLOW) && s.stuck(at + SLOW * 2), "it never showed");
        s.shown = true;
        assert!(!s.stuck(at + SLOW * 2) && s.stuck(at + DEAD * 2), "it shows, but its page is gone");
    }

    #[test]
    fn a_meeting_is_told_once_it_shows_and_goes_with_the_offer() {
        let (mut s, at) = (Speaking::default(), Instant::now());
        let one = Say { id: "m".into(), meeting: Some(Meeting::default()), told: Some("7 ten".into()), ..Say::default() };
        s.add(one.clone());
        assert_eq!(s.offered(&json!([]), Some("7 ten"), at).1, 0);
        assert!(s.told.is_empty());
        s.had(&one);
        assert!(s.told.contains("7 ten") && s.got.is_empty());
        assert_eq!(s.offered(&json!([]), Some("7 eleven"), at).1, 1);
    }

    #[test]
    fn a_meeting_and_its_link() {
        let meeting = json!({"id": "aa01", "event": 7, "at": "2026-11-24T10:00:00+00:00", "who": " Dana\n", "others": 2, "join": "https://zoom.us/j/1"});
        let say = about(&meeting).unwrap();
        assert_eq!(say.told.as_deref(), Some("7 2026-11-24T10:00:00+00:00"));
        assert_eq!(say.meeting, Some(Meeting { at: "2026-11-24T10:00:00+00:00".into(), who: "Dana".into(), others: 2, title: None, join: true }));
        assert_eq!(say.link.as_deref(), Some("https://zoom.us/j/1"));
        let with = |key: &str, value: Value| { let mut m = meeting.clone(); m[key] = value; about(&m) };
        let other = with("join", json!("https://zoom.us.example.com/j/1")).unwrap();
        assert!(other.link.is_none() && !other.meeting.unwrap().join);
        let title = |value: Value| with("title", value).unwrap().meeting.unwrap().title;
        assert_eq!((title(json!(" Kickoff\n")).as_deref(), title(json!("")).as_deref(), title(json!(7))), (Some("Kickoff"), Some(""), None));
        assert!(with("id", json!("../x")).is_none() && with("at", Value::Null).is_none() && about(&Value::Null).is_none());
    }
}
