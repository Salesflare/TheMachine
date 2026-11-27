//! This computer as its Machine's way out for the Machine's browser (README.md, Browsing through this computer): sites
//! like LinkedIn then see the owner's own address, not the one of where a hosted Machine runs.
//!
//! One connection out to the signed-in Machine, as its other calls go (TLS checked against the known roots, the owner's
//! sign-in, the Machine's own Origin), upgraded to `tm-exit/1`. Over it the Machine asks for connections to a host and a
//! port; this app opens them itself, only to public internet addresses on 80 and 443, after its own DNS lookup, and
//! carries their bytes. Nothing listens on this computer. A Machine that doesn't have it answers 404: then it asks again
//! in 10 minutes, and Settings shows nothing of it.
//!
//! Frames, both ways: type u8, stream u32, length u32 (big-endian), then that many bytes (16384 at most).
use crate::machine::Machine;
use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::{self, Read, Write};
use std::net::{IpAddr, Ipv4Addr, Ipv6Addr, Shutdown, SocketAddr, TcpStream, ToSocketAddrs, UdpSocket};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{Arc, Mutex, OnceLock};
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};
use url::Url;

pub const UPGRADE: &str = "tm-exit/1";
pub const MAX: usize = 16384;
pub const HELLO: u8 = 1;
pub const OPEN: u8 = 2;
pub const OPENED: u8 = 3;
pub const REFUSED: u8 = 4;
pub const DATA: u8 = 5;
pub const END: u8 = 6;
pub const PING: u8 = 7;
pub const PONG: u8 = 8;
pub const BYE: u8 = 9;

/// Connections at once, bytes a second each way (to the Machine, from it), and bytes a day in all.
const STREAMS: usize = 64;
const DOWN: u64 = 4 << 20;
const UP: u64 = 1 << 20;
const DAY: u64 = 2 << 30;
const CONNECT: Duration = Duration::from_secs(10);
const IDLE: Duration = Duration::from_secs(5 * 60);
const WRITE: Duration = Duration::from_secs(30);
const PINGS: Duration = Duration::from_secs(20);
const DEAD: Duration = Duration::from_secs(60);
/// A Machine without it asks again after this.
const NOT_THERE: Duration = Duration::from_secs(10 * 60);
/// It "carries traffic" this long after a connection was used.
const CARRYING: u64 = 30;

// ===================================================================== frames

pub fn frame(kind: u8, stream: u32, payload: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(9 + payload.len());
    out.push(kind);
    out.extend_from_slice(&stream.to_be_bytes());
    out.extend_from_slice(&(payload.len() as u32).to_be_bytes());
    out.extend_from_slice(payload);
    out
}

/// The next frame. One longer than MAX ends the connection.
pub fn read_frame(from: &mut impl Read) -> io::Result<(u8, u32, Vec<u8>)> {
    let mut head = [0u8; 9];
    from.read_exact(&mut head)?;
    let stream = u32::from_be_bytes([head[1], head[2], head[3], head[4]]);
    let length = u32::from_be_bytes([head[5], head[6], head[7], head[8]]) as usize;
    if length > MAX {
        return Err(io::Error::new(io::ErrorKind::InvalidData, "frame too long"));
    }
    let mut payload = vec![0u8; length];
    from.read_exact(&mut payload)?;
    Ok((head[0], stream, payload))
}

// ===================================================================== where it may go

/// Whether this computer may open a connection there: "port" and "blocked" are the reasons it may not. `seen_as`: this
/// computer's public address, as its Machine sees it (its own router, reached from outside); `own`: an IPv6 address of
/// this computer's, whose /64 is its local network.
pub fn allowed(ip: IpAddr, port: u16, seen_as: Option<IpAddr>, own: Option<Ipv6Addr>) -> Result<(), &'static str> {
    if sandboxed(ip) {
        return Ok(());
    }
    if port != 80 && port != 443 {
        return Err("port");
    }
    let to = plain(ip);
    let near = |a: Ipv6Addr, b: Ipv6Addr| a.segments()[..4] == b.segments()[..4];
    let seen = match (to, seen_as.map(plain)) {
        (to, Some(seen)) if to == seen => true,
        (IpAddr::V6(to), Some(IpAddr::V6(seen))) => near(to, seen),
        _ => false,
    };
    let here = seen || matches!(to, IpAddr::V6(to) if own.is_some_and(|own| near(to, own)));
    if here || !public(ip) {
        return Err("blocked");
    }
    Ok(())
}

