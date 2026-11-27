# The Machine on the desktop (prototype)

The Machine's robot stands in a corner of the screen, above other windows. A click opens a small box: add a to-do (with
files or a screenshot), ask about your messages, and see the first of For you, with the quick buttons of each one's
notification. A dot shows when something is new since you last looked.
The dashboard, the phone app and the Machine don't change for it. Off means not started. Its builds come with The
Machine's releases (**Install it**).

It never sends or approves anything itself. A to-do opens as the dashboard shows it, where its draft is read first. It starts with
nothing of its own: no start at login unless you turn that on, no hotkey. On Windows it has an icon by the clock while it runs, with the same dot
(Windows may put it behind the arrow there), and on a Mac one in the menu bar.

It is also an app with the dashboard in a window of its own, and the robot is a setting of it (**The window**).

**Quick buttons.** On a row, with the mouse over it or the keys in it: those of its notification on Android that do
something (Do it, Snooze, Mark done), in your Machine's words. Snooze offers the to-do's own choices, as the dashboard's
picker does; **Choose date** opens the to-do, where that is. The row then says what happened and until when, with Undo, and
goes. Your Machine takes nothing else from them. A Fleet item and a board's follow-ups have none.

**Being prepared.** After Do it the row stays and says how it goes in the dashboard's own words (Preparing…, Working…,
Prepared, Needs you, Stuck), with a moving sign while your Machine is on it. So does a row it was already on, or that was
started elsewhere. Do it is off meanwhile, and the row has the buttons of its new state after.

**Just added.** A to-do added here is the first row at once, lit for a moment, with "Just added" and the dashboard's own
word for its state under it, which follows while the box is open. The count stays the dashboard's: one it has outside For
you stands under its own "Just added" line. Next time the box opens it is a row like any other. If it isn't taken, its
text and files come back to the box. The dashboard has no Undo for adding, so there is none here. A question
takes the list's place, with its answer under it. While an answer is there, the next question goes with the last three
you asked, so it can go on from them; To-do, signing out and quitting start afresh. They are kept nowhere on this computer.

**Screenshots.** **+**, **Take a screenshot**: you pick an area or a window with the system's own tool while the robot and
its box are away, and see it in the box before you add the to-do. Remove it there and it goes from your Machine too.
Windows: its own snip (Windows itself may also keep the image, as its settings say). Linux: the desktop's portal, where it
has one that lets you pick. Mac: the picker of Command-Shift-4; the first time macOS asks whether The Machine may record
the screen, and only then. After a no, the box says where to allow it.

**Drop anything on it.** Files, an image, a link or selected text, dropped on the robot or its box: the box opens with it.
Text and links stand in the field, for To-do or Ask; files are attached as with **+**, up to 5 of 10 MB, to a to-do. Nothing
becomes a to-do or a question before you say so. A folder isn't taken. On GNOME with Wayland the robot is an X11 window,
and selected text from a Wayland app may not arrive there; files and links do.

**The dot.** Something came into For you, became ready, needs you, or became due today, since the box was open or the
dashboard's app was in front on this computer, or a to-do was opened from the box. Opening the box takes it away. A
dashboard in a browser's tab isn't seen by it. To know this it keeps fingerprints of what was there, not what it was.

## Install it

