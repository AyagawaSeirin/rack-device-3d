# Bottom-face search exhaustion and controlled fallback

Accessed: 2026-08-23 (Asia/Singapore)

Exact-model searches performed:

- HPE product catalog, HPE Support Center manuals, QuickSpecs, Parts Support Guide, product media IDs, Product Bulletin, PartSurfer, Visio references, and dynamic document galleries.
- English searches: `HPE DL360 Gen10 underside`, `bottom view`, `bottom chassis photo`, `8SFF barebone`, `867959-B21 underside`.
- Japanese/Chinese searches: `DL360 Gen10 底面`, `DL360 Gen10 サーバー 底面`, and exact-model marketplace variants.
- Third-party sources: IT Pro review, piospartslap exact 8SFF listings, current eBay 8SFF listings with 13-image and 3-image galleries, authorized/refurbished shops, rail-installation documentation, and used-equipment listings.
- Video/service-manual leads were checked for bottom geometry; available visuals cover top, open interior, front, rear, rail attachment, and side edges, not the closed underside.

Result: no usable exact DL360 Gen10 8SFF underside photograph or official underside drawing was found. Front, rear, left/right silhouette, top, configuration, and dimensions are otherwise verified.

Fallback mode: `GENERIC_BOTTOM_FALLBACK`. The imagegen input set uses inspected exact-model top/edge photographs only to lock galvanized sheet-metal color and edge treatment. The bottom is intentionally non-identifying: no labels, logos, vents, holes, feet, rails, seams, fasteners, or protrusions are invented. It cannot change the verified side silhouette. Final status must be `PASS_WITH_BOTTOM_FALLBACK`.
