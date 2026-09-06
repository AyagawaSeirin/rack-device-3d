from fetch import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
idx=json.loads((ROOT/'sources/download-index.json').read_text()); jobs=[]
for name in ['overview','install']:
 f=ROOT/'sources/official'/f'{name}.html';page=next(r['page_url'] for r in idx if r.get('local_path')==str(f.relative_to(ROOT)))
 for im in BeautifulSoup(f.read_text(),'html.parser').find_all('img'):
  u=im.get('src','')
  if re.search(r'/td/i/\d',u):
   u=urljoin(page,u);jobs.append((f'official/{name}-{u.rsplit("/",1)[-1]}',u,page))
for k,stem in enumerate(['5062024142914-100_0709','5062024142915-100_0710','5062024142915-100_0711']):jobs.append((f'third_party/nwr-{k+1}.jpg','https://nwrusa.com/cdn/shop/files/'+stem+'.jpg','https://nwrusa.com/products/21504'))
jobs.append(('third_party/c2-product.jpg','https://www.c2-computer.com/cdn/shop/files/314118.jpg','https://www.c2-computer.com/collections/condition-used/products/cisco-n9k-c9336c-fx2-nexus-9336c-fx2-switch-36-ports-managed-rack-mountable-used'))
jobs.append(('third_party/dedicated.html','https://dedicatednetworksinc.com/product/cisco-n9k-c9336c-fx2-managed-switch-36x-100gb-qsfp28-40gb-qsfp28/'))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rr=list(pool.map(fetch,jobs))
idx+=rr;(ROOT/'sources/download-index.json').write_text(json.dumps(idx,indent=2))
for r in rr:print(r.get('local_path',r['requested_path']),r['status'],r.get('image_dimensions'),flush=True)
# Derived PDF pages preserve the source bytes.
doc=fitz.open(ROOT/'sources/official/hardware-guide.pdf')
for n in [0,6,7,8,9,27,28,29,30,31,32,33,54,55]:
 p=doc[n];p.get_pixmap(matrix=fitz.Matrix(2,2)).save(ROOT/'sources/derived'/f'hardware-guide-physical-{n+1:02d}.png')
(ROOT/'sources/derived/hardware-guide-text.txt').write_text('\n'.join(f'\nPHYSICAL PAGE {i+1}\n'+p.get_text() for i,p in enumerate(doc)))
