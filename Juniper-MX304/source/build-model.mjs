import fs from 'node:fs';
import path from 'node:path';
import * as THREE from '/tmp/codex-mx304/node/node_modules/three/build/three.module.js';
import { RoundedBoxGeometry } from '/tmp/codex-mx304/node/node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { Document, NodeIO } from '/tmp/codex-mx304/node/node_modules/@gltf-transform/core/dist/index.js';
import { KHRMaterialsUnlit } from '/tmp/codex-mx304/node/node_modules/@gltf-transform/extensions/dist/index.js';

const MODEL_DIR = '/root/Project/rack-device-3d/Juniper-MX304';
const MM = 0.001;
const m = (value) => value * MM;

const BODY_W = 440.9;
const BODY_H = 88.9;
const BODY_D = 610.0;
const OVERALL_W = 482.6;
const FRONT_PROJ = 16.7;
const REAR_PROJ = 40.5;
const EAR_W = (OVERALL_W - BODY_W) / 2;

function makeMaterial(document, name, rgba, metallic = 0, roughness = 0.72) {
  return document.createMaterial(name)
    .setBaseColorFactor(rgba)
    .setMetallicFactor(metallic)
    .setRoughnessFactor(roughness)
    .setDoubleSided(false);
}

function makeTextureMaterial(document, unlitExtension, name, imagePath) {
  const texture = document.createTexture(name + ' texture')
    .setImage(fs.readFileSync(imagePath))
    .setMimeType(path.extname(imagePath).toLowerCase() === '.jpg' ? 'image/jpeg' : 'image/png');
  const material = document.createMaterial(name)
    .setBaseColorFactor([1, 1, 1, 1])
    .setBaseColorTexture(texture)
    .setMetallicFactor(0)
    .setRoughnessFactor(1)
    .setDoubleSided(false);
  material.setExtension('KHR_materials_unlit', unlitExtension.createUnlit());
  return material;
}

function geometryPrimitive(document, buffer, geometry, material) {
  if (!geometry.getAttribute('normal')) geometry.computeVertexNormals();
  const position = geometry.getAttribute('position');
  const normal = geometry.getAttribute('normal');
  const uv = geometry.getAttribute('uv');
  const primitive = document.createPrimitive();
  primitive.setAttribute('POSITION', document.createAccessor()
    .setType('VEC3').setArray(new Float32Array(position.array)).setBuffer(buffer));
  primitive.setAttribute('NORMAL', document.createAccessor()
    .setType('VEC3').setArray(new Float32Array(normal.array)).setBuffer(buffer));
  if (uv) {
    primitive.setAttribute('TEXCOORD_0', document.createAccessor()
      .setType('VEC2').setArray(new Float32Array(uv.array)).setBuffer(buffer));
  }
  let indexArray;
  if (geometry.getIndex()) {
    const source = geometry.getIndex().array;
    indexArray = position.count > 65535 ? new Uint32Array(source) : new Uint16Array(source);
  } else {
    indexArray = position.count > 65535
      ? new Uint32Array(Array.from({ length: position.count }, (_, i) => i))
      : new Uint16Array(Array.from({ length: position.count }, (_, i) => i));
  }
  primitive.setIndices(document.createAccessor()
    .setType('SCALAR').setArray(indexArray).setBuffer(buffer));
  primitive.setMaterial(material);
  return primitive;
}

function addMeshNode(context, name, mesh, translation = [0, 0, 0], rotation = [0, 0, 0]) {
  const { document, assembly } = context;
  const node = document.createNode(name).setMesh(mesh).setTranslation(translation);
  if (rotation.some((value) => Math.abs(value) > 1e-12)) {
    const quaternion = new THREE.Quaternion().setFromEuler(
      new THREE.Euler(rotation[0], rotation[1], rotation[2], 'XYZ')
    );
    node.setRotation([quaternion.x, quaternion.y, quaternion.z, quaternion.w]);
  }
  assembly.addChild(node);
  return node;
}

