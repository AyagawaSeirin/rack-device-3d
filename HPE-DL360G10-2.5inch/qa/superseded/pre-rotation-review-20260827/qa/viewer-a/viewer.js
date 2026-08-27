const canvas = document.querySelector('#c');
const status = document.querySelector('#status');
const params = new URLSearchParams(location.search);
const modelURL = params.get('model') || '../../model/HPE-DL360G10-2.5inch.glb';
const viewName = params.get('view') || 'front-right';
const bgName = params.get('bg') || 'light';
const gl = canvas.getContext('webgl2', { antialias: true, alpha: false, preserveDrawingBuffer: true });
if (!gl) throw new Error('WebGL2 unavailable');

const VS = `#version 300 es
precision highp float;
layout(location=0) in vec3 aPosition;
layout(location=1) in vec3 aNormal;
layout(location=2) in vec2 aUV;
uniform mat4 uModel;
uniform mat4 uViewProjection;
out vec2 vUV;
void main(){ vUV=aUV; gl_Position=uViewProjection*uModel*vec4(aPosition,1.0); }
`;
const FS = `#version 300 es
precision highp float;
in vec2 vUV;
uniform sampler2D uTexture;
uniform vec4 uColor;
uniform int uHasTexture;
uniform int uMask;
uniform float uCutoff;
out vec4 outColor;
void main(){
  vec4 c=uColor;
  if(uHasTexture==1) c*=texture(uTexture,vUV);
  if(uMask==1 && c.a<uCutoff) discard;
  vec3 srgb=mix(12.92*c.rgb,1.055*pow(max(c.rgb,vec3(0.0)),vec3(1.0/2.4))-0.055,step(vec3(0.0031308),c.rgb));
  outColor=vec4(srgb,1.0);
}
`;

function shader(type, src){ const s=gl.createShader(type); gl.shaderSource(s,src); gl.compileShader(s); if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
const program=gl.createProgram(); gl.attachShader(program,shader(gl.VERTEX_SHADER,VS)); gl.attachShader(program,shader(gl.FRAGMENT_SHADER,FS)); gl.linkProgram(program);
if(!gl.getProgramParameter(program,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
const U={
  model:gl.getUniformLocation(program,'uModel'), vp:gl.getUniformLocation(program,'uViewProjection'),
  tex:gl.getUniformLocation(program,'uTexture'), color:gl.getUniformLocation(program,'uColor'),
  hasTex:gl.getUniformLocation(program,'uHasTexture'), mask:gl.getUniformLocation(program,'uMask'), cutoff:gl.getUniformLocation(program,'uCutoff'),
};

const v3={
  sub:(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]],
  dot:(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2],
  cross:(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],
  norm:a=>{const l=Math.hypot(...a)||1;return a.map(x=>x/l)},
  scale:(a,s)=>a.map(x=>x*s),
};
function mul(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++){let s=0;for(let k=0;k<4;k++)s+=a[k*4+r]*b[c*4+k];o[c*4+r]=s}return o}
function trs(t=[0,0,0],q=[0,0,0,1],s=[1,1,1]){const[x,y,z,w]=q,xx=x*x,yy=y*y,zz=z*z,xy=x*y,xz=x*z,yz=y*z,wx=w*x,wy=w*y,wz=w*z;return new Float32Array([
  (1-2*(yy+zz))*s[0],(2*(xy+wz))*s[0],(2*(xz-wy))*s[0],0,
  (2*(xy-wz))*s[1],(1-2*(xx+zz))*s[1],(2*(yz+wx))*s[1],0,
  (2*(xz+wy))*s[2],(2*(yz-wx))*s[2],(1-2*(xx+yy))*s[2],0,
  t[0],t[1],t[2],1]);}
function identity(){return new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])}
function lookAt(eye,target,up){const z=v3.norm(v3.sub(eye,target)),x=v3.norm(v3.cross(up,z)),y=v3.cross(z,x);return new Float32Array([
  x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-v3.dot(x,eye),-v3.dot(y,eye),-v3.dot(z,eye),1]);}
