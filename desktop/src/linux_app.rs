//! What the dashboard's window has on Linux besides what it has everywhere: its keys, a menu of the page with what has no
//! other place here, finding, a page that ended, and the desktop's own notifications (org.freedesktop.Notifications).
use crate::given::{GivenFile, FILES};
use crate::keys::{self, Does, Held};
use crate::notify::{self, Lets};
use crate::{dash, later};
use gtk::prelude::*;
use std::cell::RefCell;
use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;
use tauri::{AppHandle, Manager, WebviewWindow};
use webkit2gtk::{ContextMenuExt, CookieManagerExt, WebsiteDataManagerExt, ContextMenuItem, DownloadExt, FindController, FindControllerExt, FindOptions, URIRequestExt, URIResponseExt, WebContextExt, WebView, WebViewExt};
use zbus::blocking::{connection::Builder, Connection, MessageIterator, Proxy};
use zbus::zvariant::Value;

/// A page that ends is there again.
pub fn lives(window: &WebviewWindow) {
    let (app, label) = (window.app_handle().clone(), window.label().to_string());
    let _ = window.with_webview(move |page| {
        page.inner().connect_web_process_terminated(move |_, _| {
            let label = label.clone();
            later(&app, move |app| dash::died(app, &label));
        });
        // What it types in has no undo of its own. Only what the page leaves comes past here
        let view = page.inner();
        if let Some(around) = view.parent() {
            around.connect_key_press_event(move |_, event| {
                let held = event.state() & (gtk::gdk::ModifierType::CONTROL_MASK | gtk::gdk::ModifierType::SHIFT_MASK | gtk::gdk::ModifierType::MOD1_MASK);
                let again = held.contains(gtk::gdk::ModifierType::SHIFT_MASK);
                let does = match named(event.keyval()).as_str() {
                    "z" if again => "Redo",
                    "z" => "Undo",
                    "y" if !again => "Redo",
                    _ => return gtk::glib::Propagation::Proceed,
                };
                if !held.contains(gtk::gdk::ModifierType::CONTROL_MASK) || held.contains(gtk::gdk::ModifierType::MOD1_MASK) {
                    return gtk::glib::Propagation::Proceed;
                }
                view.execute_editing_command(does);
                gtk::glib::Propagation::Stop
            });
        }
    });
}

/// In front, as someone asked for now. GTK asks with the time they last did something in the app, and on X11 a window
/// manager may take that as older than what they do in another one.
pub fn front(window: &WebviewWindow) {
    let _ = window.set_focus();
    let Ok(window) = window.gtk_window() else { return };
    gtk::glib::timeout_add_local_once(std::time::Duration::from_millis(80), move || {
        let shown = window.window().filter(|w| w.is_visible()).and_then(|w| w.downcast::<gdkx11::X11Window>().ok());
        if let Some(shown) = shown.filter(|_| !window.is_active()) {
            window.present_with_time(gdkx11::functions::x11_get_server_time(&shown));
        }
    });
}

/// A session's cookies, for the page at this host. wry's own runs the main loop until each is there, which may be never.
pub fn cookies(window: &WebviewWindow, cookies: Vec<(String, String)>, host: String, secure: bool, done: impl Fn() + Send + 'static) {
    let _ = window.with_webview(move |page| {
        let Some(manager) = page.inner().website_data_manager().and_then(|m| m.cookie_manager()) else { return done() };
        let left = std::rc::Rc::new((std::cell::Cell::new(cookies.len()), done));
        for (name, value) in cookies {
            let mut cookie = soup::Cookie::new(&name, &value, &host, "/", -1);
            cookie.set_http_only(true);
            cookie.set_secure(secure);
            let left = left.clone();
            manager.add_cookie(&mut cookie, None::<&gtk::gio::Cancellable>, move |_| {
                left.0.set(left.0.get() - 1);
                if left.0.get() == 0 {
                    (left.1)();
                }
            });
        }
    });
}

