from fetch import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
jobs=[('third_party/serverlama.html','https://serverlama.com/products/switch-cisco-nexus-9k-n9k-c9336c-fx2'),('third_party/bargain.html','https://www.bargainhardware.co.uk/cisco-nexus-n9k-c9336c-fx2-36xqsfp28-100g-managed-switch'),('third_party/etb.html','https://www.etb-tech.com/cisco-nexus-n9k-c9336c-fx2-switch-lan-enterprise-port-side-air-intake-sw00114.html')]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rr=list(pool.map(fetch,jobs))
f=ROOT/'sources/download-index.json';f.write_text(json.dumps(json.loads(f.read_text())+rr,indent=2))
for r in rr:
 print(r['requested_path'],r['status'])
 if r['status']=='downloaded':
  s=BeautifulSoup((ROOT/r['local_path']).read_text(),'html.parser')
  for im in s.find_all('img'):
   u=im.get('src','') or im.get('data-src','')
   if any(t in u.lower() for t in ['9336','sw00114']):print(u)
