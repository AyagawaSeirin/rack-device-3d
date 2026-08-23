async (page) => {
  const current = page.url();
  const engine = current.includes('babylonjs') ? 'babylon' : 'three';
  const base = current.split('?')[0];
  const outDir = '/root/Project/rack-device-3d/Huawei-RH1288V5-2.5inch/qa/renders';
  const views = ['front', 'rear', 'left', 'right', 'top', 'bottom', 'front-left', 'front-right', 'rear-left', 'rear-right'];
  const results = [];
  await page.setViewportSize({ width: 1600, height: 1000 });
  for (const model of ['standard', 'web']) {
    for (const view of views) {
      await page.goto(`${base}?model=${model}&view=${view}`);
      await page.waitForFunction(() => window.viewerState && (window.viewerState.loaded || window.viewerState.errors.length), null, { timeout: 30000 });
      const state = await page.evaluate(() => window.viewerState);
      if (!state.loaded || state.errors.length) throw new Error(`${engine} ${model} ${view}: ${JSON.stringify(state)}`);
      await page.screenshot({ path: `${outDir}/${engine}-${model}-${view}.png`, scale: 'css', type: 'png' });
      results.push(state);
    }
    for (const bg of ['light', 'dark']) {
      await page.goto(`${base}?model=${model}&view=front&bg=${bg}`);
      await page.waitForFunction(() => window.viewerState && (window.viewerState.loaded || window.viewerState.errors.length), null, { timeout: 30000 });
      const state = await page.evaluate(() => window.viewerState);
      if (!state.loaded || state.errors.length) throw new Error(`${engine} ${model} alpha-${bg}: ${JSON.stringify(state)}`);
      await page.screenshot({ path: `${outDir}/${engine}-${model}-alpha-front-${bg}.png`, scale: 'css', type: 'png' });
    }
  }
  return results;
}
