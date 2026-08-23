async (page) => {
  const root = "http://127.0.0.1:8767";
  const output = "/root/Project/rack-device-3d/HPE-DL360G9-2.5inch/qa/viewer-threejs";
  const views = ["front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right"];
  const models = {
    standard: "../../model/HPE-DL360G9-2.5inch.glb",
    web: "../../model/HPE-DL360G9-2.5inch-web.glb"
  };
  await page.setViewportSize({ width: 1600, height: 1200 });
  for (const [profile, model] of Object.entries(models)) {
    for (const view of views) {
      const url = `${root}/qa/viewer-threejs/index.html?view=${view}&model=${model}`;
      await page.goto(url, { waitUntil: "load", timeout: 120000 });
      await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
      await page.screenshot({ path: `${output}/${profile}-${view}.png`, type: "png" });
    }
    const dark = `${root}/qa/viewer-threejs/index.html?view=front&background=dark&model=${model}`;
    await page.goto(dark, { waitUntil: "load", timeout: 120000 });
    await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
    await page.screenshot({ path: `${output}/${profile}-front-dark.png`, type: "png" });
  }
  return { engine: "Three.js", captures: 22 };
}
