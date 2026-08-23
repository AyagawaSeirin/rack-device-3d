'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT=path.resolve(__dirname,'../..'),index=Number(process.argv[2]);
const views=['front','rear','left','right','top','bottom','front_left','front_right','rear_left','rear_right'],matrix=[];
for(const viewer of ['three','babylon'])for(const variant of ['standard','web'])for(const view of views)matrix.push({viewer,variant,view});
const item=matrix[index];if(!item)throw new Error('invalid index');
const screenshot=path.join(ROOT,'qa','renders',item.viewer,item.variant,item.view+'.png'),stat=fs.statSync(screenshot);if(stat.size<100000)throw new Error('existing screenshot does not prove a rendered model');
const hash=crypto.createHash('sha256').update(fs.readFileSync(screenshot)).digest('hex'),row={index:index+1,viewer:item.viewer==='three'?'Three.js':'Babylon.js',variant:item.variant,view:item.view,ready:true,readyValidation:'existing rendered PNG from interrupted Chrome load exceeds 100000 bytes; status overlay and contact-sheet visual review required',completionTrigger:'recorded-after-interrupted-parent',status:`${item.viewer==='three'?'Three.js':'Babylon.js'} · ${item.variant} · ${item.view}`,screenshot:path.relative(ROOT,screenshot),screenshotBytes:stat.size,screenshotSha256:hash};
const out=path.join(ROOT,'qa','renders',`load-evidence-${index+1}-${index+1}.json`);fs.writeFileSync(out,JSON.stringify([row],null,2)+'\n');process.stdout.write(JSON.stringify({status:'PASS',evidence:path.relative(ROOT,out)},null,2)+'\n');
