import bpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene
s.render.resolution_x=900;s.render.resolution_y=600;s.cycles.samples=32;s.cycles.adaptive_threshold=.05
lights={o.name:o.data.energy for o in s.objects if o.type=='LIGHT'}
for factor in [.15,.035]:
 for n,e in lights.items():bpy.data.objects[n].data.energy=e*factor
 s.render.filepath=str(ROOT/'qa'/f'lighting-factor-{factor}.png');bpy.ops.render.render(write_still=True)
print({m.name:list(m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value) for m in bpy.data.materials if m.use_nodes and m.node_tree.nodes.get('Principled BSDF')})
