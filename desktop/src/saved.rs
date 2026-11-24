//! What the app keeps: the Machine's address, a hosted Machine's session, and where the robot stands. One file only its
//! owner can read (0600; on Windows it is in the person's own profile folder). Of the Machine itself only fingerprints of
//! what was in For you (seen.rs).
use crate::place::Corner;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::{collections::BTreeMap, fs, io, path::{Path, PathBuf}};

#[derive(Clone, Debug, Default, PartialEq, Serialize, Deserialize)]
#[serde(default)]
pub struct Saved {
    pub machine: Option<String>,
    /// A hosted Machine's session cookie, from the account's app sign-in. Empty for a self-hosted one.
    pub cookie: Option<String>,
    pub monitor: Option<String>,
    pub places: BTreeMap<String, Corner>,
    /// It was told once where a hidden robot is.
    pub hide_told: bool,
    /// What was in For you when the person last looked. None: nothing was ever there.
    pub seen: Option<crate::seen::Seen>,
    /// When it speaks up ("...").
    pub speak: crate::speak::Speak,
    /// The dashboard's window: its place and size (dash.rs), whether it is as large as its screen, and its zoom (0: as made).
    pub window: Option<[f64; 4]>,
    pub wide: bool,
    pub zoom: f64,
    /// Settings: no robot, closing the window quits, and without a robot the system's own notifications.
    pub no_robot: bool,
    pub quits: bool,
    pub notify: Option<bool>,
    /// The person said no browser with notifications on is on this computer, for those there then (the Machine's number
    /// of them); and for which it was asked in a notification.
    pub none: u64,
    pub asked: u64,
    /// A random name for this robot, for its Machine to know which computer's it is (speak.rs).
    pub desk: String,
    /// What the pages' own keys are kept under (mac_app.rs).
    #[cfg(target_os = "macos")]
    pub pages: String,
}

impl Saved {
    /// What was kept, or else its second copy. One that is there and can't be read is never written over: it is put aside.
    pub fn read(file: &Path) -> Saved {
        let found = parsed(file).or_else(|| {
            let second = parsed(&second(file));
            if file.exists() {
                let _ = fs::rename(file, aside(file));
            }
            second
        });
        let mut saved = found.unwrap_or_default();
        if saved.desk.len() != 32 || !saved.desk.bytes().all(|b| b.is_ascii_hexdigit()) {
            saved.desk = crate::machine::random();
        }
        #[cfg(target_os = "macos")]
        if crate::mac_app::key(&saved.pages).is_none() {
            saved.pages = crate::machine::random();
        }
        saved
    }

    pub fn write(&self, file: &Path) -> io::Result<()> {
        if let Some(folder) = file.parent() {
            fs::create_dir_all(folder)?;
        }
        let what = serde_json::to_vec_pretty(self)?;
        whole(file, &what)?;
        whole(&second(file), &what)?;
        if self.cookie.is_none() {
            let _ = fs::remove_file(aside(file)); // signed out: no session is left anywhere
        }
        Ok(())
    }
}

fn second(file: &Path) -> PathBuf {
    file.with_extension("copy")
}

fn aside(file: &Path) -> PathBuf {
    file.with_extension("unread")
}

/// All of it is there, or what was there before: another program's own (a second one of this) never mixes with it.
fn whole(file: &Path, what: &[u8]) -> io::Result<()> {
    let fresh = file.with_extension(format!("{}.new", std::process::id()));
    let mut options = fs::OpenOptions::new();
    options.write(true).create(true).truncate(true);
    #[cfg(unix)]
    {
        use std::os::unix::fs::OpenOptionsExt;
        let _ = fs::remove_file(&fresh); // the mode only counts for a new file
        options.mode(0o600);
    }
    let done = options.open(&fresh).and_then(|mut to| {
        io::Write::write_all(&mut to, what)?;
        to.sync_all()
    }).and_then(|()| patient(|| fs::rename(&fresh, file)));
    if done.is_err() {
        let _ = fs::remove_file(&fresh);
    }
    done
}

/// On Windows another program may have the file for a moment (a virus scanner, a backup).
fn patient<T>(what: impl Fn() -> io::Result<T>) -> io::Result<T> {
    for _ in 0..if cfg!(windows) { 20 } else { 0 } {
        match what() {
            Err(error) if error.kind() != io::ErrorKind::NotFound => std::thread::sleep(std::time::Duration::from_millis(50)),
            done => return done,
        }
    }
    what()
}

