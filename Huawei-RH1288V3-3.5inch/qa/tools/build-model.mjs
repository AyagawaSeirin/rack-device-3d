#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const args = new Map();
for (let i = 2; i < process.argv.length; i += 2) {
  args.set(process.argv[i], process.argv[i + 1]);
}
const textureDir = args.get("--textures");
const outputPath = args.get("--output");
const variant = args.get("--variant") || "standard";
if (!textureDir || !outputPath) {
  throw new Error("Usage: build-model.mjs --textures DIR --output FILE [--variant standard|web]");
}

const gltf = {
  asset: {
    version: "2.0",
    generator: `RH1288 V3 exact exterior builder (${variant})`,
    copyright: "Newly constructed exact-appearance exterior; Huawei marks retained as product detail",
    extras: {
      manufacturer: "Huawei Technologies Co., Ltd.",
      product: "FusionServer RH1288 V3",
      officialNameplateModel: "H12M-03",
      configuration: "1U 4x3.5-inch LFF, four-GE FlexIO, dual 460W Platinum AC PSU",
      coordinateConvention: "+X device right, +Y up, +Z front",
      bottomEvidence: "GENERIC_BOTTOM_FALLBACK",
    },
  },
  extensionsUsed: ["KHR_materials_unlit"],
  scene: 0,
  scenes: [{ name: "Huawei RH1288 V3 4LFF", nodes: [] }],
  nodes: [],
  meshes: [],
  accessors: [],
  bufferViews: [],
  buffers: [{ byteLength: 0 }],
  materials: [],
  images: [],
  textures: [],
  samplers: [
    {
      name: "Linear clamp sampler",
      magFilter: 9729,
      minFilter: 9987,
      wrapS: 33071,
      wrapT: 33071,
    },
  ],
};

const binaryParts = [];
let binaryLength = 0;

function appendBinary(source, target) {
  const buffer = Buffer.isBuffer(source) ? source : Buffer.from(source.buffer, source.byteOffset, source.byteLength);
  const pad = (4 - (binaryLength % 4)) % 4;
  if (pad) {
    binaryParts.push(Buffer.alloc(pad));
    binaryLength += pad;
  }
  const view = {
    buffer: 0,
    byteOffset: binaryLength,
    byteLength: buffer.length,
  };
  if (target) view.target = target;
  const index = gltf.bufferViews.push(view) - 1;
  binaryParts.push(buffer);
  binaryLength += buffer.length;
  return index;
}

function addAccessor(values, componentType, type, count, target, min, max) {
  let typed;
  if (componentType === 5126) typed = new Float32Array(values);
  else if (componentType === 5123) typed = new Uint16Array(values);
  else throw new Error(`Unsupported component type ${componentType}`);
  const bufferView = appendBinary(typed, target);
  const accessor = { bufferView, byteOffset: 0, componentType, count, type };
  if (min) accessor.min = min;
  if (max) accessor.max = max;
  return gltf.accessors.push(accessor) - 1;
}

function positionBounds(values) {
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < values.length; i += 3) {
    for (let j = 0; j < 3; j++) {
      min[j] = Math.min(min[j], values[i + j]);
      max[j] = Math.max(max[j], values[i + j]);
    }
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
  const primitive = {
    attributes,
    indices: addAccessor(indices, 5123, "SCALAR", indices.length, 34963),
    material,
    mode: 4,
  };
  const mesh = gltf.meshes.push({ name, primitives: [primitive] }) - 1;
  const node = gltf.nodes.push({ name, mesh }) - 1;
  gltf.scenes[0].nodes.push(node);
  return node;
}

function addMaterial(name, color, textureIndex = null) {
  const pbr = {
    baseColorFactor: color,
    metallicFactor: 0,
    roughnessFactor: 1,
  };
  if (textureIndex !== null) pbr.baseColorTexture = { index: textureIndex };
  return gltf.materials.push({
    name,
    pbrMetallicRoughness: pbr,
    alphaMode: "OPAQUE",
    doubleSided: false,
    extensions: { KHR_materials_unlit: {} },
  }) - 1;
}

function addTexture(name) {
  const filename = path.join(textureDir, `${name}.png`);
  const bytes = fs.readFileSync(filename);
  const bufferView = appendBinary(bytes);
  const image = gltf.images.push({ name: `${name} RGB source-locked texture`, mimeType: "image/png", bufferView }) - 1;
  return gltf.textures.push({ name: `${name} texture`, sampler: 0, source: image }) - 1;
}

