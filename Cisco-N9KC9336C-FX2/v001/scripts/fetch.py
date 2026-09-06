from pathlib import Path
import requests, json, datetime, hashlib, concurrent.futures
from PIL import Image
import fitz
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/'
BOOK='b_n9336cFX2_nxos_hardware_installation_guide'
JOBS=[('official/overview.html',BASE+BOOK+'/'+BOOK+'_chapter_01.html'),('official/install.html',BASE+BOOK+'/'+BOOK+'_chapter_011.html'),('official/specs.html',BASE+BOOK+'/'+BOOK+'_appendix_0111.html'),('official/hardware-guide.pdf',BASE+BOOK+'.pdf'),('official/datasheet.html','https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.html'),('official/datasheet.pdf','https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.pdf'),('official/aci-guide-mirror.pdf','https://gzhls.at/blob/ldb/1/7/7/b/37c6c1a6f10ea639bb1bcb79e97a3dbed735.pdf'),('third_party/abacus.html','https://www.ebay.com/itm/126080121867'),('third_party/with-ears.html','https://www.ebay.it/itm/405562523057'),('third_party/maravi.html','https://www.ebay.com/itm/178043401566'),('third_party/nwr.html','https://nwrusa.com/products/21504'),('third_party/c2.html','https://www.c2-computer.com/collections/condition-used/products/cisco-n9k-c9336c-fx2-nexus-9336c-fx2-switch-36-ports-managed-rack-mountable-used'),('third_party/linknewnet.html','https://www.linknewnet.com/products/cisco-nexus-9000-series-switch-n9k-c9336c-fx2')]
def fetch(job):
 name,url,*extra=job;p=ROOT/'sources'/name;p.parent.mkdir(parents=True,exist_ok=True)
 rec={'page_url':extra[0] if extra else url,'asset_url':url,'requested_path':str(p.relative_to(ROOT)),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_model':'pending visual verification','view':'pending','options':'pending','evidence':'pending'}
 try:
  r=requests.get(url,timeout=40,headers={'User-Agent':'Mozilla/5.0'});rec.update(http_status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(r.content));valid=r.status_code==200
  if p.suffix=='.pdf':
   valid=valid and r.content.startswith(b'%PDF-')
   if valid:rec['pdf_pages']=len(fitz.open(stream=r.content,filetype='pdf'))
  if p.suffix.lower() in ['.jpg','.jpeg','.png','.webp']:
   import io
   im=Image.open(io.BytesIO(r.content));im.load();rec['image_dimensions']=list(im.size);rec['image_mode']=im.mode
  if valid:
   p.write_bytes(r.content);rec.update(local_path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(r.content).hexdigest(),status='downloaded')
  else:
   fail=p.with_suffix(p.suffix+'.http-response.txt');fail.write_bytes(r.content);rec.update(status='failed',response_path=str(fail.relative_to(ROOT)))
 except Exception as e:rec.update(status='failed',error=str(e))
 return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:records=list(pool.map(fetch,JOBS))
 (ROOT/'sources/download-index.json').write_text(json.dumps(records,indent=2))
 for r in records:print(r['requested_path'],r['status'],r.get('http_status'),r.get('pdf_pages',''),flush=True)
