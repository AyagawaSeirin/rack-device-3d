async (page) => {
  await page.setViewportSize({width: 640, height: 420});
  await page.waitForFunction(() => document.body.dataset.ready === 'true', null, {timeout: 45000});
  const urlText = page.url();
  const outputMatch = urlText.match(/[?&]output=([^&]+)/);
  const outputRel = outputMatch ? decodeURIComponent(outputMatch[1]) : null;
  const chunkMatch = urlText.match(/[?&]chunk=([0-3])/);
  const chunk = chunkMatch ? Number(chunkMatch[1]) : 0;
  if (!outputRel || !outputRel.startsWith('/')) throw new Error('missing absolute workspace-relative ?output=/...');
  const outputRoot = '/root/Project/rack-device-3d' + outputRel;
  const frames = [];
  let index = 0;
  const yawStart = chunk * 90;
  const yawEnd = yawStart + 90;
  for (let yaw = yawStart; yaw < yawEnd; yaw += 5) {
    const bg = yaw < 180 ? 'light' : 'dark';
    const state = await page.evaluate(async (value) => window.__rotationQA.setPose(value.yaw, value.pitch, value.bg), {yaw, pitch: 15, bg});
    index = yaw / 5;
    const filename = String(index).padStart(3, '0') + '-yaw-' + String(yaw).padStart(3, '0') + '-pitch-015-' + bg + '.png';
    await page.screenshot({path: outputRoot + '/frames/' + filename});
    frames.push({index, kind: 'yaw', yaw, pitch: 15, bg, filename, camera: state.camera});
    index += 1;
  }
  if (chunk === 3) for (const pitch of [-45, 0, 45]) {
    for (const yaw of [0, 90, 180, 270]) {
      const bg = (yaw / 90 + (pitch + 45) / 45) % 2 === 0 ? 'light' : 'dark';
      const state = await page.evaluate(async (value) => window.__rotationQA.setPose(value.yaw, value.pitch, value.bg), {yaw, pitch, bg});
      const pitchLabel = (pitch < 0 ? 'm' : 'p') + String(Math.abs(pitch)).padStart(2, '0');
      index = 72 + ((pitch + 45) / 45) * 4 + yaw / 90;
      const filename = String(index).padStart(3, '0') + '-pitch-' + pitchLabel + '-yaw-' + String(yaw).padStart(3, '0') + '-' + bg + '.png';
      await page.screenshot({path: outputRoot + '/frames/' + filename});
      frames.push({index, kind: 'pitch-keyframe', yaw, pitch, bg, filename, camera: state.camera});
      index += 1;
    }
  }
  const viewer = await page.evaluate(() => window.__rotationQA.getState());
  const manifest = {
    generatedAt: new Date().toISOString(),
    pageUrl: page.url(),
    viewer,
    yawStepDegrees: 5,
    chunk,
    yawFrameCount: 18,
    pitchKeyframeCount: chunk === 3 ? 12 : 0,
    totalFrameCount: frames.length,
    backgrounds: ['light-checkerboard', 'dark-checkerboard'],
    frames
  };
  const downloadPromise = page.waitForEvent('download');
  await page.evaluate((data) => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2) + '\n'], {type: 'application/json'}));
    link.download = 'frame-manifest-chunk-' + data.chunk + '.json';
    link.click();
  }, manifest);
  const download = await downloadPromise;
  await download.saveAs(outputRoot + '/frame-manifest-chunk-' + chunk + '.json');
  return {outputRoot, totalFrameCount: frames.length, engine: viewer.engine, webgl: viewer.webgl, model: viewer.model, variant: viewer.variant};
}
