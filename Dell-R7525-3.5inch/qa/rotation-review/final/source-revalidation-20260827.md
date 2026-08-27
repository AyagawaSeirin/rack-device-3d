# 2026-08-27 source revalidation

## Identity and exact installed configuration

- Product identity remains Dell Technologies PowerEdge R7525, regulatory model E68S/E68S001, 2U.
- Installed front remains the 12 x 3.5-inch/LFF, 4-column x 3-row carrier configuration behind the Dell EMC honeycomb/LCD security bezel.
- Installed rear remains the no-rear-drive, four-riser/eight-position arrangement with BOSS S2 area, OCP 3.0 area, embedded NIC/iDRAC/USB/VGA groups, absent optional DB9 serial card, and two 2400 W hot-plug AC PSUs. DC connectors are excluded.
- Factory Dell EMC branding is retained. The unsupported, readable IP address formerly painted into the bezel LCD was removed; the display stays dark and unassertive because no source proves a particular runtime value.

## Current official source check

- Dell's currently indexed Technical Specifications page still identifies the 12-drive variant and gives Xa 482.0 mm, Xb 434.0 mm, Y 86.8 mm, Za 35.84 mm with bezel / 22.0 mm without, Zb 700.7 mm ear-to-rear-wall, and Zc 736.29 mm ear-to-PSU-handle.
- Dell's currently indexed Installation and Service Manual still exposes the R7525 rear component inventory and the 12 x 3.5-inch cable-routing variant.
- The unchanged official PDFs, relevant page renders, user configuration lock, exact service-video frames and exact-device secondary photographs already preserved under `source/` remain the appearance evidence. They were reread against `identity-manifest.md`, `dimension-ledger.csv`, `face-source-lock.csv`, and all 33 rows in `feature-inventory.csv`.
- A real-browser visit on 2026-08-27 was blocked by Dell/Akamai with HTTP 403; the browser evidence is retained in `qa/playwright-research/`. This is an access-control result, not an identity contradiction.

Official URLs rechecked:

- https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ts_pub/chassis-dimensions?guid=guid-0fe55371-3ffd-43a6-b099-f8b21d291feb&lang=en-us
- https://www.dell.com/support/manuals/en-us/oth-r7525/r7525_ism_pub/rear-view-of-the-system?guid=guid-5ad00271-7f31-40ac-8491-663cd8b3c6ab&lang=en-us
- https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ism_pub/cable-routing?guid=guid-be29dfa2-3779-4452-9c57-654233815d5c
- https://i.dell.com/sites/csdocuments/Product_Docs/en/dell-emc-poweredge-r7525-technical-guide.pdf

## Public exact 3D search

Dell's official PowerEdge R7525 3D Guides listing remains public and currently lists 20 interactive service experiences, including cooling-fan, PSU, system-board, riser, OCP and control-panel procedures updated through January 2026:

- https://www.dell.com/support/product-details/en-us/product/poweredge-r7525/resources/3dguides

The experiences are service viewers, not public downloadable exterior assets. No direct official GLB, glTF, OBJ, FBX, STEP, IGES, USDZ or other reusable exact-configured 12LFF exterior binary was exposed without bypassing access controls. Therefore there is no official binary to preserve; both delivered GLBs remain independently constructed and are not claimed as Dell CAD.

## Face confidence

Front, rear, left, right and top retain exact-model/configuration source locks. No usable identity-bearing exact underside was found after the documented search, so only the bottom is `GENERIC_BOTTOM_FALLBACK`; it is a closed, plain galvanized sheet with unsupported holes, labels and stampings omitted.
