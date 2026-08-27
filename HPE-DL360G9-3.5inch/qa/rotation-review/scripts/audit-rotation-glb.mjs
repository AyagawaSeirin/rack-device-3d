#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import crypto from 'node:crypto';

const [input, outputDir] = process.argv.slice(2);
if (!input || !outputDir) {
  console.error('usage: audit-rotation-glb.mjs <model.glb> <output-dir>');
  process.exit(2);
}

const component = {
  5120: { bytes: 1, get: 'getInt8' },
  5121: { bytes: 1, get: 'getUint8' },
  5122: { bytes: 2, get: 'getInt16' },
  5123: { bytes: 2, get: 'getUint16' },
  5125: { bytes: 4, get: 'getUint32' },
  5126: { bytes: 4, get: 'getFloat32' },
};
const widthFor = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };

function readGlb(file) {
  const bytes = fs.readFileSync(file);
  if (bytes.readUInt32LE(0) !== 0x46546c67 || bytes.readUInt32LE(4) !== 2) throw new Error('not glTF 2 GLB');
  let offset = 12, json, bin;
  while (offset < bytes.length) {
    const length = bytes.readUInt32LE(offset), type = bytes.readUInt32LE(offset + 4);
    const body = bytes.subarray(offset + 8, offset + 8 + length);
    if (type === 0x4e4f534a) json = JSON.parse(body.toString('utf8').trim());
    if (type === 0x004e4942) bin = body;
    offset += 8 + length;
  }
  if (!json || !bin) throw new Error('GLB JSON/BIN chunk missing');
  return { json, bin };
}

const { json: gltf, bin } = readGlb(input);
const accessorCache = new Map();
function accessor(index) {
  if (accessorCache.has(index)) return accessorCache.get(index);
  const a = gltf.accessors[index];
  if (a.sparse) throw new Error(`sparse accessor ${index} unsupported by audit`);
  const v = gltf.bufferViews[a.bufferView], spec = component[a.componentType], n = widthFor[a.type];
  if (!v || !spec || !n) throw new Error(`unsupported accessor ${index}`);
  const stride = v.byteStride || spec.bytes * n;
  const start = (v.byteOffset || 0) + (a.byteOffset || 0);
  const data = new DataView(bin.buffer, bin.byteOffset, bin.byteLength);
  const out = new Array(a.count);
  for (let i = 0; i < a.count; i++) {
    const row = new Array(n);
    for (let j = 0; j < n; j++) row[j] = data[spec.get](start + i * stride + j * spec.bytes, true);
    out[i] = n === 1 ? row[0] : row;
  }
  accessorCache.set(index, out);
  return out;
}

const I = () => [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
function multiply(a, b) {
  const r = new Array(16).fill(0);
  for (let c = 0; c < 4; c++) for (let row = 0; row < 4; row++) {
    for (let k = 0; k < 4; k++) r[c * 4 + row] += a[k * 4 + row] * b[c * 4 + k];
  }
  return r;
}
function localMatrix(node) {
  if (node.matrix) return node.matrix;
  const [x, y, z, w] = node.rotation || [0, 0, 0, 1], [sx, sy, sz] = node.scale || [1, 1, 1];
  const [tx, ty, tz] = node.translation || [0, 0, 0];
  const xx=x*x, yy=y*y, zz=z*z, xy=x*y, xz=x*z, yz=y*z, wx=w*x, wy=w*y, wz=w*z;
  return [
    (1-2*(yy+zz))*sx, (2*(xy+wz))*sx, (2*(xz-wy))*sx, 0,
    (2*(xy-wz))*sy, (1-2*(xx+zz))*sy, (2*(yz+wx))*sy, 0,
    (2*(xz+wy))*sz, (2*(yz-wx))*sz, (1-2*(xx+yy))*sz, 0,
    tx, ty, tz, 1,
  ];
}
function determinant3(m) {
  return m[0]*(m[5]*m[10]-m[6]*m[9])-m[4]*(m[1]*m[10]-m[2]*m[9])+m[8]*(m[1]*m[6]-m[2]*m[5]);
}
function point(m, p) {
  return [m[0]*p[0]+m[4]*p[1]+m[8]*p[2]+m[12], m[1]*p[0]+m[5]*p[1]+m[9]*p[2]+m[13], m[2]*p[0]+m[6]*p[1]+m[10]*p[2]+m[14]];
}
const sub=(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]];
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const length=a=>Math.hypot(a[0],a[1],a[2]);
const normalize=a=>{const l=length(a); return l ? a.map(v=>v/l) : [0,0,0];};

