from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[1];excluded_names={'SHA256SUMS.txt','SHA256-MANIFEST.json','qa/archive-check.json'};excluded_dirs={'.venv','__pycache__','.cache'};rows=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(ROOT).as_posix()
 if rel in excluded_names or any(x in excluded_dirs for x in p.relative_to(ROOT).parts):continue
 kind='deliverable or execution evidence'
 if rel.startswith(('sources/official/','sources/third_party/')):kind='original downloaded bytes (or explicitly named HTTP error response)'
 elif rel.startswith('sources/derived/'):kind='derived source crop or PDF raster; parent recorded in sources/derived-index.json'
 elif rel.startswith(('imagegen/outputs/','imagegen/rejected/')):kind='original generated output; prompt and review in imagegen/manifest.json'
 elif rel.startswith('imagegen/prompts/'):kind='original generation prompt'
 elif rel.startswith('textures/'):kind='generated procedural PBR map or explicitly projected original-photo label'
 elif rel.startswith('desktop/') and p.suffix=='.png':kind='unmodified native desktop screenshot'
 elif rel.startswith('previews/'):kind='Blender render (see qa/final-renders.json for selected final20)'
 rows.append({'path':rel,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'category':kind})
(ROOT/'SHA256SUMS.txt').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in rows));(ROOT/'SHA256-MANIFEST.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'algorithm':'SHA256','excluded_files':sorted(excluded_names),'excluded_directories':sorted(excluded_dirs),'exclusion_reason':'Checksums cannot include themselves. qa/archive-check.json is the verification result written after checking these hashes. Runtime environments/caches are not deliverables.','files':rows},indent=2));print('Checksummed',len(rows),'files',sum(x['bytes'] for x in rows),'bytes')
