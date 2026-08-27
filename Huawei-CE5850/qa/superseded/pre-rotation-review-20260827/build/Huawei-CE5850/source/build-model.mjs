import fs from 'node:fs';
import path from 'node:path';
import * as THREE from 'three';
import { Document, NodeIO } from '@gltf-transform/core';
import { KHRMaterialsUnlit } from '@gltf-transform/extensions';

const ROOT = '/root/Project/rack-device-3d/Huawei-CE5850';
const MM = 0.001;
const m = (value) => value * MM;

const BODY_W = 442.0;
const BODY_H = 43.6;
const OVERALL_D = 420.0;
const FACE_CLEARANCE = 0.2;
const SHELL_W = BODY_W - FACE_CLEARANCE * 2;
const SHELL_H = BODY_H - FACE_CLEARANCE * 2;
const SHELL_D = 412.0;
const OVERALL_W = 482.6;
const EAR_W = (OVERALL_W - BODY_W) / 2;

function material(document, name, rgba, metallic = 0, roughness = 0.72) {
  return document.createMaterial(name)
    .setBaseColorFactor(rgba)
    .setMetallicFactor(metallic)
    .setRoughnessFactor(roughness)
    .setDoubleSided(false);
}

function textureMaterial(document, unlitExtension, name, imagePath) {
  const texture = document.createTexture(`${name} texture`)
    .setImage(fs.readFileSync(imagePath))
    .setMimeType('image/png');
  const result = document.createMaterial(name)
    .setBaseColorFactor([1, 1, 1, 1])
    .setBaseColorTexture(texture)
    .setMetallicFactor(0)
    .setRoughnessFactor(1)
    .setDoubleSided(false)
    .setAlphaMode('OPAQUE');
  result.setExtension('KHR_materials_unlit', unlitExtension.createUnlit());
  return result;
}

function primitiveFromGeometry(document, buffer, geometry, mat) {
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
    const indices = Array.from({ length: position.count }, (_, index) => index);
    indexArray = position.count > 65535 ? new Uint32Array(indices) : new Uint16Array(indices);
  }
  primitive.setIndices(document.createAccessor()
    .setType('SCALAR').setArray(indexArray).setBuffer(buffer));
  primitive.setMaterial(mat);
  return primitive;
}

function nodeWithGeometry(context, name, geometry, mat, centerMM = [0, 0, 0], rotation = [0, 0, 0], parent = null) {
  const mesh = context.document.createMesh(`${name} mesh`)
    .addPrimitive(primitiveFromGeometry(context.document, context.buffer, geometry, mat));
  const node = context.document.createNode(name)
    .setMesh(mesh)
    .setTranslation(centerMM.map(m));
  if (rotation.some((value) => Math.abs(value) > 1e-12)) {
    const quaternion = new THREE.Quaternion().setFromEuler(new THREE.Euler(...rotation, 'XYZ'));
    node.setRotation([quaternion.x, quaternion.y, quaternion.z, quaternion.w]);
  }
  (parent || context.assembly).addChild(node);
  return node;
}

function emptyNode(context, name, extras = null) {
  const node = context.document.createNode(name);
  if (extras) node.setExtras(extras);
  context.assembly.addChild(node);
  return node;
}

function addBox(context, name, sizeMM, centerMM, mat, parent = null, rounded = 0) {
  const [w, h, d] = sizeMM.map(m);
  const geometry = rounded > 0
    ? new THREE.BoxGeometry(w, h, d, 1, 1, 1)
    : new THREE.BoxGeometry(w, h, d);
  return nodeWithGeometry(context, name, geometry, mat, centerMM, [0, 0, 0], parent);
}

function addCylinder(context, name, radiusMM, depthMM, centerMM, mat, rotation, parent = null, segments = 24) {
  const geometry = new THREE.CylinderGeometry(m(radiusMM), m(radiusMM), m(depthMM), segments, 1, false);
  return nodeWithGeometry(context, name, geometry, mat, centerMM, rotation, parent);
}

function addQuad(context, name, positionsMM, uvs, indices, mat) {
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(positionsMM.map(m), 3));
  geometry.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  return nodeWithGeometry(context, name, geometry, mat);
}

