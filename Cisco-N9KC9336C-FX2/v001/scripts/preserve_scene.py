import bpy, json
from pathlib import Path
p=Path('/root/Project/rack-device-3d/Cisco-N9KC9336C-FX2/v001')
s={'original_file':bpy.data.filepath,'was_dirty':bpy.data.is_dirty,'blender_version':bpy.app.version_string,'scene':bpy.context.scene.name}
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
s['saved']=True
(p/'qa/pre-task-blender-state.json').write_text(json.dumps(s,indent=2))
print(s)
