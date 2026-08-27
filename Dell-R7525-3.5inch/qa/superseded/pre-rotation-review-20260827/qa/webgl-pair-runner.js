async page => {
  const selectedPair = await page.evaluate(() => new URL(location.href).searchParams.get('batch_pair'));
  const definitions = {
    'three-standard': {viewer:'three',variant:'standard'},
    'three-web': {viewer:'three',variant:'web'},
    'babylon-standard': {viewer:'babylon',variant:'standard'},
    'babylon-web': {viewer:'babylon',variant:'web'},
  };
  const definition = definitions[selectedPair];
  if (!definition) throw new Error(`Unknown batch_pair: ${selectedPair}`);
  const base = 'http://127.0.0.1:8792/qa/viewers';
  const outRoot = '/root/Project/rack-device-3d/Dell-R7525-3.5inch/qa/webgl-evidence-final-v2';
  const views = ['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const records = [];
  const browserErrors = [];
  const context = page.context();
  for (let start=0; start<views.length; start+=5) {
    const chunk = views.slice(start,start+5);
    const chunkRecords = await Promise.all(chunk.map(async (view,index) => {
      const p = await context.newPage();
      const current = `${definition.viewer}/${definition.variant}/${view}`;
      p.on('console', message => {
        if (message.type() === 'error') browserErrors.push({current,kind:'console',text:message.text()});
      });
      p.on('pageerror', error => browserErrors.push({current,kind:'pageerror',text:String(error)}));
      const url = `${base}/${definition.viewer}.html?view=${view}&variant=${definition.variant}&labels=1&final_v2_pair=${start+index+1}`;
      await p.goto(url,{waitUntil:'domcontentloaded',timeout:30000});
      await p.waitForFunction(() => window.__VIEWER_READY__ === true,null,{timeout:30000});
      const viewerInfo = await p.evaluate(() => window.__VIEWER_INFO__);
      const screenshot = `${outRoot}/${selectedPair}/${view}.png`;
      await p.screenshot({path:screenshot});
      await p.close();
      return {viewer:definition.viewer,variant:definition.variant,view,url,screenshot:`qa/webgl-evidence-final-v2/${selectedPair}/${view}.png`,viewer_info:viewerInfo,status:'PASS'};
    }));
    records.push(...chunkRecords);
  }
  return {pair:selectedPair,records,browserErrors};
}