function addFaceQuads(context, faces) {
  const x0 = -BODY_W / 2, x1 = BODY_W / 2;
  const y0 = -BODY_H / 2, y1 = BODY_H / 2;
  const z0 = -OVERALL_D / 2, z1 = OVERALL_D / 2;
  const rearFaceZ = -208.0, frontFaceZ = 208.0;
  const uv = [0, 0, 0, 1, 1, 1, 1, 0];
  const uvHorizontal = [0, 0, 1, 0, 1, 1, 0, 1];

  addQuad(context, 'Front exact source-locked port-side face', [
    x0, y1, frontFaceZ, x0, y0, frontFaceZ, x1, y0, frontFaceZ, x1, y1, frontFaceZ
  ], uv, [0, 1, 2, 0, 2, 3], faces.front);

  addQuad(context, 'Rear exact source-locked power-side face', [
    x1, y1, rearFaceZ, x1, y0, rearFaceZ, x0, y0, rearFaceZ, x0, y1, rearFaceZ
  ], uv, [0, 1, 2, 0, 2, 3], faces.rear);

  addQuad(context, 'Right distinct reconstructed face', [
    x1, y1, z0, x1, y1, z1, x1, y0, z1, x1, y0, z0
  ], uvHorizontal, [0, 1, 2, 0, 2, 3], faces.right);

  addQuad(context, 'Left distinct reconstructed face', [
    x0, y1, z1, x0, y1, z0, x0, y0, z0, x0, y0, z1
  ], uvHorizontal, [0, 1, 2, 0, 2, 3], faces.left);

  addQuad(context, 'Top reconstructed cover face', [
    x0, y1, z0, x0, y1, z1, x1, y1, z1, x1, y1, z0
  ], uv, [0, 1, 2, 0, 2, 3], faces.top);

  addQuad(context, 'Bottom GENERIC_BOTTOM_FALLBACK face', [
    x0, y0, z1, x0, y0, z0, x1, y0, z0, x1, y0, z1
  ], uv, [0, 1, 2, 0, 2, 3], faces.bottom);
}

function addRackEars(context, mat) {
  for (const side of [-1, 1]) {
    const shape = new THREE.Shape();
    const width = m(EAR_W);
    const height = m(BODY_H);
    shape.moveTo(-width / 2, -height / 2);
    shape.lineTo(width / 2, -height / 2);
    shape.lineTo(width / 2, height / 2);
    shape.lineTo(-width / 2, height / 2);
    shape.closePath();
    for (const yMM of [-13.0, 13.0]) {
      const hole = new THREE.Path();
      hole.absellipse(0, m(yMM), m(6.2), m(3.6), 0, Math.PI * 2, false, 0);
      shape.holes.push(hole);
    }
    const geometry = new THREE.ExtrudeGeometry(shape, {
      depth: m(2.2), bevelEnabled: false, steps: 1, curveSegments: 28
    });
    geometry.translate(0, 0, -m(1.1));
    nodeWithGeometry(
      context,
      side < 0 ? 'RackEarLeft exact separate part with two openings' : 'RackEarRight exact separate part with two openings',
      geometry,
      mat,
      [side * (BODY_W / 2 + EAR_W / 2), 0, 208.8]
    );
  }
}

function addFrontPortGeometry(context, mats) {
  const root = emptyNode(context, 'Front port assembly 48T4S2Q-EI', {
    geRj45Count: 48,
    sfpPlusCount: 4,
    qsfpPlusCount: 2,
    breakoutIndicators: 0
  });
  const blockCenters = [-158.0, -65.5, 27.5, 119.5];
  for (let block = 0; block < 4; block++) {
    const blockNode = context.document.createNode(`RJ45 block ${block + 1} (12 ports)`);
    root.addChild(blockNode);
    for (let row = 0; row < 2; row++) {
      for (let column = 0; column < 6; column++) {
        const index = block * 12 + column * 2 + row + 1;
        const x = blockCenters[block] + (column - 2.5) * 13.6;
        const y = row === 0 ? 9.4 : -9.4;
        addBox(context, `GE RJ45 ${index} raised cage rim`, [12.5, 12.0, 2.0], [x, y, 208.2], mats.silver, blockNode);
        addBox(context, `GE RJ45 ${index} recessed dark cavity`, [10.1, 8.4, 2.1], [x, y, 208.95], mats.black, blockNode);
      }
    }
  }

  const sfpRoot = context.document.createNode('Four 10GE SFP+ cages');
  root.addChild(sfpRoot);
  let sfpIndex = 1;
  for (const y of [8.2, -8.2]) {
    for (const x of [176.2, 188.1]) {
      addBox(context, `10GE SFP+ ${sfpIndex} cage`, [10.5, 9.4, 2.0], [x, y, 209.0], mats.black, sfpRoot);
      sfpIndex++;
    }
  }

  const qsfpRoot = context.document.createNode('Two 40GE QSFP+ cages EI no breakout lamps');
  root.addChild(qsfpRoot);
  for (const [index, y] of [[1, 8.2], [2, -8.2]]) {
    addBox(context, `40GE QSFP+ ${index} cage`, [15.2, 10.5, 2.0], [208.6, y, 209.0], mats.black, qsfpRoot);
  }

  const status = context.document.createNode('Front Huawei status and MODE-ID controls');
  root.addChild(status);
  for (const [index, y] of [12, 6, 0, -6, -12].entries()) {
    addCylinder(context, `Front status LED ${index + 1}`, 1.15, 1.1, [-209.5, y, 209.0], mats.led,
      [Math.PI / 2, 0, 0], status, 18);
  }
  addCylinder(context, 'Front MODE-ID push button', 3.0, 1.6, [-209.5, -16.5, 209.0], mats.dark,
    [Math.PI / 2, 0, 0], status, 28);
}

