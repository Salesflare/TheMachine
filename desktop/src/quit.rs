//! Quitting, also when the main thread is stuck and no click or window message reaches it any more.
use crate::{no_links, Shared};
use std::time::Duration;
use tauri::{AppHandle, Manager};

/// How long the event loop gets to end by itself.
const LET: Duration = Duration::from_secs(2);

pub fn quit(app: &AppHandle) {
    let here = app.clone();
    std::thread::spawn(move || {
        std::thread::sleep(LET);
        if here.state::<Shared>().pending.try_lock().map_or(true, |p| p.is_some()) {
            no_links(&here);
        }
        gone()
    });
    app.exit(0);
}

#[cfg(not(windows))]
fn gone() {
    std::process::exit(0)
}

/// Windows' own exit waits for what other threads hold. This doesn't.
#[cfg(windows)]
fn gone() {
    use windows_sys::Win32::System::Threading::{GetCurrentProcess, TerminateProcess};
    // SAFETY: it ends this process.
    unsafe { TerminateProcess(GetCurrentProcess(), 0) };
}

/// Windows passes a second start on to the main thread's message loop. --quit doesn't go that way: a named event, which
/// a thread of its own waits for. (On Linux a second start arrives on its own thread anyway.)
#[cfg(windows)]
pub mod event {
    use std::time::Duration;
    use tauri::AppHandle;
    use windows_sys::Win32::Foundation::{CloseHandle, WAIT_OBJECT_0};
    use windows_sys::Win32::System::Threading::{CreateEventW, OpenEventW, SetEvent, WaitForSingleObject, EVENT_MODIFY_STATE, INFINITE};

    fn name() -> Vec<u16> {
        "Local\\computer.themachine.desktop-quit\0".encode_utf16().collect()
    }

    pub fn wait(app: &AppHandle) {
        let app = app.clone();
        std::thread::spawn(move || {
            // SAFETY: the name ends with a 0, and the handle is this thread's for as long as the process runs.
            let asked = unsafe {
                let event = CreateEventW(std::ptr::null(), 0, 0, name().as_ptr());
                !event.is_null() && WaitForSingleObject(event, INFINITE) == WAIT_OBJECT_0
            };
            if asked {
                super::quit(&app);
            }
        });
    }

    /// Asks the one that runs to quit and waits until it has. False: none runs.
    pub fn ask() -> bool {
        let mut asked = false;
        for _ in 0..80 {
            // SAFETY: the name ends with a 0, and the handle is closed here.
            unsafe {
                let event = OpenEventW(EVENT_MODIFY_STATE, 0, name().as_ptr());
                if event.is_null() {
                    break;
                }
                if !asked {
                    SetEvent(event);
                }
                CloseHandle(event);
            }
            asked = true;
            std::thread::sleep(Duration::from_millis(100));
        }
        asked
    }
}