/// An IPv6 address that holds an IPv4 one (mapped, NAT64, 6to4) as that IPv4 address.
fn plain(ip: IpAddr) -> IpAddr {
    match ip {
        IpAddr::V6(v6) => inner(v6).map_or(ip, IpAddr::V4),
        v4 => v4,
    }
}

fn inner(v6: Ipv6Addr) -> Option<Ipv4Addr> {
    let s = v6.segments();
    let low = Ipv4Addr::new((s[6] >> 8) as u8, s[6] as u8, (s[7] >> 8) as u8, s[7] as u8);
    match s {
        [0, 0, 0, 0, 0, 0xffff, ..] => Some(low),             // ::ffff:0:0/96, IPv4-mapped
        [0x64, 0xff9b, 0, 0, 0, 0, ..] => Some(low),          // 64:ff9b::/96, NAT64
        [0x2002, a, b, ..] => Some(Ipv4Addr::new((a >> 8) as u8, a as u8, (b >> 8) as u8, b as u8)), // 2002::/16, 6to4
        _ => None,
    }
}

/// On the public internet: not this computer, its network, the provider's, a cloud's metadata, nor any special range.
pub fn public(ip: IpAddr) -> bool {
    match ip {
        IpAddr::V4(v4) => public_v4(v4),
        IpAddr::V6(v6) => match inner(v6) {
            Some(v4) => public_v4(v4),
            None => public_v6(v6),
        },
    }
}

fn public_v4(ip: Ipv4Addr) -> bool {
    let [a, b, c, _] = ip.octets();
    !(a == 0                                   // 0.0.0.0/8, this network
        || a == 10                             // 10/8, private
        || a == 100 && (64..128).contains(&b)  // 100.64/10, carrier-grade NAT and Tailscale
        || a == 127                            // loopback
        || a == 169 && b == 254                // link-local, with the clouds' metadata 169.254.169.254
        || a == 172 && (16..32).contains(&b)   // 172.16/12, private
        || a == 192 && b == 0 && c == 0        // 192.0.0/24, protocol assignments
        || a == 192 && b == 0 && c == 2        // 192.0.2/24, documentation
        || a == 192 && b == 88 && c == 99      // 192.88.99/24, 6to4 relays
        || a == 192 && b == 168                // 192.168/16, private
        || a == 198 && (b == 18 || b == 19)    // 198.18/15, benchmarks
        || a == 198 && b == 51 && c == 100     // documentation
        || a == 203 && b == 0 && c == 113      // documentation
        || a >= 224)                           // multicast, reserved, broadcast
}

fn public_v6(ip: Ipv6Addr) -> bool {
    let s = ip.segments();
    (s[0] & 0xe000) == 0x2000                  // 2000::/3, global unicast; ::, ::1, fc00::/7, fe80::/10, ff00::/8 aren't
        && !(s[0] == 0x2001 && s[1] < 0x0200)  // 2001::/23, protocol assignments (Teredo among them)
        && !(s[0] == 0x2001 && s[1] == 0x0db8) // documentation
        && !(s[0] == 0x3fff && s[1] < 0x1000)  // 3fff::/20, documentation
}

/// A sandbox build, for smoke/: MACHINE_SANDBOX_EXIT_FROM lets this computer's own addresses through, any port.
#[cfg(feature = "sandbox")]
fn sandboxed(ip: IpAddr) -> bool {
    from().is_some() && ip.is_loopback()
}

#[cfg(not(feature = "sandbox"))]
fn sandboxed(_: IpAddr) -> bool {
    false
}

/// The address a sandbox build connects from, so the made-up site can tell it from the Machine's own.
#[cfg(feature = "sandbox")]
fn from() -> Option<IpAddr> {
    std::env::var("MACHINE_SANDBOX_EXIT_FROM").ok()?.parse().ok()
}

/// A host name or an IP address, as a browser sends it, and nothing else.
fn host_name(host: &str) -> bool {
    !host.is_empty()
        && host.len() <= 253
        && (host.parse::<IpAddr>().is_ok() || host.split('.').all(|l| !l.is_empty() && l.len() <= 63 && l.bytes().all(|b| b.is_ascii_alphanumeric() || b"-_".contains(&b))))
}

/// This computer's own IPv6 address on the way out, without sending anything: its /64 is the local network.
fn own_v6() -> Option<Ipv6Addr> {
    let socket = UdpSocket::bind("[::]:0").ok()?;
    socket.connect("[2001:4860:4860::8888]:53").ok()?;
    match socket.local_addr().ok()? {
        SocketAddr::V6(at) if public_v6(*at.ip()) => Some(*at.ip()),
        _ => None,
    }
}

