# Exact underside search log

Search date: 2026-08-24

Target: Cisco `N9K-C9336C-FX2`, specifically the exterior underside. This search occurred only after chassis and installed rear configuration were verified.

Searched surfaces and query families:

- Cisco exact-model product, support, hardware guide, data sheet, media/CDN, Visio and optional 3D/CAD surfaces
- exact PID plus `bottom`, `underside`, `underneath`, `底面`, `底部`, `裏面`, `teardown`, `service`, `rail`, `rack mount`
- dynamic reseller galleries inspected with Playwright where public access allowed; ETB returned a Cloudflare 403 challenge and was not bypassed
- exact-model authorized/refurbisher galleries from ETB, PCNation/Etilize, Dedicated Networks, ServerLama, Cloud Appliances, ITinStock, Voyage Technologies and NetworkTigers
- eBay and other marketplace/used-equipment listings, including high-resolution gallery images
- Chinese and Japanese query variants
- same-family Nexus 9300/Fx and same-vendor Cisco 1U underside searches for fallback material

Result: no usable exact-model underside image, official underside drawing, public official 3D file, or exact underside video frame was found. Exact left/right/top evidence proves the outer bottom silhouette but not underside-specific holes, labels, feet, rails, fasteners, vents or stamped features.

Fallback decision: `GENERIC_BOTTOM_FALLBACK`.

Inspected fallback material:

- Generic same-vendor 1U underside photograph: https://i.ebayimg.com/images/g/V2wAAOSwI49eX9yj/s-l1200.jpg
- Local path: `source/third-party/generic-bottom-cisco-catalyst3650.jpg`
- SHA-256: `6078c4cb123138bf467c0619fb300724a7432ca69aa59961337f2b8f9957343e`

The fallback photo is a different Cisco model and is used only to establish ordinary silver sheet-metal material character. Its labels, stamped bosses, holes, vents, feet, latch openings and module layout are explicitly forbidden from transfer. The generated `bottom.png` must be a conservative blank closed sheet at the verified 439:571.5 body ratio, with no unsupported identifying or mechanical detail and no top mirroring.
