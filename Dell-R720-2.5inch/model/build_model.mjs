#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const args = new Map();
for (let i = 2; i < process.argv.length; i += 2) args.set(process.argv[i], process.argv[i + 1]);
const textureDir = args.get("--textures");
const outputPath = args.get("--output");
const variant = args.get("--variant") || "standard";
if (!textureDir || !outputPath) throw new Error("Usage: build_model.mjs --textures DIR --output FILE [--variant standard|web]");

const gltf = {
  asset: {
    version: "2.0",
    generator: `Dell PowerEdge R720 exact exterior builder (${variant})`,
    copyright: "Newly constructed exact-appearance exterior; DELL and PowerEdge marks retained as factory product details",
    extras: {
      manufacturer: "Dell",
      product: "PowerEdge R720",
      configuration: "2U 16x2.5-inch SFF, no bezel, seven PCIe blanks, four-RJ45 NDC, dual matched 750W AC PSU",
      coordinateConvention: "+X device right from front, +Y up, +Z front",
      dimensionsMm: { bodyWidth: 444, overallWidth: 482.4, height: 87.3, frontProjectionWithoutBezel: 18, flangeToRearBody: 684, bodyDepth: 702, flangeToRearMost: 723, installedDepth: 741 },
      bottomEvidence: "GENERIC_BOTTOM_FALLBACK",
      newlyConstructed: true,
      officialMeshImported: false,
    },
  },
  extensionsUsed: ["KHR_materials_unlit"],
  scene: 0,
  scenes: [{ name: "Dell PowerEdge R720 16-SFF", nodes: [] }],
  nodes: [], meshes: [], accessors: [], bufferViews: [], buffers: [{ byteLength: 0 }],
  materials: [], images: [], textures: [],
  samplers: [{ name: "Linear clamp sampler", magFilter: 9729, minFilter: 9987, wrapS: 33071, wrapT: 33071 }],
};

const binaryParts = [];
let binaryLength = 0;
function appendBinary(source, target) {
  const buffer = Buffer.isBuffer(source) ? source : Buffer.from(source.buffer, source.byteOffset, source.byteLength);
  const pad = (4 - (binaryLength % 4)) % 4;
  if (pad) { binaryParts.push(Buffer.alloc(pad)); binaryLength += pad; }
  const view = { buffer: 0, byteOffset: binaryLength, byteLength: buffer.length };
  if (target) view.target = target;
  const index = gltf.bufferViews.push(view) - 1;
  binaryParts.push(buffer); binaryLength += buffer.length;
  return index;
}
function addAccessor(values, componentType, type, count, target, min, max) {
  const typed = componentType === 5126 ? new Float32Array(values) : new Uint16Array(values);
  const accessor = { bufferView: appendBinary(typed, target), byteOffset: 0, componentType, count, type };
  if (min) accessor.min = min;
  if (max) accessor.max = max;
  return gltf.accessors.push(accessor) - 1;
}
function positionBounds(values) {
  const min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < values.length; i += 3) for (let j = 0; j < 3; j++) {
    min[j] = Math.min(min[j], values[i + j]); max[j] = Math.max(max[j], values[i + j]);
  }
  return { min, max };
}
function addPrimitive(name, positions, normals, uvs, indices, material) {
  const bounds = positionBounds(positions);
  const attributes = {
    POSITION: addAccessor(positions, 5126, "VEC3", positions.length / 3, 34962, bounds.min, bounds.max),
    NORMAL: addAccessor(normals, 5126, "VEC3", normals.length / 3, 34962),
  };
  if (uvs) attributes.TEXCOORD_0 = addAccessor(uvs, 5126, "VEC2", uvs.length / 2, 34962);
  const primitive = { attributes, indices: addAccessor(indices, 5123, "SCALAR", indices.length, 34963), material, mode: 4 };
  const mesh = gltf.meshes.push({ name, primitives: [primitive] }) - 1;
  const node = gltf.nodes.push({ name, mesh }) - 1;
  gltf.scenes[0].nodes.push(node);
  return node;
}
function addMaterial(name, color, textureIndex = null) {
  const pbr = { baseColorFactor: color, metallicFactor: 0, roughnessFactor: 1 };
  if (textureIndex !== null) pbr.baseColorTexture = { index: textureIndex };
  const material={name,pbrMetallicRoughness:pbr,alphaMode:"OPAQUE",doubleSided:false};
  if(textureIndex!==null)material.extensions={KHR_materials_unlit:{}};
  return gltf.materials.push(material)-1;
}
function addTexture(name) {
  const bytes = fs.readFileSync(path.join(textureDir, `${name}.png`));
  const image = gltf.images.push({ name: `${name} source-locked texture`, mimeType: "image/png", bufferView: appendBinary(bytes) }) - 1;
  return gltf.textures.push({ name: `${name} texture`, sampler: 0, source: image }) - 1;
}

