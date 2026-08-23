# Search escalation log

Access date: 2026-08-23

- Counted readable screenshot rows and cropped row 13 at original resolution.
- Queried Huawei support and carrier domains for CE6851 variants, dimensions, ordering, hardware description, airflow, images, 3D, CAD, Visio, and AR.
- Used a real browser on the dynamic Huawei Info-Finder pages for both 02350JAR and 02350JAS; inspected the rendered carousel, network request 66, exact image endpoints, and 3D metadata.
- Attempted the official download button; it redirected to Huawei login. No access control was bypassed. Public per-image endpoints were used instead.
- Downloaded and visually inspected the 215-page hardware PDF and 12-page datasheet; local PDF-specific skill was unavailable, so Ghostscript `ps2ascii` plus 180-dpi page renders provided the required text-and-visual checks.
- Searched authorized/reseller/used sources, exact part numbers, Chinese terms, side/top/bottom/underside/teardown/video, and local-language variants.
- Found the REVO seven-image exact-unit gallery containing a real underside, so `GENERIC_BOTTOM_FALLBACK` is not needed.
- Searched public official and third-party sources for exact 3D files; no public exact 3D was found, and Huawei metadata explicitly returned no 3D URL.