const world = new Array((gltf.nodes || []).length);
const roots = gltf.scenes?.[gltf.scene || 0]?.nodes || [];
function walk(i, parent=I()) {
  world[i] = multiply(parent, localMatrix(gltf.nodes[i]));
  for (const child of gltf.nodes[i].children || []) walk(child, world[i]);
}
for (const root of roots) walk(root);
for (let i=0;i<world.length;i++) if (!world[i]) walk(i);

const negative = [];
for (let i=0;i<world.length;i++) {
  const localDet = determinant3(localMatrix(gltf.nodes[i])), worldDet = determinant3(world[i]);
  if (localDet < 0 || worldDet < 0) negative.push({node:i,name:gltf.nodes[i].name||null,local_determinant:localDet,world_determinant:worldDet});
}

const triangles = [], meshUsers = new Map();
for (let ni=0;ni<(gltf.nodes||[]).length;ni++) {
  const node=gltf.nodes[ni]; if (node.mesh === undefined) continue;
  if (!meshUsers.has(node.mesh)) meshUsers.set(node.mesh, []); meshUsers.get(node.mesh).push(ni);
  const mesh=gltf.meshes[node.mesh];
  for (let pi=0;pi<(mesh.primitives||[]).length;pi++) {
    const primitive=mesh.primitives[pi]; if ((primitive.mode ?? 4) !== 4 || primitive.attributes?.POSITION === undefined) continue;
    const positions=accessor(primitive.attributes.POSITION), indices=primitive.indices===undefined?positions.map((_,i)=>i):accessor(primitive.indices);
    const normals=primitive.attributes.NORMAL===undefined?null:accessor(primitive.attributes.NORMAL);
    for (let k=0;k+2<indices.length;k+=3) {
      const ids=[indices[k],indices[k+1],indices[k+2]], v=ids.map(id=>point(world[ni],positions[id]));
      const raw=cross(sub(v[1],v[0]),sub(v[2],v[0])), area=length(raw)/2, normal=normalize(raw);
      let normalDot=null;
      if (normals) {
        const n=normals[ids[0]], transformed=normalize([
          world[ni][0]*n[0]+world[ni][4]*n[1]+world[ni][8]*n[2],
          world[ni][1]*n[0]+world[ni][5]*n[1]+world[ni][9]*n[2],
          world[ni][2]*n[0]+world[ni][6]*n[1]+world[ni][10]*n[2],
        ]);
        normalDot=dot(normal,transformed);
      }
      triangles.push({id:triangles.length,node:ni,nodeName:node.name||`node-${ni}`,mesh:node.mesh,meshName:mesh.name||`mesh-${node.mesh}`,primitive:pi,material:primitive.material??null,v,normal,area,normalDot});
    }
  }
}

let maxAbs=1;
for (const t of triangles) for (const v of t.v) for (const x of v) maxAbs=Math.max(maxAbs,Math.abs(x));
const eps=maxAbs*1e-7, q=x=>Math.round(x/eps), vertexKey=v=>`${q(v[0])},${q(v[1])},${q(v[2])}`;
const triKey=t=>t.v.map(vertexKey).sort().join('|');
const exactGroups=new Map();
for (const t of triangles) { const key=triKey(t); if(!exactGroups.has(key)) exactGroups.set(key,[]); exactGroups.get(key).push(t); }
const duplicateGroups=[];
for (const group of exactGroups.values()) if(group.length>1) duplicateGroups.push({
  count:group.length,
  opposing_normals:group.some((a,i)=>group.some((b,j)=>j>i&&dot(a.normal,b.normal)<-0.9999)),
  triangles:group.map(t=>({node:t.node,node_name:t.nodeName,mesh:t.mesh,mesh_name:t.meshName,primitive:t.primitive,material:t.material})),
});