Each release of The Machine that changes the app has its builds on a
[GitHub release](https://github.com/Salesflare/TheMachine/releases/latest), signed (**Releases**, below). The newest is
always at `https://github.com/Salesflare/TheMachine/releases/latest/download/` followed by the file's name.

Windows (10 or 11, 64-bit): `the-machine-desktop-setup.exe`, signed by Salesflare BV. It installs for you alone, without an
administrator, in `%LOCALAPPDATA%\The Machine`, and updates itself. On a computer where nothing used WebView2 before, the
installer takes a few seconds more to get it ready, so the app's first start is as quick as the next ones.

Mac (macOS 13 or newer, Apple silicon or Intel): `the-machine-desktop-mac.zip`, signed and notarized. Unpack it, move
**The Machine** to Applications and open it there. macOS asks once whether you want to open an app from the internet:
**Open**. Its window opens to sign in, and the robot stands in its corner when another program is in front. It updates itself.

Linux (64-bit, x86_64). The AppImage updates itself; the .deb and the Arch package are updated as they were installed, and
Settings says when a newer one is out.

- **Any distribution**: `the-machine-desktop-x86_64.AppImage` brings what it needs, gtk-layer-shell too (built by CI from
  its source, `LAYER_SHELL` in `desktop.yml`). `chmod +x` it and
  start it. It needs FUSE's `fusermount3` (or the older `fusermount`), which most desktops have; no libfuse. If it says
  FUSE is missing, install `fuse3`. Kept in a folder of yours (`~/Applications`, say), it updates itself.
- **Ubuntu and Debian** (Ubuntu 22.04, Debian 12 or newer): `sudo apt install ./the-machine-desktop-amd64.deb`, which also
  installs WebKitGTK 4.1 and gtk-layer-shell. It is in the applications menu as The Machine; `the-machine-desktop` starts it too.
- **Arch and Omarchy**: download `PKGBUILD` into an empty folder and run `makepkg -si` there. It fetches that release's .deb,
  checks it against the checksum in the file, and installs it as `the-machine-desktop-bin` with WebKitGTK 4.1 and
  gtk-layer-shell. A newer release: the same with its `PKGBUILD`. It isn't in the AUR yet. On Hyprland (Omarchy's), Sway and
  KDE the robot is a layer surface, above other windows and without a window of its own (**How it is made**); nothing to set
  for it. Where the gtk-layer-shell (the AppImage's or the system's) isn't known to work with the system's GTK, the app is an
  XWayland window instead, as on GNOME: such a one crashed the app when a tooltip or menu opened.

To try a build that isn't released: the newest run of
[Desktop prototype](https://github.com/Salesflare/TheMachine/actions/workflows/desktop.yml) has
`the-machine-desktop-windows` and `the-machine-desktop-mac` (signed, from this branch or main), the unsigned ones of a pull
request (`-unsigned`: Windows warns, **More info**, **Run anyway**; macOS stops it: **Done**, then System Settings, Privacy &
Security, **Open Anyway**), `the-machine-desktop-linux` and `the-machine-desktop-arch` (the package, for `sudo pacman -U`).

To build it yourself (below), it needs WebKitGTK 4.1 and gtk-layer-shell (`libgtk-layer-shell.so.0`, from
the system or in `lib/` next to the program); start `target/release/the-machine-desktop`. The one in `lib/` is read-only: a
plain `cp` over a running robot's library would crash it, so it is refused. Replace it with a new file (`cp -f`, `install`,
`mv`, `tar`).

On Windows it needs no administrator: started as one, it starts again as you. There is only ever one: another start, also of a
copy elsewhere, brings the one that runs forward.

The robot stands in the bottom right corner, and the first time the window opens by itself to sign in:

- **Sign in** opens your account in your browser and comes back, for a hosted Machine or one on The Machine Network. When
  nothing came back after 20 seconds, it says so: **Try again**.
- **Self-hosted?** takes your Machine's own address. Like the dashboard, it only works where you are its owner: a computer
  on your Tailscale network.

The box greets you by the first name your Machine knows, by this computer's clock, and says so when nothing needs you; or
that you aren't signed in, or that your Machine doesn't answer. Click the robot to open and close it, and drag the robot to
move it, also to another monitor. Until you drag it, it stands on the monitor the app's window is on, or was on when you
minimized or closed it; else on the main one. Dragged, it stays where you put it, and goes back to that rule when that
monitor isn't there. On Wayland's layer shell (Hyprland, Sway, KDE) a window can't tell where it is, so there it is the
main one. The box comes above it, below it where that fits better, or else beside it.
On Windows all of it grows with your Text size (Settings, Accessibility), as far as the screen has room. Right-click it, or **...** in the box, for where you are signed in, **Open dashboard**,
**Hide**, **Sign out** and **Quit**. For a key of your own, bind it to the program with `--toggle`.

