async (page) => {
  const root='/root/Project/rack-device-3d/Dell-R730-2.5inch/qa/renders/viewer-a';
  const views=['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const results=[];
  await page.setViewportSize({width:1280,height:720});
  for (const model of ['standard','web']) {
    await page.goto(`http://127.0.0.1:8123/webgl/viewer-a/?model=${model}&view=front&final=1`,{waitUntil:'load'});
    await page.waitForFunction(() => document.body.dataset.status === 'ready',null,{timeout:45000});
    const load=await page.evaluate(() => window.viewerAPI.getInfo());
    for (const view of views) {
      await page.evaluate((v) => {window.viewerAPI.setBackground('neutral');window.viewerAPI.setView(v)},view);
      await page.waitForTimeout(120);
      await page.screenshot({path:`${root}/${model}/${view}.png`});
      results.push({model,view,loaded:true,viewer:load.viewer,nodes:load.nodes,bounds:load.bounds});
    }
  }
  await page.goto('http://127.0.0.1:8123/webgl/viewer-a/?model=standard&view=front&alpha=1',{waitUntil:'load'});
  await page.waitForFunction(() => document.body.dataset.status === 'ready',null,{timeout:45000});
  for (const bg of ['light','dark']) {
    await page.evaluate((b) => {window.viewerAPI.setBackground(b);window.viewerAPI.setView('front')},bg);
    await page.waitForTimeout(120);await page.screenshot({path:`${root}/standard/front-checker-${bg}.png`});
  }
  return results;
}
