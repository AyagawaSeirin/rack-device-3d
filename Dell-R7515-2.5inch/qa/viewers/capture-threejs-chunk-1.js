async page => {
  const entries = [['standard','right',24],['standard','top',25],['standard','bottom',26]];
  const results = [];
  for (const [model, view, sequence] of entries) {
    await page.goto(`http://127.0.0.1:8790/qa/viewers/threejs.html?model=${model}&view=${view}&run=threejs-${sequence}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForFunction(() => window.__qa?.ready === true, null, { timeout: 60000 });
    await page.waitForTimeout(400);
    const qa = await page.evaluate(() => window.__qa);
    const screenshot = `/root/Project/rack-device-3d/Dell-R7515-2.5inch/qa/renders/threejs/${model}/${view}.png`;
    const image = await page.screenshot({ path: screenshot, fullPage: true });
    results.push({ ...qa, screenshot, screenshotBytes: image.length, sequence });
  }
  return results;
}
