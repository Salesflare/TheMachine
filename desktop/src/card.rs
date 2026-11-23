//! One to-do in the box, by its Machine's own dashboard: its compact page (`?compact=1#card=<id>`), in a web view of its own
//! that lies over the place the box's page keeps for it. It is the dashboard, so what is approved there is read there first.
//! The page gets none of the app's commands (no capability names this window), keeps nothing on the disk, and stays on that
//! page of its Machine: its other links open the app or the browser. It tells its state in its title, "<state>: <to-do>".
use crate::place::{Rect, BOX_WIDTH, SHADOW};
use crate::{later, windows, Shared};
use std::sync::atomic::Ordering;
use std::time::Duration;
use tauri::webview::{Cookie, NewWindowResponse};
use tauri::{AppHandle, Emitter, Manager, WebviewUrl, WebviewWindow, WebviewWindowBuilder};
use tauri_plugin_opener::OpenerExt;
use url::Url;

const STATES: [&str; 6] = ["open", "done", "snoozed", "gone", "signed-out", "offline"];
/// Where the page goes to say Escape: nowhere, it is only heard.
const BACK: &str = "https://robot.invalid/back";
/// Escape that the page has nothing of its own to close with.
const ESCAPE: &str = r#"addEventListener('keydown', e => {
  if (e.key !== 'Escape' || e.isComposing) return;
  const open = document.querySelector('dialog[open]');
  setTimeout(() => { if (!open && !e.defaultPrevented) location.href = 'https://robot.invalid/back'; });
}, true);"#;

/// How tall its page is; all the room there is for its chat, and while a dialog or menu would be cut off. 0: as it is.
const TALL: &str = r#"(() => {
  const open = [...document.querySelectorAll('dialog[open],.more-actions[open],.row-menu,.project-picker,#share-pop,#cm-menu')].filter(x => x.getClientRects().length);
  const cut = x => { const r = x.getBoundingClientRect(); return r.top < 0 || r.bottom > innerHeight + 1 || x.scrollHeight > x.clientHeight + 1; };
  if (document.body.classList.contains('chat-open') || open.some(x => [x, ...x.children].some(cut))) return 9999;
  return open.length ? 0 : Math.ceil(document.body.getBoundingClientRect().height);
})()"#;

#[derive(Default)]
pub struct Card {
    /// The to-do that is open, and how far its page is.
    todo: Option<String>,
    drawn: bool,
    /// The page's address, while it is loaded: another to-do is then a step within it.
    loaded: Option<Url>,
    /// Its place in the box's window: from the top, and how tall.
    place: Option<(f64, f64)>,
    /// How tall its page was last.
    tall: f64,
}

/// What the page is: the Machine's own address with compact=1. Frames of what a mail has are about:srcdoc.
fn own(machine: &str, url: &Url) -> bool {
    let Ok(machine) = Url::parse(machine) else { return false };
    let compact = url.origin() == machine.origin() && url.path() == machine.path() && url.query_pairs().any(|(k, v)| k == "compact" && v == "1");
    compact || matches!(url.as_str(), "about:blank" | "about:srcdoc")
}

/// What "<state>: <to-do>" says.
fn state(title: &str) -> Option<&'static str> {
    let word = title.split(':').next()?.trim();
    STATES.into_iter().find(|s| *s == word)
}

/// Where a link that leaves the page goes: the app for this Machine's own, the browser for the web's, else nowhere.
#[derive(Debug, PartialEq)]
enum Link {
    Dashboard(String),
    Web,
    No,
}

fn link(machine: &str, url: &Url) -> Link {
    let own = Url::parse(machine).is_ok_and(|m| m.origin() == url.origin());
    match (own, url.as_str().strip_prefix(machine), url.scheme()) {
        (true, Some(path), _) => Link::Dashboard(path.into()),
        (_, _, "https" | "http" | "mailto") => Link::Web,
        _ => Link::No,
    }
}

