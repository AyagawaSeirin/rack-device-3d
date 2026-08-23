# Identity manifest — Huawei FusionServer Pro 1288H V5 4LFF

## Frozen identity

- Manufacturer: Huawei Technologies Co., Ltd.
- Official product family and model: **FusionServer Pro 1288H V5 Server**
- User-list alias: `Huawei RH1288V5/3.5-inch` (the exact official V5 documentation uses `1288H V5`; `RH1288V5` is retained only as the source-list alias)
- Huawei support product PID: `21872252`
- Regulatory/platform model encountered in certification material: `H12H-05`
- Generation: V5 / Intel Purley generation. V3, V6, `RH1288H`, `1288X V5`, `2288H V5`, and other adjacent platforms are explicitly excluded.
- Form factor: 1U rack server
- Requested front-storage variant: four 3.5-inch SAS/SATA LFF bays, one row, carriers installed, no security bezel
- Frozen rear family: three external PCIe/riser openings, FlexIO/LOM group, service I/O, and two hot-swap AC power supplies
- Frozen power configuration: **2 × 900 W hot-swap AC PSUs, 1+1 capable**; no -48 VDC, 380 V HVDC, or other DC PSU geometry
- Branding: Huawei flower mark, `HUAWEI`, and `1288H V5` product marking are retained. Unit-specific serial numbers, barcodes, asset tags, drive-capacity labels, and reseller stickers are omitted.

## Authoritative dimensions

- Body width: 436 mm
- Height: 43 mm
- Chassis depth for the 3.5-inch variant: 748 mm
- Rack-ear span: 482.6 mm target
- Coordinate convention used by the model: +X right, +Y up, +Z front

The 748 mm depth is specific to the 3.5-inch chassis. The 708 mm depth documented for 2.5-inch variants is rejected.

## Installed-state freeze

- Four LFF carrier fronts are present. They are modeled as carriers with latch/handle and ventilation structure, without inventing readable drive-capacity stickers.
- No front bezel.
- Rear expansion positions are externally closed with the evidence-matched perforated/blank riser faces; no GPU or cable is exposed.
- No power cords, network cables, optical transceivers, or rack rails are installed.
- Both AC PSU modules are present.
- Seven internal hot-swap fan modules are recorded in the evidence inventory, but only externally visible ventilation and chassis effects are modeled.

## Identity confidence

`HIGH` for model family, V5 generation, 1U height, 4LFF front, 3.5-inch chassis depth, three-riser rear family, and dual AC PSU placement. `MEDIUM-HIGH` for the frozen 900 W PSU wattage: it is matched by the exact 4LFF specimen photo set and listing, while Huawei documents 550 W, 900 W, and 1500 W AC options for the product family.

