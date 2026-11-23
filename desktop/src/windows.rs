//! The windows: the robot, the box that opens at it, a to-do over the box (card.rs), and the robot's bubble. On Wayland with
//! layer-shell (Hyprland, Sway, KDE) they are layer surfaces: a normal Wayland window can't stay on top or choose its
//! place. Elsewhere they are borderless windows that stay on top, out of the taskbar. All of this runs on the main thread.
use crate::place::{self, box_at, peek, tail, Corner, Rect, BOX_WIDTH, BUBBLE_WIDTH, ROBOT, SHADOW};
use crate::Shared;
use std::sync::atomic::Ordering;
#[cfg(not(windows))]
use std::time::Duration;
use tauri::{AppHandle, Emitter, Manager, PhysicalPosition, PhysicalSize, WebviewUrl, WebviewWindow, WebviewWindowBuilder};

/// A closed box's page stays loaded this long, so it opens at once again; then its memory goes. Not on Windows: there the
/// windows are made at the start and stay, as one that is made later, inside a page's call or a message, can wait forever.
#[cfg(not(windows))]
const KEEP: Duration = Duration::from_secs(120);

/// What Tauri asks of WebView2 itself. A sandbox build can also open its pages to smoke/windows.py, which reads them.
pub fn browser() -> String {
    let args = "--disable-features=msWebOOUI,msPdfOOUI,msSmartScreenProtection".to_string();
    match std::env::var("MACHINE_SANDBOX_DEBUG").ok().and_then(|p| p.parse::<u16>().ok()) {
        Some(port) if cfg!(feature = "sandbox") => format!("{args} --remote-debugging-port={port}"),
        _ => args,
    }
}

fn build(app: &AppHandle, label: &str, title: &str, (w, h): (f64, f64)) -> tauri::Result<WebviewWindow> {
    let keys = label == "box"; // only the box takes the keys
    let window = WebviewWindowBuilder::new(app, label, WebviewUrl::App(format!("{label}.html").into()))
        .title(title)
        .inner_size(w, h)
        .decorations(false)
        .transparent(true)
        .shadow(false)
        .resizable(false)
        .maximizable(false)
        .minimizable(false)
        .always_on_top(true)
        .visible_on_all_workspaces(true)
        .skip_taskbar(true)
        .focused(keys)
        .focusable(keys || cfg!(not(target_os = "linux")) || app.state::<Shared>().layer) // X11: it comes back by itself, so it never takes the keys
        .visible(false)
        .disable_drag_drop_handler() // the page takes dropped files itself
        .additional_browser_args(&browser())
        .on_navigation(|url| url.scheme() == "tauri" || url.host_str() == Some("tauri.localhost")) // only its own pages
        .build()?;
    #[cfg(target_os = "linux")]
    linux::prepare(app, &window, label)?;
    #[cfg(windows)]
    no_menu(&window);
    Ok(window)
}

/// Windows opens a window's menu on Alt alone: here an unseen one, that keeps the page waiting until a click. No menu then.
#[cfg(windows)]
pub fn no_menu(window: &WebviewWindow) {
    use windows_sys::Win32::Foundation::{HWND, LPARAM, LRESULT, WPARAM};
    use windows_sys::Win32::UI::Shell::{DefSubclassProc, SetWindowSubclass};
    use windows_sys::Win32::UI::WindowsAndMessaging::{SC_KEYMENU, WM_SYSCOMMAND};
    unsafe extern "system" fn told(window: HWND, message: u32, w: WPARAM, l: LPARAM, _: usize, _: usize) -> LRESULT {
        if message == WM_SYSCOMMAND && w & 0xFFF0 == SC_KEYMENU as usize {
            return 0;
        }
        // SAFETY: what Windows gave, passed on.
        unsafe { DefSubclassProc(window, message, w, l) }
    }
    if let Ok(hwnd) = window.hwnd() {
        // SAFETY: the program's own window, on its own thread; the function is the program's.
        unsafe { SetWindowSubclass(hwnd.0, Some(told), 1, 0) };
    }
}

