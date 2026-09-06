"""Display-space composites of retained unmodified RGBA renders, for comparing backgrounds."""
from pathlib import Path
from PIL import Image
import json,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];prefix=sys.argv[1];p=ROOT/'qa'/f'{prefix}-shell-render-tests.json';d=json.loads(p.read_text())
for r in d['renders']:
 im=Image.open(ROOT/r['transparent']).convert('RGBA');r['background_composites']={}
 for label,color in [('light',(246,246,246,255)),('dark',(24,27,30,255))]:
  out=ROOT/'qa'/f"{prefix}-shell-{r['view']}-{label}.png";bg=Image.new('RGBA',im.size,color);Image.alpha_composite(bg,im).convert('RGB').save(out);r['background_composites'][label]={'path':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
d['background_method']='Exact displayed RGBA result alpha-composited over light/dark background; object lighting and alpha unchanged. These are QA composites, not new photographs or imagegen references.';p.write_text(json.dumps(d,indent=2));print(d['pass'])
