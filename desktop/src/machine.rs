//! Talking to the person's own Machine, as the phone app's notification buttons do: api/session for the token, then
//! api/action with the Machine's own Origin. The Machine decides who its owner is. Only the actions named here are
//! ever called: a new to-do and its files, a question, and the quick buttons of a to-do's notification (QUICK), which the
//! Machine only takes for that. None of them sends or approves anything.
use crate::address;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::path::{Path, PathBuf};
use std::time::Duration;
use url::Url;

/// Error codes the box has its own words for (ui/strings.js); anything else is the Machine's own sentence.
const UNREACHABLE: &str = "unreachable";
const NOT_OWNER: &str = "notowner";
/// How many to-dos the box lists.
const LISTED: usize = 3;

/// A Machine's address, and a hosted one's session.
#[derive(Clone)]
pub struct Machine {
    pub url: String,
    pub cookie: Option<String>,
}

/// The quick buttons of a to-do's notification that do something (PushText in the phone app): the Machine's name for each,
/// its choice and, for a snooze, until when, where the to-do names no choices of its own (an older Machine). Its others
/// (open, the draft, an answer, signing in) open the to-do, as its row does.
const QUICK: [(&str, &str, Option<&str>); 4] =
    [("prepare", "accept", None), ("snooze", "snooze", Some("tomorrow")), ("snooze2h", "snooze", Some("2h")), ("done", "complete", None)];

/// Those that only open the to-do, where the rest is done.
const OPENS: [&str; 4] = ["open", "draft", "answer", "signin"];

/// A quick button, in the Machine's words: its name, and what happened after.
#[derive(Clone, Serialize, Debug, PartialEq)]
pub struct Quick {
    act: &'static str,
    name: String,
    said: String,
}

/// One of them: what the dashboard calls its state, whether the Machine is on it, and the choices of its Snooze (option,
/// words). No id: a Fleet item, or a board's follow-ups.
#[derive(Clone, Serialize, Deserialize, Debug, PartialEq)]
pub struct Todo {
    pub id: Option<String>,
    pub title: String,
    #[serde(default)]
    pub state: String,
    #[serde(default)]
    pub working: bool,
    #[serde(default)]
    pub snooze: Vec<(String, String)>,
}

/// One that was just added in the box, and whether it is in For you.
#[derive(Clone, Serialize, Deserialize, Debug, PartialEq)]
pub struct Added {
    pub id: String,
    pub title: String,
    pub state: String,
    pub working: bool,
    #[serde(default)]
    pub snooze: Vec<(String, String)>,
    pub listed: bool,
}

#[derive(Clone, Serialize, Debug, Default, PartialEq)]
pub struct Waiting {
    pub todos: Vec<Todo>,
    pub added: Vec<Added>,
    pub count: usize,
    /// The owner's first name, as the Machine gave it; '' when it gave none.
    pub name: String,
    /// Its times are 12-hour ones.
    pub hour12: bool,
    /// The Machine said what is there: none is none.
    pub known: bool,
}

/// The account names the computer by its system (Account, Security).
fn user_agent() -> String {
    format!("TheMachineDesktop/{} ({})", env!("CARGO_PKG_VERSION"), std::env::consts::OS)
}

fn agent(seconds: u64) -> ureq::Agent {
    let config = ureq::Agent::config_builder()
        .timeout_global(Some(Duration::from_secs(seconds)))
        .max_redirects(0) // a Machine never sends the app elsewhere
        .http_status_as_error(false)
        .user_agent(user_agent());
    #[cfg(feature = "sandbox")]
    let config = match made_up() {
        Some(tls) => config.tls_config(tls),
        None => config,
    };
    config.build().into()
}

/// For smoke/: the one certificate a sandbox build checks a made-up Machine's against, instead of the known ones. No other
/// build has this.
#[cfg(feature = "sandbox")]
fn made_up() -> Option<ureq::tls::TlsConfig> {
    use ureq::tls::{Certificate, RootCerts, TlsConfig};
    let root = Certificate::from_pem(&std::fs::read(std::env::var_os("MACHINE_SANDBOX_ROOT")?).ok()?).ok()?;
    Some(TlsConfig::builder().root_certs(RootCerts::new_with_certs(&[root])).build())
}

/// What an answer that isn't a 200 means: it doesn't take this computer as its owner's, or it isn't there (a proxy in
/// front of it says so).
fn refused(status: u16) -> String {
    if (300..500).contains(&status) { NOT_OWNER.into() } else { UNREACHABLE.into() }
}