/// On Windows it is made at the start, as the other windows; elsewhere when it is first opened.
pub fn build(app: &AppHandle) -> tauri::Result<WebviewWindow> {
    let (here, there, told) = (app.clone(), app.clone(), app.clone());
    let mut window = WebviewWindowBuilder::new(app, "card", WebviewUrl::External("about:blank".parse().unwrap()))
        .title("The Machine")
        .inner_size(BOX_WIDTH, 400.0)
        .decorations(false)
        .shadow(false)
        .resizable(false)
        .maximizable(false)
        .minimizable(false)
        .always_on_top(true)
        .visible_on_all_workspaces(true)
        .skip_taskbar(true)
        .visible(false)
        .incognito(true)
        .disable_drag_drop_handler()
        .additional_browser_args(&windows::browser())
        .initialization_script(ESCAPE)
        .on_navigation(move |url| {
            if url.as_str() == BACK {
                say(&here, "back");
                return false;
            }
            here.state::<Shared>().signed_in().is_some_and(|(machine, _)| own(&machine, url))
        })
        .on_new_window(move |url, _| {
            later(&there, move |app| follow(app, &url));
            NewWindowResponse::Deny
        })
        .on_download(|_, _| false)
        .on_document_title_changed(move |_, title| {
            let Some(state) = state(&title) else { return };
            say(&told, state);
            later(&told, |app| {
                app.state::<Shared>().card.lock().unwrap().drawn = true;
                show(app);
            });
        });
    if let Some(under) = app.get_webview_window("box").filter(|_| !app.state::<Shared>().layer) {
        #[cfg(windows)]
        {
            window = window.owner(&under)?; // above it, also when that is clicked
        }
        #[cfg(target_os = "linux")]
        {
            window = window.transient_for(&under)?;
        }
        let _ = under;
    }
    let window = window.build()?;
    #[cfg(target_os = "linux")]
    windows::linux::prepare(app, &window, "card")?;
    #[cfg(windows)]
    windows::no_menu(&window);
    Ok(window)
}

fn say(app: &AppHandle, state: &str) {
    if app.state::<Shared>().card.lock().unwrap().todo.is_some() {
        let _ = app.emit_to("box", "card", state);
    }
}

fn follow(app: &AppHandle, url: &Url) {
    let Some((machine, _)) = app.state::<Shared>().signed_in() else { return };
    match link(&machine, url) {
        Link::Dashboard(path) => {
            if crate::open_path(app, &path).is_ok() {
                windows::close_box(app);
            }
        }
        Link::Web => {
            let _ = app.opener().open_url(url.as_str(), None::<&str>);
        }
        Link::No => {}
    }
}

/// Starts loading it; it shows once the page has drawn it.
pub fn open(app: &AppHandle, todo: &str) -> tauri::Result<()> {
    let shared = app.state::<Shared>();
    let Some(machine) = shared.machine().filter(|_| windows::box_open(app)) else { return Ok(()) };
    let Ok(url) = Url::parse(&format!("{}?compact=1#card={todo}", machine.url)) else { return Ok(()) };
    let was = std::mem::take(&mut *shared.card.lock().unwrap()).loaded;
    let drawn = was.as_ref() == Some(&url);
    *shared.card.lock().unwrap() = Card { todo: Some(todo.into()), drawn, loaded: Some(url.clone()), place: None, tall: 0.0 };
    let window = match app.get_webview_window("card") {
        Some(w) => w,
        None => build(app)?,
    };
    for (name, value) in machine.cookie.iter().flat_map(|c| c.split("; ")).filter_map(|c| c.split_once('=')) {
        let host = url.host_str().unwrap_or_default().to_string();
        window.set_cookie(Cookie::build((name.to_string(), value.to_string())).domain(host).path("/").secure(true).http_only(true).build())?;
    }
    if was.is_some() && !drawn {
        after(app, Duration::from_millis(1500), { // the same title: nothing says that it is drawn
            let todo = todo.to_string();
            move |app| {
                let shared = app.state::<Shared>();
                let mut card = shared.card.lock().unwrap();
                card.drawn |= card.todo.as_ref() == Some(&todo);
                drop(card);
                show(app);
            }
        });
    }
    if drawn { Ok(()) } else { window.navigate(url) }
}

fn after(app: &AppHandle, wait: Duration, work: impl FnOnce(&AppHandle) + Send + 'static) {
    let app = app.clone();
    std::thread::spawn(move || {
        std::thread::sleep(wait);
        later(&app, work);
    });
}

/// The box's page says where its place is.
pub fn put(app: &AppHandle, top: f64, height: f64) {
    if (0.0..=900.0).contains(&top) && (50.0..=900.0).contains(&height) {
        app.state::<Shared>().card.lock().unwrap().place = Some((top, height));
        windows::place(app);
        show(app);
    }
}

/// Where it is, over the box's window.
pub fn at(app: &AppHandle, around: Rect) -> Option<Rect> {
    let shared = app.state::<Shared>();
    let card = shared.card.lock().unwrap();
    let (top, height) = card.todo.as_ref().and(card.place)?;
    Some(Rect { x: around.x + SHADOW + 2.0, y: around.y + top, w: BOX_WIDTH - 4.0, h: height })
}

