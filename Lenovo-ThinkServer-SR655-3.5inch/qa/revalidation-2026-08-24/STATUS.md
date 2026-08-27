# Forced revalidation status

status: REOPENED

reason:

- The prior rear `face-source-lock.csv` row named a cropped PNG but recorded the parent PDF checksum.
- The prior left/right rows did not name independent face-specific primary geometry locks, although the final images themselves are distinct and non-mirrored.
- The prior evidence report overstated the unpacked official-viewer package byte count by 148 bytes.

The prior `qa/QA_REPORT.md` PASS is historical and is not a current acceptance decision. This status remains REOPENED until source locks are repaired, current GLB hashes are audited, and both current GLBs complete the required 40 real WebGL loads.
