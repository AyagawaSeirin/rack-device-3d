# Exact bottom-face search log

Access date: 2026-08-24 (Asia/Singapore)

Result: **EXACT_BOTTOM_NOT_FOUND — GENERIC_BOTTOM_FALLBACK AUTHORIZED**

## Search scope

The following exact-PID query families were searched on ordinary web search, image search, used-equipment marketplaces, recycler listings, and Cisco documentation:

- `"N9K-C93180YC-FX" underside`
- `"N9K-C93180YC-FX" bottom`
- `"N9K-C93180YC-FX" teardown OR disassembly`
- `"Cisco 93180YC-FX" underside OR bottom view`
- `"思科 N9K-C93180YC-FX" 底部 OR 拆机`
- exact PID plus `auction`, `used`, `parts`, `repair`, and `chassis`.

Official hardware-guide diagrams, Cisco support media, dynamic reseller galleries, eBay listings, image-search results, and exact-model product pages were inspected. They supply front, rear, top, and both side-edge evidence but no trustworthy underside.

## Fallback reference and strict transfer limits

`source/third-party/fallback-cisco-1u-underside.jpg` is a 2400 × 1800 real photograph of a Cisco Catalyst C9300-family 1RU underside from the same vendor ecosystem, not the target family. It is used only for generic silver sheet-metal material and a conservative folded perimeter lip.

The fallback must ignore and must not reproduce every source-specific hole, slot, foot, label, rail, boss, fastener pattern, stamping, or protrusion. The target bottom is constrained to a plain closed 439:571 plate aligned to the verified FX body silhouette, with only a shallow neutral perimeter fold. No logo, regulatory label, feet, rails, or service openings are invented.

This evidence limitation requires final status `PASS_WITH_BOTTOM_FALLBACK` if every other gate passes.
