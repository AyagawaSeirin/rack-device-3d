# Assembly identity manifest

manufacturer: Dell EMC
requested_product_id: PowerEdge C6420 / 2.5-inch
delivery_subject: enclosure-with-modules
host_enclosure_model: PowerEdge C6400 (regulatory model E43S / E68S series documentation)
installed_module_model: PowerEdge C6420 air-cooled compute sled
installed_module_count: 4
installed_module_positions: rear slots 1, 2, 3, 4 all occupied; rear-screen order is sled 3 upper-left, sled 4 lower-left, sled 1 upper-right, sled 2 lower-right
front_backplane_or_drive_configuration: 24 x 2.5-inch SAS/SATA direct backplane; six front bays mapped to each sled; 24 factory 14G-style vertical drive carriers are visibly installed
rear_io_or_controller_configuration: four default C6420 rear faces; empty low-profile PCIe and mezzanine/OCP openings with factory vented blanks; no externally visible add-in NIC; each sled retains two USB 3.0, system-ID, EST tab, iDRAC Direct micro-USB, mini DisplayPort, iDRAC/NIC RJ45, rear power button, blue release handle and lock
bezel_and_blanking_panel_state: no front bezel; 24 drive carriers installed; no empty rear sled positions; no rear dummy sleds
power_and_fan_configuration: two shared hot-plug EPP 1600 W AC PSUs in the center stack; four internal 60 mm dual-rotor fans; no DC PSU and no liquid-cooling hoses
u_height: 2U
dimensions_subject: fully installed C6400 enclosure with four C6420 sleds and 24 x 2.5-inch carriers
delivery_key: Dell-C6420-2.5inch
evidence_urls:
  - user screenshot `/root/.codex/attachments/6a010f6b-ae9b-41fb-95ff-f3eb06548688/codex-clipboard-125b3551-b9d1-4a93-ac51-15efd4ea24e5.png`
  - https://www.dell.com/support/manuals/en-us/poweredge-c6400/pec6400_ism_pub/dell-emc-poweredge-c6400-overview
  - https://dl.dell.com/topicspdf/poweredge-c6400_owners-manual_en-us.pdf
  - https://dl.dell.com/topicspdf/poweredge-c6400_Owners-Manual2_en-us.pdf
  - https://i.dell.com/sites/csdocuments/Product_Docs/en/poweredge-c6400-c6420-technical-guide.pdf
  - https://www.reddit.com/r/homelabsales/comments/10s2y93
  - https://store.techyparts.com/products/dell-poweredge-c6400-24sff-4-node-c6420-dual-lga3647-h730p-x710-cto-2u-server
status: VERIFIED

## Delivery-subject decision

The row labelled `DELL C6420/2.5英寸` depicts the full rack assembly, not a standalone sled. Its front is the PowerEdge C6400 24-SFF enclosure and its rear contains four C6420 sleds plus two shared AC PSUs. Dell's installation manual independently proves the same host/module relationship, sled enumeration, 24-bay mapping, and two-PSU layout. The user screenshot's rear is the same factory default composition as Dell Figure 5 and the inspected 1600 W real photograph.

## Excluded variants

- standalone C6420 sled;
- one-, two-, or three-sled C6400 assemblies;
- C6520/C6525 sleds;
- 12 x 3.5-inch front;
- 8 NVMe + 16 SAS/SATA mixed front and expander-only arrangements;
- liquid-cooled sleds;
- 2000/2400/2600 W PSU appearance;
- rear add-in NIC/SFP/QSFP cards absent from the screenshot.
