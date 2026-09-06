# Evidence by face

Original downloads and hashes: `sources/download-index.json`. Original bytes are retained. `sources/derived/` contains explicitly derived PDF page rasters and unmodified photo crops, never substituted for original evidence.

| Face/component | Confirmed | Estimated or missing |
|---|---|---|
| Front | NWR nwr-2 and macro nwr-3: exact PID, 18 double cages /36 bare sockets, two separator perforation rows, Cisco bridge, 3 chassis and 4 lane indicators/LS selector, bottom vent strip. Abacus corroborates same 36-port face. | Internal cage depth and fine contact placement estimated; no transceivers inserted. |
| Rear | NWR nwr-1, Abacus abacus-3, official 501591: 3 fans, 2 PSUs at extremes, service panel between fan3 and right PSU, matched blue exhaust. Console is upper RJ45, management lower RJ45; SFP and vertical USB-A beside lower connector; BCN/STS below. | Tiny fan/PSU label revision and hidden retention details not resolved. |
| Left | Official rear three-quarter shows physical left side; NWR shows small edge areas. Plain sheet, mounting provisions and grounding holes. | No calibrated full left real photo found; exact hole coordinates/side folds estimated from official drawings. |
| Right | Serverlama angledside and official 501590 show physical right side, mounting groups and grounding pair. | Stock photograph is low detail despite 2048 image canvas. Exact screw locations estimated. |
| Top | NWR nwr-1 and nwr-2 opposing photographs; Abacus front/rear photos; Serverlama top. Near-port perforated strip, front-left grey/yellow original label, rear screw pattern and shallow formed channels. | Minor hole count/pitch and emboss dimensions estimated. NWR removed modules obscure some lid in nwr-2. |
| Bottom | No credible exact-model underside obtained after exact PID + bottom / bottom view / top / side searches. | Entire bottom marked INFERRED, conservative closed folded sheet and fasteners. Do not copy another model's underside. |
| Mounting ears | NWR nwr-3 sharp left ear macro: 3 horizontally obround holes, solid metallic bore walls, formed corner. Official traditional N3K-C3064-ACC-KIT drawing 501768 supplies side-arm/four-screw mounting scheme. | Back wall shape, thickness, precise countersink and side-hole positions estimated. Symmetric right metal only; no mirrored lettering. |
| Fan | NWR removed modules nwr-2 and rear nwr-1: NXA-FAN-65CFM-PE marking, 3 trays, dark trapezoidal handles/paired blue tabs. Official guide confirms two counterrotating rotors per tray. | Internal rotor fine blades/fasteners are approximate and largely occluded; no invented circuit board. |
| PSU | NWR assembled and removed matching silver AC hardware. Official guide and Dedicated Networks exact-model listing support NXA-PAC-1100W-PE2. Separate 4YourBusiness images show PE2 label and internal-end layout. | Separate PE2 subrevision has dark exterior versus NWR silver; it is excluded as whole-surface material/label authority for NWR assembly. Manufacturer subrevision not asserted. |
| Printing | NWR nwr-3 sharp original Cisco bridge/control text/PID; nwr-chassis-label crop has readable PID/VID but limited microprint. | All AI text excluded. Fine labels preserve original source resolution; no fabricated serial/ratings. |

## Selection and exclusions

- Primary original set: [NW Remarketing](https://nwrusa.com/products/21504). Three 4608×3456 photos constitute one source, not three independent sources. Numerous duplicate Shopify filenames are not counted as independent evidence.
- Corroborating [Abacus item 126080121867](https://www.ebay.com/itm/126080121867): three original CDN images downloaded, though HTML request returned 403. Its ears have extra intervening round fastener provisions and therefore are excluded from ear geometry; the rest is useful independent body/rear evidence. Merchant structured metadata incorrectly says 12 LAN ports; actual photo and official 36-port count prevail.
- [Serverlama](https://serverlama.com/products/switch-cisco-nexus-9k-n9k-c9336c-fx2): same model stock photos with no ears, valid side and lid support; cannot establish selected mounting kit or PSU type.
- [Dedicated Networks](https://dedicatednetworksinc.com/product/cisco-n9k-c9336c-fx2-managed-switch-36x-100gb-qsfp28-40gb-qsfp28/): online text confirms PE2 + 65CFM-PE assembly, direct page fetch failed; claimed N2200 kit excluded. It is supporting text only, not downloaded original-photo evidence.
- [4YourBusiness PE2](https://www.ebay.com/itm/175791673150): module PID readable in downloaded original photo. Different visible manufacturer subrevision; no mixing its dark casing into NWR silver assembly.
- FX2-E, 9236C, 9336PQ, 93180YC, 93360YC search results excluded. Search results for other models are not evidence simply because they have 36 ports.
- Imagegen references are explicitly generated interpretation, never dimension/brand/port-count authority. Rejected generations remain archived with review reasons.