fn read(mut answer: ureq::http::Response<ureq::Body>) -> (u16, Value) {
    let status = answer.status().as_u16();
    let body = answer.body_mut().with_config().limit(32 << 20).read_json().unwrap_or(Value::Null);
    (status, body)
}

/// Redeems a hosted sign-in (its address has the verifier): the session cookies it answers with.
pub fn redeem(auth: &str) -> Result<String, String> {
    let answer = agent(20).get(auth).call().map_err(|_| UNREACHABLE)?;
    let cookies: Vec<String> = answer.headers().get_all("set-cookie").iter()
        .filter_map(|c| c.to_str().ok()?.split(';').next().map(str::trim).map(String::from))
        .filter(|c| c.split_once('=').is_some_and(|(_, v)| !v.is_empty()))
        .collect();
    if cookies.is_empty() { Err("signin".into()) } else { Ok(cookies.join("; ")) }
}

impl Machine {
    fn get(&self, path: &str) -> Result<(u16, Value), String> {
        let mut request = agent(20).get(format!("{}{path}", self.url));
        if let Some(cookie) = &self.cookie {
            request = request.header("Cookie", cookie);
        }
        request.call().map(read).map_err(|_| UNREACHABLE.to_string())
    }

    /// One of its files, kept in this folder. Its name there; the name it would have had, when that didn't work.
    pub fn save(&self, url: &Url, folder: &Path) -> Result<PathBuf, String> {
        let last = url.path_segments().and_then(|mut s| s.next_back()).unwrap_or_default().to_string();
        let own = url.as_str().strip_prefix(&self.url).is_some_and(|path| path.starts_with("api/"));
        let mut request = agent(300).get(url.as_str());
        if let Some(cookie) = &self.cookie {
            request = request.header("Cookie", cookie);
        }
        let mut answer = own.then(|| request.call().ok()).flatten().filter(|a| a.status() == 200).ok_or_else(|| last.clone())?;
        let named = answer.headers().get("content-disposition").and_then(|h| h.to_str().ok()).and_then(file_name);
        let file = crate::files::free(folder, &named.unwrap_or_else(|| last.clone()));
        let name = file.file_name().map(|n| n.to_string_lossy().into_owned()).unwrap_or_default();
        let kept = std::fs::File::create_new(&file).and_then(|mut to| std::io::copy(&mut answer.body_mut().as_reader(), &mut to));
        match kept {
            Ok(_) => Ok(file),
            Err(_) => {
                let _ = std::fs::remove_file(&file);
                Err(name)
            }
        }
    }

    fn csrf(&self) -> Result<String, String> {
        let (status, session) = self.get("api/session")?;
        match (status, session["csrf"].as_str()) {
            (200, Some(token)) => Ok(token.into()),
            (200, None) => Err(NOT_OWNER.into()),
            _ => Err(refused(status)),
        }
    }

    /// Whether a Machine answers here, and takes this computer as its owner's.
    pub fn check(&self) -> Result<(), String> {
        let (status, body) = self.get("manifest.webmanifest")?;
        if !address::is_machine(status, &body) {
            return Err("notmachine".into());
        }
        self.csrf().map(|_| ())
    }

    /// Whether no other Machine answers at this one's host, beside its path. None: it can't be told now.
    pub fn alone(&self) -> Option<bool> {
        let host = Machine { url: format!("{}/", address::origin(&self.url)), cookie: None };
        if host.url == self.url {
            return Some(true);
        }
        let (status, body) = host.get("manifest.webmanifest").ok()?;
        Some(!address::is_machine(status, &body))
    }

    fn action(&self, name: &str, args: Value, upload: bool, seconds: u64) -> Result<Value, String> {
        let mut request = agent(seconds)
            .post(format!("{}api/action", self.url))
            .header("Origin", address::origin(&self.url))
            .header("X-CSRF-Token", self.csrf()?);
        if let Some(cookie) = &self.cookie {
            request = request.header("Cookie", cookie);
        }
        if upload {
            request = request.header("X-Upload", "chat-file");
        }
        let (status, body) = request.send_json(json!({"action": name, "args": args})).map(read).map_err(|_| UNREACHABLE)?;
        match status {
            200 => Ok(body),
            _ => Err(body["error"].as_str().unwrap_or("failed").chars().take(300).collect()),
        }
    }

