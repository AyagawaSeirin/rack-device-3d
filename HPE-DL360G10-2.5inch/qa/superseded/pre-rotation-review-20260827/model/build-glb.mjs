#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

const GL = {
  ARRAY_BUFFER: 34962,
  ELEMENT_ARRAY_BUFFER: 34963,
  FLOAT: 5126,
  UNSIGNED_SHORT: 5123,
};

class Builder {
  constructor(label) {
    this.label = label;
    this.json = {
      asset: {
        version: '2.0',
        generator: `rack-device-exact-exterior-builder/${label}`,
        copyright: 'New source-built exterior replica; source lineage in ../source/evidence.md',
        extras: {
          manufacturer: 'HPE',
          product: 'ProLiant DL360 Gen10',
          variant: 'standard 8SFF 2.5-inch, 6+2 carrier arrangement, dual 500W AC PSU',
          bodyDimensionsMm: [434.6, 42.9, 707.0],
          overallFrontWidthMm: 482.6,
          coordinateConvention: '+X device right from front; +Y up; +Z front',
          bottomEvidence: 'GENERIC_BOTTOM_FALLBACK',
        },
      },
      extensionsUsed: ['KHR_materials_unlit'],
      scene: 0,
      scenes: [{ name: 'HPE_DL360_Gen10_8SFF', nodes: [] }],
      nodes: [],
      meshes: [],
      materials: [],
      textures: [],
      images: [],
      samplers: [{
        magFilter: 9729,
        minFilter: 9987,
        wrapS: 33071,
        wrapT: 33071,
      }],
      accessors: [],
      bufferViews: [],
      buffers: [{ byteLength: 0 }],
    };
    this.parts = [];
    this.byteChunks = [];
    this.byteLength = 0;
    this.geometry = new Map();
    this.meshCache = new Map();
    this.materialByName = new Map();
  }

  appendBuffer(data, target) {
    const src = Buffer.isBuffer(data)
      ? data
      : Buffer.from(data.buffer, data.byteOffset, data.byteLength);
    const padBefore = (4 - (this.byteLength % 4)) % 4;
    if (padBefore) {
      this.byteChunks.push(Buffer.alloc(padBefore));
      this.byteLength += padBefore;
    }
    const byteOffset = this.byteLength;
    this.byteChunks.push(Buffer.from(src));
    this.byteLength += src.length;
    const view = { buffer: 0, byteOffset, byteLength: src.length };
    if (target) view.target = target;
    this.json.bufferViews.push(view);
    return this.json.bufferViews.length - 1;
  }

