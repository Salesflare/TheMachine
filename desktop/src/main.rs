//! The Machine's robot on the desktop: a prototype (README.md). Three parts that only meet here: the windows
//! (windows.rs, place.rs), the pages (ui/) and the person's Machine (machine.rs, signin.rs).
#![cfg_attr(all(not(debug_assertions), windows), windows_subsystem = "windows")]

mod address;
mod card;
mod front;
mod machine;
mod place;
mod quit;
mod saved;
mod seen;
mod signin;
mod snip;
mod speak;
mod webapp;
mod windows;

use machine::{Machine, Waiting};
use saved::Saved;
use serde::Serialize;
use serde_json::Value;
use std::path::PathBuf;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Mutex;
use std::time::Duration;
use tauri::{AppHandle, Emitter, Manager, RunEvent, State, WindowEvent};
use tauri_plugin_deep_link::DeepLinkExt;
use tauri_plugin_opener::OpenerExt;

/// How often it looks at the dashboard's list. Also when the box opens, and when the installed app is left.
const LOOK: Duration = Duration::from_secs(30);

/// What the robot's page holds of the Machine's status, and what it has yet to take.
#[derive(Default)]
struct Held {
    machine: String,
    token: Option<String>,
    fleet: Option<Value>, // the stamp of what it holds of the Fleet
    news: Vec<News>,
}

/// An answer of the Machine's, for the robot's page.
#[derive(Serialize)]
struct News {
    machine: String,
    status: Value,
    fleet: Option<Value>,
}

/// What the robot's page makes the list from; of what was just added it also says where that is.
#[derive(Serialize)]
struct Taken {
    news: Vec<News>,
    added: Vec<String>,
}

pub struct Shared {
    saved: Mutex<Saved>,
    file: PathBuf,
    waiting: Mutex<Waiting>,
    held: Mutex<Held>,
    looking: Mutex<()>,
    /// The thread that looks, to wake it.
    looker: Mutex<Option<std::thread::Thread>>,
    /// Why the Machine didn't answer the last time, a code of machine.rs.
    problem: Mutex<Option<String>>,
    /// What is in For you, and whether some of it is new since the person last looked (seen.rs).
    now: Mutex<seen::Seen>,
    /// The Machine whose dashboard has a page for one to-do, once that is known, and the one that is open (card.rs).
    compact: Mutex<Option<String>>,
    card: Mutex<card::Card>,
    /// What the robot says, and will (speak.rs); how tall its bubble is.
    speaking: Mutex<speak::Speaking>,
    tall: Mutex<f64>,
    /// The to-do the box opens on.
    pub wanted: Mutex<Option<String>>,
    /// What was added in the box since it opened.
    pub added: Mutex<Vec<String>>,
    dot: AtomicBool,
    /// A screenshot can be taken here (snip.rs), and one is being taken.
    snip: AtomicBool,
    pub picking: AtomicBool,
    pending: Mutex<Option<signin::Pending>>,
    /// The Machine, and whether no other one answers at its host (machine.rs), once that is known.
    alone: Mutex<Option<(String, bool)>>,
    /// The box's page height, and whether it is open; how many times it opened.
    height: Mutex<f64>,
    open: AtomicBool,
    opened: AtomicU64,
    /// The box opens on its menu.
    menu: AtomicBool,
    /// The Machine's app is in front (front.rs), or something is full screen (Windows): no robot.
    away: AtomicBool,
    full: AtomicBool,
    /// Something is written in the box: its page stays loaded.
    draft: AtomicBool,
    /// The robot only looks over the bottom edge of the screen; the box opens on saying so.
    hidden: AtomicBool,
    notice: AtomicBool,
    grab: Mutex<Option<windows::Grab>>,
    /// The monitors, as they last were (Windows).
    #[cfg(windows)]
    screens: Mutex<String>,
    layer: bool,
}

impl Shared {
    fn machine(&self) -> Option<Machine> {
        let saved = self.saved.lock().unwrap();
        Some(Machine { url: saved.machine.clone()?, cookie: saved.cookie.clone() })
    }

    /// Its address, and whether no other Machine answers at its host.
    fn signed_in(&self) -> Option<(String, bool)> {
        let url = self.saved.lock().unwrap().machine.clone()?;
        let alone = self.alone.lock().unwrap().as_ref().is_some_and(|(of, alone)| *of == url && *alone);
        Some((url, alone))
    }

    fn save(&self) {
        if let Err(error) = self.saved.lock().unwrap().write(&self.file) {
            eprintln!("could not save: {error}");
        }
    }