function polygonArea(poly){let s=0;for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length];s+=a[0]*b[1]-a[1]*b[0];}return s/2;}
function clip(subject, clipper) {
  let out=subject.slice(), sign=Math.sign(polygonArea(clipper))||1;
  for(let i=0;i<clipper.length;i++){
    const a=clipper[i], b=clipper[(i+1)%clipper.length], input=out; out=[];
    const inside=p=>sign*((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))>=-eps;
    const intersect=(p,q)=>{const rx=q[0]-p[0],ry=q[1]-p[1],sx=b[0]-a[0],sy=b[1]-a[1],den=rx*sy-ry*sx;if(Math.abs(den)<1e-20)return q;const t=((a[0]-p[0])*sy-(a[1]-p[1])*sx)/den;return[p[0]+t*rx,p[1]+t*ry];};
    for(let j=0;j<input.length;j++){const p=input[j],qv=input[(j+1)%input.length],pin=inside(p),qin=inside(qv);if(pin&&qin)out.push(qv);else if(pin&&!qin)out.push(intersect(p,qv));else if(!pin&&qin){out.push(intersect(p,qv));out.push(qv);}}
    if(!out.length) break;
  }
  return out;
}
const planeBuckets=new Map();
for (const t of triangles) {
  if(t.area<=eps*eps) continue;
  let n=t.normal.slice(); const first=n.find(v=>Math.abs(v)>1e-8); if(first<0)n=n.map(v=>-v);
  const d=dot(n,t.v[0]), key=`${Math.round(n[0]*1e5)},${Math.round(n[1]*1e5)},${Math.round(n[2]*1e5)},${Math.round(d/eps)}`;
  if(!planeBuckets.has(key))planeBuckets.set(key,[]);planeBuckets.get(key).push(t);
}
let coplanarCount=0; const coplanarExamples=[];
for(const group of planeBuckets.values()){
  if(group.length<2)continue;
  const surfaceRisk=t=>/(Texture|SourceLocked|Approved_Imagegen|SourceTextureReveal)/i.test(t.nodeName);
  const risk=group.filter(surfaceRisk); if(!risk.length)continue;
  const seen=new Set();
  for(const a of risk)for(const b of group){
    const pair=[a.id,b.id].sort((x,y)=>x-y); const pairKey=pair.join(':');
    if(a===b||seen.has(pairKey)){continue;} seen.add(pairKey);
    if(a.node===b.node||triKey(a)===triKey(b)||dot(a.normal,b.normal)<0.9999)continue;
    const axis=Math.abs(a.normal[0])>Math.abs(a.normal[1])?(Math.abs(a.normal[0])>Math.abs(a.normal[2])?0:2):(Math.abs(a.normal[1])>Math.abs(a.normal[2])?1:2);
    const axes=[0,1,2].filter(x=>x!==axis), pa=a.v.map(v=>[v[axes[0]],v[axes[1]]]), pb=b.v.map(v=>[v[axes[0]],v[axes[1]]]);
    const overlap=Math.abs(polygonArea(clip(pa,pb))); if(overlap<=eps*eps*25)continue;
    coplanarCount++; if(coplanarExamples.length<200)coplanarExamples.push({node_a:a.nodeName,node_b:b.nodeName,mesh_a:a.meshName,mesh_b:b.meshName,overlap_area:overlap,normal_alignment:dot(a.normal,b.normal)});
  }
}

