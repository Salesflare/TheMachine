// Catch the Zzz: a 20-second round, offered on the fourth poke (todos-check.js).
// The game lives in its own dialog so the dashboard's refresh can't wipe a round.
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
