//! "Run as administrator", which nothing here needs. Windows keeps such a program apart from the person's others: the browser
//! can't hand it their sign-in, files can't be dropped on it, and a plain start would be a second robot. So it starts again
//! as the person themselves, by their own desktop, which has nothing to ask for that.
use std::time::Duration;

/// Whether it did, and this one ends.
pub fn leaves() -> bool {
    let plain = std::env::args().count() == 1;
    if !plain || !(full() || cfg!(feature = "sandbox") && std::env::var_os("MACHINE_SANDBOX_ELEVATED").is_some()) {
        return false;
    }
    // The one that comes of it is elevated too, or is never there: then this one does
    let mark = std::env::temp_dir().join("the-machine-desktop-elevated");
    let just = mark.metadata().and_then(|m| m.modified()).is_ok_and(|at| at.elapsed().is_ok_and(|since| since < Duration::from_secs(15)));
    if just || std::fs::write(&mark, "").is_err() {
        let _ = std::fs::remove_file(&mark);
        return false;
    }
    let Some(folder) = std::env::var_os("SystemRoot") else { return false };
    std::env::current_exe().is_ok_and(|program| std::process::Command::new(std::path::Path::new(&folder).join("explorer.exe")).arg(program).spawn().is_ok())
}

/// One runs that this one can't share with, as it is an administrator's: what this one was started for goes to it, and
/// nothing here is touched. Else there would be two, with one page cache that only one of them can open and one sign-in.
pub fn hands_over() -> bool {
    use windows_sys::Win32::Foundation::{CloseHandle, GetLastError, ERROR_ACCESS_DENIED};
    use windows_sys::Win32::System::DataExchange::COPYDATASTRUCT;
    use windows_sys::Win32::System::Threading::{OpenMutexW, SYNCHRONIZATION_SYNCHRONIZE};
    use windows_sys::Win32::UI::WindowsAndMessaging::{AllowSetForegroundWindow, GetWindowThreadProcessId, SendMessageTimeoutW, SMTO_NORMAL, WM_COPYDATA};
    // SAFETY: the name ends with a 0; the handle is this one's; what is sent outlives the call, which waits.
    unsafe {
        let mutex = OpenMutexW(SYNCHRONIZATION_SYNCHRONIZE, 0, wide("computer.themachine.desktop-sim").as_ptr());
        if !mutex.is_null() {
            CloseHandle(mutex);
            return false; // the single-instance plugin does it
        }
        if GetLastError() != ERROR_ACCESS_DENIED {
            return false;
        }
        for _ in 0..40 {
            let window = its_window();
            if !window.is_null() {
                let mut pid = 0;
                GetWindowThreadProcessId(window, &mut pid);
                AllowSetForegroundWindow(pid);
                let mut what = String::new(); // as the plugin has it: where it was started, and its arguments
                for argument in std::env::args_os() {
                    what += "\0";
                    what += &argument.to_string_lossy();
                }
                let sent = COPYDATASTRUCT { dwData: 1543, cbData: what.len() as u32, lpData: what.as_ptr().cast_mut().cast() };
                SendMessageTimeoutW(window, WM_COPYDATA, 0, &raw const sent as isize, SMTO_NORMAL, 10_000, std::ptr::null_mut());
                break;
            }
            std::thread::sleep(Duration::from_millis(25));
        }
    }
    true
}

/// That a start that isn't an administrator's is heard: only this one message, and what it says is taken as any start's.
pub fn hears() {
    use windows_sys::Win32::UI::WindowsAndMessaging::{ChangeWindowMessageFilterEx, MSGFLT_ALLOW, WM_COPYDATA};
    // SAFETY: the program's own window.
    unsafe { ChangeWindowMessageFilterEx(its_window(), WM_COPYDATA, MSGFLT_ALLOW, std::ptr::null_mut()) };
}

/// The single-instance plugin's own.
fn its_window() -> windows_sys::Win32::Foundation::HWND {
    let (class, name) = (wide("computer.themachine.desktop-sic"), wide("computer.themachine.desktop-siw"));
    // SAFETY: both end with a 0.
    unsafe { windows_sys::Win32::UI::WindowsAndMessaging::FindWindowW(class.as_ptr(), name.as_ptr()) }
}

fn wide(text: &str) -> Vec<u16> {
    text.encode_utf16().chain([0]).collect()
}

/// The person's own full token, next to the plain one the rest of theirs has. Not so where there is only one: an account that
/// is the administrator itself, or Windows without its User Account Control.
fn full() -> bool {
    use windows_sys::Win32::Foundation::CloseHandle;
    use windows_sys::Win32::Security::{GetTokenInformation, TokenElevationType, TokenElevationTypeFull, TOKEN_QUERY};
    use windows_sys::Win32::System::Threading::{GetCurrentProcess, OpenProcessToken};
    let (mut token, mut kind, mut size) = (std::ptr::null_mut(), 0i32, 0u32);
    // SAFETY: the program's own token, closed again; the places are valid and as large as said.
    unsafe {
        if OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &mut token) == 0 {
            return false;
        }
        let told = GetTokenInformation(token, TokenElevationType, (&raw mut kind).cast(), 4, &mut size);
        CloseHandle(token);
        told != 0 && kind == TokenElevationTypeFull
    }
}