A hidden robot never goes away altogether: it looks over the bottom edge of the screen, dot and all. Click it and it is
back where it stood; so do a click on its icon by the clock (Windows), **Show robot** in its menu bar menu (Mac) and
starting the program again. The first time, the box says so.

## The window

The app's icon, **Open dashboard** and a to-do opened from the box open the dashboard in a window of the app's own: the
same page as in a browser, signed in as the robot is, with no second sign-in and none of the app's commands.

- **Links** to elsewhere open in the browser, mail addresses in the mail app, and your account's pages in the browser. A
  link to a place in the dashboard stays in the window.
- **Files** open in a window of their own (Command-S, elsewhere Ctrl+S, keeps a copy), and downloads land in Downloads,
  under a name that is free there.
- **What a browser has around a page**: copy and paste, Command-F or Ctrl+F to find, zoom, full screen (F11 on Windows and
  Linux), choosing and dropping files, questions a page asks, and the microphone for Talk and dictation, for which macOS asks
  you once. Size, place and zoom are kept. On Linux a right-click on the page has find, Settings and quit too.
- **Settings** (Command-comma, Ctrl+comma): **Show the robot**, **Notifications** (only without the robot), **Start at
  login** and what closing the window does: **Keep running** (the usual) or **Quit**. Without the robot it is a plain app: no
  robot, no icon in a Mac's menu bar. On Windows its icon by the clock stays, as that is how it opens and quits.
- **Notifications**, without the robot: what the robot would have said, as the system's own, while the app runs and isn't in
  front. A click opens the to-do. They turn on when you turn the robot off (macOS asks you then), unless you turned them off
  before. With the robot there are none, so nothing comes twice. The number on its Dock icon (Mac) or taskbar button (Windows)
  is For you's. On Windows it looks as the dashboard's does when installed as an app: white on a dark circle, up to 99, then
  99+ (drawn by tools/badges.py).
- **Not reachable, off or starting, signed out, or moved to another address**: the window says so and how to go on. A Machine
  that is off (a hosted one that is paused, or still starting) is not signed out: your sign-in stays on this computer, and
  the box and the window are back by themselves within half a minute of it being on. A hosted Machine's window has a link to
  your account, which says why it is off.

The robot is away while the window is in front. At login only the robot comes, no window.

## For you

The list, its order and its count are the dashboard's For you, with your Work or Personal filter: the first three, then
how many more. The robot runs the dashboard's own rules on the Machine's own answer, so nothing is worked out twice. It
asks every 30 seconds, when the box opens and when you leave the app, and a look of the robot's doesn't count as opening
the dashboard. Follow-ups of a board and Fleet items open with the dashboard.

## It speaks up

When a to-do's notification would buzz on this computer, the robot says it in a small bubble instead: the notification's
own title and line, and its buttons (Open, Do it, Snooze with its choices, Mark done; never Send). It stays until
the mouse or the keyboard is touched, then about 12 seconds more, not while the mouse is on it, and the dot stays. Where the
system doesn't tell that (a Linux desktop without `ext-idle-notify-v1`, GNOME's idle monitor or X11's screen saver) it stays
about 12 seconds. It makes no sound and never takes the keys. **Speak up** in
**...** says when: **Always** (to start with), **Not in Do Not Disturb** or **Never** (a Mac has
Always and Never).

- **What and when is your Machine's.** Hours, the day's cap, batches, hidden text, the kinds you turned off, a dashboard in
  use: all decided before, as for every notification (`machine/delivery/desk.py`). The robot only says with its usual look,
  every 30 seconds, that it is there and may speak. So a bubble comes up to 30 seconds after the phone's push.
- **Never twice on one computer.** While the robot may speak, your Machine doesn't push to the browser or app on the
  robot's computer. Which one that is it knows after the robot has opened the dashboard there once; until then it stays
  quiet if a browser that may be there has notifications on: one on the same system, and not on another robot's computer.
  Settings then asks **Does a browser on this computer notify you too?** **Yes, open it** opens the dashboard there, and
  your Machine knows. **No** holds until another such browser turns them on. Without the robot a notification asks it
  once. A second browser with notifications on this computer still shows its own. Phones and other computers get theirs as ever.
