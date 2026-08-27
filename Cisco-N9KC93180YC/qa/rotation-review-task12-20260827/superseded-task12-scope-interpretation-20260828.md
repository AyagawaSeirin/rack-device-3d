# Superseded Task-12 scope interpretation

Preserved on 2026-08-28 before correcting acceptance metadata.

The earlier report interpreted `NXA-PAC-1100W-PI2` and `NXA-FAN-65CFM-PI` as requirements for both Cisco models and therefore marked `N9K-C93180YC-FX` as `BLOCKED`, despite its model, source locks, structure and browser evidence passing for the real two-500W/four-30CFM AC configuration.

The controller clarified that those exact FRUs apply only to `N9K-C9336C-FX2`; the common requirement for all devices is AC power. This interpretation is superseded. No GLB change is needed or permitted by the corrected scope. The active 93180 status is `PASS_WITH_BOTTOM_FALLBACK`, with the exact underside remaining the sole fallback.