pub fn start(app: &AppHandle) -> tauri::Result<()> {
    build(app, "robot", "The Machine", ROBOT)?;
    #[cfg(windows)]
    build_box(app)?;
    #[cfg(windows)]
    crate::card::build(app)?;
    build_bubble(app)?;
    show_robot(app);
    Ok(())
}

fn build_box(app: &AppHandle) -> tauri::Result<WebviewWindow> {
    let height = *app.state::<Shared>().height.lock().unwrap();
    build(app, "box", "The Machine", (BOX_WIDTH + 2.0 * SHADOW, height + 2.0 * SHADOW))
}

fn build_bubble(app: &AppHandle) -> tauri::Result<WebviewWindow> {
    let height = *app.state::<Shared>().tall.lock().unwrap();
    build(app, "bubble", "The Machine", (BUBBLE_WIDTH + 2.0 * SHADOW, height + 2.0 * SHADOW))
}

/// The robot says something (speak.rs). Its page says how tall it is, then it shows: fit_bubble.
pub fn open_bubble(app: &AppHandle) {
    match app.get_webview_window("bubble") {
        Some(window) => {
            let _ = window.emit("say", ());
        }
        None => {
            if let Err(error) = build_bubble(app) {
                eprintln!("could not open the bubble: {error}");
            }
        }
    }
}

/// The bubble's page has its words: it shows, never taking the focus.
pub fn fit_bubble(app: &AppHandle, height: f64) {
    *app.state::<Shared>().tall.lock().unwrap() = height.clamp(40.0, 400.0);
    let Some(window) = app.get_webview_window("bubble") else { return };
    if crate::speak::now(&app.state::<Shared>()).is_some() {
        place(app);
        if !window.is_visible().unwrap_or(false) {
            seen(&window, true);
            place(app);
        }
    }
}

pub fn close_bubble(app: &AppHandle) {
    let Some(window) = app.get_webview_window("bubble") else { return };
    #[cfg(windows)]
    seen(&window, false);
    #[cfg(not(windows))]
    let _ = window.destroy();
}

/// Where the bubble's tail is, and whether the bubble is below the robot.
pub fn bubble_tail(app: &AppHandle) -> (f64, bool) {
    let Some((_, screen)) = screen(app) else { return (BUBBLE_WIDTH - 44.0, false) };
    let robot = corner(app, &screen).robot(screen.area);
    let at = box_at(robot, screen.area, BUBBLE_WIDTH, *app.state::<Shared>().tall.lock().unwrap());
    (tail(robot, at), at.y > robot.y)
}

pub fn show_robot(app: &AppHandle) {
    place(app);
    if let Some(robot) = app.get_webview_window("robot") {
        let _ = robot.show();
        seen(&robot, true);
        place(app); // some window managers only take a place once the window is there
    }
}

/// Away while the Machine's app is in front or something is full screen. With its box open the person is here: it stays.
pub fn show_or_not(app: &AppHandle) {
    let Some(robot) = app.get_webview_window("robot") else { return };
    let shared = app.state::<Shared>();
    let wanted = !shared.picking.load(Ordering::Relaxed) && (box_open(app) || !shared.away.load(Ordering::Relaxed) && !shared.full.load(Ordering::Relaxed));
    if robot.is_visible().unwrap_or(true) != wanted {
        seen(&robot, wanted);
        if wanted {
            place(app);
        } else {
            crate::speak::hush(app, true);
        }
    }
}

/// Shows or hides the robot or its bubble, never taking the focus: Tauri's show() does, on Windows.
fn seen(window: &WebviewWindow, shown: bool) {
    #[cfg(windows)]
    if let Ok(hwnd) = window.hwnd() {
        use windows_sys::Win32::UI::WindowsAndMessaging::{ShowWindow, SW_HIDE, SW_SHOWNOACTIVATE};
        // SAFETY: the program's own window, on its own thread.
        unsafe { ShowWindow(hwnd.0, if shown { SW_SHOWNOACTIVATE } else { SW_HIDE }) };
    }
    #[cfg(not(windows))]
    let _ = if shown { window.show() } else { window.hide() };
}

