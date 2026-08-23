async (page) => {
  const base = "http://127.0.0.1:8927/qa/viewers";
  const viewers = [
    {id: "three", html: "three-viewer.html", renderer: "Three.js"},
    {id: "babylon", html: "babylon-viewer.html", renderer: "Babylon.js"}
  ];
  const models = ["standard", "web"];
  const views = ["front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right"];
  const expected = [482.3, 86.8, 795.9];
  const records = [];
  let sequence = 0;
  await page.setViewportSize({width: 1280, height: 900});
  for (const viewer of viewers) {
    for (const model of models) {
      for (const view of views) {
        sequence += 1;
        const run = `final-${String(sequence).padStart(2, "0")}-${Date.now()}`;
        const url = `${base}/${viewer.html}?model=${model}&view=${view}&run=${run}`;
        const started = new Date().toISOString();
        await page.goto(url, {waitUntil: "domcontentloaded", timeout: 120000});
        await page.waitForFunction(() => window.__RENDER_DONE__ === true, null, {timeout: 120000});
        const info = await page.evaluate(() => window.viewerInfo);
        if (!info || !info.renderer.startsWith(viewer.renderer) || info.flavor !== model || info.view !== view || info.webgl !== "WebGL2") {
          throw new Error(`viewer identity/load failure at sequence ${sequence}: ${JSON.stringify(info)}`);
        }
        const actual = info.bounds.size;
        if (actual.some((value, index) => Math.abs(value - expected[index]) > 0.1)) {
          throw new Error(`bounds failure at sequence ${sequence}: ${JSON.stringify(actual)}`);
        }
        if (!(info.transferSize > 1000000)) {
          throw new Error(`fresh-resource proof missing at sequence ${sequence}: ${info.transferSize}`);
        }
        const screenshot = `qa/webgl-loads/${viewer.id}/${model}/${String(sequence).padStart(2, "0")}-${view}.png`;
        await page.screenshot({path: screenshot, type: "png"});
        records.push({
          sequence,
          started_utc: started,
          completed_utc: new Date().toISOString(),
          viewer: viewer.id,
          renderer: info.renderer,
          webgl: info.webgl,
          model,
          view,
          run,
          model_url: info.model,
          load_duration_ms: info.loadDurationMs,
          resource_duration_ms: info.resourceDurationMs,
          transfer_size_bytes: info.transferSize,
          mesh_count: info.meshCount,
          bounds_xyz_mm: actual,
          screenshot,
          status: "PASS"
        });
      }
    }
  }
  const report = {
    status: "PASS",
    generated_utc: new Date().toISOString(),
    required_loads: 40,
    actual_loads: records.length,
    fresh_transfer_proof_count: records.filter(record => record.transfer_size_bytes > 1000000).length,
    viewers: [...new Set(records.map(record => record.renderer))],
    models: [...new Set(records.map(record => record.model))],
    views,
    records
  };
  const downloadPromise = page.waitForEvent("download");
  await page.evaluate(payload => {
    const blob = new Blob([payload], {type: "application/json"});
    const anchor = document.createElement("a");
    anchor.href = URL.createObjectURL(blob);
    anchor.download = "load-events.json";
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
  }, JSON.stringify(report, null, 2) + "\n");
  const download = await downloadPromise;
  await download.saveAs("qa/webgl-loads/load-events.json");
  return {
    status: report.status,
    actualLoads: report.actual_loads,
    freshTransferProofCount: report.fresh_transfer_proof_count,
    rendererCounts: Object.fromEntries([...new Set(records.map(record => record.viewer))].map(id => [id, records.filter(record => record.viewer === id).length])),
    modelCounts: Object.fromEntries(models.map(id => [id, records.filter(record => record.model === id).length])),
    first: records[0],
    last: records.at(-1)
  };
}
