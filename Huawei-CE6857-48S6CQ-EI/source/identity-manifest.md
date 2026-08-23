# Assembly identity manifest

- manufacturer: Huawei Technologies Co., Ltd.
- requested_product_id: CloudEngine CE6857-48S6CQ-EI
- frozen_full_suffix: EI
- delivery_subject: complete-appliance
- host_enclosure_model: not applicable; fixed 1U switch chassis
- installed_module_model: CE6857-EI-F-B0B / ordering part 02352CHS
- installed_module_count: 4 x FAN-031A-F fan modules; 2 x 600 W AC PAC600S12-F/PAC-600WB-F airflow-matched power modules
- installed_module_positions: fan slots 1-4 populated left-to-right on the power-supply side; PWR1 and PWR2 populated to their right
- front_backplane_or_drive_configuration: port side with 48 empty 10GE SFP+ cages in two rows of 24 and 6 empty 40/100GE QSFP28 cages in two rows of 3
- rear_io_or_controller_configuration: power-supply side with ground/ESN, CONSOLE over ETH, vertical USB and status column, four blue AIR IN FAN-031A-F modules, and two airflow-matched AC PSUs
- bezel_and_blanking_panel_state: no bezel; all 54 service cages empty; no fan or PSU blanks
- power_and_fan_configuration: unified AC; 2 x AC PSUs in 1+1; 4 x blue FAN-031A-F in 3+1; power/fan panel side intake; port-side exhaust (front-to-back in Huawei documentation)
- airflow_variant: 02352CHS, CE6857-EI-F-B0B, port-side exhaust
- u_height: 1U; chassis height 43.6 mm
- published_body_dimensions: 442.0 W x 420.0 D x 43.6 H mm
- canonical_orientation: user screenshot port side = front (+Z); power/fan side = rear (-Z); +X right as seen from the port side; +Y up
- port_module_state: all SFP+/QSFP28 cages empty; no optics, DACs, dust plugs, or cables
- rack_hardware_state: chassis side mounting-hole patterns preserved; verified power-side U-shaped rear mounting brackets/ears authored as separate geometry; no unsupported mirrored front or rear flange
- screenshot_row: twelfth readable device row in `source/originals/user-device-list.png`
- evidence_urls:
  - https://info.support.huawei.com/info-finder/search-center/en/enterprise/Switches/ce6857-48s6cq-ei-pid-23152997/web3d
  - https://info.support.huawei.com/info-finder/vue/imagelib/getPreviewImages?partNumber=02352CHQ&domain=0&lang=en&seriesPbiId=252837181
  - https://ar.ipd.huawei.com/3d-model/?product=CE6857-48S6CQ-EI&modelNumber=PARM6039&language=en_US
  - https://iq-terra.ru/upload/iblock/402/vmx06ym2910bngs6bigw73vmzok95kjj.pdf
- excluded_substitutes: CE6857 without EI; CE6857E; CE6855; CE6856; CE6860; CE6870; CE6857-EI-B-B0B / 02352CHR red port-side-intake configuration
- status: VERIFIED

The Huawei manual calls the power/fan side “Front (power supply side)”. This project follows the user's screenshot: the 48+6 service-port side is canonical `front`, and the power/fan side is canonical `rear`.
