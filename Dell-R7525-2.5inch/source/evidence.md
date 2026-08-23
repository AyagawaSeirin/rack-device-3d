# Evidence, configuration, and search record

Access date: 2026-08-23 (Asia/Singapore)

## Configuration decision

The user-provided row 9 is the binding delivery row: **DELL R7525/2.5-inch**. The row shows an installed LCD security bezel and the standard rear wall with two outer PSUs and no rear-drive module. Dell's installation manual, pages 28–29, shows that exact bezel installed over the 24 x 2.5-inch carrier bank. The independent 24SFF photographs and Dell front elevation confirm one row of 24 portrait carriers, not an LFF array.

The explicit serial-port requirement is satisfied by Dell's documented optional 9-pin DTE COM card in **Riser 3** (installation manual pages 187–188). The standard official rear image is retained as the base rear layout, with the serial card added only at the documented Riser 3 filler-bracket position.

Both outer PSU bays are populated with matching 2400 W mixed-mode units operated as AC supplies, matching the locked rear render's visible `2400W` labels. No DC-only connector, PSU blank, rear drive cage, rails, or cable-management arm is included.

## Official sources

1. Dell PowerEdge R7525 Installation and Service Manual, 56,466,133 bytes, SHA-256 `0fb5bceace24dc9e46b98a9cc9bf492504ad25660586fd41cac695ff93981c66`.
   - pp. 10–12: front layouts and exact left/right control panels.
   - pp. 13–15: standard rear layout and the separate rear-drive option that is excluded.
   - pp. 28–29: LCD bezel installed over a 24SFF front.
   - pp. 187–188: 9-pin serial COM port installed in Riser 3.
   - pp. 210–211: hot-plug PSU geometry and matching-redundant-PSU rule.
2. Dell EMC PowerEdge R7525 Technical Guide, 77 pages, SHA-256 `1e7542c9cd7c48c3dc16b34dae95ce1044688f78453023d7f3f2d2777b0f6578`.
   - p. 9: 24 x 2.5-inch elevation.
   - p. 11: standard rear and separate rear-drive option.
   - pp. 12–13: internal six-fan row and riser arrangement.
   - p. 20: supported 24 x 2.5 SAS/SATA/NVMe front options.
   - p. 22: OCP 3.0 and riser/slot definitions.
3. Dell EMC PowerEdge R7525 Technical Specifications, 22 pages, SHA-256 `f130e363d0c87e62d6ba4d38fff1b64e970910812a4531041cbf107365c79202`.
   - p. 5: Xa/Xb/Y/Za/Zb/Zc dimensions and inclusion notes.
   - p. 6: AC-capable 800/1100/1400/2400 W PSU options.
   - pp. 7–9: six fan modules and fan grades.
   - pp. 11–12: drive/backplane options and USB/NIC/serial/VGA specifications.
4. Dell official 3D/AR service experience:
   - viewer: `https://www.dell.com/support/resources/en-sc/3dviewer/ic1400r7525002201a/how-to-replace-the-expansion-card-on-a-poweredge-r7525`
   - public scene: `https://dellarassistant.glare.kaalo.com/IC1400R752500/assets/mySceneClone.glb`
   - the public model was preserved unchanged as `source/optional-3d/dell-official-ar-r7525-mySceneClone.glb` (18,454,132 bytes; SHA-256 `4d195480b7717b92687b20a9d0e96c1cd733e3cf4e4124fc92bb11fa89dbcbff`). It declares 17,773 nodes, 656 meshes, 233 materials, 69 images, 69 textures, and 39 named component dependencies. It is evidence/backup only; its meshes are not copied into the independent deliverables.

## Third-party real photographs

- IT Creations exact `DELL R7525 2.5 24B` gallery: five 800 x 600 images, including near-front, front-right, rear-left, near-rear, and R7525/PowerEdge tag close-up. The gallery proves 24SFF carrier geometry, both non-mirrored side skins, cover seams, labels, rail hooks, and real metal/plastic texture. Its rear has a one-PSU state and is never used to define the locked dual-PSU rear.
- Allegro exact `R7525 24x2.5` 2560 x 1707 real photograph: proves the cover latch, top panels, service-label band, carrier count, and overall proportions.
- OEMDrivers bezel image: component-only bezel material/style support. It contains LFF carriers behind the bezel and is explicitly excluded as requested-chassis evidence.

## Browser escalation and official 3D discovery

- A real browser request to the Dell HTML manual returned HTTP 403; the directly published `dl.dell.com` document/image resources were then downloaded with a normal browser user agent and preserved unchanged.
- The Dell 3D Guides page publicly embeds `https://dellarassistant.glare.kaalo.com/IC1400R752500/index.html?pid=2201AEN`.
- Browser network inspection confirmed HTTP 200 for `assets/mySceneClone.glb` and `assets/WebGL_R7525.json`; both were saved unchanged to `source/optional-3d/`.
- Dell's public community search for an R7525 STEP file did not expose STEP/CAD; the official public AR GLB is the available official 3D asset.

## Bottom evidence search

Queries covered exact-model official manuals, mechanical diagrams, the Dell 3D/AR viewer, Dell service videos, `bottom`, `underside`, `teardown`, eBay/marketplace/used-equipment pages, English, Chinese, and Russian wording. The IT Creations gallery, Allegro listing, ServerMonkey, Enterasource, NewServerLife, eBay results, ServeTheHome review/video, and Dell service video catalog were checked. No usable exact underside photograph was found.

Because the preserved official Dell AR GLB is a complete R7525 assembly and contains the underside, bottom production is `MULTI_REFERENCE_RECONSTRUCTION` from the official 3D evidence, not a family-photo guess. The canonical bottom must remain conservative: verified silver sheet metal and official-AR-supported relief only, no copied top, brand, feet, rails, labels, ports, or unsupported holes.

## Dimension interpretation

- `Xa=482.0 mm`: rack-ear outer span.
- `Xb=434.0 mm`: body/rear-wall width.
- `Y=86.8 mm`: actual height.
- `Za=35.84 mm` with installed bezel; `22.0 mm` without bezel.
- `Zb=700.7 mm`: ear plane to nominal rear wall.
- `Zc=736.29 mm`: ear plane to PSU handle.
- Delivered full exterior depth is therefore `Za(with bezel) + Zc = 772.13 mm`.

## Image-production rule

Every canonical face is produced in one dedicated built-in `image_gen` call. A face with no direct orthogonal photograph uses `MULTI_REFERENCE_RECONSTRUCTION` from the inspected exact references above. Real exact-device photographs remain material/style authority wherever they exist. The user row, official diagrams, and official AR geometry are configuration/geometry locks and may not be restyled into a generic CGI server.

