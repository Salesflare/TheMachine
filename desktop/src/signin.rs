//! The account's app sign-in, as the phone app does it (mobile/): the person signs in in their own browser, at
//! /open?to=app&c=<challenge>, and the browser comes back with a token that is only worth something together with the
//! verifier kept here. No password, passkey or code is ever typed into this app. The browser comes back to this computer's
//! own address, 127.0.0.1 (RFC 8252), on a port open for this sign-in only: that needs no link of the system's, which another
//! copy of the app, or one that Windows runs as an administrator, doesn't get. Where no port is free it is the link,
//! computer.themachine.app://.
use crate::address;
use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine};
use sha2::{Digest, Sha256};
use std::io::{Read, Write};
use std::net::{Ipv4Addr, TcpListener, TcpStream};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::{Duration, Instant};
use url::Url;

pub const SCHEME: &str = "computer.themachine.app";
const LASTS: Duration = Duration::from_secs(15 * 60);

pub struct Pending {
    verifier: String,
    since: Instant,
    port: Option<u16>,
    over: Arc<AtomicBool>,
}

impl Pending {
    /// Pressed again: the same one, so that each of the browser's tabs does. Not in its last minutes.
    pub fn lasts(&self) -> bool {
        self.since.elapsed() < LASTS - Duration::from_secs(180)
    }

    pub fn address(&self) -> String {
        let port = self.port.map(|p| format!("&p={p}")).unwrap_or_default();
        format!("{}/open?to=app&on=desktop&c={}{port}", account(), challenge(&self.verifier))
    }
}

