import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const OUT=path.join(ROOT,'qa/renders/final');
const EVIDENCE=path.join(ROOT,'qa/load-evidence/final-load-events.ndjson');
const EVENT_DIR=path.join(ROOT,'qa/load-evidence/final-events');
const TMP=`${EVIDENCE}.tmp`;
fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(EVENT_DIR,{recursive:true});
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.glb':'model/gltf-binary','.png':'image/png','.json':'application/json'};

const server=http.createServer((req,res)=>{
  if(req.method==='POST'&&req.url==='/qa-log'){req.resume();res.writeHead(204);res.end();return}
  const pathname=decodeURIComponent((req.url||'/').split('?')[0]);
  const rel=pathname==='/'?'/qa/viewers/three.html':pathname;
  const file=path.resolve(ROOT,'.'+rel);
  if(!file.startsWith(ROOT+path.sep)){res.writeHead(403);res.end('forbidden');return}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end('not found');return}res.writeHead(200,{'content-type':MIME[path.extname(file)]||'application/octet-stream','cache-control':'no-store'});res.end(data)});
});
await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve)});
const port=server.address().port;

const browser=await chromium.launch({headless:true});
const browserVersion=browser.version();
const context=await browser.newContext({viewport:{width:1280,height:720},deviceScaleFactor:1});
const pageErrors=[];
const consoleMessages=[];
const requestFailures=[];
const attach=(page)=>{
  page.on('pageerror',e=>pageErrors.push(String(e)));
  page.on('console',m=>consoleMessages.push(`${m.type()}: ${m.text()}`));
  page.on('requestfailed',r=>requestFailures.push(`${r.url()} :: ${r.failure()?.errorText||'failed'}`));
};

const smoke=process.argv.includes('--smoke');
const viewers=smoke?['three']:['three','babylon'];
const models=smoke?['standard']:['standard','web'];
const views=smoke?['front']:['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
const events=[];
for(const viewer of viewers){
  const html=viewer==='three'?'three.html':'babylon.html';
  for(const model of models){
    for(const view of views){
      const run=`final-${viewer}-${model}-${view}`;
      const url=`http://127.0.0.1:${port}/qa/viewers/${html}?model=${model}&view=${view}&run=${run}`;
      const screenshot=`${viewer}-${model}-${view}.png`;
      const screenshotPath=path.join(OUT,screenshot);
      const eventPath=path.join(EVENT_DIR,`${viewer}-${model}-${view}.json`);
      if(fs.existsSync(eventPath)&&fs.existsSync(screenshotPath)){
        const existing=JSON.parse(fs.readFileSync(eventPath,'utf8'));
        if(existing.loaded&&!existing.error){console.log(`SKIP ${run}`);events.push(existing);continue}
      }
      let captured=null,lastError=null;
      for(let attempt=1;attempt<=3&&!captured;attempt++){
        const page=await context.newPage();attach(page);
        try{
          console.log(`LOAD ${run} attempt=${attempt}`);
          await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
          await page.waitForFunction(()=>window.__QA&&(window.__QA.loaded||window.__QA.error),null,{timeout:45000});
          const qa=await page.evaluate(()=>window.__QA);
          if(!qa.loaded||qa.error)throw new Error(`${run}: ${qa.error||'not loaded'}`);
          await page.screenshot({path:screenshotPath});
          captured={...qa,screenshot:`qa/renders/final/${screenshot}`,browser:'Chromium',browserVersion,capturedAt:new Date().toISOString(),attempt,evidenceType:'live-page-state-and-screenshot'};
          fs.writeFileSync(`${eventPath}.tmp`,JSON.stringify(captured,null,2)+'\n');fs.renameSync(`${eventPath}.tmp`,eventPath);
        }catch(error){lastError=String(error);console.log(`RETRY ${run} ${lastError}`)}
        await page.close().catch(()=>{});
      }
      if(!captured)throw new Error(`${run} failed after 3 attempts: ${lastError}`);
      events.push(captured);
    }
  }
}

const expected=smoke?1:40;
if(events.length!==expected)throw new Error(`Expected ${expected} load events, got ${events.length}`);
fs.writeFileSync(TMP,events.map(x=>JSON.stringify(x)).join('\n')+'\n');
fs.renameSync(TMP,EVIDENCE);
await context.close();
await browser.close();
await new Promise(resolve=>server.close(resolve));
console.log(JSON.stringify({status:'PASS',loads:events.length,browser:'Chromium',browserVersion,pageErrors,consoleMessages,requestFailures},null,2));
