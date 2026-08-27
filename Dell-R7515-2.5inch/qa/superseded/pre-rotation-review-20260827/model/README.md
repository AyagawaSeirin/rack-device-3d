# Model build

Run with the existing project Python environment that provides `trimesh`, `Pillow`, `numpy`, `shapely` and `mapbox_earcut`:

```bash
python model/build_model.py --flavor both
```

The script creates a newly constructed standard GLB and a web texture-budget GLB. It does not import or reference a PowerEdge R7525 mesh. The editable construction record is the script plus `build-manifest.json`; all external resources are embedded in the final GLBs.

Coordinate convention: +X device right as seen from the front, +Y up, +Z front. glTF units are metres.
