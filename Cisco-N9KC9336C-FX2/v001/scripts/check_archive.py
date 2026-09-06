from pathlib import Path
import ast,json,hashlib,sys,re,datetime
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from PIL import Image
import fitz
ROOT=Path(__file__).resolve().parents[1];exclude={'.venv','__pycache__','.cache'};fail=[];images=0;pdfs=0;scripts=0;links=0
paths=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in exclude for x in p.relative_to(ROOT).parts)]
for p in paths:
 try:
  if p.suffix.lower() in ['.png','.jpg','.jpeg','.webp']:
   with Image.open(p) as im:im.load()
   images+=1
  elif p.suffix.lower()=='.pdf':
   assert p.read_bytes()[:5]==b'%PDF-';d=fitz.open(p);assert len(d)>0;d.close();pdfs+=1
  elif p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));scripts+=1
 except Exception as e:fail.append({'path':str(p.relative_to(ROOT)),'error':str(e)})
class Links(HTMLParser):
 def __init__(self,parent):super().__init__();self.parent=parent
 def handle_starttag(self,tag,attrs):
  global links
  for k,v in attrs:
   if k not in ['src','href'] or not v:continue
   url=urlsplit(v)
   if url.scheme or url.netloc or not url.path:continue
   links+=1;p=(self.parent/unquote(url.path)).resolve()
   if not p.is_file():fail.append({'html':str(self.parent.relative_to(ROOT)),'missing_link':v})
for p in [ROOT/'REVIEW.html',ROOT/'imagegen/REVIEW.html']:
 if p.exists():Links(p.parent).feed(p.read_text())
 else:fail.append({'missing_html':str(p.relative_to(ROOT))})
for p in [ROOT/'README.md',ROOT/'REPRODUCE.md',ROOT/'QA.md']:
 if not p.exists():fail.append({'missing_document':str(p.relative_to(ROOT))});continue
 for href in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  u=urlsplit(href)
  if not u.scheme and u.path:
   links+=1
   if not (p.parent/unquote(u.path)).exists():fail.append({'doc':p.name,'missing_link':href})
glb=ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb';gsha=hashlib.sha256(glb.read_bytes()).hexdigest()
for name,key in [('glb-container.json','sha256'),('glb-reimport.json','glb_sha256'),('glb-delivery-scene.json','glb_sha256'),('glb-ray-tests.json','source_glb_sha256')]:
 p=ROOT/'qa'/name
 if not p.exists():fail.append({'missing_report':name});continue
 d=json.loads(p.read_text())
 if d.get(key)!=gsha or not d['pass']:fail.append({'report':name,'hash_or_pass_failure':True})
for name in ['geometry-initial.json','original-delivery-scene.json','original-ray-tests.json','original-ear-render-tests.json','glb-ear-render-tests.json','original-shell-render-tests.json','glb-shell-render-tests.json','packed-reopen.json']:
 p=ROOT/'qa'/name
 if not p.exists() or not json.loads(p.read_text()).get('pass'):fail.append({'required_pass_missing':name})
for name in ['original','glb']:
 d=json.loads((ROOT/'qa'/f'{name}-ear-render-tests.json').read_text())
 if len(d['renders'])!=11 or sum(len(r['samples']) for r in d['renders'])!=42:fail.append({'incomplete_ear_render_coverage':name})
 d=json.loads((ROOT/'qa'/f'{name}-shell-render-tests.json').read_text())
 if len(d['renders'])!=4:fail.append({'incomplete_shell_coverage':name})
renders=json.loads((ROOT/'qa/final-renders.json').read_text());assert len(renders)==20
for r in renders:
 if hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['sha256']:fail.append({'stale_render_manifest':r['path']})
reopen=json.loads((ROOT/'qa/packed-reopen.json').read_text())
if reopen['master_sha256']!=hashlib.sha256((ROOT/reopen['master_file']).read_bytes()).hexdigest():fail.append({'packed_reopen_master_hash_mismatch':True})
manifest=json.loads((ROOT/'SHA256-MANIFEST.json').read_text());hashes_checked=0
for x in manifest['files']:
 p=ROOT/x['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:fail.append({'checksum_mismatch':x['path']})
 hashes_checked+=1
report={'pass':not fail,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files_examined':len(paths),'sha256_files_checked':hashes_checked,'decoded_images':images,'valid_pdfs':pdfs,'parsed_python_scripts':scripts,'local_links_checked':links,'current_glb_sha256':gsha,'failures':fail,'scope':'Project artifacts, not original downloaded HTML resource links; raw evidence bytes never formatted or rewritten.'};(ROOT/'qa/archive-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));sys.exit(bool(fail))
