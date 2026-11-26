//! Only one of it, in the Mac App Store's build. The single-instance plugin's socket is in /tmp, where the App Sandbox
//! writes nothing, so each start would run on its own. This one is in the app's own container: every start of this app is
//! given the same one, whoever starts it (Finder, the Dock, the program itself), and nothing else can reach it.
//! A second start hands over its arguments as the plugin's does, and ends.
use std::io::{Read, Write};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::PathBuf;
use std::time::Duration;
use tauri::plugin::{Builder, TauriPlugin};
use tauri::{AppHandle, RunEvent, Runtime};

/// What a second start says can't be longer than this, as a page's or the system's arguments are short.
const MOST: u64 = 64 << 10;

/// The socket, in the container's own Data folder, which the App Sandbox gives as the home folder (also to a start from a
/// shell, whose HOME is the person's). A path of a socket has at most 104 bytes: with a long user name it is a short
/// one, relative to that folder.
fn socket() -> Option<PathBuf> {
    let home = PathBuf::from(objc2_foundation::NSHomeDirectory().to_string());
    home.join("Library").is_dir().then(|| home.join(".one"))
}

fn short(socket: &PathBuf) -> PathBuf {
    if socket.as_os_str().len() < 100 {
        return socket.clone();
    }
    let _ = std::env::set_current_dir(socket.parent().unwrap_or(socket));
    PathBuf::from(".one")
}

pub fn init<R: Runtime>(again: impl Fn(&AppHandle<R>, Vec<String>) + Send + Sync + 'static) -> TauriPlugin<R> {
    Builder::new("one")
        .setup(move |app, _| {
            let Some(socket) = socket() else { return Ok(()) };
            let socket = short(&socket);
            // Starts at the same time take turns here, so that one of them is it
            let turn = std::fs::OpenOptions::new().create(true).truncate(false).write(true).open(socket.with_extension("lock"))?;
            turn.lock()?;
            if let Ok(mut there) = UnixStream::connect(&socket) {
                let said = std::env::args().collect::<Vec<_>>().join("\0");
                let _ = there.set_write_timeout(Some(Duration::from_secs(5)));
                if there.write_all(said.as_bytes()).is_ok() {
                    std::process::exit(0);
                }
            }
            // None answers there: what is left of one that ended goes
            let _ = std::fs::remove_file(&socket);
            let listener = UnixListener::bind(&socket)?;
            drop(turn);
            let app = app.clone();
            let again = std::sync::Arc::new(again);
            std::thread::spawn(move || {
                for stream in listener.incoming().flatten() {
                    let mut said = String::new();
                    let _ = stream.set_read_timeout(Some(Duration::from_secs(5)));
                    if stream.take(MOST).read_to_string(&mut said).is_ok() {
                        again(&app, said.split('\0').map(String::from).collect());
                    }
                }
            });
            Ok(())
        })
        .on_event(|_, event| {
            if let RunEvent::Exit = event {
                if let Some(socket) = socket() {
                    let _ = std::fs::remove_file(short(&socket));
                }
            }
        })
        .build()
}

#[cfg(test)]
mod tests {
    #[test]
    fn a_long_home_gets_a_short_path() {
        let long = std::path::PathBuf::from(format!("/Users/{}/Library/Containers/computer.themachine.desktop/Data/.one", "a".repeat(60)));
        let here = std::env::current_dir().unwrap();
        assert_eq!(super::short(&long), std::path::PathBuf::from(".one"));
        std::env::set_current_dir(here).unwrap();
        let fine = std::path::PathBuf::from("/Users/a/Library/Containers/computer.themachine.desktop/Data/.one");
        assert_eq!(super::short(&fine), fine);
    }
}
