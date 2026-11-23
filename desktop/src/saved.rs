//! What the app keeps: the Machine's address, a hosted Machine's session, and where the robot stands. One file only its
//! owner can read (0600; on Windows it is in the person's own profile folder). Of the Machine itself only fingerprints of
//! what was in For you (seen.rs).
use crate::place::Corner;
use serde::{Deserialize, Serialize};
use std::{collections::BTreeMap, fs, io, path::Path};

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
}

impl Saved {
    pub fn read(file: &Path) -> Saved {
        fs::read(file).ok().and_then(|b| serde_json::from_slice(&b).ok()).unwrap_or_default()
    }

    pub fn write(&self, file: &Path) -> io::Result<()> {
        if let Some(folder) = file.parent() {
            fs::create_dir_all(folder)?;
        }
        let fresh = file.with_extension("new");
        let mut options = fs::OpenOptions::new();
        options.write(true).create(true).truncate(true);
        #[cfg(unix)]
        {
            use std::os::unix::fs::OpenOptionsExt;
            let _ = fs::remove_file(&fresh); // the mode only counts for a new file
            options.mode(0o600);
        }
        io::Write::write_all(&mut options.open(&fresh)?, &serde_json::to_vec_pretty(self)?)?;
        fs::rename(fresh, file)
    }
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
        assert_eq!(Saved::read(&file), s);
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            assert_eq!(fs::metadata(&file).unwrap().permissions().mode() & 0o777, 0o600);
        }
        fs::write(&file, b"not json").unwrap();
        assert_eq!(Saved::read(&file), Saved::default());
        fs::remove_dir_all(folder).unwrap();
    }
}
