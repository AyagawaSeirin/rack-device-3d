async page => {
  const q=await page.evaluate(()=>Object.fromEntries(new URLSearchParams(location.search).entries()));
  const {base,engine,tier,model,expected,out,modelKey}=q;
  const viewer=`${base}/Dell-R730-3.5inch/qa/rotation-review-20260827/viewers/${engine}.html`;
  const nonce=`${expected}-rotation-${engine}-${tier}`;
  const url=`${viewer}?model=${encodeURIComponent(model+'?cb='+nonce)}&expected=${expected}&yaw=0&pitch=8&bg=light&nonce=${nonce}`;
  const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:120000});
  await page.setViewportSize({width:1200,height:800});
  await page.waitForFunction(()=>window.__QA__&&(window.__QA__.ready||window.__QA__.error),{timeout:120000});
  const initial=await page.evaluate(()=>window.__QA__);
  if(initial.error||!initial.ready||!initial.overlayHidden||initial.webgl!=='WebGL2'||initial.actualHash!==expected)throw new Error(JSON.stringify(initial));
  const frames=[];
  for(let yaw=0;yaw<360;yaw+=5){
    const camera=await page.evaluate(v=>window.qaSetOrbit(v,8,'light'),yaw),shot=`${out}/rotation/${engine}/${tier}/yaw/yaw-${String(yaw).padStart(3,'0')}.png`;
    await page.screenshot({path:shot,animations:'disabled'});frames.push({kind:'yaw',yaw,pitch:8,bg:'light',camera,screenshot:shot});
  }
  for(const pitch of[-28,-8,8,28])for(const yaw of[45,135,225,315]){
    const bg=pitch<0?'dark':'light',camera=await page.evaluate(v=>window.qaSetOrbit(v.yaw,v.pitch,v.bg),{yaw,pitch,bg}),shot=`${out}/rotation/${engine}/${tier}/pitch/${pitch<0?'m':'p'}${String(Math.abs(pitch)).padStart(2,'0')}-yaw-${String(yaw).padStart(3,'0')}.png`;
    await page.screenshot({path:shot,animations:'disabled'});frames.push({kind:'pitch',yaw,pitch,bg,camera,screenshot:shot});
  }
  for(const yaw of[0,90,180,270])for(const repeat of['a','b']){
    const camera=await page.evaluate(v=>window.qaSetOrbit(v,8,'light'),yaw),shot=`${out}/rotation/${engine}/${tier}/stability/yaw-${String(yaw).padStart(3,'0')}-${repeat}.png`;
    await page.screenshot({path:shot,animations:'disabled'});frames.push({kind:'stability',yaw,pitch:8,bg:'light',repeat,camera,screenshot:shot});
  }
  const manifest={model_key:modelKey,engine,tier,model,expected_hash:expected,viewer_url:url,http_status:response?.status()||null,viewport:[1200,800],initial,yaw_step_degrees:5,yaw_frame_count:72,pitch_frame_count:16,stability_frame_count:8,frames};
  const pending=page.waitForEvent('download',{timeout:30000});await page.evaluate(data=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='rotation-manifest.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);},manifest);const download=await pending;await download.saveAs(`${out}/manifests/rotation-${engine}-${tier}.json`);
  return {model_key:modelKey,engine,tier,status:'PASS',yaw:72,pitch:16,stability:8,hash:expected,webgl:initial.webgl,nearFarRatio:initial.nearFarRatio};
}