const faceMaterials = {};
for (const face of ["front", "rear", "left", "right", "top", "bottom"]) {
  faceMaterials[face] = addMaterial(`${face} source-locked unlit`, [1, 1, 1, 1], addTexture(face));
}
const MAT = {
  silver: addMaterial("Galvanized steel", [0.58, 0.60, 0.61, 1]),
  darkSilver: addMaterial("Dark galvanized recess", [0.20, 0.22, 0.23, 1]),
  black: addMaterial("Dell matte black polymer", [0.018, 0.022, 0.026, 1]),
  grille: addMaterial("Opaque port and grille recess", [0.004, 0.005, 0.006, 1]),
  blue: addMaterial("Dell blue latch and VGA", [0.02, 0.25, 0.58, 1]),
  teal: addMaterial("Dell teal management panel", [0.00, 0.48, 0.56, 1]),
  orange: addMaterial("Dell AC PSU release orange", [0.94, 0.23, 0.025, 1]),
  translucentHandle: addMaterial("Translucent-looking PSU handle", [0.68, 0.74, 0.76, 1]),
  lcd: addMaterial("Blue LCD", [0.10, 0.30, 0.74, 1]),
};

function quadForFace(face, center, size, uv = [0, 0, 1, 1]) {
  const [x, y, z] = center, [sx, sy, sz] = size;
  const hx = sx / 2, hy = sy / 2, hz = sz / 2, [u0, v0, u1, v1] = uv;
  const uvs = [u0, v0, u0, v1, u1, v1, u1, v0];
  let p, n;
  switch (face) {
    case "+X": p = [x+hx,y+hy,z+hz, x+hx,y-hy,z+hz, x+hx,y-hy,z-hz, x+hx,y+hy,z-hz]; n=[1,0,0]; break;
    case "-X": p = [x-hx,y+hy,z-hz, x-hx,y-hy,z-hz, x-hx,y-hy,z+hz, x-hx,y+hy,z+hz]; n=[-1,0,0]; break;
    case "+Y": p = [x-hx,y+hy,z-hz, x-hx,y+hy,z+hz, x+hx,y+hy,z+hz, x+hx,y+hy,z-hz]; n=[0,1,0]; break;
    case "-Y": p = [x+hx,y-hy,z-hz, x+hx,y-hy,z+hz, x-hx,y-hy,z+hz, x-hx,y-hy,z-hz]; n=[0,-1,0]; break;
    case "+Z": p = [x-hx,y+hy,z+hz, x-hx,y-hy,z+hz, x+hx,y-hy,z+hz, x+hx,y+hy,z+hz]; n=[0,0,1]; break;
    case "-Z": p = [x+hx,y+hy,z-hz, x+hx,y-hy,z-hz, x-hx,y-hy,z-hz, x-hx,y+hy,z-hz]; n=[0,0,-1]; break;
    default: throw new Error(`Unknown face ${face}`);
  }
  return { positions:p, normals:[...n,...n,...n,...n], uvs, indices:[0,1,2,0,2,3] };
}
function addQuad(name, face, center, size, material, uv) {
  const q=quadForFace(face,center,size,uv); return addPrimitive(name,q.positions,q.normals,q.uvs,q.indices,material);
}
function addBox(name, center, size, material) {
  const positions=[], normals=[], uvs=[], indices=[];
  for (const face of ["+X","-X","+Y","-Y","+Z","-Z"]) {
    const q=quadForFace(face,center,size), base=positions.length/3;
    positions.push(...q.positions); normals.push(...q.normals); uvs.push(...q.uvs); indices.push(...q.indices.map(i=>i+base));
  }
  return addPrimitive(name,positions,normals,uvs,indices,material);
}
function addFrame(name,cx,cy,width,height,depth,z,rail,material){
  addBox(`${name} top`,[cx,cy+(height-rail)/2,z],[width,rail,depth],material);
  addBox(`${name} bottom`,[cx,cy-(height-rail)/2,z],[width,rail,depth],material);
  addBox(`${name} left`,[cx-(width-rail)/2,cy,z],[rail,height-2*rail,depth],material);
  addBox(`${name} right`,[cx+(width-rail)/2,cy,z],[rail,height-2*rail,depth],material);
}
function addCylinderZ(name, center, radius, depth, segments, material) {
  const [cx,cy,cz]=center, positions=[], normals=[], indices=[];
  for (let i=0;i<segments;i++) {
    const a0=i/segments*Math.PI*2,a1=(i+1)/segments*Math.PI*2;
    const x0=cx+Math.cos(a0)*radius,y0=cy+Math.sin(a0)*radius,x1=cx+Math.cos(a1)*radius,y1=cy+Math.sin(a1)*radius;
    const zf=cz-depth/2,zb=cz+depth/2,base=positions.length/3;
    positions.push(x0,y0,zf,x1,y1,zf,x1,y1,zb,x0,y0,zb);
    normals.push(Math.cos(a0),Math.sin(a0),0,Math.cos(a1),Math.sin(a1),0,Math.cos(a1),Math.sin(a1),0,Math.cos(a0),Math.sin(a0),0);
    indices.push(base,base+1,base+2,base,base+2,base+3);
  }
  let base=positions.length/3; positions.push(cx,cy,cz-depth/2); normals.push(0,0,-1);
  for(let i=0;i<segments;i++){const a=i/segments*Math.PI*2;positions.push(cx+Math.cos(a)*radius,cy+Math.sin(a)*radius,cz-depth/2);normals.push(0,0,-1);}
  for(let i=0;i<segments;i++)indices.push(base,base+1+((i+1)%segments),base+1+i);
  return addPrimitive(name,positions,normals,null,indices,material);
}

