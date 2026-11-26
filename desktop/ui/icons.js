// What the windows share: the pictures by path, as the dashboard's, when a snooze is until, and what is dropped on them.
(function () {
  'use strict';
  const t = window.MachineText;
  const ICONS = {
    prepare: 'M5 3.2l7.5 4.8L5 12.8z', done: 'M3 8.4l3.3 3.3L13 5', snooze: 'M8 2.2a5.8 5.8 0 1 0 0 11.6A5.8 5.8 0 0 0 8 2.2M8 5v3.2l2.1 1.3', close: 'M4 4l8 8M12 4l-8 8',
    file: 'M13 7.5l-4.9 4.9a3 3 0 0 1-4.3-4.3l5.3-5.2a2 2 0 0 1 2.8 2.8L6.7 11a1 1 0 0 1-1.4-1.4l4.6-4.6', shot: 'M2 5.2V3.5A1.5 1.5 0 0 1 3.5 2h1.7M10.8 2h1.7A1.5 1.5 0 0 1 14 3.5v1.7M14 10.8v1.7a1.5 1.5 0 0 1-1.5 1.5h-1.7M5.2 14H3.5A1.5 1.5 0 0 1 2 12.5v-1.7M8 5.6a2.4 2.4 0 1 0 0 4.8 2.4 2.4 0 0 0 0-4.8',
  };
  ICONS.snooze2h = ICONS.snooze;
  function icon(name) {
    const at = 'http://www.w3.org/2000/svg', svg = document.createElementNS(at, 'svg'), path = document.createElementNS(at, 'path');
    svg.setAttribute('viewBox', '0 0 16 16');
    svg.setAttribute('aria-hidden', 'true');
    path.setAttribute('d', ICONS[name]);
    svg.append(path);
    return svg;
  }
  const fill = (text, v) => text.replace('{}', () => v);
  function when(until, hour12) {
    const at = until ? new Date(until) : null;
    if (!at || isNaN(at)) return '';
    const day = v => new Date(v).setHours(0, 0, 0, 0), days = Math.round((day(at) - day(Date.now())) / 864e5);
    const time = hour12 ? at.toLocaleTimeString([], {hour: 'numeric', minute: '2-digit', hour12}) : at.getHours() + ':' + String(at.getMinutes()).padStart(2, '0');
    return days <= 0 ? time : days === 1 ? fill(t.tomorrow, time) : at.toLocaleDateString([], days < 7 ? {weekday: 'long'} : {day: 'numeric', month: 'short'}) + ' ' + time;
  }
  // Files, else a link with its name, else text. Read at once: a drop's data is gone after its event
  const takes = data => [...(data?.types || [])].some(x => x === 'Files' || x === 'text/uri-list' || x === 'text/plain');
  function dropped(data) {
    const files = [...(data?.files || [])], read = kind => (files.length ? '' : data?.getData(kind) || '').replace(/\r\n?/g, '\n').trim();
    const link = read('text/uri-list').split('\n').find(l => /^https?:\/\//i.test(l)), text = read('text/plain');
    const [, name] = read('text/x-moz-url').split('\n');
    return {files, text: link ? [name?.trim() !== link && name?.trim(), link].filter(Boolean).join('\n') : /^file:/i.test(text) ? '' : text};
  }
  const base64 = f => new Promise((ok, no) => {
    const r = new FileReader();
    r.onload = () => ok(String(r.result).split(',')[1] || '');
    r.onerror = no;
    r.readAsDataURL(f);
  });
  // What starts soon. The first guest's first name, or the meeting's own name where none has one. A Machine without title
  // says both in who: there several words are the meeting's own
  const minutes = at => Math.round((new Date(at) - Date.now()) / 60000);
  function soon({at, who, others, join, title}) {
    const name = !who ? title : title == null && /\s/.test(who) ? who : fill(join ? t.callWith : t.meetingWith, others ? fill(others === 1 ? t.andOne : t.andMore.replace('{n}', others), who) : who);
    const left = minutes(at);
    return (name || (join ? t.call : t.meeting)) + ' ' + (left > 0 ? fill(t.inMinutes, left) : t.now);
  }
  // A title and a line, of what the robot says
  const said = say => (say.meeting ? [soon(say.meeting), ''] : [say.title, say.line]);
  window.Parts = {icon, minutes, said, when, fill, takes, dropped, base64, MAX_FILES: 5, MAX_BYTES: 10 * 1024 * 1024};
})();
