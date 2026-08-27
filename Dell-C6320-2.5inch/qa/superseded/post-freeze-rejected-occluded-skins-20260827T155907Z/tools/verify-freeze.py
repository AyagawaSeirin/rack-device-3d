#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
review=Path(__file__).resolve().parent.parent;model=review.parent.parent;frozen=json.loads((review/"final/frozen-hashes.json").read_text());records=[]
for key in ("standardGlb","webGlb","builder","threeViewer","babylonViewer"):
    item=frozen[key];path=model/item["path"];actual=hashlib.sha256(path.read_bytes()).hexdigest();records.append({"key":key,"path":item["path"],"expectedSha256":item["sha256"],"actualSha256":actual,"match":actual==item["sha256"]})
result={"model":model.name,"frozenAt":frozen["frozenAt"],"checkedAtEvidenceFinalization":True,"allMatch":all(item["match"] for item in records),"records":records};(review/"final/freeze-verification.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
raise SystemExit(0 if result["allMatch"] else 1)