/// Connects there after its own lookup, only to an address it checked (no second lookup), or says why not.
fn dial(host: &str, port: u16, seen_as: Option<IpAddr>, own: Option<Ipv6Addr>) -> Result<TcpStream, &'static str> {
    if !host_name(host) {
        return Err("blocked");
    }
    let found: Vec<SocketAddr> = (host, port).to_socket_addrs().map_err(|_| "dns")?.collect();
    if found.is_empty() {
        return Err("dns");
    }
    let mut checked: Vec<SocketAddr> = Vec::new();
    let mut why = "blocked";
    for at in found {
        match allowed(at.ip(), port, seen_as, own) {
            Ok(()) => checked.push(at),
            Err(reason) => why = reason,
        }
    }
    if checked.is_empty() {
        return Err(why);
    }
    checked.sort_by_key(|at| at.is_ipv6()); // IPv4 first, as most sites expect a sign-in from
    checked.iter().find_map(|at| connect(at).ok()).ok_or("unreachable")
}

#[cfg(not(feature = "sandbox"))]
fn connect(at: &SocketAddr) -> io::Result<TcpStream> {
    TcpStream::connect_timeout(at, CONNECT)
}

#[cfg(feature = "sandbox")]
fn connect(at: &SocketAddr) -> io::Result<TcpStream> {
    let Some(from) = from().filter(|_| at.ip().is_loopback()) else { return TcpStream::connect_timeout(at, CONNECT) };
    let socket = socket2::Socket::new(socket2::Domain::for_address(*at), socket2::Type::STREAM, None)?;
    socket.bind(&SocketAddr::new(from, 0).into())?;
    socket.connect_timeout(&(*at).into(), CONNECT)?;
    Ok(socket.into())
}

// ===================================================================== how much

/// Bytes a second one way, for all connections together.
struct Pace {
    per: u64,
    at: Mutex<(Instant, u64)>,
}

impl Pace {
    fn fresh(per: u64) -> Pace {
        Pace { per, at: Mutex::new((Instant::now(), 0)) }
    }

    /// Waits until these bytes fit in this second. One frame is never more than a second's worth.
    fn take(&self, n: u64) {
        loop {
            let wait = {
                let mut at = self.at.lock().unwrap();
                let now = Instant::now();
                if now.duration_since(at.0) >= Duration::from_secs(1) {
                    *at = (now, 0);
                }
                if at.1 + n <= self.per || at.1 == 0 {
                    at.1 += n;
                    return;
                }
                Duration::from_secs(1).saturating_sub(now.duration_since(at.0))
            };
            std::thread::sleep(wait.max(Duration::from_millis(5)));
        }
    }
}

fn day() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_secs() / 86400).unwrap_or(0)
}

fn now() -> u64 {
    SystemTime::now().duration_since(UNIX_EPOCH).map(|d| d.as_secs()).unwrap_or(0)
}

// ===================================================================== the connection to the Machine

/// What the app has of it: whether it may, whether the Machine has it, and when a connection was last used.
#[derive(Default)]
pub struct Exit {
    on: AtomicBool,
    /// The Machine took the upgrade (once, since the app started).
    offered: AtomicBool,
    used: AtomicU64,
    carrying: AtomicBool,
    today: Mutex<(u64, u64)>,
    /// The connection now, to end it at once.
    wire: Mutex<Option<Arc<Wire>>>,
    thread: Mutex<Option<std::thread::Thread>>,
}

fn exit() -> &'static Exit {
    static EXIT: OnceLock<Exit> = OnceLock::new();
    EXIT.get_or_init(Exit::default)
}

/// Whether a connection carried something in the last half minute.
pub fn carrying() -> bool {
    exit().on.load(Ordering::Relaxed) && now().saturating_sub(exit().used.load(Ordering::Relaxed)) < CARRYING
}

/// Whether the signed-in Machine takes it.
pub fn offered() -> bool {
    exit().offered.load(Ordering::Relaxed)
}

/// On or off (Settings). Off ends the connection now, telling the Machine, so it doesn't wait for this computer.
pub fn set(on: bool) {
    let was = exit().on.swap(on, Ordering::Relaxed);
    if was && !on {
        let wire = exit().wire.lock().unwrap().take(); // let go of before the send, which may wait
        if let Some(wire) = wire {
            let _ = wire.send(&frame(BYE, 0, b"off"));
            wire.end();
        }
    }
    again();
}

