// Everything the box asks of the app around it, in one place: box.js knows no Tauri. As a page of the Machine's, this
// file becomes its own fetches to api/action, and only the window's part (fit, close, openDashboard) stays native.
(function () {
  'use strict';
  const {core: {invoke}, event: {listen}} = window.__TAURI__;
  window.Native = {
    state: () => invoke('box_state'),
    look: () => invoke('box_look'),
    fit: height => invoke('box_fit', {height}),
    draft: there => invoke('box_draft', {there}),
    close: () => invoke('box_close'),
    signIn: () => invoke('sign_in'),
    given: () => invoke('box_given'),
    connect: address => invoke('connect', {address}),
    addTodo: (text, draft, files) => invoke('add_todo', {text, draft, files}),
    addFile: (draft, name, data) => invoke('add_file', {draft, name, data}),
    removeFile: (draft, id) => invoke('remove_file', {draft, id}),
    screenshot: () => invoke('take_screenshot'),
    quick: todo => invoke('todo_quick', {todo}),
    decide: (todo, act, until) => invoke('todo_decide', {todo, act, until: until ?? null}),
    undo: (todo, act) => invoke('todo_undo', {todo, act}),
    ask: (text, before) => invoke('ask', {text, before}),
    openDashboard: todo => invoke('open_dashboard', {todo: todo ?? null}),
    cardOpen: todo => invoke('card_open', {todo}),
    cardPlace: (top, height) => invoke('card_place', {top, height}),
    cardClose: () => invoke('card_close'),
    setSpeaks: when => invoke('set_speaks', {when}),
    menuItem: id => invoke('menu_item', {id}),
    onOpened: run => listen('opened', run),
    onListed: run => listen('listed', run),
    onGiven: run => listen('given', run),
    onFailed: run => listen('failed', e => run(e.payload)),
    onCard: run => listen('card', e => run(e.payload)),
    onTall: run => listen('tall', e => run(e.payload)),
    onSignIn: run => listen('signin', e => run(e.payload)),
  };
})();
