'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

const MM = 0.001;
const D = {
  overallWidth: 482 * MM,
  bodyWidth: 434 * MM,
  height: 86.8 * MM,
  frontWithBezel: 35.84 * MM,
  frontWithoutBezel: 22.0 * MM,
  earToRearWall: 700.7 * MM,
  earToPsuHandle: 736.29 * MM,
  overallDepth: 772.13 * MM,
  earZ: 350.225 * MM,
  rearWallZ: -350.475 * MM,
  bodyFrontZ: 372.225 * MM,
  bodyDepth: 722.7 * MM,
  bodyCenterZ: 10.875 * MM,
  bezelFrontZ: 386.065 * MM,
  psuHandleZ: -386.065 * MM,
  installedCenterZ: 0,
};

function align4(n) { return (n + 3) & ~3; }
function qz(rad) { return [0, 0, Math.sin(rad / 2), Math.cos(rad / 2)]; }

class GltfBuilder {
  constructor(generator) {
    this.parts = [];
    this.byteLength = 0;
    this.bufferViews = [];
    this.accessors = [];
    this.meshes = [];
    this.nodes = [];
    this.materials = [];
    this.images = [];
    this.textures = [];
    this.samplers = [{
      name: 'LinearClamp',
      magFilter: 9729,
      minFilter: 9987,
      wrapS: 33071,
      wrapT: 33071,
    }];
    this.generator = generator;
    this.meshCache = new Map();
    this.rootChildren = [];
  }

  addBytes(data, target) {
    const pad = align4(this.byteLength) - this.byteLength;
    if (pad) {
      this.parts.push(Buffer.alloc(pad));
      this.byteLength += pad;
    }
    const buf = Buffer.isBuffer(data)
      ? data
      : Buffer.from(data.buffer, data.byteOffset, data.byteLength);
    const index = this.bufferViews.length;
    const view = { buffer: 0, byteOffset: this.byteLength, byteLength: buf.length };
    if (target) view.target = target;
    this.bufferViews.push(view);
    this.parts.push(buf);
    this.byteLength += buf.length;
    return index;
  }

