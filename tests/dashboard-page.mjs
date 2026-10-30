// The dashboard page's source for the Node tests: dashboard.html with its parts filled in, the same as
// dashboard_parts.assemble() (what the service serves). Tests read the page only through here, never dashboard.html
// itself (tests/test_dashboard_parts.py checks both). A whole line /*@include dashboard/<name>.js*/ stands for that file.
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';

const MARKER=/^\/\*@include dashboard\/([a-z0-9-]+\.js)\*\/$/;

// page: another dashboard.html (a URL, or a path from the working folder), its parts beside it in dashboard/
export async function dashboardPage(page){
  const file=page instanceof URL?page:page?pathToFileURL(resolve(String(page))):new URL('../dashboard.html',import.meta.url);
  const source=await readFile(file,'utf8');
  if(!source.includes('@include'))return source;
  const lines=source.split(/(?<=\n)/),out=[];
  for(const line of lines){
    const m=line.replace(/\n$/,'').match(MARKER);
    if(!m){out.push(line);continue}
    const part=await readFile(new URL('dashboard/'+m[1],file),'utf8');
    if(!part.endsWith('\n')||/\/\*@include dashboard\//.test(part))throw new Error('dashboard/'+m[1]+': a part ends with a newline and includes no other part');
    out.push(line.endsWith('\n')?part:part.slice(0,-1));
  }
  return out.join('');
}