function ortho(l,r,b,t,n,f){return new Float32Array([2/(r-l),0,0,0,0,2/(t-b),0,0,0,0,-2/(f-n),0,-(r+l)/(r-l),-(t+b)/(t-b),-(f+n)/(f-n),1])}
function perspective(fovy,aspect,n,f){const g=1/Math.tan(fovy/2),nf=1/(n-f);return new Float32Array([g/aspect,0,0,0,0,g,0,0,0,0,(f+n)*nf,-1,0,0,2*f*n*nf,0])}

function parseGLB(buf){
  const dv=new DataView(buf); if(dv.getUint32(0,true)!==0x46546c67)throw new Error('not GLB');
  let off=12,json=null,bin=null;
  while(off<buf.byteLength){const len=dv.getUint32(off,true),type=dv.getUint32(off+4,true);off+=8;const chunk=buf.slice(off,off+len);off+=len;if(type===0x4e4f534a)json=JSON.parse(new TextDecoder().decode(chunk));if(type===0x004e4942)bin=chunk;}
  return {json,bin};
}
function componentInfo(type){return type===5126?[Float32Array,gl.FLOAT]:type===5123?[Uint16Array,gl.UNSIGNED_SHORT]:type===5125?[Uint32Array,gl.UNSIGNED_INT]:[Uint8Array,gl.UNSIGNED_BYTE]}
function comps(type){return {SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16}[type]}

const viewDefs={
  front:{dir:[0,0,1],up:[0,1,0],ortho:true}, rear:{dir:[0,0,-1],up:[0,1,0],ortho:true},
  left:{dir:[-1,0,0],up:[0,1,0],ortho:true}, right:{dir:[1,0,0],up:[0,1,0],ortho:true},
  top:{dir:[0,1,0],up:[0,0,-1],ortho:true}, bottom:{dir:[0,-1,0],up:[0,0,1],ortho:true},
  'front-left':{dir:[-.72,.34,.92],up:[0,1,0]}, 'front-right':{dir:[.72,.34,.92],up:[0,1,0]},
  'rear-left':{dir:[-.72,.34,-.92],up:[0,1,0]}, 'rear-right':{dir:[.72,.34,-.92],up:[0,1,0]},
};
function cameraMatrix(name){
  const d=viewDefs[name]||viewDefs['front-right']; const dir=v3.norm(d.dir); const target=[0,0,0]; const dims=[482.6,44.2,707.04];
  const corners=[];for(const x of [-dims[0]/2,dims[0]/2])for(const y of [-dims[1]/2,dims[1]/2])for(const z of [-dims[2]/2,dims[2]/2])corners.push([x,y,z]);
  if(d.ortho){
    const eye=v3.scale(dir,1200),fwd=v3.norm(v3.scale(dir,-1)),right=v3.norm(v3.cross(fwd,d.up)),up=v3.cross(right,fwd);
    let mx=0,my=0;for(const c of corners){mx=Math.max(mx,Math.abs(v3.dot(c,right)));my=Math.max(my,Math.abs(v3.dot(c,up)))}
    mx*=1.10;my*=1.10;const aspect=canvas.width/canvas.height;if(mx/my<aspect)mx=my*aspect;else my=mx/aspect;
    return mul(ortho(-mx,mx,-my,my,.1,3000),lookAt(eye,target,d.up));
  }
  const radius=Math.hypot(...dims)/2,dist=radius/Math.tan(34*Math.PI/360)*1.08,eye=v3.scale(dir,dist);
  return mul(perspective(34*Math.PI/180,canvas.width/canvas.height,.1,5000),lookAt(eye,target,d.up));
}

function clearBackground(){
  const dark=bgName==='checker-dark';
  if(bgName!=='checker-light' && !dark){
    const bg=bgName==='dark'?[.035,.045,.055,1]:[.91,.925,.935,1];
    gl.disable(gl.SCISSOR_TEST);gl.clearColor(...bg);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);return;
  }
  const colors=dark?[[.035,.045,.055,1],[.15,.17,.19,1]]:[[.93,.94,.95,1],[.69,.72,.75,1]];
  const cell=40;gl.enable(gl.SCISSOR_TEST);
  for(let y=0;y<canvas.height;y+=cell)for(let x=0;x<canvas.width;x+=cell){
    gl.scissor(x,y,Math.min(cell,canvas.width-x),Math.min(cell,canvas.height-y));
    gl.clearColor(...colors[((x/cell)+(y/cell))&1]);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  }
  gl.disable(gl.SCISSOR_TEST);
}