pub fn box_open(app: &AppHandle) -> bool {
    app.state::<Shared>().open.load(Ordering::Relaxed)
}

pub fn open_box(app: &AppHandle) -> tauri::Result<()> {
    let shared = app.state::<Shared>();
    shared.open.store(true, Ordering::Relaxed);
    crate::looked(app);
    crate::speak::hush(app, false);
    show_or_not(app);
    shared.opened.fetch_add(1, Ordering::Relaxed);
    let window = match app.get_webview_window("box") {
        Some(w) => {
            let _ = w.emit("opened", ());
            w
        }
        None => build_box(app)?,
    };
    place(app);
    window.show()?;
    place(app);
    let _ = window.set_focus();
    let _ = app.emit_to("robot", "box", true);
    Ok(())
}

pub fn close_box(app: &AppHandle) {
    let shared = app.state::<Shared>();
    shared.notice.store(false, Ordering::Relaxed);
    if !shared.open.swap(false, Ordering::Relaxed) {
        return;
    }
    if !shared.picking.load(Ordering::Relaxed) {
        shared.added.lock().unwrap().clear();
        shared.waiting.lock().unwrap().added.clear();
    }
    crate::card::close(app);
    if let Some(window) = app.get_webview_window("box") {
        let _ = window.hide();
    }
    show_or_not(app);
    *shared.wanted.lock().unwrap() = None;
    crate::speak::closed(app);
    let _ = app.emit_to("robot", "box", false);
    #[cfg(not(windows))]
    {
        let (app, opened) = (app.clone(), shared.opened.load(Ordering::Relaxed));
        std::thread::spawn(move || {
            std::thread::sleep(KEEP);
            let gone = app.clone();
            let _ = app.run_on_main_thread(move || {
                let shared = gone.state::<Shared>();
                if !box_open(&gone) && !shared.draft.load(Ordering::Relaxed) && !shared.picking.load(Ordering::Relaxed) && shared.opened.load(Ordering::Relaxed) == opened {
                    if let Some(window) = gone.get_webview_window("box") {
                        let _ = window.destroy();
                    }
                }
            });
        });
    }
}

/// The box's page says how tall it is.
pub fn fit_box(app: &AppHandle, height: f64) {
    *app.state::<Shared>().height.lock().unwrap() = height.clamp(80.0, 700.0);
    place(app);
}

/// A monitor: its name, its work area and its scale.
#[derive(Debug)]
struct Screen {
    name: String,
    area: Rect,
    scale: f64,
}

impl Screen {
    /// Whether this point of the whole desktop, in physical pixels, is in its work area.
    fn has(&self, x: f64, y: f64) -> bool {
        let (x, y, a) = (x / self.scale, y / self.scale, self.area);
        x >= a.x && x < a.x + a.w && y >= a.y && y < a.y + a.h
    }

    /// The corner of a robot that is held there, at this point of itself.
    fn corner(&self, x: f64, y: f64, held: (f64, f64)) -> Corner {
        Corner::at(x / self.scale - held.0, y / self.scale - held.1, self.area)
    }
}

fn screens(app: &AppHandle) -> Vec<Screen> {
    #[cfg(target_os = "linux")]
    if app.state::<Shared>().layer {
        return linux::screens();
    }
    app.available_monitors().unwrap_or_default().into_iter().enumerate().map(|(i, m)| {
        let (work, scale) = (m.work_area(), m.scale_factor());
        Screen {
            name: m.name().cloned().unwrap_or_else(|| i.to_string()),
            area: Rect {
                x: work.position.x as f64 / scale,
                y: work.position.y as f64 / scale,
                w: work.size.width as f64 / scale,
                h: work.size.height as f64 / scale,
            },
            scale,
        }
    }).collect()
}