  addAccessor(array, type, componentType, target, min, max) {
    const bufferView = this.addBytes(array, target);
    const widths = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 };
    const accessor = {
      bufferView,
      byteOffset: 0,
      componentType,
      count: array.length / widths[type],
      type,
    };
    if (min) accessor.min = min;
    if (max) accessor.max = max;
    this.accessors.push(accessor);
    return this.accessors.length - 1;
  }

  addMaterial(name, color, options = {}) {
    const mat = {
      name,
      pbrMetallicRoughness: {
        baseColorFactor: color,
        metallicFactor: options.metallic ?? 0,
        roughnessFactor: options.roughness ?? 0.72,
      },
      alphaMode: options.alphaMode || 'OPAQUE',
      doubleSided: options.doubleSided ?? false,
    };
    if (options.alphaCutoff !== undefined) mat.alphaCutoff = options.alphaCutoff;
    if (options.unlit) mat.extensions = { KHR_materials_unlit: {} };
    this.materials.push(mat);
    return this.materials.length - 1;
  }

  addTextureMaterial(name, imagePath, alphaMode) {
    const bytes = fs.readFileSync(imagePath);
    const imageView = this.addBytes(bytes);
    const image = this.images.length;
    this.images.push({ name: `${name}_Image`, bufferView: imageView, mimeType: 'image/png' });
    const texture = this.textures.length;
    this.textures.push({ name: `${name}_Texture`, sampler: 0, source: image });
    const mat = {
      name,
      pbrMetallicRoughness: {
        baseColorFactor: [1, 1, 1, 1],
        baseColorTexture: { index: texture, texCoord: 0 },
        metallicFactor: 0,
        roughnessFactor: 1,
      },
      alphaMode,
      doubleSided: false,
      extensions: { KHR_materials_unlit: {} },
    };
    if (alphaMode === 'MASK') mat.alphaCutoff = 0.45;
    this.materials.push(mat);
    return this.materials.length - 1;
  }

  addGeometry(name, geom, material) {
    const positions = new Float32Array(geom.positions);
    const normals = new Float32Array(geom.normals);
    const uvs = new Float32Array(geom.uvs || new Array((positions.length / 3) * 2).fill(0));
    const indices = new Uint16Array(geom.indices);
    const computedMin = [Infinity, Infinity, Infinity];
    const computedMax = [-Infinity, -Infinity, -Infinity];
    for (let i = 0; i < positions.length; i += 3) {
      for (let axis = 0; axis < 3; axis++) {
        computedMin[axis] = Math.min(computedMin[axis], positions[i + axis]);
        computedMax[axis] = Math.max(computedMax[axis], positions[i + axis]);
      }
    }
    const pos = this.addAccessor(positions, 'VEC3', 5126, 34962, geom.min || computedMin, geom.max || computedMax);
    const nor = this.addAccessor(normals, 'VEC3', 5126, 34962);
    const uv = this.addAccessor(uvs, 'VEC2', 5126, 34962);
    const ind = this.addAccessor(indices, 'SCALAR', 5123, 34963, [0], [Math.max(...indices)]);
    this.meshes.push({
      name,
      primitives: [{
        attributes: { POSITION: pos, NORMAL: nor, TEXCOORD_0: uv },
        indices: ind,
        material,
        mode: 4,
      }],
    });
    return this.meshes.length - 1;
  }

  cachedGeometry(key, makeGeom, material) {
    const cacheKey = `${key}:${material}`;
    if (!this.meshCache.has(cacheKey)) {
      this.meshCache.set(cacheKey, this.addGeometry(cacheKey, makeGeom(), material));
    }
    return this.meshCache.get(cacheKey);
  }

  addNode(name, mesh, translation, scale, rotation, extras = {}) {
    const node = { name, mesh, translation, scale, extras };
    if (rotation) node.rotation = rotation;
    this.nodes.push(node);
    const index = this.nodes.length - 1;
    this.rootChildren.push(index);
    return index;
  }

  addEmptyNode(name, extras) {
    this.nodes.push({ name, extras });
    const index = this.nodes.length - 1;
    this.rootChildren.push(index);
    return index;
  }

  write(outPath, extras) {
    const binPad = align4(this.byteLength) - this.byteLength;
    if (binPad) {
      this.parts.push(Buffer.alloc(binPad));
      this.byteLength += binPad;
    }
    const rootIndex = this.nodes.length;
    this.nodes.push({
      name: 'Dell_PowerEdge_R7525_24SFF_Installed_Assembly',
      children: this.rootChildren,
      extras: {
        manufacturer: 'Dell Technologies',
        product: 'PowerEdge R7525',
        physicalVariant: '24 x 2.5-inch SFF, LCD bezel installed, no rear drives, Riser 3 serial DB9, dual 2400W AC PSU',
      },
    });
    const gltf = {
      asset: {
        version: '2.0',
        generator: this.generator,
        copyright: 'Independent exact-appearance reconstruction; Dell marks retained as factual product details.',
        extras,
      },
      extensionsUsed: ['KHR_materials_unlit'],
      scene: 0,
      scenes: [{ name: 'Installed_R7525', nodes: [rootIndex] }],
      nodes: this.nodes,
      meshes: this.meshes,
      materials: this.materials,
      samplers: this.samplers,
      textures: this.textures,
      images: this.images,
      accessors: this.accessors,
      bufferViews: this.bufferViews,
      buffers: [{ byteLength: this.byteLength }],
    };
    let json = Buffer.from(JSON.stringify(gltf));
    const jsonPad = align4(json.length) - json.length;
    if (jsonPad) json = Buffer.concat([json, Buffer.alloc(jsonPad, 0x20)]);
    const bin = Buffer.concat(this.parts);
    const total = 12 + 8 + json.length + 8 + bin.length;
    const header = Buffer.alloc(12);
    header.writeUInt32LE(0x46546c67, 0);
    header.writeUInt32LE(2, 4);
    header.writeUInt32LE(total, 8);
    const jsonHeader = Buffer.alloc(8);
    jsonHeader.writeUInt32LE(json.length, 0);
    jsonHeader.writeUInt32LE(0x4e4f534a, 4);
    const binHeader = Buffer.alloc(8);
    binHeader.writeUInt32LE(bin.length, 0);
    binHeader.writeUInt32LE(0x004e4942, 4);
    fs.writeFileSync(outPath, Buffer.concat([header, jsonHeader, json, binHeader, bin]));
  }
}

