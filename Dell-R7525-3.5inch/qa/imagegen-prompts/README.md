# Image generation provenance

The six canonical faces were produced before the current takeover with the built-in `image_gen` path and a flat chroma background, followed by local alpha extraction and tight cropping. The preserved artifact chain for every face is:

`qa/imagegen-selected/<face>-chroma.png` → `<face>-alpha.png` → `<face>-trim.png` → `views/<face>.png`.

The originating task became `notLoaded` and its exact verbatim tool payload could not be retrieved without attempting to revive it. The six face records in this directory therefore preserve reconstructed acceptance prompts from the already-frozen identity manifest, face-source lock, feature inventory, inspected input roles, selected outputs, and final hashes. They are deliberately labeled as reconstructed records rather than falsely presented as recovered verbatim logs. No face was regenerated during this takeover.

Common locked identity: Dell PowerEdge R7525, 2U, 12 × 3.5-inch/LFF front, installed Dell EMC LCD/security bezel, no rear-drive module, four riser groups/eight PCIe positions, and two matching 2400 W AC PSUs. All product pixels are opaque in the GLBs; only the external canonical PNG canvas may be transparent.
