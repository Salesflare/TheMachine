// Where a script of the dashboard uses a name that only a part loaded later has (dashboard_parts.LAZY): read before that
// part is in, it throws. A use is safe when the code itself makes sure: it runs in lazyRun('<part>', …) or
// lazyPart('<part>').then(…), after lazyPart('<part>') in the same function, or where a condition asks lazyIn('<part>')
// (also through a name that holds it), typeof <name> or self.<name>. Any other needs its part in dashboard_parts.LAZY_WITH.
// The parser is the one inside Node (--expose-internals, see test_lazy_names.mjs), so there is nothing to install.
import {createRequire} from 'node:module';
const acorn=createRequire(import.meta.url)('internal/deps/acorn/acorn/dist/acorn');

const parse=source=>acorn.parse(source,{ecmaVersion:'latest',sourceType:'script',locations:true,allowAwaitOutsideFunction:true});
const isFn=n=>/Function/.test(n.type);
const kids=n=>{const out=[];for(const k in n){if(k==='loc')continue;const v=n[k];for(const x of Array.isArray(v)?v:[v])if(x&&typeof x.type==='string')out.push([k,x])}return out};
const some=(n,test)=>test(n)||kids(n).some(([,c])=>some(c,test));
const patternNames=(p,out)=>{if(!p)return;
  if(p.type==='Identifier')out.add(p.name);
  else if(p.type==='ObjectPattern')p.properties.forEach(x=>patternNames(x.value||x.argument,out));
  else if(p.type==='ArrayPattern')p.elements.forEach(x=>patternNames(x,out));
  else if(p.type==='AssignmentPattern')patternNames(p.left,out);
  else if(p.type==='RestElement')patternNames(p.argument,out)};
const declared=(list,out)=>{for(const s of list){
  if(s.type==='VariableDeclaration')s.declarations.forEach(d=>patternNames(d.id,out));
  else if((s.type==='FunctionDeclaration'||s.type==='ClassDeclaration')&&s.id)out.add(s.id.name)}return out};
const hoisted=(n,out)=>{for(const[,c]of kids(n)){if(isFn(c))continue;
  if(c.type==='VariableDeclaration'&&c.kind==='var')c.declarations.forEach(d=>patternNames(d.id,out));hoisted(c,out)}return out};
const topNames=ast=>hoisted(ast,declared(ast.body,new Set()));
// The names a node brings into scope for what is inside it
function scopeOf(n){
  const s=new Set();
  if(isFn(n)){n.params.forEach(p=>patternNames(p,s));if(n.id)s.add(n.id.name);s.add('arguments');return hoisted(n,s)}
  if(n.type==='BlockStatement'||n.type==='StaticBlock')return declared(n.body,s);
  if(/^For/.test(n.type))return declared([n.init||n.left].filter(x=>x?.type==='VariableDeclaration'),s);
  if(n.type==='SwitchStatement'){n.cases.forEach(c=>declared(c.consequent,s));return s}
  if(n.type==='CatchClause'){patternNames(n.param,s);return s}
  if(n.type==='ClassExpression'&&n.id)return s.add(n.id.name);
  return null}
const calls=(n,fn,group)=>n.type==='CallExpression'&&n.callee.name===fn&&n.arguments[0]?.value===group;

// first: the main script (or scripts); lazy: {part: script}. Returns [{from ('' is the main script), part, name, line}]
export function lazyNames(first,lazy){
  const scripts=[...[first].flat().map(s=>['',s]),...Object.entries(lazy)].map(([part,source])=>({part,ast:parse(source)}));
  const main=new Set(),owners=new Map(),holds=[];
  for(const{part,ast}of scripts)for(const name of topNames(ast))if(!part)main.add(name);else owners.set(name,(owners.get(name)||new Set()).add(part));
  // const connIn=lazyIn('connections'): a condition that asks connIn asks lazyIn
  for(const{ast}of scripts)some(ast,n=>{if(n.type==='VariableDeclarator'&&n.init&&n.id.type==='Identifier')
    some(n.init,x=>{if(x.type==='CallExpression'&&x.callee.name==='lazyIn')holds.push([n.id.name,x.arguments[0]?.value]);return false});return false});
  const asks=(test,part)=>some(test,n=>calls(n,'lazyIn',part)||n.type==='Identifier'&&holds.some(([name,p])=>name===n.name&&p===part)
    ||n.type==='UnaryExpression'&&n.operator==='typeof'&&n.argument.type==='Identifier'&&owners.get(n.argument.name)?.has(part)
    ||n.type==='MemberExpression'&&n.object.name==='self'&&!n.computed&&owners.get(n.property.name)?.has(part));
  const safe=(id,part,up)=>up.some((n,i)=>{
    if(calls(n,'lazyRun',part))return true;
    if(n.type==='CallExpression'&&n.callee.type==='MemberExpression'&&calls(n.callee.object,'lazyPart',part))return true;
    // a condition asked before this is reached: the name is not in the condition's own first part
    const test=n.type==='LogicalExpression'?n.left:n.type==='IfStatement'||n.type==='ConditionalExpression'?n.test:null,next=up[i+1]||id;
    if(test&&next!==test&&asks(test,part))return true;
    return isFn(n)&&some(n,x=>calls(x,'lazyPart',part)&&x.end<=id.start)});
  const found=[];
  for(const{part:from,ast}of scripts){
    const own=topNames(ast);
    (function visit(n,scopes,up){
      const s=scopeOf(n);if(s)scopes=[...scopes,s];
      if(n.type==='Identifier'){
        const at=owners.get(n.name),last=up.at(-1);
        if(!at||main.has(n.name)||own.has(n.name)||scopes.some(x=>x.has(n.name))||last.type==='UnaryExpression'&&last.operator==='typeof')return;
        if(![...at].some(part=>safe(n,part,up)))found.push({from,part:[...at].join(' or '),name:n.name,line:n.loc.start.line});
        return}
      for(const[k,c]of kids(n)){
        if(n.type==='MemberExpression'&&k==='property'&&!n.computed)continue;
        if(['Property','MethodDefinition','PropertyDefinition'].includes(n.type)&&k==='key'&&!n.computed)continue;
        if(['LabeledStatement','BreakStatement','ContinueStatement'].includes(n.type)&&k==='label')continue;
        visit(c,scopes,[...up,n])}
    })(ast,[],[])}
  return found}
