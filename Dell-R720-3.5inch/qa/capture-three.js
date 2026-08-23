async (page) => {
  const root = "http://127.0.0.1:8791/Dell-R720-3.5inch";
  const out = "/root/Project/rack-device-3d/Dell-R720-3.5inch/qa/viewer-threejs";
  const views = ["front","rear","left","right","top","bottom","front-left","front-right","rear-left","rear-right"];
  const models = {
    standard: "../../model/Dell-R720-3.5inch.glb",
    web: "../../model/Dell-R720-3.5inch-web.glb"
  };
  await page.setViewportSize({width:1600,height:1200});
  const errors=[];
  page.on("console", msg=>{if(msg.type()==="error") errors.push(msg.text());});
  for (const [profile,model] of Object.entries(models)) {
    for (const view of views) {
      const url=`${root}/qa/viewer-threejs/index.html?view=${view}&model=${model}`;
      await page.goto(url,{waitUntil:"load",timeout:120000});
      await page.waitForFunction(()=>window.qaReady===true,null,{timeout:120000});
      await page.screenshot({path:`${out}/${profile}/${view}.png`,type:"png"});
    }
  }
  return {engine:"Three.js 0.179.1",captures:40/2,errors};
}
