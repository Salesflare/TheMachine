//! WebView2's very first start on a computer takes seconds (about 8 on a new PC, more on CI's), whichever program starts
//! it, and all of it is the robot's first page being made, on the main thread, before anything shows. So the installer
//! starts it once (`--warm`, windows/hooks.nsh), while its own progress shows: the first start after it is as quick as
//! any other. What it keeps is the system's (its files read and checked once), not the app's.
use std::time::Duration;
use tauri::{WebviewUrl, WebviewWindowBuilder};

/// `--warm`: one hidden blank page, with the page cache and options the robot's have, then it ends. At most a minute.
/// Not as an administrator: the page cache would be made as theirs.
pub fn run() {
    if crate::elevated::full() {
        return;
    }
    std::thread::spawn(|| {
        std::thread::sleep(Duration::from_secs(60));
        std::process::exit(0);
    });
    let built = tauri::Builder::default()
        .setup(|app| {
            WebviewWindowBuilder::new(app.handle(), "warm", WebviewUrl::External("about:blank".parse().unwrap()))
                .visible(false)
                .additional_browser_args(&crate::windows::browser())
                .build()?;
            std::process::exit(0);
        })
        .build(crate::context());
    if let Ok(app) = built {
        app.run(|_, _| {});
    }
}