  addAccessor(array, componentType, type, target, min, max) {
    const bufferView = this.appendBuffer(array, target);
    const components = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 }[type];
    const accessor = {
      bufferView,
      byteOffset: 0,
      componentType,
      count: array.length / components,
      type,
    };
    if (min) accessor.min = min;
    if (max) accessor.max = max;
    this.json.accessors.push(accessor);
    return this.json.accessors.length - 1;
  }

  addGeometry(key, positions, normals, uvs, indices) {
    const min = [Infinity, Infinity, Infinity];
    const max = [-Infinity, -Infinity, -Infinity];
    for (let i = 0; i < positions.length; i += 3) {
      for (let c = 0; c < 3; c++) {
        min[c] = Math.min(min[c], positions[i + c]);
        max[c] = Math.max(max[c], positions[i + c]);
      }
    }
    const acc = {
      position: this.addAccessor(new Float32Array(positions), GL.FLOAT, 'VEC3', GL.ARRAY_BUFFER, min, max),
      normal: this.addAccessor(new Float32Array(normals), GL.FLOAT, 'VEC3', GL.ARRAY_BUFFER),
      uv: this.addAccessor(new Float32Array(uvs), GL.FLOAT, 'VEC2', GL.ARRAY_BUFFER),
      index: this.addAccessor(new Uint16Array(indices), GL.UNSIGNED_SHORT, 'SCALAR', GL.ELEMENT_ARRAY_BUFFER),
    };
    this.geometry.set(key, acc);
    return acc;
  }

  addImage(filePath, name) {
    const bytes = fs.readFileSync(filePath);
    const bufferView = this.appendBuffer(bytes);
    this.json.images.push({ name, bufferView, mimeType: 'image/png' });
    const image = this.json.images.length - 1;
    this.json.textures.push({ name, sampler: 0, source: image });
    return this.json.textures.length - 1;
  }

  addMaterial(name, color, texture = null, options = {}) {
    const mat = {
      name,
      pbrMetallicRoughness: {
        baseColorFactor: color,
        metallicFactor: 0,
        roughnessFactor: 0.82,
      },
      doubleSided: options.doubleSided ?? false,
      alphaMode: options.alphaMode ?? 'OPAQUE',
      extensions: { KHR_materials_unlit: {} },
    };
    if (texture !== null) {
      mat.pbrMetallicRoughness.baseColorTexture = { index: texture, texCoord: 0 };
    }
    if (mat.alphaMode === 'MASK') mat.alphaCutoff = options.alphaCutoff ?? 0.45;
    this.json.materials.push(mat);
    const idx = this.json.materials.length - 1;
    this.materialByName.set(name, idx);
    return idx;
  }

  meshFor(geometryKey, material, name) {
    const cacheKey = `${geometryKey}/${material}`;
    if (this.meshCache.has(cacheKey)) return this.meshCache.get(cacheKey);
    const g = this.geometry.get(geometryKey);
    const mesh = {
      name: `${name}_Mesh`,
      primitives: [{
        attributes: { POSITION: g.position, NORMAL: g.normal, TEXCOORD_0: g.uv },
        indices: g.index,
        material,
        mode: 4,
      }],
    };
    this.json.meshes.push(mesh);
    const idx = this.json.meshes.length - 1;
    this.meshCache.set(cacheKey, idx);
    return idx;
  }

  addNode(name, props = {}, parent = null, partType = null) {
    const node = { name, ...props };
    this.json.nodes.push(node);
    const idx = this.json.nodes.length - 1;
    if (parent === null) this.json.scenes[0].nodes.push(idx);
    else {
      const p = this.json.nodes[parent];
      if (!p.children) p.children = [];
      p.children.push(idx);
    }
    if (partType) this.parts.push({ node: name, type: partType });
    return idx;
  }

  addGroup(name, parent = null, partType = null) {
    return this.addNode(name, {}, parent, partType);
  }

  addBox(name, center, size, material, parent, partType = null, rotation = null) {
    const props = {
      mesh: this.meshFor('cube', material, name),
      translation: center,
      scale: size,
    };
    if (rotation) props.rotation = rotation;
    return this.addNode(name, props, parent, partType);
  }

  addCylinder(name, center, radius, depth, material, parent, partType = null, rotation = null, xyScale = [1, 1]) {
    const props = {
      mesh: this.meshFor('cylinder', material, name),
      translation: center,
      scale: [radius * xyScale[0], radius * xyScale[1], depth],
    };
    if (rotation) props.rotation = rotation;
    return this.addNode(name, props, parent, partType);
  }

  addPlane(name, geometryKey, center, scale, material, parent, partType = null) {
    return this.addNode(name, {
      mesh: this.meshFor(geometryKey, material, name),
      translation: center,
      scale,
    }, parent, partType);
  }

  finalize(outPath, manifestPath) {
    this.json.asset.extras.visibleParts = this.parts.length;
    this.json.buffers[0].byteLength = (this.byteLength + 3) & ~3;
    let bin = Buffer.concat(this.byteChunks);
    if (bin.length % 4) bin = Buffer.concat([bin, Buffer.alloc(4 - (bin.length % 4))]);
    let jsonBytes = Buffer.from(JSON.stringify(this.json), 'utf8');
    const jsonPad = (4 - (jsonBytes.length % 4)) % 4;
    if (jsonPad) jsonBytes = Buffer.concat([jsonBytes, Buffer.alloc(jsonPad, 0x20)]);

    const totalLength = 12 + 8 + jsonBytes.length + 8 + bin.length;
    const header = Buffer.alloc(12);
    header.writeUInt32LE(0x46546c67, 0);
    header.writeUInt32LE(2, 4);
    header.writeUInt32LE(totalLength, 8);
    const jsonHeader = Buffer.alloc(8);
    jsonHeader.writeUInt32LE(jsonBytes.length, 0);
    jsonHeader.writeUInt32LE(0x4e4f534a, 4);
    const binHeader = Buffer.alloc(8);
    binHeader.writeUInt32LE(bin.length, 0);
    binHeader.writeUInt32LE(0x004e4942, 4);
    fs.writeFileSync(outPath, Buffer.concat([header, jsonHeader, jsonBytes, binHeader, bin]));
    fs.writeFileSync(manifestPath, JSON.stringify({
      variant: this.label,
      output: path.basename(outPath),
      bytes: fs.statSync(outPath).size,
      nodes: this.json.nodes.length,
      meshes: this.json.meshes.length,
      primitives: this.json.meshes.reduce((n, m) => n + m.primitives.length, 0),
      materials: this.json.materials.length,
      textures: this.json.textures.length,
      images: this.json.images.length,
      visibleParts: this.parts,
    }, null, 2));
  }
}

