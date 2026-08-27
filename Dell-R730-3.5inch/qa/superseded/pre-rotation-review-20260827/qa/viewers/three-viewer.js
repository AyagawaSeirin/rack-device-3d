import * as THREE from '../../node_modules/three/build/three.module.js';
import { GLTFLoader } from '../../node_modules/three/examples/jsm/loaders/GLTFLoader.js';

const params = new URLSearchParams(location.search);
const modelKey = params.get('model') === 'web' ? 'web' : 'standard';
const viewKey = params.get('view') || 'front';
const run = params.get('run') || '0';
const file = modelKey === 'web' ? 'Dell-R730-3.5inch-web.glb' : 'Dell-R730-3.5inch.glb';
document.querySelector('#meta').textContent = `· ${modelKey} · ${viewKey} · run ${run}`;

const renderer = new THREE.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
renderer.setPixelRatio(1);
renderer.setSize(innerWidth,innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NoToneMapping;
renderer.setClearColor(0xd9dde2,1);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.add(new THREE.HemisphereLight(0xffffff,0x61707e,2.2));
const keyLight = new THREE.DirectionalLight(0xffffff,2.4);
keyLight.position.set(1.5,2.2,2.5);
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0xbfd8ff,1.0);
fillLight.position.set(-2,0.6,-1.5);
scene.add(fillLight);

const views = {
  front:{dir:[0,0,1],up:[0,1,0],ortho:true}, rear:{dir:[0,0,-1],up:[0,1,0],ortho:true},
  left:{dir:[-1,0,0],up:[0,1,0],ortho:true}, right:{dir:[1,0,0],up:[0,1,0],ortho:true},
  top:{dir:[0,1,0],up:[0,0,-1],ortho:true}, bottom:{dir:[0,-1,0],up:[0,0,1],ortho:true},
  'front-left':{dir:[-1.15,.56,1.25],up:[0,1,0]}, 'front-right':{dir:[1.15,.56,1.25],up:[0,1,0]},
  'rear-left':{dir:[-1.15,.56,-1.25],up:[0,1,0]}, 'rear-right':{dir:[1.15,.56,-1.25],up:[0,1,0]},
};

function corners(box){
  const a=[]; for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z])a.push(new THREE.Vector3(x,y,z)); return a;
}
function makeCamera(box,spec){
  const center=box.getCenter(new THREE.Vector3());
  const dir=new THREE.Vector3(...spec.dir).normalize();
  const up=new THREE.Vector3(...spec.up).normalize();
  if(spec.ortho){
    const viewDir=dir.clone().negate();
    const right=new THREE.Vector3().crossVectors(viewDir,up).normalize();
    let minR=Infinity,maxR=-Infinity,minU=Infinity,maxU=-Infinity;
    for(const p of corners(box)){const d=p.clone().sub(center);const r=d.dot(right),u=d.dot(up);minR=Math.min(minR,r);maxR=Math.max(maxR,r);minU=Math.min(minU,u);maxU=Math.max(maxU,u)}
    let w=(maxR-minR)*1.12,h=(maxU-minU)*1.18;
    const aspect=innerWidth/innerHeight;
    if(w/h<aspect)w=h*aspect;else h=w/aspect;
    const cam=new THREE.OrthographicCamera(-w/2,w/2,h/2,-h/2,.001,10);
    cam.position.copy(center).addScaledVector(dir,2);
    cam.up.copy(up); cam.lookAt(center); cam.updateProjectionMatrix(); return cam;
  }
  const sphere=box.getBoundingSphere(new THREE.Sphere());
  const cam=new THREE.PerspectiveCamera(28,innerWidth/innerHeight,.001,10);
  const dist=sphere.radius/Math.sin(THREE.MathUtils.degToRad(cam.fov/2))*1.18;
  cam.position.copy(center).addScaledVector(dir,dist);cam.up.copy(up);cam.lookAt(center);return cam;
}

const qa = window.__QA = {viewer:'three',model:modelKey,view:viewKey,run,loaded:false,error:null};
new GLTFLoader().load(`../../model/${file}`, async (gltf)=>{
  const root=gltf.scene; scene.add(root);
  root.updateMatrixWorld(true);
  const box=new THREE.Box3().setFromObject(root);
  const camera=makeCamera(box,views[viewKey]||views.front);
  renderer.render(scene,camera);
  await new Promise(requestAnimationFrame);
  renderer.render(scene,camera);
  qa.loaded=true;qa.bounds={min:box.min.toArray(),max:box.max.toArray(),dimensions:box.getSize(new THREE.Vector3()).toArray()};
  qa.nodes=root.children.length; qa.readyAt=new Date().toISOString();
  document.querySelector('#status').textContent='READY';
  fetch('/qa-log',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(qa)}).catch(()=>{});
},undefined,(err)=>{qa.error=String(err);document.querySelector('#status').textContent='ERROR';});

