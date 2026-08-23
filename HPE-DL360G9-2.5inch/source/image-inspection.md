# Raster and PDF-page inspection record

All selected sources were viewed at original detail before source lock or image generation.

| Local path | Classification | Inspection finding | Accepted role / limitation |
|---|---|---|---|
| `source/originals/user-config-lock-full.png` | user screenshot | Row 7 reads `HPE / DL360G9/2.5英寸`; front thumbnail encodes 8SFF/control zone, rear encodes blanked PCIe/LOM and dual PSU. Thumbnail is heavily resampled. | Configuration lock only; not metric geometry or photographic style. |
| `qa/reference/user-config-lock-row7.png` | user screenshot crop | Same row identity; no later-generation or LFF substitution. | Binding variant/rear-state lock. |
| `source/third-party/ecs-755258-b21-front.jpg` | exact real photo | 755258-B21 8SFF, eight Smart Carriers, Universal Media Bay with VGA/USB/optical, front control strip, both front ears; mild elevated perspective; white seller background. | Primary front identity/material/style photograph. |
| `source/third-party/vrla-dl360-gen9-8bay-front.jpg` | exact-family real photo, wrong front variant | Near-straight no-bezel front but visual inspection shows ten populated SFF carriers and no Universal Media Bay; the seller filename/title is misleading for the locked 755258-B21 8SFF configuration. | Rejected variant evidence; excluded from source lock and all imagegen/model inputs. |
| `source/third-party/itinstock-dl360-gen9-rear-blankplates-2x500w.jpg` | exact real photo | Rear/top angle, three PCIe blanks, FlexibleLOM blank, embedded I/O group, two matched 500W AC PSUs; cardboard background and wear are seller context. | Primary rear material/style and dual-PSU reference. Serial presence is locked by official diagram/user request. |
| `source/third-party/usedservers-dl360-g9-back.jpg` | exact real photo | Elevated rear/top, two 800W PSUs and some open/installed expansion differences; strong evidence for top vents, rear relief and PSU geometry. | Supporting top/PSU geometry only; not configuration authority for wattage/blank plates. |
| `source/third-party/cloudninjas-dl360-g9-8bay-2.jpg` | exact real photo | Front-right/top 8-bay chassis with empty bays, exact right-side stamp/hole pattern and top/front edge; seller caption present. | Primary right-side geometry/material; not drive-population authority. |
| `source/third-party/cloudninjas-dl360-g9-1.jpg` | exact real photo | Rear-left/top exact chassis, dual PSU and asymmetric left-side hole/perforation pattern; seller caption present. | Primary left-side geometry/material. |
| `source/third-party/cloudninjas-dl360-g9-1-alt.jpg` | duplicate exact real photo | Byte-identical to the preceding rear-left image. | Retained unchanged but excluded from generation inputs as duplicate. |
| `source/third-party/itpro-dl360-gen9-contact.jpg` | exact real/editorial composite | Front with security bezel; rear with one PSU and blank bay. | Material/form lead only; configuration differences disqualify as primary. |
| `source/third-party/serverbasket-dl360-gen9-front-rear.jpg` | low-res commercial composite | Two front states on blue background; confirms chassis family but not rear. | Discovery only; excluded from generation. |
| `source/third-party/servermonkey-dl360-gen9-banner.png` | processed commercial composite | Front security bezel and one-PSU rear; existing transparency/processing. | Supporting family lead only; excluded from generation. |
| `source/pdf-pages/maintenance-p016.png` | official technical diagram | Exploded top cover, chassis base, left/right ears and separable construction. | Binding assembly/top-cover geometry; bottom fallback support only. |
| `source/pdf-pages/maintenance-p083.png` | official technical diagram | 8SFF front is 6 carriers left plus media bay plus 2 carriers lower-right; also identifies optional front VGA/USB/optical and status/control area. | Binding front layout/count. |
| `source/pdf-pages/maintenance-p084.png` | official technical diagram | Exact right-front control strip and indicator ordering. | Binding front control geometry. |
| `source/pdf-pages/maintenance-p088.png` | official technical diagram | Exact rear order: PCIe slots 1-3, PSU 2/1, VGA, four NICs, iLO, serial, USB pair, FlexibleLOM. | Binding rear I/O identity/order. |
| `source/pdf-pages/visiocafe-p001.png` | technical visual solution | Exact DL360 Gen9 preconfigured model elevations, including 755258-B21 8SFF, rear and placement maps. | Supporting orthographic proportion/layout; not photographic style. |
| `source/pdf-pages/visiocafe-p002.png` | technical visual solution | Component option matrix including AC/DC PSUs and FlexibleLOM variants. | Confirms option families; target remains locked to dual AC/LOM blank. |

Rejected differences are never transformed into the target configuration by assumption: Gen10, 4LFF, 10SFF, front security bezel, one-PSU/blank-PSU rears, installed PCIe cards, installed FlexibleLOM ports, and DC PSUs are excluded.
