# Final QA — Huawei FusionServer Pro 1288H V5 10SFF

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

- Complete 1U Huawei FusionServer Pro 1288H V5 appliance (catalog alias RH1288V5/2.5-inch).
- Front: 10 x 2.5-inch, five columns by two rows, no security bezel, factory Huawei and `1288H V5` marks retained.
- Rear: 3-I/O family; optional LOM1/2 and FlexIO positions closed/unpopulated; fixed VGA, four RJ45 and two USB; two identical AC/IEC hot-swap PSUs.
- Body: 436 x 43 x 708 mm; delivered exterior bounds: 482.6 x 43 x 714 mm including front mounting span and the documented 6 mm rear projection.

## Acceptance results

- Six face audit: `PASS`, 0 errors; warnings are limited to verified ear/silhouette antialiasing and all opaque chassis cores report 0% transparent pixels.
- Standard GLB audit: `PASS`, 0 errors, 0 warnings.
- Web GLB audit: `PASS`, 0 errors, 0 warnings.
- Both GLBs contain 33 named visible geometry groups, 15 OPAQUE materials/textures, embedded resources, no negative/mirrored node transforms, and identical geometry hash `27ffad72d7f61e9640d21c5ac25eb2efa909c443d5618c4e8cc60738b8f7e06d`.
- Real-browser WebGL QA: Three.js r180 and Babylon.js 8.26.0 each loaded both GLBs; 40 required six-orthographic/four-oblique screenshots plus 8 light/dark alpha inspections are present; loader/page errors: 0.
- Feature inventory: 32 rows checked, unresolved: 0. Source comparison matrix: 12 rows; maximum diagnostic canvas MAE 3.552878/255.

## Geometry and appearance notes

- The model is a closed shell with separate front-only rack ears and true circular openings, ten relieved SFF carriers, control-panel relief, three rear PCIe covers, separate blank LOM/FlexIO panels, real service-strip openings, dual independently protruding AC PSU modules with recessed fan/C14 openings, aligned top vent/latch/step relief, and independent non-mirrored side fastener/slot patterns.
- Front ears remain located at the physical front plane. A direct rear orthographic projection can see their lateral extensions, but there is no rear-ear mesh.
- Main photographic surfaces and all generated solid materials are OPAQUE and unlit; black ports/vents are dark pixels or recessed geometry rather than alpha holes.
- Standard and web GLBs use the same exterior geometry. Web optimization reduces texture resolution only; feature counts, orientation, silhouette and relief are unchanged.

## Bottom fallback disclosure

No exact 10SFF underside photograph or official mechanical drawing was found after the documented official, dynamic-viewer, reseller, marketplace, used-equipment and multilingual searches. `bottom.png` is therefore the allowed conservative `GENERIC_BOTTOM_FALLBACK`: a plain opaque 436:708 galvanized base plate with no logo, label, vent, foot, rail, hole or unsupported feature. This is the sole reason the status is `PASS_WITH_BOTTOM_FALLBACK` instead of `PASS`.

## Optional official resource

The public xFusion successor-official iV3D viewer resource is preserved unchanged in `source/optional-3d/xfusion-1288hv5-viewer/`; all 49 entries in its checksum list verify successfully. It is an incompatible 8SFF viewer source and was not imported into, copied into, or substituted for either newly constructed GLB.