const faceMaterials = {};
for (const face of ["front", "rear", "left", "right", "top", "bottom"]) {
  faceMaterials[face] = addMaterial(`${face} source-locked unlit`, [1, 1, 1, 1], addTexture(face));
}

const MAT = {
  silver: addMaterial("Galvanized silver", [0.56, 0.57, 0.54, 1]),
  darkSilver: addMaterial("Dark galvanized recess", [0.22, 0.23, 0.22, 1]),
  black: addMaterial("Huawei matte black", [0.025, 0.028, 0.026, 1]),
  grille: addMaterial("Opaque grille recess", [0.008, 0.009, 0.008, 1]),
  lime: addMaterial("Huawei lime release accent", [0.47, 0.75, 0.02, 1]),
  blue: addMaterial("USB/VGA blue insert", [0.02, 0.24, 0.63, 1]),
  teal: addMaterial("Serial panel teal", [0.03, 0.51, 0.43, 1]),
  green: addMaterial("PSU green indicator", [0.0, 0.38, 0.12, 1]),
};

function quadForFace(face, center, size, uv = [0, 0, 1, 1]) {
  const [x, y, z] = center;
  const [sx, sy, sz] = size;
  const hx = sx / 2, hy = sy / 2, hz = sz / 2;
  const [u0, v0, u1, v1] = uv;
  const uvs = [u0, v0, u0, v1, u1, v1, u1, v0];
  let p, n;
  switch (face) {
    case "+X":
      p = [x + hx, y + hy, z + hz, x + hx, y - hy, z + hz, x + hx, y - hy, z - hz, x + hx, y + hy, z - hz];
      n = [1, 0, 0]; break;
    case "-X":
      p = [x - hx, y + hy, z - hz, x - hx, y - hy, z - hz, x - hx, y - hy, z + hz, x - hx, y + hy, z + hz];
      n = [-1, 0, 0]; break;
    case "+Y":
      p = [x - hx, y + hy, z - hz, x - hx, y + hy, z + hz, x + hx, y + hy, z + hz, x + hx, y + hy, z - hz];
      n = [0, 1, 0]; break;
    case "-Y":
      p = [x + hx, y - hy, z - hz, x + hx, y - hy, z + hz, x - hx, y - hy, z + hz, x - hx, y - hy, z - hz];
      n = [0, -1, 0]; break;
    case "+Z":
      p = [x - hx, y + hy, z + hz, x - hx, y - hy, z + hz, x + hx, y - hy, z + hz, x + hx, y + hy, z + hz];
      n = [0, 0, 1]; break;
    case "-Z":
      p = [x + hx, y + hy, z - hz, x + hx, y - hy, z - hz, x - hx, y - hy, z - hz, x - hx, y + hy, z - hz];
      n = [0, 0, -1]; break;
    default: throw new Error(`Unknown face ${face}`);
  }
  return { positions: p, normals: [...n, ...n, ...n, ...n], uvs, indices: [0, 1, 2, 0, 2, 3] };
}

function addQuad(name, face, center, size, material, uv) {
  const q = quadForFace(face, center, size, uv);
  return addPrimitive(name, q.positions, q.normals, q.uvs, q.indices, material);
}

function addBox(name, center, size, material) {
  const positions = [], normals = [], uvs = [], indices = [];
  for (const face of ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]) {
    const q = quadForFace(face, center, size);
    const base = positions.length / 3;
    positions.push(...q.positions);
    normals.push(...q.normals);
    uvs.push(...q.uvs);
    indices.push(...q.indices.map((value) => value + base));
  }
  return addPrimitive(name, positions, normals, uvs, indices, material);
}

