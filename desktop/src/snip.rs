//! A screenshot of what the person picks, with the system's own tool: an area or a window, or nothing. It asks for no
//! permission of its own, sees nothing else, and keeps nothing: the tool's copy goes once it is read.
const MOST: usize = 25 << 20;

/// A PNG or a JPEG. None: the person picked nothing.
pub fn take() -> Result<Option<Vec<u8>>, String> {
    let taken = system::take().map_err(|_| "shot")?;
    match taken {
        Some(i) if i.len() > MOST || !(i.starts_with(b"\x89PNG\r\n\x1a\n") || i.starts_with(&[0xff, 0xd8, 0xff])) => Err("shot".into()),
        taken => Ok(taken),
    }
}

pub fn there() -> bool {
    system::there()
}

/// The desktop's portal: its own dialog, or the compositor's own picking.
#[cfg(target_os = "linux")]
mod system {
    use std::{collections::HashMap, fs, sync::mpsc, time::Duration};
    use zbus::blocking::{Connection, Proxy};
    use zbus::zvariant::{OwnedObjectPath, OwnedValue, Value};

    const BUS: &str = "org.freedesktop.portal.Desktop";
    const PORTAL: &str = "org.freedesktop.portal.Screenshot";
    /// How long a person may take.
    const WAIT: Duration = Duration::from_secs(180);

    fn portal(bus: &Connection) -> zbus::Result<Proxy<'_>> {
        Proxy::new(bus, BUS, "/org/freedesktop/portal/desktop", PORTAL)
    }

    /// Its second version is the first that lets the person pick.
    pub fn there() -> bool {
        let version = || portal(&Connection::session()?)?.get_property::<u32>("version");
        version().is_ok_and(|v| v >= 2)
    }

    pub fn take() -> Result<Option<Vec<u8>>, Box<dyn std::error::Error>> {
        let bus = Connection::session()?;
        let mut raw = [0u8; 8];
        getrandom::fill(&mut raw).map_err(|e| e.to_string())?;
        let token = format!("machine{:016x}", u64::from_ne_bytes(raw));
        let me = bus.unique_name().ok_or("no name")?.trim_start_matches(':').replace('.', "_");
        let request = Proxy::new(&bus, BUS, format!("/org/freedesktop/portal/desktop/request/{me}/{token}"), "org.freedesktop.portal.Request")?;
        let mut answers = request.receive_signal("Response")?; // before it is asked
        let options = HashMap::from([("handle_token", Value::from(token.as_str())), ("interactive", Value::from(true))]);
        portal(&bus)?.call::<_, _, OwnedObjectPath>("Screenshot", &("", options))?;
        let (to, answer) = mpsc::channel();
        std::thread::spawn(move || {
            let _ = answers.next().map(|m| to.send(m));
        });
        let Ok(answer) = answer.recv_timeout(WAIT) else {
            request.call_method("Close", &())?;
            return Ok(None);
        };
        let (code, found): (u32, HashMap<String, OwnedValue>) = answer.body().deserialize()?;
        if code == 1 {
            return Ok(None);
        }
        let uri = found.get("uri").ok_or("no image")?.downcast_ref::<&str>()?;
        let file = url::Url::parse(uri)?.to_file_path().map_err(|()| "not a file")?;
        if !fs::symlink_metadata(&file)?.is_file() {
            return Err("not a file".into());
        }
        let image = fs::read(&file);
        let _ = fs::remove_file(&file);
        Ok(Some(image?))
    }
}

/// Windows' own snip. It puts what was picked on the clipboard, where it is taken from: Windows itself may also keep it, as
/// its own settings say (Snipping Tool, clipboard history).
#[cfg(windows)]
mod system {
    use std::time::{Duration, Instant};
    use windows_sys::Win32::Foundation::{CloseHandle, HANDLE, MAX_PATH};
    use windows_sys::Win32::System::DataExchange::{
        CloseClipboard, EmptyClipboard, GetClipboardData, GetClipboardSequenceNumber, IsClipboardFormatAvailable, OpenClipboard, RegisterClipboardFormatW,
    };
    use windows_sys::Win32::System::Memory::{GlobalLock, GlobalSize, GlobalUnlock};
    use windows_sys::Win32::System::Threading::{OpenProcess, QueryFullProcessImageNameW, PROCESS_QUERY_LIMITED_INFORMATION};
    use windows_sys::Win32::UI::Shell::ShellExecuteW;
    use windows_sys::Win32::UI::WindowsAndMessaging::{GetForegroundWindow, GetWindowThreadProcessId, SW_SHOWNORMAL};

