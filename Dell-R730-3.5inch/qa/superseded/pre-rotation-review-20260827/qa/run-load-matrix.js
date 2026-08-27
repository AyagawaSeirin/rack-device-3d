async (page) => {
  const currentTitle = await page.title();
  const viewer = currentTitle.startsWith('Babylon') ? 'babylon' : 'three';
  const pageName = viewer === 'babylon' ? 'babylon.html' : 'three.html';
  const models = ['standard', 'web'];
  const views = ['front', 'rear', 'left', 'right', 'top', 'bottom', 'front-left', 'front-right', 'rear-left', 'rear-right'];
  const results = [];
  for (const model of models) {
    for (const view of views) {
      const run = `matrix-${viewer}-${model}-${view}`;
      const url = `http://127.0.0.1:4173/qa/viewers/${pageName}?model=${model}&view=${view}&run=${run}`;
      await page.goto(url, {waitUntil: 'domcontentloaded'});
      await page.waitForFunction(() => window.__QA && (window.__QA.loaded || window.__QA.error), null, {timeout: 45000});
      const qa = await page.evaluate(() => window.__QA);
      if (!qa.loaded || qa.error) throw new Error(`${run}: ${qa.error || 'not loaded'}`);
      await page.screenshot({path: `qa/renders/${viewer}-${model}-${view}.png`});
      results.push(qa);
    }
  }
  return results;
}