thread_local! {
    static UNDER_WAY: RefCell<Vec<webkit2gtk::Download>> = const { RefCell::new(Vec::new()) };
}

/// What the app's pages download, for their names: one for all of them.
pub fn keeps(window: &WebviewWindow) {
    static ONCE: AtomicBool = AtomicBool::new(false);
    if ONCE.swap(true, Ordering::Relaxed) {
        return;
    }
    let _ = window.with_webview(|page| {
        if let Some(all) = page.inner().context() {
            all.connect_download_started(|_, started| {
                UNDER_WAY.with_borrow_mut(|under_way| under_way.push(started.clone()));
                started.connect_finished(|over| UNDER_WAY.with_borrow_mut(|under_way| under_way.retain(|d| d != over)));
            });
        }
    });
}

/// The name a file is sent with: WebKitGTK's has no spaces.
pub fn sent_as(url: &url::Url) -> Option<String> {
    UNDER_WAY.with_borrow(|under_way| {
        let its = under_way.iter().rfind(|d| d.request().and_then(|r| r.uri()).is_some_and(|u| u == url.as_str()))?;
        crate::machine::file_name(&its.response()?.http_headers()?.one("Content-Disposition")?)
    })
}

pub fn prepare(window: &WebviewWindow) {
    lives(window);
    let (app, label) = (window.app_handle().clone(), window.label().to_string());
    if let Ok(whole) = window.gtk_window() {
        let (here, of) = (app.clone(), label.clone());
        whole.connect_key_press_event(move |_, event| {
            let state = event.state();
            let held = Held {
                ctrl: state.contains(gtk::gdk::ModifierType::CONTROL_MASK),
                shift: state.contains(gtk::gdk::ModifierType::SHIFT_MASK),
                alt: state.contains(gtk::gdk::ModifierType::MOD1_MASK),
            };
            match keys::does(&of, &named(event.keyval()), held) {
                Some(what) => {
                    let of = of.clone();
                    later(&here, move |app| keys::run(app, &of, what));
                    gtk::glib::Propagation::Stop
                }
                None => gtk::glib::Propagation::Proceed,
            }
        });
    }
    let _ = window.with_webview(move |page| {
        let page = page.inner();
        shade(&page);
        if dash::label(&label) {
            menu(&app, &label, &page);
        }
        if label == dash::LABEL {
            drops(&app, &page);

            let here = app.clone();
            page.connect_scroll_event(move |_, event| {
                if !event.state().contains(gtk::gdk::ModifierType::CONTROL_MASK) {
                    return gtk::glib::Propagation::Proceed;
                }
                let step = match event.direction() {
                    gtk::gdk::ScrollDirection::Up => 1,
                    gtk::gdk::ScrollDirection::Down => -1,
                    _ => 0, // a touchpad's is far finer than a step
                };
                if step != 0 {
                    later(&here, move |app| dash::zoom(app, step));
                }
                gtk::glib::Propagation::Stop
            });
        }
        let room = page.parent().and_then(|p| p.downcast::<gtk::Box>().ok()).filter(|_| label == dash::LABEL);
        if let Some(room) = room {
            let bar = bar_in(&room, &page);
            FIND.with_borrow_mut(|f| *f = bar);
        }
    });
}

/// What isn't drawn yet while it scrolls fast has the page's own color, as in a browser, not WebKitGTK's white: its
/// theme-color, which the dashboard keeps in step with its theme (light, dark, Omarchy's). WebKitGTK has it since 2.50.
fn shade(page: &WebView) {
    if page.find_property("theme-color").is_none() {
        return;
    }
    let follow = |page: &WebView| {
        let color = page.property::<Option<gtk::gdk::RGBA>>("theme-color");
        if let Some(color) = color.filter(|c| c.alpha() > 0.9) {
            page.set_background_color(&color);
        }
    };
    follow(page);
    page.connect_notify_local(Some("theme-color"), move |page, _| follow(page));
}

