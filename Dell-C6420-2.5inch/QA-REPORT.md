# Dell C6420 2.5-inch final QA report

> Superseded for current acceptance by `qa/rotation-review-20260827/final-report.md` and its frozen-hash `final-gate.json`. Current hashes are `88348a13…` (standard) and `7a8c3b74…` (web); this older report is retained for lineage.

**Status: PASS_WITH_BOTTOM_FALLBACK**

Delivered subject: the complete Dell EMC PowerEdge C6400 2U enclosure shown by the user, populated with four C6420 compute sleds, 24 front 2.5-inch carriers, and two shared center EPP 1600 W AC PSUs. It is not a standalone sled.

- Standard GLB: `model/Dell-C6420-2.5inch.glb` — 16380768 bytes — `ecc0f7ff5b5cd595ae72e00af83f63e0857fefb079787c4737b61ef353d674f9`
- Web GLB: `model/Dell-C6420-2.5inch-web.glb` — 6890984 bytes — `b78c3c55807c96d9831ceb8da5e162684558f253135c438cd96a238ad1f61553`
- Official exact public 3D: not found; `source/optional-3d/README.md` records the negative result.
- Six faces: 6 prompt/source-lock rows and 6 independently generated alpha faces; left/right are distinct and not mirrored.
- Dual WebGL: 40/40 PASS; 40 GLB HTTP 200 requests; Three.js 0.179.1 and Babylon.js 8.22.2.
- Structural gates: six views PASS, standard GLB PASS, web GLB PASS, named geometry PASS.
- Bottom: conservative `GENERIC_BOTTOM_FALLBACK`; this is the only reason the result is not plain PASS.

Remaining risks:

- No trustworthy underside photograph was found after the documented official, manual, reseller, auction, video and multilingual search; the bottom is a conservative generic sheet-metal fallback.
- Unreadable serial/microprint glyphs on source labels were neutralized; label block positions, Dell/EMC branding and visible caution colors were retained.
- No exact public official Dell 3D asset was located, so both GLBs are independently authored from dimensions and visual evidence.
