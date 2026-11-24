//! Whether someone touched the mouse or the keys since a bubble showed: it waits for that before it goes (speak.rs). Asked of
//! the system without a permission, and only how long ago it was, never what. Where that isn't told, a bubble goes as if.
use std::time::{Duration, Instant};

/// How long one who is there may hold still and still be there.
#[cfg_attr(not(target_os = "linux"), allow(dead_code))]
const STILL: Duration = Duration::from_millis(1500);

pub struct Watch {
    since: Instant,
    #[cfg(target_os = "linux")]
    asks: linux::Asks,
}

impl Watch {
    /// Not on the main thread.
    pub fn new() -> Watch {
        Watch {
            since: Instant::now(),
            #[cfg(target_os = "linux")]
            asks: linux::Asks::new(),
        }
    }

    pub fn touched(&mut self) -> bool {
        #[cfg(target_os = "linux")]
        return self.asks.touched(self.since);
        #[cfg(not(target_os = "linux"))]
        idle().is_none_or(|idle| touched(idle, self.since.elapsed()))
    }
}

/// Nothing was touched for this long, of the time that is looked at.
fn touched(idle: Duration, looked: Duration) -> bool {
    idle < looked
}

/// How long nothing was touched.
#[cfg(windows)]
pub fn idle() -> Option<Duration> {
    use windows_sys::Win32::System::SystemInformation::GetTickCount;
    use windows_sys::Win32::UI::Input::KeyboardAndMouse::{GetLastInputInfo, LASTINPUTINFO};
    let mut last = LASTINPUTINFO { cbSize: std::mem::size_of::<LASTINPUTINFO>() as u32, dwTime: 0 };
    // SAFETY: the one argument is a valid place for the answer.
    (unsafe { GetLastInputInfo(&mut last) } != 0).then(|| Duration::from_millis(unsafe { GetTickCount() }.wrapping_sub(last.dwTime).into()))
}

#[cfg(target_os = "macos")]
pub fn idle() -> Option<Duration> {
    #[link(name = "CoreGraphics", kind = "framework")]
    extern "C" {
        fn CGEventSourceSecondsSinceLastEventType(source: i32, event: u32) -> f64;
    }
    // SAFETY: a plain call: any event of the session.
    Duration::try_from_secs_f64(unsafe { CGEventSourceSecondsSinceLastEventType(0, u32::MAX) }).ok()
}

#[cfg(not(any(windows, target_os = "linux", target_os = "macos")))]
pub fn idle() -> Option<Duration> {
    None
}

#[cfg(target_os = "linux")]
mod linux {
    use super::STILL;
    use std::time::{Duration, Instant};
    use wayland_client::globals::{registry_queue_init, GlobalListContents};
    use wayland_client::protocol::{wl_registry, wl_seat};
    use wayland_client::{Connection, Dispatch, EventQueue, QueueHandle};
    use wayland_protocols::ext::idle_notify::v1::client::{ext_idle_notification_v1 as notification, ext_idle_notifier_v1 as notifier};
    use x11rb::protocol::screensaver::ConnectionExt as _;

    /// As long as this without anything touched is told (Wayland).
    const IDLE: u32 = 500;
    const LONG: Duration = Duration::from_secs(2);

    pub enum Asks {
        Wayland(Box<(EventQueue<Told>, Told)>),
        /// GNOME's.
        Mutter(zbus::blocking::Connection),
        X11(Box<x11rb::rust_connection::RustConnection>, u32),
        Nobody,
    }

    impl Asks {
        pub fn new() -> Asks {
            if std::env::var_os("WAYLAND_DISPLAY").is_some() {
                return wayland().map(|w| Asks::Wayland(Box::new(w))).or_else(|| mutter().map(Asks::Mutter)).unwrap_or(Asks::Nobody);
            }
            mutter().map(Asks::Mutter).or_else(|| x11().map(|(x, root)| Asks::X11(Box::new(x), root))).unwrap_or(Asks::Nobody)
        }

