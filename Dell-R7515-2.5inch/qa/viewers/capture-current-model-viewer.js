async page => {
  await page.waitForFunction(() => window.__qa?.ready === true, null, { timeout: 60000 });
  await page.waitForTimeout(550);
  const qa = await page.evaluate(() => window.__qa);
  const screenshot = `/root/Project/rack-device-3d/Dell-R7515-2.5inch/qa/renders/model-viewer/${qa.model}/${qa.view}.png`;
  const image = await page.screenshot({ path: screenshot, fullPage: true });
  return { ...qa, screenshot, screenshotBytes: image.length };
}
