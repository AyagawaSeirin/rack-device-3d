async (page) => {
  await page.setViewportSize({width: 1200, height: 800});
  const initial = page.url();
  const readParam = (name) => {
    const found = initial.match(new RegExp('[?&]' + name + '=([^&]+)'));
    const value = found ? decodeURIComponent(found[1]) : null;
    if (!value) throw new Error('missing query parameter: ' + name);
    return value;
  };
  const outputRoot = '/root/Project/rack-device-3d' + readParam('output');
  const views = [
    ['front', 0, 0], ['rear', 180, 0], ['left', 270, 0],
    ['right', 90, 0], ['top', 0, 89], ['bottom', 0, -89]
  ];
  await page.waitForFunction(() => document.body.dataset.ready === 'true', null, {timeout: 180000});
  await page.evaluate(() => {
    document.body.style.background = '#ffffff';
    const badge = document.getElementById('badge');
    if (badge) badge.style.display = 'none';
  });
  const captures = [];
  for (const [face, yaw, pitch] of views) {
    const state = await page.evaluate(
      async (pose) => window.__rotationQA.setPose(pose.yaw, pose.pitch, 'light'),
      {yaw, pitch}
    );
    await page.evaluate(() => {
      document.body.style.background = '#ffffff';
      const badge = document.getElementById('badge');
      if (badge) badge.style.display = 'none';
    });
    await page.screenshot({path: outputRoot + '/render/' + face + '.png'});
    captures.push({face, yaw, pitch, engine: state.engine, webgl: state.webgl, bounds: state.bounds});
  }
  return {outputRoot, captures};
}
