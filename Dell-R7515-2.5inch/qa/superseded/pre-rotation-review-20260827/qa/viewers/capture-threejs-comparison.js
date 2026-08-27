async page => {
  const entries = [
    ['front',1600,288],['rear',1600,320],['left',1600,194],
    ['right',1600,194],['top',700,1043],['bottom',700,1043]
  ];
  await page.setViewportSize({width:1600,height:288});
  await page.goto('http://127.0.0.1:8790/qa/viewers/threejs.html?model=standard&view=front&run=comparison&raw=1',{waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForFunction(()=>window.__qa?.ready===true && !!window.__qaThree,null,{timeout:120000});
  const results=[];
  for(const [view,width,height] of entries){
    await page.setViewportSize({width,height});
    await page.evaluate((view)=>{const q=window.__qaThree;q.renderer.setSize(q.stage.clientWidth,q.stage.clientHeight,false);q.fitCamera(q.root,q.directions[view]);q.renderer.render(q.scene,q.camera);window.__qa={...window.__qa,view};},view);
    await page.waitForTimeout(250);
    const screenshot=`/root/Project/rack-device-3d/Dell-R7515-2.5inch/qa/renders/comparison-standard/${view}.png`;
    const image=await page.screenshot({path:screenshot,fullPage:true,timeout:120000});
    results.push({view,width,height,screenshot,screenshotBytes:image.length});
  }
  return results;
}