function cubeGeometry() {
  const p = [];
  const n = [];
  const uv = [];
  const idx = [];
  const faces = [
    { verts: [[-0.5,-0.5, 0.5],[ 0.5,-0.5, 0.5],[ 0.5, 0.5, 0.5],[-0.5, 0.5, 0.5]], normal: [0,0,1] },
    { verts: [[ 0.5,-0.5,-0.5],[-0.5,-0.5,-0.5],[-0.5, 0.5,-0.5],[ 0.5, 0.5,-0.5]], normal: [0,0,-1] },
    { verts: [[ 0.5,-0.5, 0.5],[ 0.5,-0.5,-0.5],[ 0.5, 0.5,-0.5],[ 0.5, 0.5, 0.5]], normal: [1,0,0] },
    { verts: [[-0.5,-0.5,-0.5],[-0.5,-0.5, 0.5],[-0.5, 0.5, 0.5],[-0.5, 0.5,-0.5]], normal: [-1,0,0] },
    { verts: [[-0.5, 0.5, 0.5],[ 0.5, 0.5, 0.5],[ 0.5, 0.5,-0.5],[-0.5, 0.5,-0.5]], normal: [0,1,0] },
    { verts: [[-0.5,-0.5,-0.5],[ 0.5,-0.5,-0.5],[ 0.5,-0.5, 0.5],[-0.5,-0.5, 0.5]], normal: [0,-1,0] },
  ];
  for (const { verts, normal } of faces) {
    const base = p.length / 3;
    for (const v of verts) { p.push(...v); n.push(...normal); }
    uv.push(0,1, 1,1, 1,0, 0,0);
    idx.push(base,base+1,base+2, base,base+2,base+3);
  }
  return [p,n,uv,idx];
}

function planeGeometry(type) {
  let p, normal, reverse = false;
  if (type === 'front') {
    p = [-.5,-.5,0, .5,-.5,0, .5,.5,0, -.5,.5,0]; normal = [0,0,1];
  } else if (type === 'rear') {
    p = [.5,-.5,0, -.5,-.5,0, -.5,.5,0, .5,.5,0]; normal = [0,0,-1];
  } else if (type === 'left') {
    p = [0,-.5,.5, 0,-.5,-.5, 0,.5,-.5, 0,.5,.5]; normal = [-1,0,0]; reverse = true;
  } else if (type === 'right') {
    p = [0,-.5,-.5, 0,-.5,.5, 0,.5,.5, 0,.5,-.5]; normal = [1,0,0]; reverse = true;
  } else if (type === 'top') {
    p = [-.5,0,.5, .5,0,.5, .5,0,-.5, -.5,0,-.5]; normal = [0,1,0];
  } else {
    p = [-.5,0,-.5, .5,0,-.5, .5,0,.5, -.5,0,.5]; normal = [0,-1,0]; reverse = true;
    // This vertex order already produces an outward -Y front face. Reversing
    // it makes the underside back-facing in conforming viewers that honor
    // doubleSided:false.
    reverse = false;
  }
  const n = [...normal,...normal,...normal,...normal];
  const uv = [0,1, 1,1, 1,0, 0,0];
  const idx = reverse ? [0,2,1,0,3,2] : [0,1,2,0,2,3];
  return [p,n,uv,idx];
}

