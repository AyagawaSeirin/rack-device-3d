from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene
for name,w in [('KEY',8.0),('FILL',5.2),('RIM',8.0)]:bpy.data.objects[name].data.energy=w
s.cycles.samples=192;s.cycles.adaptive_threshold=.015;s.cycles.use_denoising=False;s.cycles.use_preview_denoising=False
s.view_settings.look='AgX - Medium High Contrast';s['lighting_recipe']='KEY8W1.1m / FILL5.2W0.9m / RIM8W0.8m; world0.45 neutral; AgX Medium High Contrast; exposure0; compared factors1,0.15,0.035 and chose0.08'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/08-neutral-studio-calibrated.blend'),compress=True)
(ROOT/'qa/lighting-correction.json').write_text(json.dumps({'initial':'overexposed 100/65/100W','probes':[.15,.035],'adopted_factor':.08,'exposure':0,'normal_maps_unchanged':True,'samples':192,'adaptive_threshold':.015},indent=2))
print('CALIBRATED_STUDIO_SAVED')