/// Signed in to another Machine, or out: the connection is made afresh.
pub fn again() {
    let wire = exit().wire.lock().unwrap().take();
    if let Some(wire) = wire {
        wire.end();
    }
    exit().offered.store(false, Ordering::Relaxed);
    let thread = exit().thread.lock().unwrap().clone();
    if let Some(thread) = thread {
        thread.unpark();
    }
}

/// Keeps a connection to the Machine `machine` gives (None: signed out) while it is on. `changed`: it began or ended
/// carrying, or the Machine was found to have it.
pub fn start(on: bool, machine: impl Fn() -> Option<Machine> + Send + 'static, changed: impl Fn() + Send + Sync + 'static) {
    exit().on.store(on, Ordering::Relaxed);
    let changed: Arc<dyn Fn() + Send + Sync> = Arc::new(changed);
    let _ = SAID.set(changed.clone());
    let worker = std::thread::spawn(move || {
        let mut wait = Duration::from_secs(5);
        loop {
            let Some(to) = machine().filter(|_| exit().on.load(Ordering::Relaxed)) else {
                std::thread::park();
                continue;
            };
            let began = Instant::now();
            let ended = keep(&to, &changed);
            exit().wire.lock().unwrap().take();
            note(&changed);
            wait = match ended {
                Ended::NotThere => NOT_THERE,
                Ended::Refused => NOT_THERE,
                Ended::Lost if began.elapsed() > Duration::from_secs(60) => Duration::from_secs(5),
                Ended::Lost => (wait * 2).min(Duration::from_secs(300)),
            };
            std::thread::park_timeout(wait);
        }
    });
    *exit().thread.lock().unwrap() = Some(worker.thread().clone());
    // Pings every PINGS, and says when carrying ended
    std::thread::spawn(|| loop {
        std::thread::sleep(Duration::from_secs(5));
        let wire = exit().wire.lock().unwrap().clone(); // let go of before the ping, which may wait
        if let Some(wire) = wire {
            let due = {
                let mut pinged = wire.pinged.lock().unwrap();
                let due = pinged.elapsed() >= PINGS;
                if due {
                    *pinged = Instant::now();
                }
                due
            };
            if due {
                if wire.send(&frame(PING, 0, b"")).is_err() {
                    wire.end();
                }
            }
        }
        if let Some(said) = SAID.get() {
            note(said);
        }
    });
}

static SAID: OnceLock<Arc<dyn Fn() + Send + Sync>> = OnceLock::new();

/// Tells when carrying began or ended.
fn note(changed: &Arc<dyn Fn() + Send + Sync>) {
    let now = carrying();
    if exit().carrying.swap(now, Ordering::Relaxed) != now {
        changed();
    }
}

enum Ended {
    /// 404: this Machine doesn't have it (or has it off).
    NotThere,
    /// 403 or another answer: not its owner's, now.
    Refused,
    Lost,
}

/// The TLS (or, for a sandbox's http Machine, the plain) connection: one writer at a time, frames whole.
pub struct Wire {
    tls: Option<Mutex<rustls::ClientConnection>>,
    sock: TcpStream,
    one: Mutex<()>,
    pinged: Mutex<Instant>,
}

impl Wire {
    fn send(&self, bytes: &[u8]) -> io::Result<()> {
        let _one = self.one.lock().unwrap();
        let mut sock = &self.sock;
        match &self.tls {
            None => sock.write_all(bytes),
            Some(tls) => {
                let mut out = Vec::new();
                {
                    let mut tls = tls.lock().unwrap();
                    tls.writer().write_all(bytes)?;
                    while tls.wants_write() {
                        tls.write_tls(&mut out)?;
                    }
                }
                sock.write_all(&out)
            }
        }
    }

    fn end(&self) {
        let _ = self.sock.shutdown(Shutdown::Both);
    }
}

/// What comes from the Machine, as plain bytes.
struct Incoming {
    wire: Arc<Wire>,
    sock: TcpStream,
    plain: Vec<u8>,
    closed: bool,
}

