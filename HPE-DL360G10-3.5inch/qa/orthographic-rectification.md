# Dimension-driven orthographic rectification

The built-in image-generation calls produced the required exact configuration and independent face content, but the raster content bounds retained camera/product-shot thickness bias on the extremely thin 1U faces. The original generated/chroma/alpha versions are preserved in `qa/staging/`.

Final `views/` assets apply one global face-wise orthographic scale correction derived only from official dimensions; no component is moved, cloned, deleted, mirrored or reordered:

- front: 482.6 mm overall rack-ear span x 42.9 mm body height -> 4096 x 364 px
- rear: 434.6 mm body width x 42.9 mm body height -> 4096 x 404 px
- left/right: 749.8 mm LFF depth x 42.9 mm height -> 4096 x 234 px
- top: generated 2390 x 4096 ratio already within 0.7% of 434.6:749.8 and is unchanged
- bottom fallback: 434.6 mm x 749.8 mm -> 2374 x 4096 px

This is a projection/dimension correction of the generated orthographic assets, not a variant substitution or creative retouch. The GLB geometry uses the millimeter dimensions directly, so textures and independent relief are not used to establish world-space size.

Top-face dark vents are opaque recessed features, not openings through the chassis. The top repair fills only transparent pixels inside the verified central closed-cover area with dark opaque recess color; exterior transparency and perimeter silhouette remain unchanged.