function addRearModuleFrame(context, parent, name, centerX, width, mats) {
  const z = -208.3;
  const depth = 3.4;
  addBox(context, `${name} upper depth frame`, [width, 1.3, depth], [centerX, 20.9, z], mats.dark, parent);
  addBox(context, `${name} lower depth frame`, [width, 1.3, depth], [centerX, -20.9, z], mats.dark, parent);
  addBox(context, `${name} left depth frame`, [1.3, 41.0, depth], [centerX - width / 2, 0, z], mats.dark, parent);
  addBox(context, `${name} right depth frame`, [1.3, 41.0, depth], [centerX + width / 2, 0, z], mats.dark, parent);
}

function addRearGeometry(context, mats) {
  const rear = emptyNode(context, 'Rear installed assembly dual AC dual FAN-40EA-F', {
    psuCount: 2,
    psuModel: 'PAC-150WA',
    fanModuleCount: 2,
    fanModel: 'FAN-40EA-F',
    airflow: 'power-side intake; port-side exhaust'
  });

  const psu1 = context.document.createNode('PWR1 PAC-150WA AC PSU'); rear.addChild(psu1);
  const fan1 = context.document.createNode('FAN1 FAN-40EA-F module'); rear.addChild(fan1);
  const management = context.document.createNode('Central Console ETH USB management area'); rear.addChild(management);
  const fan2 = context.document.createNode('FAN2 FAN-40EA-F module'); rear.addChild(fan2);
  const psu2 = context.document.createNode('PWR2 PAC-150WA AC PSU'); rear.addChild(psu2);

  addRearModuleFrame(context, psu1, 'PWR1', -169.5, 103.0, mats);
  addRearModuleFrame(context, fan1, 'FAN1', -67.5, 98.0, mats);
  addRearModuleFrame(context, management, 'Management', 0, 42.0, mats);
  addRearModuleFrame(context, fan2, 'FAN2', 69.5, 96.0, mats);
  addRearModuleFrame(context, psu2, 'PWR2', 170.0, 102.0, mats);

  addBox(context, 'PWR1 IEC C14 inlet recess', [25, 23, 2.8], [-147.0, 0, -208.6], mats.black, psu1, 0.5);
  addBox(context, 'PWR2 IEC C14 inlet recess', [25, 23, 2.8], [193.0, 0, -208.6], mats.black, psu2, 0.5);

  for (const [parent, center, tag] of [[fan1, -67.5, 'FAN1'], [fan2, 69.5, 'FAN2']]) {
    addBox(context, `${tag} honeycomb field A relief`, [39, 27, 2.0], [center - 22, 0, -208.8], mats.black, parent);
    addBox(context, `${tag} honeycomb field B relief`, [39, 27, 2.0], [center + 22, 0, -208.8], mats.black, parent);
  }

  for (const [parent, x, name] of [
    [psu1, -189.0, 'PWR1'], [fan1, -47.0, 'FAN1'], [fan2, 52.0, 'FAN2'], [psu2, 188.5, 'PWR2']
  ]) {
    addCylinder(context, `${name} chrome pull handle`, 1.55, 24.0, [x, 0, -208.4], mats.chrome,
      [0, 0, 0], parent, 24);
  }

  addBox(context, 'Console RJ45 recessed port', [14.0, 12.0, 2.8], [-8.5, 8.2, -208.6], mats.black, management);
  addBox(context, 'ETH management RJ45 recessed port', [14.0, 12.0, 2.8], [-8.5, -8.2, -208.6], mats.black, management);
  addBox(context, 'Vertical USB port recess', [5.0, 14.0, 2.8], [14.0, -1.0, -208.6], mats.usb, management);
  addBox(context, 'Pull-out serial label tab', [15.0, 2.0, 2.0], [0, -19.0, -209.0], mats.silver, management);
}

