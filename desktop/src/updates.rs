//! A newer version: looked for once a day, fetched, and put in place when the person says so. What isn't signed with the key
//! in tauri.conf.json is never used. The look asks the one address there, and says nothing of this computer or who uses it.
//! Only where the app can replace itself: an app of its own on a Mac, or as its installer put it on Windows. Elsewhere, what
//! installed it updates it.
use tauri::AppHandle;

#[tauri::command]
pub async fn update_apply(app: AppHandle) -> Result<(), String> {
    #[cfg(any(windows, target_os = "macos"))]
    return crate::away(move || there::apply(&app)).await;
    #[cfg(not(any(windows, target_os = "macos")))]
    {
        let _ = app;
        Err("failed".into())
    }
}

/// The version that is there to be put in place.
pub fn ready() -> Option<String> {
    #[cfg(any(windows, target_os = "macos"))]
    return there::READY.lock().unwrap().as_ref().map(|(update, _)| update.version.clone());
    #[cfg(not(any(windows, target_os = "macos")))]
    None
}

pub fn watch(_app: &AppHandle) {
    #[cfg(any(windows, target_os = "macos"))]
    if there::replaces() {
        let app = _app.clone();
        std::thread::spawn(move || there::watch(&app));
    }
}

#[cfg(any(windows, target_os = "macos"))]
mod there {
    use std::path::Path;
    use std::sync::Mutex;
    use std::time::Duration;
    use tauri::{AppHandle, Emitter, Manager};
    use tauri_plugin_updater::{Update, UpdaterBuilder, UpdaterExt};

    const FIRST: Duration = Duration::from_secs(60);
    const DAY: Duration = Duration::from_secs(24 * 60 * 60);

    pub static READY: Mutex<Option<(Update, Vec<u8>)>> = Mutex::new(None);

    pub fn replaces() -> bool {
        std::env::current_exe().is_ok_and(|own| replaces_at(&own))
    }

    /// Windows: next to what uninstalls it. Mac: in an app, and not where macOS runs a download from.
    fn replaces_at(own: &Path) -> bool {
        if cfg!(windows) {
            return own.with_file_name("uninstall.exe").exists();
        }
        own.ends_with("Contents/MacOS/the-machine-desktop") && !own.to_string_lossy().contains("/AppTranslocation/")
    }

    pub fn watch(app: &AppHandle) {
        std::thread::sleep(if cfg!(feature = "sandbox") { Duration::from_secs(3) } else { FIRST });
        loop {
            match tauri::async_runtime::block_on(look(app)) {
                Ok(Some(new)) => {
                    *READY.lock().unwrap() = Some(new);
                    let _ = app.emit_to("settings", "settings", ());
                    crate::later(app, crate::follow_tray);
                }
                Ok(None) => {}
                Err(_error) => {
                    #[cfg(feature = "sandbox")]
                    eprintln!("updates: {_error}");
                }
            }
            std::thread::sleep(DAY);
        }
    }

    /// Fetched and its signature checked, if it is newer than what is here.
    async fn look(app: &AppHandle) -> tauri_plugin_updater::Result<Option<(Update, Vec<u8>)>> {
        let had = super::ready();
        let found = source(app.updater_builder())?.timeout(Duration::from_secs(15 * 60)).build()?.check().await?;
        let Some(update) = found.filter(|u| Some(&u.version) != had.as_ref()) else { return Ok(None) };
        let bytes = update.download(|_, _| {}, || {}).await?;
        Ok(Some((update, bytes)))
    }

    #[cfg(not(feature = "sandbox"))]
    fn source(of: UpdaterBuilder) -> tauri_plugin_updater::Result<UpdaterBuilder> {
        Ok(of)
    }

    /// A stand-in's, with a key of its own.
    #[cfg(feature = "sandbox")]
    fn source(of: UpdaterBuilder) -> tauri_plugin_updater::Result<UpdaterBuilder> {
        let told = |name: &str| std::env::var(name).unwrap_or_default();
        let Ok(from) = told("MACHINE_SANDBOX_UPDATES").parse() else { return Ok(of) };
        of.pubkey(told("MACHINE_SANDBOX_UPDATES_KEY")).endpoints(vec![from])
    }

    /// Windows: its installer takes over, and starts it again. Not on the main thread.
    pub fn apply(app: &AppHandle) -> Result<(), String> {
        let Some((update, bytes)) = READY.lock().unwrap().take() else { return Err("failed".into()) };
        crate::notify::quits();
        app.state::<crate::Shared>().save();
        if let Err(error) = update.install(&bytes) {
            eprintln!("could not update: {error}");
            *READY.lock().unwrap() = Some((update, bytes));
            return Err("failed".into());
        }
        app.request_restart();
        Ok(())
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn only_where_it_can_replace_itself() {
            if cfg!(target_os = "macos") {
                assert!(replaces_at(Path::new("/Applications/The Machine.app/Contents/MacOS/the-machine-desktop")));
                assert!(!replaces_at(Path::new("/private/var/folders/x/AppTranslocation/y/d/The Machine.app/Contents/MacOS/the-machine-desktop")));
            }
            assert!(!replaces_at(Path::new("/somewhere/target/release/the-machine-desktop")));
        }

        #[test]
        fn its_key_and_where_it_looks() {
            use base64::Engine;
            let all: serde_json::Value = serde_json::from_str(include_str!("../tauri.conf.json")).unwrap();
            let its = &all["plugins"]["updater"];
            let key = base64::engine::general_purpose::STANDARD.decode(its["pubkey"].as_str().unwrap()).unwrap();
            assert!(String::from_utf8(key).unwrap().starts_with("untrusted comment: "));
            assert!(its["endpoints"][0].as_str().is_some_and(|e| e.starts_with("https://") && !e.contains("{{")), "it tells nothing");
        }
    }
}