/// The saved monitor when it is there, else the main one. Its place in the list, for layer-shell.
fn screen(app: &AppHandle) -> Option<(usize, Screen)> {
    let wanted = app.state::<Shared>().saved.lock().unwrap().monitor.clone();
    let main = app.primary_monitor().ok().flatten().and_then(|m| m.name().cloned());
    let mut all: Vec<_> = screens(app).into_iter().enumerate().collect();
    let found = [wanted, main].into_iter().flatten().find_map(|name| all.iter().position(|(_, s)| s.name == name)).unwrap_or(0);
    (found < all.len()).then(|| all.swap_remove(found))
}

/// Windows tells about a new scale, but not about a new resolution, a moved taskbar or a monitor that comes or goes (a
/// remote session changes them as it connects): then the robot goes back to its corner.
#[cfg(windows)]
pub fn follow_screens(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let now = format!("{:?}", screens(app));
    let mut seen = shared.screens.lock().unwrap();
    if *seen != now && shared.grab.lock().unwrap().is_none() {
        *seen = now;
        drop(seen);
        place(app);
    }
}

/// How tall the box is with a to-do open in it.
pub fn tall(app: &AppHandle) -> f64 {
    screen(app).map_or(480.0, |(_, s)| place::tall(corner(app, &s).robot(s.area), s.area))
}

pub fn place(app: &AppHandle) {
    let Some((index, screen)) = screen(app) else { return };
    let shared = app.state::<Shared>();
    let mut robot = corner(app, &screen).robot(screen.area);
    if shared.hidden.load(Ordering::Relaxed) {
        robot = peek(robot, screen.area);
    }
    let around = box_at(robot, screen.area, BOX_WIDTH, *shared.height.lock().unwrap());
    let bubble = box_at(robot, screen.area, BUBBLE_WIDTH, *shared.tall.lock().unwrap());
    for (label, at) in [("robot", Some(robot)), ("box", Some(around)), ("card", crate::card::at(app, around)), ("bubble", Some(bubble))] {
        let Some(at) = at else { continue };
        let Some(window) = app.get_webview_window(label) else { continue };
        #[cfg(target_os = "linux")]
        if shared.layer {
            linux::put(&window, index, at, screen.area);
            continue;
        } else {
            linux::size(&window, at); // what Tauri's set_size leaves at 200 by 200 at least
        }
        let _ = index;
        let _ = window.set_position(PhysicalPosition::new((at.x * screen.scale).round(), (at.y * screen.scale).round()));
        // By its monitor's scale, not the window's: on the way to another monitor those differ
        let _ = window.set_size(PhysicalSize::new((at.w * screen.scale).round(), (at.h * screen.scale).round()));
    }
}

/// The robot, while it is dragged: where in its window it is held, and where it started.
pub struct Grab {
    held: (f64, f64),
    /// With layer-shell: the window itself only moves when it is dropped.
    #[cfg(target_os = "linux")]
    from: Corner,
    #[cfg(target_os = "linux")]
    to: Corner,
}

/// The robot is picked up at this point of its window.
pub fn grab(app: &AppHandle, x: f64, y: f64) {
    close_box(app);
    crate::speak::hush(app, false);
    #[cfg(target_os = "linux")]
    let Some((_, screen)) = screen(app) else { return };
    #[cfg(target_os = "linux")]
    let grab = Grab { held: (x, y), from: corner(app, &screen), to: corner(app, &screen) };
    #[cfg(not(target_os = "linux"))]
    let grab = Grab { held: (x, y) };
    *app.state::<Shared>().grab.lock().unwrap() = Some(grab);
    #[cfg(target_os = "linux")]
    if app.state::<Shared>().layer {
        carry(app, x, y);
    }
}

fn corner(app: &AppHandle, screen: &Screen) -> Corner {
    let saved = app.state::<Shared>().saved.lock().unwrap().places.get(&screen.name).copied().unwrap_or_default();
    saved.inside(screen.area.w, screen.area.h)
}

