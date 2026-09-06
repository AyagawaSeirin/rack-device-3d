import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.use_gtao=True;s.eevee.gtao_distance=.05;s.eevee.gtao_factor=1.1;s.eevee.taa_render_samples=128;s.eevee.use_soft_shadows=True
s.render.resolution_x=1200;s.render.resolution_y=800
s.render.filepath=str(ROOT/'qa/eevee-front-probe.png');bpy.ops.render.render(write_still=True)
c=s.camera;c.location=(-.208,-.55,.042);c.rotation_euler=(Vector((-.205,-.32,.024))-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.080
s.render.filepath=str(ROOT/'qa/eevee-brand-probe.png');bpy.ops.render.render(write_still=True)