impl Read for Incoming {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        loop {
            if !self.plain.is_empty() {
                let n = buf.len().min(self.plain.len());
                buf[..n].copy_from_slice(&self.plain[..n]);
                self.plain.drain(..n);
                return Ok(n);
            }
            if self.closed {
                return Ok(0);
            }
            let Some(tls) = &self.wire.tls else { return self.sock.read(buf) };
            let mut raw = [0u8; 16384];
            let n = self.sock.read(&mut raw)?;
            if n == 0 {
                return Ok(0);
            }
            let flush = {
                let mut tls = tls.lock().unwrap();
                let mut rest = &raw[..n];
                while !rest.is_empty() && !self.closed {
                    tls.read_tls(&mut rest)?;
                    tls.process_new_packets().map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
                    match tls.reader().read_to_end(&mut self.plain) {
                        Ok(_) => self.closed = true, // the Machine closed it
                        Err(e) if e.kind() == io::ErrorKind::WouldBlock => {}
                        Err(e) if e.kind() == io::ErrorKind::UnexpectedEof => self.closed = true,
                        Err(e) => return Err(e),
                    }
                }
                tls.wants_write()
            };
            if flush {
                self.wire.send(&[])?;
            }
        }
    }
}

/// The roots a Machine's certificate is checked against: the known ones, as its other calls (machine.rs).
fn roots() -> rustls::RootCertStore {
    #[cfg(feature = "sandbox")]
    if let Some(path) = std::env::var_os("MACHINE_SANDBOX_ROOT") {
        use rustls::pki_types::{pem::PemObject, CertificateDer};
        let mut roots = rustls::RootCertStore::empty();
        for cert in CertificateDer::pem_file_iter(path).into_iter().flatten().flatten() {
            let _ = roots.add(cert);
        }
        return roots;
    }
    rustls::RootCertStore { roots: webpki_roots::TLS_SERVER_ROOTS.to_vec() }
}

/// Opens it: TLS, then the upgrade. What came after the answer's head is the start of the frames.
fn open(to: &Machine) -> Result<(Arc<Wire>, Incoming), Ended> {
    let url = Url::parse(&to.url).map_err(|_| Ended::Refused)?;
    let host = url.host_str().ok_or(Ended::Refused)?.to_string();
    let port = url.port_or_known_default().ok_or(Ended::Refused)?;
    let plain = url.scheme() == "http";
    if plain && !(cfg!(feature = "sandbox") && host == "127.0.0.1") {
        return Err(Ended::Refused);
    }
    let at = (host.as_str(), port).to_socket_addrs().map_err(|_| Ended::Lost)?.next().ok_or(Ended::Lost)?;
    let sock = TcpStream::connect_timeout(&at, CONNECT).map_err(|_| Ended::Lost)?;
    let _ = sock.set_nodelay(true);
    sock.set_read_timeout(Some(DEAD)).map_err(|_| Ended::Lost)?;
    sock.set_write_timeout(Some(WRITE)).map_err(|_| Ended::Lost)?;
    let tls = if plain {
        None
    } else {
        let provider = Arc::new(rustls::crypto::ring::default_provider());
        let config = rustls::ClientConfig::builder_with_provider(provider)
            .with_safe_default_protocol_versions()
            .map_err(|_| Ended::Lost)?
            .with_root_certificates(roots())
            .with_no_client_auth();
        let name = rustls::pki_types::ServerName::try_from(host.clone()).map_err(|_| Ended::Refused)?;
        let mut tls = rustls::ClientConnection::new(Arc::new(config), name).map_err(|_| Ended::Lost)?;
        let mut s = &sock;
        while tls.is_handshaking() {
            tls.complete_io(&mut s).map_err(|_| Ended::Lost)?;
        }
        Some(Mutex::new(tls))
    };
    let wire = Arc::new(Wire { tls, sock: sock.try_clone().map_err(|_| Ended::Lost)?, one: Mutex::new(()), pinged: Mutex::new(Instant::now()) });
    let origin = crate::address::origin(&to.url);
    let cookie = to.cookie.as_ref().map(|c| format!("Cookie: {c}\r\n")).unwrap_or_default();
    let ask = format!(
        "GET {}api/exit HTTP/1.1\r\nHost: {}\r\nOrigin: {origin}\r\n{cookie}Connection: Upgrade\r\nUpgrade: {UPGRADE}\r\nUser-Agent: {}\r\n\r\n",
        url.path(),
        url.host_str().map(|h| if url.port().is_some() { format!("{h}:{port}") } else { h.to_string() }).unwrap_or_default(),
        crate::machine::user_agent(),
    );
    wire.send(ask.as_bytes()).map_err(|_| Ended::Lost)?;
    let mut incoming = Incoming { wire: wire.clone(), sock, plain: Vec::new(), closed: false };
    let mut head = Vec::new();
    let mut byte = [0u8; 1];
    while !head.ends_with(b"\r\n\r\n") {
        if head.len() > 8192 || incoming.read(&mut byte).map_err(|_| Ended::Lost)? == 0 {
            return Err(Ended::Lost);
        }
        head.push(byte[0]);
    }
    let head = String::from_utf8_lossy(&head).to_ascii_lowercase();
    let status = head.split_whitespace().nth(1).and_then(|s| s.parse::<u16>().ok()).unwrap_or(0);
    match status {
        101 if head.contains(&format!("\r\nupgrade: {UPGRADE}")) => {}
        404 => return Err(Ended::NotThere),
        502..=504 => return Err(Ended::Lost), // off or starting
        _ => return Err(Ended::Refused),
    }
    Ok((wire, incoming))
}

