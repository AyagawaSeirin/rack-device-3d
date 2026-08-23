async (page) => {
  const root="http://127.0.0.1:8766", out="/root/Project/rack-device-3d/HPE-DL360G9-3.5inch/qa/viewer-babylonjs";
  const standard="../../model/HPE-DL360G9-3.5inch.glb", web="../../model/HPE-DL360G9-3.5inch-web.glb";
  await page.setViewportSize({width:1600,height:1200});
  const jobs=[
    ["standard-front-dark","front",standard,"dark"],
    ["web-front","front",web,"neutral"], ["web-rear","rear",web,"neutral"],
    ["web-left","left",web,"neutral"], ["web-right","right",web,"neutral"], ["web-top","top",web,"neutral"]
  ];
  for(const [name,view,model,background] of jobs){
    await page.goto(`${root}/qa/viewer-babylonjs/index.html?view=${view}&background=${background}&model=${model}`,{waitUntil:"load",timeout:120000});
    await page.waitForFunction(()=>window.qaReady===true,null,{timeout:120000});
    await page.screenshot({path:`${out}/${name}.png`,type:"png"});
  }
  return {engine:"Babylon.js",captures:6};
}
