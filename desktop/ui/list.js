// The dashboard's For you, by the dashboard's own rules: for-you.js is its dashboard/todos-for-you.js as it is, and this
// file is the little of the page it names. ../../tests/test_for_you_rules_dashboard.mjs holds both against the dashboard.
'use strict';
class SafeHTML {
  constructor(side) { this.side = side; }
}
const TODO = {CLOSED: ['completed', 'rejected'], OPEN_NOT_SNOOZED: ['pending', 'accepted', 'prepared', 'instructions']}; // machine/todo_states.py
const SENDS = ['doc_reply', 'email', 'intercom', 'linkedin', 'signal', 'slack', 'teams', 'telegram', 'whatsapp', 'x']; // machine/kinds.py
const t = (key, ...args) => (Array.isArray(key) ? key[args.find(a => !isNaN(+a)) == 1 ? 0 : 1] : key).replace(/\{\}/g, () => args.shift() ?? '');
const fuGroupCard = (group, all) => new SafeHTML({title: fuGroupTitle(all), mark: ['follow-ups:' + group, all.some(s => s.status === 'prepared') ? 3 : 1]});
// A to-do's marks for the dot (src/seen.rs): its result is ready, it needs the person, it is due today or late
const due = s => !!s.due && (s.due <= localDay(new Date()) || Date.parse(s.due_at) < Date.now());
const mark = s => [s.id + '@' + cameIn(s), 1 | (placeOf(s) === 'ready' ? 2 : 0) | (s.needs_owner || s.preparation_status === 'blocked' ? 4 : 0) | (due(s) ? 8 : 0)];
let state = {};
// What the dashboard calls a to-do's state (cardState in dashboard/todos-cards.js), and whether it is being worked on
const PREPARING = ['accepted', 'instructions']; // machine/todo_states.py
function stateOf(s) {
  const open = !closed(s) && s.status !== 'snoozed', run = s.preparation_status;
  if (toRead(s)) return ['To read'];
  if (cleanupSettled(s)) return ['Prepared'];
  if (run === 'working' && open) return ['Working…', true];
  if (run === 'blocked' && open) return [s.preparation_error === 'stopped' ? 'Stopped' : s.preparation_questions?.length || s.preparation_browser ? 'Needs your help' : 'Stuck'];
  if (s.early && s.status === 'accepted' && (run || 'queued') === 'queued') return ['Not started yet'];
  if (PREPARING.includes(s.status) && run !== 'handed') return ['Preparing…', true];
  return [{pending: 'Needs you', accepted: 'Accepted', prepared: 'Prepared', rejected: 'Not needed', snoozed: 'Later', instructions: 'Changes requested', completed: 'Done'}[s.needs_owner ? 'pending' : s.status] || ''];
}
// Its row's: that, and the choices of its Snooze ([option, words]), both as the dashboard has them. Plain, whatever came.
const more = s => {
  const [word = '', working] = stateOf(s);
  return {state: word, working: !!working, snooze: (Array.isArray(s.snooze_choices) ? s.snooze_choices : []).filter(c => Array.isArray(c) && c.length === 2 && c.every(x => typeof x === 'string')).slice(0, 8)};
};

// The status the Machine last gave, kept as it came: the next one is what changed since (status_delta.py)
window.ForYou = class {
  // Puts an answer on what is held. False: it doesn't fit, so the whole status is needed.
  take({status, fleet}) {
    const raw = status._since ? deltaJoin(this.raw, status) : status;
    if (!raw) return false;
    this.raw = raw;
    if (fleet) this.fleet = fleet;
    return true;
  }
  // The owner's first name: an older Machine only says it on their first day
  name() { return String(this.raw.first_name || this.raw.greeting?.name || ''); }
  hour12() { return !!this.raw.locale?.hour12; }
  // Every entry of For you in order: a to-do has an id, a Fleet item and a board's follow-ups open with the dashboard.
  all() {
    state = JSON.parse(JSON.stringify(this.raw));
    state.suggestions = Array.isArray(state.suggestions) ? state.suggestions.filter(s => s && s.id) : [];
    wakeDue(state.suggestions);
    const scope = ['work', 'personal'].includes(state.locale?.todo_scope) ? state.locale.todo_scope : 'all';
    const fleet = scope === 'personal' || !state.fleet?.on ? [] : fleetRows(this.fleet).map(r => new SafeHTML({title: r.title, mark: [r.id, 1]}));
    return todoLists(scopeShown(state.suggestions, scope), fleet, state.greeting?.line?.card).fuv.foryou
      .map(x => (x instanceof SafeHTML ? {id: null, ...x.side} : {id: String(x.id), title: x.title, mark: mark(x), ...more(x)}));
  }
  // What was just added in the box, wherever it is now
  added(ids, all) {
    return ids.flatMap(id => {
      const s = (state.suggestions || []).find(x => String(x.id) === id);
      if (!s) return [];
      return [{id, title: String(s.title || ''), ...more(s), listed: all.some(x => x.id === id)}];
    });
  }
  // A Machine whose answer these rules can't read: what is open, rather than nothing
  list() {
    try { return this.all(); } catch (e) {
      return (state.suggestions || []).filter(s => !closed(s) && s.status !== 'snoozed').map(s => ({id: String(s.id), title: s.title, mark: [String(s.id), 1]}));
    }
  }
};
