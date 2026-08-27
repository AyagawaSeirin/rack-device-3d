async (page) => {
  const current=page.url(),evidencePart=(current.split("evidence=")[1]||"").split("&")[0],evidenceDir=decodeURIComponent(evidencePart);
  if(!evidenceDir||!evidenceDir.startsWith("/root/Project/rack-device-3d/"))throw new Error("absolute in-scope evidence path required");
  await page.setViewportSize({width:480,height:360});
  await page.waitForFunction(()=>window.qaReady===true||window.qaError,null,{timeout:120000});
  const failure=await page.evaluate(()=>window.qaError||null);if(failure)throw new Error(failure);
  await page.evaluate(()=>{const c=document.querySelector("canvas");c.style.width="480px";c.style.height="360px"});
  const frames=[];
  await page.evaluate(()=>window.qaSetChecker("light"));
  for(let index=0;index<72;index++){
    const yaw=index*5;await page.evaluate(v=>window.qaSetOrbit(v,10),yaw);
    const filename=`yaw-frames/frame-${String(index).padStart(3,"0")}-yaw-${String(yaw).padStart(3,"0")}.png`;
    await page.screenshot({path:`${evidenceDir}/${filename}`});frames.push({kind:"yaw",index,yaw,pitch:10,checker:"light",filename});
  }
  for(const checker of ["light","dark"]){
    await page.evaluate(v=>window.qaSetChecker(v),checker);
    for(const yaw of [0,90,180,270])for(const pitch of [-35,-15,15,35]){
      await page.evaluate(v=>window.qaSetOrbit(v.yaw,v.pitch),{yaw,pitch});
      const filename=`pitch-checker/${checker}-yaw-${String(yaw).padStart(3,"0")}-pitch-${pitch>0?"+":""}${pitch}.png`;
      await page.screenshot({path:`${evidenceDir}/${filename}`});frames.push({kind:"pitch-checker",yaw,pitch,checker,filename});
    }
    for(const [yaw,pitch] of [[0,10],[135,-25],[270,25]]){
      await page.evaluate(v=>window.qaSetOrbit(v.yaw,v.pitch),{yaw,pitch});
      for(let sample=1;sample<=3;sample++){
        await page.evaluate(()=>new Promise(requestAnimationFrame));
        const filename=`stable-frames/${checker}-yaw-${String(yaw).padStart(3,"0")}-pitch-${pitch>0?"+":""}${pitch}-sample-${sample}.png`;
        await page.screenshot({path:`${evidenceDir}/${filename}`});frames.push({kind:"stable",yaw,pitch,checker,sample,filename});
      }
    }
  }
  const runtime=await page.evaluate(()=>({...window.qaInfo,checker:document.body.className,overlayVisible:getComputedStyle(document.getElementById("loading")).display!=="none"}));
  const manifest={capturedAt:new Date().toISOString(),pageUrl:page.url(),viewport:{width:480,height:360},yawStepDegrees:5,yawFrames:72,yawPitchDegrees:10,pitchCheckerFrames:32,stableFrames:18,checkerboards:["light","dark"],runtime,frames};
  const pending=page.waitForEvent("download");await page.evaluate(value=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)+"\n"],{type:"application/json"}));a.download="rotation-manifest.json";a.click()},manifest);const download=await pending;await download.saveAs(`${evidenceDir}/rotation-manifest.json`);return manifest;
}