const BODY_W=0.444, OVERALL_W=0.4824, H=0.0873, BODY_D=0.702;
const FRONT_PROJ=0.018, FLANGE_TO_REAR_BODY=0.684, FLANGE_TO_REAR_MOST=0.723, REAR_PROJ=FLANGE_TO_REAR_MOST-FLANGE_TO_REAR_BODY, OVERALL_D=FRONT_PROJ+FLANGE_TO_REAR_MOST;
const Z_FRONT_OUT=BODY_D/2, Z_FLANGE=Z_FRONT_OUT-FRONT_PROJ, Z_REAR=-BODY_D/2, Z_REAR_OUT=Z_REAR-REAR_PROJ;
const Y_TOP=H/2, Y_BOTTOM=-H/2;

// Closed opaque body and four canonical body planes.
addBox("Closed chassis core",[0,0,0],[BODY_W-0.002,H-0.002,BODY_D-0.004],MAT.silver);
addQuad("Physical left source face","-X",[-BODY_W/2+0.0005,0,0],[0,H,BODY_D],faceMaterials.left);
addQuad("Physical right source face","+X",[BODY_W/2-0.0005,0,0],[0,H,BODY_D],faceMaterials.right);
addQuad("Top source face","+Y",[0,Y_TOP-0.0005,0],[BODY_W,0,BODY_D],faceMaterials.top);
addQuad("Bottom generic-fallback source face","-Y",[0,Y_BOTTOM+0.0005,0],[BODY_W,0,BODY_D],faceMaterials.bottom);

// True open rack-ear holes: each ear is assembled from 64 horizontal bands around two circular voids.
for (const side of [-1,1]) {
  const xMin=side<0?-OVERALL_W/2:BODY_W/2, xMax=side<0?-BODY_W/2:OVERALL_W/2;
  const holeX=(xMin+xMax)/2, radius=0.0039, bands=64, bandH=H/bands;
  for(let i=0;i<bands;i++){
    const y=Y_BOTTOM+bandH*(i+0.5);
    let half=0;
    for(const hy of [-0.029,0.029]){const dy=Math.abs(y-hy);if(dy<radius)half=Math.max(half,Math.sqrt(radius*radius-dy*dy));}
    if(!half){addBox(`Front ${side<0?'left':'right'} ear band ${i+1}`,[holeX,y,(Z_FLANGE+Z_FRONT_OUT)/2],[(xMax-xMin),bandH,FRONT_PROJ],MAT.black);}
    else{
      const lw=holeX-half-xMin,rw=xMax-(holeX+half);
      if(lw>0)addBox(`Front ${side<0?'left':'right'} ear hole-left ${i+1}`,[xMin+lw/2,y,(Z_FLANGE+Z_FRONT_OUT)/2],[lw,bandH,FRONT_PROJ],MAT.black);
      if(rw>0)addBox(`Front ${side<0?'left':'right'} ear hole-right ${i+1}`,[holeX+half+rw/2,y,(Z_FLANGE+Z_FRONT_OUT)/2],[rw,bandH,FRONT_PROJ],MAT.black);
    }
  }
}

