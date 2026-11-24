// Where the dashboard's html`` results end up as plain text, so their markup shows on screen: joined, added to a string,
// put in an untagged template or through String() or esc(), and then put in html`` (which escapes it), t(), an attribute
// or an element's text. The fix is to keep the pieces html`` (an array of them in html`` is joined as it is), never to
// make plain text raw. Values are followed through variables, functions, arguments and arrays, and through properties
// by name within a file, without running the page. An untagged template set with innerHTML is left alone.
// The parser is the one inside Node (--expose-internals, see test_html_flow.mjs), so there is nothing to install.
import {createRequire} from 'node:module';
const acorn=createRequire(import.meta.url)('internal/deps/acorn/acorn/dist/acorn');

const H=1,A=2,M=4,F=8;  // an html`` result; an array with one in it; a plain string with markup in it; an html`` result without a tag (a class name)
const MARKUP=/<\/?[a-z][a-z0-9-]*(?:[\s>/]|$)/;
const MAKERS=new Set(['raw','htmlT','orEmpty','htmlEdit','nodeHTML','netHtml']),TEXTERS=new Set(['t','esc','String','encodeURIComponent','toast','tPlain']);
const KEEP=new Set(['filter','slice','reverse','flat','sort','concat','toSorted','toReversed']),PICK=new Set(['find','at','pop','shift','findLast']);
const isFn=n=>n.type==='FunctionDeclaration'||n.type==='FunctionExpression'||n.type==='ArrowFunctionExpression';

