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
      dimensionsMm: { bodyWidth: 444, overallWidth: 482.4, height: 87.3, flangeToRearBody: 684, overallDepth: 723 },
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
  return gltf.materials.push({ name, pbrMetallicRoughness: pbr, alphaMode: "OPAQUE", doubleSided: false, extensions: { KHR_materials_unlit: {} } }) - 1;
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

const BODY_W=0.444, OVERALL_W=0.4824, H=0.0873, BODY_D=0.684;
const FRONT_PROJ=0.018, REAR_PROJ=0.021, OVERALL_D=0.723;
const Z_FLANGE=BODY_D/2, Z_REAR=-BODY_D/2, Z_FRONT_OUT=Z_FLANGE+FRONT_PROJ, Z_REAR_OUT=Z_REAR-REAR_PROJ;
const Y_TOP=H/2, Y_BOTTOM=-H/2;

// Closed opaque body and four canonical body planes.
addBox("Closed chassis core",[0,0,0],[BODY_W,H-0.001,BODY_D],MAT.silver);
addQuad("Physical left source face","-X",[-BODY_W/2-0.0001,0,(Z_FRONT_OUT+Z_REAR_OUT)/2],[0,H,OVERALL_D],faceMaterials.left);
addQuad("Physical right source face","+X",[BODY_W/2+0.0001,0,(Z_FRONT_OUT+Z_REAR_OUT)/2],[0,H,OVERALL_D],faceMaterials.right);
addQuad("Top source face","+Y",[0,Y_TOP-0.00005,0],[BODY_W,0,BODY_D],faceMaterials.top);
addQuad("Bottom generic-fallback source face","-Y",[0,Y_BOTTOM+0.00005,0],[BODY_W,0,BODY_D],faceMaterials.bottom);

// True open rack-ear holes: each ear is assembled from 64 horizontal bands around two circular voids.
for (const side of [-1,1]) {
  const xMin=side<0?-OVERALL_W/2:BODY_W/2, xMax=side<0?-BODY_W/2:OVERALL_W/2;
  const holeX=(xMin+xMax)/2, radius=0.0039, bands=64, bandH=H/bands;
  for(let i=0;i<bands;i++){
    const y=Y_BOTTOM+bandH*(i+0.5);
    let half=0;
    for(const hy of [-0.029,0.029]){const dy=Math.abs(y-hy);if(dy<radius)half=Math.max(half,Math.sqrt(radius*radius-dy*dy));}
    if(!half){addBox(`Front ${side<0?'left':'right'} ear band ${i+1}`,[holeX,y,Z_FLANGE+0.006],[(xMax-xMin),bandH,0.012],MAT.black);}
    else{
      const lw=holeX-half-xMin,rw=xMax-(holeX+half);
      if(lw>0)addBox(`Front ${side<0?'left':'right'} ear hole-left ${i+1}`,[xMin+lw/2,y,Z_FLANGE+0.006],[lw,bandH,0.012],MAT.black);
      if(rw>0)addBox(`Front ${side<0?'left':'right'} ear hole-right ${i+1}`,[holeX+half+rw/2,y,Z_FLANGE+0.006],[rw,bandH,0.012],MAT.black);
    }
  }
}

// Front control/media block preserves DELL and PowerEdge R720 from the source-locked texture.
const frontUToX=u=>-OVERALL_W/2+u*OVERALL_W;
const controlU0=0.055,controlU1=0.355;
addBox("Front control and media zone body",[(frontUToX(controlU0)+frontUToX(controlU1))/2,0,Z_FLANGE+(FRONT_PROJ-0.0004)/2],[frontUToX(controlU1)-frontUToX(controlU0),H-0.002,FRONT_PROJ-0.0004],MAT.black);
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
function addRearPlate(name,u0,u1,y,h){const x0=rearX(u0),x1=rearX(u1),cx=(x0+x1)/2,w=Math.abs(x1-x0);addBox(`${name} body`,[cx,y,Z_REAR-0.003],[w,h,0.006],MAT.silver);addQuad(`${name} source face`,`-Z`,[cx,y,Z_REAR-0.00601],[w,h,0],faceMaterials.rear,[u0,Math.max(0,0.5-y/H-h/(2*H)),u1,Math.min(1,0.5-y/H+h/(2*H))]);}
function addRearTexturedPort(name,u0,v0,u1,v1,sideMaterial){
  const cx=rearX((u0+u1)/2),cy=H/2-((v0+v1)/2)*H,w=(u1-u0)*BODY_W,h=(v1-v0)*H,depth=0.0045;
  addBox(`${name} recessed body`,[cx,cy,Z_REAR-depth/2],[w,h,depth],sideMaterial);
  addQuad(`${name} exact source face`,`-Z`,[cx,cy,Z_REAR-depth-0.00001],[w,h,0],faceMaterials.rear,[u0,v0,u1,v1]);
}
for(let i=0;i<3;i++)addRearPlate(`Low-profile PCIe blank ${i+1}`,0.026,0.225,0.028-i*0.027,0.019);
for(const [slot,u0,u1,y] of [[4,0.27,0.52,0.028],[5,0.27,0.52,0.001],[6,0.56,0.80,0.028],[7,0.56,0.80,0.001]])addRearPlate(`Full-height PCIe blank ${slot}`,u0,u1,y,0.019);
for(const [slot,u,y] of [[4,0.255,0.028],[5,0.255,0.001],[6,0.545,0.028],[7,0.545,0.001]])addBox(`Blue riser latch ${slot}`,[rearX(u),y,Z_REAR-0.0062],[0.007,0.017,0.0004],MAT.blue);