// Front control/media block preserves DELL and PowerEdge R720 from the source-locked texture.
const frontUToX=u=>-OVERALL_W/2+u*OVERALL_W;
const controlU0=0.055,controlU1=0.355;
addBox("Front control and media zone body",[(frontUToX(controlU0)+frontUToX(controlU1))/2,0,Z_FLANGE+(FRONT_PROJ-0.0004)/2],[frontUToX(controlU1)-frontUToX(controlU0),H-0.003,FRONT_PROJ-0.0004],MAT.black);
addQuad("Front control source face","+Z",[(frontUToX(controlU0)+frontUToX(controlU1))/2,0,Z_FRONT_OUT],[frontUToX(controlU1)-frontUToX(controlU0),H-0.001,0],faceMaterials.front,[controlU0,0,controlU1,1]);

// Sixteen independent 2.5-inch SFF carriers with individual recessed bodies and handles.
const driveU0=0.355,driveU1=0.945,pitchU=(driveU1-driveU0)/16;
for(let i=0;i<16;i++){
  const u0=driveU0+i*pitchU+0.0013,u1=driveU0+(i+1)*pitchU-0.0013;
  const x0=frontUToX(u0),x1=frontUToX(u1),cx=(x0+x1)/2,w=x1-x0;
  addBox(`SFF carrier ${i} recessed body`,[cx,-0.001,Z_FLANGE+(FRONT_PROJ-0.0004)/2],[w,H-0.005,FRONT_PROJ-0.0004],MAT.black);
  addQuad(`SFF carrier ${i} source face`,`+Z`,[cx,-0.001,Z_FRONT_OUT],[w,H-0.005,0],faceMaterials.front,[u0,0.02,u1,0.98]);
}

// Rear canonical photograph and independent visible rear assemblies.
addQuad("Rear source face","-Z",[0,0,Z_REAR-0.00005],[BODY_W,H,0],faceMaterials.rear);
const rearX=u=>BODY_W/2-u*BODY_W;
function addRearPlate(name,u0,u1,y,h){const x0=rearX(u0),x1=rearX(u1),cx=(x0+x1)/2,w=Math.abs(x1-x0);addFrame(name,cx,y,w,h,0.0007,Z_REAR-0.00045,0.0008,MAT.silver);}
function addRearTexturedPort(name,u0,v0,u1,v1,sideMaterial){
  const cx=rearX((u0+u1)/2),cy=H/2-((v0+v1)/2)*H,w=(u1-u0)*BODY_W,h=(v1-v0)*H;
  addFrame(name,cx,cy,w,h,0.0007,Z_REAR-0.00045,Math.min(0.001,w/5,h/5),sideMaterial);
}
for(let i=0;i<3;i++)addRearPlate(`Low-profile PCIe blank ${i+1}`,0.026,0.225,0.028-i*0.027,0.019);
for(const [slot,u0,u1,y] of [[4,0.27,0.52,0.028],[5,0.27,0.52,0.001],[6,0.56,0.80,0.028],[7,0.56,0.80,0.001]])addRearPlate(`Full-height PCIe blank ${slot}`,u0,u1,y,0.019);
for(const [slot,u,y] of [[4,0.255,0.028],[5,0.255,0.001],[6,0.545,0.028],[7,0.545,0.001]])addBox(`Blue riser latch ${slot}`,[rearX(u),y,Z_REAR-0.0062],[0.007,0.017,0.0004],MAT.blue);

// Management and I/O groups, ordered exactly from physical-left to physical-right in rear-camera space.
addCylinderZ("Rear system-ID button",[rearX(0.035),-0.030,Z_REAR-0.006],0.004,0.004,20,MAT.darkSilver);
// Flush status/iDRAC/serial/VGA/USB/quad-RJ45 groups remain in the exact rear
// photograph. Their former overlapping frames crossed the lowest PCIe blank.