    #[cfg(windows)]
    fn count(&self) -> usize {
        self.waiting.lock().unwrap().count
    }

    fn look_soon(&self) {
        if let Some(looker) = &*self.looker.lock().unwrap() {
            looker.unpark();
        }
    }
}

/// Runs this on the main thread, once whatever asks for it there has returned. On Windows a window that is made, shown or
/// focused inside a page's call, or inside a second start's message, can wait for itself.
fn later(app: &AppHandle, work: impl FnOnce(&AppHandle) + Send + 'static) {
    let app = app.clone();
    std::thread::spawn(move || {
        let here = app.clone();
        app.run_on_main_thread(move || work(&here))
    });
}

/// Runs a request to the Machine off the main thread.
async fn away<T: Send + 'static>(work: impl FnOnce() -> Result<T, String> + Send + 'static) -> Result<T, String> {
    tauri::async_runtime::spawn_blocking(work).await.map_err(|_| "failed".to_string())?
}

async fn with_machine<T: Send + 'static>(app: &AppHandle, work: impl FnOnce(Machine) -> Result<T, String> + Send + 'static) -> Result<T, String> {
    let machine = app.state::<Shared>().machine().ok_or("notowner")?;
    away(move || work(machine)).await
}

fn look(app: &AppHandle) -> Result<(), String> {
    let shared = app.state::<Shared>();
    let Some(machine) = shared.machine() else { return Ok(()) };
    let found = ask_status(app, &shared, &machine);
    if shared.machine().is_none_or(|m| m.url != machine.url) {
        return Ok(()); // signed out meanwhile
    }
    *shared.problem.lock().unwrap() = found.as_ref().err().cloned();
    match &found {
        Ok(notices) => {
            let _ = app.emit_to("robot", "news", ());
            speak::came(app, &machine, notices);
        }
        Err(_) => { // not reachable or signed out: nothing is known to wait, so no dot
            set_dot(app, false);
            listed(app, Waiting::default());
        }
    }
    if found.is_ok() && !shared.alone.lock().unwrap().as_ref().is_some_and(|(url, _)| *url == machine.url) {
        if let Some(alone) = machine.alone() {
            *shared.alone.lock().unwrap() = Some((machine.url, alone));
        }
    }
    found.map(|_| ())
}

/// One at a time: each answer is what changed since the one before. The robot's page puts them together (ui/list.js).
/// Gives what waits for the robot to say.
fn ask_status(app: &AppHandle, shared: &Shared, machine: &Machine) -> Result<Value, String> {
    let _one = shared.looking.lock().unwrap();
    let (since, fleet_held) = {
        let mut held = shared.held.lock().unwrap();
        if held.machine != machine.url {
            *held = Held { machine: machine.url.clone(), ..Held::default() };
        }
        (held.token.clone(), held.fleet.clone())
    };
    let desk = shared.saved.lock().unwrap().desk.clone();
    let mut status = machine.status(since.as_deref(), &desk, speak::up(app), &speak::got(shared))?;
    let notices = status["notices"].take(); // not part of the status
    // The Fleet's items, when its part says they changed (a change list without that part: they didn't)
    let part = &status["fleet"];
    let due = (part["on"] == true && fleet_held.as_ref() != Some(&part["stamp"])).then(|| part["stamp"].clone());
    let fleet = due.as_ref().and_then(|_| machine.fleet().ok());
    let mut held = shared.held.lock().unwrap();
    if held.machine != machine.url {
        return Ok(Value::Null); // signed out meanwhile
    }
    // One that didn't answer is asked for again, with the whole status
    held.token = if due.is_some() && fleet.is_none() { None } else { status["_token"].as_str().map(String::from) };
    if fleet.is_some() {
        held.fleet = due;
    }
    if status["_since"].is_null() {
        held.news.clear();
    }
    held.news.push(News { machine: machine.url.clone(), status, fleet });
    Ok(notices)
}

fn listed(app: &AppHandle, waiting: Waiting) {
    let shared = app.state::<Shared>();
    if std::mem::replace(&mut *shared.waiting.lock().unwrap(), waiting.clone()) == waiting {
        return;
    }
    let _ = app.emit_to("box", "listed", ());
    follow_tray(app);
}