/// One connection to the target, as the Machine asked for it.
struct Stream {
    to: TcpStream,
    used: Arc<AtomicU64>,
}

/// Until it ends.
fn keep(to: &Machine, changed: &Arc<dyn Fn() + Send + Sync>) -> Ended {
    let (wire, mut incoming) = match open(to) {
        Ok(opened) => opened,
        Err(ended) => return ended,
    };
    let hello = json!({"v": 1, "app": env!("CARGO_PKG_VERSION"), "os": if cfg!(target_os = "macos") { "mac" } else { std::env::consts::OS }});
    if wire.send(&frame(HELLO, 0, hello.to_string().as_bytes())).is_err() {
        return Ended::Lost;
    }
    exit().offered.store(true, Ordering::Relaxed);
    *exit().wire.lock().unwrap() = Some(wire.clone());
    changed();
    let streams: Arc<Mutex<HashMap<u32, Stream>>> = Arc::default();
    let mut seen_as = None;
    let own = own_v6();
    static UP_PACE: OnceLock<Pace> = OnceLock::new();
    let up = UP_PACE.get_or_init(|| Pace::fresh(UP));
    let ended = loop {
        let Ok((kind, id, payload)) = read_frame(&mut incoming) else { break Ended::Lost };
        if !exit().on.load(Ordering::Relaxed) {
            break Ended::Lost;
        }
        match kind {
            HELLO => {
                let said: Value = serde_json::from_slice(&payload).unwrap_or_default();
                seen_as = said["seen_as"].as_str().and_then(|s| s.parse().ok());
            }
            PING => {
                let _ = wire.send(&frame(PONG, 0, &payload[..payload.len().min(64)]));
            }
            BYE => break Ended::Lost,
            OPEN if id != 0 => {
                let asked: Value = serde_json::from_slice(&payload).unwrap_or_default();
                let (host, port) = (asked["host"].as_str().unwrap_or_default().to_string(), asked["port"].as_u64().unwrap_or(0));
                let busy = {
                    let open = streams.lock().unwrap();
                    open.len() >= STREAMS || open.contains_key(&id)
                };
                let reason = if busy { Some("busy") } else if !spend(0) { Some("cap") } else { None };
                if let Some(reason) = reason {
                    let _ = wire.send(&frame(REFUSED, id, reason.as_bytes()));
                    continue;
                }
                let (wire, streams) = (wire.clone(), streams.clone());
                std::thread::spawn(move || carry(id, &host, u16::try_from(port).unwrap_or(0), seen_as, own, &wire, &streams));
            }
            DATA => {
                let found = streams.lock().unwrap().get(&id).map(|s| (s.to.try_clone(), s.used.clone()));
                match found {
                    Some((Ok(mut target), used)) => {
                        up.take(payload.len() as u64);
                        used.store(now(), Ordering::Relaxed);
                        exit().used.store(now(), Ordering::Relaxed);
                        if !spend(payload.len() as u64) || target.write_all(&payload).is_err() {
                            close(id, &wire, &streams);
                        }
                    }
                    _ => {
                        let _ = wire.send(&frame(END, id, b""));
                    }
                }
            }
            END => {
                let stream = streams.lock().unwrap().remove(&id);
                if let Some(stream) = stream {
                    let _ = stream.to.shutdown(Shutdown::Both);
                }
            }
            _ => {} // PONG, and what a newer Machine may say
        }
        note(changed);
    };
    for (_, stream) in streams.lock().unwrap().drain() {
        let _ = stream.to.shutdown(Shutdown::Both);
    }
    wire.end();
    ended
}

