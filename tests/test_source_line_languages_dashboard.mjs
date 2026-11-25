import assert from 'node:assert/strict';
import {readFile,readdir} from 'node:fs/promises';
import vm from 'node:vm';
import {dashboardPage} from './dashboard-page.mjs';

// A to-do's source line reads in the owner's language, whichever form the server writes (machine/store/cards.py
// source_line): "WhatsApp to Anna" once stayed English, and Linear's and Notion's names for their messages too.
const i18n=new URL('../i18n/',import.meta.url),json=async name=>JSON.parse(await readFile(new URL(name,i18n),'utf8'));
const en=await json('en.json'),notUi=new Set(await json('not-ui.json'));
const langs=(await readdir(i18n)).filter(f=>/^[a-z]{2}(-[A-Z]{2})?\.json$/.test(f)&&f!=='en.json').map(f=>f.slice(0,-5));
assert.ok(langs.length>=10,langs.join());

const html=await dashboardPage();
const part=(from,to)=>{const i=html.indexOf(from),j=html.indexOf(to,i);assert.ok(i>=0&&j>i,from);return html.slice(i,j)};
const page=vm.createContext({});
vm.runInContext([part('const i18nPlural=',"// a count shown with separators"),part('function i18nPick','// t('),part('function t(key','function i18nPatterns'),
 part('const SRC_MON=','// A routine\'s to-do (its draft')].join('\n')
 +"\nvar I18N={lang:'en',cat:null,en:{}},DL='en';const localeDate=(d,l)=>l+' '+(d.getMonth()+1)+'/'+d.getDate();"
 +'\nfunction say(lang,cat,en,line){I18N={lang,cat,en};DL=lang;return sourceText(line)}',page);
const say=(lang,cat,line)=>page.say(lang,cat,en,line);

// English, the same words as the server's
for(const [line,shown] of [
 ['Source: WhatsApp to Anna Example · Thu, Nov 12','WhatsApp to Anna Example · en 11/12'],
 ['Source: email to Anna Example · Thu, Nov 12 (+2 more)','Email to Anna Example · en 11/12 (+2 more)'],
 ['Source: email from Sam Lee · Thu, Nov 12','Email from Sam Lee · en 11/12'],
 ['Source: notes from Intro to Sales · Q4 · Thu, Nov 12','Notes from Intro to Sales · Q4 · en 11/12'],
 ['Source: Teams to Anna Example from Acme · Thu, Nov 12','Teams to Anna Example from Acme · en 11/12'],
 ['Source: Slack DM with Sam Lee · Thu, Nov 12','Slack DM with Sam Lee · en 11/12'],
 ['Source: your routine From A to B · Thu, Nov 12','From your routine From A to B · en 11/12'],
 ['Source: your Fleet · Thu, Nov 12','From your Fleet · en 11/12'],
 ['Source: Slack · Thu, Nov 12 (+1 more)','Slack · en 11/12 (+1 more)'],
 ['Source: phone notification from WhatsApp · Thu, Nov 12','Phone notification from WhatsApp · en 11/12'],
 ['Source: phone notification · Thu, Nov 12 (+1 more)','Phone notification · en 11/12 (+1 more)'],
 ['Source: calendar','Calendar']])assert.equal(say('en',null,line),shown);

// Each language as it was read over (Korean and Russian never inflect a name): who it went to (a person, a company, a
// channel, a group chat) never reads as who it came from, and the kind never as a place or a sender ("Von WhatsApp an Anna")
const TO='{} to {} (a message)',FROM='{} from {} (a source)';
const READ={nl:['WhatsApp aan Anna','WhatsApp van Anna','Telefoonmelding van WhatsApp'],de:['WhatsApp an Anna','WhatsApp von Anna','Handy-Benachrichtigung von WhatsApp'],
 fr:['WhatsApp à Anna','WhatsApp de Anna','Notification mobile de WhatsApp'],es:['WhatsApp a Anna','WhatsApp de Anna','Notificación móvil de WhatsApp'],
 it:['WhatsApp a Anna','WhatsApp da Anna','Notifica sul telefono da WhatsApp'],'pt-BR':['WhatsApp para Anna','WhatsApp de Anna','Notificação de celular de WhatsApp'],
 ru:['WhatsApp, кому: Anna','WhatsApp: Anna','Уведомление на телефоне: WhatsApp'],ja:['WhatsApp（Anna宛）','WhatsApp（Annaから）','スマートフォンの通知（WhatsAppから）'],
 ko:['WhatsApp, 수신자: Anna','WhatsApp: Anna','휴대폰 알림: WhatsApp'],'zh-CN':['发给Anna的WhatsApp','来自Anna的WhatsApp','来自WhatsApp的手机通知']};