// source: a script; fileOf: the name of the file a line of it comes from. Returns [{line, why, code}]
export function htmlFlow(source,fileOf=()=>''){
  const ast=acorn.parse(source,{ecmaVersion:'latest',sourceType:'script',locations:true,allowAwaitOutsideFunction:true});
  const kids=n=>{const out=[];for(const k in n){if(k==='loc')continue;const v=n[k];if(Array.isArray(v))for(const x of v)x&&typeof x.type==='string'&&out.push(x);else if(v&&typeof v.type==='string')out.push(v)}return out};
  // Scopes
  const scope=up=>({up,vars:new Map()}),top=scope(null),scopeOf=new Map(),fnOf=new Map();
  const declare=(s,name)=>{if(!s.vars.has(name))s.vars.set(name,{k:0,fns:new Set()});return s.vars.get(name)};
  const names=(p,f)=>{if(!p)return;if(p.type==='Identifier')f(p);else if(p.type==='ObjectPattern')p.properties.forEach(x=>names(x.value||x.argument,f));
    else if(p.type==='ArrayPattern')p.elements.forEach(x=>names(x,f));else if(p.type==='AssignmentPattern')names(p.left,f);else if(p.type==='RestElement')names(p.argument,f)};
  const fns=[];
  (function walk(n,s,fs,fn){
    scopeOf.set(n,s);
    if(isFn(n)){if(n.id&&n.type==='FunctionDeclaration')declare(s,n.id.name);
      const inner=scope(s);n.params.forEach(p=>names(p,x=>declare(inner,x.name)));n.ret=0;n.returns=[];fns.push(n);
      if(n.body.type!=='BlockStatement')n.returns.push(n.body);
      n.params.forEach(p=>walk(p,inner,inner,n));
      if(n.body.type==='BlockStatement'){scopeOf.set(n.body,inner);n.body.body.forEach(x=>walk(x,inner,inner,n))}else walk(n.body,inner,inner,n);return}
    if(n.type==='ReturnStatement'&&n.argument&&fn)fn.returns.push(n.argument);
    if(n.type==='VariableDeclaration')n.declarations.forEach(d=>names(d.id,x=>declare(n.kind==='var'?fs:s,x.name)));
    const block=n.type==='BlockStatement'||/^For/.test(n.type)||n.type==='CatchClause'||n.type==='SwitchStatement';
    const inner=block?scope(s):s;if(n.type==='CatchClause'&&n.param)names(n.param,x=>declare(inner,x.name));
    kids(n).forEach(x=>walk(x,inner,fs,fn))})(ast,top,top,null);
  const look=(s,name)=>{for(let x=s;x;x=x.up)if(x.vars.has(name))return x.vars.get(name);return declare(top,name)};
  const props=new Map(),prop=(name,n)=>{const id=fileOf(n.loc.start.line)+'|'+name;if(!props.has(id))props.set(id,{k:0,fns:new Set()});return props.get(id)};
  let changed=true;
  const add=(v,k,f)=>{if((v.k|k)!==v.k){v.k|=k;changed=true}if(f)for(const x of f)if(!v.fns.has(x)){v.fns.add(x);changed=true}};
  const keyName=p=>!p.computed&&(p.key?.name??p.key?.value);
  // The functions an expression may be
  const callables=n=>{if(!n)return [];if(isFn(n))return [n];if(n.type==='Identifier')return [...look(scopeOf.get(n),n.name).fns];
    if(n.type==='MemberExpression'&&!n.computed)return [...prop(n.property.name,n).fns];
    if(n.type==='ConditionalExpression')return [...callables(n.consequent),...callables(n.alternate)];
    if(n.type==='LogicalExpression')return [...callables(n.left),...callables(n.right)];return []};
  const bind=(p,k,f)=>{if(!p)return;
    if(p.type==='Identifier')add(look(scopeOf.get(p),p.name),k,f);
    else if(p.type==='AssignmentPattern'){bind(p.left,k,f);bind(p.left,kind(p.right),callables(p.right))}
    else if(p.type==='ObjectPattern')p.properties.forEach(x=>{if(x.type==='RestElement')return;const q=prop(keyName(x),x);bind(x.value,q.k,q.fns)});
    else if(p.type==='ArrayPattern')p.elements.forEach(x=>x&&x.type!=='RestElement'&&bind(x,k&A?H:0));
    else if(p.type==='RestElement')bind(p.argument,k&(H|A|F)?A:0)};
  const tagged=n=>n.tag.type==='Identifier'&&n.tag.name==='html';
  // instanceof SafeHTML?a:b: b is not one
  const guard=n=>n.type==='BinaryExpression'&&n.operator==='instanceof'&&n.right.name==='SafeHTML'&&source.slice(n.left.start,n.left.end);
  const text=k=>k?M:0;  // as a plain string: its markup is only text from here on
  function kind(n){
    if(!n)return 0;
    switch(n.type){
      case 'TaggedTemplateExpression':return !tagged(n)?0:n.quasi.quasis.some(q=>q.value.cooked.includes('<'))?H:n.quasi.expressions.reduce((k,x)=>{const e=kind(x);return k|(e&(H|A)?H:0)},F);
      case 'Literal':return typeof n.value==='string'&&MARKUP.test(n.value)?M:0;
      case 'TemplateLiteral':return (n.quasis.some(q=>MARKUP.test(q.value.cooked||''))?M:0)|text(n.expressions.reduce((k,x)=>k|kind(x),0));
      case 'Identifier':return look(scopeOf.get(n),n.name).k;
      case 'ConditionalExpression':{const g=guard(n.test);return kind(n.consequent)|(g&&source.slice(n.alternate.start,n.alternate.end)===g?0:kind(n.alternate))}
      case 'LogicalExpression':return kind(n.left)|kind(n.right);
      case 'SequenceExpression':return kind(n.expressions.at(-1));
      case 'AssignmentExpression':return n.operator==='+='?text(kind(n.left)|kind(n.right)):kind(n.right);
      case 'BinaryExpression':return n.operator==='+'?text(kind(n.left)|kind(n.right)):0;
      case 'AwaitExpression':case 'ChainExpression':case 'YieldExpression':return kind(n.argument||n.expression);
      case 'ArrayExpression':return n.elements.reduce((k,x)=>{if(!x)return k;const e=kind(x.type==='SpreadElement'?x.argument:x);return k|(e&(H|A|F)?A:0)|(e&M)},0);
      case 'NewExpression':return n.callee.name==='SafeHTML'?H:0;
      case 'MemberExpression':if(n.computed){const k=kind(n.object);return (k&A?H|A:0)|(k&M)}return /^(length|s)$/.test(n.property.name)?0:prop(n.property.name,n).k;
      case 'CallExpression':{
        const c=n.callee;
        if(c.type==='Identifier'){if(MAKERS.has(c.name))return H;if(c.name==='esc')return M;if(TEXTERS.has(c.name))return c.name==='t'||c.name==='String'?text(n.arguments.reduce((k,x)=>k|kind(x),0)):0}
        if(c.type==='MemberExpression'&&!c.computed){const o=kind(c.object),m=c.property.name,r=callables(n.arguments[0]).reduce((k,f)=>k|f.ret,0);
          if(m==='map'||m==='flatMap')return (r&(H|A|F)?A:0)|(r&M);
          if(m==='reduce')return r;
          if(m==='from'&&c.object.name==='Array'){const f=callables(n.arguments[1]).reduce((k,f)=>k|f.ret,0);return (f&(H|A|F)?A:0)|(f&M)}
          if(m==='join'||m==='toString')return text(o);
          if(KEEP.has(m))return o|(m==='concat'?n.arguments.reduce((k,x)=>k|(kind(x)&(H|A|F)?A:0),0):0);
          if(PICK.has(m))return (o&A?H:0)|(o&M);
          if(m==='replace'&&/^<\[\^/.test(n.arguments[0]?.regex?.pattern||''))return 0;  // its tags taken out
          if(m==='replace'||m==='replaceAll'||m==='trim')return o&M}
        return callables(c).reduce((k,f)=>k|f.ret,0)}
      default:return 0}}
  const nodes=[],seen=new Set();(function all(n){if(seen.has(n))return;seen.add(n);nodes.push(n);kids(n).forEach(all)})(ast);
  // A lookup table (const ICONS={card:html`..`}) is read by key: its names are nobody's properties
  const tables=new Set(nodes.filter(n=>n.type==='VariableDeclarator'&&/^[A-Z][A-Z0-9_]+$/.test(n.id.name)).map(n=>n.init));
  for(let i=0;changed&&i<60;i++){changed=false;
    for(const n of nodes){
      if(n.type==='VariableDeclarator'&&n.init)bind(n.id,kind(n.init),callables(n.init));
      else if(n.type==='FunctionDeclaration')add(look(scopeOf.get(n),n.id.name),0,[n]);
      else if(n.type==='AssignmentExpression'&&/^(=|\|\|=|\?\?=|&&=)$/.test(n.operator)){
        if(n.left.type==='MemberExpression'){if(!n.left.computed)add(prop(n.left.property.name,n),kind(n.right)&~M,callables(n.right))}else bind(n.left,kind(n.right),callables(n.right))}
      else if(n.type==='AssignmentExpression'&&n.operator==='+='&&n.left.type==='Identifier')bind(n.left,text(kind(n.left)|kind(n.right)));
      else if(n.type==='ObjectExpression'&&!tables.has(n))n.properties.forEach(p=>p.type==='Property'&&keyName(p)!==false&&add(prop(keyName(p),p),kind(p.value)&~M,callables(p.value)));
      else if(n.type==='ForOfStatement'){const k=kind(n.right),e=(k&A?H:0)|(k&M);if(n.left.type==='VariableDeclaration')bind(n.left.declarations[0].id,e);else bind(n.left,e)}
      else if(n.type==='CallExpression'){
        for(const f of callables(n.callee))f.params.forEach((p,i)=>{if(p.type==='RestElement')n.arguments.slice(i).forEach(a=>bind(p,kind(a)));else if(n.arguments[i])bind(p,kind(n.arguments[i]),callables(n.arguments[i]))});
        const c=n.callee;if(c.type==='MemberExpression'&&!c.computed){const o=kind(c.object),m=c.property.name;
          if((m==='push'||m==='unshift')&&c.object.type==='Identifier'){const k=n.arguments.reduce((k,a)=>k|kind(a.type==='SpreadElement'?a.argument:a),0);bind(c.object,(k&(H|A|F)?A:0)|(k&M))}
          if(o&(A|M)&&/^(map|flatMap|filter|forEach|some|every|find)$/.test(m))for(const f of callables(n.arguments[0]))bind(f.params[0],(o&A?H:0)|(o&M))}}}
    for(const f of fns){const k=f.returns.reduce((k,x)=>k|kind(x),0);if((f.ret|k)!==f.ret){f.ret|=k;changed=true}}}
  // Where it shows as text: in html`` or t(), as text or an attribute of an element
  const out=[],say=(n,why)=>out.push({line:n.loc.start.line,why,code:source.slice(n.start,Math.min(n.end,n.start+120))});
  const inQuotes=before=>{const tag=before.slice(before.lastIndexOf('<'));return before.includes('<')&&/^<[a-z]/i.test(tag)&&(tag.replace(/="[^"]*"/g,'').match(/="/)!==null)};
  for(const n of nodes){
    if(n.type==='TaggedTemplateExpression'&&tagged(n)){let before='';
      n.quasi.expressions.forEach((x,i)=>{before+=n.quasi.quasis[i].value.cooked;const k=kind(x);
        if(inQuotes(before)){if(k&~F)say(x,'markup in an attribute')}else if(k&M)say(x,'markup as a plain string in html``');
        before+='x'})}
    else if(n.type==='CallExpression'){const c=n.callee,m=c.type==='MemberExpression'&&!c.computed&&c.property.name;
      const from=c.type==='Identifier'&&(TEXTERS.has(c.name)&&c.name!=='String'?0:c.name==='make'?2:-1);
      if(from>-1&&from!==false){for(const x of n.arguments.slice(from))if(kind(x)&(c.name==='t'?H|A|F:H|A|F|M))say(x,'markup passed to '+c.name+'()')}
      else if(/^(append|prepend|replaceChildren|before|after|replaceWith|setAttribute|createTextNode|insertAdjacentText)$/.test(m)){for(const x of n.arguments)if(kind(x))say(x,'markup passed to '+m+'()')}}
    else if(n.type==='AssignmentExpression'&&n.left.type==='MemberExpression'&&/^(textContent|innerText|title|placeholder|ariaLabel)$/.test(n.left.property.name)&&kind(n.right))say(n.right,'markup set as '+n.left.property.name)}
  return out}
