// The dashboard page's source for the Node tests: dashboard.html with its parts filled in, the same as
// dashboard_parts.assemble() (what the service serves). Tests read the page only through here, never dashboard.html
// itself (tests/test_dashboard_parts.py checks both). A whole line /*@include dashboard/<name>.js*/ (or .css), or
// <!--@include dashboard/<name>.html-->, stands for that file. Line ends read as \n, as Python's read_text() reads them:
// a checkout with CRLF line ends (Git on Windows) gives the same page. __SOURCE_KINDS__ becomes the page's kinds
// (machine/kinds.py as JSON), made by dashboard_parts.kinds_json() itself so the two can't differ.
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

const MARKER=/^(?:\/\*@include dashboard\/([a-z0-9-]+\.(?:js|css))\*\/|<!--@include dashboard\/([a-z0-9-]+\.html)-->)$/;
const KINDS_MARK='__SOURCE_KINDS__';

const lf=text=>text.replace(/\r\n?/g,'\n');

// The kinds of the app in the page's folder, as dashboard_parts.kinds_json() gives them
const kindsJSON=file=>execFileSync('python3',['-c','import sys;sys.path.insert(0,sys.argv[1]);import dashboard_parts;'+
  'sys.stdout.write(dashboard_parts.kinds_json(sys.argv[2]))',fileURLToPath(new URL('..',import.meta.url)),fileURLToPath(new URL('.',file))],
  {encoding:'utf8',maxBuffer:1<<22});

// page: another dashboard.html (a URL, or a path from the working folder), its parts beside it in dashboard/
export async function dashboardPage(page){
  const file=page instanceof URL?page:page?pathToFileURL(resolve(String(page))):new URL('../dashboard.html',import.meta.url);
  const source=lf(await readFile(file,'utf8'));
  const filled=text=>text.includes(KINDS_MARK)?text.replace(KINDS_MARK,()=>kindsJSON(file)):text;
  if(!source.includes('@include'))return filled(source);
  const lines=source.split(/(?<=\n)/),out=[];
  for(const line of lines){
    const m=line.replace(/\n$/,'').match(MARKER);
    if(!m){out.push(line);continue}
    const name=m[1]||m[2],part=lf(await readFile(new URL('dashboard/'+name,file),'utf8'));
    if(!part.endsWith('\n')||/@include dashboard\//.test(part))throw new Error('dashboard/'+name+': a part ends with a newline and includes no other part');
    out.push(line.endsWith('\n')?part:part.slice(0,-1));
  }
  return filled(out.join(''));
}