function pngAlpha(bytes) {
  if(bytes.length<33||bytes.toString('ascii',1,4)!=='PNG')return null;
  let o=8,width,height,depth,type,interlace,idat=[],paletteAlpha=null;
  while(o+12<=bytes.length){const n=bytes.readUInt32BE(o),kind=bytes.toString('ascii',o+4,o+8),data=bytes.subarray(o+8,o+8+n);if(kind==='IHDR'){width=data.readUInt32BE(0);height=data.readUInt32BE(4);depth=data[8];type=data[9];interlace=data[12];}else if(kind==='IDAT')idat.push(data);else if(kind==='tRNS')paletteAlpha=data;else if(kind==='IEND')break;o+=12+n;}
  if(depth!==8||interlace!==0)return {width,height,bit_depth:depth,color_type:type,decoded:false};
  const channels={0:1,2:3,3:1,4:2,6:4}[type]; if(!channels)return {width,height,bit_depth:depth,color_type:type,decoded:false};
  const raw=zlib.inflateSync(Buffer.concat(idat)), stride=width*channels, rows=new Array(height), paeth=(a,b,c)=>{const p=a+b-c,pa=Math.abs(p-a),pb=Math.abs(p-b),pc=Math.abs(p-c);return pa<=pb&&pa<=pc?a:pb<=pc?b:c;};let at=0, prev=Buffer.alloc(stride);
  for(let y=0;y<height;y++){const filter=raw[at++],row=Buffer.alloc(stride);for(let x=0;x<stride;x++){const val=raw[at++],left=x>=channels?row[x-channels]:0,up=prev[x],ul=x>=channels?prev[x-channels]:0;row[x]=(val+(filter===0?0:filter===1?left:filter===2?up:filter===3?Math.floor((left+up)/2):paeth(left,up,ul)))&255;}rows[y]=row;prev=row;}
  let zero=0,partial=0,opaque=0,min=255;
  for(const row of rows)for(let x=0;x<width;x++){let a=255;if(type===6)a=row[x*4+3];else if(type===4)a=row[x*2+1];else if(type===3&&paletteAlpha)a=paletteAlpha[row[x]]??255;min=Math.min(min,a);if(a===0)zero++;else if(a<255)partial++;else opaque++;}
  return {width,height,bit_depth:depth,color_type:type,decoded:true,alpha_min:min,alpha_zero_pixels:zero,alpha_partial_pixels:partial,alpha_opaque_pixels:opaque,total_pixels:width*height};
}
function imageBytes(index){const image=gltf.images[index];if(image.bufferView===undefined)return null;const v=gltf.bufferViews[image.bufferView];return bin.subarray(v.byteOffset||0,(v.byteOffset||0)+v.byteLength);}
const imageAudit=(gltf.images||[]).map((image,i)=>({index:i,name:image.name||null,mime_type:image.mimeType||null,alpha:pngAlpha(imageBytes(i))}));
const materialUsers=new Map();
for(let ni=0;ni<(gltf.nodes||[]).length;ni++){const node=gltf.nodes[ni];if(node.mesh===undefined)continue;for(const p of gltf.meshes[node.mesh].primitives||[]){if(p.material===undefined)continue;if(!materialUsers.has(p.material))materialUsers.set(p.material,[]);materialUsers.get(p.material).push(node.name||`node-${ni}`);}}
const materials=(gltf.materials||[]).map((m,i)=>{const users=[...new Set(materialUsers.get(i)||[])], main=users.some(n=>/(^Face_|TexturePlane|^Texture_(Front|Rear|Left|Right|Top|Bottom))/i.test(n)&&!/Ear/i.test(n));const pbr=m.pbrMetallicRoughness||{},factor=pbr.baseColorFactor||[1,1,1,1],texture=pbr.baseColorTexture?.index,source=texture===undefined?null:gltf.textures?.[texture]?.source;const issues=[];if(main&&(m.alphaMode||'OPAQUE')!=='OPAQUE')issues.push('main face is not OPAQUE');if(main&&factor.some((x,k)=>Math.abs(x-[1,1,1,1][k])>1e-9))issues.push('main face baseColorFactor is not neutral');if(main&&m.doubleSided===true)issues.push('main face is doubleSided');if(factor[3]!==1)issues.push('baseColorFactor alpha is not 1');return{index:i,name:m.name||null,users,main_face:main,alpha_mode:m.alphaMode||'OPAQUE',alpha_cutoff:m.alphaCutoff??null,base_color_factor:factor,double_sided:m.doubleSided===true,unlit:Boolean(m.extensions?.KHR_materials_unlit),texture_index:texture??null,image_index:source??null,image_alpha:source===undefined?null:imageAudit[source]?.alpha,issues};});
const materialUnresolved=materials.flatMap(m=>m.issues.map(issue=>({material:m.index,name:m.name,issue}))).concat(materials.filter(m=>m.main_face&&m.image_alpha?.decoded&&(m.image_alpha.alpha_zero_pixels||m.image_alpha.alpha_partial_pixels)).map(m=>({material:m.index,name:m.name,issue:'main face embedded image contains non-opaque pixels'})));