fn show(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let ready = {
        let card = shared.card.lock().unwrap();
        card.todo.is_some() && card.drawn && card.place.is_some()
    };
    let Some(window) = app.get_webview_window("card") else { return };
    if ready && shared.open.load(Ordering::Relaxed) && !window.is_visible().unwrap_or(true) {
        windows::place(app);
        let _ = window.show();
        windows::place(app);
        let _ = window.set_focus();
        let todo = shared.card.lock().unwrap().todo.clone();
        after(app, Duration::from_millis(100), move |app| measure(app, todo)); // it shows a moment later
    }
}

/// The box follows its page's height while it is open.
fn measure(app: &AppHandle, todo: Option<String>) {
    let Some(window) = app.get_webview_window("card") else { return };
    if app.state::<Shared>().card.lock().unwrap().todo != todo || !window.is_visible().unwrap_or(false) {
        return;
    }
    let told = app.clone();
    let _ = window.eval_with_callback(TALL, move |answer| {
        let Ok(tall) = answer.trim_matches('"').parse::<f64>() else { return };
        let shared = told.state::<Shared>();
        let mut card = shared.card.lock().unwrap();
        if card.todo.is_some() && card.tall != tall && tall > 0.0 {
            card.tall = tall;
            let _ = told.emit_to("box", "tall", tall);
        }
    });
    after(app, Duration::from_millis(400), move |app| measure(app, todo));
}

/// Back to the list. Its page stays a minute, for the next one.
pub fn back(app: &AppHandle) {
    {
        let shared = app.state::<Shared>();
        let mut card = shared.card.lock().unwrap();
        (card.todo, card.place) = (None, None);
    }
    if let Some(window) = app.get_webview_window("card") {
        let _ = window.hide();
        if let (true, Some(under)) = (windows::box_open(app), app.get_webview_window("box")) {
            let _ = under.set_focus();
        }
    }
    after(app, Duration::from_secs(60), |app| {
        if app.state::<Shared>().card.lock().unwrap().todo.is_none() {
            close(app);
        }
    });
}

/// Its page goes, with the box.
pub fn close(app: &AppHandle) {
    let was = std::mem::take(&mut *app.state::<Shared>().card.lock().unwrap());
    let Some(window) = app.get_webview_window("card") else { return };
    let _ = window.hide();
    #[cfg(windows)]
    if was.loaded.is_some() {
        let _ = window.navigate("about:blank".parse().unwrap());
    }
    #[cfg(not(windows))]
    {
        let _ = (was, window.destroy());
    }
}

/// Signed out: nothing of it is left.
pub fn forget(app: &AppHandle) {
    close(app);
    if let Some(window) = app.get_webview_window("card") {
        let _ = window.clear_all_browsing_data();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const OWN: &str = "https://host.example/machine/";

    #[test]
    fn it_stays_on_its_page() {
        let at = |u: &str| own(OWN, &u.parse().unwrap());
        for yes in ["?compact=1#card=aa01", "?compact=1", "?compact=1&x=2#chat=aa01"] {
            assert!(at(&format!("{OWN}{yes}")), "{yes}");
        }
        assert!(at("about:blank") && at("about:srcdoc"));
        for no in [
            OWN, "https://host.example/machine/?compact=11", "https://host.example/machine/settings?compact=1", "https://host.example/?compact=1",
            "http://host.example/machine/?compact=1", "https://host.example:8443/machine/?compact=1", "https://other.example/machine/?compact=1",
            "https://host.example/machine/?x=compact=1", "about:config", "data:text/html,x", "javascript:1", "file:///etc/passwd", "tauri://localhost/box.html",
            "https://tauri.localhost/box.html",
        ] {
            assert!(!at(no), "{no}");
        }
        assert!(!own("", &"about:srcdoc".parse().unwrap()));
    }

    #[test]
    fn a_link_out_goes_to_the_app_or_the_browser() {
        let to = |u: &str| link(OWN, &u.parse().unwrap());
        assert_eq!(to("https://host.example/machine/#person=7"), Link::Dashboard("#person=7".into()));
        assert_eq!([to("https://host.example/other/"), to("https://host.example.evil/machine/"), to("mailto:a@b.example")], [Link::Web, Link::Web, Link::Web]);
        assert_eq!([to("javascript:1"), to("file:///etc/passwd"), to("tauri://localhost/"), to("data:text/html,x"), to("ms-settings:x")].iter().filter(|l| **l == Link::No).count(), 5);
    }

    #[test]
    fn its_title_says_its_state() {
        assert_eq!([state("open: Answer Nora: lunch"), state("signed-out:"), state("done"), state("The Machine"), state("opened: x"), state("")],
            [Some("open"), Some("signed-out"), Some("done"), None, None, None]);
    }
}
