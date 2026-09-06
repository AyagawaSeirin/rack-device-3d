from PIL import Image,ImageDraw,ImageOps
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');files=sorted((P/'desktop/turntable-material').glob('frame-*.png'))
board=Image.new('RGB',(2000,5*255),'white');d=ImageDraw.Draw(board)
for i,p in enumerate(files):
 im=Image.open(p).convert('RGB');im=ImageOps.contain(im,(400,225));x=(i%5)*400;y=(i//5)*255;board.paste(im,(x,y+25));d.text((x+8,y+7),f'GUI MCP {i*15:03} deg / frame {i:03}',fill='black')
board.save(P/'qa/desktop-orbit-contact-sheet.jpg',quality=94)
print(len(files))
