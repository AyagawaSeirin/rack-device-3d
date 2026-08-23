# Evidence and source lineage

Access date for web sources: 2026-08-23. All local source images and rendered PDF pages were visually inspected at original/high detail before being assigned a role.

## User configuration lock

- URL: user attachment
- local path: `source/originals/user-config-lock-screenshot.png`
- SHA-256: `7efb5b4ccf0095fee7977f6a95083306935b9e63a990fd83bb8883fc49fdfeb9`
- claimed model: row 4, `HPE DL360G10/3.5英寸`
- authority: user configuration lock
- visual origin: screenshot containing front/rear product render thumbnails
- proves: 4LFF physical front; no bezel; four carrier fronts; exact rear overview configuration with three PCIe regions, quad RJ45 FlexibleLOM, quad embedded RJ45, serial, iLO, USB, VGA, and dual AC PSU
- limitation: thumbnail scale does not prove small label glyphs, side/top/bottom, or the internal controller SKU

## HPE QuickSpecs a00008159enw

- URL: https://www.hpe.com/psnow/doc/a00008159enw
- saved PDF: `source/originals/HPE-a00008159enw-DL360-Gen10-QuickSpecs.pdf`
- saved extracted text: `source/originals/HPE-a00008159enw-DL360-Gen10-QuickSpecs.txt`
- PDF SHA-256: `f0d53cd92892d67c6530e61e8fb943539581f4e65a5c579a495a158139fa8173`
- authority: official HPE
- source class: QuickSpecs PDF
- relevant visual pages:
  - `source/pdf-pages/quickspecs-p04.png`, SHA-256 `902e44f5d2f502a665c8532d02fb5008bd6c4f6f5af2a326a34ae94c03678cd7`: exact 4LFF front and top/front angle, ODD/display blank state, standard SID, four carriers
  - `source/pdf-pages/quickspecs-p05.png`, SHA-256 `bc268dd3c2e6dbc0e116f01e708e0c8631ccf3f1162c3a329abaf256a3c54da0`: internal view, type-a Smart Array, primary/secondary risers, up to two PSUs, seven-fan/two-processor arrangement
  - `source/pdf-pages/quickspecs-p06.png`, SHA-256 `067e89865ddea343c9827374479ad6d7d4318963e5c91fa7eac073cc67f238ae`: exact locked rear; 500W/94% labels; embedded 4x1GbE; four-port FlexibleLOM; serial/iLO/USB/VGA; PCIe slot 3; no rear drive
  - `source/pdf-pages/quickspecs-p60.png`, SHA-256 `f861a04538c8f47a64e59a7cbf6561391cc048c32911bff21a5c07fb2928da82`: 4LFF bay numbering and rear drive exclusion
  - `source/pdf-pages/quickspecs-p61.png`, SHA-256 `99e79b856e98a2ab988eaa054b244e5d2e9cc68549a27e1f9e76e51f6f572b19`: 4LFF dimensions and AC input ranges
- proves: 1U; LFF dimensions 42.9 x 434.6 x 749.8 mm; exact front/rear overview; 500W Platinum AC option and 100-240 VAC; all models include Smart Array S100i and documented hardware RAID options including P408i-a; two PSUs and two-processor/secondary-riser state are valid
- limitations: overview photos have numbered callouts and perspective; model configuration is an official shown assembly rather than a single factory BTO SKU

### Dimension interpretation

- HPE-published 4LFF body/system dimensions are 42.9 x 434.6 x 749.8 mm.
- The front rack ears are independent parts. Their 482.6 mm overall span is the standard 19-inch mounting width and yields 24.0 mm extension per side over the HPE body, cross-checked against the exact front and three-quarter sources.
- The final GLB bounds are 482.6 x 43.2 x 751.75 mm. The additional 0.3 mm height and 1.95 mm depth are the deliberately modeled visible relief/PSU-handle envelope, not chassis rescaling; the structural audit reports 0.3783% nonuniform ratio error and passes.

## HPE ProLiant DL360 Gen10 Server User Guide a00105399en_us

- URL: https://support.hpe.com/hpesc/public/docDisplay?docId=a00105399en_us&docLocale=en_US
- saved PDF: `source/originals/HPE-a00105399en-us-DL360-Gen10-Server-User-Guide.pdf`
- saved extracted text: `source/originals/HPE-a00105399en-us-DL360-Gen10-Server-User-Guide.txt`
- PDF SHA-256: `49edfbabaa5204ce55b9f03157af2876436321d7ed0fc5f0da2f18d98d950633`
- authority: official HPE
- source class: user/installation guide
- directly downloaded diagrams:
  - `source/originals/hpe-user-guide-front-4lff.png`, SHA-256 `56910e79944cf75ac4fd62c28ddbe0426fd597a1c68d5afaa6e49eb740874d4a`
  - `source/originals/hpe-user-guide-rear-panel.png`, SHA-256 `4eed5bac5c49cb0aefb350fd05fefc9af1339a1f1ddcbc6609503bb036b72b45`
- inspected rail/side pages:
  - `source/pdf-pages/user-guide-p074.png` and `p075.png`: four side rail engagement spools per side and side-wall outline
  - `source/pdf-pages/user-guide-p082.png` and `p083.png`: J-slot/spool mounting and rear-side silhouette
