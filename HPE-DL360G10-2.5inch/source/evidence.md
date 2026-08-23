# Evidence and provenance

Access date: 2026-08-23 (Asia/Singapore)

## Authoritative identity and dimensions

- HPE QuickSpecs, document `a00008159enw`: https://www.hpe.com/psnow/doc/a00008159enw.pdf. Local unchanged copy: `source/originals/HPE-DL360-Gen10-QuickSpecs-a00008159enw.pdf`, SHA-256 `f0d53cd92892d67c6530e61e8fb943539581f4e65a5c579a495a158139fa8173`. Text extracted to `source/pdf-pages/QuickSpecs.txt`; all pages rendered to `source/pdf-pages/quickspecs-page-*.png`. Page 2 distinguishes the standard eight-bay region from the optional +2SFF Universal Media Bay; page 6 proves the standard rear.
- HPE ProLiant DL360 Gen10 Maintenance and Service Guide, Edition 19, March 2026, part 30-BC3F38A8-409: https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=index.html. Browser-exported official PDF preserved as `source/originals/HPE-DL360-Gen10-Maintenance-Edition19.pdf`, SHA-256 `ac3a4fe8e92e7ee41b486c3520da84e38c419875c0fc165e11db0f34b8b6ea6c`. Printed page 189 proves 8SFF/UMB front structure; printed page 198 proves rear order; printed page 242 gives 4.29 x 43.46 x 70.7 cm SFF dimensions. Relevant rendered pages were inspected at original detail.
- HPE dynamic front/rear component pages and original line images:
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-A907F1AD-6041-4CD5-9C29-47DF3AC366A9.html
  - https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-CCF447DF-671D-4F37-9C1A-B88D67163C92.html
- HPE product support specification page: https://support.hpe.com/hpesc/public/docDisplay?docId=a00115362en_us&page=GUID-CF51EA3E-8026-4357-92C2-E047EBE6F004.html.

The available `pdf` skill is not installed in this session. The official PDFs were instead exported through the real HPE browser UI, text-extracted with Ghostscript `txtwrite`, rendered page-by-page with Ghostscript `pngalpha`, and visually inspected with the local image viewer. This preserves the required textual and visual PDF evidence.

## User configuration lock

`source/originals/user-config-screenshot.png` is the untouched supplied screenshot. Row 5 is isolated as `source/originals/user-row5-config.png`; its front/rear crops have SHA-256 values `a007a8...d9cb` and `5fdd8a...ed99`. It overrides family photos for variant/installed-state decisions: eight SFF positions, UMB blank/grille, no rear drive, blank PCIe/FlexibleLOM, embedded four RJ45, dedicated iLO, serial/USB/VGA, and dual AC PSU.

## Exact-device photographic evidence

- IT Pro review of Performance model 867963-B21: https://www.itpro.com/server/29565/hpe-proliant-dl360-gen10-review. The reviewed system is explicitly an eight-bay SFF DL360 Gen10. Its straight rear photo matches the user rear and is the primary rear photographic-style authority. The security bezel hides the front bays, so it is not a front identity source.
- piospartslap exact 8SFF listing: https://www.piospartslap.de/?a=22257&lang=eng. The seller explicitly identifies eight 2.5-inch SFF bays and provides multiple 2000px real photographs. These prove carrier geometry, UMB/control area, top cover, labels, vents, chassis material, ear construction, rear depth and PSU form. Its installed drives and 562FLR population differ from the user image and are not copied.
- eBay P05520-B21 exact 8SFF listing, item 327204807466: https://www.ebay.co.uk/itm/327204807466. Thirteen 1600px real photographs were preserved and inspected. They support front carrier/blank geometry, top labels and vents, side edges, rear chassis/PSU depth and material. The listing's optional card population is not copied.

## Source inclusion rules

- User row-5 front/rear determine configuration and counts.
- Exact 8SFF real photos determine material, wear, photographic character, carrier/handle construction, top/side relief and PSU form.
- Official diagrams/pages determine unambiguous port/bay order and dimensions but do not establish material/color by themselves.
- HPE official product images `s00002871` and `s00001312` show 10SFF/security-bezel alternatives and are retained only as rejected/same-family evidence; they are not binding front sources.
- No Gen9, Gen10 Plus, Gen11/Gen12, LFF, 8+2SFF, 10SFF Premium, rear-drive, DC PSU, or alternate card population may enter final geometry or textures.
- Bottom handling is documented separately in `source/underside-search-log.md` and requires `PASS_WITH_BOTTOM_FALLBACK`.

## Official 3D/CAD/AR search

No exact public official 3D/CAD/AR file was found. The search scope and the 2D Visio-only result are recorded in `source/optional-3d/README.md`.