function addGeometry(context, name, geometry, material, translation = [0, 0, 0], rotation = [0, 0, 0]) {
  const { document, buffer } = context;
  const mesh = document.createMesh(name + ' mesh')
    .addPrimitive(geometryPrimitive(document, buffer, geometry, material));
  return addMeshNode(context, name, mesh, translation, rotation);
}

function addBox(context, name, sizeMM, centerMM, material, rotation = [0, 0, 0], rounded = 0) {
  const cacheKey = 'box|' + sizeMM.join(',') + '|' + rounded + '|' + material.getName();
  let mesh = context.meshCache.get(cacheKey);
  if (!mesh) {
  const size = sizeMM.map(m);
  const geometry = rounded > 0
    ? new RoundedBoxGeometry(size[0], size[1], size[2], 3, m(rounded))
    : new THREE.BoxGeometry(size[0], size[1], size[2]);
    mesh = context.document.createMesh(name + ' shared mesh')
      .addPrimitive(geometryPrimitive(context.document, context.buffer, geometry, material));
    context.meshCache.set(cacheKey, mesh);
  }
  return addMeshNode(context, name, mesh, centerMM.map(m), rotation);
}

function addOpenFrontBox(context, name, sizeMM, centerMM, material, rotation = [0, 0, 0]) {
  const cacheKey = 'open-front-box|' + sizeMM.join(',') + '|' + material.getName();
  let mesh = context.meshCache.get(cacheKey);
  if (!mesh) {
    const [w, h, d] = sizeMM.map(m);
    const x0 = -w / 2, x1 = w / 2, y0 = -h / 2, y1 = h / 2, z0 = -d / 2, z1 = d / 2;
    const positions = [
      x0,y1,z0, x0,y0,z0, x1,y0,z0, x1,y1,z0,
      x0,y1,z1, x0,y0,z1, x0,y0,z0, x0,y1,z0,
      x1,y1,z0, x1,y0,z0, x1,y0,z1, x1,y1,z1,
      x0,y1,z0, x1,y1,z0, x1,y1,z1, x0,y1,z1,
      x0,y0,z1, x1,y0,z1, x1,y0,z0, x0,y0,z0
    ];
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setIndex([
      0,1,2, 0,2,3,
      4,5,6, 4,6,7,
      8,9,10, 8,10,11,
      12,13,14, 12,14,15,
      16,17,18, 16,18,19
    ]);
    geometry.computeVertexNormals();
    mesh = context.document.createMesh(name + ' shared mesh')
      .addPrimitive(geometryPrimitive(context.document, context.buffer, geometry, material));
    context.meshCache.set(cacheKey, mesh);
  }
  return addMeshNode(context, name, mesh, centerMM.map(m), rotation);
}

function addCylinder(context, name, radiusMM, depthMM, centerMM, material, rotation = [Math.PI / 2, 0, 0], segments = 24) {
  const cacheKey = 'cylinder|' + radiusMM + '|' + depthMM + '|' + segments + '|' + material.getName();
  let mesh = context.meshCache.get(cacheKey);
  if (!mesh) {
    const geometry = new THREE.CylinderGeometry(m(radiusMM), m(radiusMM), m(depthMM), segments, 1, false);
    mesh = context.document.createMesh(name + ' shared mesh')
      .addPrimitive(geometryPrimitive(context.document, context.buffer, geometry, material));
    context.meshCache.set(cacheKey, mesh);
  }
  return addMeshNode(context, name, mesh, centerMM.map(m), rotation);
}

function addQuad(context, name, positionsMM, uvs, indices, material) {
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positionsMM.map(m), 3));
  geometry.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  return addGeometry(context, name, geometry, material);
}

