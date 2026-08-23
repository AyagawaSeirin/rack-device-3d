'use strict';

const fs=require('fs');
const os=require('os');
const path=require('path');
const crypto=require('crypto');
const {spawn}=require('child_process');

const ROOT=path.resolve(__dirname,'../..');
const start=Math.max(0,Number(process.argv[2]||0));
const count=Math.max(1,Number(process.argv[3]||4));
const views=['front','rear','left','right','top','bottom','front_left','front_right','rear_left','rear_right'];
const matrix=[];
for(const viewer of ['three','babylon'])for(const variant of ['standard','web'])for(const view of views)matrix.push({viewer,variant,view});
const batch=matrix.slice(start,start+count);

function sha256(file){return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')}
function runOnce(item,offset,attempt){return new Promise((resolve,reject)=>{
  const index=start+offset;
  const outDir=path.join(ROOT,'qa','renders',item.viewer,item.variant);
  fs.mkdirSync(outDir,{recursive:true});
  const screenshot=path.join(outDir,`${item.view}.png`);
  if(fs.existsSync(screenshot))fs.unlinkSync(screenshot);
  const profile=fs.mkdtempSync(path.join(os.tmpdir(),'r7525-qa-'));
  const fileUrl=`file://${path.join(ROOT,'qa','viewers',item.viewer+'.html')}?model=${item.variant}&view=${item.view}&load=${Date.now()}-${index}-attempt${attempt}`;
  const args=['--headless=new','--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files','--enable-webgl','--ignore-gpu-blocklist','--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader','--window-size=1280,800','--virtual-time-budget=15000',`--user-data-dir=${profile}`,`--screenshot=${screenshot}`,fileUrl];
  const child=spawn('google-chrome',args,{stdio:'ignore'});
  let settled=false,lastSize=0,stable=0;
  const finish=(trigger,code)=>{
    if(settled)return;
    try{
      if(!fs.existsSync(screenshot))throw new Error(`Missing screenshot ${screenshot}`);
      const stat=fs.statSync(screenshot);
      if(stat.size<100000)throw new Error(`Screenshot too small to prove a rendered model (${stat.size} bytes): ${screenshot}`);
      settled=true;clearInterval(watch);if(child.exitCode===null)child.kill('SIGTERM');
      const status=`${item.viewer==='three'?'Three.js':'Babylon.js'} · ${item.variant} · ${item.view}`;
      resolve({index:index+1,viewer:item.viewer==='three'?'Three.js':'Babylon.js',variant:item.variant,view:item.view,ready:true,readyValidation:'rendered PNG stabilized above 100000 bytes; viewer status overlay is included and contact-sheet visual review is required',completionTrigger:trigger,status,screenshot:path.relative(ROOT,screenshot),screenshotBytes:stat.size,screenshotSha256:sha256(screenshot),fileUrl});
    }catch(e){if(trigger==='exit'){settled=true;clearInterval(watch);reject(code===0?e:new Error(`Chrome exit ${code}; ${e.message}`))}}
  };
  const watch=setInterval(()=>{
    if(!fs.existsSync(screenshot))return;
    const size=fs.statSync(screenshot).size;
    stable=size>100000&&size===lastSize?stable+1:0;lastSize=size;
    if(stable>=2)finish('stable-screenshot',0);
  },500);
  child.on('error',e=>{if(!settled){settled=true;clearInterval(watch);reject(e)}});
  child.on('exit',code=>finish('exit',code));
})}
async function run(item,offset){
  let lastError;
  for(let attempt=1;attempt<=3;attempt++){
    try{return await runOnce(item,offset,attempt)}catch(e){lastError=e}
  }
  throw lastError;
}

(async()=>{
  const rows=[];
  for(let i=0;i<batch.length;i++)rows.push(await run(batch[i],i));
  rows.sort((a,b)=>a.index-b.index);
  const end=start+rows.length;
  const out=path.join(ROOT,'qa','renders',`load-evidence-${start+1}-${end}.json`);
  fs.writeFileSync(out,JSON.stringify(rows,null,2)+'\n');
  process.stdout.write(JSON.stringify({status:'PASS',start:start+1,end,count:rows.length,evidence:path.relative(ROOT,out)},null,2)+'\n');
  process.exit(0);
})().catch(e=>{process.stderr.write(e.stack+'\n');process.exitCode=1});
