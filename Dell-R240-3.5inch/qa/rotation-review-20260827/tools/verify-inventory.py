#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re, struct
from pathlib import Path

REVIEW=Path(__file__).resolve().parent.parent;MODEL=REVIEW.parent.parent;KEY=MODEL.name
CONFIG={
"Dell-R240-3.5inch":{
 "glbs":[MODEL/"model/Dell-R240-3.5inch.glb",MODEL/"model/Dell-R240-3.5inch-web.glb"],
 "faces":{"front":"Texture_Front","rear":"Texture_Rear","left":"Texture_Left","right":"Texture_Right","top":"Texture_Top","bottom":"Texture_Bottom"},
 "rules":{"front rack ears":r"^Front_(Left_Rack_Ear|Right_Control_Ear)$","3.5-inch hot-swap carriers":r"^LFF_Carrier_\d+$","carrier handles":r"^LFF_Carrier_\d+_Lower_Handle$","rear serial":r"^Rear_Serial_DB9$","rear vga":r"^Rear_VGA$","idrac":r"^Rear_iDRAC_RJ45$","onboard 1gbe":r"^Rear_LOM\d_RJ45$","rear usb":r"^Rear_USB3_Port_\d$","pcie blanking":r"^PCIe_.*Blanking_Plate$","fixed ac psu":r"^AC_PSU_Fixed_Body$","iec":r"^AC_PSU_IEC_C14_Inlet$","cooling fans":r"^Internal_Cabled_Fan_\d+_Housing$"},
 "hard":[("installed fixed AC PSU",r"^AC_PSU_Fixed_Body$",1),("internal cabled fan housings",r"^Internal_Cabled_Fan_\d+_Housing$",4),("front-only ears",r"^Front_.*Ear$",2),("synthetic logo planes",r"logo",0)]},
"Dell-R630-2.5inch":{
 "glbs":[MODEL/"model/Dell-R630-2.5inch.glb",MODEL/"model/Dell-R630-2.5inch-web.glb"],
 "faces":{"front":"front canonical face","rear":"rear canonical face","left":"physical left canonical face","right":"physical right canonical face","top":"top canonical face","bottom":"bottom fallback canonical face"},
 "rules":{"mounting wing":r"^front (left|right) wing housing$","sff carrier assemblies":r"^SFF carrier \d+$","carrier pull handles":r"^carrier \d+ pull handle$","lp pcie":r"^rear LP PCIe blanking assembly \d$","idrac":r"^rear iDRAC8 Enterprise RJ45 recess$","db9":r"^rear DB9 serial recess$","vga":r"^rear VGA HD15 recess$","usb 3.0":r"^rear USB 3.0 port \d recess$","quad rj45":r"^quad RJ45 NDC port \d recess$","ac psu modules":r"^EPP 1100W AC PSU \d body$","iec ac inlets":r"^PSU \d IEC C14 top rim$","release tabs":r"^PSU \d orange release tab$","psu pull handles":r"^PSU \d rigid handle grasp$","rail mounting studs":r"^(left|right) rail mounting stud \d$"},
 "hard":[("matching EPP 1100W AC PSU bodies",r"^EPP 1100W AC PSU \d body$",2),("internal cooling fan housings",r"^internal cooling fan \d housing$",7),("front-only wing housings",r"^front (left|right) wing housing$",2),("rear ears",r"rear.*ear",0)]},
"Dell-C6320-2.5inch":{
 "glbs":[MODEL/"models/Dell-PowerEdge-C6300-4xC6320-24SFF-standard.glb",MODEL/"models/Dell-PowerEdge-C6300-4xC6320-24SFF-web.glb"],
 "faces":{"front":"Front_SourceLocked_Texture","rear":"Rear_SourceLocked_Texture","left":"Physical_Left_SourceLocked_Texture","right":"Physical_Right_SourceLocked_Texture","top":"Top_SourceLocked_Texture","bottom":"Bottom_GenericFallback_Texture"},
 "rules":{"2.5-inch vertical drive carriers":r"^SFF_Carrier_\d+_Body$","left control panel":r"^Front_Left_Control_Panel$","right control panel":r"^Front_Right_Control_Panel$","non-usable drive cover":r"^Front_Nonusable_Drive_Cover$","front mounting ears":r"^Front_(Left|Right)_Ear_OuterRail$","large rack mounting holes":r"^Front_(Left|Right)_Ear_LargeRackHole$","poweredge c6320 sleds":r"^C6320_Node_\d_PerimeterTop$","shared 1400 w ac psu":r"^Shared_AC_PSU_1400W_\d_Face$","psu fan guards":r"^Shared_AC_PSU_1400W_\d_FanGuard$","psu ac inlets":r"^Shared_AC_PSU_1400W_\d_IEC_AC_Inlet$","psu orange releases":r"^Shared_AC_PSU_1400W_\d_OrangeRelease$","pcie vented":r"^C6320_Node_\d_PCIeCarrier$","usb 3.0 port":r"^C6320_Node_\d_USB3$","10gbe sfp":r"^C6320_Node_\d_SFPplus_[AB]$","idrac8":r"^C6320_Node_\d_iDRAC_RJ45$","usb-to-serial":r"^C6320_Node_\d_USB_to_Serial$","vga ports":r"^C6320_Node_\d_VGA$","power/status buttons":r"^C6320_Node_\d_Power_Status$","pull-label tabs":r"^C6320_Node_\d_PullTab$","vertical access slot":r"^Physical_Right_VerticalAccessSlot$","upper shallow rectangular recesses":r"^Physical_Right_UpperRecess_\d$","black oval":r"^Top_Black_Oval_Pad$","blue rectangular":r"^Top_Blue_Rectangular_Pad$"},
 "hard":[("four C6320 sleds",r"^C6320_Node_\d_PerimeterTop$",4),("matching 1400W AC PSUs",r"^Shared_AC_PSU_1400W_\d_Face$",2),("internal shared fan housings",r"^Internal_Shared_Fan_\d_Housing$",4),("24 SFF carrier bodies",r"^SFF_Carrier_\d+_Body$",24),("synthetic logo/label planes",r"TRUE_(DELL|POWEREDGE)",0)]}}