function addFaceQuads(context, materials) {
  const x0 = -BODY_W / 2, x1 = BODY_W / 2;
  const y0 = -BODY_H / 2, y1 = BODY_H / 2;
  const z0 = -BODY_D / 2, z1 = BODY_D / 2;
  const uv = [0, 0, 0, 1, 1, 1, 1, 0];
  const uvHorizontal = [0, 0, 1, 0, 1, 1, 0, 1];
  const uvPhysicalSide = [1, 0, 0, 0, 0, 1, 1, 1];

  addQuad(context, 'Front source-locked face', [
    x0, y1, 314.0, x0, y0, 314.0, x1, y0, 314.0, x1, y1, 314.0
  ], uv, [0, 1, 2, 0, 2, 3], materials.front);

  addQuad(context, 'Rear source-locked AC face', [
    x1, y1, -(z1 + REAR_PROJ), x1, y0, -(z1 + REAR_PROJ),
    x0, y0, -(z1 + REAR_PROJ), x0, y1, -(z1 + REAR_PROJ)
  ], uv, [0, 1, 2, 0, 2, 3], materials.rear);

  addQuad(context, 'Right reconstructed face', [
    x1, y1, z0, x1, y1, z1, x1, y0, z1, x1, y0, z0
  ], uvPhysicalSide, [0, 1, 2, 0, 2, 3], materials.right);

  addQuad(context, 'Left reconstructed face', [
    x0, y1, z1, x0, y1, z0, x0, y0, z0, x0, y0, z1
  ], uvPhysicalSide, [0, 1, 2, 0, 2, 3], materials.left);

  addQuad(context, 'Top reconstructed face', [
    x0, y1, z0, x0, y1, z1, x1, y1, z1, x1, y1, z0
  ], uv, [0, 1, 2, 0, 2, 3], materials.top);

  addQuad(context, 'Bottom fallback face', [
    x0, y0, z1, x0, y0, z0, x1, y0, z0, x1, y0, z1
  ], uv, [0, 1, 2, 0, 2, 3], materials.bottom);
}

function addRackEars(context, material) {
  const depth = m(3.0);
  for (const side of [-1, 1]) {
    const shape = new THREE.Shape();
    const width = m(EAR_W), height = m(BODY_H);
    shape.moveTo(-width / 2, -height / 2);
    shape.lineTo(width / 2, -height / 2);
    shape.lineTo(width / 2, height / 2);
    shape.lineTo(-width / 2, height / 2);
    shape.closePath();
    const holes = [
      [-35.0, 7.0, 5.5], [-22.0, 3.2, 3.2], [-10.0, 7.0, 5.5],
      [10.0, 7.0, 5.5], [22.0, 3.2, 3.2], [35.0, 7.0, 5.5]
    ];
    for (const [y, rx, ry] of holes) {
      const hole = new THREE.Path();
      hole.absellipse(0, m(y), m(rx), m(ry), 0, Math.PI * 2, false, 0);
      shape.holes.push(hole);
    }
    const geometry = new THREE.ExtrudeGeometry(shape, {
      depth, bevelEnabled: false, steps: 1, curveSegments: 24
    });
    geometry.translate(0, 0, -depth / 2);
    addGeometry(context, side < 0 ? 'Front rack ear left with holes' : 'Front rack ear right with holes',
      geometry, material,
      [m(side * (BODY_W / 2 + EAR_W / 2)), 0, m(BODY_D / 2 + 1.5)]);
  }
}

