const params=new URLSearchParams(location.search);const modelKey=params.get('model')==='web'?'web':'standard';const initialView=params.get('view')||'front';
const paths={standard:'../../model/Dell-R730-2.5inch.glb',web:'../../model/Dell-R730-2.5inch-web.glb'};
const orbits={front:'0deg 90deg 48%',rear:'180deg 90deg 48%',left:'-90deg 90deg 62%',right:'90deg 90deg 62%',top:'0deg 1deg 86%',bottom:'0deg 179deg 86%','front-top':'0deg 74deg 72%','rear-top':'180deg 63deg 74%','front-left':'-42deg 68deg 65%','front-right':'42deg 68deg 65%','rear-left':'-138deg 68deg 65%','rear-right':'138deg 68deg 65%'};
const mv=document.querySelector('#mv'),status=document.querySelector('#status');mv.src=paths[modelKey];
function setView(name){mv.cameraOrbit=orbits[name]||orbits.front;mv.jumpCameraToGoal();document.body.dataset.view=name;status.textContent=`model-viewer 4.0.0 | ${modelKey} | ${name}`;return true}
function setBackground(kind){document.body.classList.remove('checker-light','checker-dark');if(kind==='light')document.body.classList.add('checker-light');else if(kind==='dark')document.body.classList.add('checker-dark')}
let resolveReady,rejectReady;const readyPromise=new Promise((r,j)=>{resolveReady=r;rejectReady=j});
window.viewerAPI={setView,setBackground,readyPromise,getInfo:()=>({viewer:'model-viewer 4.0.0',model:modelKey,view:document.body.dataset.view,loaded:mv.loaded,progress:mv.getAttribute('data-progress')})};
mv.addEventListener('progress',e=>mv.setAttribute('data-progress',String(e.detail.totalProgress)));
mv.addEventListener('load',()=>{setView(initialView);requestAnimationFrame(()=>requestAnimationFrame(()=>{document.body.dataset.status='ready';resolveReady(window.viewerAPI.getInfo())}))},{once:true});
mv.addEventListener('error',e=>{document.body.dataset.status='error';status.textContent=String(e.detail?.sourceError||e);rejectReady(e)},{once:true});