/// The dot: something is new. While the box or the Machine's app is open the person sees it, so it isn't.
fn news(app: &AppHandle, now: seen::Seen) {
    let shared = app.state::<Shared>();
    let looking = windows::box_open(app) || shared.away.load(Ordering::Relaxed);
    let dot = {
        let mut saved = shared.saved.lock().unwrap();
        match &mut saved.seen {
            Some(seen) if !looking => seen::news(seen, &now),
            _ => false,
        }
    };
    *shared.now.lock().unwrap() = now;
    if dot {
        set_dot(app, true);
    } else if looking || shared.saved.lock().unwrap().seen.is_none() {
        looked(app);
    } else {
        set_dot(app, false); // what was new is gone, or done on another device
    }
}

/// The person looks, in the box or the dashboard: nothing is new then.
pub fn looked(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let now = shared.now.lock().unwrap().clone();
    let was = shared.waiting.lock().unwrap().known.then(|| std::mem::replace(&mut shared.saved.lock().unwrap().seen, Some(now.clone())));
    if was.is_some_and(|was| was != Some(now)) {
        shared.save();
    }
    set_dot(app, false);
}

fn set_dot(app: &AppHandle, dot: bool) {
    if app.state::<Shared>().dot.swap(dot, Ordering::Relaxed) != dot {
        let _ = app.emit_to("robot", "dot", dot);
        follow_tray(app);
    }
}

/// What the Machine answered since the robot's page last took it.
#[tauri::command]
fn robot_take(shared: State<Shared>) -> Taken {
    Taken { news: std::mem::take(&mut shared.held.lock().unwrap().news), added: shared.added.lock().unwrap().clone() }
}

/// The dashboard's For you, as the robot's page made it. None: it needs the whole status.
#[tauri::command]
fn robot_list(app: AppHandle, machine: String, todos: Option<Vec<machine::Todo>>, marks: Vec<seen::Mark>, name: String, hour12: bool, added: Vec<machine::Added>) {
    let shared = app.state::<Shared>();
    if shared.machine().is_none_or(|m| m.url != machine) || shared.problem.lock().unwrap().is_some() {
        return;
    }
    let Some(todos) = todos else {
        *shared.held.lock().unwrap() = Held::default();
        return shared.look_soon();
    };
    later(&app, move |app| {
        let here = app.state::<Shared>().added.lock().unwrap().clone();
        let added = added.into_iter().filter(|a| here.contains(&a.id)).collect();
        listed(app, Waiting { hour12, ..Waiting::of(todos, marks.len(), &name, added) });
        speak::follow(app, &marks);
        news(app, seen::now(&machine, &marks));
    });
}

// The robot

#[derive(Serialize)]
struct RobotState {
    dot: bool,
    hidden: bool,
}

#[tauri::command]
fn robot_state(shared: State<Shared>) -> RobotState {
    RobotState { dot: shared.dot.load(Ordering::Relaxed), hidden: shared.hidden.load(Ordering::Relaxed) }
}

#[tauri::command]
fn robot_grab(app: AppHandle, x: f64, y: f64) -> bool {
    windows::grab(&app, x, y);
    app.state::<Shared>().layer
}

#[tauri::command]
fn robot_drag(app: AppHandle) {
    windows::drag(&app);
}

#[tauri::command]
fn robot_drop(app: AppHandle) {
    windows::dropped(&app);
    app.state::<Shared>().save();
}

#[tauri::command]
fn robot_click(app: AppHandle) {
    later(&app, show_or_toggle);
}

/// A hidden robot comes back; otherwise the box opens or closes.
fn show_or_toggle(app: &AppHandle) {
    if app.state::<Shared>().hidden.load(Ordering::Relaxed) {
        windows::close_box(app);
        show(app);
    } else {
        toggle(app);
    }
}

fn show(app: &AppHandle) {
    app.state::<Shared>().away.store(false, Ordering::Relaxed);
    set_hidden(app, false);
    windows::show_robot(app);
}

/// It looks over the bottom edge of the screen. The first time the box says so.
fn hide(app: &AppHandle) {
    windows::close_box(app);
    set_hidden(app, true);
    let shared = app.state::<Shared>();
    if !std::mem::replace(&mut shared.saved.lock().unwrap().hide_told, true) {
        shared.save();
        shared.notice.store(true, Ordering::Relaxed);
        open(app);
    }
}

fn set_hidden(app: &AppHandle, hidden: bool) {
    app.state::<Shared>().hidden.store(hidden, Ordering::Relaxed);
    if hidden {
        speak::hush(app, true);
    }
    app.state::<Shared>().look_soon(); // whether it speaks
    windows::place(app);
    let _ = app.emit_to("robot", "hidden", hidden);
    follow_tray(app);
}