function addCylinderZ(name, center, radius, depth, segments, material) {
  const [cx, cy, cz] = center;
  const positions = [], normals = [], indices = [];
  for (let i = 0; i < segments; i++) {
    const a0 = (i / segments) * Math.PI * 2;
    const a1 = ((i + 1) / segments) * Math.PI * 2;
    const x0 = cx + Math.cos(a0) * radius;
    const y0 = cy + Math.sin(a0) * radius;
    const x1 = cx + Math.cos(a1) * radius;
    const y1 = cy + Math.sin(a1) * radius;
    const zFront = cz - depth / 2;
    const zBack = cz + depth / 2;
    const base = positions.length / 3;
    positions.push(x0, y0, zFront, x1, y1, zFront, x1, y1, zBack, x0, y0, zBack);
    normals.push(Math.cos(a0), Math.sin(a0), 0, Math.cos(a1), Math.sin(a1), 0, Math.cos(a1), Math.sin(a1), 0, Math.cos(a0), Math.sin(a0), 0);
    indices.push(base, base + 1, base + 2, base, base + 2, base + 3);
  }
  let base = positions.length / 3;
  positions.push(cx, cy, cz - depth / 2);
  normals.push(0, 0, -1);
  for (let i = 0; i < segments; i++) {
    const a = (i / segments) * Math.PI * 2;
    positions.push(cx + Math.cos(a) * radius, cy + Math.sin(a) * radius, cz - depth / 2);
    normals.push(0, 0, -1);
  }
  for (let i = 0; i < segments; i++) indices.push(base, base + 1 + ((i + 1) % segments), base + 1 + i);
  return addPrimitive(name, positions, normals, null, indices, material);
}

// Authoritative outer envelope in metres.
const BODY_W = 0.436;
const OVERALL_W = 0.4826;
const HEIGHT = 0.043;
const DEPTH = 0.748;

// Closed inner shell; canonical textured planes and exterior modules sit just outside it.
addBox("Closed chassis shell", [0, 0, 0], [BODY_W - 0.001, HEIGHT - 0.002, DEPTH - 0.002], MAT.silver);

// Six canonical photographic surfaces.  The rear photo sits ahead of the small
// I/O carrier blocks so real connector shells, pins, labels, and recess shadows
// remain visible; only silhouette/parallax-critical PCIe and PSU relief projects
// beyond it.
addQuad("Front canonical base", "+Z", [0, 0, 0.37355], [OVERALL_W, HEIGHT, 0], faceMaterials.front);
addQuad("Rear canonical base", "-Z", [0, 0, -0.3742], [BODY_W, HEIGHT, 0], faceMaterials.rear);
addQuad("Physical left canonical face", "-X", [-0.2181, 0, 0], [0, HEIGHT, DEPTH], faceMaterials.left);
addQuad("Physical right canonical face", "+X", [0.2181, 0, 0], [0, HEIGHT, DEPTH], faceMaterials.right);
addQuad("Top canonical face", "+Y", [0, 0.0206, 0], [BODY_W, 0, DEPTH], faceMaterials.top);
addQuad("Bottom canonical fallback face", "-Y", [0, -0.0214, 0], [BODY_W, 0, DEPTH], faceMaterials.bottom);

// Separate front ears, all within the official 482.6 mm mounting span.
// Keep photographic subfaces measurably in front of their carrier boxes.  The
// previous coplanar placement was resolved differently by Three.js and
// Babylon.js, allowing the flat black carrier geometry to hide the source
// honeycomb texture in Babylon.
const FRONT_SOURCE_Z = 0.3742;
const FRONT_RELIEF_Z = 0.37455;
for (const [label, x, uv] of [
  ["left Huawei ear", -0.22965, [0.0, 0.0, 0.055, 1.0]],
  ["right model ear", 0.22965, [0.945, 0.0, 1.0, 1.0]],
]) {
  addBox(`Front ${label} body`, [x, 0, 0.368], [0.0233, HEIGHT, 0.012], MAT.black);
  addQuad(`Front ${label} source face`, "+Z", [x, 0, FRONT_SOURCE_Z], [0.0233, HEIGHT, 0], faceMaterials.front, uv);
}

// Four independently recessed LFF carriers with independent right-side handles/status strips.
const carrierXs = [-0.159, -0.053, 0.053, 0.159];
const carrierUv = [[0.075, 0.34, 0.278, 0.96], [0.282, 0.34, 0.478, 0.96], [0.482, 0.34, 0.681, 0.96], [0.685, 0.34, 0.89, 0.96]];
carrierXs.forEach((x, i) => {
  addBox(`LFF carrier ${i} recessed body`, [x, -0.004, 0.368], [0.102, 0.030, 0.012], MAT.black);
  addQuad(`LFF carrier ${i} source face`, "+Z", [x, -0.004, FRONT_SOURCE_Z], [0.102, 0.030, 0], faceMaterials.front, carrierUv[i]);
  addBox(`LFF carrier ${i} pull handle`, [x + 0.0435, -0.004, FRONT_RELIEF_Z], [0.012, 0.029, 0.0006], MAT.black);
  addBox(`LFF carrier ${i} lime status strip`, [x + 0.0365, -0.004, FRONT_RELIEF_Z], [0.0023, 0.028, 0.0005], MAT.lime);
});

