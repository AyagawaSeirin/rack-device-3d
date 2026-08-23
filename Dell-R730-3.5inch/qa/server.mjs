import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const LOG=path.join(ROOT,'qa/load-evidence/load-events.ndjson');
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.glb':'model/gltf-binary','.png':'image/png','.json':'application/json'};
const server=http.createServer((req,res)=>{
  if(req.method==='POST'&&req.url==='/qa-log'){
    let body='';req.on('data',c=>body+=c);req.on('end',()=>{try{const data=JSON.parse(body);fs.appendFileSync(LOG,JSON.stringify({...data,receivedAt:new Date().toISOString()})+'\n');res.writeHead(204);res.end()}catch(e){res.writeHead(400);res.end(String(e))}});return;
  }
  const pathname=decodeURIComponent((req.url||'/').split('?')[0]);
  const rel=pathname==='/'?'/qa/viewers/three.html':pathname;
  const file=path.resolve(ROOT,'.'+rel);
  if(!file.startsWith(ROOT+path.sep)){res.writeHead(403);res.end('forbidden');return}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end('not found');return}res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(data)});
});
server.listen(4173,'127.0.0.1',()=>console.log('QA server http://127.0.0.1:4173'));