/// A right click: the box, with its menu open. (Tauri's own menu waits in a loop of its own on Linux, and forever when
/// the compositor closes it.)
#[tauri::command]
fn robot_menu(app: AppHandle) {
    later(&app, |app| {
        app.state::<Shared>().menu.store(true, Ordering::Relaxed);
        if windows::box_open(app) {
            let _ = app.emit_to("box", "opened", ());
        } else {
            toggle(app);
        }
    });
}

#[tauri::command]
fn menu_item(app: AppHandle, id: String) {
    later(&app, move |app| {
        windows::close_box(app);
        chosen(app, &id);
    });
}

fn chosen(app: &AppHandle, id: &str) {
    match id {
        "dashboard" => {
            if let Err(error) = open_path(app, "") {
                open(app);
                let _ = app.emit_to("box", "failed", error);
            }
        }
        "hide" => hide(app),
        "show" => show(app),
        "signout" => {
            let shared = app.state::<Shared>();
            {
                let mut saved = shared.saved.lock().unwrap();
                (saved.machine, saved.cookie, saved.seen) = (None, None, None);
            }
            shared.save();
            *shared.held.lock().unwrap() = Held::default();
            *shared.problem.lock().unwrap() = None;
            shared.now.lock().unwrap().clear();
            *shared.compact.lock().unwrap() = None;
            card::forget(app);
            speak::hush(app, true);
            set_dot(app, false);
            listed(app, Waiting::default());
            open(app); // it says so
        }
        "quit" => quit::quit(app),
        _ => {}
    }
}

fn toggle(app: &AppHandle) {
    if windows::box_open(app) {
        windows::close_box(app);
    } else {
        open(app);
    }
}

fn open(app: &AppHandle) {
    if let Err(error) = windows::open_box(app) {
        eprintln!("could not open the box: {error}");
    }
}

// The box

#[derive(Serialize)]
struct BoxState {
    machine: Option<String>,
    problem: Option<String>,
    waiting: Waiting,
    menu: bool,
    hidden: bool,
    notice: bool,
    snip: bool,
    open: bool,
    speaks: speak::Speak,
    wanted: Option<String>,
}

#[tauri::command]
fn box_state(shared: State<Shared>) -> BoxState {
    BoxState {
        machine: shared.machine().map(|m| m.url),
        problem: shared.problem.lock().unwrap().clone(),
        waiting: shared.waiting.lock().unwrap().clone(),
        menu: shared.menu.swap(false, Ordering::Relaxed),
        hidden: shared.hidden.load(Ordering::Relaxed),
        notice: shared.notice.load(Ordering::Relaxed),
        snip: shared.snip.load(Ordering::Relaxed),
        open: shared.open.load(Ordering::Relaxed),
        speaks: shared.saved.lock().unwrap().speak,
        wanted: shared.wanted.lock().unwrap().clone(),
    }
}

/// "Speak up", in its menu.
#[tauri::command]
fn set_speaks(app: AppHandle, when: speak::Speak) {
    let shared = app.state::<Shared>();
    shared.saved.lock().unwrap().speak = when;
    shared.save();
    shared.look_soon();
    if when == speak::Speak::Never {
        later(&app, |app| speak::hush(app, true));
    }
}

// The bubble

#[derive(Serialize)]
struct BubbleState {
    say: Option<speak::Say>,
    /// Where the robot is along it, and whether it is below the robot.
    tail: f64,
    below: bool,
    hour12: bool,
}

#[tauri::command]
fn bubble_state(app: AppHandle) -> BubbleState {
    let (tail, below) = windows::bubble_tail(&app);
    let shared = app.state::<Shared>();
    let hour12 = shared.waiting.lock().unwrap().hour12;
    BubbleState { say: speak::now(&shared), tail, below, hour12 }
}

#[tauri::command]
fn bubble_fit(app: AppHandle, height: f64) {
    later(&app, move |app| windows::fit_bubble(app, height));
}

/// A button was tapped: it stays until the page is done with it.
#[tauri::command]
fn bubble_hold(shared: State<Shared>) {
    speak::hold(&shared);
}

/// It opens as a row of the box does.
#[tauri::command]
async fn bubble_open(app: AppHandle, todo: String) -> Result<(), String> {
    todo_id(&todo)?;
    if has_card(&app).await? {
        *app.state::<Shared>().wanted.lock().unwrap() = Some(todo);
        later(&app, open);
        return Ok(());
    }
    open_path(&app, &format!("#card={todo}"))
}

#[tauri::command]
fn bubble_done(app: AppHandle) {
    later(&app, speak::done);
}

