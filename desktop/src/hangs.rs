//! A main thread or a page that doesn't answer: a line in hangs.log, next to app.json, so that the next one tells why. On
//! macOS with what its threads were doing. It stays on this computer, and holds nothing but places in the programs' own code.
use crate::{later, why, windows, Shared};
use std::panic::Location;
use std::path::Path;
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use tauri::{AppHandle, Manager};

pub const NAME: &str = "hangs.log";
/// Counted in steps, not by the clock: a computer that slept didn't hang.
const STEP: Duration = Duration::from_millis(250);
const STUCK: u32 = 20;
/// The robot's own pages are asked this often, and are made again when they didn't answer this many times in a row.
const PAGES: Duration = Duration::from_secs(20);
const TWICE: u32 = 2;
/// How often a stack is written while one program runs, and a page made again.
const STACKS: u64 = 5;

/// The last work the main thread was given (main.rs, `later`), and whether that is done.
static LAST: Mutex<Option<(&'static Location<'static>, Instant, bool)>> = Mutex::new(None);

/// A newer version takes over: this one waits for the system to start it, which may ask the person first.
pub static LEAVES: AtomicBool = AtomicBool::new(false);

pub fn starts(of: &'static Location<'static>) {
    if let Ok(mut last) = LAST.lock() {
        *last = Some((of, Instant::now(), false));
    }
}

pub fn ends() {
    if let Ok(mut last) = LAST.lock() {
        if let Some(last) = &mut *last {
            last.2 = true;
        }
    }
}

fn last() -> String {
    let last = LAST.try_lock().ok().and_then(|l| *l);
    last.map_or("nothing yet".into(), |(of, at, done)| {
        format!("{}:{} {} s ago, {}", of.file(), of.line(), at.elapsed().as_secs(), if done { "done" } else { "still running" })
    })
}

pub fn watch(app: &AppHandle) {
    let file = app.state::<Shared>().file.with_file_name(NAME);
    let here = app.clone();
    std::thread::spawn(move || main_thread(&here, &file));
    let here = app.clone();
    std::thread::spawn(move || pages(&here));
}

fn main_thread(app: &AppHandle, file: &Path) {
    loop {
        let answered = Arc::new(AtomicBool::new(false));
        let told = answered.clone();
        if app.run_on_main_thread(move || told.store(true, Ordering::Relaxed)).is_err() {
            return; // it ends
        }
        if !within(&answered, STUCK) {
            if LEAVES.load(Ordering::Relaxed) {
                return;
            }
            let since = Instant::now();
            note(file, &format!("the main thread doesn't answer for 5 s ({}); last work: {}", about(), last()));
            stack(file, std::process::id());
            if !within(&answered, 4 * 55) {
                note(file, &format!("still not; last work: {}", last()));
                stack(file, std::process::id());
            }
            while !answered.load(Ordering::Relaxed) {
                std::thread::sleep(STEP);
            }
            note(file, &format!("the main thread answers again, after {} s more", since.elapsed().as_secs()));
        }
        std::thread::sleep(Duration::from_secs(1));
    }
}

fn within(answered: &AtomicBool, steps: u32) -> bool {
    (0..steps).any(|_| {
        std::thread::sleep(STEP);
        answered.load(Ordering::Relaxed)
    })
}

/// The robot's and the box's, while they are there to be seen. The dashboard's may well wait for the person (an
/// alert), and has a Reload.
fn pages(app: &AppHandle) {
    let (mut missed, mut again) = ([0_u32; 2], 0);
    loop {
        std::thread::sleep(PAGES);
        let (tell, told) = std::sync::mpsc::channel();
        let asks = tell.clone();
        if app.run_on_main_thread(move || { let _ = asks.send(None); }).is_err() {
            return;
        }
        if !matches!(told.recv_timeout(Duration::from_secs(5)), Ok(None)) {
            continue; // the main thread's own
        }
        for (i, label) in ["robot", "box"].into_iter().enumerate() {
            let Some(window) = app.get_webview_window(label) else { continue };
            // Twice: after the computer slept the first may get lost
            let answers = (0..2).any(|_| {
                let (tell, asked) = (tell.clone(), window.clone());
                let _ = app.run_on_main_thread(move || {
                    if !asked.is_visible().unwrap_or(false) {
                        let _ = tell.send(None);
                    } else {
                        let _ = asked.eval_with_callback("1", move |_| { let _ = tell.send(Some(i)); });
                    }
                });
                // An answer that comes too late is of another page than is waited for
                (0..16).any(|_| match told.recv_timeout(STEP) {
                    Ok(of) => of.is_none_or(|of| of == i),
                    Err(_) => false,
                })
            });
            missed[i] = if answers { 0 } else { missed[i] + 1 };
            if answers {
                continue;
            }
            let file = app.state::<Shared>().file.with_file_name(NAME);
            note(&file, &format!("the {label}'s page doesn't answer for 8 s ({})", about()));
            #[cfg(all(target_os = "macos", not(feature = "store")))]
            if let Some(page) = crate::mac_app::process(&window) {
                stack(&file, page);
            }
            if missed[i] >= TWICE && again < STACKS {
                (missed[i], again) = (0, again + 1);
                note(&file, &format!("the {label}'s page is made again"));
                later(app, move |app| windows::again(app, label));
            }
        }
    }
}

