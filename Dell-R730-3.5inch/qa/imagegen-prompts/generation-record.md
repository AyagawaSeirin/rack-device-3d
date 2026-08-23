# Canonical face generation record

All canonical faces were produced through the built-in `image_gen` path with one face per call, on a flat `#FF00FF` chroma background. No CLI/API fallback was used. Real exact-device photographs remain the primary binding identity and photographic-style references; generated derivatives are never source evidence.

| Face | Mode | Selected chroma SHA-256 | Final view SHA-256 | Prompt record | Result |
|---|---|---|---|---|---|
| front | SOURCE_LOCKED_GENERATION | `22f1e6f8ffa5fcf6363650b57177b6f14f1179cdf3dc928a68f5829cf0a4eb34` | `b2e7383e4ed2c2d2be27a0bcb6fc63c1018c5ca295af73c6a501e252f641cf13` | `front.txt` | selected |
| rear | SOURCE_LOCKED_GENERATION | `5b05cc5800fd9e47df6901e164dd44c9460b45bfc6c019575fab9eec538c6a3f` | `edb5ccfe53779711becd5c19bbd3c82be1e42df69733959b03f1eab8772b680c` | `rear.txt` | selected; dual EPP 750W AC |
| left | MULTI_REFERENCE_RECONSTRUCTION | `756367d061efb62af938396d432faf1727a3cb6ca5180f7e123b5c8bc9edb951` | `41e8f6a4cb4f941fca9ff4339cc805fd22f65e93d6fed30aa92299680089f3d6` | `left.txt` | selected; physical left, not mirrored |
| right | MULTI_REFERENCE_RECONSTRUCTION | `59af7c634424d1663e98675b25fce9774da28b8f7caa748821e46545e4f0c713` | `6f366e0e9ef56d6b36feb23b06d87a249d5023dde497ed7e380b33f00645f447` | `right.txt` | selected; independent studs/seams |
| top | SOURCE_LOCKED_GENERATION | `6ce8ccca7d871b20b89dc27dedda3b8340bcf4f0b3c5eb68294f61a06a1ddb6b` | `2b0f8ead1ff64d6718d47df4b4171a8c6f5b1998e6478e7e772bd37b8627dba3` | `top.txt`, `top-correction.txt` | corrected and selected |
| bottom | GENERIC_BOTTOM_FALLBACK | `6d787b649fb98df3c522395492a80d7b685d3d3bbccda94541d43a5522742802` | `8c513fabb899721f0ecb6b0c46601ed47a2a0b90b655d01dc1301ef510a1fce7` | `bottom.txt`, `bottom-correction.txt` | conservative fallback selected |

Rejected derivatives are retained as `qa/generated/top-rejected-adjacent-face.png` (adjacent front face visible) and `qa/generated/bottom-rejected-tabs.png` (unsupported tabs). Chroma removal used the installed imagegen helper with border auto-key, soft matte and despill. Final tight crops were dimension-locked to the official physical face ratios. The structural view audit reports zero errors and zero partially transparent core regions; its five warnings are limited to antialiased external silhouette pixels on non-bottom faces.
