import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import * as THREE from '../../qa/viewer/node_modules/three/build/three.module.js';
import { GLTFExporter } from '../../qa/viewer/node_modules/three/examples/jsm/exporters/GLTFExporter.js';
import { NodeIO } from '../../qa/viewer/node_modules/@gltf-transform/core/dist/index.js';
import { KHRMaterialsUnlit } from '../../qa/viewer/node_modules/@gltf-transform/extensions/dist/index.js';

// FileReader is used by THREE's exporter, but is not provided by Node.js.
if (!globalThis.FileReader) {
  globalThis.FileReader = class FileReader {
    readAsArrayBuffer(blob) {
      blob.arrayBuffer().then((value) => {
        this.result = value;
        this.onloadend?.();
      });
    }

    readAsDataURL(blob) {
      blob.arrayBuffer().then((value) => {
        this.result = `data:${blob.type};base64,${Buffer.from(value).toString('base64')}`;
        this.onloadend?.();
      });
    }
  };
}

const __filename = fileURLToPath(import.meta.url);
const sourceDir = path.dirname(__filename);
const modelDir = path.resolve(sourceDir, '..');
const projectDir = path.resolve(modelDir, '..');
const qaDir = path.join(projectDir, 'qa');

const DIM = Object.freeze({ width: 438, height: 89, depth: 554 });
const X = DIM.width / 2;
const Y = DIM.height / 2;
const Z = DIM.depth / 2;
const FRONT_TEXTURE_Z = 275.35;
const REAR_TEXTURE_Z = -275.35;
const FRONT_RELIEF_Z = 276.28;
const REAR_RELIEF_Z = -276.28;

const scene = new THREE.Scene();
scene.name = 'Fortinet_FortiGate_FG1500D_2U_AC';
scene.userData = {
  manufacturer: 'Fortinet, Inc.',
  productId: 'FortiGate FG-1500D',
  generation: 'D',
  rackHeight: '2U',
  power: 'dual hot-swappable AC',
  dimensionsMm: [DIM.width, DIM.height, DIM.depth],
  coordinateConvention: '+X device right, +Y up, +Z front',
  assemblySource: 'user-locked screenshot row 3',
  rearConflictDisclosure: 'User-locked four-fan/double-AC rear conflicts with the catalog Fortinet three-chassis-fan/left-PSU rear and is intentionally modeled as the delivery subject.',
  bottomMode: 'GENERIC_BOTTOM_FALLBACK',
  optional3D: 'Community 3D Warehouse USDZ preserved as non-official source only; no mesh reused.',
};

const appliance = new THREE.Group();
appliance.name = 'FG1500D_COMPLETE_APPLIANCE';
appliance.scale.setScalar(0.001); // millimetres -> glTF metres.
scene.add(appliance);

function makePBR(name, color, metallic = 0, roughness = 0.72) {
  const material = new THREE.MeshStandardMaterial({
    name,
    color,
    metalness: metallic,
    roughness,
    side: THREE.FrontSide,
  });
  return material;
}

function makeFaceMaterial(face) {
  return new THREE.MeshBasicMaterial({
    name: `face_${face}`,
    color: 0xffffff,
    side: THREE.FrontSide,
    transparent: false,
    depthWrite: true,
  });
}

const MAT = Object.freeze({
  shell: makePBR('shell_ivory_painted_steel', 0xe8e9e5, 0.05, 0.68),
  seam: makePBR('edge_seam_ivory', 0xd7d9d5, 0.08, 0.62),
  frame: makePBR('connector_frame_metal', 0xaeb4b4, 0.26, 0.47),
  grille: makePBR('fan_grille_metal', 0x777d7d, 0.42, 0.36),
  dark: makePBR('recess_dark', 0x111313, 0.02, 0.78),
  handle: makePBR('service_handle_black', 0x181a1a, 0.04, 0.58),
  screw: makePBR('fastener_steel', 0xb5b9b6, 0.52, 0.34),
  labelBack: makePBR('label_underlay', 0x9ea8ad, 0, 0.84),
  faces: Object.freeze({
    front: makeFaceMaterial('front'),
    rear: makeFaceMaterial('rear'),
    left: makeFaceMaterial('left'),
    right: makeFaceMaterial('right'),
    top: makeFaceMaterial('top'),
    bottom: makeFaceMaterial('bottom'),
  }),
});

