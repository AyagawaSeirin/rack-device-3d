import fs from 'node:fs';
import path from 'node:path';
import { Document, NodeIO } from '@gltf-transform/core';
import { KHRMaterialsUnlit } from '@gltf-transform/extensions';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const OUT_DIR = path.join(ROOT, 'model');

const D = {
  bodyW: 0.444,
  overallW: 0.4824,
  H: 0.0873,
  bodyD: 0.684,
  frontProjection: 0.018,
  rearProjection: 0.039,
};

const C = {
  black: [0.035, 0.038, 0.041, 1],
  dark: [0.075, 0.082, 0.088, 1],
  steel: [0.64, 0.67, 0.69, 1],
  lightSteel: [0.78, 0.80, 0.81, 1],
  silver: [0.72, 0.74, 0.75, 1],
  orange: [0.98, 0.31, 0.035, 1],
  blue: [0.08, 0.33, 0.72, 1],
  teal: [0.03, 0.38, 0.34, 1],
  green: [0.08, 0.42, 0.30, 1],
  white: [0.91, 0.92, 0.91, 1],
};

function normalOf(a, b, c) {
  const ab = [b[0] - a[0], b[1] - a[1], b[2] - a[2]];
  const ac = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
  const n = [
    ab[1] * ac[2] - ab[2] * ac[1],
    ab[2] * ac[0] - ab[0] * ac[2],
    ab[0] * ac[1] - ab[1] * ac[0],
  ];
  const l = Math.hypot(...n) || 1;
  return n.map((v) => v / l);
}

