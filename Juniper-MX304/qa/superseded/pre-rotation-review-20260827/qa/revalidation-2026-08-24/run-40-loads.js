async (page) => {
  const base = 'http://127.0.0.1:8767/Juniper-MX304';
  const run = 'mx304-revalidation-2026-08-24';
  const views = ['front', 'rear', 'left', 'right', 'top', 'bottom', 'front_left', 'front_right', 'rear_left', 'rear_right'];
  const loaders = ['three', 'babylon'];
  const queryString = (values) => Object.entries(values)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
  const variants = {
    standard: {
      file: 'Juniper-MX304.glb',
      sha: '6bd23219b2467b756de4d6f8d990ef539a0719136a28b7d8e9ae2b2ec34c3332'
    },
    web: {
      file: 'Juniper-MX304-web.glb',
      sha: '7f240baeb6ce9e8751e49bae90b0a2b40478d75dd76c673f9e2691fe9e9fc9e5'
    }
  };
  const results = [];
  await page.setViewportSize({width: 1200, height: 900});
  for (const loader of loaders) {
    for (const [variant, model] of Object.entries(variants)) {
      for (let index = 0; index < views.length; index += 1) {
        const view = views[index];
        const loadId = `${loader}-${variant}-${String(index + 1).padStart(2, '0')}-${view}`;
        const modelURL = `../../model/${model.file}?load_id=${encodeURIComponent(loadId)}&expected_sha=${model.sha}&loader=${loader}&variant=${variant}&view=${view}&run=${run}`;
        const query = queryString({model: modelURL, view, bg: 'eef0f2', validation_run: run});
        const viewerURL = `${base}/qa/viewers/${loader}.html?${query}`;
        const responsePromise = page.waitForResponse(
          (response) => response.url().includes('.glb') && response.url().includes(`load_id=${loadId}`),
          {timeout: 30000}
        );
        await page.goto(viewerURL, {waitUntil: 'domcontentloaded', timeout: 30000});
        const response = await responsePromise;
        await page.waitForFunction(() => window.__qaReady === true, {timeout: 30000});
        const pageState = await page.evaluate(() => {
          const canvas = document.querySelector('canvas');
          const gl = canvas?.getContext('webgl2') || canvas?.getContext('webgl');
          let renderer = null;
          if (gl) {
            const ext = gl.getExtension('WEBGL_debug_renderer_info');
            renderer = ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
          }
          return {
            qaReady: window.__qaReady === true,
            bodyReady: document.body.dataset.ready === 'true',
            bodyError: document.body.dataset.error || null,
            title: document.title,
            webglRenderer: renderer
          };
        });
        const screenshotPath = `/root/Project/rack-device-3d/Juniper-MX304/revalidation-2026-08-24/loads/${loader}/${variant}/${String(index + 1).padStart(2, '0')}-${view}.png`;
        await page.screenshot({path: screenshotPath});
        const proof = queryString({
          load_id: loadId,
          loader,
          variant,
          view,
          expected_sha: model.sha,
          qa_ready: String(pageState.qaReady),
          body_ready: String(pageState.bodyReady),
          body_error: String(pageState.bodyError),
          run
        });
        const proofStatus = await page.evaluate(async (url) => {
          const response = await fetch(url, {cache: 'no-store'});
          return response.status;
        }, `${base}/revalidation-2026-08-24/web-proof/ready.txt?${proof}`);
        results.push({
          loadId,
          loader,
          variant,
          view,
          expectedSha: model.sha,
          modelResponseStatus: response.status(),
          modelResponseURL: response.url(),
          readyProofStatus: proofStatus,
          screenshotPath,
          ...pageState
        });
      }
    }
  }
  return {run, count: results.length, results};
}
