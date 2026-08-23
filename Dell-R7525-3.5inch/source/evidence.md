# Evidence and source lineage

## Identity and configuration

The user-provided row-8 screenshot is the configuration lock. It shows a Dell PowerEdge R7525 3.5-inch/LFF front with the standard honeycomb/LCD bezel installed and a rear matching Dell Installation and Service Manual Figure 9: no rear-drive module, four riser groups/eight slot positions, and two AC PSUs at the lower corners. The adjacent R7525 SFF and R7515 rows are exclusion examples only and were not used as identity sources.

Official Dell drive specifications confirm support for `12 x 3.5-inch hot-swappable SAS/SATA drives`. Dell Installation and Service Manual page 9 Figure 4 proves the 4-column x 3-row carrier layout and left/right front controls. Pages 13-14 Figure 9 and Table 5 prove the locked rear layout and port groups.

## Dimensions

Dell's official chassis table gives, for the 12-drive R7525: Xa 482.0 mm, Xb 434.0 mm, Y 86.8 mm, Za 35.84 mm with bezel / 22.0 mm without bezel, Zb 700.7 mm from ear to rear wall, and Zc 736.29 mm from ear to PSU handle. The modeled installed envelope is 482.0 x 86.8 x 772.13 mm, where overall depth is the documented front bezel projection plus ear-to-PSU-handle length.

Primary dimension URL: https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ts_pub/chassis-dimensions?guid=guid-0fe55371-3ffd-43a6-b099-f8b21d291feb&lang=en-us

## Front sources

- User row-8 lock: `source/originals/user-row08-front.png`.
- Official Dell ISM page 9 Figure 4: `source/pdf-pages/ism-p002.png`.
- Official Dell ISM page 28 Figure 18 bezel: `source/pdf-pages/ism-bezel-p001.png`.
- Official Dell exact 12LFF service-video frames: `source/originals/official-video-frames/12lff-backplane/`.
- Exact 12LFF straight carrier photograph/render: `source/third-party/ebay-365655196804-main.jpg`.
- Exact R7525 bezel product photograph/render: `source/third-party/touchpoint-r7525.jpg`.

## Rear sources

- User row-8 lock: `source/originals/user-row08-rear.png`.
- Official Dell ISM page 13 Figure 9: `source/pdf-pages/ism-p006.png`.
- High-resolution Figure 9 derivative hosted by reseller: `source/third-party/ecs-r7525-rear-diagram.jpg`.

Rear screen-left to screen-right physical layout: PSU1; NIC1/NIC2; OCP 3.0 area; system-ID; dedicated iDRAC; USB 3.0; VGA; USB 2.0 above/near riser4; PSU2. Four riser groups and the BOSS S2 slot occupy the upper/middle rear. The optional serial DB9 card is not installed in the row-8 lock.

## Side and top sources

The Dell service video `How to Replace 3.5\"x12 HDD Backplane for PowerEdge R7525` is exact 12LFF evidence, not SFF. Public Brightcove frames were preserved unchanged under `source/originals/official-video-frames/12lff-backplane/`. Frames at 0 and 20 seconds prove the top cover, latch, front labels, right-side surface, right front control extrusion, side seams and rail/keyhole features. The left side is cross-checked from the exact R7525 12LFF-bezel Touchpoint photo and Dell bezel/service figures; it is not mirrored from the right.

Official video page: https://www.dell.com/support/contents/en-us/videos/videoplayer/how-to-replace-35x12-hdd-backplane-for-poweredge-r7525/6144984864001

## Power and cooling

Dell specifications allow two AC or DC PSUs, but the delivery is locked to two AC PSUs. The pictured Figure 9 modules are 2400 W AC units with rear fans, orange releases, and IEC inlets. No DC connector geometry is used. The visible PSU fans and six internal hot-swap fan modules are separately modeled; internal modules remain hidden by the closed cover in normal exterior views.

## PDF handling

The downloaded official PDFs were preserved unchanged. Text was extracted with Ghostscript `txtwrite`; relevant pages were rendered to PNG at 180 dpi and visually inspected. The installation/service manual pages 8-16, 28-32 and technical-guide pages 8-14 were inspected at original detail. Source hashes are recorded in the face lock and QA source audit.

## Completion classification

Five faces have exact-model/configuration evidence. The underside has no usable exact view after documented escalation; only the controlled conservative bottom fallback is used. The only acceptable final classification is `PASS_WITH_BOTTOM_FALLBACK`.

