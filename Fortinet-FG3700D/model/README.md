# FG-3700D model build

The two GLBs are newly constructed exact-exterior assets. No official or third-party mesh is copied.

## Rebuild

From the `Fortinet-FG3700D` directory:

```bash
python3 -m venv .venv
.venv/bin/pip install -r model/requirements.txt
.venv/bin/python model/build_model.py --profile both
```

The standard and web profiles use the same visible node structure. They differ only in embedded texture resolution and cylinder tessellation; the audited exterior bounds and visible counts remain identical.

## WebGL viewers

```bash
npm install
python3 -m http.server 8793 --bind 127.0.0.1
```

Then open either viewer and pass `model` and `view` query parameters:

- `qa/viewer-threejs/index.html`
- `qa/viewer-babylonjs/index.html`

Supported views are `front`, `rear`, `left`, `right`, `top`, `bottom`, `front-left`, `front-right`, `rear-left`, and `rear-right`.

