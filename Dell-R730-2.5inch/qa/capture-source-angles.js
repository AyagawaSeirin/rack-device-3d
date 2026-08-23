async (page) => {
  const root='/root/Project/rack-device-3d/Dell-R730-2.5inch/qa/renders/source-matched';
  await page.setViewportSize({width:1280,height:720});
  await page.goto('http://127.0.0.1:8123/webgl/viewer-b/?model=standard&view=front-top&source=5',{waitUntil:'load'});
  await page.waitForFunction(() => document.body.dataset.status === 'ready',null,{timeout:45000});
  const results=[];
  for (const view of ['front-top','rear-top']) {
    await page.evaluate((v) => window.viewerAPI.setView(v),view);
    await page.waitForTimeout(250);
    await page.screenshot({path:`${root}/${view}.png`});
    results.push({model:'standard',view,loaded:true,viewer:(await page.evaluate(() => window.viewerAPI.getInfo())).viewer});
  }
  return results;
}