function addBox(parent, name, size, position, material, rotation = [0, 0, 0]) {
  const geometry = new THREE.BoxGeometry(...size);
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = name;
  mesh.position.set(...position);
  mesh.rotation.set(...rotation);
  mesh.castShadow = false;
  mesh.receiveShadow = false;
  parent.add(mesh);
  return mesh;
}

function addCylinder(parent, name, radius, length, position, material, rotation = [0, 0, 0], segments = 20) {
  const geometry = new THREE.CylinderGeometry(radius, radius, length, segments, 1, false);
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = name;
  mesh.position.set(...position);
  mesh.rotation.set(...rotation);
  parent.add(mesh);
  return mesh;
}

function addFrameXY(parent, name, cx, cy, width, height, bar, depth, z, material) {
  const group = new THREE.Group();
  group.name = name;
  addBox(group, `${name}_top`, [width, bar, depth], [cx, cy + (height - bar) / 2, z], material);
  addBox(group, `${name}_bottom`, [width, bar, depth], [cx, cy - (height - bar) / 2, z], material);
  addBox(group, `${name}_left`, [bar, Math.max(bar, height - 2 * bar), depth], [cx - (width - bar) / 2, cy, z], material);
  addBox(group, `${name}_right`, [bar, Math.max(bar, height - 2 * bar), depth], [cx + (width - bar) / 2, cy, z], material);
  parent.add(group);
  return group;
}

function addUHandleRear(parent, name, cx, cy, height, outwardZ) {
  const group = new THREE.Group();
  group.name = name;
  const sign = Math.sign(outwardZ);
  addBox(group, `${name}_bar`, [5.6, height, 4.0], [cx, cy, outwardZ], MAT.handle);
  addBox(group, `${name}_top_mount`, [8.2, 4.0, 2.2], [cx, cy + height / 2 - 2, outwardZ - sign * 2.5], MAT.handle);
  addBox(group, `${name}_bottom_mount`, [8.2, 4.0, 2.2], [cx, cy - height / 2 + 2, outwardZ - sign * 2.5], MAT.handle);
  parent.add(group);
  return group;
}

function addRearScrew(parent, name, x, y) {
  const screw = addCylinder(parent, name, 1.05, 0.55, [x, y, -276.72], MAT.screw, [Math.PI / 2, 0, 0], 18);
  return screw;
}

function imagePxToWorldX(px, widthPx = 2560) {
  return (px / widthPx - 0.5) * DIM.width;
}

// A rear elevation is observed from -Z, so image-left maps to physical +X.
function rearImagePxToWorldX(px, widthPx = 2560) {
  return -imagePxToWorldX(px, widthPx);
}

function imagePxToWorldY(px, heightPx = 520) {
  return (0.5 - px / heightPx) * DIM.height;
}

function facePlaneGeometry(width, height) {
  const geometry = new THREE.PlaneGeometry(width, height);
  const uv = geometry.getAttribute('uv');
  for (let index = 0; index < uv.count; index += 1) {
    uv.setY(index, 1 - uv.getY(index));
  }
  uv.needsUpdate = true;
  return geometry;
}

// Closed base enclosure, inset behind the six canonical textured surfaces.
addBox(appliance, 'closed_outward_shell', [437.4, 88.4, 550.0], [0, 0, 0], MAT.shell);

// Canonical six face planes. UV orientation is explicit and contains no negative scale.
const front = new THREE.Mesh(facePlaneGeometry(DIM.width, DIM.height), MAT.faces.front);
front.name = 'CANONICAL_FRONT_TEXTURE';
front.position.set(0, 0, FRONT_TEXTURE_Z);
appliance.add(front);

const rear = new THREE.Mesh(facePlaneGeometry(DIM.width, DIM.height), MAT.faces.rear);
rear.name = 'CANONICAL_REAR_TEXTURE';
rear.position.set(0, 0, REAR_TEXTURE_Z);
rear.rotation.y = Math.PI;
appliance.add(rear);

