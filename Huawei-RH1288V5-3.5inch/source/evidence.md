# Evidence ledger

## Primary and authoritative sources

1. Huawei support product page, product PID 21872252: <https://support.huawei.com/enterprise/zh/server/1288h-v5-pid-21872252>
   - Locks the official `1288H V5` product identity and generation.
   - No exact 1288H V5 downloadable 3D/CAD asset or product-3D entry was exposed on the product page during the 2026-08-23 review.
2. Huawei, *FusionServer Pro 1288H V5 Server User Guide*, Issue 13, 2020-06-05. Local copy: `originals/huawei-1288h-v5-user-guide-issue13.pdf`.
   - Locks 1U form factor, 4 × 3.5-inch option, rear component families, service I/O, dual PSU layout, and 43 × 436 × 748 mm dimensions for the 3.5-inch chassis.
   - Text was extracted and selected pages were rendered with Ghostscript because the environment had no dedicated PDF extraction skill/tool.
3. Huawei, *1288H V5 Server Quick Guide*, V100R005, revision 07. Local copy: `originals/huawei-1288h-v5-quick-start-v100r005-07.pdf`.
   - Official two-page installation/configuration evidence and model naming.
4. Huawei product 3D display: <https://info.support.huawei.com/computing/tools/server-3d?lang=en>
   - The live `Intelligent Servers` category returned `No data` during browser inspection.
   - Its old-version link, `https://onex.info.huawei.com/computing/server3D/index_en.html`, returned DNS failure.
   - Search results expose a `2288H V5` product 3D presentation, but that is a different 2U device and is rejected as a model source.

## Exact specimen and view sources

5. Serverflow exact specimen listing, Huawei FusionServer 1288H V5 1U 4LFF, dual 900 W AC: <https://serverflow.ru/config/servernaya-platforma-huawei-fusionserver-1288h-v5-1u-4lff-2x-900w-2x-lga3647/>
   - Fourteen 3000 × 2252 photos are stored under `third-party/serverflow/`.
   - Directly locks the 4LFF front, Huawei/1288H V5 markings, top-cover seam/latch/vent bands, rear three-riser family, dual 900 W AC modules, and many visible chassis details.
   - Several photos show the cover removed and are used only to understand edge construction and internal ventilation; internal components are not exposed in the delivered closed model.
   - The photos do **not** include a direct bottom view.
6. CompuWay 1288H V5 product page: <https://www.compuway.ru/servers/huawei/huawei-fusionserver-rh1288h-v5-product-page/>
   - `compuway-1288h-v5-4lff.png` binds the exact 4LFF front.
   - `compuway-1288h-v5-rear.jpg` and `...-iso.jpg` support the rear and family-level three-quarter structure.
   - `compuway-1288h-v5-top.png` is an open-cover/internal diagram. It supports internal family identity only and is rejected as the closed top-face lock.
   - `compuway-1288h-v5-front.jpg` depicts a 2.5-inch front variant and is rejected for front geometry.
7. MyDraw Huawei 1288H V5 shape library: <https://www.mydraw.com/shape-libraries-networking-equipment-huawei-it-servers-and-storage-server-rh1288h-series-huawei-server-1288h-v5>
   - `mydraw-front-4disk.png` supports the four-disk front.
   - `mydraw-rear-3io.png` supports the frozen three-I/O rear family.
   - `mydraw-rear-2io.png` is retained as contrast evidence and rejected for this configuration.
8. User-supplied device-list screenshot: `originals/user-device-list.png`, row crop `../qa/reference/user-row8.png`.
   - Configuration clue only: confirms the requested 4LFF front and a three-riser/dual-PSU rear family.
   - It is not used as a final texture because it is a small UI thumbnail.

## Supporting-only and rejected sources

- `third-party/inrack-front.jpg` shows a different 2.5-inch front variant. It is retained for family-level chassis/branding context only and rejected for the requested front.
- `third-party/inrack-top-angle.jpg` and `...rear-angle.jpg` are supporting family views; the exact Serverflow 4LFF specimen and official drawings take precedence.
- 2-I/O MyDraw rear, any 8SFF/10SFF front, 708 mm 2.5-inch chassis dimensions, DC PSUs, V3/V6 generations, and 2288H V5 assets are excluded.

## Official 3D/CAD availability result

Searches covered Huawei support, Huawei enterprise, Huawei computing 3D display, and public web results for `1288H V5` combined with `3D`, `CAD`, `STEP`, `IGES`, `OBJ`, `GLB`, `GLTF`, and product-3D-display terms. No exact, public, downloadable official 1288H V5 4LFF model was found. Consequently `source/optional-3d/` intentionally contains only `README.md`; no adjacent-model asset was downloaded or passed off as official.

## Bottom-face status

No direct, exact bottom photograph or official bottom drawing was found. The bottom is therefore the only `CONTROLLED_FALLBACK` face. It uses the authoritative 436 × 748 mm chassis envelope, construction cues from the exact top/front/rear/three-quarter photos, and conservative galvanized-steel base seams. It contains no invented ports, labels, feet, or asymmetric access panels. Final status must be `PASS_WITH_BOTTOM_FALLBACK` if all other gates pass.
