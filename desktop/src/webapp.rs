//! The dashboard as an installed app: what Chrome, Edge and the browsers made of them call a web app. A link another
//! program opens always lands in a tab, so the app is started as its own menu entry starts it, with the address to open.
//! The open window takes it (the dashboard's launch_handler). The entry is found by the app's id, which comes from the
//! Machine's own address: another Machine's app has another one. Without one, the browser.
use sha2::{Digest, Sha256};
use std::ffi::OsString;
use std::path::Path;
use std::process::{Command, Stdio};
use url::Url;

/// Opens an address of this Machine in its installed app. False: there is none. `alone`: no other Machine answers at
/// this one's host.
pub fn open(machine: &str, address: &str, alone: bool) -> bool {
    own(machine, address) && ids(machine, alone).iter().any(|id| system::entries(id).into_iter().any(|e| start(e, address)))
}

/// How an installed app is started: the program and its arguments, as its entry on this computer has them.
#[derive(Debug, PartialEq)]
pub struct Entry {
    argv: Vec<String>,
    #[cfg(target_os = "linux")]
    file: std::path::PathBuf,
}

impl Entry {
    /// Its browser: an absolute path to a program that is there. Nothing else is started.
    fn program(&self) -> Option<&Path> {
        let program = Path::new(self.argv.first()?);
        (program.is_absolute() && program.is_file()).then_some(program)
    }

    /// The browser with the entry's own arguments, and the page to open as one more (own() checked it first).
    fn command(&self, address: &str) -> Option<Command> {
        let mut open = OsString::from("--app-launch-url-for-shortcuts-menu-item=");
        open.push(address);
        let mut command = Command::new(self.program()?);
        command.args(&self.argv[1..]).arg(open);
        command.stdin(Stdio::null()).stdout(Stdio::null()).stderr(Stdio::null());
        Some(command)
    }
}

fn start(entry: Entry, address: &str) -> bool {
    let Some(mut command) = entry.command(address) else { return false };
    system::prepare(&entry, &mut command);
    let Ok(mut child) = command.spawn() else { return false };
    std::thread::spawn(move || child.wait());
    true
}

/// The Machine's own page, with at most which robot opens it (?desk=) and a place in it (#card=...).
fn own(machine: &str, address: &str) -> bool {
    address.strip_prefix(machine).is_some_and(|rest| {
        let hex = |d: &str| d.len() == 32 && d.bytes().all(|b| b.is_ascii_hexdigit());
        let rest = rest.strip_prefix("?desk=").map_or(Some(rest), |r| r.get(32..).filter(|_| hex(&r[..32])));
        let Some(rest) = rest else { return false };
        rest.is_empty() || rest.strip_prefix('#').is_some_and(|r| r.bytes().all(|b| b.is_ascii_alphanumeric() || b"=-_/&".contains(&b)))
    })
}

/// The ids its app can have. The manifest says "id": ".", which is the host whatever the path; installed before it did,
/// the page itself.
pub fn ids(machine: &str, alone: bool) -> Vec<String> {
    let Ok(url) = Url::parse(machine) else { return Vec::new() };
    let mut ids = vec![id(url.as_str())];
    if url.path() != "/" && alone {
        ids.push(id(&format!("{}/", url.origin().ascii_serialization())));
    }
    ids
}

/// The id Chromium gives the app with this manifest id.
fn id(manifest: &str) -> String {
    Sha256::digest(Sha256::digest(manifest))[..16].iter().flat_map(|b| [b >> 4, b & 15]).map(|n| (b'a' + n) as char).collect()
}

#[cfg(target_os = "linux")]
mod system {
    use super::Entry;
    use gtk::gio::{self, prelude::*};
    use gtk::{gdk, glib};
    use std::process::Command;

    /// The browsers' .desktop files in the person's own folder, the newest first.
    pub fn entries(id: &str) -> Vec<Entry> {
        let mut files: Vec<_> = std::fs::read_dir(glib::user_data_dir().join("applications"))
            .into_iter()
            .flatten()
            .flatten()
            .filter(|f| f.file_name().to_str().is_some_and(|n| n.contains(id) && n.ends_with(".desktop")))
            .map(|f| (f.metadata().and_then(|m| m.modified()).ok(), f.path()))
            .collect();
        files.sort_by(|a, b| b.cmp(a));
        files.into_iter().filter_map(|(_, file)| entry(file, id)).collect()
    }