const left = new THREE.Mesh(facePlaneGeometry(DIM.depth, DIM.height), MAT.faces.left);
left.name = 'CANONICAL_LEFT_TEXTURE';
left.position.set(-218.92, 0, 0);
left.rotation.y = -Math.PI / 2;
appliance.add(left);

const right = new THREE.Mesh(facePlaneGeometry(DIM.depth, DIM.height), MAT.faces.right);
right.name = 'CANONICAL_RIGHT_TEXTURE';
right.position.set(218.92, 0, 0);
right.rotation.y = Math.PI / 2;
appliance.add(right);

const top = new THREE.Mesh(facePlaneGeometry(DIM.width, DIM.depth), MAT.faces.top);
top.name = 'CANONICAL_TOP_TEXTURE';
top.position.set(0, 44.42, 0);
top.rotation.x = -Math.PI / 2;
appliance.add(top);

const bottom = new THREE.Mesh(facePlaneGeometry(DIM.width, DIM.depth), MAT.faces.bottom);
bottom.name = 'CANONICAL_BOTTOM_TEXTURE_GENERIC_FALLBACK';
bottom.position.set(0, -44.42, 0);
bottom.rotation.x = Math.PI / 2;
appliance.add(bottom);

// Chassis perimeter and cover seams, all kept inside the official W/H/D envelope.
const seams = new THREE.Group();
seams.name = 'CHASSIS_SEAMS_AND_EDGE_BREAKS';
addBox(seams, 'front_upper_edge', [437.6, 0.85, 1.4], [0, 43.92, 276.15], MAT.seam);
addBox(seams, 'front_lower_edge', [437.6, 0.85, 1.4], [0, -43.92, 276.15], MAT.seam);
addBox(seams, 'rear_upper_edge', [437.6, 0.85, 1.4], [0, 43.92, -276.15], MAT.seam);
addBox(seams, 'rear_lower_edge', [437.6, 0.85, 1.4], [0, -43.92, -276.15], MAT.seam);
addBox(seams, 'top_left_perimeter_seam', [0.55, 0.5, 550.5], [-218.70, 44.23, 0], MAT.seam);
addBox(seams, 'top_right_perimeter_seam', [0.55, 0.5, 550.5], [218.70, 44.23, 0], MAT.seam);
addBox(seams, 'top_front_perimeter_seam', [437.0, 0.5, 0.65], [0, 44.23, 275.7], MAT.seam);
addBox(seams, 'top_rear_perimeter_seam', [437.0, 0.5, 0.65], [0, 44.23, -275.7], MAT.seam);
appliance.add(seams);

// Front control area and forty identity-bearing network port frame reliefs.
const frontRelief = new THREE.Group();
frontRelief.name = 'FRONT_CONTROL_AND_40_PORT_RELIEF';
frontRelief.userData = {
  fixedCounts: {
    geSfp: 16,
    geRj45: 16,
    tenGeSfpPlus: 8,
    mgmtRj45: 2,
    statusIndicators: 4,
  },
};

const groups = [
  { name: 'GE_SFP_1_8', centers: [677, 761, 845, 929], kind: 'sfp', first: 1 },
  { name: 'GE_SFP_9_16', centers: [1028, 1114, 1200, 1286], kind: 'sfp', first: 9 },
  { name: 'GE_RJ45_17_24', centers: [1409, 1495, 1581, 1667], kind: 'rj45', first: 17 },
  { name: 'GE_RJ45_25_32', centers: [1767, 1853, 1939, 2025], kind: 'rj45', first: 25 },
  { name: '10GE_SFPPLUS_33_40', centers: [2158, 2244, 2330, 2416], kind: 'sfpplus', first: 33 },
];

for (const groupSpec of groups) {
  const portGroup = new THREE.Group();
  portGroup.name = groupSpec.name;
  const portWidth = groupSpec.kind === 'rj45' ? 13.8 : 13.0;
  const portHeight = groupSpec.kind === 'rj45' ? 13.4 : 12.5;
  groupSpec.centers.forEach((centerPx, col) => {
    [0, 1].forEach((row) => {
      const portNumber = groupSpec.first + col * 2 + row;
      const x = imagePxToWorldX(centerPx);
      const y = imagePxToWorldY(row === 0 ? 319 : 415);
      addFrameXY(
        portGroup,
        `PORT_${String(portNumber).padStart(2, '0')}_${groupSpec.kind.toUpperCase()}_RECESS_FRAME`,
        x,
        y,
        portWidth,
        portHeight,
        0.72,
        1.45,
        FRONT_RELIEF_Z,
        MAT.frame,
      );
    });
  });
  frontRelief.add(portGroup);
}

