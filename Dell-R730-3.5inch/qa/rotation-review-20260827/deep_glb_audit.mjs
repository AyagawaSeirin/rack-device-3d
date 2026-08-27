import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { NodeIO } from '@gltf-transform/core';
import { KHRMaterialsUnlit } from '@gltf-transform/extensions';

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  console.error('usage: node deep_glb_audit.mjs INPUT.glb OUTPUT.json');
  process.exit(2);
}

const io = new NodeIO().registerExtensions([KHRMaterialsUnlit]);
const document = await io.read(input);
const root = document.getRoot();

const EPS_DUPLICATE = 1e-7;
const EPS_COPLANAR = 1e-7;
const EPS_NEAR = 2e-4;
const EPS_OVERLAP = 1e-10;
const MAX_PAIR_DETAILS = 300;

function transformPoint(m, p) {
  return [
    m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
    m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
    m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14],
  ];
}

function determinant3(m) {
  return m[0] * (m[5] * m[10] - m[6] * m[9])
    - m[4] * (m[1] * m[10] - m[2] * m[9])
    + m[8] * (m[1] * m[6] - m[2] * m[5]);
}

function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
function cross(a, b) {
  return [
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0],
  ];
}
function length(v) { return Math.hypot(v[0], v[1], v[2]); }
function normalize(v) {
  const l = length(v);
  return l ? [v[0] / l, v[1] / l, v[2] / l] : [0, 0, 0];
}

function triangleKey(points) {
  const vertices = points.map((p) => p.map((v) => Math.round(v / EPS_DUPLICATE)).join(','));
  vertices.sort();
  return vertices.join('|');
}

function canonicalNormal(n) {
  const out = [...n];
  const first = out.find((v) => Math.abs(v) > 1e-8) || 1;
  if (first < 0) for (let i = 0; i < 3; i++) out[i] = -out[i];
  return out;
}

function transformNormal(m, n) {
  const a00 = m[0], a01 = m[4], a02 = m[8];
  const a10 = m[1], a11 = m[5], a12 = m[9];
  const a20 = m[2], a21 = m[6], a22 = m[10];
  const cofactor = [
    a11 * a22 - a12 * a21,
    a12 * a20 - a10 * a22,
    a10 * a21 - a11 * a20,
    a02 * a21 - a01 * a22,
    a00 * a22 - a02 * a20,
    a01 * a20 - a00 * a21,
    a01 * a12 - a02 * a11,
    a02 * a10 - a00 * a12,
    a00 * a11 - a01 * a10,
  ];
  return normalize([
    cofactor[0] * n[0] + cofactor[1] * n[1] + cofactor[2] * n[2],
    cofactor[3] * n[0] + cofactor[4] * n[1] + cofactor[5] * n[2],
    cofactor[6] * n[0] + cofactor[7] * n[1] + cofactor[8] * n[2],
  ]);
}

function overlap2D(a, b, dropAxis) {
  const axes = [0, 1, 2].filter((axis) => axis !== dropAxis);
  let area = 1;
  for (const axis of axes) {
    const lo = Math.max(a.min[axis], b.min[axis]);
    const hi = Math.min(a.max[axis], b.max[axis]);
    area *= Math.max(0, hi - lo);
  }
  return area;
}