/// A key as keys.rs has it.
fn named(key: gtk::gdk::keys::Key) -> String {
    let name = key.name().map(|n| n.to_string()).unwrap_or_default();
    match name.as_str() {
        "KP_Add" => "+".into(),
        "KP_Subtract" => "-".into(),
        "KP_0" | "KP_Insert" => "0".into(),
        _ => key.to_unicode().filter(|c| !c.is_control()).map_or(name, |c| c.to_lowercase().to_string()),
    }
}

/// The page's own menu, with what has a menu or an icon elsewhere.
fn menu(app: &AppHandle, label: &str, page: &WebView) {
    let (app, label) = (app.clone(), label.to_string());
    page.connect_context_menu(move |_, menu, _, _| {
        let mine: &[(&str, Does)] = if label == dash::LABEL {
            &[("Find…", Does::Find(0)), ("Settings…", Does::Settings), ("Quit The Machine", Does::Quit)]
        } else {
            &[("Save a Copy", Does::Save), ("Print…", Does::Print)]
        };
        menu.append(&ContextMenuItem::new_separator());
        for (name, what) in mine {
            let action = gtk::gio::SimpleAction::new("the-machine", None);
            let (app, label, what) = (app.clone(), label.clone(), *what);
            action.connect_activate(move |_, _| {
                let label = label.clone();
                later(&app, move |app| keys::run(app, &label, what));
            });
            menu.append(&ContextMenuItem::from_gaction(&action, name, None));
        }
        false
    });
}

/// Files dropped on the page: WebKitGTK gives it none, so it is told of them here as any browser tells it.
fn drops(app: &AppHandle, page: &WebView) {
    let (over, view) = (app.clone(), page.clone());
    let (dropped, its) = (app.clone(), page.clone());
    crate::windows::linux::dropped(page, false, move |at| {
        let (kind, at) = at.map_or(("dragleave", (0, 0)), |at| ("dragover", at));
        tell(&over, drop_script(kind, at, view.zoom_level(), &[]));
    }, move |paths, at| {
        let (app, zoom) = (dropped.clone(), its.zoom_level());
        std::thread::spawn(move || {
            // One more than it takes, and a little more of a file than it takes: the page says so itself
            let files: Vec<_> = paths.iter().take(FILES + 1).filter_map(|p| GivenFile::read(p)).map(|(file, _)| file).collect();
            tell(&app, drop_script("drop", at, zoom, &files));
        });
    });
}

fn tell(app: &AppHandle, script: String) {
    if let Some(window) = app.get_webview_window(dash::LABEL) {
        let _ = window.eval(script);
    }
}

fn drop_script(kind: &str, at: (i32, i32), zoom: f64, files: &[GivenFile]) -> String {
    let files = serde_json::to_string(files).unwrap_or_default();
    format!("({DROP})({kind:?},{},{},{files})", f64::from(at.0) / zoom, f64::from(at.1) / zoom)
}

const DROP: &str = r#"(kind, x, y, files) => {
  const data = new DataTransfer(), was = window.machineDragged, at = kind === 'dragleave' ? null : document.elementFromPoint(x, y);
  for (const f of files) data.items.add(new File([Uint8Array.from(atob(f.data), c => c.charCodeAt(0))], f.name, {type: f.kind}));
  if (kind !== 'drop') data.items.add(new File([], ''));
  const fire = (type, to) => to?.dispatchEvent(new DragEvent(type, {bubbles: true, cancelable: true, composed: true, clientX: x, clientY: y, dataTransfer: data}));
  window.machineDragged = kind === 'dragover' ? at : null;
  if (kind === 'drop') return files.length ? fire('drop', at) : fire('dragleave', was);
  if (at && at !== was) fire('dragenter', at);
  if (was && at !== was) fire('dragleave', was);
  if (at) fire('dragover', at);
}"#;

// Find

struct Bar {
    bar: gtk::SearchBar,
    words: gtk::SearchEntry,
    looks: FindController,
}

