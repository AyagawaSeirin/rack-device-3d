async (page) => {
  const base='http://127.0.0.1:8876/Huawei-RH1288V3-2.5inch',output='/root/Project/rack-device-3d/Huawei-RH1288V3-2.5inch/qa/rotation-review-20260827/static-40-loads';
  const viewerPages={three:base+'/qa/rotation-review-20260827/viewers/three-rotation.html',babylon:base+'/qa/rotation-review-20260827/viewers/babylon-rotation.html'};
  const models={standard:base+'/model/Huawei-RH1288V3-2.5inch.glb',web:base+'/model/Huawei-RH1288V3-2.5inch-web.glb'};
  const views={front:[0,0],rear:[180,0],left:[270,0],right:[90,0],top:[0,89],bottom:[0,-89],frontLeft:[315,25],frontRight:[45,25],rearLeft:[225,25],rearRight:[135,25]};
  const manifest={device:'Huawei-RH1288V3-2.5inch',phase:'final-static-40-loads',capturedAt:new Date().toISOString(),views:[],loadCount:0};
  await page.setViewportSize({width:1280,height:720});page.setDefaultTimeout(60000);
  for(const [viewer,viewerPage] of Object.entries(viewerPages))for(const [model,modelUrl] of Object.entries(models))for(const [view,[yaw,pitch]] of Object.entries(views)){
    const url=viewerPage+'?file='+encodeURIComponent(modelUrl)+'&load='+encodeURIComponent(viewer+'-'+model+'-'+view+'-'+Date.now());const started=Date.now();await page.goto(url,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>document.body.dataset.ready==='1'||document.body.dataset.error);
    const state=await page.evaluate(({yaw,pitch})=>{const pose=window.rotationQA&&window.rotationQA.setPose(yaw,pitch,'light');return{ready:document.body.dataset.ready==='1',error:document.body.dataset.error||null,title:document.title,pose,runtime:window.rotationQA?{engine:window.rotationQA.engine,webgl2:window.rotationQA.webgl2,bounds:window.rotationQA.bounds,materials:window.rotationQA.materialMetrics()}:null,resources:performance.getEntriesByType('resource').filter(r=>r.name.includes('.glb')).map(r=>({name:r.name,transferSize:r.transferSize,decodedBodySize:r.decodedBodySize}))};},{yaw,pitch});
    if(!state.ready)throw new Error(viewer+'/'+model+'/'+view+': '+state.error);await page.waitForTimeout(30);const rel=viewer+'/'+model+'/'+view+'.png';await page.screenshot({path:output+'/'+rel,type:'png'});manifest.views.push({viewer,model,view,yawDeg:yaw,pitchDeg:pitch,url,screenshot:rel,elapsedMs:Date.now()-started,state});manifest.loadCount++;
  }
  const downloadPromise=page.waitForEvent('download');await page.evaluate(data=>{const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='static-40-load-manifest.json';a.click();},manifest);const download=await downloadPromise;await download.saveAs(output+'/static-40-load-manifest.json');return{loads:manifest.loadCount,manifest:output+'/static-40-load-manifest.json'};
}