function cubeGeometry() {
  const p = [];
  const n = [];
  const uv = [];
  const ind = [];
  const faces = [
    [[-0.5,-0.5, 0.5],[ 0.5,-0.5, 0.5],[ 0.5, 0.5, 0.5],[-0.5, 0.5, 0.5],[0,0,1]],
    [[ 0.5,-0.5,-0.5],[-0.5,-0.5,-0.5],[-0.5, 0.5,-0.5],[ 0.5, 0.5,-0.5],[0,0,-1]],
    [[ 0.5,-0.5, 0.5],[ 0.5,-0.5,-0.5],[ 0.5, 0.5,-0.5],[ 0.5, 0.5, 0.5],[1,0,0]],
    [[-0.5,-0.5,-0.5],[-0.5,-0.5, 0.5],[-0.5, 0.5, 0.5],[-0.5, 0.5,-0.5],[-1,0,0]],
    [[-0.5, 0.5, 0.5],[ 0.5, 0.5, 0.5],[ 0.5, 0.5,-0.5],[-0.5, 0.5,-0.5],[0,1,0]],
    [[-0.5,-0.5,-0.5],[ 0.5,-0.5,-0.5],[ 0.5,-0.5, 0.5],[-0.5,-0.5, 0.5],[0,-1,0]],
  ];
  for (const f of faces) {
    const base = p.length / 3;
    for (let i = 0; i < 4; i++) {
      p.push(...f[i]); n.push(...f[4]);
      uv.push(i === 1 || i === 2 ? 1 : 0, i >= 2 ? 0 : 1);
    }
    ind.push(base, base+1, base+2, base, base+2, base+3);
  }
  return { positions: p, normals: n, uvs: uv, indices: ind };
}

function cylinderGeometry(segments = 24) {
  const p = [], n = [], uv = [], ind = [];
  for (let i = 0; i <= segments; i++) {
    const a = (i / segments) * Math.PI * 2;
    const x = Math.cos(a) * 0.5, y = Math.sin(a) * 0.5;
    p.push(x,y,-0.5, x,y,0.5); n.push(x*2,y*2,0, x*2,y*2,0); uv.push(i/segments,1, i/segments,0);
  }
  for (let i = 0; i < segments; i++) {
    const b=i*2; ind.push(b,b+1,b+3,b,b+3,b+2);
  }
  const frontCenter=p.length/3; p.push(0,0,0.5); n.push(0,0,1); uv.push(0.5,0.5);
  const backCenter=p.length/3; p.push(0,0,-0.5); n.push(0,0,-1); uv.push(0.5,0.5);
  for (let i=0;i<segments;i++) {
    const a=(i*2)+1, b=(((i+1)%segments)*2)+1;
    ind.push(frontCenter,a,b);
    const c=i*2, d=((i+1)%segments)*2;
    ind.push(backCenter,d,c);
  }
  return {positions:p,normals:n,uvs:uv,indices:ind};
}

function hexRingGeometry() {
  const p=[], n=[], uv=[], ind=[];
  const outer=0.5, inner=0.43;
  for (const z of [-0.5,0.5]) {
    for (const r of [outer,inner]) {
      for (let i=0;i<6;i++) {
        const a=Math.PI/6+i*Math.PI/3;
        p.push(Math.cos(a)*r,Math.sin(a)*r,z);
        n.push(0,0,z>0?1:-1); uv.push(0.5+Math.cos(a)*r,0.5-Math.sin(a)*r);
      }
    }
  }
  const of=0, inf=6, ob=12, inb=18;
  for (let i=0;i<6;i++) {
    const j=(i+1)%6;
    ind.push(of+i,of+j,inf+j, of+i,inf+j,inf+i);
    ind.push(ob+i,inb+j,ob+j, ob+i,inb+i,inb+j);
    ind.push(of+i,ob+j,of+j, of+i,ob+i,ob+j);
    ind.push(inf+i,inf+j,inb+j, inf+i,inb+j,inb+i);
  }
  return {positions:p,normals:n,uvs:uv,indices:ind};
}

