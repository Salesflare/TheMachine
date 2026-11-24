//! The keys of the dashboard's window on Windows and Linux, as a menu has them on a Mac (mac.rs).
use crate::{dash, settings};
use tauri::{AppHandle, Manager};

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Does {
    Close,
    Full,
    Reload,
    Save,
    Settings,
    Zoom(i8),
    /// The rest is WebView2's own on Windows.
    #[cfg(target_os = "linux")]
    Find(i8),
    #[cfg(target_os = "linux")]
    Back(bool),
    #[cfg(target_os = "linux")]
    Print,
    #[cfg(target_os = "linux")]
    Quit,
}

#[derive(Clone, Copy, Default)]
pub struct Held {
    pub ctrl: bool,
    pub shift: bool,
    pub alt: bool,
}

/// `key`: what it types ("w", "+"), or its name ("F11").
pub fn does(label: &str, key: &str, held: Held) -> Option<Does> {
    let dash = label == dash::LABEL;
    let any = dash::label(label);
    #[cfg(target_os = "linux")]
    if dash && held.alt && !held.ctrl && !held.shift {
        return match key {
            "Left" => Some(Does::Back(false)),
            "Right" => Some(Does::Back(true)),
            _ => None,
        };
    }
    if held.alt {
        return None; // AltGr is Ctrl and Alt
    }
    match (key, held.ctrl) {
        ("F11", false) if any => Some(Does::Full),
        ("F5", false) if dash => Some(Does::Reload),
        ("+" | "=", true) if dash => Some(Does::Zoom(1)), // also with Shift, as + is typed
        ("-" | "_", true) if dash => Some(Does::Zoom(-1)),
        #[cfg(target_os = "linux")]
        ("F3", false) | ("g" | "G", true) if dash => Some(Does::Find(if held.shift { -1 } else { 1 })),
        _ if held.shift => None,
        ("0", true) if dash => Some(Does::Zoom(0)),
        ("r", true) if dash => Some(Does::Reload),
        ("s", true) if any && !dash => Some(Does::Save),
        ("w", true) => Some(Does::Close),
        (",", true) if any => Some(Does::Settings),
        #[cfg(target_os = "linux")]
        ("f", true) if dash => Some(Does::Find(0)),
        #[cfg(target_os = "linux")]
        ("p", true) if any => Some(Does::Print),
        #[cfg(target_os = "linux")]
        ("q", true) if any => Some(Does::Quit),
        _ => None,
    }
}

pub fn run(app: &AppHandle, label: &str, what: Does) {
    let Some(window) = app.get_webview_window(label) else { return };
    match what {
        Does::Close => { let _ = window.close(); }
        Does::Full => { let _ = window.set_fullscreen(!window.is_fullscreen().unwrap_or(false)); }
        Does::Reload => dash::reload(app),
        Does::Save => dash::save_copy(app),
        Does::Settings => settings::open(app),
        Does::Zoom(step) => dash::zoom(app, step),
        #[cfg(target_os = "linux")]
        Does::Find(step) => crate::linux_app::find(step),
        #[cfg(target_os = "linux")]
        Does::Back(forward) => dash::back(app, forward),
        #[cfg(target_os = "linux")]
        Does::Print => { let _ = window.print(); }
        #[cfg(target_os = "linux")]
        Does::Quit => crate::quit::quit(app),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn its_keys() {
        let ctrl = Held { ctrl: true, ..Held::default() };
        let shift = Held { shift: true, ..ctrl };
        let one = |label: &str, key: &str| does(label, key, ctrl);
        assert_eq!([one("app", "w"), one("app", ","), one("app", "0"), one("app", "r")], [Some(Does::Close), Some(Does::Settings), Some(Does::Zoom(0)), Some(Does::Reload)]);
        assert_eq!([does("app", "+", shift), one("app", "="), one("app", "-"), does("app", "r", shift), one("app", "s")], [Some(Does::Zoom(1)), Some(Does::Zoom(1)), Some(Does::Zoom(-1)), None, None]);
        assert_eq!([one("file-1", "s"), one("file-1", "+"), one("settings", "w"), one("settings", "s")], [Some(Does::Save), None, Some(Does::Close), None]);
        assert_eq!(does("app", "F11", Held::default()), Some(Does::Full));
        assert_eq!([does("app", "w", Held { alt: true, ..ctrl }), does("app", "w", Held::default()), does("settings", "F11", Held::default())], [None; 3]);
        #[cfg(target_os = "linux")]
        assert_eq!([one("app", "f"), one("file-1", "f"), one("app", "q"), does("app", "Left", Held { alt: true, ..Held::default() })],
            [Some(Does::Find(0)), None, Some(Does::Quit), Some(Does::Back(false))]);
    }
}
