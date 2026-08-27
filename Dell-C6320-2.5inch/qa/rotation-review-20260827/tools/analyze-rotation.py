#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw

REVIEW=Path(__file__).resolve().parent.parent

def arrays(files): return [np.asarray(Image.open(path).convert("RGB"),dtype=np.float32) for path in files]
def luma(pixels): return float(np.mean(pixels@np.asarray((.2126,.7152,.0722),dtype=np.float32)))
def main():
    phase="after";root=REVIEW/phase/"evidence"/"rotation";out=REVIEW/"final"/"frame-analysis";out.mkdir(parents=True,exist_ok=True);summary=[]
    for engine in ("three","babylon"):
        for variant in ("standard","web"):
            combo=root/engine/variant;yaw_files=sorted((combo/"yaw").glob("*.png"));pitch_files=sorted((combo/"pitch").glob("*.png"));stability_files=sorted((combo/"stability").glob("*.png"));manifest=json.loads((combo/"rotation-manifest.json").read_text());yaw=arrays(yaw_files);bg=np.asarray(((238,241,244),(196,203,210)),dtype=np.float32);metrics=[]
            for path,image in zip(yaw_files,yaw):
                distance=np.minimum(np.max(np.abs(image-bg[0]),axis=2),np.max(np.abs(image-bg[1]),axis=2));mask=distance>14;pixels=image[mask] if np.any(mask) else image.reshape(-1,3);metrics.append({"file":path.name,"objectFraction":float(mask.mean()),"objectLuma":luma(pixels),"objectMeanRGB":[float(v) for v in pixels.mean(axis=0)]})
            adjacent=[]
            for index in range(len(yaw)):
                other=(index+1)%len(yaw);adjacent.append({"from":yaw_files[index].name,"to":yaw_files[other].name,"pixelMAE":float(np.mean(np.abs(yaw[index]-yaw[other]))),"objectFractionDelta":abs(metrics[index]["objectFraction"]-metrics[other]["objectFraction"]),"objectLumaDelta":abs(metrics[index]["objectLuma"]-metrics[other]["objectLuma"])})
            stable=[]
            for a in sorted((combo/"stability").glob("*-a.png")):
                b=Path(str(a).replace("-a.png","-b.png"));ai=np.asarray(Image.open(a).convert("RGB"),dtype=np.float32);bi=np.asarray(Image.open(b).convert("RGB"),dtype=np.float32);stable.append({"a":a.name,"b":b.name,"pixelMAE":float(np.mean(np.abs(ai-bi))),"maxChannelDelta":float(np.max(np.abs(ai-bi)))})
            errors=[]
            if len(yaw_files)!=72:errors.append(f"yaw count {len(yaw_files)} != 72")
            if len(pitch_files)!=16:errors.append(f"pitch count {len(pitch_files)} != 16")
            if len(stability_files)!=16 or len(stable)!=8:errors.append("stability frame/pair count mismatch")
            if any(item["pixelMAE"]>.01 or item["maxChannelDelta"]>1 for item in stable):errors.append("same-angle stability mismatch")
            if not manifest["runtime"]["webgl2"] or manifest["runtime"]["overlayVisible"]:errors.append("runtime WebGL2/overlay gate")
            if manifest.get("consoleErrors"):errors.append("console errors")
            if metrics and min(item["objectFraction"] for item in metrics)<.008:errors.append("object disappearance/leakage candidate")
            if adjacent and max(item["objectFractionDelta"] for item in adjacent)>.08:errors.append("abrupt silhouette area jump")
            # Gray sheet metal can be numerically close to the light checker and
            # make the diagnostic object mask shrink. Treat that as a real gray
            # jump only when the unsegmented full-frame motion is also abrupt.
            if adjacent and max(item["objectLumaDelta"] for item in adjacent)>25 and max(item["pixelMAE"] for item in adjacent)>10:errors.append("abrupt texture/gray luma jump")
            result={"model":REVIEW.parent.parent.name,"engine":engine,"variant":variant,"modelSha256":manifest["modelSha256"],"counts":{"yaw":len(yaw_files),"pitch":len(pitch_files),"stabilityFrames":len(stability_files),"stabilityPairs":len(stable)},"runtime":manifest["runtime"],"objectFraction":{"min":min(item["objectFraction"] for item in metrics),"max":max(item["objectFraction"] for item in metrics),"maxAdjacentDelta":max(item["objectFractionDelta"] for item in adjacent)},"objectLuma":{"min":min(item["objectLuma"] for item in metrics),"max":max(item["objectLuma"] for item in metrics),"maxAdjacentDelta":max(item["objectLumaDelta"] for item in adjacent)},"pixelMotionMAE":{"median":float(np.median([item["pixelMAE"] for item in adjacent])),"max":max(item["pixelMAE"] for item in adjacent)},"stability":stable,"errors":errors,"errorCount":len(errors),"status":"PASS" if not errors else "REVIEW"}
            (out/f"{engine}-{variant}.json").write_text(json.dumps(result,indent=2)+"\n");summary.append({"engine":engine,"variant":variant,"status":result["status"],"errorCount":len(errors),"maxStableMAE":max(item["pixelMAE"] for item in stable),"maxAdjacentLumaDelta":result["objectLuma"]["maxAdjacentDelta"],"maxAdjacentAreaDelta":result["objectFraction"]["maxAdjacentDelta"]})
    report={"model":REVIEW.parent.parent.name,"combinationCount":len(summary),"allPass":all(item["status"]=="PASS" for item in summary),"combinations":summary};(out/"summary.json").write_text(json.dumps(report,indent=2)+"\n");print(json.dumps(report,indent=2))
if __name__=="__main__":main()
