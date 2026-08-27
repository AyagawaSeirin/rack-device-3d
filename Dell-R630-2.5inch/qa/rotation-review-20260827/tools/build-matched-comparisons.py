#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

REVIEW=Path(__file__).resolve().parent.parent
MODEL=REVIEW.parent.parent
FACES=("front","rear","left","right","top","bottom")

def bbox(image: Image.Image):
    alpha=image.getchannel("A")
    found=alpha.getbbox()
    if found:
        return found
    # Browser screenshots can be composited opaque on some Chromium builds;
    # fall back to a conservative non-white difference mask.
    rgb=image.convert("RGB")
    bg=Image.new("RGB",rgb.size,rgb.getpixel((0,0)))
    return ImageChops.difference(rgb,bg).getbbox()

def checker(size):
    out=Image.new("RGB",size,(238,241,244));draw=ImageDraw.Draw(out);step=16
    for y in range(0,size[1],step):
        for x in range(0,size[0],step):
            if (x//step+y//step)%2: draw.rectangle((x,y,x+step-1,y+step-1),fill=(196,203,210))
    return out

def fit_source(source, target_bbox, canvas_size):
    source=source.convert("RGBA");sb=source.getchannel("A").getbbox() or (0,0,*source.size);crop=source.crop(sb)
    tw,th=target_bbox[2]-target_bbox[0],target_bbox[3]-target_bbox[1]
    scale=min(tw/crop.width,th/crop.height);size=(max(1,round(crop.width*scale)),max(1,round(crop.height*scale)))
    crop=crop.resize(size,Image.Resampling.LANCZOS);canvas=Image.new("RGBA",canvas_size,(0,0,0,0));x=target_bbox[0]+(tw-size[0])//2;y=target_bbox[1]+(th-size[1])//2;canvas.alpha_composite(crop,(x,y));return canvas

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    records=[]
    for engine in ("three","babylon"):
        for variant in ("standard","web"):
            for face in FACES:
                render_path=REVIEW/"final"/"matched-camera"/"renders"/engine/variant/f"{face}.png"
                render=Image.open(render_path).convert("RGBA");rb=bbox(render)
                if not rb: raise RuntimeError(f"empty render {render_path}")
                source=fit_source(Image.open(MODEL/"views"/f"{face}.png"),rb,render.size)
                out=REVIEW/"final"/"matched-camera"/"comparisons"/engine/variant/face;out.mkdir(parents=True,exist_ok=True)
                source_path=out/"source.png";render_copy=out/"render.png";overlay_path=out/"overlay.png";difference_path=out/"difference.png";sheet_path=out/"source-render-overlay-difference.png"
                source.save(source_path);render.save(render_copy)
                base=checker(render.size);src_flat=base.copy();src_flat.paste(source.convert("RGB"),(0,0),source.getchannel("A"));ren_flat=base.copy();ren_flat.paste(render.convert("RGB"),(0,0),render.getchannel("A"));overlay=Image.blend(src_flat,ren_flat,.5);difference=ImageChops.difference(src_flat,ren_flat);overlay.save(overlay_path);difference.save(difference_path)
                panels=[src_flat,ren_flat,overlay,difference];labels=["SOURCE","RENDER","OVERLAY 50%","ABS DIFFERENCE"];sheet=Image.new("RGB",(render.width*4,render.height+28),(28,33,39));draw=ImageDraw.Draw(sheet)
                for index,(panel,label) in enumerate(zip(panels,labels)):sheet.paste(panel,(index*render.width,28));draw.text((index*render.width+8,7),label,fill=(245,247,249))
                sheet.save(sheet_path)
                records.append({"engine":engine,"variant":variant,"face":face,"renderBBox":list(rb),"source":str(source_path.relative_to(REVIEW)),"render":str(render_copy.relative_to(REVIEW)),"overlay":str(overlay_path.relative_to(REVIEW)),"difference":str(difference_path.relative_to(REVIEW)),"sheet":str(sheet_path.relative_to(REVIEW)),"sheetSha256":sha(sheet_path)})
    manifest={"model":MODEL.name,"comparisonCount":len(records),"method":"same frozen-viewer camera; transparent WebGL render; source alpha content fitted without anisotropic stretch to render bbox","records":records}
    path=REVIEW/"final"/"matched-camera"/"comparison-manifest.json";path.write_text(json.dumps(manifest,indent=2)+"\n");print(json.dumps({"model":MODEL.name,"comparisonCount":len(records)},indent=2))
if __name__=="__main__": main()
