# Independent glTF render paths

The actual GLBs are loaded from disk through a local HTTP server and rendered by two independent glTF engines:

1. three.html: Three.js WebGLRenderer plus GLTFLoader.
2. babylon.html: Babylon.js Engine plus Babylon glTF 2 loader.

Both use orthographic matched cameras, neutral backgrounds, no post-processing, and local vendored runtimes. The six orthographic and four three-quarter camera names are front, rear, left, right, top, bottom, front_left, front_right, rear_left, and rear_right.

Babylon's default coordinate-system conversion culls the reverse side of zero-thickness source-photo cards differently from Three.js. The Babylon QA page therefore disables back-face culling only for the six unlit photo-card materials after load. Solid model materials remain single-sided. This is a viewer-only diagnostic setting; the GLBs retain doubleSided false everywhere, have outward normals, and pass the structural normal/transform audit.

The viewer assets are QA tooling only. The deliverable GLBs are self-contained and do not depend on these files.