/// Asks the Machine now: whether it still answers, and what waits.
#[tauri::command]
async fn box_look(app: AppHandle) -> Result<(), String> {
    away(move || look(&app)).await
}

#[tauri::command]
fn box_fit(app: AppHandle, height: f64) {
    windows::fit_box(&app, height);
}

#[tauri::command]
fn box_draft(shared: State<Shared>, there: bool) {
    shared.draft.store(there, Ordering::Relaxed);
}

#[tauri::command]
fn box_close(app: AppHandle) {
    later(&app, windows::close_box);
}

fn signed_in(app: &AppHandle, machine: Machine) -> Result<(), String> {
    machine.check()?;
    let shared = app.state::<Shared>();
    {
        let mut saved = shared.saved.lock().unwrap();
        (saved.machine, saved.cookie, saved.seen) = (Some(machine.url), machine.cookie, None);
    }
    shared.save();
    shared.now.lock().unwrap().clear();
    *shared.held.lock().unwrap() = Held::default();
    *shared.problem.lock().unwrap() = None;
    let _ = look(app);
    Ok(())
}

/// A self-hosted Machine's own address.
#[tauri::command]
async fn connect(app: AppHandle, address: String) -> Result<(), String> {
    let url = address::parse(&address).ok_or("address")?;
    away(move || signed_in(&app, Machine { url, cookie: None })).await
}

/// The account's sign-in, in the person's browser. The scheme it comes back on is registered only while it runs.
#[tauri::command]
fn sign_in(app: AppHandle) -> Result<(), String> {
    let (pending, address) = signin::start()?;
    app.deep_link().register(signin::SCHEME).map_err(|_| "scheme")?;
    *app.state::<Shared>().pending.lock().unwrap() = Some(pending);
    app.opener().open_url(address, None::<&str>).map_err(|_| "browser".to_string())
}

/// Takes the sign-in's links back. On Linux the plugin leaves its file, emptied of them.
pub fn no_links(app: &AppHandle) {
    let _ = app.deep_link().unregister(signin::SCHEME);
    #[cfg(target_os = "linux")]
    if let (Ok(data), Ok(program)) = (app.path().data_dir(), std::env::current_exe()) {
        if let Some(name) = program.file_name() {
            let _ = std::fs::remove_file(data.join("applications").join(format!("{}-handler.desktop", name.to_string_lossy())));
        }
    }
}

fn came_back(app: &AppHandle, link: &str) {
    let shared = app.state::<Shared>();
    let Some(found) = shared.pending.lock().unwrap().as_ref().and_then(|p| signin::back(link, p)) else { return };
    *shared.pending.lock().unwrap() = None; // once
    no_links(app);
    let app = app.clone();
    std::thread::spawn(move || {
        let done = match found {
            signin::Back::Own(url) => signed_in(&app, Machine { url, cookie: None }),
            signin::Back::Hosted { auth, machine } => machine::redeem(&auth)
                .and_then(|cookie| signed_in(&app, Machine { url: machine, cookie: Some(cookie) })),
        };
        let _ = app.emit_to("box", "signin", done.err());
        later(&app, open);
    });
}

#[tauri::command]
async fn add_todo(app: AppHandle, text: String, draft: String, files: Vec<String>) -> Result<Value, String> {
    let made = with_machine(&app, move |m| m.add_todo(&text, &draft, &files)).await?;
    if let Some(id) = made["id"].as_str().filter(|id| todo_id(id).is_ok()) {
        let shared = app.state::<Shared>();
        let mut added = shared.added.lock().unwrap();
        if added.len() < 20 {
            added.push(id.into());
        }
    }
    Ok(made)
}

#[tauri::command]
async fn add_file(app: AppHandle, draft: String, name: String, data: String) -> Result<Value, String> {
    with_machine(&app, move |m| m.add_file(&draft, &name, &data)).await
}

#[tauri::command]
async fn remove_file(app: AppHandle, draft: String, id: String) -> Result<Value, String> {
    with_machine(&app, move |m| m.remove_file(&draft, &id)).await
}

/// The person picks an area or a window, with the system's own tool. None: they didn't. The robot and its box are away
/// meanwhile, and the box is back with it, still to be added.
#[tauri::command]
async fn take_screenshot(app: AppHandle) -> Result<Option<String>, String> {
    if app.state::<Shared>().picking.swap(true, Ordering::Relaxed) {
        return Err("shot".into());
    }
    let here = app.clone();
    later(&here, |app| {
        windows::close_box(app);
        windows::show_or_not(app);
    });
    let taken = away(|| {
        std::thread::sleep(Duration::from_millis(400)); // off the screen
        snip::take()
    }).await;
    later(&here, |app| {
        app.state::<Shared>().picking.store(false, Ordering::Relaxed);
        open(app);
    });
    use base64::{engine::general_purpose::STANDARD, Engine};
    Ok(taken?.map(|png| STANDARD.encode(png)))
}

