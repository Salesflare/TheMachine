// A lazy part (dashboard_parts.LAZY 'recipe'): Edit and Undo on a repeating to-do's chat line "Saved how to do this
// next time" (todos-chat-thread.js chatRecipe). Edit opens its words in place; Save keeps them (recurring_method_edit),
// Undo goes back to the way before (recurring_method_undo).
const recipeForm=i=>html`<form class="chat-event chat-recipe-edit" data-recipe-form><label for="recipe-text">${window.t('How to do this next time')}</label><textarea id="recipe-text" name="text" rows="8" maxlength="4000">${i.text}</textarea><span class="recipe-acts"><button type="button" class="ghost" data-recipe-cancel>${window.t('Cancel')}</button><button type="submit" class="primary">${window.t('Save')}</button></span></form>`;
const recipePost=(action,args)=>request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action,args:{suggestion_id:chatId,...args}})});
async function recipeAct(b){if('recipeEdit' in b.dataset){recipeEdit=chatId;paintChat();const box=$('#recipe-text');box?.focus();box?.setSelectionRange(box.value.length,box.value.length);return}
 b.disabled=true;try{await recipePost('recurring_method_undo',{});toast(window.t('Undone.'));if(chat)chat.cursor=null;await chatPoll()}catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}}
$('#suggestions').addEventListener('click',e=>{if(e.target.closest('[data-recipe-cancel]')){e.stopPropagation();recipeEdit=null;paintChat()}});
$('#suggestions').addEventListener('submit',async e=>{const f=e.target.closest('[data-recipe-form]');if(!f||!chatId)return;e.preventDefault();const b=f.querySelector('[type=submit]');b.disabled=true;
 try{await recipePost('recurring_method_edit',{text:f.elements.text.value});recipeEdit=null;toast(window.t('Saved. The next one follows it.'));if(chat)chat.cursor=null;await chatPoll()}
 catch(err){errCaught(err);b.disabled=false;toast(err.message,true)}});