// Front pull-out label and operator strip relief.
addBox("Front ESN pull-out slot", [-0.063, 0.0105, 0.3735], [0.060, 0.006, 0.001], MAT.black);
addBox("Front operator panel relief", [0.085, 0.0105, 0.3735], [0.125, 0.0065, 0.001], MAT.black);

// Top removable-cover seam, open latch frame, and two verified rows of vent relief.
// Keep the photographic label band visible: the geometry marks its seam without covering it.
addBox("Top front fixed-cover seam", [0, 0.02135, 0.250], [BODY_W, 0.00045, 0.0022], MAT.darkSilver);
addBox("Top latch frame front bar", [0, 0.02135, 0.131], [0.042, 0.00045, 0.004], MAT.darkSilver);
addBox("Top latch frame rear bar", [0, 0.02135, 0.079], [0.042, 0.00045, 0.004], MAT.darkSilver);
addBox("Top latch frame left bar", [-0.019, 0.02135, 0.105], [0.004, 0.00045, 0.052], MAT.darkSilver);
addBox("Top latch frame right bar", [0.019, 0.02135, 0.105], [0.004, 0.00045, 0.052], MAT.darkSilver);
addBox("Top latch handle", [0, 0.02155, 0.105], [0.020, 0.00035, 0.038], MAT.silver);
addBox("Top latch lime release", [0, 0.02165, 0.123], [0.016, 0.0002, 0.004], MAT.lime);
for (const [rowName, z] of [["front", 0.196], ["rear", -0.291]]) {
  for (let i = 0; i < 52; i++) {
    const x = -0.190 + (0.380 / 51) * i;
    addBox(`Top ${rowName} vent slot ${i + 1}`, [x, 0.02142, z], [0.0042, 0.00045, 0.010], MAT.grille);
  }
}

// Shallow left/right rail landmarks; these reinforce parallax without claiming open holes.
for (const [side, x, zs] of [
  ["left", -0.21835, [0.285, 0.148, -0.035, -0.245]],
  ["right", 0.21835, [0.205, -0.032]],
]) {
  zs.forEach((z, i) => addBox(`${side} rail landmark ${i + 1}`, [x, -0.004, z], [0.0005, 0.010, 0.015], MAT.darkSilver));
}
// Right-rear ventilation is physical-right only.
for (let row = 0; row < 5; row++) {
  for (let col = 0; col < 10; col++) {
    addBox(`Right rear vent ${row + 1}-${col + 1}`, [0.21838, 0.010 - row * 0.0046, -0.319 + col * 0.006], [0.00045, 0.0032, 0.0042], MAT.grille);
  }
}

// Rear PCIe blank panels and visible perforations.
for (const [name, x, width, y] of [
  ["full-height PCIe blank", 0.130, 0.154, 0.010],
  ["half-height PCIe blank", -0.012, 0.095, 0.010],
]) {
  addBox(name, [x, y, -0.369], [width, 0.020, 0.010], MAT.silver);
  const holes = Math.max(8, Math.floor(width / 0.009));
  for (let i = 0; i < holes; i++) {
    addBox(`${name} perforation ${i + 1}`, [x - width / 2 + 0.006 + i * ((width - 0.012) / Math.max(1, holes - 1)), y, -0.3745], [0.0045, 0.006, 0.0005], MAT.grille);
  }
}

// Rear I/O groups. Screen-left on the rear corresponds to positive world X.
const rearX = (screenU) => BODY_W / 2 - screenU * BODY_W;
for (let i = 0; i < 4; i++) {
  addBox(`GE service RJ45 ${i + 1}`, [rearX(0.105 + i * 0.045), -0.008, -0.372], [0.016, 0.016, 0.004], MAT.black);
  addBox(`GE service RJ45 ${i + 1} recess`, [rearX(0.105 + i * 0.045), -0.008, -0.374], [0.011, 0.010, 0.0005], MAT.grille);
}
addBox("iBMC management RJ45", [rearX(0.294), -0.008, -0.372], [0.017, 0.016, 0.004], MAT.black);
for (const [i, u] of [0.342, 0.388].entries()) addBox(`Rear USB 3.0 ${i + 1}`, [rearX(u), -0.008, -0.373], [0.019, 0.008, 0.002], MAT.blue);
addBox("Rear UID indicator", [rearX(0.420), -0.002, -0.373], [0.004, 0.004, 0.002], MAT.blue);
addBox("Rear VGA DB15", [rearX(0.470), -0.007, -0.372], [0.033, 0.017, 0.004], MAT.blue);
addBox("Rear serial DB9", [rearX(0.545), -0.007, -0.372], [0.030, 0.017, 0.004], MAT.teal);