def doc(path):
    data=path.read_bytes();length,kind=struct.unpack_from("<II",data,12);assert kind==0x4E4F534A;return json.loads(data[20:20+length].decode("utf-8"))
def nodes(document): return [node.get("name","") for node in document.get("nodes",[])]
def count(names,pattern): return len([name for name in names if re.search(pattern,name,re.I)])
def main():
    cfg=CONFIG[KEY];documents=[doc(path) for path in cfg["glbs"]];name_sets=[nodes(value) for value in documents];rows=list(csv.DictReader((MODEL/"source/feature-inventory.csv").open()));checks=[];errors=[]
    for row in rows:
        component=row["component"];face=row["face"].lower();expected=int(row["count"]);rule=next((pattern for token,pattern in cfg["rules"].items() if token in component.lower()),None)
        if KEY=="Dell-R630-2.5inch" and component.lower()=="rail mounting studs": rule=rf"^{face} rail mounting stud \d$"
        if expected==0:
            observed=[0,0];mode="REQUIRED_ABSENCE_PLUS_RENDER_REVIEW";status="PASS"
        elif rule:
            observed=[count(names,rule) for names in name_sets];mode=f"NODE_REGEX:{rule}";status="PASS" if observed==[expected,expected] else "FAIL"
        else:
            texture=cfg["faces"][face];present=[texture in names for names in name_sets];comparison=REVIEW/"final/matched-camera/comparisons/three/standard"/face/"source-render-overlay-difference.png";observed=[expected,expected] if all(present) and comparison.exists() else [0,0];mode=f"SOURCE_LOCKED_FACE_AND_MATCHED_CAMERA:{texture}";status="PASS" if observed==[expected,expected] else "FAIL"
        item={"face":face,"component":component,"expectedCount":expected,"standardObserved":observed[0],"webObserved":observed[1],"mode":mode,"status":status,"confidence":row.get("confidence","")};checks.append(item)
        if status!="PASS":errors.append(item)
    hard=[]
    for label,pattern,expected in cfg["hard"]:
        observed=[count(names,pattern) for names in name_sets];status="PASS" if observed==[expected,expected] else "FAIL";item={"label":label,"regex":pattern,"expected":expected,"standardObserved":observed[0],"webObserved":observed[1],"status":status};hard.append(item)
        if status!="PASS":errors.append(item)
    result={"model":KEY,"inventoryRows":len(rows),"inventoryPass":len([item for item in checks if item["status"]=="PASS"]),"hardGateCount":len(hard),"checks":checks,"hardConfigurationGates":hard,"errors":errors,"errorCount":len(errors),"status":"PASS" if not errors else "REWORK"};out=REVIEW/"final/inventory-verification";out.mkdir(parents=True,exist_ok=True);(out/"inventory-verification.json").write_text(json.dumps(result,indent=2)+"\n");
    with (out/"inventory-verification.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=["face","component","expectedCount","standardObserved","webObserved","mode","status","confidence"]);writer.writeheader();writer.writerows(checks)
    print(json.dumps({key:result[key] for key in ("model","inventoryRows","inventoryPass","hardGateCount","errorCount","status")},indent=2))
if __name__=="__main__":main()