fn note(file: &Path, line: &str) {
    why::note(file, line);
}

fn about() -> String {
    format!("{} {}, {} {}", crate::version(), std::env::consts::ARCH, std::env::consts::OS, system()).trim_end().to_string()
}

#[cfg(target_os = "macos")]
fn system() -> String {
    objc2_foundation::NSProcessInfo::processInfo().operatingSystemVersionString().to_string()
}

#[cfg(not(target_os = "macos"))]
fn system() -> &'static str {
    ""
}

/// What the threads of it are doing, as Activity Monitor's Sample Process tells it: the calls only, without whose computer
/// this is.
fn stack(file: &Path, process: u32) {
    static WRITTEN: AtomicU64 = AtomicU64::new(0);
    if WRITTEN.fetch_add(1, Ordering::Relaxed) >= STACKS {
        return;
    }
    let Some(calls) = calls(process) else { return note(file, "no stack: it could not be read") };
    let into = file.with_file_name(format!("hang-{}.txt", WRITTEN.load(Ordering::Relaxed)));
    if std::fs::write(&into, calls).is_ok() {
        note(file, &format!("its stacks are in {}", into.file_name().unwrap_or_default().to_string_lossy()));
    }
}

/// Not in the Mac App Store's build: in the App Sandbox sample may read no other process, and none of its own either.
#[cfg(all(target_os = "macos", feature = "store"))]
fn calls(_: u32) -> Option<String> {
    None
}

#[cfg(all(target_os = "macos", not(feature = "store")))]
fn calls(process: u32) -> Option<String> {
    use std::process::{Command, Stdio};
    let into = std::env::temp_dir().join(format!("the-machine-sample-{process}.txt"));
    let mut child = Command::new("/usr/bin/sample")
        .args([&process.to_string(), "1", "-mayDie", "-file"])
        .arg(&into)
        .stdin(Stdio::null())
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .ok()?;
    // It may hang itself
    for _ in 0..120 {
        std::thread::sleep(STEP);
        if child.try_wait().ok()?.is_some() {
            break;
        }
    }
    let _ = child.kill();
    let _ = child.wait();
    let all = std::fs::read_to_string(&into).ok();
    let _ = std::fs::remove_file(&into);
    Some(told(&all?)).filter(|t| !t.is_empty())
}

/// Windows has nothing that can be asked so; Linux tells in which of its own calls each thread waits.
#[cfg(target_os = "linux")]
fn calls(process: u32) -> Option<String> {
    let mut all = String::new();
    for thread in std::fs::read_dir(format!("/proc/{process}/task")).ok()?.flatten() {
        let of = |name: &str| std::fs::read_to_string(thread.path().join(name)).unwrap_or_default().trim().to_string();
        all += &format!("{} {}: {} {}\n", thread.file_name().to_string_lossy(), of("comm"), of("wchan"), of("syscall").split(' ').next().unwrap_or_default());
    }
    Some(all)
}

#[cfg(windows)]
fn calls(_: u32) -> Option<String> {
    None
}

