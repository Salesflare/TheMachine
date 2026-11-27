//! The app's own link, computer.themachine.desktop://open: a page opens it to bring this app to the front, as starting it
//! again does. It carries nothing, no command and no data: only exactly that link counts, and any other one of this
//! scheme (with a path, a query or a fragment) does nothing at all. Not the sign-in's computer.themachine.app://, which
//! the phone app shares and which is only taken while a sign-in runs (signin.rs).
pub const SCHEME: &str = "computer.themachine.desktop";

/// Whether `link` is exactly the open link. Windows may add a slash.
pub fn open(link: &str) -> bool {
    matches!(link, "computer.themachine.desktop://open" | "computer.themachine.desktop://open/")
}

/// Whether `link` is of this scheme at all (then only `open` may do something).
pub fn ours(link: &str) -> bool {
    link.get(..SCHEME.len() + 1).is_some_and(|s| s.eq_ignore_ascii_case(&format!("{SCHEME}:")))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn only_the_open_link_opens() {
        assert!(open("computer.themachine.desktop://open"));
        assert!(open("computer.themachine.desktop://open/"));
        for other in [
            "computer.themachine.desktop://open?to=x",
            "computer.themachine.desktop://open#x",
            "computer.themachine.desktop://open/x",
            "computer.themachine.desktop://quit",
            "computer.themachine.desktop://",
            "computer.themachine.desktop:open",
            "computer.themachine.desktop://open ",
            "computer.themachine.app://open",
            "computer.themachine.app://signed-in?u=x",
            "https://computer.themachine.desktop/open",
            "--quit",
            "",
        ] {
            assert!(!open(other), "{other}");
        }
    }

    #[test]
    fn its_scheme_is_told_apart_from_the_sign_ins() {
        assert!(SCHEME != crate::signin::SCHEME);
        assert!(ours("computer.themachine.desktop://open?to=x"));
        assert!(ours("COMPUTER.THEMACHINE.DESKTOP://x"));
        assert!(!ours("computer.themachine.app://signed-in?u=x"));
        assert!(!ours("computer.themachine.desktopx://open"));
        assert!(!ours("--toggle"));
        assert!(!ours("ü"));
    }
}
