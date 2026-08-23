async (page) => {
  const root = "http://127.0.0.1:8767";
  const output = "/root/Project/rack-device-3d/HPE-DL360G9-2.5inch/qa/viewer-threejs";
  const model = "../../model/HPE-DL360G9-2.5inch-web.glb";
  const views = ["right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right"];
  await page.setViewportSize({ width: 1600, height: 1200 });
  for (const view of views) {
    await page.goto(`${root}/qa/viewer-threejs/index.html?view=${view}&model=${model}`, {
      waitUntil: "load",
      timeout: 120000
    });
    await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
    await page.screenshot({ path: `${output}/web-${view}.png`, type: "png" });
  }
  await page.goto(`${root}/qa/viewer-threejs/index.html?view=front&background=dark&model=${model}`, {
    waitUntil: "load",
    timeout: 120000
  });
  await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
  await page.screenshot({ path: `${output}/web-front-dark.png`, type: "png" });
  return { engine: "Three.js", profile: "web", captures: 8 };
}
