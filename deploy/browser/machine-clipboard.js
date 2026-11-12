// The Machine: your own clipboard in your server's browser. Ctrl+C / Ctrl+V (Cmd on a Mac) copy and paste
// between your computer and that browser; noVNC's side panel clipboard stays for phones.
//
// Pasting takes the text from the paste event itself (Ctrl+V, Cmd+V, a menu's Paste, a long-press Paste on a phone):
// that needs no clipboard permission. Reading the clipboard (navigator.clipboard.readText) waited on a permission
// prompt that an installed app or a framed viewer often never showed, so Ctrl+V did nothing. That read is only the
// fallback now, for a browser that sends no paste event while the screen has focus. The text goes to the browser
// there as its clipboard, then Ctrl+V pastes it there. It is never logged or kept.
import UI from './app/ui.js';

const CONTROL = 0xffe3, KEYS = {a: 0x61, c: 0x63, v: 0x76, x: 0x78, z: 0x7a};
const mac = /Mac|iPhone|iPad/.test(navigator.platform);
let hooked = null, swallow = null, waiting = null;

setInterval(() => {  // noVNC makes a new connection object on every (re)connect
    if (!UI.rfb || UI.rfb === hooked) return;
    hooked = UI.rfb;
    hooked.addEventListener('clipboard', event => navigator.clipboard?.writeText(event.detail.text).catch(() => {}));
}, 300);

function combo(rfb, key) {
    if (mac) {  // Cmd is Super over there; the browser there copies and pastes with Ctrl
        rfb.sendKey(0xffeb, 'MetaLeft', false);
        rfb.sendKey(0xffe7, 'MetaLeft', false);
    }
    rfb.sendKey(CONTROL, 'ControlLeft', true);
    rfb.sendKey(KEYS[key], 'Key' + key.toUpperCase(), true);
    rfb.sendKey(KEYS[key], 'Key' + key.toUpperCase(), false);
    if (mac) rfb.sendKey(CONTROL, 'ControlLeft', false);
}

function paste(rfb, text) {  // the text as the clipboard over there, then its own Ctrl+V
    if (text) rfb.clipboardPasteFrom(text);
    setTimeout(() => combo(rfb, 'v'), 50);
}

// The screen (noVNC's canvas, or its on-screen keyboard's text box on a phone), or the page itself when nothing
// else has focus; never noVNC's side panel, whose clipboard box pastes as any text box does.
const onScreen = target => {
    const screen = document.getElementById('noVNC_container');
    return !!screen && (screen.contains(target) || target === document.body || target === document.documentElement);
};

window.addEventListener('paste', event => {
    if (!UI.rfb || !onScreen(event.target)) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    waiting = null;
    paste(UI.rfb, event.clipboardData?.getData('text/plain') || '');
}, true);

window.addEventListener('keydown', event => {
    const key = event.key.toLowerCase(), screen = document.getElementById('noVNC_container');
    if (!UI.rfb || !screen?.contains(event.target) || !(mac ? event.metaKey : event.ctrlKey) || event.altKey || !(key in KEYS)) return;
    if (!mac && key !== 'v') return;  // Ctrl already means Ctrl there; only pasting needs your clipboard first
    event.stopImmediatePropagation();  // not to noVNC, which would send it on as a plain key
    swallow = event.code;
    const rfb = UI.rfb;
    if (key !== 'v') {
        event.preventDefault();
        return combo(rfb, key);
    }
    // Ctrl+V / Cmd+V: no preventDefault, so this browser sends its paste event (above) with the text. Only when none
    // comes, read the clipboard, as before.
    const ask = waiting = {};
    setTimeout(() => {
        if (waiting !== ask) return;
        waiting = null;
        (navigator.clipboard?.readText() ?? Promise.reject())
            .then(text => paste(rfb, text), () => paste(rfb, ''));
    }, 100);
}, true);

window.addEventListener('keyup', event => {
    if (event.code === swallow) {
        swallow = null;
        event.preventDefault();
        event.stopImmediatePropagation();
    }
}, true);