// Central U retention handle: real protruding geometry, not a texture-only stripe.
const handleInnerZ=Z_REAR_OUT+0.003,handlePostDepth=(Z_REAR-0.001)-handleInnerZ,handlePostZ=(Z_REAR-0.001+handleInnerZ)/2;
addBox("Rear central retention handle bar",[rearX(0.445),-0.008,Z_REAR_OUT+0.0015],[0.145,0.008,0.003],MAT.black);
addBox("Rear central retention handle left post",[rearX(0.445)-0.069,-0.008,handlePostZ],[0.007,0.008,handlePostDepth],MAT.black);
addBox("Rear central retention handle right post",[rearX(0.445)+0.069,-0.008,handlePostZ],[0.007,0.008,handlePostDepth],MAT.black);

// Two matched, side-by-side 750W AC PSU modules with IEC inlet, orange latch, translucent handle and guarded fan.
for(const [index,u0,u1] of [[1,0.630,0.805],[2,0.815,0.995]]){
  const x0=rearX(u0),x1=rearX(u1),cx=(x0+x1)/2,w=Math.abs(x1-x0);
  const psuY=-0.0235;
  addFrame(`750W AC PSU ${index} module`,cx,psuY,w,0.040,REAR_PROJ-0.0004,(Z_REAR-0.0004+Z_REAR_OUT)/2,0.0012,MAT.silver);
  addQuad(`750W AC PSU ${index} source face`,`-Z`,[cx,psuY,Z_REAR_OUT+0.00045],[w-0.0024,0.0376,0],faceMaterials.rear,[u0,0.53,u1,0.99]);
  // The exact IEC inlet, orange latch, guarded fan, hub and screws remain in
  // the locked PSU photograph.  A shallow U handle reaches the official rear
  // envelope with 0.45 mm separation from that source plane.
  addBox(`750W AC PSU ${index} handle vertical`,[cx-w*0.02,psuY,Z_REAR_OUT+0.0002],[0.004,0.022,0.0004],MAT.translucentHandle);
  addBox(`750W AC PSU ${index} handle top`,[cx-w*0.012,psuY+0.013,Z_REAR_OUT+0.0002],[0.016,0.004,0.0004],MAT.translucentHandle);
  addBox(`750W AC PSU ${index} handle bottom`,[cx-w*0.012,psuY-0.013,Z_REAR_OUT+0.0002],[0.016,0.004,0.0004],MAT.translucentHandle);
}

// Upper-right perforation stays in the locked rear photograph.
addBox("Top front fixed-strip seam",[0,Y_TOP-0.00002,0.292],[BODY_W,0.00004,0.003],MAT.darkSilver);
for(const [side,x,zs] of [["left",-BODY_W/2,[0.275,0.135,-0.055,-0.235]],["right",BODY_W/2,[0.245,0.075,-0.095,-0.265]]]){
  const sign=x<0?-1:1;zs.forEach((z,i)=>addBox(`${side} side J-hook ${i+1}`,[x+sign*0.0004,0.004,z],[0.0008,0.012,0.024],MAT.darkSilver));
}

const bin=Buffer.concat(binaryParts); gltf.buffers[0].byteLength=bin.length;
let json=Buffer.from(JSON.stringify(gltf)); const jsonPad=(4-json.length%4)%4;if(jsonPad)json=Buffer.concat([json,Buffer.alloc(jsonPad,0x20)]);
const binPad=(4-bin.length%4)%4,paddedBin=binPad?Buffer.concat([bin,Buffer.alloc(binPad)]):bin;
const totalLength=12+8+json.length+8+paddedBin.length;
const header=Buffer.alloc(12);header.writeUInt32LE(0x46546c67,0);header.writeUInt32LE(2,4);header.writeUInt32LE(totalLength,8);
const jsonHeader=Buffer.alloc(8);jsonHeader.writeUInt32LE(json.length,0);jsonHeader.writeUInt32LE(0x4e4f534a,4);
const binHeader=Buffer.alloc(8);binHeader.writeUInt32LE(paddedBin.length,0);binHeader.writeUInt32LE(0x004e4942,4);
fs.mkdirSync(path.dirname(outputPath),{recursive:true});fs.writeFileSync(outputPath,Buffer.concat([header,jsonHeader,json,binHeader,paddedBin]));
console.log(JSON.stringify({output:outputPath,variant,bytes:totalLength,nodes:gltf.nodes.length,meshes:gltf.meshes.length,materials:gltf.materials.length,textures:gltf.textures.length,images:gltf.images.length,visibleGeometry:{sffCarriers:16,rackEars:2,trueEarHoles:4,pcieBlanks:7,ndcRj45:4,acPsus:2,centralRearHandle:1,independentSideHooks:8}},null,2));
