async (page) => {
  const base = 'http://127.0.0.1:8876/Huawei-CE5850';
  const output = '/root/Project/rack-device-3d/Huawei-CE5850/qa/rotation-review-20260827/before';
  const viewerPages = {
    three: base + '/qa/rotation-review-20260827/viewers/three-rotation.html',
    babylon: base + '/qa/rotation-review-20260827/viewers/babylon-rotation.html'
  };
  const models = {
    standard: base + '/model/Huawei-CE5850-48T4S2Q-EI-B00.glb',
    web: base + '/model/Huawei-CE5850-48T4S2Q-EI-B00-web.glb'
  };
  const manifest = { device: 'Huawei-CE5850', phase: 'before', capturedAt: new Date().toISOString(), yawStepDegrees: 5, yawFrameCountPerCombination: 72, pitchAnglesDegrees: [-35,-20,20,35], pitchYawAnchorsDegrees: [0,90,180,270], combinations: [] };
  await page.setViewportSize({width: 960, height: 540});
  page.setDefaultTimeout(60000);
  for (const [viewer, viewerPage] of Object.entries(viewerPages)) {
    for (const [model, modelUrl] of Object.entries(models)) {
      const url = viewerPage + '?file=' + encodeURIComponent(modelUrl);
      await page.goto(url, {waitUntil: 'domcontentloaded'});
      await page.waitForFunction(() => document.body.dataset.ready === '1' || document.body.dataset.error);
      const loadState = await page.evaluate(() => ({
        ready: document.body.dataset.ready === '1',
        error: document.body.dataset.error || null,
        title: document.title,
        runtime: window.rotationQA ? {
          engine: window.rotationQA.engine,
          file: window.rotationQA.file,
          bounds: window.rotationQA.bounds,
          webgl2: window.rotationQA.webgl2,
          materials: window.rotationQA.materialMetrics()
        } : null,
        resources: performance.getEntriesByType('resource').filter(r => r.name.endsWith('.glb')).map(r => ({name:r.name, transferSize:r.transferSize, decodedBodySize:r.decodedBodySize}))
      }));
      if (!loadState.ready) throw new Error(viewer + '/' + model + ': ' + loadState.error);
      const combination = {viewer, model, url, loadState, frames: []};
      for (let i=0; i<72; i++) {
        const yaw=i*5, pitch=18, background='light';
        const pose=await page.evaluate(({yaw,pitch,background}) => window.rotationQA.setPose(yaw,pitch,background), {yaw,pitch,background});
        await page.waitForTimeout(25);
        const rel = viewer + '/' + model + '/yaw-' + String(i).padStart(3,'0') + '-' + String(yaw).padStart(3,'0') + 'deg.png';
        await page.screenshot({path: output + '/' + rel, type:'png'});
        combination.frames.push({kind:'yaw',index:i,yawDeg:yaw,pitchDeg:pitch,background,screenshot:rel,pose});
      }
      let pitchIndex=0;
      for (const yaw of [0,90,180,270]) {
        for (const pitch of [-35,-20,20,35]) {
          const background='dark';
          const pose=await page.evaluate(({yaw,pitch,background}) => window.rotationQA.setPose(yaw,pitch,background), {yaw,pitch,background});
          await page.waitForTimeout(25);
          const rel = viewer + '/' + model + '/pitch-' + String(pitchIndex).padStart(2,'0') + '-yaw' + String(yaw).padStart(3,'0') + '-p' + String(pitch).replace('-','m') + '.png';
          await page.screenshot({path: output + '/' + rel, type:'png'});
          combination.frames.push({kind:'pitch',index:pitchIndex++,yawDeg:yaw,pitchDeg:pitch,background,screenshot:rel,pose});
        }
      }
      manifest.combinations.push(combination);
    }
  }
  const downloadPromise=page.waitForEvent('download');
  await page.evaluate(data => {
    const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const anchor=document.createElement('a');anchor.href=URL.createObjectURL(blob);anchor.download='rotation-manifest.json';anchor.click();
  }, manifest);
  const download=await downloadPromise;
  await download.saveAs(output + '/rotation-manifest.json');
  return {combinations:manifest.combinations.length,frames:manifest.combinations.reduce((sum,c)=>sum+c.frames.length,0),manifest:output+'/rotation-manifest.json'};
}