function primitiveTriangles(node) {
  const mesh = node.getMesh();
  if (!mesh) return [];
  const matrix = node.getWorldMatrix();
  const result = [];
  for (const [primitiveIndex, primitive] of mesh.listPrimitives().entries()) {
    const position = primitive.getAttribute('POSITION');
    if (!position) continue;
    const positions = position.getArray();
    const normalAccessor = primitive.getAttribute('NORMAL');
    const vertexNormals = normalAccessor?.getArray() || null;
    const indexAccessor = primitive.getIndices();
    const indices = indexAccessor
      ? indexAccessor.getArray()
      : Array.from({ length: position.getCount() }, (_, i) => i);
    for (let i = 0; i + 2 < indices.length; i += 3) {
      const ids = [indices[i], indices[i + 1], indices[i + 2]];
      const points = ids.map((id) => transformPoint(matrix, [
        positions[id * 3], positions[id * 3 + 1], positions[id * 3 + 2],
      ]));
      const raw = cross(sub(points[1], points[0]), sub(points[2], points[0]));
      const area2 = length(raw);
      if (area2 < 1e-16) continue;
      const directionNormal = normalize(raw);
      const normal = canonicalNormal(directionNormal);
      const plane = dot(normal, points[0]);
      let attributeNormalDot = null;
      if (vertexNormals) {
        const average = [0, 0, 0];
        for (const id of ids) {
          const transformed = transformNormal(matrix, [
            vertexNormals[id * 3], vertexNormals[id * 3 + 1], vertexNormals[id * 3 + 2],
          ]);
          average[0] += transformed[0];
          average[1] += transformed[1];
          average[2] += transformed[2];
        }
        attributeNormalDot = dot(directionNormal, normalize(average));
      }
      const bounds = {
        min: [0, 1, 2].map((axis) => Math.min(...points.map((p) => p[axis]))),
        max: [0, 1, 2].map((axis) => Math.max(...points.map((p) => p[axis]))),
      };
      result.push({
        node: node.getName() || '(unnamed)',
        mesh: mesh.getName() || '(unnamed)',
        primitive: primitiveIndex,
        triangle: i / 3,
        points,
        directionNormal,
        normal,
        plane,
        attributeNormalDot,
        min: bounds.min,
        max: bounds.max,
        area: area2 / 2,
      });
    }
  }
  return result;
}

function edgeKey(a, b) {
  const qa = a.map((v) => Math.round(v / EPS_DUPLICATE)).join(',');
  const qb = b.map((v) => Math.round(v / EPS_DUPLICATE)).join(',');
  return qa < qb ? `${qa}|${qb}` : `${qb}|${qa}`;
}

function closedMeshAudit(node) {
  const triangles = primitiveTriangles(node);
  const edges = new Map();
  let signedVolume = 0;
  for (const tri of triangles) {
    for (const [a, b] of [[0, 1], [1, 2], [2, 0]]) {
      const key = edgeKey(tri.points[a], tri.points[b]);
      edges.set(key, (edges.get(key) || 0) + 1);
    }
    signedVolume += dot(tri.points[0], cross(tri.points[1], tri.points[2])) / 6;
  }
  const boundary = [...edges.values()].filter((count) => count === 1).length;
  const nonManifold = [...edges.values()].filter((count) => count > 2).length;
  return {
    node: node.getName(),
    triangle_count: triangles.length,
    edge_count: edges.size,
    boundary_edge_count: boundary,
    non_manifold_edge_count: nonManifold,
    signed_volume: signedVolume,
    watertight: triangles.length > 0 && boundary === 0 && nonManifold === 0,
    outward_signed_volume: signedVolume > 0,
  };
}

function identifyAlpha(bytes) {
  const result = spawnSync('identify', [
    '-format',
    '%m|%w|%h|%[channels]|%[fx:minima.a]|%[fx:maxima.a]',
    'png:-',
  ], { input: bytes, maxBuffer: 1024 * 1024 });
  if (result.status !== 0) return { error: result.stderr.toString().trim() || `identify exit ${result.status}` };
  const [format, width, height, channels, alphaMin, alphaMax] = result.stdout.toString().split('|');
  return {
    format,
    width: Number(width),
    height: Number(height),
    channels,
    alpha_min: Number(alphaMin),
    alpha_max: Number(alphaMax),
    contains_nonopaque_alpha: channels.includes('a') && Number(alphaMin) < 0.999999,
  };
}

const nodes = root.listNodes();
const nodeTransforms = nodes.map((node) => {
  const matrix = node.getWorldMatrix();
  return {
    name: node.getName() || '(unnamed)',
    determinant: determinant3(matrix),
    negative: determinant3(matrix) < 0,
    zero_or_singular: Math.abs(determinant3(matrix)) < 1e-14,
  };
});