function planeGeometry(face) {
  const specs = {
    front: [
      [-0.5,-0.5,0],[0.5,-0.5,0],[0.5,0.5,0],[-0.5,0.5,0],[0,0,1]
    ],
    rear: [
      [0.5,-0.5,0],[-0.5,-0.5,0],[-0.5,0.5,0],[0.5,0.5,0],[0,0,-1]
    ],
    right: [
      [0,-0.5,0.5],[0,-0.5,-0.5],[0,0.5,-0.5],[0,0.5,0.5],[1,0,0]
    ],
    left: [
      [0,-0.5,-0.5],[0,-0.5,0.5],[0,0.5,0.5],[0,0.5,-0.5],[-1,0,0]
    ],
    top: [
      [-0.5,0,0.5],[0.5,0,0.5],[0.5,0,-0.5],[-0.5,0,-0.5],[0,1,0]
    ],
    bottom: [
      [0.5,0,0.5],[-0.5,0,0.5],[-0.5,0,-0.5],[0.5,0,-0.5],[0,-1,0]
    ],
  };
  const s=specs[face], positions=s.slice(0,4).flat(), normal=s[4], normals=[];
  for(let i=0;i<4;i++) normals.push(...normal);
  return {positions,normals,uvs:[0,1,1,1,1,0,0,0],indices:[0,1,2,0,2,3]};
}