thread_local! {
    static FIND: RefCell<Option<Bar>> = const { RefCell::new(None) };
}

const HOW: FindOptions = FindOptions::CASE_INSENSITIVE.union(FindOptions::WRAP_AROUND);
const MOST: u32 = 1000;

/// Above the page, hidden until it is asked for.
fn bar_in(room: &gtk::Box, page: &WebView) -> Option<Bar> {
    let looks = page.find_controller()?;
    let bar = gtk::SearchBar::builder().show_close_button(true).build();
    let row = gtk::Box::new(gtk::Orientation::Horizontal, 6);
    let words = gtk::SearchEntry::builder().placeholder_text("Find").width_chars(32).build();
    let button = |icon, tip| {
        let b = gtk::Button::from_icon_name(Some(icon), gtk::IconSize::Button);
        b.set_tooltip_text(Some(tip));
        b.style_context().add_class("flat");
        b
    };
    let (before, next) = (button("go-up-symbolic", "Find Previous"), button("go-down-symbolic", "Find Next"));
    row.pack_start(&words, false, false, 0);
    row.pack_start(&before, false, false, 0);
    row.pack_start(&next, false, false, 0);
    bar.add(&row);
    bar.connect_entry(&words);
    room.pack_start(&bar, false, false, 0);
    room.reorder_child(&bar, 0);
    bar.show_all();

    let look = looks.clone();
    words.connect_search_changed(move |words| match words.text().as_str() {
        "" => look.search_finish(),
        text => look.search(text, HOW.bits(), MOST),
    });
    let (b, n) = (looks.clone(), looks.clone());
    before.connect_clicked(move |_| b.search_previous());
    next.connect_clicked(move |_| n.search_next());
    let n = looks.clone();
    words.connect_activate(move |_| n.search_next());
    let over = bar.clone();
    words.connect_key_press_event(move |_, event| {
        let ends = event.keyval() == gtk::gdk::keys::constants::Escape;
        if ends {
            over.set_search_mode(false);
        }
        ends.into()
    });
    let here = words.clone();
    looks.connect_failed_to_find_text(move |_| here.style_context().add_class("error"));
    let here = words.clone();
    // Its marks are yellow under white words in the dark: the one it is at is enough
    looks.connect_found_text(move |looks, _| {
        here.style_context().remove_class("error");
        looks.search_finish();
    });
    let (over, back, text) = (looks.clone(), page.clone(), words.clone());
    bar.connect_search_mode_enabled_notify(move |bar| {
        if !bar.is_search_mode() {
            over.search_finish();
            text.style_context().remove_class("error");
            back.grab_focus();
        }
    });
    Some(Bar { bar, words, looks })
}

/// 0: the bar, else the next or the one before.
pub fn find(step: i8) {
    FIND.with_borrow(|find| {
        let Some(find) = find else { return };
        if step == 0 || !find.bar.is_search_mode() {
            find.bar.set_search_mode(true);
            find.words.grab_focus();
            let text = find.words.text();
            if !text.is_empty() {
                find.looks.search(&text, HOW.bits(), MOST); // what it looked for last
            }
        } else if step > 0 {
            find.looks.search_next();
        } else {
            find.looks.search_previous();
        }

    });
}

// Notifications

const SHOWS: &str = "org.freedesktop.Notifications";

/// While they are on.
static BUS: Mutex<Option<Connection>> = Mutex::new(None);
/// Those that are there: the desktop's number for each, and its to-do.
static SHOWN: Mutex<Vec<(u32, String)>> = Mutex::new(Vec::new());
/// Nothing shows them.
static NONE: AtomicBool = AtomicBool::new(false);

fn proxy(bus: &Connection) -> zbus::Result<Proxy<'_>> {
    Proxy::new(bus, SHOWS, "/org/freedesktop/Notifications", SHOWS)
}

fn connect() -> zbus::Result<Connection> {
    Builder::session()?.method_timeout(std::time::Duration::from_secs(5)).build()
}

