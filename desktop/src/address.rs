//! Which addresses the app takes as "your Machine": the phone app's rules (mobile/www/machine-url.js), for a self-hosted
//! Machine. A hosted one is never typed: it comes through the account's sign-in (signin.rs).
use url::{Host, Url};

pub const HOSTED: &str = "app.themachine.computer";

/// A hosted Machine's own host: one name under app.themachine.computer.
pub fn hosted_host(host: &str) -> bool {
    host.strip_suffix(HOSTED).and_then(|h| h.strip_suffix('.')).is_some_and(label)
}

fn label(s: &str) -> bool {
    !s.is_empty()
        && s.len() <= 63
        && s.bytes().all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
        && !s.starts_with('-')
        && !s.ends_with('-')
}

fn own_host(host: &str) -> bool {
    let parts: Vec<&str> = host.split('.').collect();
    if host.len() > 253 || !parts.iter().all(|p| label(p)) {
        return false;
    }
    if host.ends_with(".ts.net") {
        return parts.len() >= 4;
    }
    let top = parts[parts.len() - 1];
    parts.len() >= 2
        && (2..=63).contains(&top.len())
        && top.bytes().all(|b| b.is_ascii_lowercase())
        && host != HOSTED
        && !host.ends_with(".app.themachine.computer")
}

fn path(url: &Url) -> Option<String> {
    let mut path = url.path().to_string();
    if !path.ends_with('/') {
        path.push('/');
    }
    let fine = path == "/"
        || path[1..path.len() - 1]
            .split('/')
            .all(|p| !p.is_empty() && p.bytes().all(|b| b.is_ascii_alphanumeric() || b"._~-".contains(&b)));
    fine.then_some(path)
}

/// What the person typed as their Machine's address, in its normal form, or None.
pub fn parse(input: &str) -> Option<String> {
    let text = input.trim();
    if text.is_empty() {
        return None;
    }
    let url = Url::parse(&if text.contains("://") { text.to_string() } else { format!("https://{text}") }).ok()?;
    if !url.username().is_empty() || url.password().is_some() {
        return None;
    }
    if cfg!(feature = "sandbox") && url.scheme() == "http" && url.host_str() == Some("127.0.0.1") {
        return Some(format!("http://127.0.0.1:{}/", url.port()?));
    }
    if url.scheme() != "https" || !matches!(url.port(), None | Some(8443)) {
        return None;
    }
    let host = match url.host()? {
        Host::Domain(d) => d.to_lowercase(),
        _ => return None,
    };
    if !own_host(&host) {
        return None;
    }
    let port = url.port().map(|p| format!(":{p}")).unwrap_or_default();
    Some(format!("https://{host}{port}{}", path(&url)?))
}

/// A link that joins a call of a service the Machine knows (its meet.video_link found it): on that service's own host.
pub fn call(link: &str) -> bool {
    const HOSTS: [&str; 4] = ["zoom.us", "meet.google.com", "teams.microsoft.com", "teams.live.com"];
    Url::parse(link).is_ok_and(|url| {
        let host = url.host_str().unwrap_or_default();
        let own = HOSTS.iter().any(|h| host == *h || host.strip_suffix(h).is_some_and(|sub| sub.ends_with('.')));
        own && link.len() <= 2000 && url.scheme() == "https" && url.port().is_none() && url.username().is_empty() && url.password().is_none()
    })
}

/// The Origin of a Machine's address, which its actions ask for.
pub fn origin(machine: &str) -> String {
    Url::parse(machine).map(|u| u.origin().ascii_serialization()).unwrap_or_default()
}

/// Whether what <address>manifest.webmanifest answered is a Machine's dashboard (isMachine in machine-url.js).
pub fn is_machine(status: u16, body: &serde_json::Value) -> bool {
    match status {
        200 => body["name"] == "The Machine" && body["start_url"].is_string() && body["icons"].is_array(),
        403 => body["error"] == "Use the owner-authenticated Tailscale dashboard",
        _ => false,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn takes_a_machine() {
        for (typed, url) in [
            ("box.tail1234.ts.net", "https://box.tail1234.ts.net/"),
            ("https://Box.tail1234.ts.net:8443/assistant", "https://box.tail1234.ts.net:8443/assistant/"),
            (" my.example.com ", "https://my.example.com/"),
        ] {
            assert_eq!(parse(typed).as_deref(), Some(url), "{typed}");
        }
    }

    #[test]
    fn refuses_the_rest() {
        for typed in [
            "", "localhost", "192.168.1.4", "http://my.example.com", "https://my.example.com:9000", "https://a:b@my.example.com",
            "box.ts.net", "app.themachine.computer", "name.app.themachine.computer", "https://my.example.com/a%20b", "javascript://my.example.com",
            "https://[::1]/", "ftp://my.example.com", "https://-a.example.com",
        ] {
            assert_eq!(parse(typed), None, "{typed}");
        }
    }

    #[test]
    fn sandbox_only_with_its_feature() {
        assert_eq!(parse("http://127.0.0.1:8870").is_some(), cfg!(feature = "sandbox"));
        assert_eq!(parse("http://10.0.0.1:8870"), None);
    }

    #[test]
    fn knows_a_machine() {
        assert!(is_machine(200, &json!({"name": "The Machine", "start_url": ".", "icons": []})));
        assert!(is_machine(403, &json!({"error": "Use the owner-authenticated Tailscale dashboard"})));
        assert!(!is_machine(200, &json!({"name": "Something else", "start_url": ".", "icons": []})));
        assert!(!is_machine(404, &json!({"name": "The Machine", "start_url": ".", "icons": []})));
    }

    #[test]
    fn a_call_is_on_its_service() {
        for link in ["https://zoom.us/j/1", "https://us02web.zoom.us/j/1?pwd=x", "https://meet.google.com/abc-defg-hij", "https://teams.microsoft.com/l/meetup-join/x"] {
            assert!(call(link), "{link}");
        }
        for link in ["http://zoom.us/j/1", "https://zoom.us.example.com/j/1", "https://notzoom.us/j/1", "https://a@zoom.us/j/1", "https://zoom.us:8443/j/1", "javascript:1", "file:///etc", ""] {
            assert!(!call(link), "{link}");
        }
    }

    #[test]
    fn origin_has_no_path() {
        assert_eq!(origin("https://my.example.com:8443/assistant/"), "https://my.example.com:8443");
        assert_eq!(origin("https://my.example.com/"), "https://my.example.com");
    }
}