addFrameXY(frontRelief, 'CONSOLE_RJ45_USB_RECESSED_STACK', imagePxToWorldX(414), imagePxToWorldY(365), 15.2, 24.0, 0.85, 1.5, FRONT_RELIEF_Z, MAT.frame);
addFrameXY(frontRelief, 'MGMT1_MGMT2_RJ45_RECESSED_STACK', imagePxToWorldX(548), imagePxToWorldY(365), 15.4, 24.0, 0.85, 1.5, FRONT_RELIEF_Z, MAT.frame);
addFrameXY(frontRelief, 'USB_MINIB_MANAGEMENT_RECESS', imagePxToWorldX(226), imagePxToWorldY(422), 8.3, 4.8, 0.68, 1.3, FRONT_RELIEF_Z, MAT.frame);

['STATUS', 'ALARM', 'HA', 'POWER'].forEach((label, index) => {
  addCylinder(
    frontRelief,
    `LED_${label}`,
    0.8,
    0.45,
    [imagePxToWorldX(350), imagePxToWorldY(334 + index * 31), 276.78],
    index === 3 ? MAT.dark : MAT.frame,
    [Math.PI / 2, 0, 0],
    16,
  );
});

appliance.add(frontRelief);

// Rear user-locked four fan trays, service panel, segmented lower panels and dual AC PSUs.
const rearRelief = new THREE.Group();
rearRelief.name = 'USER_LOCKED_REAR_4FAN_DUAL_AC_RELIEF';
rearRelief.userData = {
  source: 'source/user-row/row3-rear-enlarged.png',
  conflict: 'Not the catalog Fortinet rear; see source/identity-manifest.md and source/evidence.md.',
};

const fanSpecs = [
  { centerPx: 344, leftPx: 150, rightPx: 548 },
  { centerPx: 776, leftPx: 581, rightPx: 970 },
  { centerPx: 1184, leftPx: 997, rightPx: 1374 },
  { centerPx: 1590, leftPx: 1398, rightPx: 1782 },
];

fanSpecs.forEach((spec, index) => {
  const cx = rearImagePxToWorldX(spec.centerPx);
  const cy = imagePxToWorldY(171);
  const trayWidth = (spec.rightPx - spec.leftPx) / 2560 * DIM.width;
  const trayHeight = 57.0;
  const tray = new THREE.Group();
  tray.name = `FAN_TRAY_${index + 1}`;
  addFrameXY(tray, `FAN_TRAY_${index + 1}_FRAME`, cx, cy, trayWidth, trayHeight, 1.05, 1.45, REAR_RELIEF_Z, MAT.seam);

  const fanCenterX = cx + 5.0;
  const fanCenterY = cy + 0.5;
  [9.4, 13.2, 17.0, 20.8].forEach((radius, ringIndex) => {
    const torus = new THREE.Mesh(new THREE.TorusGeometry(radius, 0.52, 8, 48), MAT.grille);
    torus.name = `FAN_${index + 1}_GRILLE_RING_${ringIndex + 1}`;
    torus.position.set(fanCenterX, fanCenterY, -276.82);
    rearRelief.add(torus);
  });

  for (let spoke = 0; spoke < 8; spoke += 1) {
    const bar = addBox(
      rearRelief,
      `FAN_${index + 1}_GRILLE_SPOKE_${spoke + 1}`,
      [42.0, 0.82, 0.62],
      [fanCenterX, fanCenterY, -276.82],
      MAT.grille,
      [0, 0, spoke * Math.PI / 4],
    );
    bar.renderOrder = 2;
  }

  addCylinder(rearRelief, `FAN_${index + 1}_HUB`, 3.6, 0.65, [fanCenterX, fanCenterY, -276.83], MAT.grille, [Math.PI / 2, 0, 0], 32);
  const handleX = rearImagePxToWorldX(spec.leftPx + 38);
  addUHandleRear(rearRelief, `FAN_TRAY_${index + 1}_PULL_HANDLE`, handleX, cy, 29.0, -276.74);

  const halfW = trayWidth / 2 - 4.0;
  const halfH = trayHeight / 2 - 4.0;
  addRearScrew(rearRelief, `FAN_TRAY_${index + 1}_SCREW_TL`, cx - halfW, cy + halfH);
  addRearScrew(rearRelief, `FAN_TRAY_${index + 1}_SCREW_TR`, cx + halfW, cy + halfH);
  addRearScrew(rearRelief, `FAN_TRAY_${index + 1}_SCREW_BL`, cx - halfW, cy - halfH);
  addRearScrew(rearRelief, `FAN_TRAY_${index + 1}_SCREW_BR`, cx + halfW, cy - halfH);
});

