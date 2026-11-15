// Languages (i18n/, glossary.md, locale_prefs.py): the owner's language from Settings, General, else the browser's on
// the first load. English is the source and the fallback. The catalog is keyed by the English text, so markup and code
// stay as they are: any text, placeholder, aria-label, title or alt equal to a key reads translated, here at start and
// for whatever renders later (a MutationObserver). A key with {} matches text around the filled-in parts ("Due {}"),
// a plural entry ({"one":"{} to-do","other":"{} to-dos"}) picks the form for the number. t() is the same lookup for
// code. Skipped: translate="no" subtrees, inputs, code and editable text. Each node keeps its English, so switching
// language (or back to English) re-reads it without a reload. The last catalog is kept on the device for the next start.
const I18N={lang:'en',cat:null,en:{},pats:[],memo:new Map(),orig:new WeakMap(),shown:new WeakMap(),attrs:new WeakMap(),obs:null,ver:'__UI_VERSION__'};
const I18N_ATTRS=['placeholder','aria-label','title','alt'],I18N_SKIP='[translate="no"],script,style,textarea,pre,code,[contenteditable="true"],svg';
const i18nPlural=(n,lang)=>{try{return new Intl.PluralRules(lang).select(Math.abs(+n))}catch{return +n===1?'one':'other'}};
function i18nFill(s,args){let i=0;return String(s).replace(/\{(\d*)\}/g,(m,d)=>{const k=d===''?i++:+d;return k<args.length?String(args[k]):m})}
// a count shown with separators (2,894) still picks its plural
function i18nPick(v,args,lang){if(v&&typeof v==='object'){const n=args.map(a=>typeof a==='string'&&/^\d{1,3}([.,'\s\u00a0\u202f]\d{3})+$/.test(a)?a.replace(/\D/g,''):a).find(a=>a!==''&&!isNaN(+a));return v[i18nPlural(n??0,lang)]||v.other||''}return v}
// t('Save'), t('{} of {} ready',2,5): in the owner's language, English (the key, or en.json's plural) when there is none.
// A count with its English forms, t(['{} guest','{} guests'],n), reads right in English before any catalog is loaded.
// a label inside a sentence ("Filter people"): lowercased, except in German where nouns keep their capital
const i18nLower=s=>I18N.lang==='de'?s:String(s).toLocaleLowerCase(I18N.lang);
function t(key,...args){if(Array.isArray(key))key=I18N.cat?.[key[1]]!=null||I18N.en[key[1]]?key[1]:args.find(a=>!isNaN(+a))==1?key[0]:key[1];const tr=I18N.cat&&I18N.cat[key];return i18nFill(i18nPick(tr!=null?tr:(I18N.en[key]??(typeof key==='string'?key.replace(/ \(an? [a-z]+\)$/,''):key)),args,tr!=null?I18N.lang:'en'),args)}
function i18nPatterns(cat){const out=[],esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
 for(const key of Object.keys(cat)){const forms=I18N.en[key]&&typeof I18N.en[key]==='object'?Object.values(I18N.en[key]):[key];
  for(const f of forms){if(!/\{\d*\}/.test(f))continue;const parts=f.split(/\{\d*\}/);const head=parts[0];
   // two holes around a word or less ("{} and {}", "{}: {}") would read into anyone's sentence: those are t() only
   if(parts.length>2&&(parts.join('').match(/[A-Za-z]/g)||[]).length<=4)continue;
   // a hole glued to its text ("Pick a source to connect.{}", a sentence added only sometimes) may be empty
   const re=parts.map((x,i)=>esc(x)+(i<parts.length-1?x&&!/\s$/.test(x)&&!/^\s/.test(parts[i+1])?'((?:(?! · ).)*?)':'((?:(?! · ).)+?)':'')).join('');
   out.push({head,key,f,lit:parts.join('').length,re:new RegExp('^'+re+'$','s')})}}
 // the longest head first, then the most specific (most literal text), then by text: never the catalog file's order
 const by=(x,y)=>x<y?-1:x>y?1:0;return out.sort((a,b)=>b.head.length-a.head.length||b.lit-a.lit||by(a.key,b.key)||by(a.f,b.f))}
// a hole's text read again only when it is a catalog entry itself ("Due {}" with "today"); a name, a title or a
// message in it stays as written, even when it looks like UI ("Change {}" around "the intro.")
function i18nExact(text){const s=text.replace(/\s+/g,' ').trim(),cat=I18N.cat;if(!s||!Object.prototype.hasOwnProperty.call(cat,s))return null;const v=cat[s];return typeof v==='object'?(v.one&&I18N.en[s]?.one===s?v.one:v.other):v}
function i18nLookup(text){const s=text.replace(/\s+/g,' ').trim();if(!s||s.length>400||!/[A-Za-z]/.test(s))return null;
 if(I18N.memo.has(s))return I18N.memo.get(s);let out=null;const cat=I18N.cat;
 if(Object.prototype.hasOwnProperty.call(cat,s)){const v=cat[s];out=typeof v==='object'?(v.one&&I18N.en[s]?.one===s?v.one:v.other):v}
 else for(const p of I18N.pats){if(p.head&&!s.startsWith(p.head))continue;const m=p.re.exec(s);if(!m)continue;
  // a plural entry counts something: text without a number in its holes is no count ("nu een to-do", already Dutch)
  if(cat[p.key]&&typeof cat[p.key]==='object'&&!m.slice(1).some(a=>/\d/.test(a)))continue;
  const args=m.slice(1).map(a=>{const tr=i18nExact(a);return tr==null?a:/^\s*/.exec(a)[0]+tr+/\s*$/.exec(a)[0]});out=i18nFill(i18nPick(cat[p.key],m.slice(1),I18N.lang),args);break}
 // a row of parts joined by ' · ' (sources, plan, usage): each part on its own
 if(out==null&&s.includes(' · ')){const parts=s.split(' · '),tr=parts.map(x=>i18nLookup(x));if(tr.some(x=>x!=null))out=parts.map((x,i)=>tr[i]??x).join(' · ')}
 // a mark around the words ("+ New organization", "· retry", "Open ↗", "Waiting ·"): the words on their own
 if(out==null){const m=/^([+·•▶✓←]\s+)?([\s\S]*?)(\s+[·↗→]|\s*…)?$/.exec(s);if(m&&(m[1]||m[3])&&m[2]){const tr=i18nLookup(m[2]);if(tr!=null)out=(m[1]||'')+tr+(m[3]||'')}}
 if(I18N.memo.size>20000)I18N.memo.clear();I18N.memo.set(s,out);return out}
// the English an element was written in, whatever language it shows now (titles built from a label stay catalog keys)
function i18nEnglish(el){if(!el)return '';let out='';const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);for(let n;(n=w.nextNode());)out+=I18N.shown.get(n)===n.nodeValue&&I18N.orig.has(n)?I18N.orig.get(n):n.nodeValue;return out.replace(/\s+/g,' ').trim()}
function i18nText(node){const cur=node.nodeValue;if(I18N.shown.get(node)!==cur)I18N.orig.set(node,cur);
 const en=I18N.orig.get(node);let out=en;if(I18N.cat){const tr=i18nLookup(en);if(tr!=null){const m=/^(\s*)[\s\S]*?(\s*)$/.exec(en);out=m[1]+tr+m[2]}}
 I18N.shown.set(node,out);if(out!==cur)node.nodeValue=out}
function i18nEl(el){let kept=I18N.attrs.get(el);for(const a of I18N_ATTRS){if(!el.hasAttribute(a))continue;const cur=el.getAttribute(a);
  if(!kept){kept={};I18N.attrs.set(el,kept)}if(!kept[a]||kept[a].shown!==cur)kept[a]={en:cur,shown:cur};
  const tr=I18N.cat?i18nLookup(kept[a].en):null,out=tr??kept[a].en;kept[a].shown=out;if(out!==cur)el.setAttribute(a,out)}}
function i18nWalk(root){if(root?.nodeType===1&&root.matches('textarea')&&!root.parentElement?.closest(I18N_SKIP)){i18nEl(root);return}if(!root||(root.nodeType===1&&root.closest?.(I18N_SKIP)))return;if(root.nodeType===3){if(!root.parentElement?.closest(I18N_SKIP))i18nText(root);return}
 if(root.nodeType===1)i18nEl(root);const w=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT|NodeFilter.SHOW_TEXT,{acceptNode:n=>n.nodeType===1&&n.matches(I18N_SKIP)?(n.matches('textarea')&&!n.closest('[translate="no"]')&&i18nEl(n),NodeFilter.FILTER_REJECT):NodeFilter.FILTER_ACCEPT});
 for(let n=w.nextNode();n;n=w.nextNode())n.nodeType===3?i18nText(n):i18nEl(n)}
function i18nObserve(){if(I18N.obs)return;I18N.obs=new MutationObserver(list=>{for(const r of list){
  if(r.type==='childList')r.addedNodes.forEach(i18nWalk);else if(r.type==='characterData'){if(!r.target.parentElement?.closest(I18N_SKIP))i18nText(r.target)}
  else if(r.type==='attributes'&&!(r.target.matches('textarea')?r.target.closest('[translate="no"]')||r.target.parentElement?.closest(I18N_SKIP):r.target.closest(I18N_SKIP)))i18nEl(r.target)}});  // a textarea's placeholder too, never its text
 I18N.obs.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:I18N_ATTRS})}
// Switch the page to lang with its catalog (null for English): every node re-reads its English.
function i18nUse(lang,cat){I18N.lang=lang;I18N.cat=lang==='en'?null:cat;I18N.memo.clear();I18N.pats=I18N.cat?i18nPatterns(I18N.cat):[];
 document.documentElement.lang=lang;i18nWalk(document.body);if(I18N.cat)i18nObserve();const ci=document.getElementById('chat-input');if(ci)ci.placeholder=t('Ask or change something')}  // text areas are left alone by the walk
// true when the page switched (so what renders from data, like region names, renders again)
async function i18nLoad(lang){if(!lang||lang===I18N.lang&&(lang==='en'||I18N.cat)||lang===I18N.loading)return false;
 if(lang==='en'){i18nUse('en',null);try{localStorage.removeItem('i18n')}catch{}return true}
 I18N.loading=lang;try{const [cat,en]=await Promise.all([fetch('i18n/'+lang+'.json?v='+I18N.ver).then(r=>r.ok?r.json():null),Object.keys(I18N.en).length?I18N.en:fetch('i18n/en.json?v='+I18N.ver).then(r=>r.ok?r.json():{})]);
  if(!cat)return false;I18N.en=en||{};i18nUse(lang,cat);try{localStorage.setItem('i18n',JSON.stringify({lang,ver:I18N.ver,cat,en:I18N.en}))}catch{}return true}catch{return false}finally{I18N.loading=null}}
// The first language a browser asks for that there is a catalog for (navigator.languages is its Accept-Language):
// the exact tag (pt-BR), else its language (it-CH reads it), Portuguese from Portugal reading Brazilian and any Chinese
// (zh-TW, zh-Hant) Simplified Chinese for now.
const I18N_NEAREST={pt:'pt-BR',zh:'zh-CN'};
function i18nBrowser(langs){const codes=Object.fromEntries(Object.keys(langs).map(c=>[c.toLowerCase(),c]));
 for(const l of (navigator.languages?.length?navigator.languages:[navigator.language||'en'])){const t=String(l).toLowerCase(),b=t.split('-')[0],c=codes[t]||codes[b]||(langs[I18N_NEAREST[b]]?I18N_NEAREST[b]:'');if(c)return c}return 'en'}
// With each state (applyLocale): the owner's language; never chosen yet (language_set false), the browser's, saved once.
let i18nAsked=false;
function i18nApply(l){let lang=l.language||'en';
 if(l.language_set===false&&l.saveable&&!i18nAsked){i18nAsked=true;lang=i18nBrowser(l.languages||{en:1});
  request('api/action',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({action:'set_locale',args:{language:lang}})})
   .then(v=>{if(v?.language){state.locale=v;render()}}).catch(()=>{})}
 i18nLoad(lang).then(changed=>{if(changed)i18nRerender()})}
