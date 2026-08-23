# Optional official 3D discovery

Access date: 2026-08-23

Huawei's official gallery API returns the historic interactive viewer:

`https://info.support.huawei.com/computing/server3D/res/server/rh1288v3/index.html?lang=en`

The viewer used `tree.json` and `./res/model/` resources and offered original/exploded/component views. Huawei currently returns HTTP 302 to the 3D-service migration/maintenance page; the public service states access has been restricted for an upgrade since 2026-01-30. Browser and network inspection found no current public raw GLB, glTF, OBJ, FBX, STEP, CAD, IV3D, tree or model payload. Direct model/resource requests redirect to the maintenance page. No authentication, internal environment, private API or access control was bypassed.

Preserved files:

- `Huawei-RH1288-V3-official-viewer-index-20221209.html`: original official viewer index recovered from the public Internet Archive capture; SHA-256 is recorded in the source ledger.
- `../originals/Huawei-product-gallery-RH1288-V3-official-download-all.zip`: Huawei's current official download-all archive, unchanged; it contains only two 2.5-inch/SFF PNG product photographs at 720p and 1080p.

The archived viewer's visible component names include the DVD-based 8-SFF front, so it is not proven to be the requested 4-LFF exterior even if its model payload later becomes available. No file is represented as an exact public official 4-LFF 3D model.
