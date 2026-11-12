// A to-do's named questions (askLine in todos-cards.js), loaded on the first pick or Answer. A pick answers its own
// question (the same pick again takes it back). Answer sends every answer as one message, a line per question with its
// answer (machine/chat.py chat_unglued splits them for the chat); one still without an answer is marked instead.
const askReply=(qs,vals)=>qs.map((q,i)=>sentence(q.question)+' '+vals[i]).join('\n');
async function askAct(b){const id=b.dataset.id,s=state.suggestions.find(x=>x.id===id),qs=s?.preparation_questions||[],box=b.closest('.ask-line');if(!qs.length||!box)return;
 if(b.dataset.choice==='pick'){const p={...askPicks.get(id)},i=b.dataset.q;if(p[i]===b.dataset.pick)delete p[i];else{p[i]=b.dataset.pick;askMissing.get(id)?.delete(+i)}askPicks.set(id,p);focusKept(render);return}
 const vals=qs.map((q,i)=>String(box.querySelector(`[data-ask-field][data-q="${i}"]`)?.value??askValue(s,i)).trim()),miss=vals.flatMap((v,i)=>v?[]:[i]);
 if(miss.length){askMissing.set(id,new Set(miss));render();document.querySelector(`#ask-${CSS.escape(id)}-${miss[0]},.pick[data-id="${CSS.escape(id)}"][data-q="${miss[0]}"]`)?.focus();return}
 const inChat=!!b.closest('.chat-ask');b.disabled=true;
 try{await saveDecision(id,'other',askReply(qs,vals),true,inChat?'chat-':'');askPicks.delete(id);askMissing.delete(id);
  if(inChat&&chatId===id){chat={...chat,active:true,cursor:null};paintChat();chatToEnd();chatPoll()}}
 catch(e){errCaught(e);toast(e.message,true)}finally{b.disabled=false}}
