async (page)=>{
  const current=page.url();
  const batch=(current.match(/[?&]batch=([^&]+)/)||[])[1];
  const model=decodeURIComponent((current.match(/[?&]model=([^&]+)/)||[])[1]||"");
  const jobs={
    std0:["front","rear"],
    std1:["left","right"],
    std2:["top","bottom"],
    std3:["front-left","front-right"],
    std4:["rear-left","rear-right"],
    stdtail:["rear-left","rear-right"],
    web0:["front","rear"],
    web1:["left","right"],
    web2:["top","bottom"],
    web3:["front-left","front-right"],
    web4:["rear-left","rear-right"]
  }[batch];
  if(!jobs) throw new Error(`unknown batch ${batch}`);
  const profile=model.includes("-web.glb")?"web":"standard";
  const origin=await page.evaluate(()=>location.origin);
  const root=`${origin}/Dell-R720-3.5inch`;
  const out=`/root/Project/rack-device-3d/Dell-R720-3.5inch/qa/viewer-babylonjs/${profile}`;
  await page.setViewportSize({width:1600,height:1200});
  for(const view of jobs){
    await page.goto(`${root}/qa/viewer-babylonjs/index.html?view=${view}&model=${model}`,{waitUntil:"load",timeout:120000});
    await page.waitForFunction(()=>window.qaReady===true,null,{timeout:120000});
    await page.screenshot({path:`${out}/${view}.png`,type:"png"});
  }
  return {batch,profile,captures:jobs.length};
}