fn todo_id(id: &str) -> Result<(), String> {
    let plain = !id.is_empty() && id.len() <= 64 && id.bytes().all(|b| b.is_ascii_alphanumeric());
    if plain { Ok(()) } else { Err("failed".into()) }
}

/// The quick buttons of its notification, what they do, and their Undo.
#[tauri::command]
async fn todo_quick(app: AppHandle, todo: String) -> Result<Vec<machine::Quick>, String> {
    todo_id(&todo)?;
    with_machine(&app, move |m| m.quick(&todo)).await
}

#[tauri::command]
async fn todo_decide(app: AppHandle, todo: String, act: String, until: Option<String>) -> Result<Value, String> {
    todo_id(&todo)?;
    let done = with_machine(&app, move |m| m.decide(&todo, &act, until.as_deref())).await;
    app.state::<Shared>().look_soon();
    done
}

#[tauri::command]
async fn todo_undo(app: AppHandle, todo: String, act: String) -> Result<Value, String> {
    todo_id(&todo)?;
    let done = with_machine(&app, move |m| m.undo(&todo, &act)).await;
    app.state::<Shared>().look_soon();
    done
}

#[tauri::command]
async fn ask(app: AppHandle, text: String) -> Result<Value, String> {
    with_machine(&app, move |m| m.ask(&text)).await
}

/// Whether its Machine's dashboard has a page for one to-do: asked once.
async fn has_card(app: &AppHandle) -> Result<bool, String> {
    let known = app.state::<Shared>().compact.lock().unwrap().clone();
    let url = with_machine(app, move |m| Ok((known.as_ref() == Some(&m.url) || m.compact()).then_some(m.url))).await?;
    if url.is_some() {
        *app.state::<Shared>().compact.lock().unwrap() = url.clone();
    }
    Ok(url.is_some())
}

/// Opens it in the box. The box's height with it; none: this Machine has no page for that, so it opens in the dashboard.
#[tauri::command]
async fn card_open(app: AppHandle, todo: String) -> Result<Option<f64>, String> {
    todo_id(&todo)?;
    *app.state::<Shared>().wanted.lock().unwrap() = None;
    if !has_card(&app).await? {
        return Ok(None);
    }
    let (tell, told) = std::sync::mpsc::channel();
    later(&app, move |app| {
        let _ = tell.send(windows::tall(app));
        if card::open(app, &todo).is_err() {
            let _ = app.emit_to("box", "card", "failed");
        }
    });
    away(move || told.recv().map(Some).map_err(|_| "failed".into())).await
}

#[tauri::command]
fn card_place(app: AppHandle, top: f64, height: f64) {
    later(&app, move |app| card::put(app, top, height));
}

#[tauri::command]
fn card_close(app: AppHandle) {
    later(&app, card::back);
}

/// The dashboard, or one of its to-dos: where a draft is read and approved.
#[tauri::command]
fn open_dashboard(app: AppHandle, todo: Option<String>) -> Result<(), String> {
    match todo {
        Some(id) => todo_id(&id).and_then(|()| open_path(&app, &format!("#card={id}"))),
        None => open_path(&app, ""),
    }?;
    later(&app, windows::close_box);
    Ok(())
}

/// In the Machine's installed app, or else in the browser.
fn open_path(app: &AppHandle, path: &str) -> Result<(), String> {
    let (machine, alone) = app.state::<Shared>().signed_in().ok_or("notowner")?;
    looked(app);
    // Which robot opens it: the page tells the Machine what browser is on this computer (speak.rs)
    let address = format!("{machine}?desk={}{path}", app.state::<Shared>().saved.lock().unwrap().desk);
    if webapp::open(&machine, &address, alone) {
        return Ok(());
    }
    app.opener().open_url(address, None::<&str>).map_err(|_| "browser".to_string())
}