async function main(){
  status.textContent=`fetch ${modelURL.split('/').pop()}`;
  const {json,bin}=parseGLB(await (await fetch(modelURL)).arrayBuffer());
  const textures=[];
  for(let i=0;i<(json.textures||[]).length;i++){
    const image=json.images[json.textures[i].source],bv=json.bufferViews[image.bufferView],bytes=bin.slice(bv.byteOffset||0,(bv.byteOffset||0)+bv.byteLength);
    const img=await new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=URL.createObjectURL(new Blob([bytes],{type:image.mimeType}))});
    const t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);gl.texImage2D(gl.TEXTURE_2D,0,gl.SRGB8_ALPHA8,gl.RGBA,gl.UNSIGNED_BYTE,img);gl.generateMipmap(gl.TEXTURE_2D);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);textures.push(t);
  }
  const meshGPU=(json.meshes||[]).map(mesh=>mesh.primitives.map(prim=>{
    const vao=gl.createVertexArray();gl.bindVertexArray(vao);
    for(const [semantic,loc] of [['POSITION',0],['NORMAL',1],['TEXCOORD_0',2]]){const ai=prim.attributes[semantic];if(ai===undefined)continue;const a=json.accessors[ai],bv=json.bufferViews[a.bufferView],offset=(bv.byteOffset||0)+(a.byteOffset||0),[Ctor,glt]=componentInfo(a.componentType),arr=new Ctor(bin,offset,a.count*comps(a.type));const bo=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,bo);gl.bufferData(gl.ARRAY_BUFFER,arr,gl.STATIC_DRAW);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,comps(a.type),glt,false,0,0)}
    const ia=json.accessors[prim.indices],ibv=json.bufferViews[ia.bufferView],io=(ibv.byteOffset||0)+(ia.byteOffset||0),[ICtor,igt]=componentInfo(ia.componentType),iarr=new ICtor(bin,io,ia.count);const ebo=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ebo);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,iarr,gl.STATIC_DRAW);gl.bindVertexArray(null);return{vao,count:ia.count,indexType:igt,material:prim.material};
  }));
  const draws=[];
  function walk(ni,parent){const node=json.nodes[ni],local=node.matrix?new Float32Array(node.matrix):trs(node.translation,node.rotation,node.scale),world=mul(parent,local);if(node.mesh!==undefined)for(const p of meshGPU[node.mesh])draws.push({p,world});for(const c of node.children||[])walk(c,world)}
  for(const root of json.scenes[json.scene||0].nodes)walk(root,identity());

  gl.viewport(0,0,canvas.width,canvas.height);clearBackground();gl.enable(gl.DEPTH_TEST);gl.enable(gl.CULL_FACE);gl.frontFace(gl.CCW);gl.cullFace(gl.BACK);gl.useProgram(program);gl.uniformMatrix4fv(U.vp,false,cameraMatrix(viewName));gl.uniform1i(U.tex,0);
  for(const {p,world} of draws){const mat=json.materials[p.material]||{},pbr=mat.pbrMetallicRoughness||{},color=pbr.baseColorFactor||[1,1,1,1],ti=pbr.baseColorTexture?.index;gl.uniformMatrix4fv(U.model,false,world);gl.uniform4fv(U.color,color);gl.uniform1i(U.hasTex,ti===undefined?0:1);gl.uniform1i(U.mask,mat.alphaMode==='MASK'?1:0);gl.uniform1f(U.cutoff,mat.alphaCutoff||.5);if(ti!==undefined){gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,textures[ti])}gl.bindVertexArray(p.vao);gl.drawElements(gl.TRIANGLES,p.count,p.indexType,0)}
  gl.bindVertexArray(null);status.textContent=`PASS · ${viewName} · ${draws.length} draws · ${json.nodes.length} nodes`;document.querySelector('#tag').textContent=`Viewer A · native WebGL2 · ${modelURL.includes('-web')?'web':'standard'} GLB`;window.__RENDER_DONE__=true;
}
main().catch(e=>{console.error(e);status.textContent=`ERROR ${e.message}`;window.__RENDER_DONE__='error'});
