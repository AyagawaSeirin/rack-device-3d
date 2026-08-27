async page => {
  const q=await page.evaluate(()=>Object.fromEntries(new URLSearchParams(location.search).entries()));
  const {base,viewerBase,model,expected,out,modelKey}=q,viewer=`${base}/${viewerBase}/three.html`,nonce=`${expected}-matched-comparison`;
  const url=`${viewer}?model=${encodeURIComponent(model+'?cb='+nonce)}&expected=${expected}&yaw=0&pitch=0&bg=light&nonce=${nonce}`;
  await page.goto(url,{waitUntil:'domcontentloaded',timeout:120000});await page.setViewportSize({width:1200,height:800});
  await page.waitForFunction(()=>window.__QA__&&(window.__QA__.ready||window.__QA__.error),{timeout:120000});const initial=await page.evaluate(()=>window.__QA__);
  if(initial.error||!initial.ready||initial.actualHash!==expected||initial.webgl!=='WebGL2')throw new Error(JSON.stringify(initial));
  const views={front:[0,0],rear:[180,0],left:[270,0],right:[90,0],top:[0,89],bottom:[0,-89]},frames=[];
  for(const[view,[yaw,pitch]]of Object.entries(views))for(const bg of['light','dark']){const camera=await page.evaluate(v=>window.qaSetOrbit(v.yaw,v.pitch,v.bg),{yaw,pitch,bg}),screenshot=`${out}/${view}-${bg}.png`;await page.screenshot({path:screenshot,animations:'disabled'});frames.push({view,yaw,pitch,bg,camera,screenshot});}
  const manifest={model_key:modelKey,engine:'three',tier:'standard',model,expected_hash:expected,initial,views,frames};const pending=page.waitForEvent('download',{timeout:30000});await page.evaluate(data=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='matched-capture-manifest.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);},manifest);const download=await pending;await download.saveAs(`${out}/matched-capture-manifest.json`);return{model_key:modelKey,status:'PASS',captures:frames.length,hash:expected};
}
