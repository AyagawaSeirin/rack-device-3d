# Dell PowerEdge R620 10×2.5 SFF evidence

Accessed: 2026-08-23 (Asia/Singapore).

## Authoritative documents

1. Dell, *PowerEdge R620 Technical Guide* — https://i.dell.com/sites/content/shared-content/data-sheets/en/documents/dell-poweredge-r620-technical-guide.pdf
   - Page 11: official 8- and 10-drive front views and fixed chassis distinction.
   - Page 13–14: 10-drive LED/mini-USB control identity.
   - Page 30: three PCIe slots are the only rear option on the 10-drive chassis.
   - Page 31: Intel I350 4×1Gb Base-T supported.
   - Page 35: 750W AC PSU geometry and redundant pair support.
   - Page 51: 10-drive dimensions Xa 482.4, Xb 434.0, Y 42.8, Za 20.4 without bezel, Zb 731.0, Zc 752.1 mm.
   - Page 52: 750W AC electrical variants.
2. Dell, *PowerEdge R620 Owner's Manual* — https://dl.dell.com/topicspdf/poweredge-r620_owners-manual_en-us.pdf
   - Pages 14–16: exact 3-slot rear feature order and alternate NIC families.
   - Page 17: AC versus DC PSU face/indicator distinction.
   - Pages 35–36: separate removable cover and latch.
   - Pages 73–74: AC PSU connector, latch, handle, and matching-pair rule.
3. Dell HTML manual, back-panel features — https://www.dell.com/support/manuals/en-us/poweredge-r620/r620systemownersmanual-v1/back-panel-features-and-indicators

Both PDFs are preserved unchanged under `source/originals/`; full text was extracted locally because the PDF skill was unavailable, and every listed page was rendered under `source/pdf-pages/` and visually inspected at original detail.

## Exact-configuration real photography

- Cloud Ninjas R620 gallery — https://cloudninjas.com/products/dell-poweredge-r620-server
  - Exact 10SFF front, top, right-front three-quarter, open internal, and mixed-NIC rear. The mixed-NIC rear is explicitly excluded from the target.
- PC Server & Parts exact 10-bay/I350 listing — https://pcserverandparts.com/dell-poweredge-r620-10-bay-sff-server-2x-intel-xeon-e5-2670-2-60-ghz-8c-32gb-ddr3-4x-600gb-hdd-i350-h710-refurbished/
  - Listing states Dell I350 4×1Gbps RJ45; image 5 proves three ventilated PCIe blanks, four RJ45 ports, and dual 750W AC PSUs.
- IT Creations exact 10-bay/3-slot listing — https://www.itcreations.com/product/144161
  - Dynamic gallery inspected with Playwright. Exact left-side/top angles and PowerEdge R620 control-strip close-up. Its photographed rear has one PSU plus blanks and is supporting-only.
- UsedServers exact 10-bay listing — https://usedservers.ca/dell-poweredge-r620-1u-server-10-x-2-5-bay-sff.html
  - Independent elevated rear/top corroboration for quad RJ45 and dual PSUs.

## Configuration conclusion

The user screenshot and official page 11 agree on the 10-drive face. The screenshot rear, official page 30, Dell rear diagram, PC Server & Parts I350 listing, and UsedServers photography jointly lock a three-slot rear with quad RJ45 and two matching 750W AC PSUs. This is one physically valid 10-drive configuration and does not combine an 8-drive front, two-slot rear, SFP+ RNDC, or DC PSU.

## Dimension interpretation

The 482.4 mm value includes the front rack latch assemblies; the 434.0 mm body width excludes them. The 42.8 mm value is actual chassis height. Figure 14 draws both `Zb=731.0 mm` and `Zc=752.1 mm` from the EIA rack flange, while `Za=20.4 mm` runs from the bezel-absent front outermost feature to that flange. Therefore the real body depth is `Za+Zb=751.4 mm` and the installed front-to-rear envelope is `Za+Zc=772.5 mm`. The prior 752.1 mm GLB bound omitted the entire front projection and was corrected during the 2026-08-27 rotation review. Final GLB audit bounds are 482.4×42.8×772.5 mm, with a 434.0×42.8×751.4 mm main body.

## Source exclusions

All saved 8SFF images, the 8-drive Dell video still, the two-PCIe rear drawing, Cloud Ninjas mixed 2×SFP+ + 2×RJ45 rear, optional bezel photos, empty-bay photos, seller straps, cables, labels, watermarks, and backgrounds are classified and cannot override the target lock.