    /// Nothing for one that is hidden, or whose browser is gone.
    fn entry(file: std::path::PathBuf, id: &str) -> Option<Entry> {
        let line = gio::DesktopAppInfo::from_filename(&file)?.commandline()?;
        Some(Entry { argv: argv(line.to_str()?, id)?, file })
    }

    fn argv(line: &str, id: &str) -> Option<Vec<String>> {
        let argv: Vec<String> = glib::shell_parse_argv(line).ok()?.into_iter().map(|a| a.into_string().ok()).collect::<Option<_>>()?;
        let argv: Vec<String> = argv.into_iter().filter(|a| !(a.len() == 2 && a.starts_with('%'))).map(|a| a.replace("%%", "%")).collect();
        argv.contains(&format!("--app-id={id}")).then_some(argv)
    }

    /// The click's own token, so that the app may take the focus (Wayland, and X11's startup id).
    pub fn prepare(entry: &Entry, command: &mut Command) {
        let token = gdk::Display::default()
            .and_then(|d| d.app_launch_context())
            .zip(gio::DesktopAppInfo::from_filename(&entry.file))
            .and_then(|(context, info)| context.startup_notify_id(&info, &[]));
        if let Some(token) = token {
            command.env("XDG_ACTIVATION_TOKEN", &token).env("DESKTOP_STARTUP_ID", &token);
        }
    }

    #[cfg(test)]
    #[test]
    fn reads_an_entry() {
        let id = super::id("https://my.example.com/");
        let line = format!("\"/opt/a b/chrome\" --profile-directory=\"Profile 1\" --app-id={id} %U");
        assert_eq!(argv(&line, &id).unwrap(), ["/opt/a b/chrome", "--profile-directory=Profile 1", &format!("--app-id={id}")]);
        assert_eq!(argv(&line, &super::id("https://other.example.com/")), None);
        assert_eq!(argv(&format!("/opt/chrome --app-id={id}x"), &id), None);
        assert_eq!(argv("/opt/chrome \"", &id), None);
    }
}

#[cfg(windows)]
mod system {
    use super::Entry;
    use std::path::{Path, PathBuf};
    use std::process::Command;
    use ::windows::core::{Interface, HSTRING};
    use ::windows::Win32::System::Com::{CoCreateInstance, CoInitializeEx, IPersistFile, CLSCTX_INPROC_SERVER, COINIT_MULTITHREADED, STGM_READ};
    use ::windows::Win32::UI::Shell::{IShellLinkW, ShellLink};
    use windows_registry::CURRENT_USER;
    use windows_sys::Win32::Foundation::LocalFree;
    use windows_sys::Win32::UI::Shell::CommandLineToArgvW;

    /// What Windows lists under installed apps, in the person's own part of the registry. When it isn't there (an app an
    /// administrator installed), what the Start menu has.
    pub fn entries(id: &str) -> Vec<Entry> {
        let listed: Vec<_> = uninstalls().iter().filter_map(|line| argv(&split(line), id)).collect();
        let found = if listed.is_empty() { shortcuts(id) } else { listed };
        found.into_iter().map(|argv| Entry { argv }).collect()
    }

    fn uninstalls() -> Vec<String> {
        let Ok(all) = CURRENT_USER.open(r"Software\Microsoft\Windows\CurrentVersion\Uninstall") else { return Vec::new() };
        all.keys().into_iter().flatten().filter_map(|name| all.open(name).ok()?.get_string("UninstallString").ok()).collect()
    }

    /// The Start menu's own folder and the ones in it (Chrome keeps its apps in "Chrome Apps").
    fn shortcuts(id: &str) -> Vec<Vec<String>> {
        let Some(menu) = std::env::var_os("APPDATA").map(|a| Path::new(&a).join(r"Microsoft\Windows\Start Menu\Programs")) else { return Vec::new() };
        let list = |folder: &Path| -> Vec<PathBuf> { std::fs::read_dir(folder).into_iter().flatten().flatten().map(|f| f.path()).collect() };
        let here = list(&menu);
        let below: Vec<PathBuf> = here.iter().filter(|p| p.is_dir()).flat_map(|p| list(p)).collect();
        let links = here.iter().chain(&below).filter(|p| p.extension().is_some_and(|e| e.eq_ignore_ascii_case("lnk")));
        links.filter_map(|link| argv(&read(link).ok()?, id)).collect()
    }