const triangles = nodes.flatMap(primitiveTriangles);
const duplicateBuckets = new Map();
for (const tri of triangles) {
  const key = triangleKey(tri.points);
  if (!duplicateBuckets.has(key)) duplicateBuckets.set(key, []);
  duplicateBuckets.get(key).push(tri);
}
const duplicateGroups = [...duplicateBuckets.values()]
  .filter((group) => group.some((a, i) => group.some((b, j) => j > i && a.node !== b.node && dot(a.directionNormal, b.directionNormal) > 0.9999)))
  .map((group) => ({
    nodes: [...new Set(group.map((tri) => tri.node))],
    count: group.length,
    area: group[0].area,
  }));

const planeBuckets = new Map();
for (let i = 0; i < triangles.length; i++) {
  const tri = triangles[i];
  const nKey = tri.normal.map((v) => Math.round(v * 10000)).join(',');
  const pBin = Math.round(tri.plane / EPS_NEAR);
  const key = `${nKey}|${pBin}`;
  if (!planeBuckets.has(key)) planeBuckets.set(key, []);
  planeBuckets.get(key).push(i);
}

const exactPairs = [];
const nearPairs = [];
let exactPairCount = 0;
let nearPairCount = 0;
const seenPairs = new Set();
for (let i = 0; i < triangles.length; i++) {
  const a = triangles[i];
  const nKey = a.normal.map((v) => Math.round(v * 10000)).join(',');
  const pBin = Math.round(a.plane / EPS_NEAR);
  for (const bin of [pBin - 1, pBin, pBin + 1]) {
    for (const j of planeBuckets.get(`${nKey}|${bin}`) || []) {
      if (j <= i) continue;
      const b = triangles[j];
      if (a.node === b.node) continue;
      const pairKey = `${i}:${j}`;
      if (seenPairs.has(pairKey)) continue;
      seenPairs.add(pairKey);
      const planeDistance = Math.abs(a.plane - b.plane);
      if (planeDistance > EPS_NEAR) continue;
      if (dot(a.directionNormal, b.directionNormal) < 0.9999) continue;
      const dominant = a.normal.map(Math.abs).indexOf(Math.max(...a.normal.map(Math.abs)));
      const overlapArea = overlap2D(a, b, dominant);
      if (overlapArea <= EPS_OVERLAP) continue;
      const detail = {
        node_a: a.node,
        node_b: b.node,
        plane_m: a.plane,
        plane_distance_m: planeDistance,
        overlap_aabb_area_m2: overlapArea,
        normal: a.normal,
        direction_normal_a: a.directionNormal,
        direction_normal_b: b.directionNormal,
      };
      if (planeDistance <= EPS_COPLANAR) {
        exactPairCount++;
        if (exactPairs.length < MAX_PAIR_DETAILS) exactPairs.push(detail);
      } else {
        nearPairCount++;
        if (nearPairs.length < MAX_PAIR_DETAILS) nearPairs.push(detail);
      }
    }
  }
}

const materials = root.listMaterials().map((material) => {
  const texture = material.getBaseColorTexture();
  const image = texture?.getImage() || null;
  return {
    name: material.getName() || '(unnamed)',
    alpha_mode: material.getAlphaMode(),
    base_color_factor: material.getBaseColorFactor(),
    double_sided: material.getDoubleSided(),
    unlit: Boolean(material.getExtension('KHR_materials_unlit')),
    embedded_image: image ? identifyAlpha(image) : null,
  };
});
const primaryMaterials = materials.filter((material) => /^(photo-|Face_|Factory_DELL_EMC_Badge)/.test(material.name));
const primaryMaterialErrors = [];
for (const material of primaryMaterials) {
  if (material.alpha_mode !== 'OPAQUE') primaryMaterialErrors.push(`${material.name}: alphaMode=${material.alpha_mode}`);
  if (JSON.stringify(material.base_color_factor) !== JSON.stringify([1, 1, 1, 1])) primaryMaterialErrors.push(`${material.name}: non-neutral baseColorFactor`);
  if (material.double_sided) primaryMaterialErrors.push(`${material.name}: doubleSided=true`);
}

