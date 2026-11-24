//! The account's app sign-in, as the phone app does it (mobile/): the person signs in in their own browser, at
//! /open?to=app&c=<challenge>, and the browser comes back on computer.themachine.app:// with a token that is only worth
//! something together with the verifier kept here. No password, passkey or code is ever typed into this app.
use crate::address;
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine};
use sha2::{Digest, Sha256};
use std::time::{Duration, Instant};
use url::Url;

pub const SCHEME: &str = "computer.themachine.app";
const LASTS: Duration = Duration::from_secs(15 * 60);

pub struct Pending {
    verifier: String,
    since: Instant,
}

#[derive(Debug, PartialEq)]
pub enum Back {
    /// A hosted Machine: its sign-in address, with the verifier, and the Machine's own.
    Hosted { auth: String, machine: String },
    /// A self-hosted Machine on The Machine Network: only its address. It knows its owner by itself.
    Own(String),
}

pub fn account() -> String {
    if cfg!(feature = "sandbox") {
        if let Some(stand_in) = std::env::var("MACHINE_SANDBOX_ACCOUNT").ok().filter(|s| !s.is_empty()) {
            return stand_in;
        }
    }
    format!("https://{}", address::HOSTED)
}

pub fn start() -> Result<(Pending, String), String> {
    let mut raw = [0u8; 32];
    getrandom::fill(&mut raw).map_err(|_| "failed")?;
    let verifier = URL_SAFE_NO_PAD.encode(raw);
    let address = format!("{}/open?to=app&on=desktop&c={}", account(), challenge(&verifier));
    Ok((Pending { verifier, since: Instant::now() }, address))
}

fn challenge(verifier: &str) -> String {
    URL_SAFE_NO_PAD.encode(Sha256::digest(verifier.as_bytes()))
}

/// What a computer.themachine.app:// link means, for the sign-in going on. None: not one of ours, or too late.
pub fn back(link: &str, pending: &Pending) -> Option<Back> {
    let link = Url::parse(link).ok()?;
    if link.scheme() != SCHEME || link.host_str() != Some("signed-in") || pending.since.elapsed() > LASTS {
        return None;
    }
    let part = |name: &str| link.query_pairs().find(|(k, _)| k == name).map(|(_, v)| v.into_owned());
    if let Some(m) = part("m") {
        return address::parse(&m).map(Back::Own);
    }
    let mut auth = Url::parse(&part("u")?).ok()?;
    let token = auth.query_pairs().find(|(k, _)| k == "t").map(|(_, v)| v.into_owned())?;
    let fine = (20..=100).contains(&token.len()) && token.bytes().all(|b| b.is_ascii_alphanumeric() || b"_-".contains(&b));
    let stand_in = cfg!(feature = "sandbox") && matches!(auth.scheme(), "http" | "https") && auth.host_str() == Some("127.0.0.1");
    let hosted = auth.scheme() == "https" && auth.port().is_none() && address::hosted_host(auth.host_str()?);
    if !fine || !(hosted || stand_in) || auth.path() != "/_machine/auth" || !auth.username().is_empty() || auth.password().is_some() {
        return None;
    }
    let machine = format!("{}/", auth.origin().ascii_serialization());
    auth.query_pairs_mut().append_pair("v", &pending.verifier);
    Some(Back::Hosted { auth: auth.into(), machine })
}

#[cfg(test)]
mod tests {
    use super::*;

    const T: &str = "abcdefghijklmnopqrstuvwxyz0123456789_-";

    fn link(u: &str) -> String {
        let u: String = url::form_urlencoded::byte_serialize(u.as_bytes()).collect();
        format!("{SCHEME}://signed-in?u={u}")
    }

    #[test]
    fn the_challenge_is_the_verifiers_hash() {
        // RFC 7636, appendix B
        assert_eq!(challenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"), "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM");
        let (pending, address) = start().unwrap();
        assert!(address.contains("/open?to=app&on=desktop&c=") && address.ends_with(&challenge(&pending.verifier)) && !address.contains(&pending.verifier));
        assert_eq!(pending.verifier.len(), 43);
    }

    #[test]
    fn a_hosted_machine_comes_back() {
        let (p, _) = start().unwrap();
        let got = back(&link(&format!("https://name.app.themachine.computer/_machine/auth?t={T}&to=app")), &p).unwrap();
        assert_eq!(got, Back::Hosted {
            auth: format!("https://name.app.themachine.computer/_machine/auth?t={T}&to=app&v={}", p.verifier),
            machine: "https://name.app.themachine.computer/".into(),
        });
    }

    #[test]
    fn a_self_hosted_machine_comes_back() {
        let (p, _) = start().unwrap();
        let got = back(&format!("{SCHEME}://signed-in?m=https%3A%2F%2Fmy.example.com%2Fassistant%2F"), &p);
        assert_eq!(got, Some(Back::Own("https://my.example.com/assistant/".into())));
    }

    #[test]
    fn a_made_up_one_only_in_a_sandbox() {
        let (p, _) = start().unwrap();
        for scheme in ["http", "https"] {
            assert_eq!(back(&link(&format!("{scheme}://127.0.0.1:8943/_machine/auth?t={T}")), &p).is_some(), cfg!(feature = "sandbox"));
        }
    }

    #[test]
    fn nothing_else_does() {
        let (p, _) = start().unwrap();
        for u in [
            format!("https://evil.example/_machine/auth?t={T}"),
            format!("https://name.app.themachine.computer.evil.example/_machine/auth?t={T}"),
            format!("http://name.app.themachine.computer/_machine/auth?t={T}"),
            format!("https://name.app.themachine.computer:444/_machine/auth?t={T}"),
            format!("https://a@name.app.themachine.computer/_machine/auth?t={T}"),
            format!("https://name.app.themachine.computer/other?t={T}"),
            format!("https://a.b.app.themachine.computer/_machine/auth?t={T}"),
            format!("https://app.themachine.computer/_machine/auth?t={T}"),
            "https://name.app.themachine.computer/_machine/auth?t=short".into(),
            "https://name.app.themachine.computer/_machine/auth".into(),
        ] {
            assert_eq!(back(&link(&u), &p), None, "{u}");
        }
        assert_eq!(back(&format!("{SCHEME}://connected?h=x"), &p), None);
        assert_eq!(back(&format!("{SCHEME}://signed-in?m=http%3A%2F%2Fevil.example"), &p), None);
        assert_eq!(back("https://example.com", &p), None);
    }
}
