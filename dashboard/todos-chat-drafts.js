// A chat message being typed stays on the device until it is sent (encrypted with the rest), so a reload, a crash or a
// lost connection never loses it. In memory too, for a device that keeps nothing.
const chatDrafts=new Map(),chatDraftTouched=new Set();let chatDraftTimer=null;
function chatDraftKeep(id,text){if(!id)return;chatDraftTouched.add(id);text=String(text||'');if(text.trim())chatDrafts.set(id,text);else chatDrafts.delete(id);clearTimeout(chatDraftTimer);
 chatDraftTimer=setTimeout(chatDraftsSave,250)}
function chatDraftsSave(){clearTimeout(chatDraftTimer);chatDraftTimer=null;return localCache.put('chat-drafts',Object.fromEntries(chatDrafts))}
addEventListener('pagehide',()=>{if(chatDraftTimer)chatDraftsSave()});document.addEventListener('visibilitychange',()=>{if(document.hidden&&chatDraftTimer)chatDraftsSave()});
const chatDraftsLoaded=localCache.read('chat-drafts').then(hit=>{for(const [k,v] of Object.entries(hit?.value||{}))if(typeof v==='string'&&!chatDraftTouched.has(k)&&!chatDrafts.has(k))chatDrafts.set(k,v)}).catch(()=>{});
// A chat message that didn't go (canceled, or refused) back into its draft, before what was typed since: never over it
async function chatDraftReturn(id,text){await chatDraftsLoaded;const input=$('#chat-input'),open=id===chatId&&input;
 const merged=[text,(open?input.value:chatDrafts.get(id))||''].filter(x=>x.trim()).join('\n\n');chatDraftKeep(id,merged);
 if(open){input.value=merged;chatGrow(input);chatSendState()}}
async function chatDraftBack(id){await chatDraftsLoaded;const text=chatDrafts.get(id),input=$('#chat-input');if(!text||id!==chatId||!input||input.value.trim())return;input.value=text;chatGrow(input);chatSendState()}