- proves: official front/rear component identities; left-to-right rear port families; rack rail side interfaces; absence of rear rack ears; supported 4LFF-to-P408i-a cabling path
- limitations: most illustrations are technical line art and do not establish color/material; side drawings are configuration-common and are combined with exact 4LFF real photos and exact LFF depth

## HPE standard-model identity

- URL: https://support.hpe.com/hpesc/public/docDisplay?docId=a00018806en_us&docLocale=en_US
- authority: official HPE
- source class: Product Information Reference
- proves: `867958-B21` is the HPE DL360 Gen10 4-LFF CTO server with embedded-LOM generation; `P19765-B21` is the later 4-LFF Network Choice CTO and is not allowed to replace the screenshot rear

## Exact 4LFF real photographs

### retail.era P19765-B21 unit

- URL: https://retail.era.ca/products/hpe-proliant-dl360-gen10-1u-3-5-1x-gold-6138-32gb-ddr4-ram-e208i-a-sr-gen10-10g-2x500w
- authority: secondary used-equipment seller
- source class: exact-unit real photographs
- selected files:
  - `source/third-party/era-4lff-01-900x2000.png`, SHA-256 `9a7d76adb5441406f59b3ac4495cbb4a2be178fb246782d31377d11e81462174`: exact top with access cover, latch, vents, front fixed LFF section, labels, wear and both front ears
  - `source/third-party/era-4lff-02-2000x900.png`: rear angle with dual 500W AC PSUs; rear adapter arrangement differs from user lock and is excluded from rear identity
  - `source/third-party/era-4lff-05-900x2000.png`: opened exact 4LFF internal view
  - `source/third-party/era-4lff-06-2000x901.png`: exact empty 4LFF front frame; carrier state differs and is excluded from front identity
  - BIOS photos `era-4lff-03`/`04`: Product ID `P19765-B21`, E208i-a and 640FLR-SFP28 prove the photographed unit identity but also prove why its rear cannot replace the screenshot rear
- proves: exact 4LFF chassis/top/edge material and wear; dual 500W PSU mechanics; physical depth family
- limitations: Network Choice rear, E208i-a and SFP28 FlexibleLOM differ from locked rear; photos are not used for those features

### ETB Technologies exact 4LFF angle

- URL: https://www.etb-tech.com/hpe-proliant-dl360-gen10-4lff-1-x-bronze-3106-1-7ghz-8-core-32gb-s100i-ilo5-standard-svr-dl360g10-002.html
- direct image path: `source/third-party/etb-tech-4lff-angle.jpg`
- SHA-256: `afcd52abe664377113c649e632c511930197162d3111408d6f8ad94158985cb0`
- authority: secondary refurbished-equipment seller
- source class: exact-model real photograph
- proves: exact 4LFF right-side front ear, side-wall seam, rail studs/recesses, front carrier envelope, top-cover return and LFF depth
- limitations: page itself was Cloudflare-blocked in interactive Browser; the public Cloudinary image and indexed exact-product metadata were accessible. Rear/internal S100i state is not used to override the lock.

## Exact elevation support

- MyDraw URL: https://www.mydraw.com/shape-libraries-networking-equipment-hewlett-packard-enterprise-pro-liant-hpe-pro-liant-dl
- files: `source/third-party/mydraw-dl360-gen10-4lff-front.png` and `mydraw-dl360-gen10-rear.png`
- visual origin: low-resolution transparent 2D equipment stencil derived from HPE/Visio family material
- proves: non-mirrored straight elevation and screenshot similarity
- limitation: 150 x 15/14 product pixels after trim; supporting orientation only, never material or small-feature authority

- 4RGroup URL: https://4rgroup.com/sanpham/maychuhp-DL360-G10-4LFF-CTO.html
- selected file: `source/third-party/4rgroup-rear-standard.png`
- proves: the exact HPE QuickSpecs locked rear at larger direct elevation scale
- rejection: `source/third-party/4rgroup-front-4lff.png` is actually an 8SFF front despite the page text and filename. It is preserved as a rejected source and must never enter imagegen or the GLB.

## Source/search exceptions

- PDF skill availability: no PDF skill/tool was available in the environment. Ghostscript `txtwrite` and high-resolution PNG rendering were used as the documented equivalent; every relevant render listed above was inspected visually.
- official 3D: see `source/optional-3d/README.md`; none found.
- bottom: no exact underside found after official, dynamic Browser, reseller, used-equipment, marketplace, auction and multilingual searches. Final bottom mode is the documented conservative `GENERIC_BOTTOM_FALLBACK`.

## Final evidence status

- identity: VERIFIED
- front: VERIFIED by user lock + official QuickSpecs + official guide + exact real angle
- rear: VERIFIED by user lock + source-locked official QuickSpecs rear + guide
- left: VERIFIED reconstruction inputs (official rail/side diagrams + exact 4LFF top/edge photos + dimensions)
- right: VERIFIED reconstruction inputs (exact 4LFF right-side angle + official diagrams + dimensions)
- top: VERIFIED by exact-unit 4LFF real photograph + official overview
- bottom: GENERIC_BOTTOM_FALLBACK
- expected completion class: PASS_WITH_BOTTOM_FALLBACK
