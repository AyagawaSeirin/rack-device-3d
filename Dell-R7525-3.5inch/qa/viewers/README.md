# Independent WebGL validation viewers

- `three.html` uses Three.js 0.170.0 with GLTFLoader and loads the standard GLB by default.
- `babylon.html` uses Babylon.js 7.44.0 with its independent glTF loader and loads the web GLB by default.

Babylon is explicitly configured with `scene.useRightHandedSystem = true` so its cameras use the same project convention as glTF and Three.js: `+X` is the device's physical right, `+Y` is up, and `+Z` is front. This prevents the default Babylon left-handed conversion from swapping physical left/right validation views.

Both pages accept `?view=front|rear|left|right|top|bottom|front-left|front-right|rear-left|rear-right` and set `window.__VIEWER_READY__` only after the requested GLB has parsed, its bounds have been computed, and at least one frame has rendered.

For the required alpha inspection pass, both pages also accept `&bg=light` or `&bg=dark` to place the rendered GLB over an explicit light or dark checkerboard while retaining the transparent WebGL clear color.

The validation capture sizes the WebGL drawing buffer to the actual browser viewport so screenshots cannot non-uniformly stretch the model. It uses a transparent clear color, neutral two-direction lighting for PBR geometry, no post-processing, and orthographic cameras for the six faces.
