async page => {
  const base = 'http://127.0.0.1:8792/qa/viewers';
  const outRoot = '/root/Project/rack-device-3d/Dell-R7525-3.5inch/qa/webgl-evidence-final-v2';
  const views = ['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const combinations = [
    {viewer:'three',variant:'standard',dir:'three-standard'},
    {viewer:'three',variant:'web',dir:'three-web'},
    {viewer:'babylon',variant:'standard',dir:'babylon-standard'},
    {viewer:'babylon',variant:'web',dir:'babylon-web'},
  ];
  const browserErrors = [];
  let current = 'initial';
  page.on('console', message => {
    if (message.type() === 'error') browserErrors.push({current,kind:'console',text:message.text()});
  });
  page.on('pageerror', error => browserErrors.push({current,kind:'pageerror',text:String(error)}));
  const records = [];
  let loadIndex = 0;
  for (const combination of combinations) {
    for (const view of views) {
      loadIndex += 1;
      current = `${combination.viewer}/${combination.variant}/${view}`;
      const url = `${base}/${combination.viewer}.html?view=${view}&variant=${combination.variant}&labels=1&final_v2=${loadIndex}`;
      await page.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
      await page.waitForFunction(() => window.__VIEWER_READY__ === true,null,{timeout:30000});
      const viewerInfo = await page.evaluate(() => window.__VIEWER_INFO__);
      const screenshot = `${outRoot}/${combination.dir}/${view}.png`;
      await page.screenshot({path:screenshot});
      records.push({load_index:loadIndex,viewer:combination.viewer,variant:combination.variant,view,url,screenshot:`qa/webgl-evidence-final-v2/${combination.dir}/${view}.png`,viewer_info:viewerInfo,status:'PASS'});
    }
  }
  return {records,browserErrors};
}
