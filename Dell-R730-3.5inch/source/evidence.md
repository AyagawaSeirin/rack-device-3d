# Evidence, lineage and inclusion rules

## Identity lock

The authoritative user lock is `source/originals/user-row12-r730-lff.png`. It shows Dell `R730/3.5英寸`, eight LFF carriers in 2 × 4, no security bezel, a standard R730 rear without rear drive bays, seven PCIe positions, four-NIC NDC area and two PSUs. This excludes R730xd, SFF, R720 and alternate rear assemblies.

## Official sources

1. Dell PowerEdge R730 Owner's Manual (Rev. A05), original official document preserved through a byte-preserving public mirror at `source/originals/Dell-PowerEdge-R730-Owners-Manual.pdf` after the direct `dl.dell.com` route returned 403. Rendered pages 10, 16, 27, 71 and 72 prove the 8 × 3.5 front option, standard rear group order, dimensions, top-cover form and removal direction.
2. Dell PowerEdge R730 and R730xd Technical Guide v1.7, downloaded from Dell and preserved at `source/originals/Dell-PowerEdge-R730-R730xd-Technical-Guide-v1-7.pdf`. Page 13 distinguishes R730 from R730xd and confirms R730 supports 8 × 3.5; page 14 proves the standard R730 rear versus the R730xd rear; pages 57-59 prove dimensions, 3.5-chassis identity and AC PSU options.
3. Dell R730 specification sheet at `source/originals/Dell-PowerEdge-R730-Spec-Sheet.pdf` confirms 2U, 44.40 × 8.73 × 68.40 cm body dimensions and 8 × 3.5 support.
4. Dell live manual topics:
   - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/35-inch-hard-drive-chassis?guid=guid-cf7676b4-eb53-47a8-8ffb-34a74ca4f4a4&lang=en-us
   - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/back-panel?guid=guid-1dc323f8-8173-4723-8bac-b781cdb7fc9b&lang=en-us
   - https://www.dell.com/support/manuals/en-us/poweredge-r730/r730_ompublication/chassis-dimensions?guid=guid-9f567556-3e45-41f8-bece-bd67cb41383e&lang=en-us

## Exact 8LFF real-photo sources

- eBay item 387258968614: exact Dell PowerEdge R730 8LFF; front, rear and top photographs preserved unchanged under `source/third-party/ebay-387258968614-*`. Images 2, 4 and 5 are the binding front/rear/top style references. Seller watermark and background are excluded during reference-guided generation; the server's real material character is retained.
- Amazon product B08D2B1NK7 via Manuals+: exact R730 8LFF exploded/front-right/top/rear photographs preserved under `source/third-party/amazon-B08D2B1NK7-*`. Image 4 proves right-side sheet metal, seam, holes and mounting studs; image 5 corroborates rear group order.
- Cloud Ninjas video `OSV3PdYySjM`: explicitly compares 8 Bay SFF, 8 Bay LFF and 16 Bay SFF. `t060`, `t200` and `t210` frames identify the center/lowest 8LFF server. `t230`-`t250` prove the standard rear with 1100 W AC option; they corroborate geometry but do not override the screenshot-locked 750 W photographed rear.
- Bob Pellerin video `CVg_X-OO9Kc`: the same physical R730 8LFF unit is shown with the eight LFF openings, top cover, both internal side walls, standard rear, four RJ45 ports and two 750 W AC PSUs. `t090`, `t420`, `t450` and `t510` are retained as primary supporting frames.
- eBay item 182270992348: exact R730 8 × 3.5 bare chassis packaging/top sources; retained only to corroborate 8LFF identity and cover material, not used for installed rear configuration.

## Dimension interpretation

`Xa=482.4 mm` is the overall rack-flange width; `Xb=444.0 mm` is the body width; `Y=87.3 mm` is actual chassis height; `Zb=684.0 mm` is the body depth reference; `Zc=723.0 mm` includes the farthest rear feature; `Za=18.0 mm` is the bezel-absent front projection. The model body is built at 444 × 87.3 × 684 mm, with front ears/control/handles and rear PSU handles extending to the overall envelope. No shipping dimension is used.

## Face lock decisions

- front/rear/top: `SOURCE_LOCKED_GENERATION` from direct exact-device real photographs.
- right: `MULTI_REFERENCE_RECONSTRUCTION` because the direct evidence is a high-resolution front-right photograph rather than a flat elevation; exact top/rear/video views jointly bind its features.
- left: `MULTI_REFERENCE_RECONSTRUCTION`; no straight face photo exists, but the exact 8LFF videos expose both non-mirrored side walls and top edges while the official cover-removal view constrains the seam. No right-side pattern is copied.
- bottom: `GENERIC_BOTTOM_FALLBACK` after the documented exhaustion search; conservative and non-identifying.

Every selected raster source and rendered PDF page was inspected at original/high detail before being assigned a role.