function buildVariant(textureDir, outputName, variant) {
  const b = new GltfBuilder(`Codex exact-appearance R7525 builder (${variant})`);
  const mat = {};
  mat.silver = b.addMaterial('Galvanized_Silver', [0.56,0.58,0.59,1], {metallic:0.32,roughness:0.64});
  mat.silverDark = b.addMaterial('Stamped_Silver_Dark', [0.34,0.36,0.37,1], {metallic:0.25,roughness:0.7});
  mat.graphite = b.addMaterial('Bezel_Graphite', [0.12,0.13,0.14,1], {metallic:0.15,roughness:0.58});
  mat.black = b.addMaterial('Port_Black', [0.018,0.022,0.025,1], {metallic:0.02,roughness:0.8});
  mat.vent = b.addMaterial('Vent_Recess', [0.006,0.008,0.009,1], {metallic:0,roughness:0.95});
  mat.orange = b.addMaterial('Dell_Release_Orange', [0.92,0.28,0.025,1], {metallic:0,roughness:0.52});
  mat.blue = b.addMaterial('Dell_Service_Blue', [0.015,0.28,0.68,1], {metallic:0.05,roughness:0.5});
  mat.green = b.addMaterial('Status_Green', [0.01,0.72,0.13,1], {metallic:0,roughness:0.4});
  mat.white = b.addMaterial('Factory_Marking_White', [0.97,0.97,0.96,1], {metallic:0,roughness:0.55});
  mat.screen = b.addMaterial('LCD_Black_Glass', [0.012,0.018,0.022,1], {metallic:0.08,roughness:0.23});
  mat.frontTex = b.addTextureMaterial('Face_Front_SourceLocked', path.join(textureDir,'front.png'), 'OPAQUE');
  mat.rearTex = b.addTextureMaterial('Face_Rear_SourceLocked', path.join(textureDir,'rear.png'), 'OPAQUE');
  mat.leftTex = b.addTextureMaterial('Face_Left_SourceLocked', path.join(textureDir,'left.png'), 'OPAQUE');
  mat.rightTex = b.addTextureMaterial('Face_Right_SourceLocked', path.join(textureDir,'right.png'), 'OPAQUE');
  mat.topTex = b.addTextureMaterial('Face_Top_SourceLocked', path.join(textureDir,'top.png'), 'OPAQUE');
  mat.bottomTex = b.addTextureMaterial('Face_Bottom_OfficialAR_MultiReference', path.join(textureDir,'bottom.png'), 'OPAQUE');
  mat.frontLogoTex = b.addTextureMaterial('Factory_DELL_EMC_Badge_SourceLocked', path.join(ROOT,'qa','build','front-logo-source.png'), 'OPAQUE');

  const cube = (m) => b.cachedGeometry('UnitCube', cubeGeometry, m);
  const cylinder = (m) => b.cachedGeometry('UnitCylinder24', () => cylinderGeometry(24), m);
  const hex = (m) => b.cachedGeometry('UnitHexRing', hexRingGeometry, m);
  const plane = (f,m) => b.cachedGeometry(`UnitPlane_${f}`, () => planeGeometry(f), m);
  const box = (name, material, t, s, r, extras={}) => b.addNode(name,cube(material),t,s,r,extras);
  const cyl = (name, material, t, s, extras={}) => b.addNode(name,cylinder(material),t,s,null,extras);

  // Closed enclosure and six source-locked exterior cards.
  box('Closed_Chassis_Body',mat.silver,[0,0,(D.bodyFrontZ+D.rearWallZ)/2],[D.bodyWidth,D.height,D.bodyFrontZ-D.rearWallZ],null,{category:'closed-shell'});
  b.addNode('Texture_Front',plane('front',mat.frontTex),[0,0,D.bezelFrontZ-0.0009],[D.overallWidth,D.height,1],null,{face:'front',sourceLocked:true});
  b.addNode('Texture_Rear',plane('rear',mat.rearTex),[0,0,D.rearWallZ-0.00015],[D.bodyWidth,D.height,1],null,{face:'rear',sourceLocked:true});
  b.addNode('Texture_Right',plane('right',mat.rightTex),[D.bodyWidth/2+0.00012,0,D.bodyCenterZ],[1,D.height,D.bodyDepth],null,{face:'right',sourceLocked:true,embedding:'opaque body crop'});
  b.addNode('Texture_Left',plane('left',mat.leftTex),[-D.bodyWidth/2-0.00012,0,D.bodyCenterZ],[1,D.height,D.bodyDepth],null,{face:'left',sourceLocked:true,embedding:'opaque body crop'});
  b.addNode('Texture_Top',plane('top',mat.topTex),[0,D.height/2,D.bodyCenterZ],[D.bodyWidth,1,D.bodyDepth],null,{face:'top',sourceLocked:true,embedding:'opaque body crop'});
  b.addNode('Texture_Bottom',plane('bottom',mat.bottomTex),[0,-D.height/2,D.bodyCenterZ],[D.bodyWidth,1,D.bodyDepth],null,{face:'bottom',productionMode:'MULTI_REFERENCE_RECONSTRUCTION',primaryGeometrySource:'official Dell AR GLB',embedding:'opaque body crop'});

  // Front ears/control housings and mounted bezel volume.
  const bezelBackingFront = D.bezelFrontZ - 0.0017;
  box('Front_Left_Control_Housing',mat.graphite,[-0.229,0,(D.earZ+bezelBackingFront)/2],[0.024,D.height,bezelBackingFront-D.earZ],null,{category:'rack-ear-control-backing'});
  box('Front_Right_Control_Housing',mat.graphite,[0.229,0,(D.earZ+bezelBackingFront)/2],[0.024,D.height,bezelBackingFront-D.earZ],null,{category:'rack-ear-control-backing'});
  box('Front_Bezel_Recess',mat.black,[0,0,(D.bodyFrontZ+bezelBackingFront)/2],[0.41,0.079,bezelBackingFront-D.bodyFrontZ],null,{category:'bezel-backing-behind-texture-and-lattice'});
  box('Bezel_Top_Rail',mat.graphite,[0,0.0385,D.bezelFrontZ-0.0016],[0.41,0.008,0.0032],null,{category:'bezel-rail'});
  box('Bezel_Bottom_Rail',mat.graphite,[0,-0.0385,D.bezelFrontZ-0.0016],[0.41,0.008,0.0032],null,{category:'bezel-rail'});

  // Twenty-four portrait SFF carriers behind the installed bezel; every carrier remains separate.
  const carrierStartX=-0.1932;
  const carrierPitch=0.0168;
  for (let drive=0;drive<24;drive++) {
    const id=drive+1;
    const x=carrierStartX+drive*carrierPitch;
    box(`SFF_Carrier_${String(id).padStart(2,'0')}`,mat.black,[x,-0.001,D.bodyFrontZ+0.003],[0.0153,0.071,0.006],null,{category:'2.5-inch-SFF-carrier',slot:drive});
    box(`SFF_Handle_${String(id).padStart(2,'0')}`,mat.silverDark,[x,-0.020,D.bodyFrontZ+0.007],[0.0023,0.031,0.003],null,{category:'carrier-handle'});
    cyl(`SFF_Release_${String(id).padStart(2,'0')}`,mat.orange,[x,0.016,D.bodyFrontZ+0.009],[0.0064,0.0064,0.002],{category:'carrier-release'});
    box(`SFF_Status_${String(id).padStart(2,'0')}`,mat.green,[x+0.0035,0.031,D.bodyFrontZ+0.0095],[0.003,0.003,0.001],null,{category:'carrier-status'});
  }

  // Eleven large non-XE9680 Dell 15G bezel openings: 6 upper, 5 staggered lower.
  const upper=[-0.170,-0.102,-0.034,0.034,0.102,0.170];
  const lower=[-0.136,-0.068,0,0.068,0.136];
  let hc=0;
  for (const x of upper) b.addNode(`Bezel_Hex_Upper_${++hc}`,hex(mat.silverDark),[x,0.019,D.bezelFrontZ-0.00039],[0.077,0.0488,0.0006],null,{category:'bezel-honeycomb'});
  hc=0;
  for (const x of lower) b.addNode(`Bezel_Hex_Lower_${++hc}`,hex(mat.silverDark),[x,-0.019,D.bezelFrontZ-0.00039],[0.077,0.0488,0.0006],null,{category:'bezel-honeycomb'});
  b.addNode('Factory_DELL_EMC_Badge',plane('front',mat.frontLogoTex),[0,0,D.bezelFrontZ],[0.1366,0.0382,1],null,{category:'factory-branding',text:'DELL EMC',sourceLocked:true});
  cyl('Bezel_Lock_Cylinder',mat.graphite,[-0.184,0.021,D.bezelFrontZ-0.00035],[0.021,0.021,0.0007],{category:'bezel-lock'});
  box('Bezel_LCD',mat.screen,[0.105,0.032,D.bezelFrontZ-0.0002],[0.092,0.011,0.0004],null,{category:'bezel-lcd'});
  for (let i=0;i<3;i++) box(`Bezel_LCD_Button_${i+1}`,mat.silverDark,[0.073+i*0.009,0.032,D.bezelFrontZ-0.00002],[0.006,0.006,0.00004],null,{category:'bezel-lcd-button'});

  // Rack-ear apertures and front-control physical relief.
  for (const side of [-1,1]) for (const y of [-0.027,0.027]) {
    box(`Rack_Ear_Recess_${side<0?'Left':'Right'}_${y<0?'Lower':'Upper'}`,mat.vent,[side*0.238,y,D.bezelFrontZ-0.0001],[0.0045,0.009,0.0002],null,{category:'rack-ear-hole-recess'});
  }
  for (let i=0;i<4;i++) box(`Left_Status_LED_${i+1}`,i===2?mat.blue:mat.green,[-0.220,0.025-i*0.010,D.bezelFrontZ-0.00002],[0.0024,0.006,0.00004],null,{category:'front-status'});
  cyl('Front_Power_Button',mat.green,[0.220,0.031,D.bezelFrontZ-0.00002],[0.009,0.009,0.00004],{category:'front-control'});
  box('Front_VGA',mat.blue,[0.220,0.009,D.bezelFrontZ-0.00002],[0.013,0.012,0.00004],null,{category:'front-port',port:'VGA'});
  box('Front_USB2',mat.black,[0.220,-0.010,D.bezelFrontZ-0.00002],[0.006,0.012,0.00004],null,{category:'front-port',port:'USB2'});
  box('Front_iDRAC_Direct',mat.black,[0.220,-0.027,D.bezelFrontZ-0.00002],[0.005,0.009,0.00004],null,{category:'front-port',port:'Micro-AB'});

  // Rear PCIe/riser covers and dense stamped vent relief.
  const slotDefs=[
    ['Slot_1',0.165,0.028,0.080],['Slot_2',0.165,0.012,0.080],
    ['Slot_3',0.055,-0.002,0.062],['Slot_6',-0.015,-0.002,0.062],
    ['Slot_4',0.045,0.028,0.090],['Slot_5',0.045,0.012,0.090],
    ['Slot_7',-0.145,0.028,0.108],['Slot_8',-0.145,0.012,0.108],
  ];
  for (const [name,x,y,w] of slotDefs) {
    box(`PCIe_${name}_Filler`,mat.silverDark,[x,y,D.rearWallZ-0.0016],[w,0.013,0.003],null,{category:'pcie-filler'});
    const holes=Math.max(7,Math.round(w/0.007));
    for(let i=0;i<holes;i++) {
      const hx=x-w/2+0.004+(i*(w-0.008)/(holes-1));
      box(`PCIe_${name}_Vent_${String(i+1).padStart(2,'0')}`,mat.vent,[hx,y,D.rearWallZ-0.00315],[0.004,0.006,0.00035],null,{category:'pcie-vent'});
    }
  }
  box('BOSS_S2_Cartridge',mat.black,[0.105,0.021,D.rearWallZ-0.004],[0.019,0.034,0.008],null,{category:'BOSS-S2'});
  box('BOSS_S2_Release_Top',mat.orange,[0.105,0.034,D.rearWallZ-0.0082],[0.012,0.004,0.0004],null,{category:'BOSS-release'});
  box('BOSS_S2_Release_Bottom',mat.orange,[0.105,0.008,D.rearWallZ-0.0082],[0.012,0.004,0.0004],null,{category:'BOSS-release'});
  for (const x of [0.115,0.000,-0.095]) cyl(`Rear_Retention_${x}`,mat.blue,[x,0.021,D.rearWallZ-0.004],[0.009,0.009,0.005],{category:'rear-retention'});

  // Dual 2400 W AC PSUs with true projecting blocks, fan rotors and inlets.
  const psuXs=[0.169,-0.169];
  for(let p=0;p<2;p++) {
    const x=psuXs[p], id=p+1;
    const psuFaceZ=D.rearWallZ-0.006;
    box(`AC_PSU_${id}_Body`,mat.silverDark,[x,-0.024,(D.rearWallZ+psuFaceZ)/2],[0.082,0.037,D.rearWallZ-psuFaceZ],null,{category:'AC-PSU',watts:2400});
    const fanX=x+(p===0?0.020:-0.020);
    cyl(`AC_PSU_${id}_Fan_Rim`,mat.black,[fanX,-0.024,psuFaceZ-0.0008],[0.034,0.034,0.0016],{category:'PSU-fan'});
    cyl(`AC_PSU_${id}_Fan_Hub`,mat.silverDark,[fanX,-0.024,psuFaceZ-0.00165],[0.012,0.012,0.0003],{category:'PSU-fan-hub'});
    for(let blade=0;blade<8;blade++) box(`AC_PSU_${id}_Fan_Blade_${blade+1}`,mat.black,[fanX,-0.024,psuFaceZ-0.001675],[0.003,0.028,0.00025],qz(blade*Math.PI/4),{category:'PSU-fan-blade'});
    const inletX=x+(p===0?-0.020:0.020);
    box(`AC_PSU_${id}_IEC_C20`,mat.black,[inletX,-0.024,psuFaceZ-0.00165],[0.029,0.028,0.0003],null,{category:'AC-inlet',connector:'IEC-C20'});
    box(`AC_PSU_${id}_Orange_Release`,mat.orange,[x+(p===0?-0.038:0.038),-0.023,psuFaceZ-0.001675],[0.005,0.017,0.00035],null,{category:'PSU-release'});
    const handleX=x+(p===0?-0.034:0.034);
    box(`AC_PSU_${id}_Handle`,mat.black,[handleX,-0.024,(psuFaceZ+D.psuHandleZ)/2],[0.007,0.025,psuFaceZ-D.psuHandleZ],null,{category:'PSU-handle',outermostDepth:true});
  }

  // Rear management/network port geometry with the documented optional serial DB9 in Riser 3.
  const rearPort = (name,material,x,y,w,h,port) => box(name,material,[x,y,D.rearWallZ-0.0044],[w,h,0.008],null,{category:'rear-port',port});
  rearPort('NIC_1',mat.black,0.098,-0.031,0.018,0.014,'RJ45 NIC1');
  rearPort('NIC_2',mat.black,0.076,-0.031,0.018,0.014,'RJ45 NIC2');
  rearPort('OCP_3_Port_A',mat.black,0.033,-0.030,0.025,0.013,'OCP 3.0');
  rearPort('OCP_3_Port_B',mat.black,0.004,-0.030,0.025,0.013,'OCP 3.0');
  cyl('Rear_System_ID_Button',mat.blue,[-0.033,-0.030,D.rearWallZ-0.0085],[0.006,0.006,0.001],{category:'rear-control'});
  rearPort('iDRAC_Dedicated',mat.black,-0.058,-0.030,0.018,0.014,'iDRAC RJ45');
  rearPort('Rear_USB3',mat.blue,-0.082,-0.030,0.013,0.006,'USB 3.0');
  rearPort('Rear_VGA_DB15',mat.blue,-0.111,-0.030,0.021,0.014,'VGA DB15');
  rearPort('Rear_USB2',mat.black,-0.070,-0.006,0.013,0.006,'USB 2.0');
  rearPort('Optional_Serial_DB9_Riser3',mat.silverDark,0.017,0.029,0.022,0.012,'9-pin DTE serial COM in Riser 3');
  for(let pin=0;pin<9;pin++) {
    const col=pin<5?pin:pin-5;
    const row=pin<5?0:1;
    cyl(`Serial_DB9_Pin_${pin+1}`,mat.black,[0.009+col*0.0038,0.032-row*0.005,D.rearWallZ-0.0087],[0.0011,0.0011,0.0005],{category:'serial-pin'});
  }
  b.addEmptyNode('Rear_Drive_Module_ABSENT',{category:'configuration-lock',installed:false,reason:'user row-09 rear and Dell Figure 9 prove standard no-rear-drive wall'});

  // Six internal hot-swap fan assemblies; hidden by the closed cover but individually modeled.
  const fanXs=[-0.150,-0.090,-0.030,0.030,0.090,0.150];
  for(let i=0;i<6;i++) {
    box(`Internal_Fan_Module_${i+1}`,mat.black,[fanXs[i],0,0.235],[0.052,0.074,0.050],null,{category:'internal-hot-swap-fan',visibleWithCover:false});
    cyl(`Internal_Fan_Rotor_${i+1}`,mat.silverDark,[fanXs[i],0,0.260],[0.036,0.036,0.018],{category:'internal-fan-rotor',visibleWithCover:false});
  }

  // Top release latch geometry and explicitly non-mirrored side relief.
  box('Top_Cover_Latch',mat.screen,[0,D.height/2-0.0005,0.015],[0.022,0.001,0.055],null,{category:'top-cover-latch'});
  const rightSlots=[[-0.245,0.014,0.016],[-0.075,-0.002,0.011],[0.105,0.008,0.014],[0.255,-0.010,0.012]];
  for(let i=0;i<rightSlots.length;i++) {
    const [z,y,len]=rightSlots[i];
    box(`Right_Side_Rail_Slot_${i+1}`,mat.vent,[D.bodyWidth/2+0.00025,y,z],[0.0005,0.006,len],null,{category:'right-side-slot'});
  }
  const leftSlots=[[-0.270,-0.010,0.012],[-0.130,0.006,0.015],[0.035,-0.004,0.010],[0.205,0.013,0.018],[0.315,-0.013,0.010]];
  for(let i=0;i<leftSlots.length;i++) {
    const [z,y,len]=leftSlots[i];
    box(`Left_Side_Rail_Slot_${i+1}`,mat.vent,[-D.bodyWidth/2-0.00025,y,z],[0.0005,0.006,len],null,{category:'left-side-slot'});
  }

  const extras = {
    exactProductId: 'Dell PowerEdge R7525',
    configuration: '24x2.5-inch SFF; Dell EMC LCD security bezel installed; no rear drives; four riser groups/eight PCIe positions; optional 9-pin serial DB9 in Riser 3; dual 2400W AC PSU',
    dimensionsMillimeters: { overallWidth:482, bodyWidth:434, height:86.8, overallInstalledDepth:772.13 },
    coordinateConvention: '+X device right from front; +Y up; +Z front',
    bottomStatus: 'MULTI_REFERENCE_RECONSTRUCTION_FROM_OFFICIAL_AR',
    faceTextureEmbedding: 'All six primary face materials are OPAQUE; transparent canonical canvases are retained in ../views and body-only derived crops are embedded for left/right/top/bottom.',
    textureVariant: variant,
    sourceManifest: '../source/identity-manifest.md',
    featureInventory: '../source/feature-inventory.csv',
  };
  b.write(path.join(__dirname,outputName),extras);
}

buildVariant(path.join(ROOT,'qa','build','opaque-standard'),'Dell-R7525-2.5inch.glb','standard');
buildVariant(path.join(ROOT,'qa','build','opaque-web'),'Dell-R7525-2.5inch-web.glb','web');
