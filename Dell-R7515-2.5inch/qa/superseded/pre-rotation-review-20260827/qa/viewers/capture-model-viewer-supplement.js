async page => {
  const base = 'http://127.0.0.1:8790/qa/viewers/model-viewer.html';
  const root = '/root/Project/rack-device-3d/Dell-R7515-2.5inch/qa/renders/model-viewer/web';
  const results = [];
  for (const [sequence, view] of [[19, 'rear-left'], [20, 'rear-right']]) {
    const run = `model-viewer-${String(sequence).padStart(2, '0')}-supplement`;
    await page.goto(`${base}?model=web&view=${view}&run=${run}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForFunction(() => window.__qa?.ready === true, null, { timeout: 60000 });
    await page.waitForTimeout(550);
    const qa = await page.evaluate(() => window.__qa);
    const screenshot = `${root}/${view}.png`;
    const image = await page.screenshot({ path: screenshot, fullPage: true });
    results.push({ ...qa, screenshot, screenshotBytes: image.length, sequence });
  }
  return results;
}