/// With layer-shell the window stays until the drop, since compositors don't agree on where the pointer is in a surface
/// that moves under it: a picture of the robot goes along instead. GTK says where the pointer is (linux::prepare), as
/// WebKit doesn't outside its own window.
#[cfg(target_os = "linux")]
fn carry(app: &AppHandle, x: f64, y: f64) {
    let Some((index, screen)) = screen(app) else { return };
    if let Some(grab) = app.state::<Shared>().grab.lock().unwrap().as_mut() {
        let to = Corner { right: grab.from.right - (x - grab.held.0), bottom: grab.from.bottom - (y - grab.held.1) };
        grab.to = to.inside(screen.area.w, screen.area.h);
        linux::carry(index, grab.to);
    }
}

/// Elsewhere the window follows the pointer, onto another monitor too.
pub fn drag(app: &AppHandle) {
    let shared = app.state::<Shared>();
    if shared.layer {
        return;
    }
    let Some(held) = shared.grab.lock().unwrap().as_ref().map(|g| g.held) else { return };
    let Ok(pointer) = app.cursor_position() else { return };
    let Some(screen) = screens(app).into_iter().find(|s| s.has(pointer.x, pointer.y)).or_else(|| screen(app).map(|s| s.1)) else { return };
    let at = screen.corner(pointer.x, pointer.y, held);
    put_down(app, screen.name, at);
}

pub fn dropped(app: &AppHandle) {
    let shared = app.state::<Shared>();
    let Some(_grab) = shared.grab.lock().unwrap().take() else { return };
    #[cfg(target_os = "linux")]
    if shared.layer {
        if let Some((_, screen)) = screen(app) {
            put_down(app, screen.name, _grab.to);
        }
        linux::put_away();
    }
}

fn put_down(app: &AppHandle, monitor: String, at: Corner) {
    {
        let shared = app.state::<Shared>();
        let mut saved = shared.saved.lock().unwrap();
        saved.places.insert(monitor.clone(), at);
        saved.monitor = Some(monitor);
    }
    place(app);
}

#[cfg(target_os = "linux")]
pub mod linux {
    use super::{Corner, Rect, Screen, ROBOT};
    use gtk::{cairo, gdk, prelude::*};
    use gtk_layer_shell::{Edge, KeyboardMode, Layer, LayerShell};
    use std::cell::RefCell;
    use tauri::{AppHandle, Manager, WebviewWindow};

    /// Layer-shell when this is Wayland and its compositor has it. GNOME has not: there main() picks XWayland.
    pub fn has_layer_shell() -> bool {
        gtk_layer_shell::is_supported()
    }

