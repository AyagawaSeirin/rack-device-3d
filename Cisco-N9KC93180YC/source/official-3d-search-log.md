# Official and public 3D search log

Access date: 2026-08-24 (Asia/Singapore)

Result: **no public exact matching official 3D file was found for any identity candidate**. No file is stored in `source/optional-3d/`.

## Official Cisco searches

Searched Cisco for each candidate PID with: `3D`, `AR`, `GLB`, `glTF`, `OBJ`, `FBX`, `STEP`, `STP`, `CAD`, and `Visio`.

- `site:cisco.com "N9K-C93180YC-EX" (3D OR GLB OR glTF OR OBJ OR STEP OR CAD)`
- `site:cisco.com "N9K-C93180YC-FX" (3D OR GLB OR glTF OR OBJ OR STEP OR CAD)`
- `site:cisco.com "N9K-C93180YC-FX3" (3D OR GLB OR glTF OR OBJ OR STEP OR CAD)`
- `site:cisco.com "N9K-C93180YC" "Visio"`

Official results were product support pages, datasheets, and hardware installation guides. The Cisco support pages expose a 76 MB `switches_cisco_nexus_9000.zip` **Visio stencil**, which is a 2D diagram package and is not an official 3D model. It was not copied into `optional-3d/`.

The rendered FX3 support page was inspected with Playwright. Its accessibility snapshot contains `Visio Stencil` and no `3D`, `CAD`, `GLB`, `glTF`, `OBJ`, `FBX`, or `STEP` asset. Evidence: `qa/browser/cisco-fx3-support-snapshot.yml`.

Official support pages checked:

- https://www.cisco.com/c/en/us/support/switches/nexus-93180yc-ex-switch/model.html
- https://www.cisco.com/c/en/us/support/switches/nexus-93180yc-fx-switch/model.html
- https://www.cisco.com/c/en/us/support/switches/nexus-93180yc-fx3-switch/model.html
- https://www.cisco.com/c/en/us/support/switches/nexus-93180yc-fx3s-switch/model.html

## Broader public searches

- `"N9K-C93180YC-EX" (GLB OR glTF OR OBJ OR FBX OR STEP OR STP OR "3D model")`
- `"N9K-C93180YC-FX" (GLB OR glTF OR OBJ OR FBX OR STEP OR STP OR "3D model")`
- `"N9K-C93180YC-FX3" (GLB OR glTF OR OBJ OR FBX OR STEP OR STP OR "3D model")`
- `"Cisco 93180YC" 3D model CAD`

Results were reseller pages, product photographs, manuals, and NetBox metadata. None exposed an exact official 3D asset or a public exact third-party 3D file suitable for preservation.

## Dynamic/browser inspection

- Cisco EX hardware guide rendered successfully; its official front/rear figure URLs were extracted. Evidence: `qa/browser/cisco-ex-overview-snapshot.yml` and `qa/browser/cisco-ex-overview.png`.
- Cisco FX hardware guide rendered successfully; its distinct FX figures were extracted. Evidence: `qa/browser/cisco-fx-overview-snapshot.yml`.
- Cisco FX3 support page rendered successfully; only the official Visio stencil was present. Evidence: `qa/browser/cisco-fx3-support-snapshot.yml`.
- Exact EX used-equipment gallery rendered successfully and five originals were downloaded. Evidence: `qa/browser/pios-ex-product-snapshot.yml`.
- One attempted headed launch failed because no X server is present; the documented headless path then succeeded.

## Local repository search

`rg --files` was searched for `N9K.?C93180YC`, `93180YC`, and `Cisco.*93180`. No pre-existing model, mesh, texture set, or official 3D file was found outside this new model directory.

## Conclusion

Official 3D status is `NOT_FOUND`. Even if an official file had been found, the skill requires a separate newly constructed standard/web GLB after identity verification; an official file would not replace that build.