// Two independent 460 W Platinum AC hot-swap PSU modules.
for (const [index, u] of [[1, 0.690], [2, 0.885]]) {
  const x = rearX(u);
  addBox(`460W AC PSU ${index} module`, [x, 0, -0.359], [0.080, 0.041, 0.030], MAT.silver);
  addCylinderZ(`460W AC PSU ${index} fan`, [x + 0.017, 0.001, -0.372], 0.0145, 0.004, 28, MAT.grille);
  addBox(`460W AC PSU ${index} fan guard horizontal`, [x + 0.017, 0.001, -0.374], [0.032, 0.003, 0.0006], MAT.silver);
  addBox(`460W AC PSU ${index} fan guard vertical`, [x + 0.017, 0.001, -0.374], [0.003, 0.032, 0.0006], MAT.silver);
  addBox(`460W AC PSU ${index} IEC C14 inlet`, [x - 0.021, 0.000, -0.373], [0.025, 0.025, 0.002], MAT.black);
  addBox(`460W AC PSU ${index} green indicator`, [x + 0.029, 0.013, -0.374], [0.006, 0.006, 0.0007], MAT.green);
  addBox(`460W AC PSU ${index} lime release lever`, [x - 0.036, -0.001, -0.374], [0.006, 0.026, 0.0008], MAT.lime);
  addBox(`460W AC PSU ${index} pull handle bar`, [x + 0.017, -0.008, -0.374], [0.034, 0.004, 0.001], MAT.black);
  addBox(`460W AC PSU ${index} pull handle post A`, [x + 0.003, -0.013, -0.3735], [0.004, 0.012, 0.002], MAT.black);
  addBox(`460W AC PSU ${index} pull handle post B`, [x + 0.031, -0.013, -0.3735], [0.004, 0.012, 0.002], MAT.black);
}

// Re-add key PSU relief over the complete photographic rear so three-quarter
// parallax remains visible without replacing the exact photographed module face.
for (const [index, u] of [[1, 0.690], [2, 0.885]]) {
  const x = rearX(u);
  addCylinderZ(`PSU ${index} visible fan relief`, [x + 0.017, 0.001, -0.3745], 0.014, 0.0005, 28, MAT.grille);
  addBox(`PSU ${index} visible handle`, [x + 0.017, -0.008, -0.3748], [0.034, 0.004, 0.0004], MAT.black);
  addBox(`PSU ${index} visible inlet`, [x - 0.021, 0.000, -0.3748], [0.023, 0.023, 0.0004], MAT.black);
  addBox(`PSU ${index} visible lime lever`, [x - 0.036, -0.001, -0.3748], [0.005, 0.024, 0.0004], MAT.lime);
}

const bin = Buffer.concat(binaryParts);
gltf.buffers[0].byteLength = bin.length;
let json = Buffer.from(JSON.stringify(gltf));
const jsonPad = (4 - (json.length % 4)) % 4;
if (jsonPad) json = Buffer.concat([json, Buffer.alloc(jsonPad, 0x20)]);
const binPad = (4 - (bin.length % 4)) % 4;
const paddedBin = binPad ? Buffer.concat([bin, Buffer.alloc(binPad)]) : bin;
const totalLength = 12 + 8 + json.length + 8 + paddedBin.length;
const header = Buffer.alloc(12);
header.writeUInt32LE(0x46546c67, 0);
header.writeUInt32LE(2, 4);
header.writeUInt32LE(totalLength, 8);
const jsonHeader = Buffer.alloc(8);
jsonHeader.writeUInt32LE(json.length, 0);
jsonHeader.writeUInt32LE(0x4e4f534a, 4);
const binHeader = Buffer.alloc(8);
binHeader.writeUInt32LE(paddedBin.length, 0);
binHeader.writeUInt32LE(0x004e4942, 4);

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, Buffer.concat([header, jsonHeader, json, binHeader, paddedBin]));
console.log(JSON.stringify({
  output: outputPath,
  variant,
  bytes: totalLength,
  nodes: gltf.nodes.length,
  meshes: gltf.meshes.length,
  materials: gltf.materials.length,
  textures: gltf.textures.length,
  images: gltf.images.length,
}, null, 2));