/// On Windows an icon by the clock too, where people look for what runs, and it needs no page to work.
#[cfg(windows)]
fn tray(app: &AppHandle) -> tauri::Result<()> {
    use tauri::menu::{Menu, MenuItem};
    use tauri::tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent};
    let item = |id, text| MenuItem::with_id(app, id, text, true, None::<&str>);
    let (hide, dashboard) = (item("hide", "Hide")?, item("dashboard", "Open dashboard")?);
    let mut icon = TrayIconBuilder::with_id("tray")
        .tooltip("The Machine")
        .menu(&Menu::with_items(app, &[&hide, &dashboard, &item("quit", "Quit")?])?)
        .show_menu_on_left_click(false)
        .on_menu_event(|app, event| {
            let id = event.id.as_ref().to_string();
            later(app, move |app| match id.as_str() {
                "hide" if app.state::<Shared>().hidden.load(Ordering::Relaxed) => chosen(app, "show"),
                id => chosen(app, id),
            });
        })
        .on_tray_icon_event(|icon, event| {
            if let TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. } = event {
                later(icon.app_handle(), show_or_toggle);
            }
        });
    if let Some(image) = app.default_window_icon() {
        icon = icon.icon(image.clone());
    }
    icon.build(app)?;
    app.manage(TrayItems { hide, dashboard });
    follow_tray(app);
    Ok(())
}

#[cfg(windows)]
struct TrayItems {
    hide: tauri::menu::MenuItem<tauri::Wry>,
    dashboard: tauri::menu::MenuItem<tauri::Wry>,
}

/// The icon by the clock has the robot's dot too, and its menu what can be done now.
fn follow_tray(app: &AppHandle) {
    #[cfg(windows)]
    if let (Some(items), Some(icon), Some(image)) = (app.try_state::<TrayItems>(), app.tray_by_id("tray"), app.default_window_icon()) {
        let shared = app.state::<Shared>();
        let _ = items.hide.set_text(if shared.hidden.load(Ordering::Relaxed) { "Show robot" } else { "Hide" });
        let _ = items.dashboard.set_enabled(shared.machine().is_some());
        let count = shared.count();
        let _ = icon.set_icon(Some(if shared.dot.load(Ordering::Relaxed) { dotted(image) } else { image.clone() }));
        let _ = icon.set_tooltip(Some(if count > 0 { format!("The Machine. {count} for you.") } else { "The Machine".into() }));
    }
    #[cfg(not(windows))]
    let _ = app;
}