impl Drop for Pending {
    fn drop(&mut self) {
        self.over.store(true, Ordering::Relaxed);
    }
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

/// `came`: what the browser comes back with, as the link has it. Whether it was this sign-in's.
pub fn start(came: impl Fn(&str) -> bool + Send + Sync + 'static) -> Result<Pending, String> {
    let mut raw = [0u8; 32];
    getrandom::fill(&mut raw).map_err(|_| "failed")?;
    let verifier = URL_SAFE_NO_PAD.encode(raw);
    let over = Arc::<AtomicBool>::default();
    let port = listen(challenge(&verifier), over.clone(), came);
    Ok(Pending { verifier, since: Instant::now(), port, over })
}

/// A free port of 127.0.0.1 only, which no other computer reaches and no firewall asks about.
#[cfg(not(windows))]
fn port() -> Option<TcpListener> {
    TcpListener::bind((Ipv4Addr::LOCALHOST, 0)).ok()
}

/// On Windows another program may share a port unless it is asked for alone, before it is bound.
#[cfg(windows)]
fn port() -> Option<TcpListener> {
    use std::os::windows::io::FromRawSocket;
    use windows_sys::Win32::Networking::WinSock::{
        bind, listen, setsockopt, WSASocketW, AF_INET, INVALID_SOCKET, IN_ADDR, IN_ADDR_0, IPPROTO_TCP, SOCKADDR_IN, SOCK_STREAM, SOL_SOCKET, SO_EXCLUSIVEADDRUSE,
        WSA_FLAG_NO_HANDLE_INHERIT, WSA_FLAG_OVERLAPPED,
    };
    drop(TcpListener::bind((Ipv4Addr::LOCALHOST, 0)).ok()?); // it starts Winsock
    let to = SOCKADDR_IN { sin_family: AF_INET, sin_port: 0, sin_addr: IN_ADDR { S_un: IN_ADDR_0 { S_addr: u32::from_ne_bytes([127, 0, 0, 1]) } }, sin_zero: [0; 8] };
    // SAFETY: a socket of its own, which the listener closes; the option and the address are valid and as large as said.
    unsafe {
        let socket = WSASocketW(AF_INET.into(), SOCK_STREAM, IPPROTO_TCP, std::ptr::null(), 0, WSA_FLAG_OVERLAPPED | WSA_FLAG_NO_HANDLE_INHERIT);
        if socket == INVALID_SOCKET {
            return None;
        }
        let server = TcpListener::from_raw_socket(socket as _);
        let alone = 1i32;
        let done = setsockopt(socket, SOL_SOCKET, SO_EXCLUSIVEADDRUSE, (&raw const alone).cast(), 4) == 0
            && bind(socket, (&raw const to).cast(), size_of::<SOCKADDR_IN>() as i32) == 0
            && listen(socket, 16) == 0;
        done.then_some(server)
    }
}

/// Each request on its own, so one that says nothing doesn't keep the browser's waiting.
fn listen(path: String, over: Arc<AtomicBool>, came: impl Fn(&str) -> bool + Send + Sync + 'static) -> Option<u16> {
    let server = port()?;
    server.set_nonblocking(true).ok()?;
    let port = server.local_addr().ok()?.port();
    let (came, since, going) = (Arc::new(came), Instant::now(), Arc::<AtomicUsize>::default());
    std::thread::spawn(move || {
        while !over.load(Ordering::Relaxed) && since.elapsed() < LASTS {
            match server.accept() {
                Ok((stream, from)) if from.ip().is_loopback() && going.load(Ordering::Relaxed) < 16 => {
                    let (path, came, going) = (path.clone(), came.clone(), going.clone());
                    going.fetch_add(1, Ordering::Relaxed);
                    std::thread::spawn(move || {
                        let _ = answer(stream, port, &path, &*came);
                        going.fetch_sub(1, Ordering::Relaxed);
                    });
                }
                Ok(_) => {}
                Err(_) => std::thread::sleep(Duration::from_millis(100)),
            }
        }
    });
    Some(port)
}

/// What the browser's tab says then. Nothing of the sign-in is in it, and nothing of it is kept.
const THERE: &str = "<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content=\"width=device-width\"><title>The Machine</title>\
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:light-dark(#f8f7f3,#1b1c1f);color:light-dark(#222,#eee);color-scheme:light dark;font:17px system-ui,sans-serif}</style>\
<p>Back to The Machine. You can close this tab.";

fn answer(mut stream: TcpStream, port: u16, path: &str, came: &dyn Fn(&str) -> bool) -> std::io::Result<()> {
    stream.set_nonblocking(false)?;
    stream.set_read_timeout(Some(Duration::from_secs(5)))?;
    stream.set_write_timeout(Some(Duration::from_secs(5)))?;
    let (mut request, mut part) = (Vec::new(), [0; 2048]);
    while !request.windows(4).any(|w| w == b"\r\n\r\n") {
        let n = stream.read(&mut part)?;
        if n == 0 || request.len() + n > 16 * 1024 {
            return Ok(());
        }
        request.extend_from_slice(&part[..n]);
    }
    let done = asked(&String::from_utf8_lossy(&request), port, path).is_some_and(|query| came(&format!("{SCHEME}://signed-in?{query}")));
    let (state, page) = if done { ("200 OK", THERE) } else { ("404 Not Found", "") };
    stream.write_all(format!(
        "HTTP/1.1 {state}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\nCache-Control: no-store\r\nReferrer-Policy: no-referrer\r\n\
         Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; frame-ancestors 'none'\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\n\r\n{page}",
        page.len()
    ).as_bytes())
}

/// What this sign-in's browser asks with. Its path is the challenge, which no other page knows, and its host this one, so a
/// page that tries every port, or a name that points here, gets nothing.
fn asked<'a>(request: &'a str, port: u16, path: &str) -> Option<&'a str> {
    let mut lines = request.split("\r\n");
    let mut first = lines.next()?.split(' ');
    let (method, target, version) = (first.next()?, first.next()?, first.next()?);
    let mut hosts = lines.take_while(|l| !l.is_empty()).filter_map(|l| l.split_once(':')).filter(|(k, _)| k.eq_ignore_ascii_case("host"));
    let here = hosts.next()?.1.trim() == format!("127.0.0.1:{port}") && hosts.next().is_none();
    let (at, query) = target.strip_prefix('/')?.split_once('?')?;
    (method == "GET" && version.starts_with("HTTP/1.") && here && at == path).then_some(query)
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
        let pending = start(|_| true).unwrap();
        let address = pending.address();
        let address = address.split("&p=").next().unwrap();
        assert!(address.contains("/open?to=app&on=desktop&c=") && address.ends_with(&challenge(&pending.verifier)) && !address.contains(&pending.verifier));
        assert_eq!(pending.verifier.len(), 43);
    }

    #[test]
    fn a_hosted_machine_comes_back() {
        let p = start(|_| true).unwrap();
        let got = back(&link(&format!("https://name.app.themachine.computer/_machine/auth?t={T}&to=app")), &p).unwrap();
        assert_eq!(got, Back::Hosted {
            auth: format!("https://name.app.themachine.computer/_machine/auth?t={T}&to=app&v={}", p.verifier),
            machine: "https://name.app.themachine.computer/".into(),
        });
    }

    #[test]
    fn a_self_hosted_machine_comes_back() {
        let p = start(|_| true).unwrap();
        let got = back(&format!("{SCHEME}://signed-in?m=https%3A%2F%2Fmy.example.com%2Fassistant%2F"), &p);
        assert_eq!(got, Some(Back::Own("https://my.example.com/assistant/".into())));
    }

    #[test]
    fn a_made_up_one_only_in_a_sandbox() {
        let p = start(|_| true).unwrap();
        for scheme in ["http", "https"] {
            assert_eq!(back(&link(&format!("{scheme}://127.0.0.1:8943/_machine/auth?t={T}")), &p).is_some(), cfg!(feature = "sandbox"));
        }
    }

    #[test]
    fn nothing_else_does() {
        let p = start(|_| true).unwrap();
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

    #[test]
    fn only_this_sign_ins_browser_is_heard() {
        let request = |line: &str, host: &str| format!("{line}\r\nHost: {host}\r\nAccept: */*\r\n\r\n");
        assert_eq!(asked(&request("GET /abc?u=x%26y HTTP/1.1", "127.0.0.1:4000"), 4000, "abc"), Some("u=x%26y"));
        for (line, host) in [
            ("GET /abd?u=x HTTP/1.1", "127.0.0.1:4000"),
            ("GET /abc HTTP/1.1", "127.0.0.1:4000"),
            ("GET /?u=x HTTP/1.1", "127.0.0.1:4000"),
            ("GET /abc/?u=x HTTP/1.1", "127.0.0.1:4000"),
            ("POST /abc?u=x HTTP/1.1", "127.0.0.1:4000"),
            ("GET /abc?u=x HTTP/1.1", "127.0.0.1:4001"),
            ("GET /abc?u=x HTTP/1.1", "evil.example:4000"),
            ("GET /abc?u=x HTTP/1.1", "localhost:4000"),
            ("GET /abc?u=x HTTP/1.1", "127.0.0.1:4000\r\nHost: evil.example"),
            ("GET http://127.0.0.1:4000/abc?u=x HTTP/1.1", "127.0.0.1:4000"),
            ("GET /abc?u=x", "127.0.0.1:4000"),
            ("", ""),
        ] {
            assert_eq!(asked(&request(line, host), 4000, "abc"), None, "{line} {host}");
        }
    }

    fn get(port: u16, what: &str) -> String {
        let mut to = TcpStream::connect((Ipv4Addr::LOCALHOST, port)).unwrap();
        to.write_all(format!("GET {what} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n\r\n").as_bytes()).unwrap();
        let mut got = String::new();
        to.read_to_string(&mut got).unwrap();
        got
    }

    #[test]
    fn the_browser_comes_back_to_a_port_of_this_computer() {
        let (tell, told) = std::sync::mpsc::channel();
        let tell = std::sync::Mutex::new(tell);
        let over = Arc::<AtomicBool>::default();
        let port = listen("abc".into(), over.clone(), move |link| { tell.lock().unwrap().send(link.to_string()).unwrap(); link.ends_with("good") }).unwrap();
        let quiet = TcpStream::connect((Ipv4Addr::LOCALHOST, port)).unwrap(); // a browser opens more than it uses
        assert!(get(port, "/favicon.ico").starts_with("HTTP/1.1 404 "));
        assert!(get(port, "/abd?u=good").starts_with("HTTP/1.1 404 "));
        assert!(told.try_recv().is_err());
        assert!(get(port, "/abc?u=bad").starts_with("HTTP/1.1 404 ")); // and it goes on
        assert_eq!(told.recv().unwrap(), format!("{SCHEME}://signed-in?u=bad"));
        let got = get(port, "/abc?u=good");
        assert!(got.starts_with("HTTP/1.1 200 ") && got.contains("Cache-Control: no-store") && got.contains("Referrer-Policy: no-referrer") && !got.contains("good"), "{got}");
        drop(quiet);
        // The port is its own while it lasts, on this address only
        assert!(TcpListener::bind((Ipv4Addr::LOCALHOST, port)).is_err());
        #[cfg(windows)]
        assert!(!shares(port));
        let others = std::net::UdpSocket::bind("0.0.0.0:0").and_then(|s| s.connect("192.0.2.1:9").map(|()| s)).and_then(|s| s.local_addr());
        if let Some(own) = others.ok().filter(|a| !a.ip().is_loopback()) {
            assert!(TcpStream::connect_timeout(&std::net::SocketAddr::new(own.ip(), port), Duration::from_millis(500)).is_err());
        }
        over.store(true, Ordering::Relaxed);
        std::thread::sleep(Duration::from_millis(400));
        assert!(TcpStream::connect_timeout(&(Ipv4Addr::LOCALHOST, port).into(), Duration::from_millis(500)).is_err()); // closed
    }

    /// Whether a program that asks to share the port gets it.
    #[cfg(windows)]
    fn shares(port: u16) -> bool {
        use windows_sys::Win32::Networking::WinSock::*;
        let to = SOCKADDR_IN { sin_family: AF_INET, sin_port: port.to_be(), sin_addr: IN_ADDR { S_un: IN_ADDR_0 { S_addr: u32::from_ne_bytes([127, 0, 0, 1]) } }, sin_zero: [0; 8] };
        // SAFETY: as above.
        unsafe {
            let socket = WSASocketW(AF_INET.into(), SOCK_STREAM, IPPROTO_TCP, std::ptr::null(), 0, 0);
            assert!(socket != INVALID_SOCKET);
            let yes = 1i32;
            assert_eq!(setsockopt(socket, SOL_SOCKET, SO_REUSEADDR, (&raw const yes).cast(), 4), 0);
            let got = bind(socket, (&raw const to).cast(), size_of::<SOCKADDR_IN>() as i32) == 0;
            closesocket(socket);
            got
        }
    }

    #[test]
    fn its_port_goes_with_it() {
        let p = start(|_| true).unwrap();
        assert!(p.lasts());
        assert_eq!(p.port.is_some(), cfg!(feature = "sandbox"));
        assert_eq!(p.address().contains("&p="), p.port.is_some());
        let over = p.over.clone();
        drop(p);
        assert!(over.load(Ordering::Relaxed));
    }
}
