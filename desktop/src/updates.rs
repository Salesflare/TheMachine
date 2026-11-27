//! A newer version: looked for once a day, fetched, and put in place when the person says so. What isn't signed with the key
//! in tauri.conf.json is never used. The look asks the one address there, and says nothing of this computer or who uses it.
//! Only where the app can replace itself: an app of its own on a Mac, as its installer put it on Windows, and an AppImage in
//! a folder of the person's own on Linux. A .deb or Arch package is its package manager's: there Settings only says that a
//! newer one is out, and where. Elsewhere, what installed it updates it, as the Mac App Store does its own build, which has
//! none of this (Cargo.toml, `updates`).
use tauri::AppHandle;

#[tauri::command]
pub async fn update_apply(app: AppHandle) -> Result<(), String> {
    #[cfg(feature = "updates")]
    return crate::away(move || there::apply(&app)).await;
    #[cfg(not(feature = "updates"))]
    {
        let _ = app;
        Err("failed".into())
    }
}

/// The version that is there to be put in place.
pub fn ready() -> Option<String> {
    #[cfg(feature = "updates")]
    return there::READY.lock().unwrap().as_ref().map(|(update, _)| update.version.clone());
    #[cfg(not(feature = "updates"))]
    None
}

/// A newer version that the package manager puts in place, and which kind of package this is: `deb` or `arch`.
#[derive(Clone, serde::Serialize)]
pub struct Out {
    pub version: String,
    pub how: &'static str,
}

pub fn out() -> Option<Out> {
    #[cfg(feature = "updates")]
    return there::OUT.lock().unwrap().clone();
    #[cfg(not(feature = "updates"))]
    None
}

pub fn watch(_app: &AppHandle) {
    #[cfg(feature = "updates")]
    if let Some(how) = there::how() {
        let app = _app.clone();
        std::thread::spawn(move || there::watch(&app, how));
    }
}

#[cfg(feature = "updates")]
mod there {
    use super::Out;
    use std::path::Path;
    use std::sync::Mutex;
    use std::time::Duration;
    use tauri::{AppHandle, Emitter, Manager};
    use tauri_plugin_updater::{Update, UpdaterBuilder, UpdaterExt};

    const FIRST: Duration = Duration::from_secs(60);
    const DAY: Duration = Duration::from_secs(24 * 60 * 60);
    /// Where a release's files are, as tauri.conf.json's address has it; what a package needs is one of them.
    pub const FILES: &str = "https://github.com/Salesflare/TheMachine/releases/latest/download/";

    pub static READY: Mutex<Option<(Update, Vec<u8>)>> = Mutex::new(None);
    pub static OUT: Mutex<Option<Out>> = Mutex::new(None);

    #[derive(Clone, Copy, Debug, PartialEq)]
    #[cfg_attr(not(target_os = "linux"), allow(dead_code))]
    pub enum How {
        /// It puts the newer one in place of itself.
        Replaces,
        /// Its package manager does: `deb` or `arch`.
        Package(&'static str),
    }

    pub fn how() -> Option<How> {
        let own = std::env::current_exe().ok()?;
        #[cfg(target_os = "linux")]
        {
            // Only while it runs from that AppImage's mount: an APPIMAGE left over from elsewhere doesn't count
            let mounted = std::env::var_os("APPDIR").is_some_and(|at| !at.is_empty() && own.starts_with(at));
            let image = std::env::var_os("APPIMAGE").filter(|_| mounted);
            return linux_how(&own, image.as_deref().map(Path::new));
        }
        #[cfg(not(target_os = "linux"))]
        replaces_at(&own).then_some(How::Replaces)
    }

    /// Windows: next to what uninstalls it. Mac: in an app, and not where macOS runs a download from.
    #[cfg(not(target_os = "linux"))]
    fn replaces_at(own: &Path) -> bool {
        if cfg!(windows) {
            return own.with_file_name("uninstall.exe").exists();
        }
        own.ends_with("Contents/MacOS/the-machine-desktop") && !own.to_string_lossy().contains("/AppTranslocation/")
    }

    /// An AppImage (its runtime says where in APPIMAGE) that is the person's own, in a folder of theirs: it is renamed away
    /// and the newer one written in its place, never written over. The program of a .deb or an Arch package is its package
    /// manager's. Anything else (unpacked, built here) is left as it is.
    #[cfg(target_os = "linux")]
    fn linux_how(own: &Path, appimage: Option<&Path>) -> Option<How> {
        use std::os::unix::fs::MetadataExt;
        if let Some(image) = appimage {
            let me = std::fs::read_to_string("/proc/self/status").ok()?.lines().find_map(|l| l.strip_prefix("Uid:"))?.split_whitespace().nth(1)?.parse::<u32>().ok()?;
            let mine = |p: &Path| std::fs::metadata(p).is_ok_and(|m| m.uid() == me && m.mode() & 0o200 != 0);
            let theirs = image.is_absolute() && image.is_file() && mine(image) && image.parent().is_some_and(mine);
            return theirs.then_some(How::Replaces);
        }
        if own != Path::new("/usr/bin/the-machine-desktop") {
            return None;
        }
        let listed = |folder: &str, starts: &str, ends: &str| {
            std::fs::read_dir(folder).is_ok_and(|all| all.flatten().any(|e| e.file_name().to_str().is_some_and(|n| n.starts_with(starts) && n.ends_with(ends))))
        };
        if listed("/var/lib/pacman/local", "the-machine-desktop-bin-", "") {
            Some(How::Package("arch"))
        } else if listed("/var/lib/dpkg/info", "the-machine", ".list") {
            Some(How::Package("deb"))
        } else {
            None
        }
    }