// Text code builds in the language (date ranges, t()) builds again once the language changes; the rest the page swaps itself
// rows a list already loaded (Done, Graph pages) are built again from their items, so their dates and words follow too
function i18nRerender(){if(typeof pagers!=='undefined')for(const p of pagers.values()){try{p.html=p.items.map(x=>p.row(x)).join('')}catch{}for(const el of document.querySelectorAll('[data-pager]'))if(el.dataset.pager===p.key)el.replaceChildren()}
 if(typeof render==='function')render();if(typeof pagerMount==='function')pagerMount();if(typeof calRender==='function'&&!$('#calendar')?.hidden)calRender()}
// Settings, General, Language: each language in its own name.
function i18nLanguages(l){const sel=document.getElementById('locale-language');if(!sel)return;const langs=l.languages||{en:'English'},cur=l.language||'en',key=cur+Object.keys(langs).join();
 if(sel.dataset.for!==key){sel.replaceChildren(...Object.entries(langs).map(([c,n])=>new Option(n,c,c===cur,c===cur)));sel.dataset.for=key}
 document.getElementById('locale-language-note').textContent=''}
try{const kept=JSON.parse(localStorage.getItem('i18n')||'null');if(kept?.lang&&kept.lang!=='en'&&kept.cat){I18N.en=kept.en||{};i18nUse(kept.lang,kept.cat);if(kept.ver!==I18N.ver){I18N.lang='';i18nLoad(kept.lang)}}}catch{}