function cylinderGeometry(segments = 32) {
  const p = [], n = [], uv = [], idx = [];
  for (let i = 0; i <= segments; i++) {
    const a = i / segments * Math.PI * 2;
    const x = Math.cos(a), y = Math.sin(a);
    p.push(x,y,-.5, x,y,.5);
    n.push(x,y,0, x,y,0);
    uv.push(i/segments,1, i/segments,0);
  }
  for (let i = 0; i < segments; i++) {
    const k = i*2;
    idx.push(k,k+1,k+3, k,k+3,k+2);
  }
  const frontCenter = p.length/3;
  p.push(0,0,.5); n.push(0,0,1); uv.push(.5,.5);
  const backCenter = p.length/3;
  p.push(0,0,-.5); n.push(0,0,-1); uv.push(.5,.5);
  for (let i = 0; i < segments; i++) {
    const a = i*2+1, b = (i+1)*2+1;
    idx.push(frontCenter,a,b);
    const c = i*2, d = (i+1)*2;
    idx.push(backCenter,d,c);
  }
  return [p,n,uv,idx];
}

function rectHoleGeometry(w = 1, h = 1, depth = 1, radius = 0.2, segments = 40, holeY = 0) {
  const p = [], n = [], uv = [], idx = [];
  const rings = { frontOuter: [], frontInner: [], backOuter: [], backInner: [] };
  for (let i = 0; i < segments; i++) {
    const a = i / segments * Math.PI * 2;
    const c = Math.cos(a), s = Math.sin(a);
    const tx = Math.abs(c) < 1e-6 ? Infinity : (c > 0 ? (w/2)/c : (-w/2)/c);
    const ty = Math.abs(s) < 1e-6 ? Infinity : (s > 0 ? (h/2-holeY)/s : (-h/2-holeY)/s);
    const t = Math.min(tx, ty);
    const ox = c*t, oy=holeY+s*t, ix=c*radius, iy=holeY+s*radius;
    for (const [key,x,y,z,nz] of [
      ['frontOuter',ox,oy,depth/2,1],['frontInner',ix,iy,depth/2,1],
      ['backOuter',ox,oy,-depth/2,-1],['backInner',ix,iy,-depth/2,-1],
    ]) {
      rings[key].push(p.length/3); p.push(x,y,z); n.push(0,0,nz); uv.push(x/w+.5,.5-y/h);
    }
  }
  for (let i = 0; i < segments; i++) {
    const j=(i+1)%segments;
    const fo=rings.frontOuter, fi=rings.frontInner, bo=rings.backOuter, bi=rings.backInner;
    idx.push(fo[i],fo[j],fi[j], fo[i],fi[j],fi[i]);
    idx.push(bo[i],bi[j],bo[j], bo[i],bi[i],bi[j]);
    idx.push(fi[i],fi[j],bi[j], fi[i],bi[j],bi[i]);
    idx.push(fo[i],bo[j],fo[j], fo[i],bo[i],bo[j]);
  }
  return [p,n,uv,idx];
}

function qz(angle) { return [0,0,Math.sin(angle/2),Math.cos(angle/2)]; }
function qy(angle) { return [0,Math.sin(angle/2),0,Math.cos(angle/2)]; }
function qx(angle) { return [Math.sin(angle/2),0,0,Math.cos(angle/2)]; }

