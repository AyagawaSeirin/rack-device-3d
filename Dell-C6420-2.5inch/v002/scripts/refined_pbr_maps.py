"""Deterministic computational PBR data, not retouched photographs.
Micron scale random grain calibrated visually to original steel/plastic macro photos.
These generic manufacturing micro-surfaces are an approximation, not scanned Dell data.
"""
from pathlib import Path
import numpy as np
from PIL import Image
import json
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002/textures/refined');P.mkdir(exist_ok=True);N=2048;rng=np.random.default_rng(642002)
y,x=np.mgrid[:N,:N];fx=np.fft.fftfreq(N);fy=np.fft.fftfreq(N);f2=fy[:,None]**2+fx[None,:]**2

def noise(s):
 n=rng.normal(size=(N,N));a=np.fft.ifft2(np.fft.fft2(n)*np.exp(-2*np.pi**2*s*s*f2)).real;a=(a-a.mean())/(a.std()+1e-9);return a

def write(prefix,base,rough,height,repeat):
 rgb=np.asarray(base);rgb=np.clip(rgb,0,1);rgb=rgb if rgb.ndim==3 else np.repeat(rgb[:,:,None],3,axis=2)
 Image.fromarray(np.uint8(rgb*255),'RGB').save(P/f'{prefix}-base.png')
 Image.fromarray(np.uint8(np.clip(rough,0,1)*255),'L').save(P/f'{prefix}-rough.png')
 step=repeat/N;dx=(np.roll(height,-1,1)-np.roll(height,1,1))/(2*step);dy=(np.roll(height,-1,0)-np.roll(height,1,0))/(2*step)
 # image rows increase downward, normal green follows UV v upward.
 norm=np.stack([-dx,dy,np.ones_like(dx)],2);norm/=np.linalg.norm(norm,axis=2,keepdims=True)
 Image.fromarray(np.uint8(np.clip(norm*.5+.5,0,1)*255),'RGB').save(P/f'{prefix}-normal.png')

coarse=noise(45);spangle=noise(6);fine=noise(.8);streak=noise(1)
base=np.array([.745,.754,.762])[None,None,:]*(1+.004*coarse[:,:,None]+.002*spangle[:,:,None])
write('zinc',base,.33+.024*coarse+.018*spangle+.012*fine,1.2e-6*spangle+2.5e-7*fine,.04)
coarse=noise(20);grain=noise(1.6);fine=noise(.7)
base=np.array([.070,.075,.081])[None,None,:]*(1+.025*coarse[:,:,None]+.032*grain[:,:,None])
write('abs',base,.49+.025*coarse+.045*grain,1.0e-6*grain+2e-7*fine,.0256)
# Delicate anisotropic nickel manufacturing scratch grain.
line=np.repeat(rng.normal(size=(N,1)),N,axis=1);grain=noise(.8)
base=np.array([.85,.855,.86])[None,None,:]*(1+.003*grain[:,:,None])
write('nickel',base,.22+.011*grain+.012*line,1.4e-7*grain+1.2e-7*line,.032)
# Woven nylon pull strap: alternating warp/weft, generic factory material.
u=x/24;v=y/24;checker=(np.floor(u/2)+np.floor(v/2))%2
weave=np.where(checker<1,np.sin(u*np.pi)**2,np.sin(v*np.pi)**2);fuzz=noise(.65)
base=np.array([.030,.034,.039])[None,None,:]*(.8+.22*weave[:,:,None]+.04*fuzz[:,:,None])
write('nylon',base,.79+.04*fuzz,65e-6*weave+1.8e-6*fuzz,.0256)
(P/'PROCEDURAL-MAPS.json').write_text(json.dumps({'resolution':[N,N],'generated_by':'procedural_pbr_maps.py, numpy deterministic seed642002','type':'PBR computational material data; no photographic retouching','units':'normal amplitude physical metres, repeats specified per material','textures':['zinc','abs','nickel','nylon'],'confidence':'generic visually calibrated manufacturing microtexture, not an exact measured scan'},indent=2))
print('Wrote12 physically scaled PBR maps')
