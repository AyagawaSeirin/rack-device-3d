async page => {
  const model = 'web';
  const entries = [
    ['front','0deg 90deg 0.95m'],['rear','180deg 90deg 0.95m'],
    ['left','-90deg 90deg 1.45m'],['right','90deg 90deg 1.45m'],
    ['top','0deg 0.01deg 1.45m'],['bottom','0deg 179.99deg 1.45m'],
    ['front-left','-45deg 70deg 1.55m'],['front-right','45deg 70deg 1.55m'],
    ['rear-left','-135deg 70deg 1.55m'],['rear-right','135deg 70deg 1.55m']
  ];
  await page.goto('http://127.0.0.1:8790/qa/viewers/model-viewer.html?model=web&view=front&run=final-fast', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForFunction(() => window.__qa?.ready === true, null, { timeout: 120000 });
  const results = [];
  for (const [view, orbit] of entries) {
    await page.evaluate(({view, orbit, model}) => {
      const viewer = document.querySelector('#viewer');
      viewer.setAttribute('camera-orbit', orbit); viewer.jumpCameraToGoal();
      const canvases = viewer.shadowRoot?.querySelectorAll('canvas').length || 0;
      document.querySelector('#status').textContent = `LOADED · ${model} · ${view} · canvas ${canvases}`;
      window.__qa = { ...window.__qa, view, run: `model-viewer-final-fast-${model}-${view}`, canvasCount: canvases, modelIsVisible: viewer.modelIsVisible };
    }, {view, orbit, model});
    await page.waitForTimeout(650);
    const qa = await page.evaluate(() => window.__qa);
    const screenshot = `/root/Project/rack-device-3d/Dell-R7515-2.5inch/qa/renders/model-viewer/${model}/${view}.png`;
    const image = await page.screenshot({ path: screenshot, fullPage: true });
    results.push({ ...qa, screenshot, screenshotBytes: image.length });
  }
  return results;
}
