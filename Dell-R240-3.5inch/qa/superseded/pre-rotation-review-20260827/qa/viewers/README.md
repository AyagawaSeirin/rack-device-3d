# Independent WebGL validation viewers

- `three.html` uses Three.js 0.170.0 and explicitly fetches/parses the selected GLB.
- `babylon.html` uses Babylon.js 7.44.0 and explicitly fetches/parses the selected GLB through its independent loader.

Both expose `window.__VIEWER_INFO__` only after parsing and rendering the real bytes. Ten camera names are supported: six orthographic faces plus four three-quarter views.