    pub fn prepare(app: &AppHandle, window: &WebviewWindow, label: &str) -> tauri::Result<()> {
        let robot = label == "robot";
        let gtk = window.gtk_window()?;
        if app.state::<crate::Shared>().layer {
            if gtk.is_realized() {
                gtk.unrealize();
            }
            gtk.init_layer_shell();
            gtk.set_namespace(&format!("the-machine-{label}"));
            gtk.set_layer(Layer::Top); // under full-screen windows
            gtk.set_exclusive_zone(0);
            for edge in [Edge::Right, Edge::Bottom] {
                gtk.set_anchor(edge, true);
            }
            gtk.set_keyboard_mode(if label == "box" || label == "card" { KeyboardMode::OnDemand } else { KeyboardMode::None });
        }
        if robot && app.state::<crate::Shared>().layer {
            let app = app.clone();
            window.with_webview(move |page| {
                page.inner().connect_event(move |_, e| {
                    if let (gdk::EventType::MotionNotify, Some((x, y))) = (e.event_type(), e.coords()) {
                        super::carry(&app, x, y);
                    }
                    gtk::glib::Propagation::Proceed
                });
            })?;
        }
        if label == "bubble" {
            // WebKit doesn't tell the page that the pointer left its window
            let app = app.clone();
            window.with_webview(move |page| {
                page.inner().connect_event(move |_, e| {
                    if let gdk::EventType::EnterNotify | gdk::EventType::LeaveNotify = e.event_type() {
                        let _ = tauri::Emitter::emit_to(&app, "bubble", "over", e.event_type() == gdk::EventType::EnterNotify);
                    }
                    gtk::glib::Propagation::Proceed
                });
            })?;
        }
        if label == "card" {
            // As tall as it is asked to be: a web view's own wish is its whole page, an overlay's is none
            window.with_webview(move |page| {
                let (page, over) = (page.inner(), gtk::Overlay::new());
                let Some(vbox) = page.parent().and_downcast::<gtk::Box>() else { return };
                vbox.remove(&page);
                over.add_overlay(&page);
                vbox.pack_start(&over, true, true, 0);
                over.show();
            })?;
        }
        if robot {
            // Only the robot itself takes clicks: an ellipse, the window's corners let them through
            gtk.connect_size_allocate(|gtk, a| {
                let region = cairo::Region::create();
                let (w, h) = (a.width() as f64, a.width() as f64); // a hidden one is cut off below
                for y in 0..a.height() {
                    let t = ((y as f64 + 0.5) - h / 2.0) / (h / 2.0);
                    let half = (w / 2.0 * (1.0 - t * t).max(0.0).sqrt()).ceil();
                    let row = cairo::RectangleInt::new((w / 2.0 - half) as i32, y, (2.0 * half) as i32, 1);
                    let _ = region.union_rectangle(&row);
                }
                gtk.input_shape_combine_region(Some(&region));
            });
        }
        Ok(())
    }

    fn name(index: usize, monitor: &gdk::Monitor) -> String {
        format!("{index} {}", monitor.model().unwrap_or_default())
    }

    pub(super) fn screens() -> Vec<Screen> {
        let Some(display) = gdk::Display::default() else { return vec![] };
        (0..display.n_monitors()).filter_map(|i| display.monitor(i)).enumerate().map(|(i, m)| {
            let g = m.workarea();
            let area = Rect { x: 0.0, y: 0.0, w: g.width() as f64, h: g.height() as f64 };
            Screen { name: name(i, &m), area, scale: 1.0 }
        }).collect()
    }

    pub fn put(window: &WebviewWindow, monitor: usize, at: Rect, area: Rect) {
        let Ok(gtk) = window.gtk_window() else { return };
        if let Some(m) = gdk::Display::default().and_then(|d| d.monitor(monitor as i32)) {
            if gtk.monitor().as_ref() != Some(&m) {
                gtk.set_monitor(&m);
            }
        }
        gtk.set_layer_shell_margin(Edge::Right, (area.w - at.x - at.w).round() as i32);
        gtk.set_layer_shell_margin(Edge::Bottom, (area.h - at.y - at.h).round() as i32);
        size(window, at);
    }

    pub fn size(window: &WebviewWindow, at: Rect) {
        let Ok(gtk) = window.gtk_window() else { return };
        gtk.set_size_request(at.w as i32, at.h as i32);
        gtk.resize(at.w as i32, at.h as i32);
    }

    thread_local! { static CARRIED: RefCell<Option<gtk::Window>> = const { RefCell::new(None) }; }

    /// The picture of the robot that follows the pointer in a drag, at this corner.
    pub fn carry(monitor: usize, at: Corner) {
        CARRIED.with_borrow_mut(|carried| {
            let window = carried.get_or_insert_with(|| picture(monitor));
            window.set_layer_shell_margin(Edge::Right, at.right.round() as i32);
            window.set_layer_shell_margin(Edge::Bottom, at.bottom.round() as i32);
            window.show_all();
        });
    }

    pub fn put_away() {
        if let Some(window) = CARRIED.take() {
            // A moment later, once the robot itself is there
            gtk::glib::timeout_add_local_once(std::time::Duration::from_millis(60), move || window.close());
        }
    }