// Upper blank/service panel between fan bank and PSU bank.
const blankCx = rearImagePxToWorldX((1784 + 2101) / 2);
const blankCy = imagePxToWorldY(171);
addFrameXY(rearRelief, 'UPPER_BLANK_SERVICE_PANEL_FRAME', blankCx, blankCy, (2101 - 1784) / 2560 * DIM.width, 57.0, 0.9, 1.25, REAR_RELIEF_Z, MAT.seam);
addBox(rearRelief, 'UPPER_BLANK_SERVICE_PANEL_HORIZONTAL_SEAM', [(2101 - 1784) / 2560 * DIM.width - 3, 0.65, 0.7], [blankCx, blankCy, -276.73], MAT.seam);
addRearScrew(rearRelief, 'UPPER_BLANK_SERVICE_PANEL_SCREW_TL', rearImagePxToWorldX(1810), imagePxToWorldY(64));
addRearScrew(rearRelief, 'UPPER_BLANK_SERVICE_PANEL_SCREW_TR', rearImagePxToWorldX(2070), imagePxToWorldY(64));
addRearScrew(rearRelief, 'UPPER_BLANK_SERVICE_PANEL_SCREW_BL', rearImagePxToWorldX(1810), imagePxToWorldY(231));
addRearScrew(rearRelief, 'UPPER_BLANK_SERVICE_PANEL_SCREW_BR', rearImagePxToWorldX(2070), imagePxToWorldY(231));

// Lower segmented grille/service panels. Perforation stays in the locked texture;
// frames and seam depth are geometric.
const lowerPanels = [
  [150, 678, 'LOWER_GRILLE_PANEL_1'],
  [680, 1238, 'LOWER_GRILLE_PANEL_2'],
  [1240, 1704, 'LOWER_GRILLE_PANEL_3'],
  [1708, 2047, 'LOWER_GRILLE_PANEL_4'],
];
lowerPanels.forEach(([x0, x1, name], index) => {
  const cx = rearImagePxToWorldX((x0 + x1) / 2);
  const cy = imagePxToWorldY(429);
  const width = (x1 - x0) / 2560 * DIM.width;
  addFrameXY(rearRelief, name, cx, cy, width, 28.2, 0.82, 1.15, REAR_RELIEF_Z, MAT.seam);
  addRearScrew(rearRelief, `${name}_SCREW_LEFT`, rearImagePxToWorldX(x0 + 30), cy);
  addRearScrew(rearRelief, `${name}_SCREW_RIGHT`, rearImagePxToWorldX(x1 - 30), cy);
  if (index < 3) {
    addBox(rearRelief, `${name}_INSET_LIP`, [width - 7.0, 0.55, 0.7], [cx, cy + 10.7, -276.74], MAT.seam);
  }
});