/// A part that this version doesn't know the shape of (another version wrote it) goes; the rest stays.
fn parsed(file: &Path) -> Option<Saved> {
    let Value::Object(all) = serde_json::from_slice(&patient(|| fs::read(file)).ok()?).ok()? else { return None };
    let fits = |part: (String, Value)| serde_json::from_value::<Saved>(Value::Object([part.clone()].into_iter().collect())).is_ok().then_some(part);
    serde_json::from_value(Value::Object(all.into_iter().filter_map(fits).collect())).ok()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn keeps_and_reads_back_for_the_owner_only() {
        let folder = std::env::temp_dir().join(format!("machine-desktop-{}", std::process::id()));
        let file = folder.join("app.json");
        let mut s = Saved { machine: Some("https://my.example.com/".into()), cookie: Some("a=b".into()), ..Default::default() };
        s.places.insert("DP-1".into(), Corner { right: 1.0, bottom: 2.0 });
        s.write(&file).unwrap();
        s.write(&file).unwrap();
        let read = Saved::read(&file);
        #[cfg(target_os = "macos")]
        let read = Saved { pages: String::new(), ..read };
        assert_eq!(Saved { desk: String::new(), ..read }, s);
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            assert_eq!(fs::metadata(&file).unwrap().permissions().mode() & 0o777, 0o600);
        }
        fs::write(&file, b"not json").unwrap();
        fs::remove_file(second(&file)).unwrap();
        let fresh = Saved::read(&file);
        assert!(fresh.desk.len() == 32 && fresh.desk != Saved::read(&file).desk);
        #[cfg(target_os = "macos")]
        let fresh = Saved { pages: String::new(), ..fresh };
        assert_eq!(Saved { desk: String::new(), ..fresh }, Saved::default());
        fs::remove_dir_all(folder).unwrap();
    }

    fn folder(name: &str) -> PathBuf {
        let folder = std::env::temp_dir().join(format!("machine-desktop-{name}-{}", std::process::id()));
        let _ = fs::remove_dir_all(&folder);
        fs::create_dir_all(&folder).unwrap();
        folder
    }

    fn one() -> Saved {
        Saved { machine: Some("https://my.example.com/".into()), cookie: Some("a=b".into()), quits: true, ..Default::default() }
    }

    #[test]
    fn a_file_that_cant_be_read_is_put_aside_and_its_copy_read() {
        let folder = folder("copy");
        let file = folder.join("app.json");
        one().write(&file).unwrap();
        for broken in [&b""[..], b"{\"machine\": \"https://my.ex", b"\0\0\0\0", b"[]"] {
            fs::write(&file, broken).unwrap();
            let read = Saved::read(&file);
            assert_eq!((read.machine, read.cookie, read.quits), (one().machine, one().cookie, true), "{broken:?}");
            assert_eq!(fs::read(aside(&file)).unwrap(), broken);
            assert!(!file.exists());
        }
        // Both: nothing is lost either
        fs::write(&file, b"half").unwrap();
        fs::write(second(&file), b"half too").unwrap();
        let read = Saved::read(&file);
        assert_eq!(read.machine, None);
        assert_eq!(fs::read(aside(&file)).unwrap(), b"half");
        read.write(&file).unwrap(); // signed out: what was put aside has no session in it any more
        assert!(!aside(&file).exists());
        fs::remove_dir_all(folder).unwrap();
    }

    #[test]
    fn what_another_version_wrote_costs_only_itself() {
        let folder = folder("version");
        let file = folder.join("app.json");
        one().write(&file).unwrap();
        let mut all: Value = serde_json::from_slice(&fs::read(&file).unwrap()).unwrap();
        (all["speak"], all["window"], all["later"]) = ("sometimes".into(), "left".into(), 1.into());
        fs::write(&file, all.to_string()).unwrap();
        let read = Saved::read(&file);
        assert_eq!((read.machine, read.cookie, read.quits, read.speak, read.window), (one().machine, one().cookie, true, Default::default(), None));
        fs::remove_dir_all(folder).unwrap();
    }

    #[test]
    fn two_that_write_at_once_never_leave_half_a_file() {
        let folder = folder("two");
        let file = folder.join("app.json");
        one().write(&file).unwrap();
        let (writes, reads) = (file.clone(), file.clone());
        let writer = std::thread::spawn(move || (0..40).all(|n| Saved { zoom: f64::from(n), ..one() }.write(&writes).is_ok()));
        for _ in 0..200 {
            assert_eq!(parsed(&reads).and_then(|s| s.cookie), one().cookie);
        }
        assert!(writer.join().unwrap());
        assert_eq!(fs::read_dir(&folder).unwrap().count(), 2); // and nothing else
        fs::remove_dir_all(folder).unwrap();
    }

    #[test]
    fn signing_out_leaves_no_session_behind() {
        let folder = folder("out");
        let file = folder.join("app.json");
        one().write(&file).unwrap();
        Saved { machine: None, cookie: None, ..one() }.write(&file).unwrap();
        for left in fs::read_dir(&folder).unwrap() {
            assert!(!fs::read_to_string(left.unwrap().path()).unwrap().contains("a=b"));
        }
        fs::remove_dir_all(folder).unwrap();
    }
}