    const CF_DIB: u32 = 8;
    /// How long a person may take, and how long it may take to come up.
    const WAIT: Duration = Duration::from_secs(180);
    const START: Duration = Duration::from_secs(8);
    /// After it is gone, the image can still be on its way.
    const LATE: Duration = Duration::from_millis(2500);

    fn wide(text: &str) -> Vec<u16> {
        text.encode_utf16().chain([0]).collect()
    }

    fn address() -> String {
        match std::env::var("MACHINE_SANDBOX_SNIP") {
            Ok(other) if cfg!(feature = "sandbox") && std::path::Path::new(&other).exists() => other, // for smoke/
            _ => "ms-screenclip:".into(),
        }
    }

    pub fn there() -> bool {
        windows_registry::CLASSES_ROOT.open("ms-screenclip").is_ok() || address() != "ms-screenclip:"
    }

    /// Whether its window is the one in front.
    fn picking() -> bool {
        // SAFETY: plain calls; the handle is closed.
        unsafe {
            let mut id = 0;
            GetWindowThreadProcessId(GetForegroundWindow(), &mut id);
            let process = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, id);
            if process.is_null() {
                return false;
            }
            let mut name = [0u16; MAX_PATH as usize];
            let mut length = MAX_PATH;
            let known = QueryFullProcessImageNameW(process, 0, name.as_mut_ptr(), &mut length) != 0;
            CloseHandle(process);
            let name = String::from_utf16_lossy(&name[..length as usize]).to_lowercase();
            let program = name.rsplit('\\').next().unwrap_or_default().to_string();
            known && ["screenclippinghost.exe", "snippingtool.exe", "screensketch.exe", "shellexperiencehost.exe"].contains(&program.as_str())
        }
    }

    pub fn take() -> Result<Option<Vec<u8>>, &'static str> {
        // SAFETY: plain calls; the strings end in 0 and outlive the call.
        let before = unsafe { GetClipboardSequenceNumber() };
        let (open, what) = (wide("open"), wide(&address()));
        // SAFETY: as above.
        let started = unsafe { ShellExecuteW(std::ptr::null_mut(), open.as_ptr(), what.as_ptr(), std::ptr::null(), std::ptr::null(), SW_SHOWNORMAL) };
        if started as usize <= 32 {
            return Err("not there");
        }
        let (start, mut came, mut gone) = (Instant::now(), false, None);
        while start.elapsed() < WAIT {
            std::thread::sleep(Duration::from_millis(150));
            // SAFETY: plain calls.
            if unsafe { GetClipboardSequenceNumber() } != before {
                std::thread::sleep(Duration::from_millis(250)); // every format is on it
                if let Some(image) = read()? {
                    return Ok(Some(image));
                }
            }
            match picking() {
                true => (came, gone) = (true, None),
                false if came && gone.get_or_insert_with(Instant::now).elapsed() > LATE => return Ok(None),
                false if !came && start.elapsed() > START => return Err("not there"),
                false => {}
            }
        }
        Ok(None)
    }

    /// The image on the clipboard, which is empty after.
    fn read() -> Result<Option<Vec<u8>>, &'static str> {
        let png = wide("PNG");
        // SAFETY: plain calls; the clipboard is closed, and its data copied while it is open.
        unsafe {
            let png = RegisterClipboardFormatW(png.as_ptr());
            if IsClipboardFormatAvailable(png) == 0 && IsClipboardFormatAvailable(CF_DIB) == 0 {
                return Ok(None);
            }
            if OpenClipboard(std::ptr::null_mut()) == 0 {
                return Ok(None); // someone else has it: again in a moment
            }
            let image = copy(GetClipboardData(png)).or_else(|| copy(GetClipboardData(CF_DIB)).and_then(|dib| super::png(&dib)));
            EmptyClipboard();
            CloseClipboard();
            image.map(Some).ok_or("no image")
        }
    }

    /// SAFETY: a clipboard handle, while the clipboard is open.
    unsafe fn copy(data: HANDLE) -> Option<Vec<u8>> {
        if data.is_null() {
            return None;
        }
        let (size, from) = (GlobalSize(data), GlobalLock(data) as *const u8);
        if from.is_null() {
            return None;
        }
        let copied = std::slice::from_raw_parts(from, size).to_vec();
        GlobalUnlock(data);
        Some(copied)
    }
}

/// macOS' own, as by Command-Shift-4. Its file is in a folder only its owner can read. (macOS isn't built yet.)
#[cfg(target_os = "macos")]
mod system {
    use std::{fs, os::unix::fs::DirBuilderExt, process::Command};

