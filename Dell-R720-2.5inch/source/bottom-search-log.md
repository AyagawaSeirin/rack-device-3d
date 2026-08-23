# Bottom-face search log

Access date: 2026-08-23.

The following exact-model searches were exhausted before invoking the bottom-only fallback:

- Dell official support manuals, technical guide, getting-started guide, B6 ReadyRails installation guide, current product support page, 3D Guides index, top-cover and rack-installation videos.
- English: `Dell PowerEdge R720 underside`, `Dell R720 bottom chassis photo`, `PowerEdge R720 regulatory underside`, `Dell R720 server bottom underside`.
- Chinese: `Dell R720 底部 服务器`, `Dell R720 底部 图片 服务器`.
- German: `Dell R720 unterseite server`.
- Exact-model reseller/used/marketplace galleries inspected: eBay item 394100550218 (all six images), ITinStock 16-SFF gallery, ServerLama 16-SFF gallery, Walmart CDN side image, Grays auction top view, SureDone rear, Recompute/BigCommerce rear, and Dell owner/technical-guide page images.
- Browser escalation: eBay and Walmart interactive pages were attempted; eBay interactive access returned HTTP 403 and Walmart returned a human-verification gate. Public image CDN objects and search-cached public page content were used without bypassing controls. ServerLama's JavaScript gallery was opened successfully and all nine public images were preserved.
- Public official 3D/CAD/AR searches: Dell support/product/media/current 3D guide, CAD/STEP/GLB/glTF/OBJ/FBX/AR queries, 3DContentCentral, GrabCAD and Sketchfab. No exact official R720 exterior model or downloadable official CAD/AR asset was located.

No usable exact R720 underside photograph or diagram was found. The bottom therefore uses `GENERIC_BOTTOM_FALLBACK`: a conservative, plain, opaque galvanized sheet-metal plate at the verified 444:684 body ratio. It contains no logo, service label, vent, hole, foot, rail, seam, fastener or protrusion not established by side silhouette evidence. Final status must be `PASS_WITH_BOTTOM_FALLBACK`, never ordinary `PASS`.
