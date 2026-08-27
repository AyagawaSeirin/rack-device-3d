'use strict';
const fs=require('fs');
const path=require('path');

const glb=path.resolve(__dirname,'../model/Dell-R240-3.5inch.glb');
const payload=fs.readFileSync(glb);
if(payload.toString('ascii',0,4)!=='glTF')throw new Error('invalid GLB');
const jsonLength=payload.readUInt32LE(12);
const document=JSON.parse(payload.subarray(20,20+jsonLength).toString('utf8').trim());
const names=(document.nodes||[]).map(node=>node.name||'');
const count=pattern=>names.filter(name=>pattern.test(name)).length;
const exact=name=>names.includes(name);
const checks={
  source_locked_faces:{actual:count(/^Texture_(Front|Rear|Left|Right|Top|Bottom)$/),expected:6},
  lff_carrier_bodies:{actual:count(/^LFF_Carrier_[1-4]$/),expected:4},
  lff_carrier_handles:{actual:count(/^LFF_Carrier_[1-4]_Lower_Handle$/),expected:4},
  lff_release_rings:{actual:count(/^LFF_Carrier_[1-4]_Release_Ring$/),expected:4},
  fixed_ac_psu_installed:{actual:count(/^AC_PSU_Fixed_Body$/),expected:1},
  second_psu_absent_marker:{actual:count(/^Second_AC_PSU_ABSENT$/),expected:1},
  pcie_blanking_plates:{actual:count(/^PCIe_(HalfHeight|FullHeight)_Blanking_Plate$/),expected:2},
  cabled_fan_housings:{actual:count(/^Internal_Cabled_Fan_[1-4]_Housing$/),expected:4},
  physical_right_side_features:{actual:count(/^Right_Side_Rail_Feature_/),expected:5},
  physical_left_side_features:{actual:count(/^Left_Side_Rail_Feature_/),expected:5},
  front_only_rack_ears:{actual:count(/^Front_(Left_Rack_Ear|Right_Control_Ear)$/),expected:2},
};
const requiredRearNodes=['Rear_Serial_DB9','Rear_VGA','Rear_iDRAC_RJ45','Rear_LOM1_RJ45','Rear_LOM2_RJ45','Rear_USB3_Port_1','Rear_USB3_Port_2','Rear_System_ID_Button','Rear_CMA_Connector','Rear_Blue_Expansion_Latch','AC_PSU_IEC_C14_Inlet'];
const missingRearNodes=requiredRearNodes.filter(name=>!exact(name));
const mismatches=Object.entries(checks).filter(([,value])=>value.actual!==value.expected).map(([name,value])=>({name,...value}));
const report={
  status:mismatches.length===0&&missingRearNodes.length===0?'PASS':'REWORK',
  glb:'model/Dell-R240-3.5inch.glb',
  node_count:names.length,
  checks,
  required_rear_io_nodes:requiredRearNodes,
  missing_rear_io_nodes:missingRearNodes,
  mismatches,
  note:'Fine factual branding, carrier grille patterns and port face appearance are retained in the source-locked OPAQUE textures; these node checks verify the distinct structural assemblies and installed-count lock.',
};
fs.writeFileSync(path.join(__dirname,'feature-count-audit.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
process.exit(report.status==='PASS'?0:1);

