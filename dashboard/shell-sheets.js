// On a phone every dialog and sheet is the whole screen, like an app's: the title and × stay on top, the buttons stay at
// the bottom (above the home bar), and only what is between scrolls, never the page behind. Its height is what the
// keyboard leaves (--vv-top, --vv-h follow the visual viewport, todos-chat.js), so the buttons stay in reach while typing.
// A wrapper form that holds only the title row sticks, else the row itself; a form that holds the whole dialog fills it,
// so its buttons sit at the bottom. Send: the message grows into the room there is and scrolls inside itself; the ×
// closes, so Cancel goes when there is a Send; the editor is the message, so no Message label over it (screen readers
// still read it). Help: the answers fill the screen, the question box at the bottom. The quick add composer (#new-card)
// stays a sheet on the keyboard and the palette stays under the top bar. Two :not(#…) lift these over each dialog's own
// #id rules. Its own style sheet, after the page's (dashboard.html stays small enough to scan).
document.head.append(Object.assign(document.createElement('style'),{id:'phone-sheets',textContent:`@media(max-width:560px){
  html:has(dialog[open]:modal:not(#palette):not(#new-card)){overflow:hidden}
  dialog:not(#palette):not(#new-card){position:fixed;inset:var(--vv-top,0px) 0 auto;width:100%;max-width:100%;height:var(--vv-h,100dvh);max-height:var(--vv-h,100dvh);margin:0;box-sizing:border-box;padding:0 16px;border:0;border-radius:0;background:var(--surface-2);overflow:auto;overscroll-behavior:contain;scroll-padding:72px 0 96px}
  dialog:not(#palette):not(#new-card)[open]{display:flex;flex-direction:column;gap:0}
  dialog:not(#palette):not(#new-card)[open]>:not(.fr-list){flex-shrink:0}
  dialog:not(#palette):not(#new-card):not(:has(.snooze-heading)){padding-top:calc(16px + env(safe-area-inset-top))}
  dialog:not(#palette):not(#new-card)::backdrop{background:var(--surface-2)}
  dialog:not(#palette):not(#new-card) :is(.snooze-heading,form[method=dialog]:has(>.snooze-heading:only-child)){position:sticky;top:0;z-index:3;background:var(--surface-2)}
  dialog:not(#palette):not(#new-card) .snooze-heading{margin:0 -16px 12px;padding:calc(12px + env(safe-area-inset-top)) 16px 10px;box-shadow:0 1px 0 var(--border)}
  dialog:not(#palette):not(#new-card)>form[method=dialog]:has(>.snooze-heading:only-child){margin:0 -16px;padding:0 16px}
  dialog:not(#palette):not(#new-card)>form[method=dialog]:has(>.snooze-heading:only-child)>.snooze-heading{margin:0 -16px 12px}
  dialog:not(#palette):not(#new-card) :is(dialog>*,dialog>form>*,dialog>*>form>*,#snooze-calendar>*):is(.actions,.send-act,.ed-actions,.snooze-footer,#send-ask):not(#send-ask *){position:sticky;bottom:0;z-index:3;margin:auto -16px 0;padding:12px 16px calc(12px + env(safe-area-inset-bottom));background:var(--surface-2);box-shadow:0 -1px 0 var(--border)}
  dialog:not(#palette):not(#new-card)>:last-child:not([popover]):not(:has(:is(.actions,.send-act,.ed-actions,.snooze-footer,#send-ask))):not(:is(.actions,.send-act,.ed-actions,.snooze-footer,#send-ask)){margin-bottom:calc(16px + env(safe-area-inset-bottom))}
  dialog:not(#palette):not(#new-card)>form:not([method=dialog]:has(>.snooze-heading:only-child)):has(>:is(.actions,.send-act,.ed-actions)){display:flex;flex-direction:column;flex:1 0 auto}
  dialog:not(#palette):not(#new-card)>form:not([method=dialog]:has(>.snooze-heading:only-child))>*{flex-shrink:0}
  #send-dialog[open]:not(#_){min-height:0}
  #send-dialog:not(#_) .send-top{border-top:0}
  #send-dialog:not(#_) #send-editor:not([hidden]),#send-dialog:not(#_) #send-rich:not([hidden]),#send-dialog:not(#_) #send-body-label:not([hidden]){display:flex;flex-direction:column;flex:1 1 0}
  #send-dialog:not(#_) #send-rich-body,#send-dialog:not(#_) #send-body{flex:1 1 0;min-height:132px;max-height:none;overflow:auto}
  #send-dialog:not(#_) #send-body{height:auto;resize:none}
  #send-dialog:not(#_) #send-editor{margin:0 0 10px}#send-dialog:not(#_) #send-editor label{margin:0}
  #send-dialog:not(#_) #send-rich-label,#send-dialog:not(#_) #send-body-label>span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
  #send-act:has(#send-confirm:not([hidden])) #send-cancel{display:none}
  #help-panel:not(#_):not(#_)[open]{gap:12px}#help-panel:not(#_):not(#_) .snooze-heading{margin-bottom:0}
  #help-panel:not(#_) #help-ask-pane:not([hidden]){flex:1 1 0;min-height:0;padding-bottom:calc(12px + env(safe-area-inset-bottom))}
  #help-panel:not(#_) .help-log{flex:1 1 0;min-height:0;max-height:none;overflow:auto}
  #help-panel:not(#_) #help-bug-pane:not([hidden]),#help-panel:not(#_) #bug-form{display:flex;flex-direction:column;flex:1 0 auto}
}`}));
