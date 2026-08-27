# Independent WebGL QA viewers

- `viewer-a/index.html`: `<model-viewer>` 4.3.1.
- `viewer-b/index.html`: Three.js 0.185.1 with `GLTFLoader` and an independently calculated orthographic camera.

Both accept `?model=standard|web&view=front|rear|left|right|top|bottom|front-left|front-right|rear-left|rear-right` and expose `window.__QA__` after the actual GLB has loaded.
