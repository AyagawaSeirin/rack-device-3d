async (page) => {
  const evidencePart = page.url().split("evidence=")[1] || "";
  const evidenceDir = decodeURIComponent(evidencePart.split("&")[0]);
  if (!evidenceDir || !evidenceDir.startsWith("/root/Project/rack-device-3d/")) {
    throw new Error("absolute in-scope evidence query parameter is required");
  }
  await page.setViewportSize({width: 480, height: 360});
  await page.waitForFunction(() => window.qaReady === true || window.qaError, null, {timeout: 120000});
  const failure = await page.evaluate(() => window.qaError || null);
  if (failure) throw new Error(failure);
  await page.evaluate(() => {
    const canvas = document.querySelector("canvas");
    canvas.style.width = "480px";
    canvas.style.height = "360px";
  });
  const frames = [];
  for (let index = 0; index < 72; index++) {
    const yaw = index * 5;
    await page.evaluate(async value => window.qaSetOrbit(value, 10), yaw);
    const filename = `yaw-frames/frame-${String(index).padStart(3, "0")}-yaw-${String(yaw).padStart(3, "0")}.jpg`;
    await page.screenshot({path: `${evidenceDir}/${filename}`, type: "jpeg", quality: 78});
    frames.push({kind: "yaw", index, yaw, pitch: 10, filename});
  }
  for (const yaw of [0, 90, 180, 270]) {
    for (const pitch of [-35, -15, 15, 35]) {
      await page.evaluate(async value => window.qaSetOrbit(value.yaw, value.pitch), {yaw, pitch});
      const filename = `pitch-frames/yaw-${String(yaw).padStart(3, "0")}-pitch-${pitch > 0 ? "+" : ""}${pitch}.jpg`;
      await page.screenshot({path: `${evidenceDir}/${filename}`, type: "jpeg", quality: 84});
      frames.push({kind: "pitch", yaw, pitch, filename});
    }
  }
  const runtime = await page.evaluate(() => ({...window.qaInfo, overlayVisible: !document.getElementById("loading").hidden}));
  const manifest = {
    capturedAt: new Date().toISOString(),
    pageUrl: page.url(),
    viewport: {width: 480, height: 360},
    yawStepDegrees: 5,
    yawFrames: 72,
    yawPitchDegrees: 10,
    pitchDegrees: [-35, -15, 15, 35],
    pitchYaws: [0, 90, 180, 270],
    pitchFrames: 16,
    checkerboard: true,
    runtime,
    frames,
  };
  const pending = page.waitForEvent("download");
  await page.evaluate(value => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + "\n"], {type: "application/json"}));
    link.download = "rotation-manifest.json";
    link.click();
  }, manifest);
  const download = await pending;
  await download.saveAs(`${evidenceDir}/rotation-manifest.json`);
  return manifest;
}