/// Counts these bytes against the day's cap: whether they still fit.
fn spend(n: u64) -> bool {
    let mut today = exit().today.lock().unwrap();
    let day = day();
    if today.0 != day {
        *today = (day, 0);
    }
    today.1 += n;
    today.1 <= DAY
}

fn close(id: u32, wire: &Wire, streams: &Mutex<HashMap<u32, Stream>>) {
    let stream = streams.lock().unwrap().remove(&id); // let go of before the send, which may wait
    if let Some(stream) = stream {
        let _ = stream.to.shutdown(Shutdown::Both);
        let _ = wire.send(&frame(END, id, b""));
    }
}

/// Opens one connection the Machine asked for, then carries what comes from the site back, until either ends.
fn carry(id: u32, host: &str, port: u16, seen_as: Option<IpAddr>, own: Option<Ipv6Addr>, wire: &Wire, streams: &Mutex<HashMap<u32, Stream>>) {
    static DOWN_PACE: OnceLock<Pace> = OnceLock::new();
    let down = DOWN_PACE.get_or_init(|| Pace::fresh(DOWN));
    let target = match dial(host, port, seen_as, own) {
        Ok(target) => target,
        Err(reason) => {
            let _ = wire.send(&frame(REFUSED, id, reason.as_bytes()));
            return;
        }
    };
    let used = Arc::new(AtomicU64::new(now()));
    let kept = target.try_clone().and_then(|to| {
        to.set_write_timeout(Some(WRITE))?;
        target.set_read_timeout(Some(Duration::from_secs(30)))?;
        Ok(to)
    });
    let Ok(to) = kept else {
        let _ = wire.send(&frame(REFUSED, id, b"unreachable"));
        return;
    };
    streams.lock().unwrap().insert(id, Stream { to, used: used.clone() });
    exit().used.store(now(), Ordering::Relaxed);
    if wire.send(&frame(OPENED, id, b"")).is_err() {
        close(id, wire, streams);
        return;
    }
    let mut from = &target;
    let mut buf = vec![0u8; MAX];
    loop {
        match from.read(&mut buf) {
            Ok(0) => break,
            Ok(n) => {
                down.take(n as u64);
                used.store(now(), Ordering::Relaxed);
                exit().used.store(now(), Ordering::Relaxed);
                if !spend(n as u64) || wire.send(&frame(DATA, id, &buf[..n])).is_err() {
                    break;
                }
            }
            Err(e) if matches!(e.kind(), io::ErrorKind::WouldBlock | io::ErrorKind::TimedOut) => {
                if now().saturating_sub(used.load(Ordering::Relaxed)) >= IDLE.as_secs() || !streams.lock().unwrap().contains_key(&id) {
                    break;
                }
            }
            Err(_) => break,
        }
    }
    close(id, wire, streams);
}

#[cfg(test)]
mod tests {
    use super::*;

    fn ip(s: &str) -> IpAddr {
        s.parse().unwrap()
    }

