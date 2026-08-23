async page => {
  await page.setViewportSize({width:1280,height:800});
  const views=['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const records=[];const browserErrors=[];let current='initial';
  page.on('console',message=>{if(message.type()==='error')browserErrors.push({current,kind:'console',text:message.text()})});
  page.on('pageerror',error=>browserErrors.push({current,kind:'pageerror',text:String(error)}));
  let index=0;
  for(const view of views){
    index+=1;current=`babylon/standard/${view}`;
    const url=`http://127.0.0.1:8794/qa/viewers/babylon.html?view=${view}&variant=standard&labels=1&bg=light&load=babylon-standard-${index}`;
    await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
    await page.waitForFunction(()=>window.__VIEWER_READY__===true,null,{timeout:30000});
    const viewerInfo=await page.evaluate(()=>window.__VIEWER_INFO__);
    await page.screenshot({path:`/root/Project/rack-device-3d/Dell-R240-3.5inch/qa/webgl-evidence/babylon-standard/${view}.png`,scale:'css',type:'png'});
    records.push({load_index:index,viewer:'babylon',variant:'standard',view,url,screenshot:`qa/webgl-evidence/babylon-standard/${view}.png`,viewer_info:viewerInfo,status:'PASS'});
  }
  return {status:'PASS',actual_loads:records.length,records,browserErrors};
}