    /// A shortcut's program and arguments.
    fn read(link: &Path) -> ::windows::core::Result<Vec<String>> {
        let text = |b: &[u16]| String::from_utf16_lossy(b.split(|c| *c == 0).next().unwrap_or_default());
        let (mut program, mut arguments) = ([0; 1024], [0; 2048]);
        // SAFETY: plain calls with buffers of their own length; the rest frees itself.
        unsafe {
            let _ = CoInitializeEx(None, COINIT_MULTITHREADED);
            let shortcut: IShellLinkW = CoCreateInstance(&ShellLink, None, CLSCTX_INPROC_SERVER)?;
            shortcut.cast::<IPersistFile>()?.Load(&HSTRING::from(link), STGM_READ)?;
            shortcut.GetPath(&mut program, std::ptr::null_mut(), 0)?;
            shortcut.GetArguments(&mut arguments)?;
        }
        Ok(split(&format!("\"{}\" {}", text(&program), text(&arguments))))
    }

    /// Windows' own way to take a command line apart.
    fn split(line: &str) -> Vec<String> {
        let line: Vec<u16> = line.encode_utf16().chain([0]).collect();
        let mut count = 0;
        // SAFETY: the line ends with a 0; what comes back is `count` strings that end with one, freed once here.
        unsafe {
            let parts = CommandLineToArgvW(line.as_ptr(), &mut count);
            if parts.is_null() {
                return Vec::new();
            }
            let read = |part: *const u16| {
                let length = (0..).take_while(|&i| *part.add(i) != 0).count();
                String::from_utf16_lossy(std::slice::from_raw_parts(part, length))
            };
            let found = (0..count as usize).map(|i| read(*parts.add(i))).collect();
            LocalFree(parts.cast());
            found
        }
    }

    /// From how the browser starts or uninstalls this app to how it starts it.
    fn argv(listed: &[String], id: &str) -> Option<Vec<String>> {
        let program = listed.first().filter(|p| Path::new(p).is_absolute() && p.to_lowercase().ends_with(".exe"))?;
        if !listed.iter().any(|a| [format!("--uninstall-app-id={id}"), format!("--app-id={id}")].contains(a)) {
            return None;
        }
        let kept = listed.iter().filter(|a| a.starts_with("--profile-directory=") || a.starts_with("--user-data-dir="));
        Some([program].into_iter().chain(kept).cloned().chain([format!("--app-id={id}")]).collect())
    }

    pub fn prepare(_: &Entry, _: &mut Command) {}

