//! Files that leave the dashboard: they land in Downloads, under a name of their own there.
use crate::{dash, later, Shared};
use std::path::{Path, PathBuf};
use tauri::webview::DownloadEvent;
use tauri::{AppHandle, Manager};
use url::Url;

/// What a page downloads. Where it goes is only told when it starts: those under way are kept until they are done.
pub fn download(app: &AppHandle, event: DownloadEvent<'_>) -> bool {
    match event {
        DownloadEvent::Requested { url, destination } => {
            let Ok(folder) = app.path().download_dir() else { return false };
            let name = destination.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
            #[cfg(target_os = "linux")]
            let name = crate::linux_app::sent_as(&url).unwrap_or(name);
            #[cfg(target_os = "linux")]
            dash::kept(app, &url, false);
            *destination = free(&folder, &name);
            app.state::<Shared>().downloads.lock().unwrap().push((url.into(), destination.clone()));
        }
        DownloadEvent::Finished { url, path, success } => {
            let shared = app.state::<Shared>();
            let mut under_way = shared.downloads.lock().unwrap();
            let kept = under_way.iter().position(|(of, _)| *of == url.as_str()).map(|i| under_way.remove(i).1);
            drop(under_way);
            let path = if cfg!(target_os = "linux") { None } else { path }; // there each window is told of all of them
            if let Some(file) = path.or(kept) {
                #[cfg(target_os = "linux")]
                dash::kept(app, &url, true);
                done(app, file, success);
            }
        }
        _ => {}
    }
    true
}

/// A file that is open in a window of its own, kept too.
pub fn save(app: &AppHandle, url: Url) {
    let Some(machine) = app.state::<Shared>().machine() else { return };
    let app = app.clone();
    std::thread::spawn(move || {
        let Ok(folder) = app.path().download_dir() else { return };
        match machine.save(&url, &folder) {
            Ok(file) => {
                #[cfg(windows)]
                crate::windows_app::from_the_internet(&file);
                done(&app, file, true)
            }
            Err(name) => done(&app, folder.join(name), false),
        }
    });
}

fn done(app: &AppHandle, file: PathBuf, saved: bool) {
    later(app, move |app| {
        #[cfg(target_os = "macos")]
        if saved {
            crate::mac_app::downloaded(&file);
        }
        let name = file.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        dash::tell(app, &serde_json::json!({ if saved { "saved" } else { "failed" }: name }));
    });
}

/// A file of this name that isn't there yet, as browsers count: "a.pdf", "a (1).pdf".
pub fn free(folder: &Path, name: &str) -> PathBuf {
    // What a Machine says is a name: never a place elsewhere, and nothing hidden
    let name: String = name.chars().map(|c| if c.is_control() || "/\\:*?\"<>|".contains(c) { '_' } else { c }).collect();
    let name = name.trim().trim_start_matches('.').trim_end_matches(['.', ' ']);
    let name = if name.is_empty() { "download" } else { name };
    let (stem, end) = match name.rfind('.').filter(|at| *at > 0 && name.len() - at <= 12) {
        Some(at) => name.split_at(at),
        None => (name, ""),
    };
    let stem: String = stem.chars().take(120).collect();
    (0..).map(|n| folder.join(if n == 0 { format!("{stem}{end}") } else { format!("{stem} ({n}){end}") })).find(|p| !p.exists()).expect("one that is free")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_name_of_its_own_in_that_folder() {
        let folder = std::env::temp_dir().join(format!("machine-files-{}", std::process::id()));
        std::fs::create_dir_all(&folder).unwrap();
        let named = |n: &str| free(&folder, n).strip_prefix(&folder).unwrap().to_string_lossy().into_owned();
        assert_eq!([named("a.pdf"), named("../../a.pdf"), named("..\\a.pdf"), named(".hidden"), named(""), named(" . ")],
            ["a.pdf", "_.._a.pdf", "_a.pdf", "hidden", "download", "download"]);
        assert_eq!(named("a\nb:c?.txt"), "a_b_c_.txt");
        std::fs::write(folder.join("a.pdf"), "x").unwrap();
        std::fs::write(folder.join("a (1).pdf"), "x").unwrap();
        assert_eq!(named("a.pdf"), "a (2).pdf");
        assert!(named(&"x".repeat(400)).len() <= 120 && named(&format!("{}.pdf", "x".repeat(400))).ends_with("x.pdf"));
        std::fs::remove_dir_all(folder).unwrap();
    }
}
