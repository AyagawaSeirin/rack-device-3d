async (page) => {
  await page.waitForFunction(() => window.__qa?.ready === true || window.__qa?.error, null, {timeout: 120000});
  const qa = await page.evaluate(() => JSON.parse(JSON.stringify(window.__qa)));
  if (!qa.ready || qa.error || !qa.loadingOverlayCleared || !String(qa.webglVersion).includes('WebGL 2')) {
    throw new Error(JSON.stringify(qa));
  }
  const views = [
    ['front', 0, 0],
    ['rear', 180, 0],
    ['right', 90, 0],
    ['left', 270, 0],
    ['top', 0, 89.9],
    ['bottom', 0, -89.9]
  ];
  const captures = [];
  for (const [face, yaw, pitch] of views) {
    const camera = await page.evaluate(({yaw, pitch}) => window.__rotation.setView(yaw, pitch, 'light'), {yaw, pitch});
    const pending = page.waitForEvent('download', {timeout: 30000});
    await page.evaluate(face => {
      const anchor = document.createElement('a');
      anchor.href = document.querySelector('canvas').toDataURL('image/png');
      anchor.download = `${face}.png`;
      anchor.click();
    }, face);
    const download = await pending;
    const path = `matched-camera-current/renders/${face}.png`;
    await download.saveAs(path);
    captures.push({face, yaw, pitch, path, camera});
  }
  return {status: 'PASS', qa, captures};
}
