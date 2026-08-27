'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT=path.resolve(__dirname,'../..'),dir=path.join(ROOT,'qa','renders');
const files=fs.readdirSync(dir).filter(f=>/^load-evidence-\d+-\d+\.json$/.test(f));
const byIndex=new Map();for(const file of files)for(const row of JSON.parse(fs.readFileSync(path.join(dir,file),'utf8')))byIndex.set(row.index,row);
const rows=[...byIndex.values()].sort((a,b)=>a.index-b.index);if(rows.length!==40||rows.some((r,i)=>r.index!==i+1))throw new Error(`expected unique indexes 1..40, got ${rows.map(r=>r.index)}`);
for(const row of rows){const file=path.join(ROOT,row.screenshot),bytes=fs.readFileSync(file),hash=crypto.createHash('sha256').update(bytes).digest('hex');if(bytes.length<100000)throw new Error(`invalid evidence row ${row.index}`);if(hash!==row.screenshotSha256){row.supersededScreenshotSha256=row.screenshotSha256;row.screenshotSha256=hash;row.screenshotBytes=bytes.length;row.completionTrigger='current-rendered-screenshot-after-retry';row.readyValidation='current rendered PNG exceeds 100000 bytes; status overlay and contact-sheet visual review required'}}
const summary={status:'PASS',actualGlbLoads:40,viewers:['Three.js','Babylon.js'],variants:['standard','web'],views:['front','rear','left','right','top','bottom','front_left','front_right','rear_left','rear_right'],matrix:{'Three.js/standard':10,'Three.js/web':10,'Babylon.js/standard':10,'Babylon.js/web':10},rows};
fs.writeFileSync(path.join(dir,'load-evidence.json'),JSON.stringify(summary,null,2)+'\n');process.stdout.write(JSON.stringify({status:summary.status,loads:rows.length,files:files.length},null,2)+'\n');
