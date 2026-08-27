async (page) => {
  const base='http://127.0.0.1:8787/qa/viewers';
  const views=['front','rear','left','right','top','bottom','front_left','front_right','rear_left','rear_right'];
  const viewers=['three','babylon'];
  const variants=['standard','web'];
  const controlUrl=page.url();
  const start=Math.max(0,Number((controlUrl.match(/[?&]start=(\d+)/)||[])[1]||0));
  const count=Math.max(1,Number((controlUrl.match(/[?&]count=(\d+)/)||[])[1]||40));
  const matrix=[];
  for(const viewer of viewers) for(const variant of variants) for(const view of views) matrix.push({viewer,variant,view});
  const batch=matrix.slice(start,start+count);
  const evidence=[];
  await page.setViewportSize({width:1280,height:800});
  for(const {viewer,variant,view} of batch){
    const url=`${base}/${viewer}.html?model=${variant}&view=${view}&load=${Date.now()}-${evidence.length}`;
    await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
    await page.waitForFunction(()=>document.body.dataset.ready==='1'||document.body.dataset.error,{timeout:60000});
    const err=await page.evaluate(()=>document.body.dataset.error||null); if(err) throw new Error(`${viewer}/${variant}/${view}: ${err}`);
    await page.waitForTimeout(250);
    const row=await page.evaluate(()=>window.__LOAD_EVIDENCE__); row.index=start+evidence.length+1; row.pageUrl=url; evidence.push(row);
    await page.screenshot({path:`/root/Project/rack-device-3d/Dell-R7525-2.5inch/qa/renders/${viewer}/${variant}/${view}.png`,timeout:30000});
  }
  const end=start+evidence.length;
  const downloadPromise=page.waitForEvent('download');
  await page.evaluate(({rows,name})=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(rows,null,2)],{type:'application/json'}));a.download=name;document.body.appendChild(a);a.click()}, {rows:evidence,name:`load-evidence-${start+1}-${end}.json`});
  const download=await downloadPromise;
  await download.saveAs(`/root/Project/rack-device-3d/Dell-R7525-2.5inch/qa/renders/load-evidence-${start+1}-${end}.json`);
  return evidence;
}