function addSideAndTopGeometry(context, mats) {
  const sides = emptyNode(context, 'Asymmetric side mechanical details');
  const sideData = [
    { label: 'Left', x: -221.5, rotation: [0, 0, Math.PI / 2] },
    { label: 'Right', x: 221.5, rotation: [0, 0, Math.PI / 2] }
  ];
  for (const side of sideData) {
    const sideNode = context.document.createNode(`${side.label} side attachment recesses`); sides.addChild(sideNode);
    for (const [endLabel, z, ys] of [
      ['port-side', 193, [12, 0, -12]],
      ['power-side', -193, [13, 4.3, -4.3, -13]]
    ]) {
      ys.forEach((y, index) => addCylinder(context, `${side.label} ${endLabel} recess ${index + 1}`,
        1.7, 1.2, [side.x, y, z], mats.black, side.rotation, sideNode, 18));
    }
  }
  addCylinder(context, 'Right-side grounding screw relief', 3.0, 1.4, [222.0, 0, -10], mats.chrome,
    [0, 0, Math.PI / 2], sides, 28);
  addBox(context, 'Top port-side perforated band relief', [438.0, 1.0, 18.0], [0, 21.3, 200.5], mats.vent, sides);
}

async function build(variant, outputName) {
  const document = new Document();
  const buffer = document.createBuffer('Embedded geometry buffer');
  const unlit = document.createExtension(KHRMaterialsUnlit).setRequired(false);
  const scene = document.createScene('Huawei CE5850 Scene');
  const assembly = document.createNode('Huawei CE5850-EI-B00 complete assembly').setExtras({
    manufacturer: 'Huawei Technologies Co., Ltd.',
    chassisPid: 'CE5850-48T4S2Q-EI',
    completeBundle: 'CE5850-EI-B00',
    partNumber: '02359104',
    uHeight: 1,
    dimensionsMM: [442.0, 43.6, 420.0],
    rackEnvelopeWidthMM: 482.6,
    installedPower: '2 x PAC-150WA AC',
    installedFans: '2 x FAN-40EA-F',
    airflow: 'power-side intake; port-side exhaust',
    portInventory: '48 x GE RJ45; 4 x 10GE SFP+; 2 x 40GE QSFP+',
    coordinateConvention: '+X device right from user front, +Y up, +Z user front/port side',
    bottomStatus: 'GENERIC_BOTTOM_FALLBACK',
    textureVariant: variant
  });
  scene.addChild(assembly);
  const context = { document, buffer, assembly };

  const textureDir = path.join(ROOT, 'qa', 'textures', variant);
  const faceMats = {};
  for (const face of ['front', 'rear', 'left', 'right', 'top', 'bottom']) {
    faceMats[face] = textureMaterial(document, unlit, `${face} source-locked unlit OPAQUE`, path.join(textureDir, `${face}.png`));
  }
  const mats = {
    shell: material(document, 'Dark gray closed chassis', [0.12, 0.13, 0.14, 1], 0.18, 0.72),
    dark: material(document, 'Dark painted module frame', [0.055, 0.06, 0.065, 1], 0.12, 0.78),
    black: material(document, 'Opaque black port and grille recess', [0.012, 0.014, 0.016, 1], 0, 0.9),
    silver: material(document, 'Port cage silver', [0.55, 0.54, 0.50, 1], 0.32, 0.55),
    chrome: material(document, 'Handle chrome', [0.78, 0.79, 0.78, 1], 0.72, 0.25),
    led: material(document, 'Status LED dark green', [0.08, 0.25, 0.11, 1], 0, 0.42),
    usb: material(document, 'USB dark slot', [0.03, 0.035, 0.04, 1], 0.15, 0.65),
    vent: material(document, 'Port-side top vent relief', [0.045, 0.05, 0.055, 1], 0.08, 0.82),
    ear: material(document, 'Separate rack ears black steel', [0.075, 0.08, 0.085, 1], 0.22, 0.7)
  };

  // Keep the closed shell just behind the exact face cards. Coplanar shell and
  // face surfaces z-fight in independent WebGL viewers at oblique cameras.
  // The cards retain the verified external 442.0 x 43.6 mm body envelope.
  addBox(context, 'Closed outward chassis shell', [SHELL_W, SHELL_H, SHELL_D], [0, 0, 0], mats.shell);
  addFaceQuads(context, faceMats);
  addRackEars(context, mats.ear);
  addFrontPortGeometry(context, mats);
  addRearGeometry(context, mats);
  addSideAndTopGeometry(context, mats);

  const io = new NodeIO().registerExtensions([KHRMaterialsUnlit]);
  await io.write(path.join(ROOT, 'model', outputName), document);
}

await build('standard', 'Huawei-CE5850-48T4S2Q-EI-B00.glb');
await build('web', 'Huawei-CE5850-48T4S2Q-EI-B00-web.glb');
