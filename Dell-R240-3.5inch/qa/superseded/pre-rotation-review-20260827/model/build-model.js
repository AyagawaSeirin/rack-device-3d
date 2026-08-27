'use strict';

// Self-contained GLB writer for the exact installed Dell PowerEdge R240 4LFF
// exterior. Coordinates are metres: +X device-right from the front, +Y up,
// +Z front. This is an independent exterior reconstruction, not Dell CAD.

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const MM = 0.001;
const D = {
  overallWidth: 482.0 * MM,
  bodyWidth: 434.0 * MM,
  height: 42.8 * MM,
  bodyDepth: 534.496 * MM,
  bodyFrontZ: 267.248 * MM,
  bodyRearZ: -267.248 * MM,
  frontMostZ: 289.248 * MM,
  rearMostZ: -284.348 * MM,
  overallDepth: 573.596 * MM,
};

function align4(value) { return (value + 3) & ~3; }

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
      name: 'LinearClamp', magFilter: 9729, minFilter: 9987,
      wrapS: 33071, wrapT: 33071,
    }];
    this.generator = generator;
    this.meshCache = new Map();
    this.rootChildren = [];
  }

  addBytes(data, target) {
    const pad = align4(this.byteLength) - this.byteLength;
    if (pad) { this.parts.push(Buffer.alloc(pad)); this.byteLength += pad; }
    const bytes = Buffer.isBuffer(data)
      ? data : Buffer.from(data.buffer, data.byteOffset, data.byteLength);
    const view = { buffer: 0, byteOffset: this.byteLength, byteLength: bytes.length };
    if (target) view.target = target;
    const index = this.bufferViews.length;
    this.bufferViews.push(view);
    this.parts.push(bytes);
    this.byteLength += bytes.length;
    return index;
  }

  addAccessor(array, type, componentType, target, min, max) {
    const widths = { SCALAR: 1, VEC2: 2, VEC3: 3 };
    const accessor = {
      bufferView: this.addBytes(array, target), byteOffset: 0, componentType,
      count: array.length / widths[type], type,
    };
    if (min) accessor.min = min;
    if (max) accessor.max = max;
    this.accessors.push(accessor);
    return this.accessors.length - 1;
  }

  addMaterial(name, color, options = {}) {
    const material = {
      name,
      pbrMetallicRoughness: {
        baseColorFactor: color,
        metallicFactor: options.metallic ?? 0,
        roughnessFactor: options.roughness ?? 0.72,
      },
      alphaMode: 'OPAQUE',
      doubleSided: false,
    };
    this.materials.push(material);
    return this.materials.length - 1;
  }

  addTextureMaterial(name, imagePath) {
    const imageBytes = fs.readFileSync(imagePath);
    const source = this.images.length;
    this.images.push({
      name: `${name}_Image`,
      bufferView: this.addBytes(imageBytes),
      mimeType: 'image/png',
    });
    const texture = this.textures.length;
    this.textures.push({ name: `${name}_Texture`, sampler: 0, source });
    this.materials.push({
      name,
      pbrMetallicRoughness: {
        baseColorFactor: [1, 1, 1, 1],
        baseColorTexture: { index: texture, texCoord: 0 },
        metallicFactor: 0,
        roughnessFactor: 1,
      },
      alphaMode: 'OPAQUE',
      doubleSided: false,
      extensions: { KHR_materials_unlit: {} },
    });
    return this.materials.length - 1;
  }

  addGeometry(name, geometry, material) {
    const positions = new Float32Array(geometry.positions);
    const normals = new Float32Array(geometry.normals);
    const uvs = new Float32Array(geometry.uvs);
    const indices = new Uint16Array(geometry.indices);
    const min = [Infinity, Infinity, Infinity];
    const max = [-Infinity, -Infinity, -Infinity];
    for (let i = 0; i < positions.length; i += 3) {
      for (let axis = 0; axis < 3; axis++) {
        min[axis] = Math.min(min[axis], positions[i + axis]);
        max[axis] = Math.max(max[axis], positions[i + axis]);
      }
    }
    const pos = this.addAccessor(positions, 'VEC3', 5126, 34962, min, max);
    const nor = this.addAccessor(normals, 'VEC3', 5126, 34962);
    const uv = this.addAccessor(uvs, 'VEC2', 5126, 34962);
    const ind = this.addAccessor(indices, 'SCALAR', 5123, 34963, [0], [Math.max(...indices)]);
    this.meshes.push({
      name,
      primitives: [{
        attributes: { POSITION: pos, NORMAL: nor, TEXCOORD_0: uv },
        indices: ind, material, mode: 4,
      }],
    });
    return this.meshes.length - 1;
  }

  cachedGeometry(key, makeGeometry, material) {
    const cacheKey = `${key}:${material}`;
    if (!this.meshCache.has(cacheKey)) {
      this.meshCache.set(cacheKey, this.addGeometry(cacheKey, makeGeometry(), material));
    }
    return this.meshCache.get(cacheKey);
  }

  addNode(name, mesh, translation, scale, extras = {}) {
    this.nodes.push({ name, mesh, translation, scale, extras });
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

  write(outputPath, extras) {
    const binPad = align4(this.byteLength) - this.byteLength;
    if (binPad) { this.parts.push(Buffer.alloc(binPad)); this.byteLength += binPad; }
    const rootIndex = this.nodes.length;
    this.nodes.push({
      name: 'Dell_PowerEdge_R240_4LFF_Installed_Assembly',
      children: this.rootChildren,
      extras: {
        manufacturer: 'Dell Technologies',
        product: 'Dell EMC PowerEdge R240',
        regulatoryModel: 'E57S / E57S001',
        physicalVariant: '1U; 4 x 3.5-inch hot-swap LFF; bezel absent; one fixed cabled AC PSU installed',
      },
    });
    const document = {
      asset: {
        version: '2.0', generator: this.generator,
        copyright: 'Independent exact-appearance reconstruction; factual Dell and PowerEdge markings retained.',
        extras,
      },
      extensionsUsed: ['KHR_materials_unlit'],
      scene: 0,
      scenes: [{ name: 'Installed_R240_4LFF', nodes: [rootIndex] }],
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
    let json = Buffer.from(JSON.stringify(document));
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
    fs.writeFileSync(outputPath, Buffer.concat([header, jsonHeader, json, binHeader, bin]));
  }
}

function cubeGeometry() {
  const positions = [], normals = [], uvs = [], indices = [];
  const faces = [
    [[-0.5,-0.5, 0.5],[ 0.5,-0.5, 0.5],[ 0.5, 0.5, 0.5],[-0.5, 0.5, 0.5],[0,0,1]],
    [[ 0.5,-0.5,-0.5],[-0.5,-0.5,-0.5],[-0.5, 0.5,-0.5],[ 0.5, 0.5,-0.5],[0,0,-1]],
    [[ 0.5,-0.5, 0.5],[ 0.5,-0.5,-0.5],[ 0.5, 0.5,-0.5],[ 0.5, 0.5, 0.5],[1,0,0]],
    [[-0.5,-0.5,-0.5],[-0.5,-0.5, 0.5],[-0.5, 0.5, 0.5],[-0.5, 0.5,-0.5],[-1,0,0]],
    [[-0.5, 0.5, 0.5],[ 0.5, 0.5, 0.5],[ 0.5, 0.5,-0.5],[-0.5, 0.5,-0.5],[0,1,0]],
    [[-0.5,-0.5,-0.5],[ 0.5,-0.5,-0.5],[ 0.5,-0.5, 0.5],[-0.5,-0.5, 0.5],[0,-1,0]],
  ];
  for (const face of faces) {
    const base = positions.length / 3;
    for (let i = 0; i < 4; i++) {
      positions.push(...face[i]); normals.push(...face[4]);
      uvs.push(i === 1 || i === 2 ? 1 : 0, i >= 2 ? 0 : 1);
    }
    indices.push(base, base + 1, base + 2, base, base + 2, base + 3);
  }
  return { positions, normals, uvs, indices };
}

function cylinderGeometry(segments = 28) {
  const positions = [], normals = [], uvs = [], indices = [];
  for (let i = 0; i <= segments; i++) {
    const angle = (i / segments) * Math.PI * 2;
    const x = Math.cos(angle) * 0.5;
    const y = Math.sin(angle) * 0.5;
    positions.push(x, y, -0.5, x, y, 0.5);
    normals.push(x * 2, y * 2, 0, x * 2, y * 2, 0);
    uvs.push(i / segments, 1, i / segments, 0);
  }
  for (let i = 0; i < segments; i++) {
    const base = i * 2;
    indices.push(base, base + 1, base + 3, base, base + 3, base + 2);
  }
  const front = positions.length / 3;
  positions.push(0, 0, 0.5); normals.push(0, 0, 1); uvs.push(0.5, 0.5);
  const rear = positions.length / 3;
  positions.push(0, 0, -0.5); normals.push(0, 0, -1); uvs.push(0.5, 0.5);
  for (let i = 0; i < segments; i++) {
    const a = i * 2 + 1;
    const b = ((i + 1) % segments) * 2 + 1;
    indices.push(front, a, b);
    const c = i * 2;
    const d = ((i + 1) % segments) * 2;
    indices.push(rear, d, c);
  }
  return { positions, normals, uvs, indices };
}

function planeGeometry(face) {
  const specs = {
    front: [[-0.5,-0.5,0],[0.5,-0.5,0],[0.5,0.5,0],[-0.5,0.5,0],[0,0,1]],
    rear: [[0.5,-0.5,0],[-0.5,-0.5,0],[-0.5,0.5,0],[0.5,0.5,0],[0,0,-1]],
    right: [[0,-0.5,0.5],[0,-0.5,-0.5],[0,0.5,-0.5],[0,0.5,0.5],[1,0,0]],
    left: [[0,-0.5,-0.5],[0,-0.5,0.5],[0,0.5,0.5],[0,0.5,-0.5],[-1,0,0]],
    top: [[-0.5,0,0.5],[0.5,0,0.5],[0.5,0,-0.5],[-0.5,0,-0.5],[0,1,0]],
    bottom: [[0.5,0,0.5],[-0.5,0,0.5],[-0.5,0,-0.5],[0.5,0,-0.5],[0,-1,0]],
  };
  const spec = specs[face];
  return {
    positions: spec.slice(0, 4).flat(),
    normals: [...spec[4], ...spec[4], ...spec[4], ...spec[4]],
    uvs: [0,1, 1,1, 1,0, 0,0],
    indices: [0,1,2, 0,2,3],
  };
}

function buildVariant(textureDir, outputName, variant) {
  const b = new GltfBuilder(`Codex Dell R240 exact-appearance builder (${variant})`);
  const mat = {};
  mat.silver = b.addMaterial('Galvanized_Steel', [0.59,0.61,0.62,1], { metallic:0.34, roughness:0.65 });
  mat.silverDark = b.addMaterial('Stamped_Steel_Shadow', [0.31,0.33,0.34,1], { metallic:0.28, roughness:0.72 });
  mat.graphite = b.addMaterial('Dell_Graphite', [0.075,0.083,0.088,1], { metallic:0.05, roughness:0.68 });
  mat.black = b.addMaterial('Port_and_Vent_Black', [0.008,0.011,0.013,1], { metallic:0.01, roughness:0.88 });
  mat.orange = b.addMaterial('Dell_Carrier_Release_Orange', [0.96,0.24,0.018,1], { metallic:0, roughness:0.48 });
  mat.blue = b.addMaterial('Dell_Service_Blue', [0.01,0.25,0.74,1], { metallic:0.02, roughness:0.48 });
  mat.green = b.addMaterial('PSU_BIST_Green', [0.02,0.69,0.12,1], { metallic:0, roughness:0.38 });
  mat.frontTex = b.addTextureMaterial('Face_Front_SourceLocked', path.join(textureDir, 'front.png'));
  mat.rearTex = b.addTextureMaterial('Face_Rear_SourceLocked', path.join(textureDir, 'rear.png'));
  mat.leftTex = b.addTextureMaterial('Face_Left_SourceLocked', path.join(textureDir, 'left.png'));
  mat.rightTex = b.addTextureMaterial('Face_Right_SourceLocked', path.join(textureDir, 'right.png'));
  mat.topTex = b.addTextureMaterial('Face_Top_SourceLocked', path.join(textureDir, 'top.png'));
  mat.bottomTex = b.addTextureMaterial('Face_Bottom_ConservativeFallback', path.join(textureDir, 'bottom.png'));

  const cube = material => b.cachedGeometry('UnitCube', cubeGeometry, material);
  const cylinder = material => b.cachedGeometry('UnitCylinder28', () => cylinderGeometry(28), material);
  const plane = (face, material) => b.cachedGeometry(`UnitPlane_${face}`, () => planeGeometry(face), material);
  const box = (name, material, position, scale, extras = {}) =>
    b.addNode(name, cube(material), position, scale, extras);
  const cyl = (name, material, position, scale, extras = {}) =>
    b.addNode(name, cylinder(material), position, scale, extras);

  // Closed enclosure, separate cover/deck, and all six independent source-locked faces.
  box('Closed_Chassis_Body', mat.silver, [0,0,0], [D.bodyWidth,0.040,D.bodyDepth], { category:'closed-shell' });
  box('Top_Cover_Stamped_Panel', mat.silver, [0,0.0209,-0.006], [0.428,0.0010,0.498], { category:'top-cover' });
  box('Bottom_Deck_Panel', mat.silver, [0,-0.0209,0], [D.bodyWidth,0.0010,D.bodyDepth], { category:'bottom-deck', bottomMode:'conservative-fallback' });
  b.addNode('Texture_Front', plane('front',mat.frontTex), [0,0,D.frontMostZ], [D.overallWidth,D.height,1], { face:'front', sourceLocked:true });
  b.addNode('Texture_Rear', plane('rear',mat.rearTex), [0,0,D.rearMostZ], [D.bodyWidth,D.height,1], { face:'rear', sourceLocked:true });
  b.addNode('Texture_Right', plane('right',mat.rightTex), [D.bodyWidth/2+0.00008,0,0], [1,D.height,D.bodyDepth], { face:'right', sourceLocked:true, independentlyGenerated:true });
  b.addNode('Texture_Left', plane('left',mat.leftTex), [-D.bodyWidth/2-0.00008,0,0], [1,D.height,D.bodyDepth], { face:'left', sourceLocked:true, independentlyGenerated:true });
  b.addNode('Texture_Top', plane('top',mat.topTex), [0,D.height/2,0], [D.bodyWidth,1,D.bodyDepth], { face:'top', sourceLocked:true });
  b.addNode('Texture_Bottom', plane('bottom',mat.bottomTex), [0,-D.height/2,0], [D.bodyWidth,1,D.bodyDepth], { face:'bottom', sourceLocked:true, productionMode:'GENERIC_BOTTOM_FALLBACK' });

  // Front rack ears supply the 482 mm verified overall width.
  b.addNode('Front_Left_Rack_Ear', plane('front',mat.graphite), [-0.229,0,0.2889], [0.024,D.height,1], { category:'rack-ear', frontFacingOnly:true });
  b.addNode('Front_Right_Control_Ear', plane('front',mat.graphite), [0.229,0,0.2889], [0.024,D.height,1], { category:'rack-ear-control', frontFacingOnly:true });

  // Four physically separate 3.5-inch hot-swap carrier assemblies.
  const driveXs = [-0.1455,-0.0485,0.0485,0.1455];
  for (let index = 0; index < driveXs.length; index++) {
    const x = driveXs[index];
    const id = index + 1;
    box(`LFF_Carrier_${id}`, mat.graphite, [x,-0.003,0.2771], [0.093,0.0335,0.0200], { category:'3.5-inch-LFF-hot-swap-carrier', installed:true, bay:id });
    box(`LFF_Carrier_${id}_Lower_Handle`, mat.silverDark, [x+0.010,-0.0170,0.2880], [0.070,0.0024,0.0015], { category:'carrier-handle' });
    cyl(`LFF_Carrier_${id}_Release_Ring`, mat.orange, [x-0.044,0.0015,0.2880], [0.0090,0.0090,0.0015], { category:'carrier-release-ring' });
    for (let slot = 0; slot < 4; slot++) {
      box(`LFF_Carrier_${id}_Vent_Rib_${slot+1}`, mat.black, [x-0.006+slot*0.013,-0.001,0.2880], [0.0020,0.0175,0.0010], { category:'carrier-vent-relief' });
    }
  }

  // Front top ventilation and the service-tag pull tab are real relief, while
  // the exact fine pattern and DELL EMC / PowerEdge R240 text remain in texture.
  box('Front_Upper_Vent_Recess', mat.black, [0,0.0135,0.2869], [0.385,0.0120,0.0030], { category:'front-vent-recess' });
  box('Front_Pullout_Information_Tag', mat.graphite, [0.173,-0.0188,0.2880], [0.074,0.0032,0.0015], { category:'factory-information-tag', brandingRetainedInTexture:true });

  // Rear standard I/O: explicit connector relief in the exact fixed layout.
  const rearZ = -0.28245;
  box('Rear_Serial_DB9', mat.graphite, [0.183,0.010,rearZ], [0.039,0.013,0.0035], { category:'DB9-serial', installed:true });
  box('Rear_VGA', mat.blue, [0.180,-0.010,rearZ], [0.035,0.012,0.0035], { category:'VGA', installed:true });
  box('Rear_iDRAC_RJ45', mat.black, [0.126,-0.010,rearZ], [0.024,0.014,0.0035], { category:'iDRAC-RJ45', installed:true });
  box('Rear_LOM1_RJ45', mat.black, [0.092,0.006,rearZ], [0.024,0.016,0.0035], { category:'1GbE-RJ45', installed:true, port:1 });
  box('Rear_LOM2_RJ45', mat.black, [0.057,0.006,rearZ], [0.024,0.016,0.0035], { category:'1GbE-RJ45', installed:true, port:2 });
  box('Rear_USB3_Port_1', mat.blue, [0.089,-0.012,rearZ], [0.022,0.008,0.0035], { category:'USB-3.0', installed:true, port:1 });
  box('Rear_USB3_Port_2', mat.blue, [0.054,-0.012,rearZ], [0.022,0.008,0.0035], { category:'USB-3.0', installed:true, port:2 });
  cyl('Rear_System_ID_Button', mat.blue, [0.022,-0.008,-0.2829], [0.007,0.007,0.0026], { category:'system-ID' });
  box('Rear_CMA_Connector', mat.black, [0.010,0.010,rearZ], [0.012,0.014,0.0035], { category:'CMA-connector' });

  // One half-height and one full-height PCIe blanking plate, not rear drives.
  box('PCIe_HalfHeight_Blanking_Plate', mat.silverDark, [-0.040,0.008,-0.2790], [0.071,0.023,0.0100], { category:'PCIe-blanking-plate', form:'half-height', installed:true });
  box('PCIe_FullHeight_Blanking_Plate', mat.silverDark, [-0.115,0.008,-0.2790], [0.078,0.026,0.0100], { category:'PCIe-blanking-plate', form:'full-height', installed:true });
  box('Rear_Blue_Expansion_Latch', mat.blue, [0.016,0.0149,-0.2822], [0.012,0.013,0.0040], { category:'Dell-blue-retention-latch' });

  // Lower rear vent field as recessed cells.
  for (let i = 0; i < 24; i++) {
    const x = 0.185 - i * 0.0125;
    box(`Rear_Lower_Vent_Cell_${String(i+1).padStart(2,'0')}`, mat.black, [x,-0.0155,-0.28235], [0.0080,0.0048,0.0032], { category:'rear-vent-cell' });
  }

  // R240 has exactly one fixed/cabled non-redundant AC PSU. The opposite area
  // is chassis/expansion metal; no second PSU slot or handle is present.
  box('AC_PSU_Fixed_Body', mat.silverDark, [-0.169,-0.0034,-0.2757], [0.093,0.036,0.0170], { category:'fixed-cabled-AC-PSU', installed:true, count:1, topology:'non-redundant', nominalOptions:'250W Bronze or 450W Platinum' });
  box('AC_PSU_IEC_C14_Inlet', mat.black, [-0.173,-0.002,-0.28235], [0.035,0.026,0.0039], { category:'IEC-C14-AC-inlet' });
  cyl('AC_PSU_BIST_LED', mat.green, [-0.137,0.005,-0.2830], [0.006,0.006,0.0025], { category:'PSU-BIST-LED' });
  for (let col = 0; col < 4; col++) for (let row = 0; row < 3; row++) {
    box(`AC_PSU_Exhaust_${col+1}_${row+1}`, mat.black, [-0.205+col*0.010,-0.012+row*0.010,-0.2827], [0.0062,0.0062,0.0030], { category:'PSU-exhaust-cell' });
  }
  box('AC_PSU_Cable_Retention_Strap', mat.graphite, [-0.215,-0.0044,-0.27935], [0.008,0.034,0.0096], { category:'PSU-cable-retention' });
  b.addEmptyNode('Second_AC_PSU_ABSENT', { category:'configuration-lock', installed:false, reason:'PowerEdge R240 supports one fixed cabled non-redundant PSU only' });

  // Physical left and right side details are independent, asymmetric nodes.
  const rightDetails = [[0.210,0.010,0.010],[0.114,-0.006,0.007],[-0.004,0.007,0.011],[-0.157,-0.005,0.009],[-0.239,0.006,0.008]];
  rightDetails.forEach((item,index) => box(`Right_Side_Rail_Feature_${index+1}`, index === 0 ? mat.graphite : mat.black, [0.21745,item[1],item[0]], [0.0008,0.005,item[2]], { category:'right-side-rail-feature' }));
  const leftDetails = [[0.242,-0.009,0.009],[0.133,0.006,0.011],[0.018,-0.005,0.008],[-0.111,0.008,0.010],[-0.231,-0.006,0.007]];
  leftDetails.forEach((item,index) => box(`Left_Side_Rail_Feature_${index+1}`, index === 4 ? mat.graphite : mat.black, [-0.21745,item[1],item[0]], [0.0008,0.005,item[2]], { category:'left-side-rail-feature' }));

  // Verified top service latch and rear ventilation band relief.
  box('Top_Service_Latch', mat.graphite, [0,0.0209,0.105], [0.030,0.0010,0.068], { category:'top-cover-latch', visibleSurfaceAtTop:true });
  for (let i = 0; i < 18; i++) {
    box(`Top_Rear_Vent_Cell_${String(i+1).padStart(2,'0')}`, mat.black, [-0.160+i*0.019,0.0209,-0.217], [0.011,0.0010,0.020], { category:'top-rear-vent-cell' });
  }

  // Four single-rotor cabled fans are source-verified. They remain below the
  // opaque installed cover but are separately named/modelled for configuration QA.
  const fanXs = [-0.120,-0.040,0.040,0.120];
  fanXs.forEach((x,index) => {
    box(`Internal_Cabled_Fan_${index+1}_Housing`, mat.black, [x,0,0.105], [0.054,0.034,0.050], { category:'single-rotor-cabled-fan', visibleWithCover:false });
    cyl(`Internal_Cabled_Fan_${index+1}_Rotor`, mat.silverDark, [x,0,0.105], [0.036,0.036,0.018], { category:'fan-rotor', visibleWithCover:false });
  });

  const extras = {
    exactProductId: 'Dell EMC PowerEdge R240',
    regulatoryModel: 'E57S / E57S001',
    configuration: '4 x 3.5-inch LFF hot-swap; bezel absent; standard rear; one fixed/cabled AC PSU installed; four cabled fans',
    dimensionsMillimeters: {
      overallWidth:482.0, bodyWidth:434.0, height:42.8,
      bodyDepth:534.496, overallDepth:573.596,
      frontProjectionWithoutBezel:22.0, rearProjection:17.1,
    },
    coordinateConvention: '+X device right from front; +Y up; +Z front',
    bottomStatus: 'GENERIC_BOTTOM_FALLBACK',
    faceTextureEmbedding: 'All six materials OPAQUE; six canonical transparent PNGs remain in ../views.',
    textureVariant: variant,
    sourceManifest: '../source/identity-manifest.md',
    featureInventory: '../source/feature-inventory.csv',
    faceSourceLock: '../source/face-source-lock.csv',
  };
  b.write(path.join(__dirname, outputName), extras);
}

buildVariant(path.join(ROOT,'qa','build','opaque-standard'), 'Dell-R240-3.5inch.glb', 'standard');
buildVariant(path.join(ROOT,'qa','build','opaque-web'), 'Dell-R240-3.5inch-web.glb', 'web');
