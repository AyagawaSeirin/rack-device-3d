async (page) => {
  const base = "http://127.0.0.1:8927/qa/viewers";
  const viewers = [
    {id: "three", html: "three-viewer.html", renderer: "Three.js"},
    {id: "babylon", html: "babylon-viewer.html", renderer: "Babylon.js"}
  ];
  const models = ["standard", "web"];
  const expectedHashes = {
    standard: "0d6f8bbfd0993a33014b887ab6c4deabbb94b7a01c79abcecc9c57b04a3e740a",
    web: "e15f5488d4c5eadfeebb00e2056fc49194fe755ff20524aa344d3bc44ab5ff7e"
  };
  const expectedBytes = {standard: 9883884, web: 3492720};
  const expectedLastModified = {
    standard: "Mon, 24 Aug 2026 08:14:51 GMT",
    web: "Mon, 24 Aug 2026 08:14:56 GMT"
  };
  const views = ["front", "rear", "left", "right", "top", "bottom", "front-left", "front-right", "rear-left", "rear-right"];
  const expectedBounds = [482.6, 45.15, 581.58];
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
        if (info.sha256 !== expectedHashes[model] || info.proofBytes !== expectedBytes[model]) {
          throw new Error(`hash/byte proof failure at sequence ${sequence}: ${JSON.stringify(info)}`);
        }
        if (info.lastModified !== expectedLastModified[model]) {
          throw new Error(`GLB mtime proof failure at sequence ${sequence}: ${JSON.stringify(info)}`);
        }
        const actual = info.bounds.size;
        if (actual.some((value, index) => Math.abs(value - expectedBounds[index]) > 0.25)) {
          throw new Error(`bounds failure at sequence ${sequence}: ${JSON.stringify(actual)}`);
        }
        if (!(info.transferSize > 1000000)) {
          throw new Error(`fresh-resource proof missing at sequence ${sequence}: ${info.transferSize}`);
        }
        const screenshot = `qa/webgl-loads/${viewer.id}/${model}/${String(sequence).padStart(2, "0")}-${view}.png`;
        await page.screenshot({path: screenshot, type: "png"});
        records.push({
          sequence, started_utc: started, completed_utc: new Date().toISOString(),
          viewer: viewer.id, renderer: info.renderer, webgl: info.webgl,
          model, view, run, model_url: info.model,
          load_duration_ms: info.loadDurationMs, resource_duration_ms: info.resourceDurationMs,
          transfer_size_bytes: info.transferSize, mesh_count: info.meshCount,
          sha256: info.sha256, proof_bytes: info.proofBytes,
          model_last_modified_http: info.lastModified,
          bounds_xyz_mm: actual, screenshot, status: "PASS"
        });
      }
    }
  }
  const report = {
    status: "PASS", generated_utc: new Date().toISOString(), required_loads: 40,
    actual_loads: records.length,
    fresh_transfer_proof_count: records.filter(record => record.transfer_size_bytes > 1000000).length,
    viewers: [...new Set(records.map(record => record.renderer))],
    models: [...new Set(records.map(record => record.model))], views,
    expected_hashes: expectedHashes, expected_bytes: expectedBytes,
    expected_last_modified_http: expectedLastModified,
    expected_bounds_xyz_mm: expectedBounds, records
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
    freshTransferProofCount: report.fresh_transfer_proof_count,
    rendererCounts: Object.fromEntries(viewers.map(v => [v.id, records.filter(r => r.viewer === v.id).length])),
    modelCounts: Object.fromEntries(models.map(id => [id, records.filter(r => r.model === id).length])),
    first: records[0], last: records.at(-1)
  };
}
