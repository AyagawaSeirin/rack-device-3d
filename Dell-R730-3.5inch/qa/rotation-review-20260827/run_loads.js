async page => {
  const q=await page.evaluate(()=>Object.fromEntries(new URLSearchParams(location.search).entries())),{base,modelKey,out}=q;
  const specs={standard:{model:q.standardModel,hash:q.standardHash},web:{model:q.webModel,hash:q.webHash}};
  const combos=[['three','standard'],['three','web'],['babylon','standard'],['babylon','web']],results=[];
  for(let i=0;i<40;i++){
    const [engine,tier]=combos[i%4],spec=specs[tier],seq=i+1,yaw=(i*37)%360,pitch=[8,-8,28,-28][i%4],bg=pitch<0?'dark':'light',nonce=`${spec.hash}-load-${String(seq).padStart(3,'0')}`;
    const viewer=`${base}/Dell-R730-3.5inch/qa/rotation-review-20260827/viewers/${engine}.html`,url=`${viewer}?model=${encodeURIComponent(spec.model+'?cb='+nonce)}&expected=${spec.hash}&yaw=${yaw}&pitch=${pitch}&bg=${bg}&nonce=${nonce}`;
    const p=await page.context().newPage();await p.setViewportSize({width:1200,height:800});const errors=[];p.on('pageerror',e=>errors.push(String(e)));const started=Date.now(),response=await p.goto(url,{waitUntil:'domcontentloaded',timeout:120000});await p.waitForFunction(()=>window.__QA__&&(window.__QA__.ready||window.__QA__.error),{timeout:120000});const info=await p.evaluate(()=>window.__QA__);
    if(info.error||!info.ready||!info.overlayHidden||info.webgl!=='WebGL2'||info.actualHash!==spec.hash)throw new Error(JSON.stringify({seq,engine,tier,info}));
    const shot=`${out}/loads/${engine}/${tier}/load-${String(seq).padStart(3,'0')}.png`;await p.screenshot({path:shot,animations:'disabled'});results.push({sequence:seq,engine,tier,yaw,pitch,bg,cache_bust:nonce,url,http_status:response?.status()||null,elapsed_ms:Date.now()-started,screenshot:shot,info,page_errors:errors});await p.close();
  }
  const manifest={model_key:modelKey,required:40,completed:results.length,independent_pages:true,cache_busted:true,results};const pending=page.waitForEvent('download',{timeout:30000});await page.evaluate(data=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download='load-manifest.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);},manifest);const download=await pending;await download.saveAs(`${out}/manifests/load-manifest.json`);return {model_key:modelKey,status:'PASS',loads:results.length,by_combo:Object.fromEntries(combos.map(([e,t])=>[`${e}-${t}`,results.filter(r=>r.engine===e&&r.tier===t).length]))};
}
