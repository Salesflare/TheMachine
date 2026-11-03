// deploy/cdp-relay.mjs: the one shared DevTools connection to desktop Chrome. Loaded without its server and with fake
// sockets and timers, so nothing listens and no Chrome is reached.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const source=readFileSync(new URL('../deploy/cdp-relay.mjs',import.meta.url),'utf8');
const sockets=[],timers=new Map(),answers=[];let nextTimer=0,missing=false,file='9222\n/devtools/browser/test';
class FakeSocket {constructor(url){this.url=url;sockets.push(this)}close(){this.closed=true;this.onclose?.()} }
const context=vm.createContext({WebSocket:FakeSocket,fs:{readFileSync(){if(missing)throw Error('missing');return file}},process:{env:{HOME:'/fixture'}},console:{log(){}},
 setTimeout(fn){const id=++nextTimer;timers.set(id,fn);return id},send(c,m){answers.push(JSON.parse(m))}});
vm.runInContext(source.slice(0,source.indexOf('// Minimal WebSocket server')).replace(/^import .*;$/gm,''),context);
const run=()=>{assert.equal(timers.size,1);const [id,fn]=[...timers][0];timers.delete(id);fn()};
vm.runInContext('connectUp();connectUp()',context);assert.equal(sockets.length,1);
assert.equal(sockets[0].url,'ws://127.0.0.1:9222/devtools/browser/test','the port and path Chrome wrote');
for(let i=0;i<100;i++) {const ws=sockets.at(-1);ws.onerror();ws.onclose();assert.equal(timers.size,1);assert(ws.closed);run();assert.equal(sockets.length,i+2);}
const current=sockets.at(-1);current.onopen();vm.runInContext('connectUp()',context);assert.equal(timers.size,0);assert.equal(sockets.length,101);
vm.runInContext("routes.set(1,[{},42])",context);current.onerror();current.onclose();assert.equal(answers.length,1);assert.equal(answers[0].id,42);run();
const replacement=sockets.at(-1);replacement.onopen();current.onopen();assert(current.closed);assert.equal(vm.runInContext('up === connecting',context),false);
replacement.onclose();missing=true;run();assert.equal(timers.size,1);missing=false;run();assert.equal(timers.size,0);
// A DevToolsActivePort that doesn't look like Chrome's is never connected to; it is read again later.
sockets.at(-1).onclose();file='9222\nws://elsewhere.example/x';const before=sockets.length;run();assert.equal(sockets.length,before);assert.equal(timers.size,1);file='9222\n/devtools/browser/test';run();
// Only programs on this computer, never a web page: a handshake with an Origin, or for another Host, is refused.
const allowed=headers=>vm.runInContext(`allowed(${JSON.stringify(headers)})`,context);
assert.equal(allowed({host:'127.0.0.1:9333'}),true);
assert.equal(allowed({host:'localhost:9333'}),true);
assert.equal(allowed({host:'127.0.0.1:9333',origin:'https://evil.example'}),false,'a site open in a browser here');
assert.equal(allowed({host:'127.0.0.1:9333',origin:'null'}),false,'a sandboxed frame or a file');
assert.equal(allowed({host:'evil.example:9333'}),false,'DNS rebinding');
assert.equal(allowed({}),false);
console.log('CDP relay: error+close owns one reconnect; pending connections stay single; outstanding requests fail once; web pages are refused');
