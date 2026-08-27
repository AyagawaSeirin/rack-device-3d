async (page)=>{
  await page.setViewportSize({width:1600,height:1200});
  await page.waitForFunction(()=>window.qaReady===true,null,{timeout:120000});
  const current=page.url();
  const view=(current.match(/[?&]view=([^&]+)/)||[])[1];
  const model=decodeURIComponent((current.match(/[?&]model=([^&]+)/)||[])[1]||"");
  const profile=model.includes("-web.glb")?"web":"standard";
  const out=`/root/Project/rack-device-3d/Dell-R720-3.5inch/qa/viewer-babylonjs/${profile}/${view}.png`;
  await page.screenshot({path:out,type:"png"});
  return {profile,view,out};
}
