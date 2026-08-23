async (page) => {
  const batch = await page.evaluate(() => new URL(location.href).searchParams.get('batch'));
  const batches = {
    standard_rest: {
      model: 'standard',
      views: ['bottom','front-left','front-right','rear-left','rear-right','front-logo','rear-psu']
    },
    web_ortho: {
      model: 'web',
      views: ['front','rear','left','right','top','bottom']
    },
    web_oblique: {
      model: 'web',
      views: ['front-left','front-right','rear-left','rear-right']
    },
    web_closeups: {
      model: 'web',
      views: ['front-logo','rear-psu']
    }
  };
  const selected = batches[batch];
  if (!selected) throw new Error(`Unknown QA_BATCH ${batch}`);
  for (const view of selected.views) {
    const qaId = `babylon-${selected.model}-${view}`;
    const url = `http://127.0.0.1:8791/qa/viewers/babylon.html?model=${selected.model}&view=${view}&qa=${qaId}`;
    await page.goto(url, {waitUntil: 'domcontentloaded', timeout: 90000});
    await page.waitForFunction(
      () => window.__QA__?.status === 'PASS' && window.__QA__?.server?.ok === true,
      null,
      {timeout: 90000}
    );
    await page.screenshot({
      path: `/root/Project/rack-device-3d/Dell-R7515-3.5inch/qa/renders/babylon/${selected.model}/${view}.png`,
      type: 'png'
    });
    console.log(`PASS babylon ${selected.model} ${view}`);
  }
}
