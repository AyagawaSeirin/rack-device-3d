# User-authorized assembly correction

Date: 2026-08-23

The original user table row paired a correct RH2288 V3 24-SFF front with a rear image from another appliance. The pre-build gate correctly stopped as BLOCKED. The user has now explicitly authorized treating that rear thumbnail as a table-image mistake and selecting the official RH2288 V3 rear.

Corrected assembly:

- Huawei FusionServer RH2288 V3 / H22M-03.
- 24 x 2.5-inch front, slots 0-23.
- No rear disks; the Issue 32 guide states the 24-disk configuration does not support rear disks.
- Standard official rear I/O/PCIe/flexible-NIC arrangement.
- Two hot-swap AC PSUs stacked vertically at the same rear side.
- Real Huawei/FusionServer/RH2288 V3 branding retained.

The rejected rear remains evidence of the table error only. It is excluded from every image-generation and modeling input role.