    pub fn add_todo(&self, text: &str, draft: &str, files: &[String]) -> Result<Value, String> {
        let mut args = json!({"text": text});
        if !files.is_empty() {
            args["draft"] = json!(draft);
            args["files"] = json!(files);
        }
        self.action("card_new", args, false, 30)
    }

    pub fn add_file(&self, draft: &str, name: &str, data: &str) -> Result<Value, String> {
        self.action("chat_upload", json!({"draft": draft, "name": name, "data": data}), true, 90)
    }

    pub fn remove_file(&self, draft: &str, id: &str) -> Result<Value, String> {
        self.action("chat_file_remove", json!({"draft": draft, "id": id}), false, 30)
    }

    /// The quick buttons of this to-do's notification, as it is now. An older Machine names none.
    pub fn quick(&self, todo: &str) -> Result<Vec<Quick>, String> {
        let (status, notice) = self.get(&format!("api/notice?v=2&tag={todo}"))?;
        Ok(if status == 200 { quick(&notice) } else { Vec::new() })
    }

    /// `until`: one of the to-do's own Snooze choices. The Machine takes only those.
    pub fn decide(&self, todo: &str, act: &str, until: Option<&str>) -> Result<Value, String> {
        let (_, choice, usual) = QUICK.iter().find(|(name, ..)| *name == act).ok_or("failed")?;
        let plain = |o: &&str| *choice == "snooze" && (1..=20).contains(&o.len()) && o.bytes().all(|b| b.is_ascii_alphanumeric());
        let until = match until {
            Some(option) => Some(Some(option).filter(plain).ok_or("failed")?),
            None => *usual,
        };
        let mut args = json!({"suggestion_id": todo, "choice": choice, "feedback": "", "decision_id": format!("notify-{}", uuid())});
        if let Some(until) = until {
            args["snooze_option"] = json!(until);
        }
        self.action("decide", args, false, 30)
    }

    /// Takes back Mark done, or Snooze, as the dashboard's Undo does.
    pub fn undo(&self, todo: &str, act: &str) -> Result<Value, String> {
        let choice = match act {
            "done" => "undo",
            "snooze" | "snooze2h" => "accept", // on a snoozed to-do: back where it was
            _ => return Err("failed".into()),
        };
        self.action("decide", json!({"suggestion_id": todo, "choice": choice, "feedback": "", "decision_id": uuid()}), false, 30)
    }

    /// Whether its dashboard has the compact page of one to-do (card.rs).
    pub fn compact(&self) -> bool {
        self.get("api/session").is_ok_and(|(status, session)| status == 200 && session["compact"] == 1)
    }

    pub fn ask(&self, text: &str) -> Result<Value, String> {
        self.action("search_ask", json!({"query": text}), false, 120)
    }

    /// What this to-do's notification says now, and its buttons, as the phone app asks it. None: it no longer waits.
    pub fn notice(&self, todo: &str, kind: &str) -> Result<Option<crate::speak::Say>, String> {
        let plain = |s: &str| !s.is_empty() && s.len() <= 64 && s.bytes().all(|b| b.is_ascii_alphanumeric());
        if !plain(todo) {
            return Ok(None);
        }
        let kind = if plain(kind) { format!("&kind={kind}") } else { String::new() };
        let (status, notice) = self.get(&format!("api/notice?v=2&tag={todo}{kind}"))?;
        told(status, todo, &notice)
    }

    /// What the dashboard's list is made of: its status (with a token of an earlier one, what changed since) and, when
    /// that asks for it, the Fleet's items. `look`: this is no one opening the dashboard.
    /// `desk`: this robot's name, and whether it may speak, and what it got the time before (speak.rs).
    /// `none`: the browsers there up to then aren't on this computer (saved.rs).
    pub fn status(&self, since: Option<&str>, desk: &str, up: bool, got: &[String], none: u64) -> Result<Value, String> {
        let since = since.filter(|t| t.bytes().all(|b| b.is_ascii_alphanumeric() || b"-_".contains(&b)));
        let on = if cfg!(target_os = "macos") { "mac" } else { std::env::consts::OS };
        self.page(&format!("api/status?look=1&desk={desk}&on={on}&none={none}&up={}&got={}{}", u8::from(up), got.join(","), since.map(|t| format!("&since={t}")).unwrap_or_default()))
    }

