import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const OUT=path.join(ROOT,'qa/renders/final');
const EVENT_DIR=path.join(ROOT,'qa/load-evidence/final-events');
fs.mkdirSync(OUT,{recursive:true});
fs.mkdirSync(EVENT_DIR,{recursive:true});
const specs=process.argv.slice(2);
if(!specs.length)throw new Error('Pass viewer:model:view specs');
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.glb':'model/gltf-binary','.png':'image/png','.json':'application/json'};
const server=http.createServer((req,res)=>{
  if(req.method==='POST'&&req.url==='/qa-log'){req.resume();res.writeHead(204);res.end();return;}
  const pathname=decodeURIComponent((req.url||'/').split('?')[0]);
  const rel=pathname==='/'?'/qa/viewers/three.html':pathname;
  const file=path.resolve(ROOT,'.'+rel);
  if(!file.startsWith(ROOT+path.sep)){res.writeHead(403);res.end('forbidden');return;}
  fs.readFile(file,(err,data)=>{
    if(err){res.writeHead(404);res.end('not found');return;}
    res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(data);
  });
});
await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
const port=server.address().port;
const browser=await chromium.launch({headless:true});
const browserVersion=browser.version();
const context=await browser.newContext({viewport:{width:1280,height:720},deviceScaleFactor:1});
const page=await context.newPage();
for(const spec of specs){
  const [viewer,model,view]=spec.split(':');
  if(!viewer||!model||!view)throw new Error(`Bad spec ${spec}`);
  const html=viewer==='babylon'?'babylon.html':'three.html';
  const run=`final-${viewer}-${model}-${view}`;
  const url=`http://127.0.0.1:${port}/qa/viewers/${html}?model=${model}&view=${view}&run=${run}`;
  console.log(`LOAD ${spec}`);
  await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>window.__QA&&(window.__QA.loaded||window.__QA.error),null,{timeout:60000});
  const qa=await page.evaluate(()=>window.__QA);
  if(!qa.loaded||qa.error)throw new Error(`${spec}: ${qa.error||'not loaded'}`);
  const screenshot=`${viewer}-${model}-${view}.png`;
  const screenshotPath=path.join(OUT,screenshot);
  await page.screenshot({path:screenshotPath});
  const event={...qa,screenshot:`qa/renders/final/${screenshot}`,browser:'Chromium',browserVersion,capturedAt:new Date().toISOString(),evidenceType:'live-page-state-and-screenshot',url};
  const eventPath=path.join(EVENT_DIR,`${viewer}-${model}-${view}.json`);
  const tmp=`${eventPath}.tmp`;
  fs.writeFileSync(tmp,JSON.stringify(event,null,2)+'\n');
  fs.renameSync(tmp,eventPath);
}
await context.close();
await browser.close();
await new Promise(resolve=>server.close(resolve));
console.log(JSON.stringify({status:'PASS',events:specs.length,browserVersion}));
