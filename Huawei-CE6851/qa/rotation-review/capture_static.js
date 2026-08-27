async (page) => {
  await page.setViewportSize({width: 1200, height: 800});
  const initial = page.url();
  const viewer = initial.split('?')[0];
  const match = (name) => {
    const found = initial.match(new RegExp('[?&]' + name + '=([^&]+)'));
    return found ? decodeURIComponent(found[1]) : null;
  };
  const model = match('model');
  const variant = match('variant') || 'unknown';
  const outputRel = match('output');
  const chunk = Number(match('chunk') || 0);
  if (!model || !outputRel || !outputRel.startsWith('/')) throw new Error('missing model/output');
  const outputRoot = '/root/Project/rack-device-3d' + outputRel;
  const views = [
    ['front', 0, 0], ['rear', 180, 0], ['left', 270, 0], ['right', 90, 0],
    ['top', 0, 89], ['bottom', 0, -89],
    ['front-left', 315, 25], ['front-right', 45, 25],
    ['rear-left', 225, 25], ['rear-right', 135, 25]
  ];
  const loads = [];
  const start = chunk * 5;
  const end = start + 5;
  for (let index = start; index < end; index += 1) {
    const [name, yaw, pitch] = views[index];
    const bg = index % 2 ? 'dark' : 'light';
    const modelRequest = model + '?final-static-load=' + index;
    const url = viewer + '?model=' + encodeURIComponent(modelRequest) + '&variant=' + encodeURIComponent(variant) + '&bg=' + bg;
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 180000});
    await page.waitForFunction(() => document.body.dataset.ready === 'true', null, {timeout: 180000});
    const state = await page.evaluate(async (value) => window.__rotationQA.setPose(value.yaw, value.pitch, value.bg), {yaw, pitch, bg});
    const filename = String(index).padStart(2, '0') + '-' + name + '-' + bg + '.png';
    await page.screenshot({path: outputRoot + '/static/' + filename});
    loads.push({index, name, yaw, pitch, bg, filename, pageUrl: page.url(), viewer: {engine: state.engine, webgl: state.webgl, model: state.model, variant: state.variant, bounds: state.bounds}});
  }
  const manifest = {generatedAt: new Date().toISOString(), requestedModel: model, variant, chunk, successfulLoadCount: loads.length, views: loads};
  const downloadPromise = page.waitForEvent('download');
  await page.evaluate((data) => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2) + '\n'], {type: 'application/json'}));
    link.download = 'static-load-manifest-chunk-' + data.chunk + '.json';
    link.click();
  }, manifest);
  const download = await downloadPromise;
  await download.saveAs(outputRoot + '/static-load-manifest-chunk-' + chunk + '.json');
  return {outputRoot, successfulLoadCount: loads.length, engine: loads[0].viewer.engine, webgl: loads[0].viewer.webgl, model};
}
