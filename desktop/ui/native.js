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
    connect: address => invoke('connect', {address}),
    addTodo: (text, draft, files) => invoke('add_todo', {text, draft, files}),
    addFile: (draft, name, data) => invoke('add_file', {draft, name, data}),
    removeFile: (draft, id) => invoke('remove_file', {draft, id}),
    screenshot: () => invoke('take_screenshot'),
    quick: todo => invoke('todo_quick', {todo}),
    decide: (todo, act) => invoke('todo_decide', {todo, act}),
    undo: (todo, act) => invoke('todo_undo', {todo, act}),
    ask: text => invoke('ask', {text}),
    openDashboard: todo => invoke('open_dashboard', {todo: todo ?? null}),
    menuItem: id => invoke('menu_item', {id}),
    onOpened: run => listen('opened', run),
    onListed: run => listen('listed', run),
    onFailed: run => listen('failed', e => run(e.payload)),
    onSignIn: run => listen('signin', e => run(e.payload)),
  };
})();
