async (page) => {
  const base = "http://127.0.0.1:8936/qa/viewers";
  const viewers = [
    {id: "three", html: "three-viewer.html", renderer: "Three.js"},
    {id: "babylon", html: "babylon-viewer.html", renderer: "Babylon.js"}
  ];
  const modelFacts = {
    standard: {bytes: 25463576, sha256: "80dc0f2030145a0b2320c2d4fbc76a5144d1af62ceb0ad0be91974d6b3043c66"},
    web: {bytes: 1282004, sha256: "18f0cb525689dfea1df6dd5ee4c18a1ffa34b0ff0d95df97f980b32beb5a4d1b"}
  };
  const models = ["standard", "web"];
  const views = ["front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right"];
  const expectedBounds = [439, 44, 623];
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
        if (!info || !info.renderer.startsWith(viewer.renderer) || info.flavor !== model || info.view !== view) {
          throw new Error(`viewer identity/load failure at sequence ${sequence}: ${JSON.stringify(info)}`);
        }
        const actual = info.bounds.size;
        if (actual.some((value, index) => Math.abs(value - expectedBounds[index]) > 0.01)) {
          throw new Error(`bounds failure at sequence ${sequence}: ${JSON.stringify(actual)}`);
        }
        if (!(info.decodedBodySize >= modelFacts[model].bytes)) {
          throw new Error(`fresh full-body proof missing at sequence ${sequence}: ${info.decodedBodySize}`);
        }
        const screenshot = `qa/webgl-loads/${viewer.id}/${model}/${String(sequence).padStart(2, "0")}-${view}.png`;
        await page.screenshot({path: screenshot, type: "png"});
        records.push({
          sequence, started_utc: started, completed_utc: new Date().toISOString(),
          viewer: viewer.id, renderer: info.renderer, webgl: info.webgl,
          model, model_sha256: modelFacts[model].sha256, expected_file_bytes: modelFacts[model].bytes,
          view, run, model_url: info.model,
          load_duration_ms: info.loadDurationMs, resource_duration_ms: info.resourceDurationMs,
          transfer_size_bytes: info.transferSize, decoded_body_size_bytes: info.decodedBodySize,
          mesh_node_count: info.meshCount, bounds_xyz_mm: actual, screenshot, status: "PASS"
        });
      }
    }
  }
  const report = {
    status: "PASS", generated_utc: new Date().toISOString(), required_loads: 40,
    actual_loads: records.length,
    fresh_full_body_proof_count: records.filter(record => record.decoded_body_size_bytes >= record.expected_file_bytes).length,
    viewers: [...new Set(records.map(record => record.renderer))],
    models: modelFacts, views, expected_bounds_xyz_mm: expectedBounds, records
  };
  const downloadPromise = page.waitForEvent("download");
  await page.evaluate(payload => {
    const blob = new Blob([payload], {type: "application/json"});
    const anchor = document.createElement("a");
    anchor.href = URL.createObjectURL(blob);
    anchor.download = "load-events.json";
    document.body.appendChild(anchor); anchor.click(); anchor.remove();
  }, JSON.stringify(report, null, 2) + "\n");
  const download = await downloadPromise;
  await download.saveAs("qa/webgl-loads/load-events.json");
  return {
    status: report.status, actualLoads: report.actual_loads,
    freshFullBodyProofCount: report.fresh_full_body_proof_count,
    rendererCounts: Object.fromEntries(viewers.map(v => [v.id, records.filter(r => r.viewer === v.id).length])),
    modelCounts: Object.fromEntries(models.map(id => [id, records.filter(r => r.model === id).length])),
    first: records[0], last: records.at(-1)
  };
}
