async page => {
const base = 'http://127.0.0.1:8790/qa/viewers/threejs.html';
const root = '/root/Project/rack-device-3d/Dell-R7515-2.5inch/qa/renders/threejs';
const models = ['standard', 'web'];
const views = ['front', 'rear', 'left', 'right', 'top', 'bottom', 'front-left', 'front-right', 'rear-left', 'rear-right'];
const results = [];
let serial = 20;
for (const model of models) {
  for (const view of views) {
    serial += 1;
    const run = `threejs-${String(serial).padStart(2, '0')}`;
    const url = `${base}?model=${encodeURIComponent(model)}&view=${encodeURIComponent(view)}&run=${run}`;
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForFunction(() => window.__qa?.ready === true, null, { timeout: 60000 });
    await page.waitForTimeout(400);
    const qa = await page.evaluate(() => window.__qa);
    const screenshot = `${root}/${model}/${view}.png`;
    const image = await page.screenshot({ path: screenshot, fullPage: true });
    const result = { ...qa, screenshot, screenshotBytes: image.length, sequence: serial };
    results.push(result);
    console.log(`QA_LOAD ${JSON.stringify(result)}`);
  }
}
return results;
}
