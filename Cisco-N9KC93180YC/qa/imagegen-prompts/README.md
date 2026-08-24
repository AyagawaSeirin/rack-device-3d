# Built-in image generation prompt ledger

Each of the six faces has one dedicated built-in image-generation call and a fully preserved prompt in this directory. Inputs are ordered exactly as labeled in each prompt. Generated chroma-key intermediates are preserved under `qa/intermediate/`; only locally de-keyed outputs become `views/*.png`.

The face authority and production mode are binding from `source/face-source-lock.csv`. Left and right prompts are deliberately different and are never produced by mirroring. Bottom is the sole `GENERIC_BOTTOM_FALLBACK`.
