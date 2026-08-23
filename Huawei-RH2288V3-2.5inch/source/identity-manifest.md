# Assembly identity manifest — corrected and frozen

manufacturer: Huawei Technologies Co., Ltd.
requested_product_id: FusionServer RH2288 V3
official_nameplate_model: H22M-03
delivery_subject: complete-appliance
host_enclosure_model: RH2288 V3 2U 2.5-inch chassis
installed_module_model: not applicable
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 24 x 2.5-inch front backplane, slots 0-23, 24 carrier/filler fronts, no security bezel
rear_io_or_controller_configuration: official standard RH2288 V3 rear matching the locked exact photograph; no rear disks; I/O module 1, I/O module 2, onboard slots 4/5, two-port flexible NIC marked A1/A2, USB 3.0, Mgmt, LAN, VGA, serial
bezel_and_blanking_panel_state: no security bezel; front carriers installed; unused PCIe positions use factory perforated blank covers
power_and_fan_configuration: two hot-swap AC PSUs in 1+1 redundancy, stacked vertically at the official rear right; AC inlets and green/yellow release handles; four internal hot-swap fan modules are not externally exposed
u_height: 2U
body_width_mm: 447
overall_width_mm: 482.6 rack mounting span; body and ears modeled separately
height_mm: 86.1
body_depth_mm: 708 for the official 2.5-inch chassis
overall_depth_mm: 708 body plus measured front/rear protrusion relief; final GLB documents relief tolerance
evidence_urls:
  - https://support.huawei.com/enterprise/en/servers/rh2288-v3-pid-9901877
  - https://www.doit.com.cn/subject/hcc2015/pdf/7.pdf
  - https://www.nforce.com/files/Huawei%20FusionServer%20RH2288%20V3%20Data%20Sheet.pdf
  - https://pdfcoffee.com/user-manual-rh2288-v3-pdf-free.html
  - https://img2.zol.com.cn/product/146/150/cejpY66MME9Z2.jpg
status: VERIFIED
delivery_status: PASS_WITH_BOTTOM_FALLBACK
standard_glb: model/Huawei-RH2288V3-2.5inch.glb
web_glb: model/Huawei-RH2288V3-2.5inch-web.glb
official_optional_3d: not found in public exact-PID search

## User correction

The user explicitly classified the original row-7 rear thumbnail as a table-image error and authorized the official compatible RH2288 V3 rear. The old BLOCKED manifest, report, audit, source locks and conflict image are retained under `qa/repair-before-user-correction/`. The corresponding VERIFIED transition record is frozen under `repair-official-rear/`.

The corrected delivery subject is internally consistent: RH2288 V3/H22M-03, 24 x 2.5-inch front, no rear disks, standard official I/O/PCIe panel, and two AC PSUs stacked on the same rear side.

## Final front lineage correction

The initial corrected build used a directly rectified merchant photograph for the front texture. That state is retained under `repair-imagegen-front/before/`. The final front is now a built-in ImageGen source-locked generation based on the exact 24-SFF photograph and Huawei whitepaper Figure 4-4. It contains exactly 24 carriers, the correct asymmetric left/right operator controls and the retained Huawei/RH2288 V3 identity. Only feature-free top and bottom chassis edge rails were extended to restore the verified 482.6:86.1 silhouette; no identity-bearing feature was synthesized or rescaled by that repair.
