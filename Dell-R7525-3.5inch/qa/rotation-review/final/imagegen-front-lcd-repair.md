# Dell front LCD repair lineage

The old front elevation contained readable text `IP:23.75.248.127`. Neither the user configuration lock nor the official bezel sources prove that runtime value, so it was treated as invented identity-bearing content.

Image editing was restricted to the LCD interior. The generated full-canvas edit was rejected because its 1920 x 819 canvas and surrounding pixels drifted from the 2400 x 432 locked elevation. It is preserved, not used, at `qa/rotation-review/imagegen/front-lcd-edit-rejected-canvas-drift.png`, SHA-256 `3ef4f5504f479057ffc767a40f4509f7e162ee57d8d835ed61d1c0c0d569dca8`.

`model/repair-front-lcd.py` composites only the generated dark LCD interior into the existing source-locked 2400 x 432 elevation. All pixels outside the bounded LCD replacement are inherited from the prior elevation. The accepted output is `views/front.png`, SHA-256 `6630c2bd90a7e5d24c386461ff97ae60493e14cd030eda5239945cfac31b0a1b`; identical standard build input is stored at `qa/build/opaque-standard/front.png`. The web texture is a deterministic downsample.

Before/after inspection crops are retained at:

- `qa/rotation-review/imagegen/front-lcd-before-crop.png`
- `qa/rotation-review/imagegen/front-lcd-after-crop.png`
- `qa/rotation-review/imagegen/front-lcd-generated-crop.png`

No logo, carrier, bezel lattice, control strip, port, silhouette or dimension was regenerated or altered by the accepted repair.
