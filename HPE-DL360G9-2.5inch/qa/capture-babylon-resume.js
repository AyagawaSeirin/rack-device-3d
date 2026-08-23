async (page) => {
  const root = "http://127.0.0.1:8767";
  const output = "/root/Project/rack-device-3d/HPE-DL360G9-2.5inch/qa/viewer-babylonjs";
  const missing = [
    ["standard", "../../model/HPE-DL360G9-2.5inch.glb", "rear-left"],
    ["standard", "../../model/HPE-DL360G9-2.5inch.glb", "rear-right"],
    ["standard", "../../model/HPE-DL360G9-2.5inch.glb", "front", "dark"],
    ...["front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right"].map(
      view => ["web", "../../model/HPE-DL360G9-2.5inch-web.glb", view]
    ),
    ["web", "../../model/HPE-DL360G9-2.5inch-web.glb", "front", "dark"]
  ];

  await page.setViewportSize({ width: 1600, height: 1200 });
  const captured = [];
  for (const [profile, model, view, background = "neutral"] of missing) {
    const suffix = background === "dark" ? `${view}-dark` : view;
    const url = `${root}/qa/viewer-babylonjs/index.html?view=${view}&background=${background}&model=${model}`;
    await page.goto(url, { waitUntil: "load", timeout: 120000 });
    await page.waitForFunction(() => window.qaReady === true, null, { timeout: 120000 });
    await page.screenshot({ path: `${output}/${profile}-${suffix}.png`, type: "png" });
    captured.push(`${profile}-${suffix}`);
  }
  return { engine: "Babylon.js", captures: captured.length, captured };
}
