# Optional official 3D search

Access date: 2026-08-23 (Asia/Singapore)

Searched Dell product/support/media pages and public web indexes for the exact `Dell EMC PowerEdge R240` combined with `3D`, `AR`, `GLB`, `glTF`, `CAD`, `STEP`, `OBJ`, `FBX`, `Visio`, `BIM` and direct `site:i.dell.com` asset queries. The browser-rendered Dell Australia R240 gallery exposes four 2D image assets and no public 3D/AR control or model network resource. Dell support/manual and official-video pages likewise expose no public exact-model 3D download.

Result: no official public exact R240 3D file or viewer asset was found. Nothing is placed in this directory other than this reproducible log. This does not change the requirement to deliver the two newly constructed GLBs.

## Rotation-review recheck — 2026-08-27

Re-ran exact-PID searches for Dell-hosted `3D`, `CAD`, `STEP`, `OBJ`, `FBX`, `GLB`, `glTF`, `AR`, `BIM`, and Visio resources. The official PSU/manual page was also opened in a fresh Playwright CLI browser session after taking a snapshot; Dell returned HTTP 403 and the request list contained only that blocked HTML request, with no public model payload. The preserved browser snapshot and console log are under `qa/rotation-review-20260827/research/playwright-dell/`. No exact official public 3D file was found, so there is no official binary to download; both self-built GLBs remain required.
