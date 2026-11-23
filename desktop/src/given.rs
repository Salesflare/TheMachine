//! What was dropped on the robot or its box, until the box's page has it. It goes nowhere from here but into the box:
//! nothing becomes a to-do or a question before the person says so. The page takes drops itself; only files on Linux come
//! from the system's own drop, as WebKitGTK doesn't give a page those.
use serde::{Deserialize, Serialize};

/// As the box's own limits for + (ui/box.js).
pub const FILES: usize = 5;
const FILE: u64 = 10 << 20;

#[derive(Deserialize, Serialize, Debug, Default, PartialEq)]
pub struct Given {
    pub text: String,
    pub files: Vec<GivenFile>,
    /// A code of the page's words: some of it isn't there.
    pub error: Option<String>,
}

#[derive(Deserialize, Serialize, Debug, PartialEq)]
pub struct GivenFile {
    pub name: String,
    pub kind: String,
    /// base64
    pub data: String,
}

impl Given {
    /// What a page gave, or nothing.
    pub fn within(self) -> Option<Given> {
        let small = self.files.len() <= FILES && self.files.iter().all(|f| f.data.len() as u64 <= FILE.div_ceil(3) * 4);
        small.then(|| Given { text: self.text.chars().take(4000).collect(), ..self })
    }

    #[cfg(target_os = "linux")]
    pub fn read(paths: &[std::path::PathBuf]) -> Given {
        use base64::{engine::general_purpose::STANDARD, Engine};
        use std::io::Read;
        let mut given = Given { error: (paths.len() > FILES).then(|| "files".into()), ..Given::default() };
        for path in paths.iter().take(FILES) {
            let mut data = Vec::new();
            let name = path.file_name().map(|n| n.to_string_lossy().into_owned());
            // Asked before it is opened: a folder, a pipe or a device is never read
            let read = std::fs::metadata(path).is_ok_and(|m| m.is_file())
                && std::fs::File::open(path).and_then(|f| f.take(FILE + 1).read_to_end(&mut data)).is_ok();
            match name {
                Some(name) if read && data.len() as u64 <= FILE => given.files.push(GivenFile { kind: kind(&name).into(), name, data: STANDARD.encode(data) }),
                _ => given.error = Some(if read { "size" } else { "file" }.into()),
            }
        }
        given
    }
}

/// Of the images the box shows; anything else goes by its name.
#[cfg(target_os = "linux")]
fn kind(name: &str) -> &'static str {
    match name.rsplit_once('.').map(|(_, end)| end.to_ascii_lowercase()).as_deref() {
        Some("png") => "image/png",
        Some("jpg" | "jpeg") => "image/jpeg",
        Some("gif") => "image/gif",
        Some("webp") => "image/webp",
        _ => "",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn only_as_much_as_with_plus() {
        let file = |n: usize| GivenFile { name: "a".into(), kind: String::new(), data: "A".repeat(n) };
        assert!(Given { files: vec![file(13_981_016)], ..Given::default() }.within().is_some());
        assert!(Given { files: vec![file(13_981_020)], ..Given::default() }.within().is_none());
        assert!(Given { files: (0..6).map(|_| file(4)).collect(), ..Given::default() }.within().is_none());
        assert_eq!(Given { text: "x".repeat(5000), ..Given::default() }.within().unwrap().text.len(), 4000);
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn files_are_read_and_nothing_else() {
        let dir = std::env::temp_dir().join(format!("given-{}", std::process::id()));
        std::fs::create_dir_all(&dir).unwrap();
        let (one, big) = (dir.join("a & b.PNG"), dir.join("big"));
        std::fs::write(&one, "hi").unwrap();
        std::fs::File::create(&big).unwrap().set_len(FILE + 1).unwrap();
        let got = Given::read(&[one.clone(), dir.clone()]);
        assert_eq!((got.files[0].name.as_str(), got.files[0].kind.as_str(), got.files[0].data.as_str()), ("a & b.PNG", "image/png", "aGk="));
        assert_eq!((got.files.len(), got.error.as_deref()), (1, Some("file")));
        assert_eq!(Given::read(&[big]).error.as_deref(), Some("size"));
        assert_eq!(Given::read(&["/dev/zero".into()]).error.as_deref(), Some("file"));
        let many = Given::read(&vec![one; 6]);
        assert_eq!((many.files.len(), many.error.as_deref()), (5, Some("files")));
        std::fs::remove_dir_all(&dir).unwrap();
    }
}