- **It may not speak** while it is hidden, off, or away for the app or something in full screen; nor, where the system
  tells without a permission, while the screen is locked or presented. Windows: the lock screen and screen saver, an app
  or game in full screen, presentation mode, duplicated displays, or no mouse and keys for 5 minutes. Linux: a lock the
  sign-in manager knows of, as GNOME's and KDE's, or Hyprland. Mac: the lock screen, an app in full screen, mirrored displays,
  or no mouse and keys for 5 minutes. That the screen is shared in a call no system tells an app like this. A bubble that is there
  stays behind a lock and waits for who comes back; it goes when something is full screen, presented or mirrored.
- **The dashboard open, but not in front:** it speaks. In front it doesn't.
- **Notifications switched off** on the computer don't keep it quiet. **Do Not Disturb** does only with **Not in Do Not
  Disturb**: on Windows 11 (23H2 and later; Focus turns it on too; also the first hour of a new account, which Windows
  keeps quiet), KDE, dunst, mako (a mode named do-not-disturb or dnd) and GNOME. Elsewhere the system doesn't tell, and
  it speaks. A Mac tells whether a Focus is on only with a permission, which isn't asked, so there the choice isn't
  offered. GNOME has one switch for both, so there notifications off is Do Not Disturb.
- A robot that may not speak takes nothing. Your Machine pushes to the browser as ever. **Got is shown:** the robot says
  it got one when its bubble shows, or when it was decided before that. One it doesn't say in 90 seconds (the box stayed
  open, the robot went away, an answer was lost on the way) goes to the browser after all, and the robot doesn't say it then.
- **Decided elsewhere**, on the phone or the dashboard: the bubble goes with the robot's next look.
- **A meeting that starts within 10 minutes** and has a briefing from your Machine: who it is with, or its own name,
  and when, **Open brief**, and **Join** for a Zoom, Meet or Teams link. Once. Only while your Machine may push
  reminders, and none for all-day or declined ones; with hidden text it names nobody. **Join** opens the link in the
  browser.