    #[cfg(test)]
    #[test]
    fn reads_an_entry() {
        let id = super::id("https://my.example.com/");
        let line = format!(r#""C:\a b\chrome.exe" --profile-directory="Profile 1" --uninstall-app-id={id}"#);
        assert_eq!(argv(&split(&line), &id).unwrap(), [r"C:\a b\chrome.exe", "--profile-directory=Profile 1", &format!("--app-id={id}")]);
        assert_eq!(argv(&split(&line), &super::id("https://other.example.com/")), None);
        assert_eq!(argv(&split(&format!(r#""chrome.exe" --uninstall-app-id={id}"#)), &id), None);
        assert_eq!(argv(&split(&format!(r#""C:\a\chrome.exe" --uninstall-app-id={id}x"#)), &id), None);
        assert_eq!(argv(&split(""), &id), None);
        let shortcut = split(&format!(r#""C:\a b\chrome_proxy.exe"  --profile-directory=Default --app-id={id}"#));
        assert_eq!(argv(&shortcut, &id).unwrap(), [r"C:\a b\chrome_proxy.exe", "--profile-directory=Default", &format!("--app-id={id}")]);
    }
}

/// macOS: each installed app is a small program its browser made, with the browser and the app's id in its Info.plist.
#[cfg(target_os = "macos")]
mod system {
    use super::Entry;
    use objc2_app_kit::NSWorkspace;
    use objc2_foundation::{NSBundle, NSString};
    use std::process::Command;

    const BROWSERS: [&str; 7] = [
        "com.google.Chrome", "com.microsoft.edgemac", "com.brave.Browser", "com.vivaldi.Vivaldi", "org.chromium.Chromium", "com.google.Chrome.beta", "com.microsoft.edgemac.Beta",
    ];

    pub fn entries(id: &str) -> Vec<Entry> {
        BROWSERS.iter().filter_map(|browser| entry(browser, id)).collect()
    }

    fn bundle(name: &str) -> Option<objc2::rc::Retained<NSBundle>> {
        let found = NSWorkspace::sharedWorkspace().URLForApplicationWithBundleIdentifier(&NSString::from_str(name))?;
        NSBundle::bundleWithURL(&found).filter(|b| b.bundleIdentifier().is_some_and(|i| i.to_string() == name))
    }

    /// Nothing for one whose browser is gone.
    fn entry(browser: &str, id: &str) -> Option<Entry> {
        let app = bundle(&format!("{browser}.app.{id}"))?;
        let says = |key: &str| app.objectForInfoDictionaryKey(&NSString::from_str(key)).and_then(|v| v.downcast::<NSString>().ok()).map(|v| v.to_string());
        let program = bundle(browser)?.executableURL()?.path()?.to_string();
        argv(program, says("CrAppModeShortcutID")?, says("CrAppModeProfileDir"), id).map(|argv| Entry { argv })
    }

    fn argv(program: String, named: String, profile: Option<String>, id: &str) -> Option<Vec<String>> {
        let profile = profile.filter(|p| !p.is_empty()).map(|p| format!("--profile-directory={p}"));
        (named == id).then(|| [program].into_iter().chain(profile).chain([format!("--app-id={id}")]).collect())
    }

    pub fn prepare(_: &Entry, _: &mut Command) {}

    #[cfg(test)]
    #[test]
    fn reads_an_entry() {
        let id = super::id("https://my.example.com/");
        let chrome = || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome".to_string();
        assert_eq!(argv(chrome(), id.clone(), Some("Profile 1".into()), &id).unwrap(), [chrome(), "--profile-directory=Profile 1".into(), format!("--app-id={id}")]);
        assert_eq!(argv(chrome(), id.clone(), None, &id).unwrap().len(), 2);
        assert_eq!(argv(chrome(), super::id("https://other.example.com/"), None, &id), None);
    }
}

#[cfg(not(any(windows, target_os = "linux", target_os = "macos")))]
mod system {
    use super::Entry;

    pub fn entries(_: &str) -> Vec<Entry> {
        Vec::new()
    }

    pub fn prepare(_: &Entry, _: &mut std::process::Command) {}
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_id_chrome_gives() {
        assert_eq!(id("http://127.0.0.1:8931/"), "fgbphkfplekcbajjgdeoaplmlccnhblm"); // as Chrome 154 installed it
    }

    #[test]
    fn only_this_machines_app() {
        let root = "https://box.tail1234.ts.net:8443/";
        assert_eq!(ids(root, false), [id(root)]);
        let path = "https://box.tail1234.ts.net:8443/assistant/";
        assert_eq!(ids(path, true), [id(path), id(root)]);
        assert_eq!(ids(path, false), [id(path)]); // the host's own app is another Machine's
        assert_ne!(id("https://one.app.themachine.computer/"), id("https://two.app.themachine.computer/"));
    }

    #[test]
    fn only_a_browser_that_is_there() {
        let entry = |program: &str| Entry {
            argv: vec![program.into(), "--app-id=x".into()],
            #[cfg(target_os = "linux")]
            file: Default::default(),
        };
        let here = std::env::current_exe().unwrap();
        let there = entry(here.to_str().unwrap());
        assert_eq!(there.program(), Some(here.as_path()));
        let started = there.command("https://my.example.com/").unwrap();
        let said: Vec<_> = started.get_args().collect();
        assert_eq!(said, ["--app-id=x", "--app-launch-url-for-shortcuts-menu-item=https://my.example.com/"]);
        let name = here.file_name().unwrap().to_str().unwrap();
        for not in [name, "", "/no/such/browser", here.parent().unwrap().to_str().unwrap()] {
            assert!(entry(not).command("https://my.example.com/").is_none(), "{not}");
        }
    }

    #[test]
    fn only_this_machines_page() {
        let machine = "https://my.example.com/assistant/";
        for fine in ["", "?desk=0123456789abcdef0123456789abcdef", "?desk=0123456789abcdef0123456789abcdef#card=244d6ae4cf6842a2", "#card=244d6ae4cf6842a2", "#settings/general"] {
            assert!(own(machine, &format!("{machine}{fine}")), "{fine}");
        }
        for other in ["https://my.example.com/", "https://my.example.com/assistant/?desk=a", "https://my.example.com/assistant/?x=0123456789abcdef0123456789abcdef", "https://my.example.com/assistant/../", "https://my.example.com/assistant/#card=a b",
            "https://my.example.com/assistant/#card=\"", "https://my.example.com.evil.example/assistant/", "file:///etc/passwd"] {
            assert!(!own(machine, other), "{other}");
        }
    }
}
