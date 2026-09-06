# Background Blender is used for scheduled preview rendering only.
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sc=bpy.context.scene;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
sc.render.filepath=str(ROOT/'previews/first-front-right.png');bpy.ops.render.render(write_still=True)
