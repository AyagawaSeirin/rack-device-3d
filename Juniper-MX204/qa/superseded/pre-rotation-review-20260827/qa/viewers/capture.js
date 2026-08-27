async page => {
  const root = '/root/Project/rack-device-3d/Juniper-MX204/qa/renders';
  const base = 'http://127.0.0.1:4173/Juniper-MX204/qa/viewers';
  const standard = '/Juniper-MX204/model/Juniper-MX204.glb';
  const web = '/Juniper-MX204/model/Juniper-MX204-web.glb';
  const all = ['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const checks = ['front','rear','top','front-left'];
  await page.setViewportSize({width:1600,height:900});
  async function shot(engine, model, view, out, bg='light') {
    const url = `${base}/${engine}.html?model=${encodeURIComponent(model)}&view=${encodeURIComponent(view)}&bg=${bg}`;
    await page.goto(url, {waitUntil:'domcontentloaded'});
    await page.waitForFunction(() => window.__READY === true || window.__ERROR, null, {timeout:60000});
    const err = await page.evaluate(() => window.__ERROR || '');
    if (err) throw new Error(`${engine} ${view}: ${err}`);
    await page.screenshot({path:`${root}/${out}/${view}${bg==='dark'?'-dark':''}.png`,type:'png'});
  }
  for (const v of all) await shot('three', standard, v, 'three-standard');
  for (const v of ['front','rear']) await shot('three', standard, v, 'three-standard','dark');
  for (const v of checks) await shot('three', web, v, 'three-web-check');
  for (const v of checks) await shot('babylon', standard, v, 'babylon-standard-check');
  for (const v of all) await shot('babylon', web, v, 'babylon-web');
  for (const v of ['front','rear']) await shot('babylon', web, v, 'babylon-web','dark');
  return {threeStandard:all.length+2, threeWeb:checks.length, babylonStandard:checks.length, babylonWeb:all.length+2};
}
