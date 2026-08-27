async page => {
  await page.setViewportSize({width:1280,height:800});
  const base='http://127.0.0.1:8794/qa/viewers';
  const outputRoot='/root/Project/rack-device-3d/Dell-R240-3.5inch/qa/webgl-evidence';
  const views=['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const combinations=[
    {viewer:'three',variant:'standard',directory:'three-standard'},
    {viewer:'three',variant:'web',directory:'three-web'},
    {viewer:'babylon',variant:'standard',directory:'babylon-standard'},
    {viewer:'babylon',variant:'web',directory:'babylon-web'},
  ];
  const browserErrors=[];
  let current='initial';
  page.on('console',message=>{if(message.type()==='error')browserErrors.push({current,kind:'console',text:message.text()})});
  page.on('pageerror',error=>browserErrors.push({current,kind:'pageerror',text:String(error)}));
  const records=[];
  let loadIndex=0;
  for(const combination of combinations){
    for(const view of views){
      loadIndex+=1;
      current=`${combination.viewer}/${combination.variant}/${view}`;
      const url=`${base}/${combination.viewer}.html?view=${view}&variant=${combination.variant}&labels=1&bg=light&load=final-${loadIndex}`;
      await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
      await page.waitForFunction(()=>window.__VIEWER_READY__===true,null,{timeout:30000});
      const viewerInfo=await page.evaluate(()=>window.__VIEWER_INFO__);
      if(viewerInfo.status!=='PASS')throw new Error(`Viewer did not pass: ${current}`);
      const screenshot=`${outputRoot}/${combination.directory}/${view}.png`;
      await page.screenshot({path:screenshot,scale:'css',type:'png'});
      records.push({
        load_index:loadIndex,
        viewer:combination.viewer,
        variant:combination.variant,
        view,
        url,
        screenshot:`qa/webgl-evidence/${combination.directory}/${view}.png`,
        viewer_info:viewerInfo,
        status:'PASS',
      });
    }
  }
  return {status:'PASS',required_loads:40,actual_loads:records.length,records,browserErrors};
}