// Two tall AC PSU modules at the rear far right.
const psuRanges = [[2113, 2264], [2267, 2428]];
psuRanges.forEach(([x0, x1], index) => {
  const cx = rearImagePxToWorldX((x0 + x1) / 2);
  const cy = imagePxToWorldY(216);
  const width = (x1 - x0) / 2560 * DIM.width;
  const height = 59.3;
  addFrameXY(rearRelief, `AC_PSU_${index + 1}_MODULE_FRAME`, cx, cy, width, height, 0.95, 1.45, REAR_RELIEF_Z, MAT.frame);
  addFrameXY(rearRelief, `AC_PSU_${index + 1}_IEC_C14_RECESS`, cx, imagePxToWorldY(242), width * 0.57, 16.8, 0.9, 1.55, REAR_RELIEF_Z - 0.05, MAT.dark);
  addUHandleRear(rearRelief, `AC_PSU_${index + 1}_PULL_HANDLE`, cx, imagePxToWorldY(383), 19.0, -276.84);
  addRearScrew(rearRelief, `AC_PSU_${index + 1}_SCREW_TL`, rearImagePxToWorldX(x0 + 18), imagePxToWorldY(31));
  addRearScrew(rearRelief, `AC_PSU_${index + 1}_SCREW_TR`, rearImagePxToWorldX(x1 - 18), imagePxToWorldY(31));
  addRearScrew(rearRelief, `AC_PSU_${index + 1}_SCREW_BL`, rearImagePxToWorldX(x0 + 18), imagePxToWorldY(423));
  addRearScrew(rearRelief, `AC_PSU_${index + 1}_SCREW_BR`, rearImagePxToWorldX(x1 - 18), imagePxToWorldY(423));
});

appliance.add(rearRelief);

// Non-mirrored side details: cover seams and sparse fasteners. Right label remains
// source-locked in the canonical texture and is not replaced with synthetic text.
const sideDetails = new THREE.Group();
sideDetails.name = 'NON_MIRRORED_SIDE_COVER_DETAILS';
addBox(sideDetails, 'LEFT_UPPER_COVER_SEAM', [0.42, 0.62, 536], [-218.98, 36.6, -1], MAT.seam);
addBox(sideDetails, 'RIGHT_UPPER_COVER_SEAM', [0.42, 0.62, 536], [218.98, 36.6, -1], MAT.seam);

[-246, -94, 118, 248].forEach((z, index) => {
  addCylinder(sideDetails, `LEFT_SIDE_UPPER_FASTENER_${index + 1}`, 0.9, 0.38, [-218.99, 38.0, z], MAT.screw, [0, 0, Math.PI / 2], 16);
});
[-242, -132, 54, 232].forEach((z, index) => {
  addCylinder(sideDetails, `RIGHT_SIDE_UPPER_FASTENER_${index + 1}`, 0.9, 0.38, [218.99, 38.0, z], MAT.screw, [0, 0, Math.PI / 2], 16);
});
[-235, -82, 104, 247].forEach((z, index) => {
  addCylinder(sideDetails, `LEFT_SIDE_LOWER_FASTENER_${index + 1}`, 0.85, 0.38, [-218.99, -36.8, z], MAT.screw, [0, 0, Math.PI / 2], 16);
});
[-226, -60, 126, 242].forEach((z, index) => {
  addCylinder(sideDetails, `RIGHT_SIDE_LOWER_FASTENER_${index + 1}`, 0.85, 0.38, [218.99, -36.8, z], MAT.screw, [0, 0, Math.PI / 2], 16);
});
appliance.add(sideDetails);

// A small asymmetric top fastener set proven by the oblique exact-model sources.
const topDetails = new THREE.Group();
topDetails.name = 'TOP_COVER_EDGE_FASTENERS';
[
  [-185, -248], [-48, -248], [130, -248], [188, -188],
  [-186, 236], [46, 236], [184, 236],
].forEach(([x, z], index) => {
  addCylinder(topDetails, `TOP_FASTENER_${index + 1}`, 0.85, 0.34, [x, 44.49, z], MAT.screw, [0, 0, 0], 16);
});
appliance.add(topDetails);

function sceneStats() {
  let meshes = 0;
  let primitives = 0;
  let triangles = 0;
  const names = [];
  scene.updateMatrixWorld(true);
  scene.traverse((object) => {
    if (!object.isMesh) return;
    meshes += 1;
    primitives += Array.isArray(object.material) ? object.material.length : 1;
    const indexCount = object.geometry.index?.count ?? 0;
    const positionCount = object.geometry.attributes.position?.count ?? 0;
    triangles += Math.floor((indexCount || positionCount) / 3);
    names.push(object.name);
  });
  return { meshes, primitives, triangles, meshNames: names };
}