    pub fn fleet(&self) -> Result<Value, String> {
        self.page("api/fleet")
    }

    fn page(&self, path: &str) -> Result<Value, String> {
        match self.get(path)? {
            (200, body) if body.is_object() => Ok(body),
            (200, _) => Err(UNREACHABLE.into()),
            (status, _) => Err(refused(status)),
        }
    }
}

/// The name in a Content-Disposition, as a Machine writes it: filename*=UTF-8''<percent-encoded>, or filename="...".
pub fn file_name(header: &str) -> Option<String> {
    let part = |name: &str| header.split(';').find_map(|p| p.trim().strip_prefix(name)).map(str::trim);
    let encoded = part("filename*=UTF-8''").map(|n| format!("n={}", n.replace('+', "%2B").replace('&', "%26")));
    let decoded = encoded.and_then(|n| url::form_urlencoded::parse(n.as_bytes()).next().map(|(_, v)| v.into_owned()));
    decoded.or_else(|| part("filename=").map(|n| n.trim_matches('"').to_string())).filter(|n| !n.is_empty())
}

fn quick(notice: &Value) -> Vec<Quick> {
    let words = |part: &str, act: &str| notice[part][act].as_str().map(|w| w.chars().take(60).collect::<String>());
    notice["actions"].as_array().into_iter().flatten()
        .filter_map(|a| QUICK.iter().find(|(name, ..)| a == name))
        .filter_map(|(act, ..)| Some(Quick { act, name: words("labels", act)?, said: words("events", act)? }))
        .take(3)
        .collect()
}

/// Gone is what the Machine says is gone. Anything else it doesn't say is asked again.
fn told(status: u16, todo: &str, notice: &Value) -> Result<Option<crate::speak::Say>, String> {
    match status {
        200 if notice["gone"] == true => Ok(None),
        200 => said(todo, notice).map(Some).ok_or_else(|| UNREACHABLE.into()),
        status => Err(refused(status)),
    }
}

/// The notification, as a bubble. Its first button that only opens names the one that does.
fn said(todo: &str, notice: &Value) -> Option<crate::speak::Say> {
    let words = |v: &Value, most: usize| v.as_str().map(|w| w.split_whitespace().collect::<Vec<_>>().join(" ").chars().take(most).collect::<String>()).filter(|w| !w.is_empty());
    let opens = notice["actions"].as_array().into_iter().flatten().filter_map(Value::as_str).find(|a| OPENS.contains(a)).unwrap_or("open");
    Some(crate::speak::Say {
        id: todo.into(),
        title: words(&notice["title"], 160)?,
        line: words(&notice["body"], 200).unwrap_or_default(),
        opens: words(&notice["labels"][opens], 30).unwrap_or_else(|| "Open".into()),
        quick: quick(notice),
        ..Default::default()
    })
}

/// 32 hex digits.
pub fn random() -> String {
    uuid().replace('-', "")
}

fn uuid() -> String {
    let mut b = [0u8; 16];
    getrandom::fill(&mut b).expect("the system has random numbers");
    (b[6], b[8]) = (b[6] & 0x0f | 0x40, b[8] & 0x3f | 0x80);
    let hex: Vec<String> = b.iter().map(|b| format!("{b:02x}")).collect();
    [&hex[..4], &hex[4..6], &hex[6..8], &hex[8..10], &hex[10..]].map(|p| p.concat()).join("-")
}

