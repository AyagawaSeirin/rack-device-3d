# Reproduce and edit

The delivered master is the authoritative editable result. Open it in Blender4.0.2 or a compatible newer version, then use its component collections. Textures and font resources are packed. External copies use paths relative to the master. The original Windows/XRDP desktop is not needed to open the asset.

## Script execution

All model creation, material setup, UV baking, saves, export and import were actually executed through the existing GUI Blender MCP. The recorded wrapper reads the exact user goal from REQUEST.md and binds __file__ and PROJECT_ROOT explicitly:

```bash
python3 scripts/mcp_run.py scripts/audit_delivery_scene.py
```

Run from the version directory. The wrapper uses the installed real MCP protocol client under /root/.local/share/blender-mcp-setup; that is an environment dependency, not a texture dependency. Do not run modelling stages in a scene containing unsaved user work. After the original work was saved to its own file and the clean state verified, Stage00 created the Cisco scene and removed the previous scenes from the new Cisco document. It preserves the previous work on disk, not as embedded scenes inside the Cisco model. The original Dell preservation report is inqa/pre-task-blender-state.json.

Creation order:00_isolate_scene,01_body_and_ears,02_qsfp_ports,03_fans_and_psus,04_controls_and_brand,05_photo_label_and_pbr,repair_label_projection,06_studio,apply_neutral_studio,09_refine_front_and_latches,10_refine_cage_proportions,11_prepare_final_mesh,12_finish_geometry,13_remove_degenerate_print_faces,14_fix_handle_sweep. Read the scripts' preconditions before rerunning; they are deliberately staged operations and not all idempotent. Stages01–05 build their parts once. Refinement scripts replace named parts without duplicating the assembly.

`parameters.json` and `DIMENSIONS.md` distinguish official dimensions and estimates. `model_lib.py` converts working millimetres to metres. Several refinement scripts use explicitly documented local working estimates; changing the parameter file alone will not recompute every refinement. Use the source scripts and named stages to rebuild a revised variant.

`audit_geometry.py` checks original topology; `audit_delivery_scene.py` checks original/imported geometry, large planar split normals, positive transforms, material contracts, packed image dependencies, UV names, dimensions, reading axes and label gap. For imported glTF only, a diagnostic BMesh copy welds split vertices at1e-7m. It never welds the formal imported mesh. Text ink permits intentional open boundaries; zero-area and duplicate faces remain failures.

`export_glb.py` exports selected formal nodes, with normals/tangents/UVs and extras. `audit_glb.py` validates the binary container, materials and embedded images. `reimport_glb.py` imports into a separate GUI scene, then adds only copied studio equipment for QA. `ear_and_opacity_qa.py` runs original/reimport ray tests and saves isolated fixtures.

## Rendering and desktop evidence

Background Blender is used only for rendering already-saved models/fixtures:

```bash
blender -b model/CISCO-Nexus-N9K-C9336C-FX2.blend -t 4 --python scripts/render_final_views.py -- 0 1
blender -b qa/original-ear-fixture.blend -t 4 --python scripts/render_ear_fixture.py -- original
blender -b model/CISCO-Nexus-N9K-C9336C-FX2.blend -t 4 --python scripts/render_shell_alpha.py -- original
python3 scripts/qa_alpha_backgrounds.py original
```

The equivalent glb fixtures are under qa. OIDN is unavailable in this Blender build; both final and preview denoising are disabled. Cycles images use128/192 samples, small adaptive threshold and neutral recorded lights; fine residual Monte Carlo noise can remain. The neutral light-gray beauty background is linear white passed through AgX, not a claim of pure RGB255 output. Light/dark shell QA images are exact display-space composites of the retained unmodified transparent result; they do not change lighting or object Alpha.

`desktop_orbit.py` and `desktop_inspection.py` send actual server_desktop keys and capture raw screenshots. Before these scripts run, take a fresh native screenshot, focus a blank 3D-view region and verify a single rotation. Coordinate scaling must use the current desktop resolution. The original Solid and Material series before the final handle sweep correction are retained as intermediate evidence; final GLB orbit and final master screenshots verify the corrected visible geometry. Do not label script camera renders as desktop input.

Final master material preview uses Scene World/Scene Lights. Real-time Eevee ambient occlusion distance0.04m/factor1.25 supplies local cavity shading; it differs from final path-traced indirect illumination. Near/far viewport clip0.01/10m avoids depth precision problems with the measured25µm ink separation. Only the active viewport uses Material Preview; no animation runs by default.

## Archive

Run scripts/check_sources.py for original-download integrity, scripts/build_review.py for the offline comparison gallery, and scripts/check_archive.py for final file/format/link/hash checks. Runtime dependencies (Pillow, numpy, requests, pymupdf, bs4) are not committed. Git LFS is scoped by the parent device directory's.gitattributes; download LFS objects when cloning. Stage snapshots and rejected generations are intentionally retained.