// Management and I/O groups, ordered exactly from physical-left to physical-right in rear-camera space.
addCylinderZ("Rear system-ID button",[rearX(0.035),-0.030,Z_REAR-0.006],0.004,0.004,20,MAT.darkSilver);
addRearTexturedPort("Rear status connector",0.045,0.73,0.064,0.92,MAT.grille);
addRearTexturedPort("Dedicated iDRAC7 RJ45",0.074,0.67,0.137,0.95,MAT.grille);
addRearTexturedPort("DB9 serial",0.147,0.70,0.220,0.94,MAT.teal);
addRearTexturedPort("Rear VGA",0.225,0.70,0.294,0.94,MAT.blue);
addRearTexturedPort("Rear USB upper",0.302,0.68,0.340,0.805,MAT.grille);
addRearTexturedPort("Rear USB lower",0.302,0.815,0.340,0.95,MAT.grille);
for(let i=0;i<4;i++){const u0=0.355+i*0.055;addRearTexturedPort(`Integrated NDC RJ45 ${i+1}`,u0,0.70,u0+0.045,0.95,MAT.grille);}

// Central U retention handle: real protruding geometry, not a texture-only stripe.
addBox("Rear central retention handle bar",[rearX(0.445),-0.008,Z_REAR_OUT+0.003],[0.145,0.008,0.006],MAT.black);
addBox("Rear central retention handle left post",[rearX(0.445)-0.069,-0.008,Z_REAR-0.010],[0.007,0.008,0.020],MAT.black);
addBox("Rear central retention handle right post",[rearX(0.445)+0.069,-0.008,Z_REAR-0.010],[0.007,0.008,0.020],MAT.black);

// Two matched, side-by-side 750W AC PSU modules with IEC inlet, orange latch, translucent handle and guarded fan.
for(const [index,u0,u1] of [[1,0.625,0.805],[2,0.815,0.995]]){
  const x0=rearX(u0),x1=rearX(u1),cx=(x0+x1)/2,w=Math.abs(x1-x0);
  const psuY=-0.0235;
  addBox(`750W AC PSU ${index} module`,[cx,psuY,Z_REAR-(REAR_PROJ-0.0004)/2],[w,0.040,REAR_PROJ-0.0004],MAT.silver);
  addQuad(`750W AC PSU ${index} source face`,`-Z`,[cx,psuY,Z_REAR_OUT],[w,0.040,0],faceMaterials.rear,[u0,0.53,u1,0.99]);
  addBox(`750W AC PSU ${index} IEC inlet`,[cx-w*0.28,psuY,Z_REAR_OUT+0.00001],[0.027,0.025,0.00002],MAT.black);
  addBox(`750W AC PSU ${index} orange release`,[cx-w*0.47,psuY,Z_REAR_OUT+0.00001],[0.007,0.027,0.00002],MAT.orange);
  addCylinderZ(`750W AC PSU ${index} fan`,[cx+w*0.23,psuY,Z_REAR_OUT+0.00002],0.016,0.00003,32,MAT.grille);
  addCylinderZ(`750W AC PSU ${index} fan hub`,[cx+w*0.23,psuY,Z_REAR_OUT+0.00001],0.0065,0.00002,24,MAT.darkSilver);
  for(const [sx,sy] of [[-1,-1],[-1,1],[1,-1],[1,1]])addCylinderZ(`750W AC PSU ${index} fan screw ${sx},${sy}`,[cx+w*0.23+sx*0.013,psuY+sy*0.013,Z_REAR_OUT+0.00001],0.0018,0.00002,12,MAT.silver);
  addBox(`750W AC PSU ${index} translucent handle bar`,[cx-w*0.02,psuY,Z_REAR_OUT+0.00001],[0.008,0.034,0.00002],MAT.translucentHandle);
}

// Upper-right perforated filler and top/side relief that remains visible in oblique views.
for(let row=0;row<6;row++)for(let col=0;col<11;col++)addBox(`Rear upper-right vent ${row+1}-${col+1}`,[rearX(0.82+col*0.015),0.036-row*0.006,Z_REAR-0.0062],[0.0045,0.004,0.0004],MAT.grille);
addBox("Top front fixed-strip seam",[0,Y_TOP-0.00002,0.292],[BODY_W,0.00004,0.003],MAT.darkSilver);
for(const [side,x,zs] of [["left",-BODY_W/2,[0.275,0.135,-0.055,-0.235]],["right",BODY_W/2,[0.245,0.075,-0.095,-0.265]]]){
  zs.forEach((z,i)=>addBox(`${side} side J-hook ${i+1}`,[x,0.004,z],[0.00002,0.012,0.024],MAT.darkSilver));
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
