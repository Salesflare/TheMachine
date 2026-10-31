// Clicks a sidebar row the way a person would: below 1024px the sidebar is a drawer, so it opens the drawer first when
// the row is out of sight (picking a tab, a card or Settings closes it again). It waits for the drawer to stop sliding.
const still=page=>page.waitForFunction(()=>!document.querySelector('#app-side')?.getAnimations().length);
export async function navClick(row){const page=row.page();await still(page);
 if(!(await row.isVisible())&&await page.evaluate(()=>typeof drawerOpen==='function'&&!matchMedia('(min-width:1024px)').matches)){
  await page.evaluate(()=>drawerOpen());await row.waitFor({state:'visible'});await still(page)}
 await row.click();await still(page)}
// The card filter (All, Work, Personal) in the sidebar; on a phone the drawer closes again afterwards
export async function scopeClick(page,name){await navClick(page.locator(`#side-cards [data-scope="${name.toLowerCase()}"]`));
 if(await page.evaluate(()=>document.documentElement.dataset.drawer==='open')){await page.keyboard.press('Escape');await still(page)}}
// Uses an item in a menu or a fold (a <details>): opens it when the item is out of sight, then does act on the item (a
// click by default). An answer that comes in between (a change saved, a quiet refresh) redraws the page and closes it;
// then it opens it again, as a person would. open: how to press the summary (a tap on a phone), a click by default.
export async function menuPick(summary,item,{open=l=>l.click(),act=l=>l.click()}={}){
 for(let tries=0;;tries++){
  if(!(await item.isVisible()))await open(summary);
  try{await item.waitFor({state:'visible',timeout:2000});await act(item);return}catch(e){if(tries>=5)throw e}}}
// Puts focus on an element and waits until it is there. The list redraws when an answer comes in (a quiet refresh, a
// rename closing): focus given to the row it replaces is lost, and the new row has no tabindex yet (J gives a row one,
// as kbFocus does), so it gives the row now shown a tabindex of -1 and focus again.
export async function focusOn(target){
 for(let tries=0;;tries++){await target.evaluate(e=>{if(!e.matches('a[href],button,input,select,textarea,summary,[tabindex],[contenteditable="true"]'))e.tabIndex=-1});await target.focus();
  if(await target.evaluate(e=>e===document.activeElement).catch(()=>false))return;
  if(tries>=20)throw new Error('focus never stayed on '+target)}}