const closedCoreNodes = nodes.filter((node) => /closed.*(body|chassis)|(?:body|chassis).*closed/i.test(node.getName() || ''));
const closedCore = closedCoreNodes.map(closedMeshAudit);
const watertightMeshes = nodes.map(closedMeshAudit).filter((item) => item.watertight);
const normalAttributeMismatches = triangles.filter((tri) => tri.attributeNormalDot !== null && tri.attributeNormalDot < 0.5);

const result = {
  input,
  byte_size: fs.statSync(input).size,
  thresholds: {
    exact_duplicate_m: EPS_DUPLICATE,
    exact_coplanar_m: EPS_COPLANAR,
    near_coplanar_m: EPS_NEAR,
  },
  counts: {
    nodes: nodes.length,
    meshes: root.listMeshes().length,
    triangles_world_instances: triangles.length,
    duplicate_triangle_groups: duplicateGroups.length,
    exact_coplanar_triangle_pairs: exactPairCount,
    near_coplanar_triangle_pairs: nearPairCount,
    negative_transforms: nodeTransforms.filter((item) => item.negative).length,
    singular_transforms: nodeTransforms.filter((item) => item.zero_or_singular).length,
    blend_materials: materials.filter((item) => item.alpha_mode === 'BLEND').length,
    double_sided_materials: materials.filter((item) => item.double_sided).length,
    primary_material_errors: primaryMaterialErrors.length,
    closed_core_nodes: closedCore.length,
    closed_core_failures: closedCore.filter((item) => !item.watertight || !item.outward_signed_volume).length,
    watertight_mesh_instances: watertightMeshes.length,
    inward_watertight_mesh_instances: watertightMeshes.filter((item) => !item.outward_signed_volume).length,
    normal_attribute_mismatch_triangles: normalAttributeMismatches.length,
  },
  duplicate_triangle_groups: duplicateGroups.slice(0, MAX_PAIR_DETAILS),
  exact_coplanar_pairs: exactPairs,
  near_coplanar_pairs: nearPairs,
  negative_or_singular_transforms: nodeTransforms.filter((item) => item.negative || item.zero_or_singular),
  materials,
  primary_material_errors: primaryMaterialErrors,
  closed_core: closedCore,
  inward_watertight_meshes: watertightMeshes.filter((item) => !item.outward_signed_volume).slice(0, MAX_PAIR_DETAILS),
  normal_attribute_mismatches: normalAttributeMismatches.slice(0, MAX_PAIR_DETAILS).map((tri) => ({
    node: tri.node,
    mesh: tri.mesh,
    primitive: tri.primitive,
    triangle: tri.triangle,
    attribute_normal_dot: tri.attributeNormalDot,
  })),
  unresolved: [],
};

if (duplicateGroups.length) result.unresolved.push('duplicate world-space triangles exist across nodes');
if (exactPairCount) result.unresolved.push('overlapping exact-coplanar triangle pairs exist across nodes');
if (nearPairCount) result.unresolved.push('overlapping near-coplanar triangle pairs exist within 0.2 mm across nodes');
if (result.counts.negative_transforms) result.unresolved.push('negative transforms exist');
if (result.counts.singular_transforms) result.unresolved.push('singular transforms exist');
if (result.counts.blend_materials) result.unresolved.push('BLEND materials exist');
if (result.counts.double_sided_materials) result.unresolved.push('double-sided materials exist');
if (primaryMaterialErrors.length) result.unresolved.push('primary face material invariant failed');
if (!closedCore.length) result.unresolved.push('no named closed chassis core was found');
if (result.counts.closed_core_failures) result.unresolved.push('named closed chassis core is not watertight/outward');
if (result.counts.inward_watertight_mesh_instances) result.unresolved.push('watertight mesh instances with inward winding exist');
if (result.counts.normal_attribute_mismatch_triangles) result.unresolved.push('triangle winding disagrees with NORMAL attributes');
result.status = result.unresolved.length ? 'REWORK' : 'PASS';

fs.mkdirSync(new URL('.', `file://${output}`).pathname, { recursive: true });
fs.writeFileSync(output, `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify({ input, status: result.status, counts: result.counts, unresolved: result.unresolved }, null, 2));