for(const [lang,[to,from,phone]] of Object.entries(READ)){const cat=await json(lang+'.json');
 for(const who of ['Anna','Acme','#general','Weekend crew']){
  assert.equal(say(lang,cat,`Source: WhatsApp to ${who} · Thu, Nov 12`),to.replace('Anna',who)+` · ${lang} 11/12`);
  assert.equal(say(lang,cat,`Source: WhatsApp from ${who} · Thu, Nov 12`),from.replace('Anna',who)+` · ${lang} 11/12`)}
 assert.equal(say(lang,cat,'Source: phone notification from WhatsApp'),phone)}
const nl=await json('nl.json');
assert.equal(say('nl',nl,'Source: WhatsApp to Anna Example · Thu, Nov 12 (+2 more)'),'WhatsApp aan Anna Example · nl 11/12 (+2 meer)');
assert.equal(say('nl',nl,'Source: email to Anna Example from Acme · Thu, Nov 12'),'E-mail aan Anna Example from Acme · nl 11/12');

// Every language, every kind a line can name (machine/kinds.py), every form: its own words, none left in English
const kinds=[...new Set(Object.values(JSON.parse(/<script id="source-kinds"[^>]*>([^<]*)</.exec(html)[1]).kinds).map(k=>k.name).filter(Boolean)
 .map(n=>n==='phone'?'phone notification':n))];  // as the line is shown (machine/cards.py source_kind_shown)
const up=s=>s[0].toUpperCase()+s.slice(1);
assert.ok(kinds.length>30);
for(const name of kinds)assert.ok(up(name) in en||notUi.has(up(name))||name.length<2,`"${up(name)}" is in no catalog: a source line keeps it English (python3 scripts/i18n_extract.py --add)`);
for(const lang of langs){
 const own=await json(lang+'.json'),cat={...own};
 if(own[TO])assert.notEqual(own[TO],own[FROM],`${lang}: "to" reads as "from"`);
 for(const key of [TO,...kinds.map(up)])if(key in en)cat[key]??=key===TO?'⟦{1}⟧ ⟦{0}⟧':`⟦${key}⟧`;  // not translated yet
 const fill=(key,...a)=>{let i=0;return cat[key].replace(/\{(\d*)\}/g,(_,d)=>a[d===''?i++:+d])};
 for(const name of kinds){const kind=cat[up(name)]??up(name);
  assert.equal(say(lang,cat,`Source: ${name} to Anna Example · Thu, Nov 12`),up(fill(TO,kind,'Anna Example'))+` · ${lang} 11/12`,lang);
  assert.equal(say(lang,cat,`Source: ${name} from Anna Example`),up(fill('{} from {} (a source)',kind,'Anna Example')),lang);
  assert.equal(say(lang,cat,`Source: ${name}`),up(kind),lang)}
 assert.equal(say(lang,cat,'Source: Slack DM with Sam Lee'),up(fill('Slack DM with {} (a source)','Sam Lee')),lang);
 assert.equal(say(lang,cat,'Source: your routine Spam cleanup'),up(fill('From your routine {}','Spam cleanup')),lang);
 assert.equal(say(lang,cat,'Source: your Fleet'),up(cat['From your Fleet']),lang);
}
console.log(`Source lines: every form in ${langs.length} languages, ${kinds.length} kinds.`);