/// Of sample's answer: the system's version and the calls, not the paths.
#[cfg(any(all(target_os = "macos", not(feature = "store")), test))]
fn told(all: &str) -> String {
    let heads = all.lines().filter(|l| l.starts_with("OS Version:") || l.starts_with("Code Type:") || l.starts_with("Version:"));
    let calls = all.lines().skip_while(|l| !l.starts_with("Call graph:")).take_while(|l| !l.starts_with("Binary Images:")).take(1500);
    let calls: Vec<&str> = calls.collect();
    if calls.is_empty() {
        return String::new();
    }
    heads.chain(calls).collect::<Vec<_>>().join("\n") + "\n"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn a_stack_without_paths() {
        let all = "Analysis of sampling x (pid 1)\nPath: /Users/someone/App\nOS Version: macOS 15.1\n\nCall graph:\n  1 Thread_1 main\nBinary Images:\n 0x1 /Users/someone/App\n";
        let told = told(all);
        assert!(told.starts_with("OS Version: macOS 15.1\nCall graph:\n  1 Thread_1 main\n"), "{told}");
        assert!(!told.contains("someone"));
        assert!(super::told("").is_empty());
    }

    /// A lock that is kept while something is asked that waits (a window, the Machine, another lock) can keep the main thread
    /// waiting for good: first copy what is in it, then let it go, then ask. What is locked for one statement ends with that.
    #[test]
    fn no_lock_is_kept_while_something_waits() {
        const WAITS: [&str; 34] = [
            "window.is_", "window.set", "window.eval", "window.show", "window.hide", "window.unmin", "window.max", "window.url", "window.nav", ".outer_", ".inner_",
            "webview", "windows::", "emit", "later(", "note(", "save()", "notify::gone", "notify::show", "notify::look", "card::", "dash::", "login::", "app.get",
            "app.run", "app.opener", ".check(", ".status(", ".notice(", ".lock()", "recv", "sleep", "proxy(", "eval",
        ];
        let (mut bad, mut seen) = (Vec::new(), 0);
        for file in std::fs::read_dir(concat!(env!("CARGO_MANIFEST_DIR"), "/src")).unwrap().flatten() {
            let all = std::fs::read_to_string(file.path()).unwrap();
            let lines: Vec<&str> = all.lines().take_while(|l| !l.starts_with("#[cfg(test)]")).map(|l| l.split(" // ").next().unwrap()).collect();
            let deep = |l: &str| l.len() - l.trim_start().len();
            for (i, line) in lines.iter().enumerate().filter(|(_, l)| l.contains(".lock()") && !l.trim_start().starts_with("//")) {
                seen += 1;
                let (what, at) = (line.trim_start(), format!("{}:{}: {}", file.file_name().to_string_lossy(), i + 1, line.trim()));
                // Kept for the whole block, or for all of what is made
                let block = ["if let", "while let", "match", "for "].iter().any(|b| what.starts_with(b)) || what.contains("= match") || what.contains("= if let");
                let field = what.split_once(": ").is_some_and(|(name, _)| name.chars().all(|c| c.is_ascii_lowercase() || c == '_'));
                if field || what.matches(".lock()").count() > 1 {
                    bad.push(at);
                    continue;
                }
                let kept = what.strip_prefix("let ").and_then(|l| l.strip_prefix("mut ").or(Some(l))).and_then(|l| l.split_once(" = ")).filter(|_| what.ends_with(".lock().unwrap();"));
                let own = kept.map(|(name, _)| name).filter(|n| !n.starts_with('('));
                if !block && (kept.is_none() || own.is_some_and(|n| n.starts_with("_one"))) {
                    continue;
                }
                let until = own.map(|n| format!("drop({n})"));
                let body = lines[i + 1..].iter().take_while(|l| l.trim().is_empty() || if block { deep(l) > deep(line) } else { deep(l) >= deep(line) && until.as_ref().is_none_or(|u| !l.contains(u)) });
                bad.extend(body.filter(|l| WAITS.iter().any(|w| l.contains(w))).map(|l| format!("{at} ... {}", l.trim())));
            }
        }
        assert!(seen > 100, "{seen}");
        assert!(bad.is_empty(), "{}", bad.join("\n"));
    }

    #[test]
    fn what_ran_last() {
        starts(Location::caller());
        assert!(last().ends_with("still running"));
        ends();
        assert!(last().contains("hangs.rs") && last().ends_with("done"));
    }

    #[test]
    fn it_answers() {
        assert!(within(&AtomicBool::new(true), 1));
        assert!(!within(&AtomicBool::new(false), 1));
    }
}