    pub fn watch(app: &AppHandle, how: How) {
        std::thread::sleep(if cfg!(feature = "sandbox") { Duration::from_secs(3) } else { FIRST });
        loop {
            match tauri::async_runtime::block_on(look(app, how)) {
                Ok(true) => {
                    let _ = app.emit_to("settings", "settings", ());
                    crate::later(app, crate::follow_tray);
                }
                Ok(false) => {}
                Err(_error) => {
                    #[cfg(feature = "sandbox")]
                    eprintln!("updates: {_error}");
                }
            }
            std::thread::sleep(DAY);
        }
    }

    /// Whether there is a newer version than what is here and than what it found before: fetched and its signature checked
    /// where it replaces itself; for a package, only its version.
    async fn look(app: &AppHandle, how: How) -> tauri_plugin_updater::Result<bool> {
        let had = super::ready().or_else(|| super::out().map(|o| o.version));
        #[allow(unused_mut)]
        let mut of = source(app.updater_builder())?.timeout(Duration::from_secs(15 * 60));
        #[cfg(target_os = "linux")]
        if let Some(image) = std::env::var_os("APPIMAGE") {
            of = of.executable_path(image); // what is put in place: the AppImage, not the program inside it
        }
        let found = of.build()?.check().await?;
        let Some(update) = found.filter(|u| Some(&u.version) != had.as_ref()) else { return Ok(false) };
        match how {
            How::Package(kind) => *OUT.lock().unwrap() = Some(Out { version: update.version.clone(), how: kind }),
            How::Replaces => {
                let bytes = update.download(|_, _| {}, || {}).await?;
                *READY.lock().unwrap() = Some((update, bytes));
            }
        }
        Ok(true)
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

    /// Windows: its installer takes over, and starts it again. A Mac's app and an AppImage are replaced, and it starts again.
    /// A package: its file opens in the browser, for the package manager. Not on the main thread.
    pub fn apply(app: &AppHandle) -> Result<(), String> {
        if let Some(out) = OUT.lock().unwrap().clone() {
            use tauri_plugin_opener::OpenerExt;
            let file = if out.how == "arch" { "PKGBUILD" } else { "the-machine-desktop-amd64.deb" };
            return app.opener().open_url(format!("{FILES}{file}"), None::<&str>).map_err(|_| "browser".to_string());
        }
        let Some((update, bytes)) = READY.lock().unwrap().take() else { return Err("failed".into()) };
        crate::notify::quits();
        app.state::<crate::Shared>().save();
        if let Err(error) = update.install(&bytes) {
            eprintln!("could not update: {error}");
            *READY.lock().unwrap() = Some((update, bytes));
            return Err("failed".into());
        }
        crate::hangs::LEAVES.store(true, std::sync::atomic::Ordering::Relaxed);
        app.request_restart();
        Ok(())
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        #[cfg(not(target_os = "linux"))]
        fn only_where_it_can_replace_itself() {
            if cfg!(target_os = "macos") {
                assert!(replaces_at(Path::new("/Applications/The Machine.app/Contents/MacOS/the-machine-desktop")));
                assert!(!replaces_at(Path::new("/private/var/folders/x/AppTranslocation/y/d/The Machine.app/Contents/MacOS/the-machine-desktop")));
            }
            assert!(!replaces_at(Path::new("/somewhere/target/release/the-machine-desktop")));
        }

        #[test]
        #[cfg(target_os = "linux")]
        fn an_appimage_of_the_persons_own() {
            let folder = std::env::temp_dir().join(format!("updates-test-{}", std::process::id()));
            std::fs::create_dir_all(&folder).unwrap();
            let image = folder.join("the-machine-desktop-x86_64.AppImage");
            std::fs::write(&image, b"\x7fELF").unwrap();
            let built = Path::new("/somewhere/target/release/the-machine-desktop");
            assert_eq!(linux_how(built, Some(image.as_path())), Some(How::Replaces));
            assert_eq!(linux_how(built, Some(Path::new("relative.AppImage"))), None);
            assert_eq!(linux_how(built, Some(folder.join("gone.AppImage").as_path())), None);
            assert_eq!(linux_how(built, None), None, "unpacked or built here: left as it is");
            std::fs::remove_dir_all(&folder).unwrap();
        }

        #[test]
        fn its_key_and_where_it_looks() {
            use base64::Engine;
            let all: serde_json::Value = serde_json::from_str(include_str!("../tauri.conf.json")).unwrap();
            let its = &all["plugins"]["updater"];
            let key = base64::engine::general_purpose::STANDARD.decode(its["pubkey"].as_str().unwrap()).unwrap();
            assert!(String::from_utf8(key).unwrap().starts_with("untrusted comment: "));
            let at = its["endpoints"][0].as_str().unwrap();
            assert!(at.starts_with("https://") && !at.contains("{{"), "it tells nothing");
            assert_eq!(at.strip_suffix("latest.json"), Some(FILES), "a package's files are where latest.json is");
        }
    }
}