const cores=[];
for(let ni=0;ni<(gltf.nodes||[]).length;ni++){
  const node=gltf.nodes[ni];if(node.mesh===undefined||!/closed.*(chassis|core|body)|(chassis|core|body).*closed/i.test(node.name||''))continue;
  const edges=new Map();let volume=0,triCount=0,degenerate=0;
  for(const p of gltf.meshes[node.mesh].primitives||[]){if((p.mode??4)!==4)continue;const pos=accessor(p.attributes.POSITION),idx=p.indices===undefined?pos.map((_,i)=>i):accessor(p.indices);for(let k=0;k+2<idx.length;k+=3){const v=[idx[k],idx[k+1],idx[k+2]].map(i=>point(world[ni],pos[i]));triCount++;const ar=length(cross(sub(v[1],v[0]),sub(v[2],v[0])))/2;if(ar<=eps*eps)degenerate++;volume+=dot(v[0],cross(v[1],v[2]))/6;for(const [a,b]of[[v[0],v[1]],[v[1],v[2]],[v[2],v[0]]]){const key=[vertexKey(a),vertexKey(b)].sort().join('|');edges.set(key,(edges.get(key)||0)+1);}}}
  const counts=[...edges.values()];cores.push({node:ni,name:node.name,triangles:triCount,boundary_edges:counts.filter(x=>x===1).length,nonmanifold_edges:counts.filter(x=>x>2).length,degenerate_triangles:degenerate,signed_volume:volume,status:counts.every(x=>x===2)&&degenerate===0&&Math.abs(volume)>eps**3?'PASS':'REWORK'});
}

const reversedNormals=triangles.filter(t=>t.normalDot!==null&&t.normalDot<-0.001).map(t=>({node:t.nodeName,mesh:t.meshName,normal_dot:t.normalDot}));
const degenerate=triangles.filter(t=>t.area<=eps*eps).map(t=>({node:t.nodeName,mesh:t.meshName,area:t.area}));
const common={model:path.resolve(input),sha256:crypto.createHash('sha256').update(fs.readFileSync(input)).digest('hex'),generated_at:new Date().toISOString()};
fs.mkdirSync(outputDir,{recursive:true});
const write=(name,data)=>fs.writeFileSync(path.join(outputDir,name),JSON.stringify(data,null,2)+'\n');
write('negative-transform.json',{...common,status:negative.length?'REWORK':'PASS',negative_count:negative.length,negative_transforms:negative,unresolved:negative});
write('material-alpha.json',{...common,status:materialUnresolved.length?'REWORK':'PASS',materials,images:imageAudit,allowed_nonopaque:materials.filter(m=>!m.main_face&&m.alpha_mode==='MASK').map(m=>({material:m.index,name:m.name,users:m.users,reason:'isolated verified rack-ear through-hole surface; geometric ear ring remains authoritative'})),unresolved:materialUnresolved});
const duplicateUnresolved=duplicateGroups.map((g,i)=>({kind:'exact_duplicate_triangle_group',group:i,...g}));
const coplanarUnresolved=coplanarExamples.map((x,i)=>({kind:'coplanar_overlap',example:i,...x}));
write('duplicate-coplanar.json',{...common,status:(duplicateGroups.length||coplanarCount)?'REWORK':'PASS',epsilon:eps,triangle_count:triangles.length,exact_duplicate_group_count:duplicateGroups.length,exact_duplicate_groups:duplicateGroups,coplanar_overlap_count:coplanarCount,coplanar_overlap_examples:coplanarExamples,unresolved:[...duplicateUnresolved,...coplanarUnresolved]});
write('closed-core.json',{...common,status:cores.length&&cores.every(x=>x.status==='PASS')&&!reversedNormals.length&&!degenerate.length?'PASS':'REWORK',cores,reversed_normal_triangle_count:reversedNormals.length,reversed_normal_examples:reversedNormals.slice(0,200),degenerate_triangle_count:degenerate.length,degenerate_examples:degenerate.slice(0,200),unresolved:[...cores.filter(x=>x.status!=='PASS'),...reversedNormals,...degenerate]});
console.log(JSON.stringify({model:input,negative:negative.length,material_unresolved:materialUnresolved.length,duplicate_groups:duplicateGroups.length,coplanar_overlaps:coplanarCount,cores,reversed_normals:reversedNormals.length,degenerate:degenerate.length},null,2));
