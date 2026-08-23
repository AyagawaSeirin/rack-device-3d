async (page) => {
  const root = "http://127.0.0.1:8767", output = "/root/Project/rack-device-3d/HPE-DL360G9-2.5inch/qa/viewer-babylonjs";
  const model = "../../model/HPE-DL360G9-2.5inch.glb", views = ["front-left", "front-right", "rear-left", "rear-right"];
  await page.setViewportSize({ width: 1600, height: 1200 });
  for (const view of views) {
    await page.goto(`${root}/qa/viewer-babylonjs/index.html?view=${view}&model=${model}`, { waitUntil: "load", timeout: 120000 });
    await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
    await page.screenshot({ path: `${output}/standard-${view}.png`, type: "png" });
  }
  await page.goto(`${root}/qa/viewer-babylonjs/index.html?view=front&background=dark&model=${model}`, { waitUntil: "load", timeout: 120000 });
  await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
  await page.screenshot({ path: `${output}/standard-front-dark.png`, type: "png" });
  return { engine: "Babylon.js", profile: "standard", captures: [...views, "front-dark"] };
}
