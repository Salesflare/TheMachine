// Keeps ONE approved DevTools connection to your desktop Chrome and shares it with programs on this computer, so
// Chrome's "Allow remote debugging?" prompt appears once per Chrome start, not once per script or agent run.
// Clients connect to ws://127.0.0.1:9333 (CDP_RELAY_PORT). Only clients that are not web pages: like Chrome's own
// DevTools port, a handshake with an Origin header (every browser page sends one) or another Host is refused, so a
// site open in any browser here can't drive your Chrome. Run it as a user service: deploy/cdp-relay.service.
import http from 'node:http';
import fs from 'node:fs';
import crypto from 'node:crypto';
const PORT = Number(process.env.CDP_RELAY_PORT || 9333);
const FILE = process.env.CHROME_DEVTOOLS_FILE || process.env.HOME + '/.config/google-chrome/DevToolsActivePort';
let up = null, connecting = null, reconnectTimer = null, nextId = 1;
const routes = new Map();          // upstream id -> [client, original id]
const clients = new Set();
const sessions = new Set();       // CDP sessions clients attached through the shared connection

function scheduleReconnect() {
  if (reconnectTimer !== null || up || connecting) return;
  reconnectTimer = setTimeout(() => { reconnectTimer = null; connectUp(); }, 5000);
}
function connectUp() {
  if (up || connecting) return;
  let port, path;
  try { [port, path] = fs.readFileSync(FILE, 'utf8').split('\n'); }
  catch { scheduleReconnect(); return; }
  if (!/^\d+$/.test(port) || !/^\/devtools\/browser\/[\w-]+$/.test(path)) { scheduleReconnect(); return; }
  let ws;
  try { ws = new WebSocket(`ws://127.0.0.1:${port}${path}`); }
  catch { scheduleReconnect(); return; }
  connecting = ws;
  let ended = false;
  const disconnected = () => {
    // WebSocket emits error AND close for one failed attempt. They own one retry.
    if (ended) return;
    ended = true;
    if (connecting === ws) connecting = null;
    if (up === ws) {
      up = null;
      for (const [c, id] of routes.values())
        send(c, JSON.stringify({ id, error: { code: -32000, message: 'Chrome connection closed' } }));
      routes.clear();
    }
    try { ws.close(); } catch {}
    scheduleReconnect();
  };
  ws.onopen = () => {
    if (ended || connecting !== ws) { try { ws.close(); } catch {} return; }
    connecting = null; up = ws; console.log('upstream connected');
  };
  ws.onmessage = e => {
    if (up !== ws) return;
    const m = JSON.parse(e.data);
    if (m.method === 'Target.attachedToTarget') sessions.add(m.params.sessionId);
    else if (m.method === 'Target.detachedFromTarget') sessions.delete(m.params.sessionId);
    else if (m.result?.sessionId) sessions.add(m.result.sessionId);
    if (m.id && routes.has(m.id)) { const [c, id] = routes.get(m.id); routes.delete(m.id); m.id = id; send(c, JSON.stringify(m)); }
    else for (const c of clients) send(c, e.data);
  };
  ws.onclose = ws.onerror = disconnected;
}

// Sessions and auto-attach live on the shared upstream connection, so they outlive the client
// that made them. Auto-attach with waitForDebuggerOnStart then freezes every new frame or popup
// in Chrome. Once the last client leaves, switch auto-attach off and detach what is left.
function reset() {
  if (!up) return;
  const call = (method, params, sessionId) => up.send(JSON.stringify({ id: nextId++, method, params, sessionId }));
  call('Target.setAutoAttach', { autoAttach: false, waitForDebuggerOnStart: false, flatten: true });
  call('Target.setDiscoverTargets', { discover: false });
  for (const sessionId of sessions) { call('Runtime.runIfWaitingForDebugger', undefined, sessionId); call('Target.detachFromTarget', { sessionId }); }
  sessions.clear();
}

// A program on this computer, not a web page: no Origin header, and the Host it asked for is this relay's own.
function allowed(headers) {
  if (headers.origin !== undefined) return false;
  return [`127.0.0.1:${PORT}`, `localhost:${PORT}`, `[::1]:${PORT}`].includes(String(headers.host || '').toLowerCase());
}

// Minimal WebSocket server (text frames only) so this needs no npm packages.
function send(sock, text) {
  const b = Buffer.from(text); let h;
  if (b.length < 126) h = Buffer.from([0x81, b.length]);
  else if (b.length < 65536) { h = Buffer.alloc(4); h[0] = 0x81; h[1] = 126; h.writeUInt16BE(b.length, 2); }
  else { h = Buffer.alloc(10); h[0] = 0x81; h[1] = 127; h.writeBigUInt64BE(BigInt(b.length), 2); }
  if (!sock.destroyed) sock.write(Buffer.concat([h, b]));
}
const server = http.createServer((q, r) => { if (!allowed(q.headers)) { r.statusCode = 403; r.end(); return; } r.end(JSON.stringify({ up: !!up, connecting: !!connecting, reconnectPending: reconnectTimer !== null, clients: clients.size })); });
server.on('upgrade', (req, sock) => {
  if (!allowed(req.headers) || !req.headers['sec-websocket-key']) { sock.end('HTTP/1.1 403 Forbidden\r\nConnection: close\r\n\r\n'); return; }
  const key = crypto.createHash('sha1').update(req.headers['sec-websocket-key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest('base64');
  sock.write(`HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ${key}\r\n\r\n`);
  clients.add(sock); let buf = Buffer.alloc(0), parts = [];
  sock.on('data', d => {
    buf = Buffer.concat([buf, d]);
    for (;;) {
      if (buf.length < 2) return;
      let len = buf[1] & 127, off = 2;
      if (len === 126) { if (buf.length < 4) return; len = buf.readUInt16BE(2); off = 4; }
      else if (len === 127) { if (buf.length < 10) return; len = Number(buf.readBigUInt64BE(2)); off = 10; }
      const masked = buf[1] & 128, mask = masked ? buf.subarray(off, off + 4) : null; if (masked) off += 4;
      if (buf.length < off + len) return;
      const p = Buffer.from(buf.subarray(off, off + len)); if (mask) for (let i = 0; i < p.length; i++) p[i] ^= mask[i % 4];
      const fin = buf[0] & 128, op = buf[0] & 15; buf = buf.subarray(off + len);
      if (op === 8) { sock.end(); return; }
      if (op === 9 || op === 10) continue;
      parts.push(p); if (!fin) continue;
      const text = Buffer.concat(parts).toString(); parts = [];
      const m = JSON.parse(text);
      if (!up) { send(sock, JSON.stringify({ id: m.id, error: { message: 'Chrome not connected (approve the prompt)' } })); continue; }
      const id = nextId++; routes.set(id, [sock, m.id]); m.id = id; up.send(JSON.stringify(m));
    }
  });
  const gone = () => { if (clients.delete(sock) && !clients.size) reset(); };
  sock.on('close', gone); sock.on('error', gone);
});
server.listen(PORT, '127.0.0.1', () => console.log('relay on 127.0.0.1:' + PORT));
connectUp();
