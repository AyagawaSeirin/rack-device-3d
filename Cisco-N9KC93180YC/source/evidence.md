# Evidence and identity audit

Audit date: 2026-08-24 (Asia/Singapore)

Identity gate: **VERIFIED**

## Requested subject and screenshot lock

The user-provided table is preserved unchanged at `source/originals/user-screenshot.png` (SHA-256 `00861cf47eb85ee4f20fc3dc3fc850820368df4e3db7b2721b3226dfca8c1921`). The target row is preserved at `source/originals/user-screenshot-N9KC93180YC-row.png` (SHA-256 `dc4f35b16756256b9c9768a3ca2ed59bf0cc064a315ea53a39795a0fd7e01e32`).

The user subsequently fixed the exact chassis identity as **Cisco Nexus 9000 C93180YC-FX**, PID `N9K-C93180YC-FX`, and required AC power. The target rear thumbnail visibly contains two installed AC PSUs, four installed fan trays, and burgundy/dark-magenta latch pixels on all four fans. The front shows all 48 SFP28 and 6 QSFP28 cages empty, with no bezel.

## Exact installed configuration

Official Cisco FX documentation identifies two airflow families. Burgundy is port-side intake and blue is port-side exhaust; Cisco requires every fan and PSU in the chassis to have the same airflow direction. The screenshot's four burgundy fan latches lock the physical intake configuration. The preserved legacy guide names that fan `NXA-FAN-30CFM-B`; the user's final exact configuration lock specifies the ordering PID `NXA-FAN-30CFM-PI`. With user-required AC power and matched port-side intake airflow, the FX support matrix locks the power supplies as 2 × `NXA-PAC-500W-PI`.

The delivery assembly is:

- chassis `N9K-C93180YC-FX`, full 48-port base PID, 1 RU;
- front: 48 empty SFP28 cages plus 6 empty QSFP28 cages, no optics or bezel;
- rear: 4 × `NXA-FAN-30CFM-PI`, 2 × `NXA-PAC-500W-PI`;
- airflow: port-side intake, burgundy-coded;
- rear I/O: FX L1/L2 software-defined ports, BCN/STS, console, USB, and RJ-45 out-of-band management;
- front rack ears present; no rear ears inferred.

## Authoritative dimensions and visual evidence

The selected Cisco hardware guide is preserved unchanged at `source/originals/cisco-n93180yc-fx-nxos-hig.pdf`. It establishes a body envelope of 439 × 571 × 44 mm and the exact FX front/rear layout. The nominal front-ear span is modeled at 482.6 mm; each front-only ear extends about 21.8 mm beyond the 439 mm body. Relevant official pages are preserved as high-resolution renders in `source/pdf-pages/` and were inspected at original detail.

Real exact-FX used-equipment photography supplies the color/material/top/front source lock. The rear is a multi-reference reconstruction: the user screenshot binds installed PI module count/order/color; a high-resolution exact FX PE rear image supplies only FX sheet-metal, L1/L2, fan-tray, and 500W PSU geometry; an exact FX listing with loose PI modules supplies the burgundy PI color/material. Blue PE parts are explicitly excluded.

One reseller image claimed FX but visibly showed the EX management-port cluster and 650W modules. It is rejected as mismatched stock and cannot override Cisco or the screenshot.

## Bottom-face escalation

Exact-model underside, bottom, teardown, disassembly, auction, recycler, and multilingual searches found no trustworthy `N9K-C93180YC-FX` bottom photograph or diagram. The permitted bottom fallback therefore uses only generic Cisco 1RU silver sheet-metal material and a conservative folded perimeter lip. All non-exact holes, feet, rails, labels, bosses, and protrusions are forbidden. Full details are in `source/bottom-search-log.md`.

## Official/public 3D

Official Cisco support and public-web searches found no exact `N9K-C93180YC-FX` GLB/glTF/OBJ/FBX/STEP/CAD file. Cisco's public 76 MB Nexus 9000 Visio archive is 2D and was not stored as 3D. An exhaustive scan of all 214 publicly enumerated Cisco Kaon WebGL application manifests found only the distinct Nexus 93180LC-EX application and unrelated textual references, never C93180YC-FX geometry. See `source/official-3d-search-log.md`.

## Processing note

The workflow-requested PDF skill was unavailable in this session. The official PDFs were still preserved unchanged, text-extracted using Ghostscript `txtwrite`, and relevant pages rendered to PNG at 150 dpi. Every selected render was visually inspected. Playwright headless browser inspection was used for dynamic Cisco and reseller pages; preserved snapshots are under `qa/browser/`.

## Gate decision

Assembly identity is resolved and all six face-production modes are locked. The only permitted approximation is the explicitly documented bottom fallback. The expected final classification, if all modeling and QA gates pass, is `PASS_WITH_BOTTOM_FALLBACK`.