function buildVariant(label, textureDir, outFile) {
  const b = new Builder(label);
  b.addGeometry('cube', ...cubeGeometry());
  b.addGeometry('cylinder', ...cylinderGeometry());
  for (const type of ['front','rear','left','right','top','bottom']) b.addGeometry(`plane-${type}`, ...planeGeometry(type));
  b.addGeometry('ear-ring', ...rectHoleGeometry(24,42.9,6,4.8,48,10));

  const tex = {};
  for (const name of ['front-body','front-ear-left','front-ear-right','rear','left','right','top','bottom']) {
    tex[name] = b.addImage(path.join(textureDir, `${name}.png`), name);
  }

  const silver = b.addMaterial('Galvanized_Silver', [0.69,0.70,0.69,1]);
  const lightSilver = b.addMaterial('PSU_Silver', [0.79,0.79,0.77,1]);
  const black = b.addMaterial('HPE_Black_Plastic', [0.035,0.04,0.04,1]);
  const dark = b.addMaterial('Dark_Recess', [0.012,0.014,0.014,1]);
  const gray = b.addMaterial('Handle_Gray', [0.14,0.15,0.15,1]);
  const red = b.addMaterial('HPE_Latch_Red', [0.34,0.075,0.07,1]);
  const green = b.addMaterial('HPE_Status_Green', [0.06,0.72,0.29,1]);
  const blue = b.addMaterial('Connector_Blue', [0.03,0.30,0.68,1]);
  const teal = b.addMaterial('Serial_Teal', [0.05,0.34,0.31,1]);
  const frontBodyMat = b.addMaterial('Front_Body_Texture_sRGB', [1,1,1,1], tex['front-body']);
  const earLeftMat = b.addMaterial('Front_Ear_Left_Texture_MASK', [1,1,1,1], tex['front-ear-left'], {alphaMode:'MASK'});
  const earRightMat = b.addMaterial('Front_Ear_Right_Texture_MASK', [1,1,1,1], tex['front-ear-right'], {alphaMode:'MASK'});
  const rearMat = b.addMaterial('Rear_Texture_sRGB', [1,1,1,1], tex.rear);
  const leftMat = b.addMaterial('Left_Texture_sRGB', [1,1,1,1], tex.left);
  const rightMat = b.addMaterial('Right_Texture_sRGB', [1,1,1,1], tex.right);
  const topMat = b.addMaterial('Top_Texture_sRGB', [1,1,1,1], tex.top);
  const bottomMat = b.addMaterial('Bottom_Texture_sRGB_GENERIC_FALLBACK', [1,1,1,1], tex.bottom);

  const assembly = b.addGroup('HPE_ProLiant_DL360_Gen10_8SFF_Assembly', null, 'complete-appliance');
  const chassis = b.addGroup('Chassis', assembly, 'closed-chassis');
  b.addBox('ChassisBody_Closed', [0,0,0], [432.0,41.0,690.0], silver, chassis, 'closed-body');

  const faces = b.addGroup('Canonical_Face_Surfaces', assembly, 'six-face-texture-set');
  b.addPlane('FrontBody_TexturePlane', 'plane-front', [0,0,348.14], [434.6,42.9,1], frontBodyMat, faces, 'opaque-front-surface');
  b.addPlane('Rear_TexturePlane', 'plane-rear', [0,0,-348.14], [434.6,42.9,1], rearMat, faces, 'opaque-rear-surface');
  b.addPlane('Left_TexturePlane', 'plane-left', [-217.32,0,0], [1,42.9,707], leftMat, faces, 'opaque-left-surface');
  b.addPlane('Right_TexturePlane', 'plane-right', [217.32,0,0], [1,42.9,707], rightMat, faces, 'opaque-right-surface');
  b.addPlane('Top_TexturePlane', 'plane-top', [0,21.31,0], [434.6,1,707], topMat, faces, 'opaque-top-surface');
  b.addPlane('Bottom_TexturePlane_GENERIC_BOTTOM_FALLBACK', 'plane-bottom', [0,-21.31,0], [434.6,1,707], bottomMat, faces, 'opaque-bottom-surface');

  const ears = b.addGroup('Front_Rack_Ears', assembly, 'separate-rack-ear-assemblies');
  for (const [side,x,mat] of [['Left',-229.3,earLeftMat],['Right',229.3,earRightMat]]) {
    const g = b.addGroup(`RackEar_${side}`, ears, 'front-rack-ear');
    b.addNode(`RackEar_${side}_Plate_With_Circular_ThroughHole`, {
      mesh: b.meshFor('ear-ring', silver, `RackEar_${side}`),
      translation: [x,0,350.35],
    }, g, 'geometric-through-hole-ear');
    b.addBox(`RackEar_${side}_LowerPlate`, [x,-10.725,350.35], [24,21.45,6], silver, g, 'ear-lower-plate');
    b.addPlane(`RackEar_${side}_TexturePlane`, 'plane-front', [x,0,353.42], [24,42.9,1], mat, g, 'ear-only-alpha-mask');
    b.addBox(`RackEar_${side}_InnerBlackTrim`, [x + (side==='Left'?10.5:-10.5),0,352.0], [3,39,2.5], black, g, 'ear-trim');
  }
  b.addCylinder('RackEar_Left_Lower_StatusDisc', [-229.3,-7.0,353.20], 4.2, .55, gray, ears, 'non-through-status-disc');
  b.addBox('RackEar_Right_ProLiant_Badge_Relief', [229.3,-9.0,353.22], [17,18,.6], black, ears, 'HPE-ProLiant-badge-relief');

  const front = b.addGroup('Front_Visible_Assemblies', assembly, 'front-relief-assemblies');
  b.addBox('Front_DriveBay_ID_PullTab', [-204,0,350.9], [18,34,4.7], black, front, 'drive-support-label-pulltab');
  const carrierCenters = [];
  for (const x of [-174,-102,-30]) for (const y of [10.1,-10.1]) carrierCenters.push([x,y]);
  carrierCenters.push([47,-10.1],[118,-10.1]);
  carrierCenters.forEach(([x,y],i) => {
    const id = String(i+1).padStart(2,'0');
    const cg = b.addGroup(`SFF_Carrier_${id}`, front, 'independent-SFF-carrier');
    b.addBox(`SFF_Carrier_${id}_Recess`, [x,y,347.00], [68,18.2,2.0], dark, cg, 'carrier-recess-behind-source-texture');
    b.addBox(`SFF_Carrier_${id}_TopRail`, [x,y+8.4,351.35], [66,1.15,2.2], black, cg, 'carrier-frame');
    b.addBox(`SFF_Carrier_${id}_BottomRail`, [x,y-8.4,351.35], [66,1.15,2.2], black, cg, 'carrier-frame');
    b.addBox(`SFF_Carrier_${id}_LeftRail`, [x-33,y,351.35], [1.2,16.8,2.2], black, cg, 'carrier-frame');
    b.addBox(`SFF_Carrier_${id}_RightRail`, [x+33,y,351.35], [1.2,16.8,2.2], black, cg, 'carrier-frame');
    b.addBox(`SFF_Carrier_${id}_PullHandle`, [x-7,y-3.0,352.32], [39,2.6,1.55], gray, cg, 'independent-carrier-handle');
    b.addCylinder(`SFF_Carrier_${id}_HandleHub`, [x+14,y,352.36], 4.7, 1.65, gray, cg, 'handle-hub');
    b.addBox(`SFF_Carrier_${id}_ReleaseLatch`, [x+28,y,352.48], [6.3,11.5,1.9], red, cg, 'carrier-release-latch');
  });
  const umb = b.addGroup('Universal_Media_Bay', front, 'standard-8SFF-UMB');
  b.addBox('UniversalMediaBay_Upper_OpticalDisplay_Blank', [82.5,10.0,350.35], [137,17.6,4.2], black, umb, 'upper-UMB-blank');
  b.addBox('UniversalMediaBay_Upper_Blank_Lip', [82.5,1.4,352.25], [136,1.1,1.8], gray, umb, 'UMB-seam');
  const controls = b.addGroup('Front_Control_Area', front, 'front-control-area');
  b.addBox('FrontControl_Backplate', [172,0,350.45], [22,36,4.1], black, controls, 'control-backplate');
  b.addBox('Front_USB3_Port', [176,-9,352.65], [4.2,10,1.2], blue, controls, 'USB3-port');
  b.addBox('Front_iLO_Service_Port', [168,-9,352.65], [4.2,10,1.2], dark, controls, 'iLO-service-port');
  for (let i=0;i<4;i++) b.addCylinder(`Front_Status_LED_${i+1}`, [174,12-i*5,352.75], 1.45,.9,i===3?blue:green,controls,'front-status-LED');

  const rear = b.addGroup('Rear_Visible_Assemblies', assembly, 'rear-relief-assemblies');
  const blankDefs = [
    ['PCIe_Blank_Slot1',157,11,92,17],
    ['PCIe_Blank_Slot2',69,11,73,17],
    ['PCIe_Blank_Slot3',2,11,53,17],
  ];
  for (const [name,x,y,w,h] of blankDefs) {
    const g=b.addGroup(name,rear,'independent-PCIe-blank');
    b.addBox(`${name}_Plate`,[x,y,-350.10],[w,h,3.8],lightSilver,g,'blanking-plate');
    for(let k=0;k<6;k++) b.addBox(`${name}_Vent_${k+1}`,[x-w/2+12+k*(w-24)/5,y,-352.15],[3.6,h-6,.7],dark,g,'blank-vent-relief');
  }
  b.addBox('FlexibleLOM_Blank_Plate',[170,-10.3,-350.35],[84,16.5,4.1],lightSilver,rear,'FlexibleLOM-blank');
  for(let k=0;k<8;k++) b.addBox(`FlexibleLOM_Blank_Vent_${k+1}`,[140+k*8.2,-10.3,-352.45],[3.8,9,.7],dark,rear,'FlexibleLOM-vent-relief');

  const ports = b.addGroup('Rear_IO_Ports', rear, 'rear-port-group');
  b.addBox('Rear_USB3_Port_1',[116,-11,-352.15],[7.0,6.0,1.8],blue,ports,'USB3-port');
  b.addBox('Rear_USB3_Port_2',[106,-11,-352.15],[7.0,6.0,1.8],blue,ports,'USB3-port');
  b.addBox('Rear_Serial_DB9',[83,-10.5,-352.30],[20,9.8,2.0],teal,ports,'serial-DB9');
  b.addBox('Rear_iLO_Management_RJ45',[56,-10.5,-352.35],[13.5,12.5,2.0],dark,ports,'dedicated-iLO-management-port');
  for(let i=0;i<4;i++) {
    b.addBox(`Embedded_1GbE_RJ45_${i+1}`,[31-i*16,-10.5,-352.35],[13.5,12.5,2.0],dark,ports,'embedded-1GbE-RJ45');
    b.addCylinder(`Embedded_1GbE_LED_${i+1}`,[31-i*16,-2.4,-352.55],1.1,.55,green,ports,'NIC-status-LED');
  }
  b.addBox('Rear_VGA_Port',[-48,-10.5,-352.30],[22,11,2.0],blue,ports,'VGA-port');

  const psus = b.addGroup('Dual_AC_Power_Supplies', rear, 'dual-500W-AC-PSU');
  for(let i=0;i<2;i++) {
    const x=-119-i*49;
    const id=i+1;
    const pg=b.addGroup(`PSU_${id}_500W_AC`,psus,'independent-500W-AC-PSU');
    b.addBox(`PSU_${id}_ModuleBody`,[x,0,-350.0],[46,39,6.6],lightSilver,pg,'PSU-module');
    b.addCylinder(`PSU_${id}_Fan`,[x-7,3,-353.05],12.4,.8,dark,pg,'visible-PSU-fan');
    b.addCylinder(`PSU_${id}_FanHub`,[x-7,3,-353.42],3.2,.12,gray,pg,'PSU-fan-hub');
    for(let k=0;k<7;k++) {
      const a=k*Math.PI*2/7;
      b.addBox(`PSU_${id}_FanBlade_${k+1}`,[x-7+Math.cos(a)*5.3,3+Math.sin(a)*5.3,-353.40],[10.5,1.7,.14],gray,pg,'PSU-fan-blade',qz(a+0.5));
    }
    b.addBox(`PSU_${id}_IEC_C14_Inlet`,[x+13,-2,-353.12],[13,20,.8],black,pg,'AC-IEC-C14-inlet');
    b.addBox(`PSU_${id}_ReleaseHandle`,[x+12,14,-353.38],[15,3.0,.18],red,pg,'PSU-release-handle');
    b.addCylinder(`PSU_${id}_StatusLED`,[x+13,16.8,-353.45],1.4,.1,green,pg,'PSU-status-LED');
  }

  const top = b.addGroup('Top_Visible_Geometry', assembly, 'top-cover-relief');
  b.addBox('Top_Fixed_Front_Panel_Seam',[0,21.36,250],[434,0.10,1.0],gray,top,'fixed-front-cover-seam');
  b.addBox('Top_Access_Panel_Release_Latch',[0,21.40,82],[12,0.15,45],black,top,'top-release-latch');
  const ventBanks=[
    ['TopVent_RearLeft',-65,-270,10,4,7,7],
    ['TopVent_RearRight',117,-272,8,4,7,7],
    ['TopVent_MidLeft',-118,82,7,5,6,6],
    ['TopVent_FrontLeft',-155,278,8,3,5,5],
  ];
  for(const [name,cx,cz,cols,rows,cw,cd] of ventBanks){
    const vg=b.addGroup(name,top,'top-vent-bank');
    for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
      const x=cx+(c-(cols-1)/2)*(cw+2.0);
      const z=cz+(r-(rows-1)/2)*(cd+2.0);
      b.addBox(`${name}_Cell_${r+1}_${c+1}`,[x,21.39,z],[cw,0.13,cd],dark,vg,'closed-vent-recess');
    }
  }
  b.addBox('Top_Service_Label_Left_Relief',[-128,21.39,295],[90,.13,38],black,top,'factory-service-label-relief');
  b.addBox('Top_Service_Label_Right_Relief',[130,21.39,295],[85,.13,38],black,top,'factory-service-label-relief');
  for(let i=0;i<6;i++) b.addCylinder(`Top_Front_Rivet_${i+1}`,[-120+i*48,21.39,250],1.3,.10,lightSilver,top,'top-rivet',qx(Math.PI/2));

  const sideRelief=b.addGroup('Side_Rail_Attachment_Relief',assembly,'independent-left-right-side-relief');
  const sideSets={
    Left:[[-185,8],[-58,-6],[114,-4],[268,7]],
    Right:[[-255,6],[-122,-7],[42,-2],[255,5]],
  };
  for(const [side,items] of Object.entries(sideSets)){
    const x=side==='Left'?-217.38:217.38;
    const rot=qy(Math.PI/2);
    items.forEach(([z,y],i)=>{
      b.addCylinder(`${side}_RailStud_${i+1}`,[x,y,z],2.4,.20,lightSilver,sideRelief,`${side.toLowerCase()}-rail-stud`,rot,[1,.72]);
      b.addBox(`${side}_RailSlot_${i+1}`,[x,y-6,z+18],[.20,4.2,12],dark,sideRelief,`${side.toLowerCase()}-rail-slot`);
    });
  }

  const manifest = path.join(ROOT,'qa','manifests',`${path.basename(outFile,'.glb')}-parts.json`);
  b.finalize(outFile,manifest);
}

const standardTextures=path.join(ROOT,'work','geometry','textures-standard');
const webTextures=path.join(ROOT,'work','geometry','textures-web');
buildVariant('standard',standardTextures,path.join(HERE,'HPE-DL360G10-2.5inch.glb'));
buildVariant('web',webTextures,path.join(HERE,'HPE-DL360G10-2.5inch-web.glb'));

console.log('Built standard and web GLBs.');
