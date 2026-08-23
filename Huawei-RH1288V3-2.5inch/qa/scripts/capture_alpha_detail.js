async (page) => {
  const base = 'http://127.0.0.1:4173/qa/viewers/three.html';
  const out = '/root/Project/rack-device-3d/Huawei-RH1288V3-2.5inch/qa/renders/alpha-check';
  const darkChecker = () => {
    document.body.style.backgroundColor = '#20252a';
    document.body.style.backgroundImage = [
      'linear-gradient(45deg,#343a40 25%,transparent 25%)',
      'linear-gradient(-45deg,#343a40 25%,transparent 25%)',
      'linear-gradient(45deg,transparent 75%,#343a40 75%)',
      'linear-gradient(-45deg,transparent 75%,#343a40 75%)'
    ].join(',');
  };

  await page.setViewportSize({ width: 1600, height: 900 });
  for (const view of ['front', 'rear']) {
    await page.goto(`${base}?model=standard&view=${view}&rev=final3`,
                    { waitUntil: 'domcontentloaded' });
    await page.waitForFunction(() => document.body.dataset.ready === '1');
    await page.screenshot({ path: `${out}/${view}-light-checker.png` });
    await page.evaluate(darkChecker);
    await page.screenshot({ path: `${out}/${view}-dark-checker.png` });
  }

  await page.setViewportSize({ width: 3200, height: 1800 });
  await page.goto(`${base}?model=standard&view=front&compare=1&rev=final3`,
                  { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => document.body.dataset.ready === '1');
  await page.screenshot({
    path: '/root/Project/rack-device-3d/Huawei-RH1288V3-2.5inch/qa/work/front-final-hires.png'
  });
  return { alphaChecks: 4, detailSource: 'qa/work/front-final-hires.png' };
}
