# Image generation checkpoint record

The six accepted chroma-key source images in `qa/imagegen-raw/` are separate built-in `image_gen` outputs recovered from the pre-restart checkpoint. Their distinct files, dimensions, content, and hashes are retained unchanged. The original conversational tool-call envelopes were lost when the prior task stopped, so the per-face files in this directory preserve the recovered and normalized final prompt contract, source roles, selected raw hash, post-processing, and accepted final hash without repeating the high-cost generations.

Generation mode was one dedicated built-in call per face, `product-mockup`, on a uniform `#FF00FF` chroma-key background. Local processing removed only the border-connected key, sealed accidental internal alpha, preserved physical ratio without scaling identity-bearing components, and emitted the final RGBA assets. Rejected variants remain under `qa/imagegen-raw/` and never enter `views/` or either GLB.

The top face received one deterministic post-generation factual repair after the checkpoint: the existing factory hot-surface label pixel block was moved from the unsupported front-right position to the rear-right position proven by the exact-device rear/top photographs. No other top texture pixels, vents, seams, latches, or material style were regenerated. The pre-repair top is retained as `qa/work/top-before-warning-relocation.png`.

The bottom face is the sole documented `GENERIC_BOTTOM_FALLBACK`; therefore the deliverable status is `PASS_WITH_BOTTOM_FALLBACK`.
