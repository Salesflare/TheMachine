//! Starting at login: off until the person turns it on in Settings, and the system's own list of it says whether it is. Such a
//! start opens no window.
use serde::Serialize;

#[derive(Clone, Copy, Debug, PartialEq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum State {
    Off,
    On,
    /// The person turned it off in the system's own list, where only they turn it on again.
    #[cfg_attr(not(any(windows, target_os = "macos")), allow(dead_code))]
    Asks,
}

#[cfg_attr(target_os = "macos", allow(dead_code))]
const ARGUMENT: &str = "--login";

pub fn state() -> State {
    system::state()
}

pub fn set(on: bool) -> bool {
    system::set(on)
}

/// This start is the one at login.
pub fn started() -> bool {
    std::env::args().nth(1).as_deref() == Some(ARGUMENT) || system::started()
}

#[cfg(target_os = "macos")]
mod system {
    pub use crate::mac_app::{at_login as started, login_state as state, set_login as set};
}

/// The person's own list of what starts (Settings, Apps, Startup shows it).
#[cfg(windows)]
mod system {
    use super::{State, ARGUMENT};
    const LIST: &str = "Software\\Microsoft\\Windows\\CurrentVersion\\Run";
    const NAME: &str = "The Machine";
    /// Where Settings and Task Manager keep what the person turned off there: an odd first byte.
    const KEPT: &str = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StartupApproved\\Run";

    pub fn state() -> State {
        if windows_registry::CURRENT_USER.open(LIST).and_then(|list| list.get_string(NAME)).is_err() {
            return State::Off;
        }
        let kept = windows_registry::CURRENT_USER.open(KEPT).and_then(|kept| kept.get_value(NAME));
        let off = kept.is_ok_and(|said| said.first().is_some_and(|b| b % 2 == 1));
        if off { State::Asks } else { State::On }
    }

    pub fn set(on: bool) -> bool {
        let Ok(list) = windows_registry::CURRENT_USER.create(LIST) else { return false };
        if !on {
            return list.remove_value(NAME).is_ok() || state() == State::Off;
        }
        let Ok(program) = std::env::current_exe() else { return false };
        list.set_string(NAME, format!("\"{}\" {ARGUMENT}", program.display())).is_ok() && state() == State::On
    }

    pub fn started() -> bool {
        false
    }
}

/// The desktop's own folder of what starts.
#[cfg(target_os = "linux")]
mod system {
    use super::{State, ARGUMENT};
    use std::path::PathBuf;

    fn file() -> PathBuf {
        gtk::glib::user_config_dir().join("autostart").join("computer.themachine.desktop.desktop")
    }

    pub fn state() -> State {
        if file().exists() { State::On } else { State::Off }
    }

    pub fn set(on: bool) -> bool {
        let file = file();
        if !on {
            return std::fs::remove_file(&file).is_ok() || !file.exists();
        }
        // An AppImage runs from a folder that is gone after it quits: the file itself starts it again
        let program = std::env::var_os("APPIMAGE").map(PathBuf::from).filter(|p| p.is_absolute()).or_else(|| std::env::current_exe().ok());
        let Some(program) = program.and_then(|p| p.into_os_string().into_string().ok()) else { return false };
        // Quoted as the desktop's own rules ask
        let program: String = program.chars().flat_map(|c| if "\"`$\\".contains(c) { vec!['\\', '\\', c] } else if c == '%' { vec!['%', '%'] } else { vec![c] }).collect();
        let entry = format!("[Desktop Entry]\nType=Application\nName=The Machine\nExec=\"{program}\" {ARGUMENT}\nNoDisplay=true\n");
        file.parent().is_some_and(|f| std::fs::create_dir_all(f).is_ok()) && std::fs::write(&file, entry).is_ok()
    }

    pub fn started() -> bool {
        false
    }
}

#[cfg(not(any(windows, target_os = "linux", target_os = "macos")))]
mod system {
    use super::State;

    pub fn state() -> State {
        State::Off
    }

    pub fn set(_: bool) -> bool {
        false
    }

    pub fn started() -> bool {
        false
    }
}