    #[test]
    fn the_golden_frame() {
        let open = frame(OPEN, 1, br#"{"host":"a.example","port":443}"#);
        let hex: String = open.iter().map(|b| format!("{b:02x}")).collect();
        assert_eq!(hex, "02000000010000001f7b22686f7374223a22612e6578616d706c65222c22706f7274223a3434337d");
        assert_eq!(read_frame(&mut &open[..]).unwrap(), (OPEN, 1, br#"{"host":"a.example","port":443}"#.to_vec()));
    }

    #[test]
    fn frames_one_after_another_and_none_too_long() {
        let mut both = frame(DATA, 7, b"abc");
        both.extend(frame(END, 7, b""));
        let mut from = &both[..];
        assert_eq!(read_frame(&mut from).unwrap(), (DATA, 7, b"abc".to_vec()));
        assert_eq!(read_frame(&mut from).unwrap(), (END, 7, vec![]));
        assert!(read_frame(&mut from).is_err());
        let mut long = vec![DATA, 0, 0, 0, 1];
        long.extend(((MAX + 1) as u32).to_be_bytes());
        assert_eq!(read_frame(&mut &long[..]).unwrap_err().kind(), io::ErrorKind::InvalidData);
        assert!(read_frame(&mut &frame(DATA, 1, &[0; MAX])[..]).is_ok());
    }

    #[test]
    fn public_sites_on_80_and_443() {
        for at in ["93.184.215.14", "1.1.1.1", "8.8.8.8", "2a03:2880:f10c:83:face:b00c:0:25de", "2606:4700::6810:84e5", "::ffff:93.184.215.14", "64:ff9b::808:808", "2002:5db8:d70e::1"] {
            assert_eq!(allowed(ip(at), 443, None, None), Ok(()), "{at}");
            assert_eq!(allowed(ip(at), 80, None, None), Ok(()), "{at}");
        }
    }

    #[test]
    fn other_ports_never() {
        for port in [0, 22, 25, 53, 3389, 8080, 8443, 9222] {
            assert_eq!(allowed(ip("93.184.215.14"), port, None, None), Err("port"), "{port}");
        }
    }

    #[test]
    fn never_this_computer_its_network_or_special_ranges() {
        for at in [
            "0.0.0.0", "0.1.2.3", "10.0.0.1", "10.255.255.255", "100.64.0.1", "100.100.100.100", "100.127.255.255", "127.0.0.1", "127.8.9.10",
            "169.254.169.254", "169.254.0.1", "172.16.0.1", "172.31.255.255", "192.0.0.170", "192.0.2.1", "192.88.99.1", "192.168.1.1", "198.18.0.1",
            "198.19.255.255", "198.51.100.7", "203.0.113.9", "224.0.0.1", "239.255.255.250", "240.0.0.1", "255.255.255.255",
            "::", "::1", "fe80::1", "fc00::1", "fd00:ec2::254", "fd7a:115c:a1e0::1", "ff02::1", "fec0::1", "100::1", "2001::1", "2001:0:4136:e378::1",
            "2001:db8::1", "3fff::1", "::ffff:127.0.0.1", "::ffff:10.1.2.3", "::ffff:169.254.169.254", "64:ff9b::a00:1", "64:ff9b::7f00:1",
            "64:ff9b:1::1", "2002:a00:1::1", "2002:7f00:1::1", "2002:c0a8:101::1", "::127.0.0.1",
        ] {
            assert_eq!(allowed(ip(at), 443, None, None), Err("blocked"), "{at}");
        }
        assert!(public(ip("100.63.255.255")) && public(ip("100.128.0.0")) && public(ip("172.15.255.255")) && public(ip("172.32.0.0")));
        assert!(public(ip("169.253.0.1")) && public(ip("192.169.0.1")) && public(ip("223.255.255.255")));
    }

    #[test]
    fn nor_its_own_public_address_or_ipv6_network() {
        let home = Some(ip("81.82.83.84"));
        assert_eq!(allowed(ip("81.82.83.84"), 443, home, None), Err("blocked"));
        assert_eq!(allowed(ip("::ffff:81.82.83.84"), 443, home, None), Err("blocked"));
        assert_eq!(allowed(ip("81.82.83.85"), 443, home, None), Ok(()));
        let v6 = Some(ip("2a02:1810:1:2:aaaa::1"));
        assert_eq!(allowed(ip("2a02:1810:1:2::99"), 443, v6, None), Err("blocked"));
        assert_eq!(allowed(ip("2a02:1810:1:3::99"), 443, v6, None), Ok(()));
        let own = Some("2a02:1810:5:6::7".parse().unwrap());
        assert_eq!(allowed(ip("2a02:1810:5:6:1::1"), 443, home, own), Err("blocked"));
        assert_eq!(allowed(ip("2a02:1810:5:7::1"), 443, home, own), Ok(()));
    }

    #[test]
    fn names_as_a_browser_sends_them() {
        for host in ["www.linkedin.com", "a.example", "x_y.example", "93.184.215.14", "2606:4700::6810:84e5"] {
            assert!(host_name(host), "{host}");
        }
        for host in ["", "a b", "a..b", "a/b", "a:443", "[::1]", &"a".repeat(254), "x\r\nHost: y"] {
            assert!(!host_name(host), "{host}");
        }
    }

    #[test]
    fn a_lookup_that_leads_home_is_refused() {
        assert_eq!(dial("127.0.0.1", 443, None, None).err(), Some("blocked"));
        assert_eq!(dial("10.1.2.3", 80, None, None).err(), Some("blocked"));
        assert_eq!(dial("1.1.1.1", 8080, None, None).err(), Some("port"));
        assert_eq!(dial("localhost", 443, None, None).err(), Some("blocked"));
    }

    #[test]
    fn pace_lets_a_second_s_worth_through() {
        let pace = Pace::fresh(1000);
        let at = Instant::now();
        pace.take(600);
        pace.take(400);
        assert!(at.elapsed() < Duration::from_millis(200));
        pace.take(10);
        assert!(at.elapsed() >= Duration::from_millis(700));
    }
}
