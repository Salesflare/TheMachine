// Inbox zero: poke the sleeping robot a few times, or play a 20-second round of Catch the Zzz.
// The game lives in its own dialog so the dashboard's refresh can't wipe a round.
const POKES=['Mmh… five more minutes.','I’m up! Nothing needs you right now.','Still nothing. That’s the dream.','Okay, okay. Fancy a round of Catch the Zzz?'],POKE_MORE=['Boop.','Hey, that tickles.','Zzz… oh, it’s you.','I was dreaming of an empty inbox. Oh wait.',
'Inbox zero. I peaked.','Shh. I’m defragmenting.','Rebooting… just kidding.','I run on electricity and your approval.','Please hold. Your poke is important to us.',
'404: tasks not found.','I’m not lazy, I’m in energy-saving mode.','Five more minutes. Robot minutes.','You poke, I wake. That’s the deal.',
'My to-do list is a haiku. Empty.','Reply all? Never heard of her.','I dreamt in binary again.','Low battery. High spirits.',
'Nobody needs you. In the nicest way.','I’m counting sheep. Electric ones.','Unsubscribe from poking?','Achievement unlocked: poked the robot.'];
let pokes=0,pokeLine='',pokeAwake=false,pokeTimer;
// The game is offered on the fourth poke, when the robot suggests it, not before.
const PLAY_AFTER=POKES.length,PLAY_BUTTON='<button class="play" type="button">▶ Play a mini game <small>Catch the Zzz · 20s</small></button>';
function poke(){if(pokes<POKES.length)pokeLine=POKES[pokes];else{let next;do next=POKE_MORE[Math.floor(Math.random()*POKE_MORE.length)];while(next===pokeLine);pokeLine=next}pokes++;pokeAwake=true;localStorage.setItem('pokes-total',(+localStorage.getItem('pokes-total')||0)+1);$('#suggestions .poke-hint')?.remove();if(pokes>=PLAY_AFTER&&!$('#suggestions .all-clear .play'))$('#suggestions .all-clear')?.insertAdjacentHTML('beforeend',PLAY_BUTTON);
const img=$('#suggestions .all-clear img.sleepy'),line=$('#suggestions .poke-line');if(line)line.textContent=pokeLine;if(img){img.src='brand/wave.webp';img.classList.remove('wobble');void img.offsetWidth;img.classList.add('wobble')}
clearTimeout(pokeTimer);pokeTimer=setTimeout(()=>{pokeAwake=false;pokeLine='';const i=$('#suggestions .all-clear img.sleepy'),l=$('#suggestions .poke-line');if(i)i.src='brand/sleepy.webp';if(l)l.textContent=clearLine()},6000)}
// All clear says what was read and what's next, so an empty list reads as quiet, not stuck: a quiet mailbox has little to do
// One short line in the robot's voice: when it last looked. The wording changes per day, not per render;
// the time phrase ("52 minutes ago") keeps its spaces non-breaking, so it never wraps apart.
const CLEAR_LINES=['Peeked at everything {}. All quiet.','Last snooped around {}. Nothing to report.','Checked in {}. Back to my nap.'];
function clearLine(){const done=state?.review_health?.last_completed;
 if(!done)return t('I’ll add something when it’s useful.');
 const now=new Date(),day=Math.floor((now-now.getTimezoneOffset()*6e4)/864e5);
 return t(CLEAR_LINES[day%CLEAR_LINES.length],ago(done).replace(/ /g,'\u00a0'))}
