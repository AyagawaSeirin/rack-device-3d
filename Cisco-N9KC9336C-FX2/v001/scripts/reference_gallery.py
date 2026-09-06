from pathlib import Path
import json,html,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'imagegen';r=json.loads((p/'manifest.json').read_text());selected=[];cards=[]
for j in r:
 f=p/j['output'];ok=f.is_file()
 if ok:
  im=Image.open(f);im.load();j['image_size']=list(im.size);j['sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
 j['local_output_exists']=ok
 j['input_paths_relative']=[str(Path(x).relative_to(ROOT)) if str(x).startswith(str(ROOT)) else x for x in j['inputs']]
 (p/'prompts'/(j['id']+'.txt')).write_text(j['prompt'])
 if j['review'].startswith('SELECTED'):selected.append(j)
 cards.append('<article><h2>'+html.escape(j['id'])+'</h2><p>'+html.escape(j['review'])+'</p><a href="'+html.escape(j['output'])+'"><img loading="lazy" src="'+html.escape(j['output'])+'"></a><p><a href="prompts/'+html.escape(j['id'])+'.txt">Exact prompt</a></p></article>')
(p/'manifest.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
(p/'SELECTED.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
(p/'REVIEW.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Cisco FX2 generated reference review</title><style>body{max-width:1400px;margin:30px auto;padding:0 20px;font:16px system-ui;background:#eee;color:#111}article{background:white;padding:20px;margin:24px 0}h2{font-size:20px}img{display:block;max-width:100%;max-height:850px;margin:auto}</style><h1>N9K-C9336C-FX2 — generated reference review</h1><p>AI working references. Original photos and official specifications remain the only source of physical evidence. Printing, dimensions and unverified details are never adopted from generated pixels. Rejected versions remain visible for the correction history.</p>'+''.join(cards)+'</html>')
print('records',len(r),'selected',len(selected),'all_files_exist',all(j['local_output_exists'] for j in r))