    fn picture(monitor: usize) -> gtk::Window {
        let window = gtk::Window::new(gtk::WindowType::Toplevel);
        window.set_app_paintable(true);
        if let Some(visual) = GtkWindowExt::screen(&window).and_then(|s| s.rgba_visual()) {
            window.set_visual(Some(&visual));
        }
        window.init_layer_shell();
        window.set_namespace("the-machine-robot");
        window.set_layer(Layer::Overlay);
        window.set_exclusive_zone(0);
        window.set_anchor(Edge::Right, true);
        window.set_anchor(Edge::Bottom, true);
        if let Some(m) = gdk::Display::default().and_then(|d| d.monitor(monitor as i32)) {
            window.set_monitor(&m);
        }
        let scale = window.scale_factor().max(1);
        let stream = gtk::gio::MemoryInputStream::from_bytes(&gtk::glib::Bytes::from_static(include_bytes!("../ui/img/machine.png")));
        let px = 80 * scale; // as in style.css: the window less its padding
        let image = gdk::gdk_pixbuf::Pixbuf::from_stream_at_scale(&stream, px, px, true, gtk::gio::Cancellable::NONE)
            .ok()
            .and_then(|p| p.create_surface(scale, None::<&gdk::Window>));
        window.add(&gtk::Image::from_surface(image.as_ref()));
        window.set_size_request(ROBOT.0 as i32, ROBOT.1 as i32);
        window.connect_size_allocate(|w, _| w.input_shape_combine_region(Some(&cairo::Region::create())));
        window
    }
}

/// Windows says when something is full screen or presenting: the robot goes away.
#[cfg(windows)]
pub fn full_screen() -> bool {
    use windows_sys::Win32::UI::Shell::{
        SHQueryUserNotificationState, QUNS_BUSY, QUNS_PRESENTATION_MODE, QUNS_RUNNING_D3D_FULL_SCREEN,
    };
    let mut state = 0;
    // SAFETY: the one argument is a valid place for the answer.
    let told = unsafe { SHQueryUserNotificationState(&mut state) } == 0;
    told && matches!(state, QUNS_BUSY | QUNS_RUNNING_D3D_FULL_SCREEN | QUNS_PRESENTATION_MODE)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_drag_goes_to_the_monitor_under_the_pointer() {
        // The main one at 150%, one to its left at 100%, one to its right at 200%, as Windows lays them out
        let screen = |name: &str, x: f64, w: f64, h: f64, scale: f64| Screen {
            name: name.into(),
            area: Rect { x: x / scale, y: 0.0, w: w / scale, h: h / scale },
            scale,
        };
        let all = [screen("left", -1920.0, 1920.0, 1040.0, 1.0), screen("main", 0.0, 2560.0, 1400.0, 1.5), screen("right", 2560.0, 3840.0, 2080.0, 2.0)];
        for (x, y, name) in [(-960.0, 500.0, "left"), (-1.0, 0.0, "left"), (0.0, 0.0, "main"), (2559.0, 1399.0, "main"), (2560.0, 30.0, "right"), (6000.0, 2000.0, "right")] {
            let found: Vec<_> = all.iter().filter(|s| s.has(x, y)).collect();
            assert_eq!(found.iter().map(|s| s.name.as_str()).collect::<Vec<_>>(), [name], "{x},{y}");
            // Held at its middle, it stands around the pointer, kept inside that monitor
            let s = found[0];
            let r = s.corner(x, y, (44.0, 44.0)).robot(s.area);
            let wanted = |at: f64, from: f64, size: f64| (at / s.scale - 44.0).clamp(from, from + size - 88.0);
            assert!((r.x - wanted(x, s.area.x, s.area.w)).abs() < 0.01 && (r.y - wanted(y, s.area.y, s.area.h)).abs() < 0.01, "{x},{y} {r:?}");
        }
        assert!(!all.iter().any(|s| s.has(100.0, 1401.0))); // on the taskbar: it stays on the monitor it is on
    }
}
