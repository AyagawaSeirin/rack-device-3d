async (page) => {
  const initialUrl = page.url();
  const viewerBase = initialUrl.split("?")[0];
  const modelPart = (initialUrl.split("model=")[1] || "").split("&")[0];
  const evidencePart = (initialUrl.split("evidence=")[1] || "").split("&")[0];
  const modelBase = decodeURIComponent(modelPart).split("?")[0];
  const evidenceDir = decodeURIComponent(evidencePart);
  if (!modelBase.startsWith("/") || !evidenceDir.startsWith("/root/Project/rack-device-3d/")) throw new Error("model/evidence query parameters required");
  const views = [
    ["front",0,0],["rear",180,0],["left",270,0],["right",90,0],
    ["top",0,72],["bottom",0,-72],
    ["front-left",315,25],["front-right",45,25],["rear-left",225,25],["rear-right",135,25],
  ];
  const loads=[];
  for (let index=0; index<views.length; index++) {
    const [name,yaw,pitch]=views[index];
    const nonce=`${Date.now()}-${index}-${name}`;
    const modelUrl=`${modelBase}?cb=${nonce}`;
    const target=`${viewerBase}?model=${encodeURIComponent(modelUrl)}&yaw=${yaw}&pitch=${pitch}&load=${nonce}`;
    await page.goto(target,{waitUntil:"domcontentloaded",timeout:120000});
    await page.setViewportSize({width:640,height:480});
    await page.waitForFunction(()=>window.qaReady===true||window.qaError,null,{timeout:120000});
    const failure=await page.evaluate(()=>window.qaError||null);if(failure)throw new Error(failure);
    await page.evaluate(()=>{const c=document.querySelector("canvas");c.style.width="640px";c.style.height="480px"});
    const runtime=await page.evaluate(()=>({...window.qaInfo,overlayVisible:getComputedStyle(document.getElementById("loading")).display!=="none"}));
    const filename=`${String(index+1).padStart(2,"0")}-${name}.png`;
    await page.screenshot({path:`${evidenceDir}/${filename}`});
    loads.push({index:index+1,name,yaw,pitch,nonce,modelUrl,pageUrl:target,filename,runtime});
  }
  const manifest={capturedAt:new Date().toISOString(),viewerBase,modelBase,loadCount:loads.length,cacheBusted:true,independentPageNavigations:true,loads};
  const pending=page.waitForEvent("download");
  await page.evaluate(value=>{const link=document.createElement("a");link.href=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)+"\n"],{type:"application/json"}));link.download="load-manifest.json";link.click()},manifest);
  const download=await pending;await download.saveAs(`${evidenceDir}/load-manifest.json`);return manifest;
}
