import bpy,bmesh
from pathlib import Path
P=Path('/root/Blender/DELL-C6420/v001');p=P/'scripts/build_c6420.py';ns={'__name__':'c6420_finish','__file__':str(p)}
exec(compile(p.read_text(),str(p),'exec'),ns);ns['MAT']={m.name:m for m in bpy.data.materials}
prior=set(bpy.context.scene.objects)
ns['collection']('05_POWER_SUPPLIES')
for i,z in enumerate([.02225,.06455],1):
 ns['PART']=bpy.data.objects['Power_Supply_'+str(i)]
 ns['panel']('PSU%d_black_AC_rim'%i,.033,.036,[(0,0,.027,.031)],(.023,.3830,z),'Plastic',ns['REAR'],.0015)
 for ob in bpy.context.scene.objects:
  if ob.name.startswith('PSU%d_AC_inlet'%i) and any(x in ob.name for x in ['sidewall','horizontalwall']):
   ob.data.materials.clear();ob.data.materials.append(ns['MAT']['Plastic'])
ns['collection']('06_FASTENERS_AND_STAMPING')
# Raised edge of shallow sheet-metal embosses, under max chassis height.
for xc in [-.112,0,.112]:
 points=[(xc-.043,-.343,.08643),(xc+.043,-.343,.08643),(xc+.043,-.319,.08643),(xc+.012,-.319,.08643),(xc+.012,-.275,.08643),(xc-.012,-.275,.08643),(xc-.012,-.319,.08643),(xc-.043,-.319,.08643)]
 ns['tube_curve']('Front_cover_shallow_T_stamp',points,.00016,'Steel',True)
# Small rear embossed channel / unlabeled service recess, observed gross arrangement only.
for yy in [.283,.327]:
 points=[(-.040,yy,.08643),(.040,yy,.08643),(.040,yy+.005,.08643),(-.040,yy+.005,.08643)]
 ns['tube_curve']('Rear_cover_shallow_stamp',points,.00016,'Steel',True)
new=[o for o in bpy.context.scene.objects if o not in prior]
bpy.ops.object.select_all(action='DESELECT')
for ob in new:ob.select_set(True)
bpy.context.view_layer.objects.active=new[0];bpy.ops.object.convert(target='MESH')
for ob in new:
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
# Balanced studio light levels preserve metal contrast and saturated service latches.
for ob in bpy.context.scene.objects:
 if ob.type=='LIGHT':ob.data.energy*=.35
bpy.context.scene.world.node_tree.nodes['Background'].inputs[1].default_value=.30
bpy.context.scene.cycles.samples=96
bpy.ops.object.select_all(action='DESELECT')
for tx in ['build_c6420.py','repair_geometry.py','refine_finish.py']:
 t=bpy.data.texts.get(tx) or bpy.data.texts.new(tx);t.clear();t.write((P/'scripts'/tx).read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/07-finish-reviewed.blend'))
print('Refined AC black housings, stamped channels, studio lighting')
