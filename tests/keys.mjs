// Keys that move the caret in a text box, as a person presses them on this computer. On a Mac, Home and End scroll the
// page instead and Ctrl+letter keys are the Emacs moves (Ctrl+B goes back a letter): the line and the text's ends are
// ⌘← ⌘→ ⌘↓ there. The dashboard's own shortcuts are ⌘ on a Mac and Ctrl elsewhere: press them as 'ControlOrMeta+k'.
const MAC=process.platform==='darwin';
export const LINE_START=MAC?'Meta+ArrowLeft':'Home';
export const LINE_END=MAC?'Meta+ArrowRight':'End';
export const TEXT_END=MAC?'Meta+ArrowDown':'Control+End';
export const SELECT_TO_LINE_START=MAC?'Shift+Meta+ArrowLeft':'Shift+Home';
// The menu key (Shift+F10) opens the menu of what has focus on Linux and Windows; a Mac has no menu key, so there the
// same keyboard-made contextmenu event (no mouse button) goes to the focused element.
export async function menuKey(page){
 if(!MAC)return page.keyboard.press('Shift+F10');
 await page.evaluate(()=>{const a=document.activeElement,r=a.getBoundingClientRect();
  a.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,button:0,clientX:r.left,clientY:r.top}))})}
