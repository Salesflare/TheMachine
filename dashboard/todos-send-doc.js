// A lazy part (dashboard_parts.LAZY 'docwrite'): a new doc or a doc edit in the send dialog (todos-send.js).
// The review dialog for it: everything that goes in, then Create or Save. The tap here writes it, once.
function openDocWrite(draft){if(draft.file_kind&&!lazyIn('filewrite'))return lazyRun('filewrite',()=>openDocWrite(draft));$('#send-edit').hidden=true;
 const page=draft.provider==='notion',file=draft.file_kind;
 $('#send-title').textContent=draft.op==='done'?t('Mark it done in Notion?'):draft.op==='create'?(page?t('Create this page?'):t('Create this doc?')):t('Save these changes?');$('#send-confirm').textContent=draft.op==='done'?t('Mark done'):draft.op==='create'?t('Create'):t('Save');
 $('#send-preview').classList.remove('code','mail');
 sendHeader=()=>sendRows(draft.op==='done'?[['Task',draft.doc_title],['Where',docWhere(draft)]]:draft.op==='create'?[[page?'Page':'Doc',draft.title],['Where',docWhere(draft)+(draft.account_name?' · '+draft.account_name:'')]]:[[file?'File':'Doc',draft.doc_title],['Where',docWhere(draft)],['Changes',String((draft.changes||[]).length)]]);sendHeader();
 $('#send-preview').hidden=false;setHTML($('#send-preview'),html`<div class="dw">${docWriteHtml(draft)}</div>`);
 sendFine(draft.op==='done'?t('Only its status changes.'):draft.op==='create'?(page?t('Only you can see the new page until you share it.'):t('Only you can see the new doc until you share it.')):file?t('Only these changes are made, and only if the file hasn’t changed since.'):t('Only these changes are made, and only if the doc hasn’t changed since.'));$('#send-dialog').showModal()}
