# Assembly identity manifest

manufacturer: Dell Technologies (Dell EMC branding on the locked bezel)
requested_product_id: PowerEdge R7525
delivery_subject: complete-appliance
host_enclosure_model: Dell PowerEdge R7525 2U rack chassis
installed_module_model: not applicable; monolithic rack server
installed_module_count: not applicable
installed_module_positions: not applicable
front_backplane_or_drive_configuration: 24 x 2.5-inch SFF hot-plug backplane; twenty-four portrait carriers in one horizontal row; no LFF carriers
installed_drive_carrier_state: twenty-four factory-style SFF carriers present; black lower honeycomb, gray handles, orange latch rings, green status details
rear_io_or_controller_configuration: standard no-rear-drive rear wall; Riser 1 slots 1/2, Riser 2 slots 3/6, Riser 3 slots 4/5, Riser 4 slots 7/8; BOSS S2 module present; optional 9-pin serial COM card installed in Riser 3; two-port SFP-style OCP 3.0 NIC; dual RJ45 LOM; dedicated iDRAC RJ45; one USB 2.0, one USB 3.0, rear VGA, system-ID button
bezel_and_blanking_panel_state: Dell EMC LCD security bezel installed and locked; factory irregular honeycomb lattice, center DELL EMC mark, left key lock/release and upper-right LCD/navigation strip; screenshot row 9 is the appearance lock
power_and_fan_configuration: two matching 2400 W mixed-mode PSUs used as AC supplies, both installed; no PSU blank; six internal hot-plug fan modules retained as real geometry; both visible rear PSU fans/inlets/handles retained
rear_storage_state: no 2 x 2.5-inch or 4 x 2.5-inch rear drive module
rack_hardware_state: front integrated rack ears/handles only; no rear ears, rails, or cable-management arm
u_height: 2U
coordinate_convention: right-handed glTF; +X device right viewed from front, +Y up, +Z front
delivery_dimensions_mm: 482.0 overall ear width x 86.8 height x 772.13 bezel-front-to-PSU-handle depth
evidence_urls:
  - https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ism_pub/front-view-of-the-system?guid=guid-6ee4302e-d12b-4757-8230-8a26b0a428ae&lang=en-us
  - https://www.dell.com/support/manuals/en-au/poweredge-r7525/r7525_ism_pub/rear-view-of-the-system?guid=guid-5ad00271-7f31-40ac-8491-663cd8b3c6ab&lang=en-us
  - https://www.dell.com/support/manuals/en-us/poweredge-r7525/r7525_ts_pub/chassis-dimensions?guid=guid-0fe55371-3ffd-43a6-b099-f8b21d291feb&lang=en-us
  - https://www.dell.com/support/manuals/en-us/oth-r7525/r7525_ism_pub/installing-the-serial-com-port?guid=guid-cceb6074-67cb-4f28-ba1f-94eaf835d017&lang=en-us
  - https://dellarassistant.glare.kaalo.com/IC1400R752500/index.html?pid=2201AEN
  - https://www.itcreations.com/product/140713
status: VERIFIED

## Exclusion lock

- Do not use R7515 geometry, ports, rear wall, branding, or photos.
- Do not use 8/12 x 3.5-inch LFF carriers or an LFF front as configuration evidence.
- The LFF image sometimes used on Dell marketing pages may prove the removable bezel component only; it may never define the requested chassis behind that bezel.
- Do not add a rear-drive cage, GPU rear panel, DC-only PSU inlet, one-PSU/one-blank state, or rear rack ears.