#[cfg(windows)]
fn dotted(image: &tauri::image::Image<'_>) -> tauri::image::Image<'static> {
    let (w, h) = (image.width(), image.height());
    let (mut px, r) = (image.rgba().to_vec(), w as f64 * 0.22);
    for (i, p) in px.chunks_exact_mut(4).enumerate() {
        let (x, y) = ((i as u32 % w) as f64 + 0.5, (i as u32 / w) as f64 + 0.5);
        if (x - (w as f64 - r)).hypot(y - r) <= r {
            p.copy_from_slice(&[0xe2, 0x70, 0x3a, 0xff]);
        }
    }
    tauri::image::Image::new_owned(px, w, h)
}

fn watch(app: AppHandle) {
    let looking = app.clone();
    let looker = std::thread::spawn(move || loop {
        let _ = look(&looking);
        std::thread::park_timeout(LOOK);
    });
    *app.state::<Shared>().looker.lock().unwrap() = Some(looker.thread().clone());
    #[cfg(windows)]
    std::thread::spawn(move || loop {
        std::thread::sleep(Duration::from_secs(3));
        let full = windows::full_screen();
        let here = app.clone();
        let _ = app.run_on_main_thread(move || {
            windows::follow_screens(&here);
            if here.state::<Shared>().full.swap(full, Ordering::Relaxed) != full {
                here.state::<Shared>().look_soon(); // whether it speaks
            }
            windows::show_or_not(&here);
        });
    });
    #[cfg(not(windows))]
    let _ = app;
}

fn main() {
    // GNOME's Wayland has no layer-shell, and a plain Wayland window can't stay on top or keep its place: XWayland can.
    #[cfg(target_os = "linux")]
    if std::env::var_os("GDK_BACKEND").is_none()
        && std::env::var_os("DISPLAY").is_some()
        && std::env::var("XDG_CURRENT_DESKTOP").is_ok_and(|d| d.to_uppercase().contains("GNOME"))
    {
        std::env::set_var("GDK_BACKEND", "x11");
    }
    #[cfg(windows)]
    if std::env::args().nth(1).as_deref() == Some("--quit") && quit::event::ask() {
        return;
    }
    tauri::Builder::default()
        .plugin(tauri_plugin_single_instance::init(|app, args, _| {
            // Started again: --toggle (for a key the person binds), --quit, or just show the robot. Or a sign-in comes
            // back.
            if args.get(1).is_some_and(|a| a == "--quit") {
                return quit::quit(app);
            }
            later(app, move |app| match args.get(1).map(String::as_str) {
                Some("--toggle") => toggle(app),
                #[cfg(feature = "sandbox")]
                Some("--hang") => std::thread::sleep(Duration::from_secs(60)), // for smoke/: --quit still has to work
                Some(link) if link.starts_with(signin::SCHEME) => came_back(app, link),
                _ => {
                    show(app);
                    if app.state::<Shared>().machine().is_none() {
                        open(app);
                    }
                }
            });
        }))
        .plugin(tauri_plugin_deep_link::init())
        .plugin(tauri_plugin_opener::Builder::new().open_js_links_on_click(false).build()) // the pages have no links of their own (card.rs)
        .invoke_handler(tauri::generate_handler![
            robot_state, robot_grab, robot_drag, robot_drop, robot_click, robot_menu, robot_take, robot_list, box_state, box_look, box_fit, box_draft, box_close,
            connect, sign_in, add_todo, add_file, remove_file, take_screenshot, todo_quick, todo_decide, todo_undo, ask, open_dashboard, menu_item,
            card_open, card_place, card_close, set_speaks, bubble_state, bubble_fit, bubble_hold, bubble_open, bubble_done
        ])
        .on_window_event(|window, event| {
            // Alt+F4 closes the box. On the robot it quits, on Windows: on Linux a monitor that goes away closes it too.
            if let WindowEvent::CloseRequested { api, .. } = event {
                api.prevent_close();
                if window.label() == "bubble" {
                    speak::done(window.app_handle());
                } else if window.label() != "robot" {
                    windows::close_box(window.app_handle());
                } else if cfg!(windows) {
                    quit::quit(window.app_handle());
                }
            }
            if let WindowEvent::ScaleFactorChanged { .. } = event {
                later(window.app_handle(), windows::place); // once the window system is done with its own move
            }
        })
        .setup(|app| {
            if std::env::args().nth(1).as_deref() == Some("--quit") {
                std::process::exit(0); // nothing was running
            }
            #[cfg(target_os = "linux")]
            if let Ok(own) = std::env::current_exe() {
                windows::linux::keep(&own.with_file_name("lib/libgtk-layer-shell.so.0"));
            }
            #[cfg(target_os = "linux")]
            let layer = windows::linux::has_layer_shell();
            #[cfg(not(target_os = "linux"))]
            let layer = false;
            let file = app.path().app_config_dir()?.join("app.json");
            app.manage(Shared {
                saved: Mutex::new(Saved::read(&file)),
                file,
                waiting: Mutex::default(),
                held: Mutex::default(),
                looking: Mutex::default(),
                looker: Mutex::default(),
                problem: Mutex::default(),
                now: Mutex::default(),
                compact: Mutex::default(),
                card: Mutex::default(),
                added: Mutex::default(),
                speaking: Mutex::default(),
                wanted: Mutex::default(),
                tall: Mutex::new(90.0),
                dot: AtomicBool::new(false),
                snip: AtomicBool::new(false),
                picking: AtomicBool::new(false),
                pending: Mutex::default(),
                alone: Mutex::default(),
                height: Mutex::new(200.0),
                open: AtomicBool::new(false),
                opened: AtomicU64::new(0),
                hidden: AtomicBool::new(false),
                away: AtomicBool::new(false),
                full: AtomicBool::new(false),
                draft: AtomicBool::new(false),
                notice: AtomicBool::new(false),
                menu: AtomicBool::new(false),
                grab: Mutex::default(),
                #[cfg(windows)]
                screens: Mutex::default(),
                layer,
            });
            if app.state::<Shared>().machine().is_some() {
                app.state::<Shared>().save(); // its name, made once
            }
            // Left by a sign-in that was cut off
            if app.deep_link().is_registered(signin::SCHEME).unwrap_or(false) {
                no_links(app.handle());
            }
            #[cfg(windows)]
            quit::event::wait(app.handle());
            windows::start(app.handle())?;
            #[cfg(windows)]
            tray(app.handle())?;
            if app.state::<Shared>().machine().is_none() {
                open(app.handle()); // it says what it is, and signs in
            }
            watch(app.handle().clone());
            let here = app.handle().clone();
            std::thread::spawn(move || here.state::<Shared>().snip.store(snip::there(), Ordering::Relaxed));
            front::watch(app.handle());
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("The Machine could not start")
        .run(|app, event| {
            if let RunEvent::Exit = event {
                if app.state::<Shared>().pending.lock().unwrap().is_some() {
                    no_links(app);
                }
            }
        });
}
