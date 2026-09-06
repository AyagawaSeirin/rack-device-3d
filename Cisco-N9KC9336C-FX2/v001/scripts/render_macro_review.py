import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene;c=s.camera
s.render.resolution_x=1600;s.render.resolution_y=900;s.cycles.samples=192;s.cycles.adaptive_threshold=.012
jobs=[('front-brand-macro',(-.205,-.32,.024),(-.208,-.55,.042),.080),('rear-review',(0,.29,.022),(-.65,1.4,.60),.73)]
for name,target,pos,scale in jobs:
 c.location=pos;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 s.render.filepath=str(ROOT/'previews'/f'{name}.png');bpy.ops.render.render(write_still=True)
