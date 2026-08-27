# Official 3D review — 2026-08-27

Target: exact Dell PowerEdge R730 16 × 2.5-inch SFF, no bezel, standard seven-blank rear, dual 750 W AC PSU installed configuration.

- Dell's current official R730 3D Guides index exposes 22 exact-model service experiences, including PSU, risers, cover, cooling fan assembly, control panel and backplane procedures. The PSU guide is `ic14000r730002401a`.
- These are service experiences, not a published raw download for the requested 16-SFF fully installed exterior; the guide page does not establish that its visible front/rear option equals this delivery configuration.
- Fresh real Chromium/Playwright and direct public HTTP requests to the official PSU experience both returned Dell/Akamai HTTP 403. The screenshot, response headers and untouched HTML error response are preserved in `official-3d-review/`.
- Access controls were not bypassed. No public GLB, glTF, STEP/STP, OBJ or FBX payload could be downloaded and preserved.

Result: `OFFICIAL_SERVICE_3D_DISCOVERED_RAW_PAYLOAD_BLOCKED_NOT_CONFIGURATION_COMPLETE`. This optional official path does not replace or block the independently validated standard/web GLBs.
