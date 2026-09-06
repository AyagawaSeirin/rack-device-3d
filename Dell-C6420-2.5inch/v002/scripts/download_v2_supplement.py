import requests,json,concurrent.futures
from pathlib import Path
from PIL import Image
from io import BytesIO
p=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002/sources/third_party')
ids=['lOYAAeSwI9VpnvJv','mdQAAeSwJ2xpnvJ8','8Y0AAeSwEe1pnvKB','JJIAAeSwTmlpw7Gs','fVUAAeSwCONppxJn','gc8AAeSwnc1ppxKN','5JoAAeSw2XRpnvIa','lVcAAeSwDRBpnvVn','MYkAAeSwhkpp~GvT','9LgAAeSwUv5p~GvT']
more=['lXcAAeSwN01qGlSj','fTQAAeSwqExqGlSj','ePsAAeSwlGBqGlSk','ZZcAAeSw82ZqGlSj','cAYAAeSwVUhqGlSj']
jobs=[(f'techbuyer-{i+1:02}',f'https://i.ebayimg.com/images/g/{v}/s-l1600.webp','https://www.ebay.com/itm/366227485948') for i,v in enumerate(ids)]
jobs += [(f'bargain-{i+2:02}',f'https://i.ebayimg.com/images/g/{v}/s-l1600.webp','https://www.ebay.com/itm/126728243283') for i,v in enumerate(more)]
jobs += [(f'itc-{i:02}','https://www.itcreations.com/images/products/large/DELL_C6400_2.5'+('' if i==0 else '_'+str(i))+'.jpg','https://www.itcreations.com/product/99899') for i in range(5)]
def go(j):
 name,url,page=j
 try:
  r=requests.get(url,timeout=30);im=Image.open(BytesIO(r.content));im.verify();im=Image.open(BytesIO(r.content));f=p/(name+('.jpg' if im.format=='JPEG' else '.webp'));f.write_bytes(r.content);return dict(name=name,url=url,page=page,status=r.status_code,size=im.size,path=str(f))
 except Exception as e:return dict(name=name,url=url,page=page,error=str(e))
with concurrent.futures.ThreadPoolExecutor(8) as ex:res=list(ex.map(go,jobs))
(p/'v2-supplement-downloads.json').write_text(json.dumps(res,indent=2))
for r in res:print(r)