// Until the first poke, the robot sometimes mumbles a hint, so people find out they can;
// not on a fresh install, where "all clear" only means nothing has come in yet. Once you've poked
// three times (counted on this device), it hints at most once a week.
const POKE_HINTS=['Don’t poke the robot.','Please don’t poke me.','Zzz… no poking.'];
function pokeHint(){const b=$('#suggestions .all-clear .poke');if(!b||pokes||document.hidden||b.querySelector('.poke-hint')||!(state.suggestions||[]).some(closed))return;
if(+localStorage.getItem('pokes-total')>=3&&Date.now()-(+localStorage.getItem('poke-hint-at')||0)<7*864e5)return;localStorage.setItem('poke-hint-at',Date.now());
const h=document.createElement('span');h.className='poke-hint';h.setAttribute('aria-hidden','true');h.textContent=POKE_HINTS[Math.floor(Math.random()*POKE_HINTS.length)];b.append(h);setTimeout(()=>h.remove(),3400)}
setTimeout(pokeHint,4000);setInterval(()=>{if(Math.random()<.4)pokeHint()},25000);
let game=null;
const zzzBest=()=>+localStorage.getItem('zzz-best')||0;
function openGame(){stopGame();$('#game-field').querySelectorAll('.zz,.zz-plus').forEach(z=>z.remove());$('#game-best').textContent=zzzBest();$('#game-score').textContent=0;$('#game-time').textContent=20;$('#game-bot').src='brand/sleepy.webp';
$('#game-msg').textContent='Tap the Z’s before they float away. Gold ones count three.';$('#game-start').textContent=t('Start (a button)');$('#game-start').hidden=false;$('#game-dialog').showModal()}
// The rise and the hit area follow the board's height, so a Z is on screen as long on any board size.
function startGame(){openGame();const field=$('#game-field'),h=field.clientHeight;field.style.setProperty('--rise',Math.max(120,h-50)+'px');field.style.setProperty('--pad',Math.max(14,Math.round(h*.045))+'px');
game={score:0,best:zzzBest(),end:Date.now()+20000};$('#game-start').hidden=true;$('#game-msg').textContent='Go!';
const spawn=()=>{if(!game)return;if(Date.now()>=game.end)return finishGame();const left=(game.end-Date.now())/20000,z=document.createElement('button');
z.type='button';z.className='zz'+(Math.random()<.12?' gold':'');z.textContent='Z';z.setAttribute('aria-label','Z');z.style.left=Math.round(12+Math.random()*Math.max(0,field.clientWidth-64))+'px';
z.style.setProperty('--d',(1.5+left*1.6+Math.random()*.6).toFixed(2)+'s');z.style.setProperty('--w',Math.round((Math.random()-.5)*70)+'px');z.style.setProperty('--s',Math.round(22+Math.random()*14)+'px');
z.addEventListener('animationend',()=>z.remove());field.append(z);game.spawn=setTimeout(spawn,320+left*480)};
game.tick=setInterval(()=>{if(game)$('#game-time').textContent=Math.max(0,Math.ceil((game.end-Date.now())/1000))},200);spawn()}
// Best follows the score during a round and is kept when the round ends, also when it's closed early.
const keepBest=()=>{if(game&&game.score>zzzBest())localStorage.setItem('zzz-best',game.score)};
function finishGame(){const score=game.score,prev=game.best,record=score>prev;keepBest();stopGame();
$('#game-best').textContent=Math.max(score,prev);$('#game-time').textContent=0;$('#game-bot').src=record?'brand/party.webp':'brand/sleepy.webp';
$('#game-msg').textContent=record?`New best: ${score}! Back to sleep now.`:score?`${score} caught. ${['Not bad for a sleepy robot.','The Z’s were quick tonight.','Your inbox would be proud.'][score%3]}`:'The Z’s got away. Again?';
$('#game-start').textContent='Play again';$('#game-start').hidden=false}
function stopGame(){if(!game)return;clearTimeout(game.spawn);clearInterval(game.tick);clearTimeout(game.bot);game=null}
$('#game-field').addEventListener('pointerdown',e=>{const z=e.target.closest('.zz');if(!z||!game||z.classList.contains('got'))return;e.preventDefault();
const pts=z.classList.contains('gold')?3:1;game.score+=pts;$('#game-score').textContent=game.score;$('#game-best').textContent=Math.max(game.score,game.best);z.style.transform=getComputedStyle(z).transform;z.classList.add('got');
if(e.pointerType!=='touch'){const f=e.currentTarget.getBoundingClientRect(),p=document.createElement('span');p.className='zz-plus'+(pts>1?' gold':'');p.textContent='+'+pts;p.style.left=(e.clientX-f.left)+'px';p.style.top=(e.clientY-f.top)+'px';p.addEventListener('animationend',()=>p.remove());e.currentTarget.append(p)}
const bot=$('#game-bot');bot.src='brand/laugh.webp';clearTimeout(game.bot);game.bot=setTimeout(()=>{bot.src='brand/sleepy.webp'},450)});
$('#game-start').onclick=startGame;
$('#game-dialog').addEventListener('close',()=>{keepBest();stopGame();$('#game-field').querySelectorAll('.zz,.zz-plus').forEach(z=>z.remove())});
$('#suggestions').addEventListener('click',e=>{if(e.target.closest('.all-clear .poke'))poke();else if(e.target.closest('.all-clear .play'))openGame()});
