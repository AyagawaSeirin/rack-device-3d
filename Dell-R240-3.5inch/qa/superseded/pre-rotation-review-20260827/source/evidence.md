# Evidence and inclusion rules

Access date: 2026-08-23 (Asia/Singapore)

## Binding configuration

The user screenshot fifth readable device row says `DELL R240/3.5英寸` and shows the 1U no-bezel, four-carrier hot-swap front plus the standard single-fixed-PSU rear. Dell Technical Guide page 11 separates the four hot-swap carrier design from the visually different four-drive cabled design; the user row matches the hot-swap figure. Page 13 shows the matching four-drive backplane assembly and four individual fan modules. Page 24 states the power subsystem is non-redundant and accepts one cabled 250 W Bronze or 450 W Platinum AC PSU. Page 31/32 supplies the 482.0/434.0/42.8/22.0/534.496/573.596 mm dimension ledger.

The exact delivery subject is frozen in `identity-manifest.md`. R240 cannot accept the R340 dual-redundant PSU rear. The literal dual-PSU appearance is therefore excluded as an impossible hybrid; the requested AC-powered installed state is represented with the single installed fixed 250 W Bronze-style exterior cross-locked by the screenshot, official guide, ServeTheHome and exact 4LFF seller photographs.

## Official sources

- Dell EMC PowerEdge R240 Technical Guide, June 2021 Rev. A03: https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r240-technical-guide.pdf. Original PDF preserved unchanged; extracted text and visually inspected renders for pages 1, 11, 12, 13, 14, 24, 31 and 32 are under `source/pdf-pages/`.
- Dell Australia R240 product page: https://www.dell.com/en-au/shop/dell-poweredge-servers/poweredge-r240-rack-server/spd/poweredge-r240/4er2400301auoo. HTML preserved unchanged. It proves the archived official gallery and image-CDN names. Its downloaded `above-lf` and `rear` PSD-render responses contain duplicated/layer-composited equipment and are rejected as generation inputs; they remain preserved, never silently repaired or used as face identity sources. The official internal-top response is usable and supports chassis layout, four fans, single PSU and shell edges.
- Dell support technical specifications: https://www.dell.com/support/manuals/en-us/poweredge-r240/per240_ts_pub/chassis-dimensions?guid=guid-023bf937-6846-4a75-9b5f-76e7461462ea&lang=en-us.
- Dell Installation and Service Manual rear view: https://www.dell.com/support/manuals/en-us/poweredge-r240/per240_ism_pub/rear-view-of-the-system?guid=guid-70bdc3e2-3d17-4c23-9822-6d1650e69dba&lang=en-us. Browser access returned 403, while the public semantic page and Technical Guide provide the same numbered rear inventory.
- Dell support video index and top-cover topic: https://www.dell.com/support/contents/en-us/videos/videoplayer/how-to-replace-top-cover-for-poweredge-r240/6079770014001. The topic proves exact-model service coverage; browser delivery was access-denied, so it is not a face-generation input.

## Exact-model real photographs and video

- ETB exact 4 x 3.5-inch hot-swap listing: https://www.etb-tech.com/dell-poweredge-r240-1x4-3-5-1-x-e-2224-3-4ghz-quad-core-32gb-4-x-12tb-7-2k-sata-perc-h330-idrac9-basic-svr-r240-005.html. `etb-r240-4lff-front.jpg` is the primary binding real front photograph; `etb-r240-4lff-angle.jpg` is the primary physical-right-side/three-quarter source; `etb-r240-4lff-rear.jpg` cross-checks the standard rear and single PSU.
- NewServerLife exact R240 4LFF page: https://newserverlife.com/configure/dell-poweredge-r240_4lff/. `nsl-r240-4lff-back.jpg` is the primary binding real rear photograph. `nsl-r240-4lff-top.jpg` and `nsl-r240-4lff-up.jpg` prove top-cover seams, latch, front carrier pattern and absence of a security bezel.
- TechMikeNY exact 4-bay 3.5-inch listing: https://techmikeny.com/products/dell-poweredge-r240-server-4-bay-lff-4-00ghz-6-core-24gb-ram-40tb-hdds-rails. Dynamic gallery inspected with Playwright and full-resolution Shopify images preserved. The `TECHMIKENY` top sticker, studio rail kit and seller surroundings are excluded. The photos prove top cover, physical-right shell, front relief, standard rear and one fixed 250 W Bronze AC PSU.
- ServeTheHome R240 review: https://www.servethehome.com/dell-emc-poweredge-r240-review-1u-entry-server/. Exact real-photo crops prove rear I/O, blanking-plate form, 250 W PSU label and four-fan internal layout. The front photo has the optional security bezel and is supporting only, not the requested front state.
- Cloud Ninjas exact chassis comparison video: https://www.youtube.com/watch?v=FGw0nzLS6rU. Full public video preserved as `cloudninjas-r240-chassis-overview.mp4` with metadata JSON. Selected inspected frames prove the hot-swap 4LFF carrier front, identical top-cover shell, four fans/backplane layout and the standard single-PSU rear. The compared 2-bay/cabled unit is not used for front identity.
- Garland exact 4LFF listing: https://www.garlandcomputers.com/product/dell-poweredge-r240-1u-server-e-2134-3-5ghz-16gb-perc-h330-4x-lff-trays/. Low-resolution WebP images are exact-model corroboration only; their artifacted/chroma surroundings preclude primary use.
- Dell same-vendor 1U generic underside material reference: https://cdn.awsli.com.br/2500x2500/2619/2619846/produto/244189486/servidor_dell_poweredge_r210_07-g4iahg6844.jpg. Used only under the controlled bottom fallback, never as R240 geometry.

Every local raster listed in `image-inspection-log.csv` was opened with original-detail image inspection before a role was accepted. Every seller sticker, cable, rail, hand, tabletop, backdrop, configuration-specific capacity sticker and non-factory overlay is excluded. Genuine `DELL EMC` and `PowerEdge R240` branding is required in its real pull-tag position.

## Face decisions

- Front: `SOURCE_LOCKED_GENERATION`; exact near-front real photograph exists.
- Rear: `SOURCE_LOCKED_GENERATION`; exact straight real photograph exists.
- Right: `MULTI_REFERENCE_RECONSTRUCTION`; exact physical right shell is visible across multiple exact 4LFF angles but no direct orthographic face photograph exists.
- Left: `MULTI_REFERENCE_RECONSTRUCTION`; exact top/inside/rear photographs and the Dell dimension side outline jointly prove the closed left silhouette and material. The output is independently constructed and is not a mirrored right face.
- Top: `MULTI_REFERENCE_RECONSTRUCTION`; multiple exact exterior angles and an exact top-cover video frame jointly prove the cover.
- Bottom: `GENERIC_BOTTOM_FALLBACK`; see `bottom-search-log.md`.
