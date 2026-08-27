async (page) => {
  const base = 'http://127.0.0.1:4173/qa/viewers';
  const output = '/root/Project/rack-device-3d/Huawei-RH1288V3-2.5inch/qa/renders';
  const viewers = ['three', 'babylon'];
  const models = ['standard', 'web'];
  const views = [
    'front', 'rear', 'left', 'right', 'top', 'bottom',
    'frontLeft', 'frontRight', 'rearLeft', 'rearRight'
  ];

  await page.setViewportSize({ width: 1600, height: 900 });
  for (const viewer of viewers) {
    for (const model of models) {
      for (const view of views) {
        const url = `${base}/${viewer}.html?model=${model}&view=${view}&compare=1&rev=final3`;
        await page.goto(url, { waitUntil: 'domcontentloaded' });
        await page.waitForFunction(() => document.body.dataset.ready === '1', null,
                                   { timeout: 30000 });
        await page.screenshot({
          path: `${output}/${viewer}/${model}/${view}.png`,
          type: 'png'
        });
      }
    }
  }
  return { viewers, models, views, captures: viewers.length * models.length * views.length };
}
