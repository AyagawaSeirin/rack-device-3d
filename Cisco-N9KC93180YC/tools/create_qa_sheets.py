#!/usr/bin/env python3
"""Create contact sheets, matched-camera comparisons, and load CSV."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
LOADS=ROOT/"qa/webgl-loads"
OUT=ROOT/"qa/comparisons"
FONT_PATH="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
VIEWS=("front","rear","left","right","top","bottom","front-left","front-right","rear-left","rear-right")


def font(size):
    return ImageFont.truetype(FONT_PATH,size)


def contain(image,size,bg=(238,241,245)):
    image=image.convert("RGBA")
    image.thumbnail(size,Image.Resampling.LANCZOS)
    canvas=Image.new("RGBA",size,bg+(255,))
    canvas.alpha_composite(image,((size[0]-image.width)//2,(size[1]-image.height)//2))
    return canvas.convert("RGB")


def label(image,text,height=28):
    canvas=Image.new("RGB",(image.width,image.height+height),(20,27,34))
    canvas.paste(image,(0,height))
    ImageDraw.Draw(canvas).text((8,5),text,font=font(14),fill=(245,248,250))
    return canvas


report=json.loads((LOADS/"load-events.json").read_text())
records=report["records"]
by_key={(r["viewer"],r["model"],r["view"]):r for r in records}

# Flatten the complete per-load hash and screenshot evidence into CSV.
with (ROOT/"qa/viewer-load-evidence.csv").open("w",newline="") as handle:
    fields=["sequence","viewer","renderer","webgl","model","view","sha256","proof_bytes","model_last_modified_http",
            "transfer_size_bytes","bounds_xyz_mm","model_url","screenshot","screenshot_sha256","status"]
    writer=csv.DictWriter(handle,fieldnames=fields)
    writer.writeheader()
    for record in records:
        shot=ROOT/record["screenshot"]
        row={key:record.get(key) for key in fields}
        row["bounds_xyz_mm"]=json.dumps(record["bounds_xyz_mm"],separators=(",",":"))
        row["screenshot_sha256"]=hashlib.sha256(shot.read_bytes()).hexdigest()
        writer.writerow(row)

# Four ten-view contact sheets plus one all-40 overview.
contact=LOADS/"contact-sheets"
contact.mkdir(parents=True,exist_ok=True)
all_tiles=[]
for viewer in ("three","babylon"):
    for model in ("standard","web"):
        tiles=[]
        for view in VIEWS:
            record=by_key[(viewer,model,view)]
            tile=contain(Image.open(ROOT/record["screenshot"]),(320,225))
            tile=label(tile,f"{record['sequence']:02d} {viewer} · {model} · {view}")
            tiles.append(tile)
            all_tiles.append(contain(tile,(256,203)))
        sheet=Image.new("RGB",(1600,506),(14,18,23))
        for index,tile in enumerate(tiles):
            sheet.paste(tile,((index%5)*320,(index//5)*253))
        sheet.save(contact/f"{viewer}-{model}-10views.png",optimize=True)

all_sheet=Image.new("RGB",(1280,1624),(14,18,23))
for index,tile in enumerate(all_tiles):
    all_sheet.paste(tile,((index%5)*256,(index//5)*203))
all_sheet.save(contact/"all-40-hash-proven-loads.png",optimize=True)

# Matched-camera Three.js versus Babylon.js comparisons for both GLBs and all
# ten views: side-by-side, 50% overlay, and amplified absolute difference.
matched=OUT/"matched-engine"
matched.mkdir(parents=True,exist_ok=True)
for model in ("standard","web"):
    for view in VIEWS:
        a=Image.open(ROOT/by_key[("three",model,view)]["screenshot"]).convert("RGB")
        b=Image.open(ROOT/by_key[("babylon",model,view)]["screenshot"]).convert("RGB")
        if b.size!=a.size:
            b=b.resize(a.size,Image.Resampling.LANCZOS)
        small_a=a.resize((640,450),Image.Resampling.LANCZOS)
        small_b=b.resize((640,450),Image.Resampling.LANCZOS)
        side=Image.new("RGB",(1280,478),(20,27,34))
        side.paste(small_a,(0,28)); side.paste(small_b,(640,28))
        draw=ImageDraw.Draw(side)
        draw.text((8,6),f"Three.js · {model} · {view}",font=font(14),fill="white")
        draw.text((648,6),f"Babylon.js · {model} · {view}",font=font(14),fill="white")
        overlay=Image.blend(a,b,.5).resize((640,450),Image.Resampling.LANCZOS)
        diff=ImageChops.difference(a,b)
        diff=ImageEnhance.Contrast(diff).enhance(4).resize((640,450),Image.Resampling.LANCZOS)
        lower=Image.new("RGB",(1280,478),(20,27,34))
        lower.paste(overlay,(0,28)); lower.paste(diff,(640,28))
        d=ImageDraw.Draw(lower)
        d.text((8,6),"Matched-camera 50% overlay",font=font(14),fill="white")
        d.text((648,6),"Absolute difference ×4 contrast",font=font(14),fill="white")
        sheet=Image.new("RGB",(1280,956),(14,18,23))
        sheet.paste(side,(0,0)); sheet.paste(lower,(0,478))
        sheet.save(matched/f"{model}-{view}.png",optimize=True)

# Orthographic source-lock asset versus actual standard-GLB render.
source_compare=OUT/"source-vs-render"
source_compare.mkdir(parents=True,exist_ok=True)
for face in VIEWS[:6]:
    source=contain(Image.open(ROOT/"views"/f"{face}.png"),(640,450))
    render=contain(Image.open(ROOT/by_key[("three","standard",face)]["screenshot"]),(640,450))
    sheet=Image.new("RGB",(1280,478),(20,27,34))
    sheet.paste(source,(0,28)); sheet.paste(render,(640,28))
    d=ImageDraw.Draw(sheet)
    d.text((8,6),f"Generated source-lock · {face}",font=font(14),fill="white")
    d.text((648,6),f"Actual standard GLB · Three.js · {face}",font=font(14),fill="white")
    sheet.save(source_compare/f"standard-{face}.png",optimize=True)

# Authoritative real-photo cross-checks for front/top and rear/top obliques.
authoritative=OUT/"authoritative-oblique"
authoritative.mkdir(parents=True,exist_ok=True)
pairs=[
    ("front-left",ROOT/"source/third-party/ebay-187543569351-03.jpg"),
    ("rear-right",ROOT/"source/third-party/made-in-china-fx-rear.webp"),
    ("top",ROOT/"source/third-party/ebay-187543569351-04.jpg"),
]
for view,reference in pairs:
    left=contain(Image.open(reference),(640,450))
    right=contain(Image.open(ROOT/by_key[("three","standard",view)]["screenshot"]),(640,450))
    sheet=Image.new("RGB",(1280,478),(20,27,34))
    sheet.paste(left,(0,28)); sheet.paste(right,(640,28))
    d=ImageDraw.Draw(sheet)
    d.text((8,6),f"Inspected exact-FX reference · {reference.name}",font=font(14),fill="white")
    d.text((648,6),f"Actual standard GLB · {view}",font=font(14),fill="white")
    sheet.save(authoritative/f"{view}.png",optimize=True)

print(json.dumps({
    "status":"PASS","contact_sheets":5,"matched_engine_sheets":20,
    "source_vs_render_sheets":6,"authoritative_oblique_sheets":3,
    "viewer_load_csv_records":len(records),
},indent=2))