function addFrontGeometry(context, materials) {
  const moduleX = [-103.0, 103.0];
  const moduleY = [22.0, -22.0];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 2; col++) {
      const type = row === 0 ? 'Routing Engine' : 'LMIC16';
      addBox(context, type + ' module ' + row + '-' + col,
        [198.0, 39.0, 6.0], [moduleX[col], moduleY[row], 308.0], materials.silver, [0, 0, 0], 1.0);
    }
  }

  const handleX = [-212.5, -15.5, 4.0, 192.0];
  for (const y of moduleY) {
    handleX.forEach((x, index) => {
      addOpenFrontBox(context, 'Cyan ejector handle depth shell ' + y + '-' + index,
        [9.0, 24.0, 7.8], [x, y, BODY_D / 2 + FRONT_PROJ - 3.9], materials.cyan);
    });
  }

  const lmics = [
    { x0: -192.0, x1: -26.0, tag: 'LMIC0' },
    { x0: 18.0, x1: 184.0, tag: 'LMIC1' }
  ];
  for (const lmic of lmics) {
    for (let column = 0; column < 8; column++) {
      const x = lmic.x0 + (lmic.x1 - lmic.x0) * (column + 0.5) / 8;
      for (let row = 0; row < 2; row++) {
        const y = -17.0 - row * 14.0;
        addBox(context, lmic.tag + ' cage rim ' + column + '-' + row,
          [18.0, 11.0, 2.0], [x, y, 312.2], materials.cageRim, [0, 0, 0], 0.8);
        addBox(context, lmic.tag + ' empty cage ' + column + '-' + row,
          [15.5, 8.5, 1.8], [x, y, 313.0], materials.black, [0, 0, 0], 0.5);
      }
    }
  }

  for (const centerX of moduleX) {
    addBox(context, 'RE console port ' + centerX, [15, 12, 2.5],
      [centerX - 18, 20.5, 312.6], materials.black, [0, 0, 0], 0.7);
    addBox(context, 'RE management port ' + centerX, [15, 12, 2.5],
      [centerX + 22, 20.5, 312.6], materials.black, [0, 0, 0], 0.7);
    addBox(context, 'RE USB port ' + centerX, [5, 14, 2.6],
      [centerX + 46, 20.5, 312.6], materials.usb, [0, 0, 0], 0.5);
  }
}

function addSideGeometry(context, materials) {
  const zPositions = [-205, -70, 65, 200];
  for (const side of [-1, 1]) {
    for (const y of [-22, 22]) {
      zPositions.forEach((z, i) => {
        addOpenFrontBox(context, (side < 0 ? 'Left' : 'Right') + ' rail recess depth shell ' + y + '-' + i,
          [92.0, 12.0, 4.0], [side * (BODY_W / 2 - 2.0), y, z], materials.slot,
          [0, side < 0 ? -Math.PI / 2 : Math.PI / 2, 0]);
      });
    }
    addOpenFrontBox(context, (side < 0 ? 'Left' : 'Right') + ' front rectangular pad depth shell',
      [48.0, 31.0, 4.0], [side * (BODY_W / 2 - 2.0), 0, 263], materials.pad,
      [0, side < 0 ? -Math.PI / 2 : Math.PI / 2, 0]);
  }
}

function addTopGeometry(context, materials) {
  addBox(context, 'Top transverse seam', [BODY_W - 2, 0.7, 2.0],
    [0, BODY_H / 2 - 0.35, -38], materials.seam, [0, 0, 0], 0.2);
}

function addRearGeometry(context, materials) {
  const blockDepth = REAR_PROJ - 1.0;
  const rearCenter = -(BODY_D / 2 + blockDepth / 2);
  const rearFace = -(BODY_D / 2 + REAR_PROJ);

  for (let row = 0; row < 2; row++) {
    const y = row === 0 ? 22 : -22;
    addBox(context, 'AC PSU' + row, [72, 40, blockDepth], [180, y, rearCenter], materials.psu, [0, 0, 0], 1.0);
  }

  addBox(context, 'Timing interface panel', [31, 82, blockDepth], [127, 0, rearCenter], materials.darkGray, [0, 0, 0], 0.8);

  const fanCenters = [61, -49, -159];
  fanCenters.forEach((x, index) => {
    addBox(context, 'Fan tray ' + index, [98, 82, blockDepth], [x, 0, rearCenter], materials.pad, [0, 0, 0], 1.0);
    addOpenFrontBox(context, 'Fan orange frame depth shell ' + index,
      [90, 74, 8], [x, 0, rearFace + 4.1], materials.orange, [0, Math.PI, 0]);
  });

  addBox(context, 'Ground and ESD end panel', [12, 82, blockDepth], [-214, 0, rearCenter], materials.darkGray, [0, 0, 0], 0.8);
}

