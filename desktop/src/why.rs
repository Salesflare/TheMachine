//! Why it speaks or doesn't, in a small file next to app.json: one line per change, with the time (UTC) and a reason.
//! Reasons only, never whose to-do it is or what it says: every line here is one of the program's own.
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::Path;
use std::sync::Mutex;
use std::time::{SystemTime, UNIX_EPOCH};

pub const NAME: &str = "speaks.log";
/// Past this the older half goes.
const MOST: u64 = 64 * 1024;

static ONE: Mutex<()> = Mutex::new(());

pub fn note(file: &Path, reason: &str) {
    let _one = ONE.lock().unwrap_or_else(|e| e.into_inner());
    if fs::metadata(file).is_ok_and(|m| m.len() > MOST) {
        if let Ok(all) = fs::read_to_string(file) {
            let half = all.char_indices().map(|(i, _)| i).find(|i| *i >= all.len() / 2).unwrap_or(0);
            let _ = fs::write(file, all[half..].split_once('\n').map_or("", |(_, rest)| rest));
        }
    }
    let seconds = SystemTime::now().duration_since(UNIX_EPOCH).map_or(0, |d| d.as_secs());
    let _ = file.parent().map(fs::create_dir_all); // the very first start may hang before anything is kept
    if let Ok(mut out) = OpenOptions::new().create(true).append(true).open(file) {
        let _ = writeln!(out, "{} {reason}", at(seconds));
    }
}

/// "2026-11-24 13:42:07" in UTC.
fn at(seconds: u64) -> String {
    let (days, s) = ((seconds / 86400) as i64, seconds % 86400);
    // Days to a date, counted in years that start in March (Howard Hinnant's civil_from_days)
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let (d, m) = (doy - (153 * mp + 2) / 5 + 1, if mp < 10 { mp + 3 } else { mp - 9 });
    let y = yoe + era * 400 + i64::from(m <= 2);
    format!("{y:04}-{m:02}-{d:02} {:02}:{:02}:{:02}", s / 3600, s / 60 % 60, s % 60)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_time() {
        assert_eq!(at(0), "1970-01-01 00:00:00");
        assert_eq!(at(951_782_399), "2000-02-28 23:59:59");
        assert_eq!(at(951_782_400), "2000-02-29 00:00:00");
        assert_eq!(at(1_795_527_727), "2026-11-24 13:42:07");
    }

    #[test]
    fn it_stays_small_and_keeps_the_newest() {
        let file = std::env::temp_dir().join(format!("why-{}-{NAME}", std::process::id()));
        let _ = fs::remove_file(&file);
        for i in 0..3000 {
            note(&file, &format!("may not speak: full screen {i}"));
        }
        let all = fs::read_to_string(&file).unwrap();
        let _ = fs::remove_file(&file);
        assert!(all.len() as u64 <= MOST + 100, "{}", all.len());
        assert!(all.ends_with("full screen 2999\n"));
        assert!(all.lines().all(|l| l.starts_with("20") && l.contains(" may not speak: ")));
    }
}