- While the box is open nothing is said, and what its rows showed isn't said after.
- **Why it said nothing:** `speaks.log` next to `app.json` (see [Remove it](#remove-it) for the folder) has the reason with each
  change, and when a bubble showed. Times are UTC. No titles, text or addresses, and it stays under 100 KB.

A Machine without this part gives nothing to say, and nothing changes.

## Opening a to-do

A row opens the to-do in the box, which grows with it, up to a comfortable height: the dashboard's own page of one to-do
(`?compact=1#card=<id>`), with **Back**,
a button for the app, and close. Escape closes what is open in it, then goes back. A to-do that is done or snoozed there
goes back by itself after a few seconds. It is the dashboard, in a web view of its own over the box: signed in as the robot
is, with nothing kept on the disk (its page goes a minute after Back, or with the box), none of the app's commands, and no
way to any other page: a link in it opens the app, or the browser when it isn't your Machine's. A file opens in the browser,
where you may have to sign in, and a mail address in your mail app. What is sent or approved
there is so by you, as in the dashboard. On a Machine whose dashboard hasn't that page (`compact` in `api/session`) the row
opens the app.

What opens outside the box goes to the app's own window, and its files to Downloads or a window of their own. Signing in
stays in the browser.

## Hidden while the app is in front

While the app's window is the one in front, or the dashboard's app that Chrome or Edge installed, the robot and its box are
away, and what you wrote in the box stays. They come back when another window is in front, or that one is minimized or
closed. A robot you hid yourself stays hidden. In an ordinary browser tab the dashboard doesn't hide it.

It finds the installed app where the browser listed it (Linux: the applications menu; Windows: the Start menu and installed
apps; Mac: the app of its own they made, also Brave's and Vivaldi's), only for the Machine you are signed in to. For this the
robot asks the system one thing: which app the window in front belongs to (Windows: the app id of its
taskbar button; X11: its window class; Mac: the program in front). It compares that with the installed app's id and forgets it. It reads no titles
and nothing on the screen, needs no permission, and stores, logs and sends none of it. On Linux this works on X11,
and on Hyprland, which tells what comes to the front on a socket of its own: the robot takes the class from it and drops
the rest. Other Wayland desktops tell a program nothing about other windows, so there the robot stays.

## Browsing through this computer

Sites like LinkedIn refuse sign-ins from a data center, so a hosted Machine's browser can go out through the computer
the app runs on (src/exit.rs, help: browse-through-this-computer). While signed in, the app keeps one connection to its
Machine: `GET /api/exit` with its cookie, upgraded to `tm-exit/1`, over TLS (rustls, the Mozilla roots). On that
connection the Machine asks for a host and port, and the app connects there and carries the bytes both ways, in frames
of a type byte, a stream number and a length (at most 16 KB). The app opens no port of its own.

The app connects only to ports 80 and 443 on public internet addresses, checked after its own DNS lookup: never this
computer, its local network or its IPv6 /64, private, shared, link-local (cloud metadata), test or multicast ranges,
nor the Machine's own address. It keeps to 64 streams, 4 MB/s down, 1 MB/s up and 2 GB a day; a connection gets 10
seconds to open and is dropped after 5 minutes idle. A Machine without it answers 404, and the app asks again in 10
minutes; Settings shows the switch, Let my Machine browse through this computer (on by default), only once its Machine
took the connection. Off says so to the Machine and closes it. While a stream was open in the last 30 seconds, the box
and the icon's tooltip say Your Machine is browsing through this computer. smoke/exit.py runs a real browser through
it on Windows, with `MACHINE_SANDBOX_EXIT_FROM` (sandbox builds only) to let loopback through from 127.0.0.2.

## Quit

To quit: the menu above; on Windows also its icon by the clock, or Alt+F4 after a click on the robot; on a Mac its menu bar
menu, or Command-Q in the box. The program with `--quit` stops it whatever state it is in.

## Updates

On a Mac, on Windows when the installer put it there, and as an AppImage in a folder of the person's own (theirs, and they
may write in it), it looks for a newer version a minute after it starts and once a day, fetches it and waits: **Settings**
has **Restart to update**. The AppImage is renamed away and the newer one written in its place, never over the one that
runs; it then starts from there.

The .deb and the Arch package are their package manager's: the app never replaces what they installed. It looks the same
way, fetches nothing, and **Settings** says that a newer version is out, with **Download** for that release's .deb or
`PKGBUILD` (`sudo apt install ./the-machine-desktop-amd64.deb`, or `makepkg -si`). Anything else, such as a build of your
own or an AppImage unpacked into a folder, is left as it is: take the newer file.

- **What it asks:** one fixed address on GitHub (`tauri.conf.json`). No version, id or account goes with it.
- **What it takes:** only what is signed with the one key it trusts, whose public half is in `tauri.conf.json`.
- **The key** is the secret `DESKTOP_UPDATER_KEY` of this repository's `mac-signing` environment, which pull requests don't
  get, and `desktop-updater-key` in the maintainers' key vault. It has no password. Lost, no installed app can be updated
  any more: people would install a new one by hand.
- **Where:** `releases/latest/download/latest.json`, the newest GitHub release. It names that release's own files, so a
  newer one published meanwhile never pairs a version with another one's file: the Mac's and Windows' as before, and for
  `linux-x86_64` the AppImage, signed as it is downloaded (`updates-sign`, in the same environment).

## Releases

`python3 scripts/release.py cut` signs a release of The Machine (`release-YYYYMMDD-HHMM`). When `desktop/` changed since
the GitHub release that is the latest (or there is none), it starts `Desktop prototype` on main with that tag; else it says
the app is as it was. By hand: `gh workflow run desktop.yml --ref main -f release=<tag>`.

That run first checks the tag: signed with the release key as main's `deploy/release-signers` has it, and on main. Then
every job builds the tag, with its version (`tools/version.py`: `release-20261126-1430` is 2026.1126.1430, so each later
release is a newer version), uses it as for a pull request, and signs it: Developer ID and Apple's notarization, Azure
Artifact Signing, and the update key. Only when all of that passed, `publish` puts the files on a GitHub release of the tag,
marked latest: `the-machine-desktop-setup.exe`, `the-machine-desktop-mac.zip`, `the-machine-desktop-mac.app.tar.gz` (for
updates), `latest.json`, the AppImage and its `.sig`, the .deb, `PKGBUILD` with that release's tag and checksum, the Arch package and
`SHA256SUMS`. A run that fails publishes nothing; the app stays at the release before.

Each of those files has GitHub's build provenance: a signed statement that this workflow made it, from that tag. To check a
download: `gh attestation verify <file> -R Salesflare/TheMachine`.

The AppImage's runtime, the small program in front of its files that mounts them, is the static one of
[type2-runtime](https://github.com/AppImage/type2-runtime), a release named with its checksum in `desktop.yml`:
`linux/runtime.py` puts it in place of the one Tauri's tools fetched, and keeps the rest as it was. It mounts with fuse3,
without libfuse2. CI starts it where only fuse3 is: Ubuntu 24.04, and Arch.

Windows: `windows/installer.json` and `windows/hooks.nsh` make the installer, `windows/sign.ps1` signs the program, the
installer and the uninstaller with Azure Artifact Signing, and `windows/verify.ps1` checks the installer and the program in it are
signed by Salesflare BV with a timestamp. The `windows-signing` environment, open only to this branch and main, holds IDs only
(`ARTIFACT_SIGNING_CLIENT_ID`, `_TENANT_ID`, `_SUBSCRIPTION_ID`, `_ENDPOINT`, `_ACCOUNT`, `_PROFILE`); without a profile
nothing is signed. GitHub's own word that the job runs in that environment opens it: no key or password is kept, and Azure
lets it sign with that one profile and do nothing else. A run by hand can skip the Mac with **windows-only**.

## When it hangs

It writes a line in `hangs.log` next to `app.json` when it doesn't answer for 5 seconds, or when the robot's page doesn't, with
its version and what it was doing. On a Mac `hang-1.txt` and so on next to it have what its threads were at, without paths or
names. Nothing is sent anywhere. A page of the robot that stays stuck is made again.

## Mac App Store

A build of its own, for macOS 14 and later: `cargo build --release --no-default-features --features store`, then
`STORE=1 mac/bundle.sh`. It runs in the App Sandbox (`mac/store-entitlements.plist`), and the store updates it. Otherwise it
is the same app, except:

- **No updater** and no plans or links to buy one, as in the phone app (`NO_BUY` in `src/dash.rs`, `.no-buy` in the dashboard).
- **One of it:** its socket is in its own container (`src/one.rs`), not in /tmp.
- **Screenshots:** macOS' own picker (ScreenCaptureKit), then one frame of a stream of what was picked (a screenshot of it
  would ask for Screen Recording). It asks for no permission and keeps nothing.
- **Sign-in** comes back to its port only: the sandbox can't claim the link. It says `on=store`, and the account shows it
  nothing to buy.
- **Downloads** go to the person's own Downloads folder, not the container's. The sandbox's WebKit drops a link's own
  download (`<a download>` of the Machine's address), so the page fetches it and saves that (`DOWNLOADS` in `src/dash.rs`).
- **A stuck page** gets a new window; nothing else is stopped. `hangs.log` has no stacks.
- **Installed web apps** open with their own small program, as when a link is dropped on it.
- **No private methods** (App Review): the robot and the box are panels from the moment they are made (a click on
  them leaves the program in front where it is), and WebKit keeps the pages' key in the person's keychain itself. The `mac-store` job fails when its program names one of `mac/store-denied-selectors.txt`.

The `mac-store` job (a run by hand with **mac-store-only**) uses it in the sandbox, signed ad hoc (`smoke/store.py`).
`mac-store-sign` then signs it and makes the `.pkg`, in the `mac-store` environment: `MAS_APP_P12` (Apple Distribution) and
`MAS_INSTALLER_P12` (Mac Installer Distribution) with their `_PASSWORD`s, `MAS_PROVISIONING_PROFILE` (base64), and
`ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8` to check it with App Store Connect. **mac-store-upload** sends it there too,
as the version in **mac-store-version** (App Store Connect's, `1.0` unless given) with the run's number as its build.
Without them nothing is signed. Its ID is `computer.themachine.app`, one listing with the phone app (`mac/bundle.sh`, or the
repository variable `MAS_BUNDLE_ID`); the direct download keeps `computer.themachine.desktop`.

## Remove it

On Windows uninstall it in Settings, Apps: its folders and what it put in the registry go with it. Else quit it, delete the
program, and delete its folders:

| | Address, session, place, `speaks.log`, `hangs.log` | Page cache |
|---|---|---|
| Windows | `%APPDATA%\computer.themachine.desktop` | `%LOCALAPPDATA%\computer.themachine.desktop` |
| Linux | `~/.config/computer.themachine.desktop` | `~/.local/share/computer.themachine.desktop`, `~/.cache/computer.themachine.desktop` |
| Mac | `~/Library/Application Support/computer.themachine.desktop` | `~/Library/Caches/computer.themachine.desktop`, `~/Library/WebKit/computer.themachine.desktop` |

For a hosted Machine, sign it out on your account page too (**Security**).

`app.copy` next to `app.json` is the same, in case that one can't be read: then it is kept as `app.unread`, until you sign
out.

Signing in with an account waits for the browser at a port of this computer (127.0.0.1), for at most 15 minutes: only the
page with that sign-in's own name is taken, and only once. It also registers `computer.themachine.app:` links while the browser is open, and takes that back
when it returns, the app quits or it next starts. After a crash in between, what is left is
`HKCU\Software\Classes\computer.themachine.app` on Windows, and on Linux
`~/.local/share/applications/the-machine-desktop-handler.desktop` with its line in `~/.config/mimeapps.list`. On a Mac the
app itself names them, as every Mac app does: they go with the app.

Its own link, `computer.themachine.desktop://open`, brings it to the front, as starting it again does (`src/link.rs`). It
carries nothing: any other link of that scheme, with a path, a query or a fragment, does nothing. Windows and Linux
register it at every start (`HKCU\Software\Classes\computer.themachine.desktop`, which uninstalling removes; on Linux in
that same handler file); a Mac app names it in its Info.plist.

## How it is made

Tauri 2: a small Rust program and the system's own web view. Three parts, each replaceable without the others:

| Part | Files | Knows |
|---|---|---|
| Windows | `src/windows.rs`, `src/place.rs`, `src/mac.rs` | Where the robot and the box are. Nothing of the Machine. |
| The window | `src/dash.rs`, `src/files.rs`, `src/keys.rs`, `src/mac_app.rs`, `src/windows_app.rs`, `src/linux_app.rs`, `ui/app.*` | Which page it may be, where links and files go, its place. |
| Settings | `src/settings.rs`, `src/login.rs`, `src/notify.rs`, `ui/settings.*` | The app's own choices, not your Machine's. |
| A to-do in the box | `src/card.rs` | Which page it may be, and where its links go. |
| Pages | `ui/` | What is in them. `robot.js` only clicks and drags; `box.js` asks `native.js` for everything. |
| The Machine | `src/machine.rs`, `src/signin.rs`, `src/address.rs`, `src/saved.rs` | The same requests and address rules as the phone app (`mobile/`). |
| A screenshot | `src/snip.rs` | The system's own tool. |
| The dot | `src/seen.rs` | What was there when the person last looked. |
| Speaking up | `src/speak.rs`, `ui/bubble.js` | What waits to be said, and whether the system says not to disturb. |
| The installed app | `src/webapp.rs`, `src/front.rs` | Where it is, how it is started, whether it is in front. |

`ui/for-you.js` is `dashboard/todos-for-you.js` as it is, and `ui/list.js` the few names it needs. When the dashboard's file
changes, copy it again: `tests/test_for_you_rules_dashboard.mjs` compares both, and the two lists for every state.

`src/main.rs` joins them. `build.rs` names every command and `capabilities/` says which window may call which (the to-do's has none); the
pages load nothing from elsewhere (`tauri.conf.json`, `csp`). The address and a hosted Machine's session are in one file only
its owner can read (`app.json` in the folder above).

To a Machine it sends `GET manifest.webmanifest`, `api/session`, `api/status` (with a random name for this robot and whether
it may speak), `api/fleet` and `api/notice`, the page of a to-do open in the box, and the actions
`card_new`, `chat_upload`, `chat_file_remove`, `search_ask` and `decide` (as a notification's buttons do, and Undo), with
the dashboard's own token and Origin. No others.

| | Windows | Linux: layer-shell (Hyprland, Sway, KDE) | Linux: X11, GNOME (XWayland) | macOS |
|---|---|---|---|---|
| Built | yes, by CI | yes, by CI | yes, by CI | yes, by CI |
| On top, no taskbar entry | window flags | layer surface | window hints | a floating panel on every Space; the Dock icon is the window's |
| The dashboard's window | yes | yes | yes | yes |
| Notifications | toasts, with its name and icon in `HKCU\Software\Classes\AppUserModelId` while they are on | the desktop's own (`org.freedesktop.Notifications`), also kept where it keeps them | as beside | Notification Center |
| Full screen | hidden, says nothing | under it; says nothing on Hyprland | the window manager decides; says nothing | beside it; says nothing |
| Away while the app is in front | yes | Hyprland only, by the socket it tells it on | yes, XWayland apps on GNOME only | yes |
| Clicks beside the robot | taken in the window's corners | go through | go through | go through |

## Develop

```bash
scripts/sandbox.sh busy 8870                                  # a Machine with made-up data
cargo run --release --features sandbox --manifest-path desktop/Cargo.toml   # takes http://127.0.0.1:8870 as an address
cargo test --manifest-path desktop/Cargo.toml
```

CI also uses the Windows and the Mac build, with real mouse and keys against a made-up Machine (`smoke/windows.py` and
`smoke/mac.py` the robot, `smoke/window.py` the window, `smoke/text.py` Windows' Text size and scales,
`smoke/signin.py` a sign-in with a second copy or an administrator's beside it,
`smoke/updates.py` the installer and an update; on Ubuntu an older sandbox AppImage that puts a newer one in its place),
and keeps the screenshots with the run. They move the mouse and
change the screen, so they are for a throwaway computer. `smoke/linux.sh` runs `window.py` on a screen that isn't there,
with a home of its own: nothing of the desktop it is started on is seen or touched. Also over https, as a hosted Machine: with a certificate made for that run
(`smoke/certificate.sh`), which only a sandbox build and that computer trust, until it ends.

The Linux builds for people (`linux/bundle.json`, `linux/PKGBUILD`) are started by `smoke/started.py`: the window opens to
sign in, and a start at login has only the robot. On Ubuntu with X11 (`smoke/linux.sh`) the AppImage and the installed .deb;
on Arch the AppImage where nothing of the app is installed, then the package, on Wayland: `smoke/wayland.sh` runs sway
headless, and there the robot has to be a layer surface. Both start the AppImage on FUSE with fuse3 alone. On Ubuntu,
AppArmor's limit on user namespaces is on, as Ubuntu 23.10 and newer and Debian 13 have it, and `smoke/namespaces.sh` checks
that the app and its web view need none: no AppArmor profile is needed for it.

On a Mac, `mac/bundle.sh <folder> target/release/the-machine-desktop` makes the app. CI signs and notarizes the one for
people in a job of its own, which runs none of this repository's code.

On Windows, never make a window from a page's call or a message: it can wait for itself (`later` in `src/main.rs`). The
robot's windows are all made at the start. WebView2's very first start on a computer takes seconds (8 on CI's runner), all
of it while the first of them is made, before anything shows: the installer takes it with `--warm` (`src/warm.rs`,
`windows/hooks.nsh`), and `smoke/windows.py` checks that the first start after it shows within 4 seconds, with no hang.

## Before a release

- The box as a page of the Machine's, so its words come from the catalogs (`i18n/`); `native.js` is the seam.
- A check of the whole hosted sign-in.
- A hotkey for who wants one.
- Talk and dictation: the dashboard has no address that opens Talk yet.

The robot's images come from `brand/` ([TRADEMARKS.md](../TRADEMARKS.md)). The font is Inter (`ui/fonts/Inter-OFL.txt`).
