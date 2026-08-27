# WebGL load-run notes

The accepted final evidence set contains exactly 40 real, byte-fetched, parsed and rendered loads: two independent WebGL engines × two GLBs × ten views. Every URL used a unique load token and each viewer fetched the final GLB with `cache: no-store` before parsing it. The local HTTP server returned 200 for every accepted model request.

Earlier diagnostic batches exposed and allowed repair of a Babylon loading-overlay artifact, a rear PSU depth overlap and false rear-view rack-ear silhouettes. Those screenshots and all pre-repair loads are excluded. After the last repair, all four viewer/model groups were rerun from scratch in fresh browser processes; each complete ten-view run returned PASS with zero browser errors.

Only the 40 post-repair screenshots listed in `load-evidence.json` and `load-evidence.ndjson` count toward the final gate.