    pub fn there() -> bool {
        true
    }

    pub fn take() -> std::io::Result<Option<Vec<u8>>> {
        let folder = std::env::temp_dir().join(format!("the-machine-{}", std::process::id()));
        fs::DirBuilder::new().mode(0o700).create(&folder)?;
        let file = folder.join("screenshot.png");
        let done = Command::new("/usr/sbin/screencapture").args(["-i", "-x"]).arg(&file).status();
        let image = fs::read(&file).ok();
        fs::remove_dir_all(&folder)?;
        done.map(|_| image)
    }
}

/// A Windows bitmap (a DIB: its header, then rows of blue, green and red, from the bottom up unless its height is negative)
/// as a PNG.
#[cfg(any(windows, test))]
fn png(dib: &[u8]) -> Option<Vec<u8>> {
    let int = |at: usize| Some(i32::from_le_bytes(dib.get(at..at + 4)?.try_into().ok()?));
    let (header, wide, high) = (int(0)? as usize, int(4)?, int(8)?);
    let (bits, packed) = (u16::from_le_bytes(dib.get(14..16)?.try_into().ok()?), int(16)?);
    let (w, h) = (usize::try_from(wide).ok()?, high.unsigned_abs() as usize);
    if !(40..=200).contains(&header) || w == 0 || h == 0 || w > 32768 || h > 32768 || ![24, 32].contains(&bits) || ![0, 3].contains(&packed) {
        return None;
    }
    if packed == 3 && (int(40)?, int(44)?, int(48)?) != (0xff0000, 0xff00, 0xff) {
        return None; // another order of colors
    }
    let from = header + if packed == 3 && header == 40 { 12 } else { 0 };
    let (each, row) = (bits as usize / 8, (w * bits as usize).div_ceil(32) * 4);
    let rows = dib.get(from..from.checked_add(row.checked_mul(h)?)?)?;
    let mut rgb = Vec::with_capacity(w * h * 3);
    for y in 0..h {
        let line = &rows[row * if high < 0 { y } else { h - 1 - y }..];
        rgb.extend(line[..w * each].chunks_exact(each).flat_map(|p| [p[2], p[1], p[0]]));
    }
    let mut out = Vec::new();
    let mut encoder = png::Encoder::new(&mut out, w as u32, h as u32);
    encoder.set_color(png::ColorType::Rgb);
    encoder.write_header().ok()?.write_image_data(&rgb).ok()?;
    Some(out)
}

#[cfg(test)]
mod tests {
    #[test]
    fn a_bitmap_as_a_png() {
        let dib = |high: i32, bits: u16, packed: u32, rows: &[u8]| {
            let mut d = Vec::new();
            for n in [40i32, 2, high] {
                d.extend(n.to_le_bytes());
            }
            d.extend(1u16.to_le_bytes());
            d.extend(bits.to_le_bytes());
            d.extend(packed.to_le_bytes());
            d.extend([0; 20]);
            if packed == 3 {
                for n in [0xff0000u32, 0xff00, 0xff] {
                    d.extend(n.to_le_bytes());
                }
            }
            d.extend(rows);
            d
        };
        let pixels = |png: Vec<u8>| {
            let mut reader = png::Decoder::new(std::io::Cursor::new(png)).read_info().unwrap();
            let mut px = vec![0; 12];
            reader.next_frame(&mut px).unwrap();
            px
        };
        let (red, green, blue, white) = ([0, 0, 255], [0, 255, 0], [255, 0, 0], [255, 255, 255]);
        let wanted = [255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255];
        // From the bottom up, each row to a multiple of four bytes
        let rows: Vec<u8> = [&blue[..], &white, &[0, 0], &red, &green, &[0, 0]].concat();
        assert_eq!(pixels(super::png(&dib(2, 24, 0, &rows)).unwrap()), wanted);
        let rows: Vec<u8> = [red, green, blue, white].iter().flat_map(|p| [p[0], p[1], p[2], 0]).collect();
        assert_eq!(pixels(super::png(&dib(-2, 32, 0, &rows)).unwrap()), wanted);
        assert_eq!(pixels(super::png(&dib(-2, 32, 3, &rows)).unwrap()), wanted);
        assert!(super::png(&dib(2, 32, 0, &rows[..8])).is_none() && super::png(&dib(2, 8, 0, &rows)).is_none() && super::png(&[40]).is_none());
        assert!(super::png(&dib(i32::MIN, 32, 0, &rows)).is_none());
    }
}
