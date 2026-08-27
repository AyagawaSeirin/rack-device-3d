async page => {
  const base='http://127.0.0.1:4174/Juniper-MX204/qa/revalidation-2026-08-24/viewers';
  const root='/root/Project/rack-device-3d/Juniper-MX204/qa/revalidation-2026-08-24/renders';
  const views=['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right'];
  const engines=['three','babylon'];
  const models=[
    {variant:'standard',path:'/Juniper-MX204/model/Juniper-MX204.glb',sha256:'ebb52cb184647cf599e33fd3fdd7b441d15b85f367e4233a91ad9f494732d696',bytes:12190384},
    {variant:'web',path:'/Juniper-MX204/model/Juniper-MX204-web.glb',sha256:'ceada7361c08e13c88ee6435ab75566c108c0539021f2d90845b9189f3c6c0a7',bytes:7845472}
  ];
  const records=[];
  await page.setViewportSize({width:1600,height:900});
  for(const engine of engines){
    for(const model of models){
      for(const view of views){
        const loadId=`${String(records.length+1).padStart(2,'0')}-${engine}-${model.variant}-${view}`;
        const url=`${base}/${engine}.html?model=${encodeURIComponent(model.path)}&expected=${model.sha256}&view=${encodeURIComponent(view)}&load_id=${encodeURIComponent(loadId)}`;
        await page.goto(url,{waitUntil:'domcontentloaded',timeout:120000});
        await page.waitForFunction(()=>window.__READY===true||Boolean(window.__ERROR),null,{timeout:120000});
        const error=await page.evaluate(()=>window.__ERROR||'');
        if(error)throw new Error(`${loadId}: ${error}`);
        const result=await page.evaluate(()=>window.__LOAD_RESULT);
        if(!result||!result.hash_match||result.bytes!==model.bytes)throw new Error(`${loadId}: invalid proof ${JSON.stringify(result)}`);
        const screenshot=`${root}/${engine}/${model.variant}/${view}.png`;
        await page.screenshot({path:screenshot,type:'png'});
        records.push({...result,variant:model.variant,screenshot,timestamp:new Date().toISOString()});
      }
    }
  }
  return {
    status:'PASS',
    requirement:'2 independent WebGL loaders x 2 current GLBs x 10 prescribed views',
    prescribed_views:views,
    expected_loads:40,
    actual_loads:records.length,
    all_hash_match:records.every(r=>r.hash_match),
    unique_load_ids:new Set(records.map(r=>r.load_id)).size,
    engine_variant_counts:Object.fromEntries(engines.flatMap(e=>models.map(m=>[`${e}-${m.variant}`,records.filter(r=>r.load_id.includes(`-${e}-${m.variant}-`)).length]))),
    records
  };
}
