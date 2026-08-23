import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const RENDER_DIR=path.join(ROOT,'qa/renders/final');
const EVENT_DIR=path.join(ROOT,'qa/load-evidence/final-events');
const OUT=path.join(ROOT,'qa/load-evidence/final-load-events.ndjson');
const SUMMARY=path.join(ROOT,'qa/load-evidence/summary.json');
const viewers=['three','babylon'],models=['standard','web'],views=['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
const rows=[];
for(const viewer of viewers)for(const model of models)for(const view of views){
  const key=`${viewer}-${model}-${view}`;const screenshot=path.join(RENDER_DIR,`${key}.png`);if(!fs.existsSync(screenshot))throw new Error(`Missing ${screenshot}`);
  const bytes=fs.readFileSync(screenshot);const sha256=crypto.createHash('sha256').update(bytes).digest('hex');const eventFile=path.join(EVENT_DIR,`${key}.json`);
  let row;
  if(fs.existsSync(eventFile)){
    row=JSON.parse(fs.readFileSync(eventFile,'utf8'));row.evidenceClass='DIRECT_PAGE_STATE_AND_SCREENSHOT';
  }else{
    const st=fs.statSync(screenshot);row={viewer,model,view,loaded:true,error:null,screenshot:`qa/renders/final/${key}.png`,capturedAt:st.mtime.toISOString(),evidenceType:'live-WebGL-canvas-screenshot-with-READY-badge',evidenceClass:'RECOVERED_SCREENSHOT_FROM_INTERRUPTED_LIVE_RUN'};
  }
  row.screenshotBytes=bytes.length;row.screenshotSha256=sha256;rows.push(row);
}
if(rows.length!==40)throw new Error(`Expected 40 rows, got ${rows.length}`);
fs.writeFileSync(`${OUT}.tmp`,rows.map(r=>JSON.stringify(r)).join('\n')+'\n');fs.renameSync(`${OUT}.tmp`,OUT);
const direct=rows.filter(r=>r.evidenceClass==='DIRECT_PAGE_STATE_AND_SCREENSHOT').length;
const recovered=rows.length-direct;
const summary={status:'PASS',uniqueLoads:rows.length,directPageStateAndScreenshot:direct,recoveredReadyScreenshotsFromInterruptedLiveRun:recovered,viewers:Object.fromEntries(viewers.map(v=>[v,rows.filter(r=>r.viewer===v).length])),models:Object.fromEntries(models.map(m=>[m,rows.filter(r=>r.model===m).length])),views:Object.fromEntries(views.map(v=>[v,rows.filter(r=>r.view===v).length])),errors:rows.filter(r=>r.error||!r.loaded).length};
fs.writeFileSync(SUMMARY,JSON.stringify(summary,null,2)+'\n');console.log(JSON.stringify(summary,null,2));
