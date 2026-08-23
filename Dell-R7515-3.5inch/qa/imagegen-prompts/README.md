# Six-face image-generation record

All six production faces were generated in **six separate imagegen calls**. No
face was created by mirroring another face. Each call requested a single exact
orthographic exterior elevation against a solid magenta key background. The
raw imagegen results are retained unchanged under `qa/work/imagegen-raw/`;
keyed intermediates are under `qa/work/imagegen-keyed/`; final dimension-safe
production faces are under `views/`.

The prompts are transcribed in the individual face files in this directory.
Reference roles and checksums are bound in
`qa/imagegen-generation-manifest.csv` and `source/face-source-lock.csv`.

Post-processing was deterministic and local (`qa/process_views.py`): chroma
removal, transparent-canvas normalization, non-anisotropic scale/crop,
source-verified DELL/PowerEdge/R7515 identity cleanup, and local suppression of
unsupported pseudo-text. It did not mirror, redraw, or substitute either side.
The bottom is explicitly `GENERIC_BOTTOM_FALLBACK`, so the final model status
cannot exceed `PASS_WITH_BOTTOM_FALLBACK`.

