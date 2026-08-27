# Evidence, source matrix, and search log

Accessed on 2026-08-23 unless noted. The delivery subject is the complete 1U **HPE ProLiant DL360 Gen9 755258-B21 8SFF** appliance fixed by the user screenshot's seventh row.

## Official identity, dimensions, and configuration

- HPE QuickSpecs, `c04346229`: https://www.hpe.com/psnow/downloadDoc/HPE%20ProLiant%20DL360%20Gen9%20Server-c04346229.pdf?form=false&hf=slim&id=c04346229.pdf&isFutureVersion=true&preview=false&servePdfFile=true&ver=44
  - Proves 755258-B21 is the 8SFF CTO chassis, HPE Quick Release ears, 8 SFF hot-plug backplane, Embedded 4-port 331i, two PCIe slots with optional third riser, FlexibleLOM, and supported Flex Slot PSU families.
  - Publishes 8/10SFF system dimensions as 4.32 x 43.47 x 69.85 cm.
  - The HPE endpoint intermittently failed direct local download; authoritative fields were cross-checked through the HPE support HTML/API result and the downloaded maintenance manual. URL is preserved without fabricating a local copy.
- HPE Maintenance and Service Guide, `767928-008`, November 2016, Edition 8: https://support.hpe.com/hpesc/public/api/document/c04441985?v=1771326120000
  - Preserved unchanged as `source/originals/hpe-dl360-gen9-maintenance-service-c04441985.pdf`, SHA-256 `901681fda18339500580d0d8c0973a697de57027acf3f0ac76a766e5d1bf9d8c`.
  - PDF page 16: top cover/chassis/ear exploded geometry.
  - PDF page 83: exact 8SFF 6+2 carrier layout and Universal Media Bay.
  - PDF page 84: front control LEDs/buttons.
  - PDF page 88: exact rear component order.
- HPE Identifying Components: https://support.hpe.com/hpesc/public/docDisplay?docId=c04444501&docLocale=en_US
  - Proves front components and rear PCIe/PSU/VGA/NIC/iLO/serial/USB/FlexibleLOM identities.
- HPE Specifications: https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-c04443049
  - Confirms 43.2 x 434.7 x 698.5 mm for 8/10 SFF.

## Exact-model color and geometry sources

- Express Computer Systems exact 755258-B21 photo/page: https://expresscomputersystems.com/products/755258-b21
  - Real 8SFF front, all eight carriers, HPE ears, Universal Media Bay, no security bezel. Primary front photo.
- ITinStock exact DL360 Gen9 8-bay rear/top: https://www.itinstock.com/hp-proliant-dl360-gen9-8c-e5-2630v2-260ghz-2-x-600gb-hdd-8-bay-1u-rack-server-86606-p.asp
  - Real rear/top with PCIe blanks, FlexibleLOM blank and dual 500W AC PSU. Primary rear photo.
- UsedServers exact DL360 Gen9 8x2.5 page/image: https://www.usedservers.com/hpe-proliant-dl360-gen9-8x-2-5-1u-server/
  - Real elevated rear/top; target-incompatible expansion/wattage details used only for top and PSU form.
- Cloud Ninjas dynamic configurator: https://cloudninjas.com/products/hpe-proliant-dl360-gen9-1u-server
  - Inspected in a real browser; switched chassis selector to `8 Bay SFF`. Gallery supplied exact front-right/top and rear-left/top views. The source page explicitly lists the rear USB, VGA, serial, iLO, four embedded RJ45, FlexibleLOM bay and two hot-swap PSU bays.
- VisioCafe Visual Solution Document: https://visiocafe.info/downloads/hp/documents/VSD-DL360Gen9.pdf
  - Preserved under `source/third-party/`; page 1 names CTO 755258-B21 and supplies exact front/rear colored elevations and option maps. Supporting technical evidence only.

## Configuration-lock interpretation

The user crop `qa/reference/user-config-lock-row7.png` is the highest authority for the requested row/variant and dual-PSU state. It is too small and resampled to define bay geometry. Official HPE PDF page 83 and exact 755258-B21 photos prove that Gen9 8SFF is not eight portrait slots: it is six horizontal Smart Carriers in a 2x3 block plus two horizontal carriers below the Universal Media Bay. Modeling follows the official exact chassis, not thumbnail interpolation.

The rear is frozen to the user's no-card/dual-AC state: three PCIe blanking plates, FlexibleLOM blank, USB pair, serial, iLO, embedded four-port NIC, VGA and two matched 500W AC PSUs. Photos showing one PSU, an empty PSU bay, 800W labels, DC input, installed PCIe cards or an installed FlexibleLOM adapter are only supporting geometry sources and do not alter the lock.

## Six-face evidence status

- Front: exact real photo + official HPE elevation + user lock: `SOURCE_LOCKED_GENERATION`.
- Rear: exact real photo + official HPE elevation + user lock: `SOURCE_LOCKED_GENERATION`.
- Physical left: exact rear-left/top real photo plus official exploded view: `MULTI_REFERENCE_RECONSTRUCTION`.
- Physical right: exact front-right/top real photo plus official exploded view: `MULTI_REFERENCE_RECONSTRUCTION`.
- Top: two exact-model elevated real photos plus official cover diagram: `MULTI_REFERENCE_RECONSTRUCTION`.
- Bottom: `GENERIC_BOTTOM_FALLBACK`; keep a plain closed sheet preserving verified width/depth/material/side silhouette, with no unsupported labels, holes, vents, feet, rails, seams or protrusions.

## Bottom search-exhaustion log

Searched HPE manuals, HPE support/media, the HPE exploded-view resource, HPE parts pages, QuickSpecs, public/dynamic gallery resources, VisioCafe, exact-model retailer/refurbisher/used-server galleries, review pages, videos/search results, marketplaces and multilingual queries in English, Chinese, Japanese, German and Russian using `underside`, `bottom`, `under`, `底面`, `底部`, `Unterseite`, and `снизу`. Browser-assisted inspection of the dynamic Cloud Ninjas 8SFF gallery found top and both side angles but no underside. No usable exact-model underside photo or official mechanical underside drawing was found. The sole allowed bottom exception is therefore invoked.

## Official 3D/CAD/AR result

No exact public official 3D/CAD/AR file was found. See `source/optional-3d/README.md`. No Gen10, generic CAD or third-party mesh is being substituted.