async function exportBase() {
  const exporter = new GLTFExporter();
  const binary = await exporter.parseAsync(scene, {
    binary: true,
    onlyVisible: true,
    trs: false,
    truncateDrawRange: true,
  });
  const out = path.join(sourceDir, 'FG1500D-geometry-base.glb');
  fs.writeFileSync(out, Buffer.from(binary));
  return out;
}

async function attachTextures(basePath, variant) {
  const io = new NodeIO().registerExtensions([KHRMaterialsUnlit]);
  const document = await io.read(basePath);
  const root = document.getRoot();
  const unlitExtension = document.createExtension(KHRMaterialsUnlit);
  const textureDir = path.join(modelDir, variant === 'standard' ? 'textures-standard' : 'textures-web');
  const extension = variant === 'standard' ? 'png' : 'jpg';
  const mimeType = variant === 'standard' ? 'image/png' : 'image/jpeg';

  for (const faceName of ['front', 'rear', 'left', 'right', 'top', 'bottom']) {
    const material = root.listMaterials().find((item) => item.getName() === `face_${faceName}`);
    if (!material) throw new Error(`Missing material face_${faceName}`);
    const imagePath = path.join(textureDir, `${faceName}.${extension}`);
    const texture = document
      .createTexture(`${faceName}_${variant}_srgb`)
      .setImage(fs.readFileSync(imagePath))
      .setMimeType(mimeType);
    material
      .setBaseColorFactor([1, 1, 1, 1])
      .setBaseColorTexture(texture)
      .setMetallicFactor(0)
      .setRoughnessFactor(1)
      .setAlphaMode('OPAQUE')
      .setDoubleSided(false)
      .setExtension('KHR_materials_unlit', unlitExtension.createUnlit());
  }

  for (const material of root.listMaterials()) {
    material.setAlphaMode('OPAQUE').setDoubleSided(false);
  }

  const outputName = variant === 'standard' ? 'Fortinet-FG1500D.glb' : 'Fortinet-FG1500D-web.glb';
  const outputPath = path.join(modelDir, outputName);
  await io.write(outputPath, document);
  return outputPath;
}

fs.mkdirSync(sourceDir, { recursive: true });
fs.mkdirSync(qaDir, { recursive: true });

const basePath = await exportBase();
const standardPath = await attachTextures(basePath, 'standard');
const webPath = await attachTextures(basePath, 'web');
const stats = sceneStats();

const buildReport = {
  generatedAt: new Date().toISOString(),
  product: 'Fortinet FortiGate FG-1500D 2U AC',
  dimensionsMm: DIM,
  coordinateConvention: '+X device right, +Y up, +Z front',
  build: 'newly constructed visible exterior; optional USDZ mesh not reused',
  visibleGeometry: {
    closedShell: true,
    frontPortRecessFrames: 40,
    frontManagementAndControlFrames: 3,
    rearFanTrays: 4,
    rearFanGrilleRings: 16,
    rearFanGrilleSpokes: 32,
    rearFanHandles: 4,
    rearBlankServicePanel: 1,
    rearLowerPanels: 4,
    rearAcPsuModules: 2,
    rearAcPsuHandles: 2,
    sideConfiguration: 'non-mirrored; right regulatory label preserved in locked texture',
    topBranding: 'FORTINET wordmark preserved in locked top texture',
    bottom: 'conservative closed shell; GENERIC_BOTTOM_FALLBACK',
  },
  geometryStats: stats,
  files: {
    geometryBase: path.relative(projectDir, basePath),
    standardGlb: path.relative(projectDir, standardPath),
    webGlb: path.relative(projectDir, webPath),
  },
};

fs.writeFileSync(path.join(qaDir, 'build-report.json'), `${JSON.stringify(buildReport, null, 2)}\n`);

console.log(JSON.stringify({
  standardPath,
  webPath,
  standardBytes: fs.statSync(standardPath).size,
  webBytes: fs.statSync(webPath).size,
  meshes: stats.meshes,
  triangles: stats.triangles,
}, null, 2));
