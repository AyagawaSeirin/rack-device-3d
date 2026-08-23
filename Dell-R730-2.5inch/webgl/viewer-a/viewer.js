import * as THREE from 'three';
import {GLTFLoader} from '../vendor/GLTFLoader.js';

const params=new URLSearchParams(location.search);
const modelKey=params.get('model')==='web'?'web':'standard';
const initialView=params.get('view')||'front';
const paths={standard:'../../model/Dell-R730-2.5inch.glb',web:'../../model/Dell-R730-2.5inch-web.glb'};
const directions={
  front:{d:[0,0,1],u:[0,1,0]},rear:{d:[0,0,-1],u:[0,1,0]},
  left:{d:[-1,0,0],u:[0,1,0]},right:{d:[1,0,0],u:[0,1,0]},
  top:{d:[0,1,0],u:[0,0,-1]},bottom:{d:[0,-1,0],u:[0,0,-1]},
  'front-top':{d:[0,.55,1],u:[0,1,0]},'rear-top':{d:[0,.55,-1],u:[0,1,0]},
  'front-left':{d:[-1,.62,1],u:[0,1,0]},'front-right':{d:[1,.62,1],u:[0,1,0]},
  'rear-left':{d:[-1,.62,-1],u:[0,1,0]},'rear-right':{d:[1,.62,-1],u:[0,1,0]}
};
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(innerWidth,innerHeight);renderer.setClearColor(0x000000,0);
renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.NoToneMapping;
document.body.prepend(renderer.domElement);
const scene=new THREE.Scene();
scene.add(new THREE.HemisphereLight(0xffffff,0x6b7280,1.8));
const key=new THREE.DirectionalLight(0xffffff,2.0);key.position.set(1,2,2);scene.add(key);
const fill=new THREE.DirectionalLight(0xffffff,1.1);fill.position.set(-2,1,-1);scene.add(fill);
let root,box,center;
const camera=new THREE.OrthographicCamera(-1,1,1,-1,.01,10);
const status=document.querySelector('#status');

function corners(b){const a=[];for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z])a.push(new THREE.Vector3(x,y,z));return a}
function setView(name){
  const spec=directions[name]||directions.front; const dir=new THREE.Vector3(...spec.d).normalize(); const up=new THREE.Vector3(...spec.u).normalize();
  camera.up.copy(up);camera.position.copy(center).addScaledVector(dir,1.65);camera.lookAt(center);camera.updateMatrixWorld(true);
  const forward=center.clone().sub(camera.position).normalize();const right=new THREE.Vector3().crossVectors(forward,up).normalize();const actualUp=new THREE.Vector3().crossVectors(right,forward).normalize();
  let hx=0,hy=0;for(const p of corners(box)){const rel=p.clone().sub(center);hx=Math.max(hx,Math.abs(rel.dot(right)));hy=Math.max(hy,Math.abs(rel.dot(actualUp)))}
  const aspect=innerWidth/innerHeight;const halfY=Math.max(hy,hx/aspect)*1.16;camera.left=-halfY*aspect;camera.right=halfY*aspect;camera.top=halfY;camera.bottom=-halfY;camera.updateProjectionMatrix();
  renderer.render(scene,camera);document.body.dataset.view=name;status.textContent=`Three.js | ${modelKey} | ${name}`;return true;
}
function setBackground(kind){document.body.classList.remove('checker-light','checker-dark');if(kind==='light')document.body.classList.add('checker-light');else if(kind==='dark')document.body.classList.add('checker-dark');renderer.render(scene,camera)}
function resize(){renderer.setSize(innerWidth,innerHeight);if(root)setView(document.body.dataset.view||initialView)}addEventListener('resize',resize);

let resolveReady,rejectReady;const readyPromise=new Promise((r,j)=>{resolveReady=r;rejectReady=j});
window.viewerAPI={setView,setBackground,readyPromise,getInfo:()=>({viewer:'Three.js 0.170.0',model:modelKey,view:document.body.dataset.view,nodes:root?.children.length||0,bounds:box?{min:box.min.toArray(),max:box.max.toArray()}:null})};
new GLTFLoader().load(paths[modelKey],gltf=>{root=gltf.scene;scene.add(root);box=new THREE.Box3().setFromObject(root);center=box.getCenter(new THREE.Vector3());setView(initialView);document.body.dataset.status='ready';resolveReady(window.viewerAPI.getInfo())},undefined,error=>{document.body.dataset.status='error';status.textContent=String(error);rejectReady(error)});
