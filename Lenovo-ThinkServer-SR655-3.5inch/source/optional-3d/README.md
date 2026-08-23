# Official optional 3D source

Viewer: https://lenovopress.lenovo.com/3dtours/sr655/

Discovered from the public DCSC ThinkSystem SR655 page on 2026-08-23.

The original-generation SR655 viewer does not publish a single GLB/GLTF download. It streams an InfinityRT WebGL package made of `hierarchy.xml`, RAW/Draco mesh blocks, textures and runtime files. Every public file requested by the viewer was downloaded through ordinary unauthenticated GET requests and retained byte-for-byte under `viewer-public/`.

`viewer-public/MANIFEST.sha256` contains per-file checksums. `Lenovo-ThinkSystem-SR655-official-viewer-original-files.tar.gz` is a deterministic convenience container around those unchanged files.

Archive size: 16,590,938 bytes

Archive SHA-256: `2d99c8fe4bc86f0ed28575421e76630a356cb69360e1dcb09b44c2c81af24a3e`

Usage terms clue: Lenovo Press displays Lenovo copyright and “All rights reserved”; no model-download or redistribution license was found. The package is retained for internal evidence/backup only. It is not copied into or substituted for the newly constructed deliverable GLBs.
