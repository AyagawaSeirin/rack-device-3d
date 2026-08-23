# rear.png

Production mode: `SOURCE_LOCKED_GENERATION`

Input roles:

1. `source/pdf-pages/quickspecs-p06.png`: PRIMARY BINDING OFFICIAL REAR IMAGE; exact identity, layout, material, color and photographic style.
2. `source/originals/user-config-lock-screenshot.png`: BINDING USER CONFIGURATION LOCK, row 4 rear.
3. `source/originals/hpe-user-guide-rear-panel.png`: OFFICIAL TECHNICAL DIAGRAM for port/slot identity and order.
4. `source/third-party/4rgroup-rear-standard.png`: SUPPORTING larger direct elevation of the same official shown rear.
5. `source/third-party/mydraw-dl360-gen10-rear.png`: SUPPORTING non-mirrored rear orientation only.

Final prompt:

Use case: product-mockup
Asset type: exact website GLB rear-face source for a rack server
Primary request: Generate one new perfectly straight orthographic REAR view of the exact HPE ProLiant DL360 Gen10 1U 4LFF embedded-LOM-generation configuration shown in Image 1 and locked by Image 2. Image 1 is the highest-authority binding identity-and-style reference and may not be redesigned.
Scene/backdrop: perfectly flat uniform solid #00FFFF chroma-key background with no shadow, gradient, floor, reflection or texture; do not use #00FFFF on the device.
Style/medium: source-locked HPE real product photography. Preserve Image 1’s silver galvanized panel grain, black connector cavities, genuine fan/PSU texture, restrained wear, neutral color balance, highlight softness and dark recess shadows. Not cleaner CGI, illustration, vector art or a new lighting treatment.
Composition/framing: one complete rear only, perfectly straight, no top/side/bottom visible; physical body width:height 434.6:42.9; wide centered equipment with padding; rear view must retain its natural screen order and must never be horizontally flipped.
Verified screen-left to screen-right structure: bare rear chassis flange with real fasteners, PCIe slot 1 and slot 2 blanking/riser structure, installed optional slot 3 blanking/riser structure, one four-RJ45 HPE 331FLR FlexibleLOM module in the lower left, two stacked USB 3.0 ports, installed DB9 serial port, dedicated iLO 5 RJ45 management port, four embedded 331i RJ45 NIC ports, blue VGA DB15, then two independent HPE 500W Flex Slot Platinum 94% hot-plug AC PSU modules (PS2 then PS1) each with real round fan recess, IEC AC inlet, handle, magenta release lever and green status element. No rear SFF/uFF drive cage. No rear rack ears.
Constraints: model every port opening, removable blank, PSU, fan recess, inlet, latch and handle as distinct real visible structure. Preserve exact “500W” and “94%” PSU marks when legible. Keep HPE marks only where verified. Product pixels fully opaque; black vents and connector holes remain black, not transparent. Remove only callout bubbles/arrows/background, never device facts.
Avoid: SFP/SFP28 FlexibleLOM, empty FlexibleLOM blank, missing embedded NIC row, one PSU, DC PSU, 800W/1600W label, rear drive option, Gen9/Gen10 Plus/Gen11 rear, extra PCIe cards, fake ports, pseudo-text, mirroring, repeated patterns, CGI cleanup, smoothing, recoloring or blank rectangles replacing mechanical structure.

Method: built-in `image_gen`, one dedicated call; chroma-key removal follows locally.
