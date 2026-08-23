(() => {
  const params=new URLSearchParams(location.search);
  const modelKey=params.get('model')==='web'?'web':'standard';
  const viewKey=params.get('view')||'front';
  const run=params.get('run')||'0';
  const file=modelKey==='web'?'Dell-R620-2.5inch-web.glb':'Dell-R620-2.5inch.glb';
  document.querySelector('#meta').textContent=`· ${modelKey} · ${viewKey} · run ${run}`;
  const canvas=document.querySelector('#renderCanvas');
  const engine=new BABYLON.Engine(canvas,true,{preserveDrawingBuffer:true,stencil:true,antialias:true},false);
  engine.setHardwareScalingLevel(1);
  const scene=new BABYLON.Scene(engine);
  scene.useRightHandedSystem=true;
  scene.clearColor=new BABYLON.Color4(.694,.718,.745,1);
  const hemi=new BABYLON.HemisphericLight('hemi',new BABYLON.Vector3(0,1,0),scene);
  hemi.intensity=1.8;hemi.groundColor=new BABYLON.Color3(.35,.40,.45);
  const key=new BABYLON.DirectionalLight('key',new BABYLON.Vector3(-1,-1.6,-1.8),scene);key.intensity=1.7;
  const fill=new BABYLON.DirectionalLight('fill',new BABYLON.Vector3(1,-.3,1),scene);fill.intensity=.7;
  const specs={
    front:{d:[0,0,1],u:[0,1,0],o:1},rear:{d:[0,0,-1],u:[0,1,0],o:1},left:{d:[-1,0,0],u:[0,1,0],o:1},right:{d:[1,0,0],u:[0,1,0],o:1},
    top:{d:[0,1,0],u:[0,0,-1],o:1},bottom:{d:[0,-1,0],u:[0,0,1],o:1},
    'front-left':{d:[-1.15,.56,1.25],u:[0,1,0]},'front-right':{d:[1.15,.56,1.25],u:[0,1,0]},
    'rear-left':{d:[-1.15,.56,-1.25],u:[0,1,0]},'rear-right':{d:[1.15,.56,-1.25],u:[0,1,0]}
  };
  const qa=window.__QA={viewer:'babylon',model:modelKey,view:viewKey,run,loaded:false,error:null,modelFile:file};
  const V=(a)=>new BABYLON.Vector3(...a);
  BABYLON.SceneLoader.ImportMeshAsync('', '../../model/', file, scene).then(async result=>{
    let min=new BABYLON.Vector3(Infinity,Infinity,Infinity),max=new BABYLON.Vector3(-Infinity,-Infinity,-Infinity);
    for(const m of result.meshes){
      if(!m.getBoundingInfo||!m.getTotalVertices||!m.getTotalVertices())continue;
      m.computeWorldMatrix(true);
      const b=m.getBoundingInfo().boundingBox;
      min=BABYLON.Vector3.Minimize(min,b.minimumWorld);max=BABYLON.Vector3.Maximize(max,b.maximumWorld);
    }
    const center=min.add(max).scale(.5),size=max.subtract(min),spec=specs[viewKey]||specs.front,dir=V(spec.d).normalize(),up=V(spec.u).normalize();
    const cam=new BABYLON.FreeCamera('qa-camera',center.add(dir.scale(2)),scene);
    cam.upVector=up;cam.setTarget(center);cam.minZ=.001;cam.maxZ=10;
    if(spec.o){
      cam.mode=BABYLON.Camera.ORTHOGRAPHIC_CAMERA;
      const viewDir=dir.scale(-1),right=BABYLON.Vector3.Cross(viewDir,up).normalize();
      const corners=[];
      for(const x of [min.x,max.x])for(const y of [min.y,max.y])for(const z of [min.z,max.z])corners.push(new BABYLON.Vector3(x,y,z));
      let minR=Infinity,maxR=-Infinity,minU=Infinity,maxU=-Infinity;
      for(const p of corners){
        const d=p.subtract(center),r=BABYLON.Vector3.Dot(d,right),u=BABYLON.Vector3.Dot(d,up);
        minR=Math.min(minR,r);maxR=Math.max(maxR,r);minU=Math.min(minU,u);maxU=Math.max(maxU,u);
      }
      let w=(maxR-minR)*1.12,h=(maxU-minU)*1.18;
      const aspect=engine.getRenderWidth()/engine.getRenderHeight();
      if(w/h<aspect)w=h*aspect;else h=w/aspect;
      cam.orthoLeft=-w/2;cam.orthoRight=w/2;cam.orthoTop=h/2;cam.orthoBottom=-h/2;
    }else{
      cam.fov=28*Math.PI/180;
      const radius=size.length()/2,dist=radius/Math.sin(cam.fov/2)*1.18;
      cam.position=center.add(dir.scale(dist));cam.setTarget(center);
    }
    scene.activeCamera=cam;
    engine.runRenderLoop(()=>scene.render());scene.render();await new Promise(requestAnimationFrame);scene.render();
    qa.loaded=true;qa.bounds={min:min.asArray(),max:max.asArray(),dimensions:size.asArray()};qa.meshes=result.meshes.length;qa.readyAt=new Date().toISOString();
    document.body.dataset.ready='true';document.body.dataset.engine='babylonjs';document.body.dataset.model=modelKey;document.body.dataset.view=viewKey;
    document.querySelector('#status').textContent='READY';
    fetch('/qa-log',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(qa)}).catch(()=>{});
  }).catch(err=>{
    qa.error=String(err);document.body.dataset.ready='error';document.querySelector('#status').textContent='ERROR';
  });
  addEventListener('resize',()=>engine.resize());
})();