function makeBuilder(textureDir) {
  const document = new Document();
  const buffer = document.createBuffer('embedded-buffer');
  const scene = document.createScene('Dell PowerEdge R730 8LFF');
  scene.setExtras({
    manufacturer: 'Dell',
    product: 'PowerEdge R730',
    variant: '8 x 3.5-inch LFF, bezel absent',
    power: 'dual 750W AC PSU',
    coordinateConvention: '+X device right, +Y up, +Z front',
    bottomEvidence: 'GENERIC_BOTTOM_FALLBACK',
  });

  const unlit = document.createExtension(KHRMaterialsUnlit);
  const materials = new Map();

  function colorMaterial(name, color, { roughness = 0.72, metallic = 0 } = {}) {
    if (materials.has(name)) return materials.get(name);
    const m = document.createMaterial(name)
      .setBaseColorFactor(color)
      .setMetallicFactor(metallic)
      .setRoughnessFactor(roughness)
      .setAlphaMode('OPAQUE')
      .setDoubleSided(false);
    materials.set(name, m);
    return m;
  }

  function textureMaterial(face) {
    const key = `photo-${face}`;
    if (materials.has(key)) return materials.get(key);
    const imagePath = path.join(textureDir, `${face}.png`);
    const texture = document.createTexture(`Dell-R730-${face}`)
      .setImage(fs.readFileSync(imagePath))
      .setMimeType('image/png');
    const m = document.createMaterial(key)
      .setBaseColorFactor([1, 1, 1, 1])
      .setBaseColorTexture(texture)
      .setMetallicFactor(0)
      .setRoughnessFactor(1)
      .setAlphaMode('OPAQUE')
      .setDoubleSided(false);
    m.setExtension('KHR_materials_unlit', unlit.createUnlit());
    m.getBaseColorTextureInfo()
      .setMagFilter(9729)
      .setMinFilter(9987)
      .setWrapS(33071)
      .setWrapT(33071);
    materials.set(key, m);
    return m;
  }

  const steel = colorMaterial('galvanized-steel', C.steel, { roughness: 0.8, metallic: 0.16 });
  const lightSteel = colorMaterial('light-galvanized-steel', C.lightSteel, { roughness: 0.78, metallic: 0.12 });
  const silver = colorMaterial('brushed-silver', C.silver, { roughness: 0.62, metallic: 0.2 });
  const black = colorMaterial('black-molded-metal-and-plastic', C.black, { roughness: 0.8 });
  const dark = colorMaterial('connector-black', C.dark, { roughness: 0.85 });
  const orange = colorMaterial('psu-release-orange', C.orange, { roughness: 0.65 });
  const blue = colorMaterial('dell-release-blue', C.blue, { roughness: 0.65 });
  const teal = colorMaterial('serial-teal', C.teal, { roughness: 0.7 });
  const green = colorMaterial('mounting-stud-green-zinc', C.green, { roughness: 0.58, metallic: 0.22 });
  const white = colorMaterial('fan-hub-label', C.white, { roughness: 0.85 });

  function accessor(name, type, array, ctor = Float32Array) {
    return document.createAccessor(name)
      .setType(type)
      .setArray(new ctor(array))
      .setBuffer(buffer);
  }

  function addPrimitive(name, positions, normals, uvs, indices, material) {
    const primitive = document.createPrimitive()
      .setAttribute('POSITION', accessor(`${name}-POSITION`, 'VEC3', positions))
      .setAttribute('NORMAL', accessor(`${name}-NORMAL`, 'VEC3', normals))
      .setIndices(accessor(`${name}-INDICES`, 'SCALAR', indices, Uint32Array))
      .setMaterial(material);
    if (uvs) primitive.setAttribute('TEXCOORD_0', accessor(`${name}-TEXCOORD_0`, 'VEC2', uvs));
    const mesh = document.createMesh(name).addPrimitive(primitive);
    const node = document.createNode(name).setMesh(mesh);
    scene.addChild(node);
    return node;
  }

  function addQuad(name, verts, material, uvRect = [0, 0, 1, 1]) {
    const n = normalOf(verts[0], verts[1], verts[2]);
    const [u0, v0, u1, v1] = uvRect;
    const positions = verts.flat();
    const normals = [...n, ...n, ...n, ...n];
    const uvs = [u0, v1, u1, v1, u1, v0, u0, v0];
    return addPrimitive(name, positions, normals, uvs, [0, 1, 2, 0, 2, 3], material);
  }

  function addBox(name, center, size, material, rotZ = 0) {
    const [cx, cy, cz] = center;
    const [sx, sy, sz] = size;
    const hx = sx / 2, hy = sy / 2, hz = sz / 2;
    const rawFaces = [
      [[-hx,-hy, hz],[ hx,-hy, hz],[ hx, hy, hz],[-hx, hy, hz]],
      [[ hx,-hy,-hz],[-hx,-hy,-hz],[-hx, hy,-hz],[ hx, hy,-hz]],
      [[ hx,-hy, hz],[ hx,-hy,-hz],[ hx, hy,-hz],[ hx, hy, hz]],
      [[-hx,-hy,-hz],[-hx,-hy, hz],[-hx, hy, hz],[-hx, hy,-hz]],
      [[-hx, hy, hz],[ hx, hy, hz],[ hx, hy,-hz],[-hx, hy,-hz]],
      [[-hx,-hy,-hz],[ hx,-hy,-hz],[ hx,-hy, hz],[-hx,-hy, hz]],
    ];
    const positions = [], normals = [], uvs = [], indices = [];
    const cs = Math.cos(rotZ), sn = Math.sin(rotZ);
    const tx = (p) => [cx + p[0] * cs - p[1] * sn, cy + p[0] * sn + p[1] * cs, cz + p[2]];
    rawFaces.forEach((face, fi) => {
      const vs = face.map(tx);
      const n = normalOf(vs[0], vs[1], vs[2]);
      const base = positions.length / 3;
      positions.push(...vs.flat());
      normals.push(...n, ...n, ...n, ...n);
      uvs.push(0,1, 1,1, 1,0, 0,0);
      indices.push(base, base+1, base+2, base, base+2, base+3);
    });
    return addPrimitive(name, positions, normals, uvs, indices, material);
  }

  function addWatertightCore(name, center, size, material) {
    const [cx, cy, cz] = center;
    const [sx, sy, sz] = size;
    const hx = sx / 2, hy = sy / 2, hz = sz / 2;
    const positions = [
      cx-hx,cy-hy,cz-hz, cx+hx,cy-hy,cz-hz,
      cx+hx,cy+hy,cz-hz, cx-hx,cy+hy,cz-hz,
      cx-hx,cy-hy,cz+hz, cx+hx,cy-hy,cz+hz,
      cx+hx,cy+hy,cz+hz, cx-hx,cy+hy,cz+hz,
    ];
    const q = 1 / Math.sqrt(3);
    const normals = [
      -q,-q,-q, q,-q,-q, q,q,-q, -q,q,-q,
      -q,-q,q, q,-q,q, q,q,q, -q,q,q,
    ];
    const indices = [
      0,3,2, 0,2,1, 4,5,6, 4,6,7,
      0,4,7, 0,7,3, 1,2,6, 1,6,5,
      0,1,5, 0,5,4, 3,7,6, 3,6,2,
    ];
    return addPrimitive(name, positions, normals, null, indices, material);
  }

  function addCylinder(name, center, radius, length, axis, segments, material) {
    const [cx, cy, cz] = center;
    const positions = [], normals = [], uvs = [], indices = [];
    const p = (a, axial) => {
      const c = Math.cos(a) * radius, s = Math.sin(a) * radius;
      if (axis === 'x') return [cx + axial, cy + c, cz + s];
      if (axis === 'y') return [cx + c, cy + axial, cz + s];
      return [cx + c, cy + s, cz + axial];
    };
    const n = (a) => {
      const c = Math.cos(a), s = Math.sin(a);
      if (axis === 'x') return [0, c, s];
      if (axis === 'y') return [c, 0, s];
      return [c, s, 0];
    };
    for (let i = 0; i <= segments; i++) {
      const a = i / segments * Math.PI * 2;
      positions.push(...p(a, -length/2), ...p(a, length/2));
      normals.push(...n(a), ...n(a));
      uvs.push(i/segments, 1, i/segments, 0);
    }
    for (let i = 0; i < segments; i++) {
      const b = i * 2;
      indices.push(b, b+3, b+1, b, b+2, b+3);
    }
    for (const side of [-1, 1]) {
      const centerIndex = positions.length / 3;
      const centerPos = axis === 'x' ? [cx + side*length/2,cy,cz] : axis === 'y' ? [cx,cy + side*length/2,cz] : [cx,cy,cz + side*length/2];
      const capNormal = axis === 'x' ? [side,0,0] : axis === 'y' ? [0,side,0] : [0,0,side];
      positions.push(...centerPos); normals.push(...capNormal); uvs.push(0.5,0.5);
      const start = positions.length / 3;
      for (let i = 0; i <= segments; i++) {
        const a = i / segments * Math.PI * 2;
        positions.push(...p(a, side*length/2)); normals.push(...capNormal); uvs.push(0.5+0.5*Math.cos(a),0.5+0.5*Math.sin(a));
      }
      for (let i = 0; i < segments; i++) {
        if (side > 0) indices.push(centerIndex, start+i, start+i+1);
        else indices.push(centerIndex, start+i+1, start+i);
      }
    }
    return addPrimitive(name, positions, normals, uvs, indices, material);
  }

  function frontRect(name, cx, cy, w, h, z, uvRect, material = textureMaterial('front')) {
    return addQuad(name, [[cx-w/2,cy-h/2,z],[cx+w/2,cy-h/2,z],[cx+w/2,cy+h/2,z],[cx-w/2,cy+h/2,z]], material, uvRect);
  }
  function rearRect(name, cx, cy, w, h, z, uvRect, material = textureMaterial('rear')) {
    return addQuad(name, [[cx+w/2,cy-h/2,z],[cx-w/2,cy-h/2,z],[cx-w/2,cy+h/2,z],[cx+w/2,cy+h/2,z]], material, uvRect);
  }
  const uv = (x0,y0,x1,y1,W,H) => [x0/W,y0/H,x1/W,y1/H];

  // Closed body and six canonical photo-locked surfaces.
  addBox('closed-chassis-body', [0,0,0], [D.bodyW-0.0008,D.H-0.003,D.bodyD-0.0008], steel);
  addQuad('front-photo-surface', [[-D.overallW/2,-D.H/2,0.3424],[D.overallW/2,-D.H/2,0.3424],[D.overallW/2,D.H/2,0.3424],[-D.overallW/2,D.H/2,0.3424]], textureMaterial('front'));
  addQuad('rear-photo-surface', [[D.bodyW/2,-D.H/2,-0.34225],[-D.bodyW/2,-D.H/2,-0.34225],[-D.bodyW/2,D.H/2,-0.34225],[D.bodyW/2,D.H/2,-0.34225]], textureMaterial('rear'));
  const sideCardX = D.bodyW/2;
  addQuad('right-photo-surface', [[sideCardX,-D.H/2,D.bodyD/2],[sideCardX,-D.H/2,-D.bodyD/2],[sideCardX,D.H/2,-D.bodyD/2],[sideCardX,D.H/2,D.bodyD/2]], textureMaterial('right'));
  addQuad('left-photo-surface', [[-sideCardX,-D.H/2,-D.bodyD/2],[-sideCardX,-D.H/2,D.bodyD/2],[-sideCardX,D.H/2,D.bodyD/2],[-sideCardX,D.H/2,-D.bodyD/2]], textureMaterial('left'));
  const topPhotoY = D.H/2 - 0.00080;
  addQuad('top-photo-surface', [[-D.bodyW/2,topPhotoY,D.bodyD/2],[D.bodyW/2,topPhotoY,D.bodyD/2],[D.bodyW/2,topPhotoY,-D.bodyD/2],[-D.bodyW/2,topPhotoY,-D.bodyD/2]], textureMaterial('top'));
  addQuad('bottom-photo-surface', [[-D.bodyW/2,-D.H/2,-D.bodyD/2],[D.bodyW/2,-D.H/2,-D.bodyD/2],[D.bodyW/2,-D.H/2,D.bodyD/2],[-D.bodyW/2,-D.H/2,D.bodyD/2]], textureMaterial('bottom'));

  // Separate front-only rack ears and latches; no rear ears.
  const earW = (D.overallW-D.bodyW)/2;
  for (const s of [-1,1]) {
    addBox(`front-${s<0?'left':'right'}-rack-ear`, [s*(D.bodyW/2+earW/2),0,0.3508], [earW,D.H,0.0176], black);
    addBox(`front-${s<0?'left':'right'}-ear-release`, [s*(D.bodyW/2+earW*0.52),-0.017,0.357], [earW*0.62,0.028,0.006], dark);
  }

  // Upper control, iDRAC Direct, ventilation and optical-drive relief.
  const upper = [
    ['front-control-branding-block',-0.14235,0.027,0.14130,0.030,uv(105,0,825,155,2400,434)],
    ['front-idrac-direct-usb-block',-0.04570,0.027,0.05200,0.030,uv(825,0,1090,155,2400,434)],
    ['front-upper-ventilation-block',0.02740,0.027,0.09420,0.030,uv(1090,0,1570,155,2400,434)],
    ['front-optical-drive',0.14375,0.027,0.13850,0.030,uv(1570,0,2275,155,2400,434)],
  ];
  for (const [name,cx,cy,w,h,texUV] of upper) {
    addBox(`${name}-depth`,[cx,cy,0.347],[w,h,0.009],black);
    frontRect(name,cx,cy,w,h,0.352,texUV);
  }

  // Eight distinct 3.5-inch carriers, their recesses, handles and latches.
  const colX = [-0.165,-0.055,0.055,0.165];
  const imgX = [[120,650],[650,1195],[1195,1740],[1740,2275]];
  const rows = [
    {y:-0.002, img:[150,288], key:'upper'},
    {y:-0.030, img:[286,434], key:'lower'},
  ];
  for (let r=0;r<2;r++) for (let c=0;c<4;c++) {
    const cx=colX[c], cy=rows[r].y, name=`front-lff-carrier-${r*4+c}`;
    addBox(`${name}-bay-recess`,[cx,cy,0.348],[0.103,0.0265,0.012],dark);
    frontRect(`${name}-photo-face`,cx,cy,0.101,0.0258,0.355,uv(imgX[c][0],rows[r].img[0],imgX[c][1],rows[r].img[1],2400,434));
    addBox(`${name}-swing-handle`,[cx+0.041,cy,0.3578],[0.012,0.023,0.0036],black);
    addBox(`${name}-silver-latch`,[cx+0.0373,cy+0.004,0.3585],[0.004,0.010,0.003],silver);
    addBox(`${name}-grille-relief`,[cx-0.012,cy,0.358],[0.054,0.016,0.004],dark);
  }

  // A shallow six-fan row behind the verified front airflow path.
  for (let i=0;i<6;i++) {
    const x=-0.145+i*0.058;
    addCylinder(`internal-fan-${i}`,[x,0.020,0.337],0.012,0.006,'z',18,dark);
    addCylinder(`internal-fan-orange-hub-${i}`,[x,0.020,0.341],0.0045,0.002,'z',18,orange);
  }

  // Rear PCIe blank relief frames: 3 half-height and 4 full-height slots.
  const frame = (name,cx,cy,w,h) => {
    const z=-0.3428, t=0.0005, d=0.0008;
    addBox(`${name}-top`,[cx,cy+h/2-t/2,z],[w-2*t,t,d],lightSteel);
    addBox(`${name}-bottom`,[cx,cy-h/2+t/2,z],[w-2*t,t,d],lightSteel);
    addBox(`${name}-left`,[cx-w/2+t/2,cy,z],[t,h,d],lightSteel);
    addBox(`${name}-right`,[cx+w/2-t/2,cy,z],[t,h,d],lightSteel);
  };
  for (let i=0;i<3;i++) frame(`rear-pcie-slot-${i+1}`,0.183,0.030-i*0.025,0.073,0.019);
  frame('rear-pcie-slot-4',0.063,0.027,0.125,0.021);
  frame('rear-pcie-slot-5',0.063,0.002,0.125,0.021);
  frame('rear-pcie-slot-6',-0.073,0.027,0.117,0.021);
  frame('rear-pcie-slot-7',-0.073,0.002,0.117,0.021);
  addBox('rear-slot-separator-blue-1',[0.127,0.015,-0.353],[0.004,0.041,0.007],blue);
  addBox('rear-slot-separator-blue-2',[-0.132,0.015,-0.353],[0.004,0.041,0.007],blue);

  // Rear carry/retention handle and mounts.
  addCylinder('rear-horizontal-retention-handle',[0.044,-0.008,-0.349],0.0030,0.160,'x',20,black);
  addBox('rear-handle-left-mount',[0.124,-0.008,-0.347],[0.006,0.016,0.008],black);
  addBox('rear-handle-right-mount',[-0.036,-0.008,-0.347],[0.006,0.016,0.008],black);

  // Rear I/O port groups, independently recessed and source-textured.
  const rearPorts = [
    ['rear-idrac8-enterprise',0.184,-0.030,0.042,0.020,uv(100,340,310,470,2400,472),dark],
    ['rear-db9-serial',0.136,-0.030,0.043,0.020,uv(310,340,475,470,2400,472),teal],
    ['rear-vga',0.090,-0.030,0.043,0.020,uv(475,340,680,470,2400,472),blue],
    ['rear-two-usb3',0.051,-0.030,0.027,0.020,uv(680,340,810,470,2400,472),dark],
    ['rear-four-rj45-ndc',-0.020,-0.030,0.102,0.020,uv(810,340,1290,470,2400,472),dark],
  ];
  for (const [name,cx,cy,w,h,texUV,sideMat] of rearPorts) {
    addBox(`${name}-recess`,[cx,cy,-0.349],[w,h,0.011],sideMat);
    rearRect(`${name}-photo-face`,cx,cy,w,h,-0.355,texUV);
  }

  // Two exact hot-swap 750W AC PSU blocks, AC inlets, fans, release tabs and handles.
  const psus = [
    {i:1,cx:-0.112,uv:uv(1380,235,1905,472,2400,472)},
    {i:2,cx:-0.193,uv:uv(1905,235,2400,472,2400,472)},
  ];
  for (const p of psus) {
    addBox(`rear-psu-${p.i}-module`,[p.cx,-0.022,-0.359],[0.076,0.043,0.034],silver);
    // The source photo is a backing layer; mechanical fan, inlet, guards and
    // handles must sit outward of it instead of being hidden behind an opaque
    // card.  Preserve the authoritative -0.381 m envelope with the handles.
    rearRect(`rear-psu-${p.i}-photo-face`,p.cx,-0.022,0.075,0.042,-0.3764,p.uv);
    const inletX=p.cx+0.018, fanX=p.cx-0.018;
    addBox(`rear-psu-${p.i}-iec-c14-inlet`,[inletX,-0.020,-0.3785],[0.026,0.028,0.003],black);
    addBox(`rear-psu-${p.i}-orange-release`,[inletX+0.017,-0.020,-0.3785],[0.005,0.025,0.003],orange);
    addCylinder(`rear-psu-${p.i}-axial-fan`,[fanX,-0.020,-0.3779],0.018,0.003,'z',24,black);
    addCylinder(`rear-psu-${p.i}-750w-hub`,[fanX,-0.020,-0.3791],0.007,0.0014,'z',24,white);
    addBox(`rear-psu-${p.i}-fan-guard-a`,[fanX,-0.020,-0.3796],[0.041,0.0022,0.0012],silver,Math.PI/4);
    addBox(`rear-psu-${p.i}-fan-guard-b`,[fanX,-0.020,-0.3800],[0.041,0.0022,0.0012],silver,-Math.PI/4);
    addBox(`rear-psu-${p.i}-handle-left`,[p.cx+0.004,-0.020,-0.3789],[0.004,0.035,0.0042],silver);
    addBox(`rear-psu-${p.i}-handle-right`,[p.cx-0.005,-0.020,-0.3789],[0.004,0.035,0.0042],silver);
    addBox(`rear-psu-${p.i}-handle-crossbar`,[p.cx-0.0005,0.000,-0.3789],[0.013,0.004,0.0042],silver);
  }

  // The photo card carries the flush factory labels.  Verified raised relief
  // sits above the card but stays inside the official 87.3 mm height envelope.
  addBox('top-long-stamped-rib',[0,0.04335,0.170],[0.330,0.0006,0.007],lightSteel);
  addBox('top-cover-latch-pocket',[0.000,0.04320,0.040],[0.033,0.0003,0.055],black);
  addBox('top-cover-latch-lever',[0.000,0.04350,0.040],[0.020,0.0003,0.038],dark);

  // Side-cover lips; three right-side green-zinc rail mounting studs only.
  addBox('left-upper-cover-lip',[-(D.bodyW/2+0.0004),0.034,0],[0.0008,0.010,D.bodyD-0.018],lightSteel);
  addBox('right-upper-cover-lip',[D.bodyW/2+0.0004,0.034,0],[0.0008,0.010,D.bodyD-0.018],lightSteel);
  // Centers measured from the independent right-face source (2400 px wide):
  // x = 866, 1356, 2012 -> z = +0.095, -0.044, -0.231 m.
  for (const [i,z] of [0.095,-0.044,-0.231].entries()) {
    addCylinder(`right-green-rail-stud-${i+1}`,[D.bodyW/2+0.0018,-0.013,z],0.0032,0.0024,'x',18,green);
    addCylinder(`right-stud-washer-${i+1}`,[D.bodyW/2+0.0005,-0.013,z],0.0043,0.0012,'x',18,silver);
  }

  return document;
}

async function build(textureKind, outputName) {
  const textureDir = path.join(OUT_DIR, `textures-${textureKind}`);
  const document = makeBuilder(textureDir);
  const io = new NodeIO().registerExtensions([KHRMaterialsUnlit]);
  await io.write(path.join(OUT_DIR, outputName), document);
}

await build('standard', 'Dell-R730-3.5inch.glb');
await build('web', 'Dell-R730-3.5inch-web.glb');
console.log('Built standard and web GLBs.');