pub fn notices_on(_: &AppHandle, on: bool) {
    if !on {
        notices_clear();
        *BUS.lock().unwrap() = None;
        return;
    }
    std::thread::spawn(|| {
        if BUS.lock().unwrap().is_some() {
            return;
        }
        match connect() {
            Ok(bus) => {
                *BUS.lock().unwrap() = Some(bus.clone());
                NONE.store(!answers(&bus), Ordering::Relaxed);
                let _ = follow(&bus);
            }
            Err(_) => NONE.store(true, Ordering::Relaxed),
        }
    });
}

fn answers(bus: &Connection) -> bool {
    proxy(bus).and_then(|p| p.call::<_, _, Vec<String>>("GetCapabilities", &())).is_ok()
}

/// What the person does with them.
fn follow(bus: &Connection) -> zbus::Result<()> {
    let rule = zbus::MatchRule::builder().msg_type(zbus::message::Type::Signal).sender(SHOWS)?.interface(SHOWS)?.build();
    for message in MessageIterator::for_match_rule(rule, bus, None)? {
        let message = message?;
        let (header, body) = (message.header(), message.body());
        match header.member().map(|m| m.as_str().to_string()).as_deref() {
            Some("ActionInvoked") => {
                if let Ok((number, _)) = body.deserialize::<(u32, String)>() {
                    let todo = SHOWN.lock().unwrap().iter().find(|(n, _)| *n == number).map(|(_, id)| id.clone());
                    if let Some(id) = todo {
                        notify::opened(&id);
                    }
                }
            }
            Some("NotificationClosed") => {
                if let Ok((number, _)) = body.deserialize::<(u32, u32)>() {
                    SHOWN.lock().unwrap().retain(|(n, _)| *n != number);
                }
            }
            _ => {}
        }
        if BUS.lock().unwrap().is_none() {
            break; // turned off
        }
    }
    Ok(())
}

pub fn notices_lets() -> Lets {
    if NONE.load(Ordering::Relaxed) { Lets::No } else { Lets::Yes }
}

pub fn notice(id: &str, title: &str, line: &str) {
    let (id, title, line) = (id.to_string(), title.to_string(), line.to_string());
    std::thread::spawn(move || {
        let Some(bus) = BUS.lock().unwrap().clone() else { return };
        let was = SHOWN.lock().unwrap().iter().find(|(_, of)| *of == id).map_or(0, |(n, _)| *n);
        // A desktop may take the line for HTML: what would be a tag stays what it is
        let line = line.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;");
        let hints = HashMap::from([("suppress-sound", Value::from(true)), ("desktop-entry", Value::from("computer.themachine.desktop"))]);
        let shown = proxy(&bus).and_then(|p| p.call::<_, _, u32>("Notify", &("The Machine", was, "", title, line, vec!["default", "Open"], hints, -1i32)));
        NONE.store(shown.is_err(), Ordering::Relaxed);
        if let Ok(number) = shown {
            let mut all = SHOWN.lock().unwrap();
            all.retain(|(_, of)| *of != id);
            all.push((number, id));
        }
    });
}

pub fn notice_gone(id: &str) {
    let number = SHOWN.lock().unwrap().iter().find(|(_, of)| of == id).map(|(n, _)| *n);
    let bus = BUS.lock().unwrap().clone();
    if let (Some(number), Some(bus)) = (number, bus) {
        std::thread::spawn(move || {
            let _ = proxy(&bus).and_then(|p| p.call::<_, _, ()>("CloseNotification", &(number,)));
        });
    }
}

/// Without the program nothing answers a click on them.
pub fn notices_clear() {
    let all = std::mem::take(&mut *SHOWN.lock().unwrap());
    let bus = BUS.lock().unwrap().clone();
    if let Some(bus) = bus {
        for (number, _) in all {
            let _ = proxy(&bus).and_then(|p| p.call::<_, _, ()>("CloseNotification", &(number,)));
        }
    }
}