/// What the robot's page made of it (ui/list.js): the first of the dashboard's For you, and how many there are.
impl Waiting {
    pub fn of(todos: Vec<Todo>, count: usize, name: &str, added: Vec<Added>) -> Waiting {
        let cut = |t: Todo| Todo { title: t.title.chars().take(200).collect(), ..t };
        let count = count.max(todos.len());
        Waiting {
            todos: todos.into_iter().take(LISTED).map(cut).collect(),
            added: added.into_iter().map(|a| Added { title: a.title.chars().take(200).collect(), ..a }).collect(),
            count,
            name: name.trim().chars().filter(|c| !c.is_control()).take(40).collect(),
            known: true,
            hour12: false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_says_its_version_and_its_system() {
        let version = concat!("TheMachineDesktop/", env!("CARGO_PKG_VERSION"));
        assert!(["windows", "macos", "linux"].map(|os| format!("{version} ({os})")).contains(&user_agent()));
        assert!(user_agent().ends_with(if cfg!(windows) { "(windows)" } else if cfg!(target_os = "macos") { "(macos)" } else { "(linux)" }));
    }

    #[test]
    fn a_files_own_name() {
        assert_eq!(file_name("inline; filename*=UTF-8''Plan%20B%20%26%20c%2B%2B.pdf").as_deref(), Some("Plan B & c++.pdf"));
        assert_eq!(file_name("attachment; filename=\"plan.pdf\"; filename*=UTF-8''pl%C3%A1n.pdf").as_deref(), Some("plán.pdf"));
        assert_eq!([file_name("attachment; filename=\"plan.pdf\"").as_deref(), file_name("inline").as_deref(), file_name("attachment; filename=").as_deref()], [Some("plan.pdf"), None, None]);
    }

    #[test]
    fn the_first_three_and_how_many() {
        let todos: Vec<Todo> = (0..5).map(|i| Todo { id: Some(i.to_string()), title: "é".repeat(300), state: "Needs you".into(), working: false, snooze: vec![] }).collect();
        let w = Waiting::of(todos, 9, " Sam\n", vec![]);
        assert_eq!((w.todos.len(), w.count, w.todos[0].title.chars().count()), (3, 9, 200));
        assert_eq!((w.name.as_str(), w.known), ("Sam", true));
        assert_eq!((Waiting::of(vec![], 0, "", vec![]).count, Waiting::of(vec![], 0, &"x".repeat(60), vec![]).name.len()), (0, 40));
        assert!(!Waiting::default().known);
    }

    #[test]
    fn the_notifications_buttons_without_the_ones_that_open() {
        let notice = json!({
            "actions": ["draft", "snooze2h", "send", "done", "approve"],
            "labels": {"draft": "See draft", "snooze2h": "Snooze", "done": "Mark done", "send": "Send"},
            "events": {"snooze2h": "Snoozed it", "done": "Marked it done", "send": "Sent"},
        });
        let acts: Vec<_> = quick(&notice).into_iter().map(|q| (q.act, q.name)).collect();
        assert_eq!(acts, [("snooze2h", "Snooze".into()), ("done", "Mark done".into())]);
        assert!(quick(&json!({"gone": true})).is_empty() && quick(&Value::Null).is_empty());
        let m = Machine { url: "http://127.0.0.1:9/".into(), cookie: None };
        assert_eq!((m.decide("a", "send", None), m.undo("a", "prepare")), (Err("failed".into()), Err("failed".into())));
        for (act, until) in [("done", "tomorrow"), ("prepare", "2h"), ("snooze", ""), ("snooze", "2h&x"), ("snooze", "2026-11-24T09:00")] {
            assert_eq!(m.decide("a", act, Some(until)), Err("failed".into()), "{act} {until}");
        }
        let id = uuid();
        assert!(id.len() == 36 && &id[14..15] == "4" && id != uuid(), "{id}");
    }

    #[test]
    fn a_notification_as_a_bubble() {
        let notice = json!({"title": "Ready: Reply to\n Dana", "body": "Hi.", "actions": ["draft", "snooze2h", "done"],
            "labels": {"open": "Open", "draft": "Open draft", "snooze2h": "Snooze", "done": "Mark done"}, "events": {"snooze2h": "Snoozed it", "done": "Marked it done"}});
        let say = said("a1", &notice).unwrap();
        assert_eq!((say.title.as_str(), say.opens.as_str(), say.quick.len()), ("Ready: Reply to Dana", "Open draft", 2));
        assert!(said("a1", &json!({"gone": true})).is_none());
        assert_eq!(told(200, "a1", &notice), Ok(Some(say)));
        assert_eq!(told(200, "a1", &json!({"gone": true})), Ok(None));
        for (status, answer) in [(500, Value::Null), (502, json!({"gone": true})), (403, json!({"error": "x"})), (200, Value::Null), (200, json!({"body": "x"}))] {
            assert!(told(status, "a1", &answer).is_err(), "{status} {answer}: not gone, asked again");
        }
        assert_eq!(said("a1", &json!({"title": "T", "actions": ["prepare"]})).unwrap().opens, "Open");
        assert_eq!(random().len(), 32);
    }

    #[test]
    fn nothing_in_an_odd_answer() {
        assert_eq!([302, 401, 403].map(refused), [NOT_OWNER; 3]);
        assert_eq!([502, 503].map(refused), [UNREACHABLE; 2]);
    }
}