async function build(textureVariant, outputName) {
  const document = new Document();
  const buffer = document.createBuffer('Embedded geometry buffer');
  const unlitExtension = document.createExtension(KHRMaterialsUnlit).setRequired(false);
  const scene = document.createScene('Juniper MX304 Scene');
  const assembly = document.createNode('Juniper MX304-PREM-AC-FS complete assembly').setExtras({
    manufacturer: 'Juniper Networks',
    pid: 'MX304-PREM-AC-FS',
    configuration: '2x JNP304-RE; 2x MX304-LMIC16-BASE; 2x JNP-PWR2200-AC; 3x JNP-FAN-2RU',
    uHeight: 2,
    coordinateConvention: '+X device right from front, +Y up, +Z front',
    bottom: 'GENERIC_BOTTOM_FALLBACK'
  });
  scene.addChild(assembly);
  const context = { document, buffer, assembly, meshCache: new Map() };

  const textureDir = path.join(MODEL_DIR, 'qa/model-textures', textureVariant);
  const textureSuffix = textureVariant === 'web' ? '.jpg' : '.png';
  const faceMaterials = {
    front: makeTextureMaterial(document, unlitExtension, 'Front source-locked photo material', path.join(textureDir, 'front-body' + textureSuffix)),
    rear: makeTextureMaterial(document, unlitExtension, 'Rear AC source-locked photo material', path.join(textureDir, 'rear-body' + textureSuffix)),
    left: makeTextureMaterial(document, unlitExtension, 'Left reconstructed photo material', path.join(textureDir, 'left-body' + textureSuffix)),
    right: makeTextureMaterial(document, unlitExtension, 'Right reconstructed photo material', path.join(textureDir, 'right-body' + textureSuffix)),
    top: makeTextureMaterial(document, unlitExtension, 'Top reconstructed photo material', path.join(textureDir, 'top-body' + textureSuffix)),
    bottom: makeTextureMaterial(document, unlitExtension, 'Bottom fallback photo material', path.join(textureDir, 'bottom-body' + textureSuffix))
  };

  const materials = {
    silver: makeMaterial(document, 'Brushed silver FRU metal', [0.72, 0.73, 0.73, 1], 0.05, 0.52),
    steel: makeMaterial(document, 'Silver fastener metal', [0.58, 0.60, 0.61, 1], 0.55, 0.3),
    cyan: makeMaterial(document, 'Juniper cyan ejector plastic', [0.20, 0.67, 0.84, 1], 0, 0.45),
    orange: makeMaterial(document, 'Juniper orange fan and PSU handle', [1.0, 0.27, 0.035, 1], 0, 0.46),
    black: makeMaterial(document, 'Black recessed connector and grille', [0.008, 0.010, 0.012, 1], 0, 0.86),
    darkGray: makeMaterial(document, 'Rear dark gray panel', [0.22, 0.23, 0.24, 1], 0.03, 0.62),
    psu: makeMaterial(document, 'AC PSU housing', [0.43, 0.44, 0.45, 1], 0.12, 0.52),
    gold: makeMaterial(document, 'Timing BNC gold metal', [0.86, 0.52, 0.12, 1], 0.75, 0.28),
    cageRim: makeMaterial(document, 'QSFP cage rim', [0.62, 0.63, 0.62, 1], 0.32, 0.42),
    usb: makeMaterial(document, 'USB 3 blue insert', [0.01, 0.25, 0.68, 1], 0, 0.65),
    slot: makeMaterial(document, 'Side rail recess', [0.23, 0.24, 0.24, 1], 0.02, 0.85),
    pad: makeMaterial(document, 'Side and top inset panel', [0.51, 0.52, 0.52, 1], 0.04, 0.75),
    seam: makeMaterial(document, 'Panel seam', [0.15, 0.16, 0.16, 1], 0, 0.92)
  };

  addFaceQuads(context, faceMaterials);
  addRackEars(context, materials.steel);
  addFrontGeometry(context, materials);
  addSideGeometry(context, materials);
  addTopGeometry(context, materials);
  addRearGeometry(context, materials);

  const io = new NodeIO().registerExtensions([KHRMaterialsUnlit]);
  await io.write(path.join(MODEL_DIR, 'model', outputName), document);
}

await build('standard', 'Juniper-MX304.glb');
await build('web', 'Juniper-MX304-web.glb');