        pub fn touched(&mut self, since: Instant) -> bool {
            let idle = match self {
                Asks::Wayland(of) => {
                    let (queue, told) = &mut **of;
                    // Never still since: someone is there
                    return queue.roundtrip(told).is_err() || told.touched || !told.idled && since.elapsed() > STILL;
                }
                Asks::Mutter(bus) => asked(bus),
                Asks::X11(x, root) => x.screensaver_query_info(*root).ok().and_then(|a| a.reply().ok()).map(|i| Duration::from_millis(i.ms_since_user_input.into())),
                Asks::Nobody => None,
            };
            idle.is_none_or(|idle| super::touched(idle, since.elapsed()))
        }
    }

    fn asked(bus: &zbus::blocking::Connection) -> Option<Duration> {
        let monitor = zbus::blocking::Proxy::new(bus, "org.gnome.Mutter.IdleMonitor", "/org/gnome/Mutter/IdleMonitor/Core", "org.gnome.Mutter.IdleMonitor").ok()?;
        monitor.call::<_, _, u64>("GetIdletime", &()).ok().map(Duration::from_millis)
    }

    fn mutter() -> Option<zbus::blocking::Connection> {
        let bus = zbus::blocking::connection::Builder::session().ok()?.method_timeout(LONG).build().ok()?;
        let there = zbus::blocking::fdo::DBusProxy::new(&bus).ok()?.name_has_owner("org.gnome.Mutter.IdleMonitor".try_into().ok()?).ok()?;
        (there && asked(&bus).is_some()).then_some(bus)
    }

    fn x11() -> Option<(x11rb::rust_connection::RustConnection, u32)> {
        use x11rb::connection::Connection;
        let (x, screen) = x11rb::connect(None).ok()?;
        let root = x.setup().roots.get(screen)?.root;
        x.screensaver_query_info(root).ok()?.reply().ok()?; // not every X server tells
        Some((x, root))
    }

    /// ext-idle-notify-v1: KDE, Hyprland, Sway and others.
    #[derive(Default)]
    pub struct Told {
        idled: bool,
        touched: bool,
    }

    fn wayland() -> Option<(EventQueue<Told>, Told)> {
        let connection = Connection::connect_to_env().ok()?;
        let (globals, mut queue) = registry_queue_init::<Told>(&connection).ok()?;
        let to = queue.handle();
        let seat: wl_seat::WlSeat = globals.bind(&to, 1..=1, ()).ok()?;
        let asks: notifier::ExtIdleNotifierV1 = globals.bind(&to, 1..=2, ()).ok()?;
        if wayland_client::Proxy::version(&asks) >= 2 {
            asks.get_input_idle_notification(IDLE, &seat, &to, ()); // also while a video keeps the screen on
        } else {
            asks.get_idle_notification(IDLE, &seat, &to, ());
        }
        let mut told = Told::default();
        queue.roundtrip(&mut told).ok()?;
        Some((queue, told))
    }

    impl Dispatch<notification::ExtIdleNotificationV1, ()> for Told {
        fn event(told: &mut Told, _: &notification::ExtIdleNotificationV1, event: notification::Event, _: &(), _: &Connection, _: &QueueHandle<Told>) {
            match event {
                notification::Event::Idled => told.idled = true,
                notification::Event::Resumed => told.touched = true,
                _ => {}
            }
        }
    }

    impl Dispatch<wl_registry::WlRegistry, GlobalListContents> for Told {
        fn event(_: &mut Told, _: &wl_registry::WlRegistry, _: wl_registry::Event, _: &GlobalListContents, _: &Connection, _: &QueueHandle<Told>) {}
    }

    wayland_client::delegate_noop!(Told: ignore wl_seat::WlSeat);
    wayland_client::delegate_noop!(Told: notifier::ExtIdleNotifierV1);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn what_was_touched_before_it_showed_is_not_for_it() {
        let seconds = Duration::from_secs;
        assert!(!touched(seconds(40), seconds(3)), "nobody was there");
        assert!(touched(seconds(1), seconds(3)), "someone came");
        assert!(!touched(seconds(3), seconds(3)));
    }
}
