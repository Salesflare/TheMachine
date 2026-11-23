//! What the dot means: something is new in For you since the box, or the dashboard's app on this computer, was last open.
//! It keeps what was there then, as fingerprints: what a to-do is called or about is not in them.
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;

/// An entry of For you, as the robot's page made it (ui/list.js): its name (its id, and since when it is there) and its
/// marks, one bit each: it is there, its result is ready, it needs the person, it is due. A new mark is news too.
pub type Mark = (String, u8);
pub type Seen = BTreeMap<String, u8>;

fn fingerprint(machine: &str, name: &str) -> String {
    Sha256::digest(format!("{machine}\n{name}"))[..8].iter().map(|b| format!("{b:02x}")).collect()
}

/// What is there now, to keep when the person looks.
pub fn now(machine: &str, marks: &[Mark]) -> Seen {
    marks.iter().take(2000).map(|(name, bits)| (fingerprint(machine, name), bits | 1)).collect()
}

/// Whether there is news. What went is forgotten: when it comes back, it is news again.
pub fn news(seen: &mut Seen, now: &Seen) -> bool {
    seen.retain(|name, bits| now.get(name).is_some_and(|n| {
        *bits &= n;
        true
    }));
    now.iter().any(|(name, bits)| bits & !seen.get(name).copied().unwrap_or(0) != 0)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn marks(all: &[(&str, u8)]) -> Seen {
        now("https://my.example.com/", &all.iter().map(|(n, b)| (n.to_string(), *b)).collect::<Vec<_>>())
    }

    #[test]
    fn news_is_what_was_not_there() {
        let mut seen = marks(&[("a", 1), ("b", 3)]);
        assert!(!news(&mut seen, &marks(&[("a", 1), ("b", 3)])));
        assert!(!news(&mut seen, &marks(&[("a", 1)]))); // one went
        assert!(news(&mut seen, &marks(&[("a", 1), ("b", 3)]))); // and came back
        let mut seen = marks(&[("a", 1), ("b", 3)]);
        assert!(news(&mut seen, &marks(&[("a", 3), ("b", 3)]))); // a's result became ready
        assert!(news(&mut seen, &marks(&[("a", 9), ("b", 3)]))); // a became due
        assert!(!news(&mut seen, &marks(&[("a", 1), ("b", 1)]))); // b was sent back
        assert!(news(&mut seen, &marks(&[("a", 1), ("b", 3)]))); // and is ready again
        assert!(news(&mut Seen::new(), &marks(&[("a", 1)])) && !news(&mut Seen::new(), &Seen::new()));
    }

    #[test]
    fn only_fingerprints() {
        let a = now("https://my.example.com/", &[("a1b2@2026".into(), 0)]);
        assert!(a.keys().all(|k| k.len() == 16 && !k.contains("a1b2")) && a.values().all(|b| *b == 1));
        assert_ne!(a, now("https://other.example.com/", &[("a1b2@2026".into(), 0)]));
    }
}
