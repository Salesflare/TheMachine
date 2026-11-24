# The Machine on the desktop (prototype)

The Machine's robot stands in a corner of the screen, above other windows. A click opens a small box: add a to-do (with
files or a screenshot), ask about your messages, and see the first of For you, with the quick buttons of each one's
notification. A dot shows when something is new since you last looked.
The dashboard, the phone app and the Machine don't change for it. It is not part of a release, and off means not started.

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
takes the list's place, with its answer under it.

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

## Try it

Windows (10 or 11, 64-bit): download `the-machine-desktop-windows-unsigned` from the newest run of
[Desktop prototype](https://github.com/Salesflare/TheMachine/actions/workflows/desktop.yml), unpack it and start
`the-machine-desktop.exe`. It isn't signed, so Windows warns: **More info**, **Run anyway**.

Mac (macOS 13 or newer, Apple silicon or Intel): download `the-machine-desktop-mac` from the newest run of the same
workflow, unpack it, move **The Machine** to Applications and open it there. macOS asks once whether you want to open an app
from the internet: **Open**. Its window opens to sign in, and the robot stands in its corner when another program is in front.
A pull request's build is `the-machine-desktop-mac-unsigned`. macOS stops that one: **Done**, then System Settings,
Privacy & Security, scroll down, **Open Anyway**, and your password.

Linux (64-bit): build it (below), then start `target/release/the-machine-desktop`. It needs WebKitGTK 4.1 and
gtk-layer-shell (`libgtk-layer-shell.so.0`, from the system or in `lib/` next to the program). The one in `lib/` is
read-only: a plain `cp` over a running robot's library would crash it, so it is refused. Replace it with a new file (`cp
-f`, `install`, `mv`, `tar`).

The robot stands in the bottom right corner, and the first time the window opens by itself to sign in:

- **Sign in** opens your account in your browser and comes back, for a hosted Machine or one on The Machine Network.
- **Self-hosted?** takes your Machine's own address. Like the dashboard, it only works where you are its owner: a computer
  on your Tailscale network.

The box greets you by the first name your Machine knows, by this computer's clock, and says so when nothing needs you; or
that you aren't signed in, or that your Machine doesn't answer. Click the robot to open and close it, and drag the robot to
move it, also to another monitor. The box comes above it, below it where that fits better, or else beside it. Right-click it, or **...** in the box, for where you are signed in, **Open dashboard**,
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
  is For you's.
- **Not reachable, signed out or moved to another address**: the window says so and how to go on.

The robot is away while the window is in front. At login only the robot comes, no window.

## For you

The list, its order and its count are the dashboard's For you, with your Work or Personal filter: the first three, then
how many more. The robot runs the dashboard's own rules on the Machine's own answer, so nothing is worked out twice. It
asks every 30 seconds, when the box opens and when you leave the app, and a look of the robot's doesn't count as opening
the dashboard. Follow-ups of a board and Fleet items open with the dashboard.

## It speaks up

When a to-do's notification would buzz on this computer, the robot says it in a small bubble instead: the notification's
own title and line, and its buttons (Open, Do it, Snooze with its choices, Mark done; never Send). It goes after about 12
seconds, not while the mouse is on it, and the dot stays. It makes no sound and never takes the keys. **Speak up** in
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
  or no mouse and keys for 5 minutes. That the screen is shared in a call no system tells an app like this.
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

## Quit

To quit: the menu above; on Windows also its icon by the clock, or Alt+F4 after a click on the robot; on a Mac its menu bar
menu, or Command-Q in the box. The program with `--quit` stops it whatever state it is in.

## Remove it

Quit it, delete the program, and delete its folders:

| | Address, session, place, `speaks.log` | Page cache |
|---|---|---|
| Windows | `%APPDATA%\computer.themachine.desktop` | `%LOCALAPPDATA%\computer.themachine.desktop` |
| Linux | `~/.config/computer.themachine.desktop` | `~/.local/share/computer.themachine.desktop`, `~/.cache/computer.themachine.desktop` |
| Mac | `~/Library/Application Support/computer.themachine.desktop` | `~/Library/Caches/computer.themachine.desktop`, `~/Library/WebKit/computer.themachine.desktop` |

For a hosted Machine, sign it out on your account page too (**Security**).

Signing in with an account registers `computer.themachine.app:` links while the browser is open, and takes that back
when it returns, the app quits or it next starts. After a crash in between, what is left is
`HKCU\Software\Classes\computer.themachine.app` on Windows, and on Linux
`~/.local/share/applications/the-machine-desktop-handler.desktop` with its line in `~/.config/mimeapps.list`. On a Mac the
app itself names them, as every Mac app does: they go with the app.

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
| Built | yes, by CI | yes | yes | yes, by CI |
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
`smoke/mac.py` the robot, `smoke/window.py` the window), and keeps the screenshots with the run. They move the mouse and
change the screen, so they are for a throwaway computer. `smoke/linux.sh` runs `window.py` on a screen that isn't there,
with a home of its own: nothing of the desktop it is started on is seen or touched. Also over https, as a hosted Machine: with a certificate made for that run
(`smoke/certificate.sh`), which only a sandbox build and that computer trust, until it ends.

On a Mac, `mac/bundle.sh <folder> target/release/the-machine-desktop` makes the app. CI signs and notarizes the one for
people in a job of its own, which runs none of this repository's code.

On Windows, never make a window from a page's call or a message: it can wait for itself (`later` in `src/main.rs`). The
robot's windows are all made at the start.

## Before a release

- The box as a page of the Machine's, so its words come from the catalogs (`i18n/`); `native.js` is the seam.
- A check of the whole hosted sign-in.
- A hotkey for who wants one, updates, signing on Windows.
- Talk and dictation: the dashboard has no address that opens Talk yet.

The robot's images come from `brand/` ([TRADEMARKS.md](../TRADEMARKS.md)). The font is Inter (`ui/fonts/Inter-OFL.txt`).
