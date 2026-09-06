"""Review-driven exterior corrections, run in existing build namespace."""

def finish_external():
 global PART
 collection('03_24SFF_HOTSWAP_CARRIERS')
 for i in range(24):
  PART=bpy.data.objects[f'Carrier_{i:02d}_2p5inch'];x=(i-11.5)*.0174
  ob=box(f'Carrier{i:02}_setback_dark_air_shade',(x,F-.001,.0416),(.0115,.0008,.044),'DarkCavity',.00007)
  ob['source_basis']='Opaque recess shading behind genuine carrier vent, dark nose ahead of physical disk envelope'
 # Normal bump is deliberately restrained at whole-device scale; GLSL and glTF use same maps.
 for name,strength in [('Zinc',.035),('Nickel',.06),('ABS',.32),('Nylon',.65)]:
  m=MAT.get(name)
  if m:
   for n in m.node_tree.nodes:
    if n.type=='NORMAL_MAP':n.inputs['Strength'].default_value=strength
 for name,strength in [('BlueLatch',.22),('OrangeLatch',.20),('ButtonBlack',.20)]:
  m=MAT[name];nt=m.node_tree;bs=nt.nodes.get('Principled BSDF')
  tx=nt.nodes.new('ShaderNodeTexImage');tx.image=bpy.data.images.get('abs-normal.png');nm=nt.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=strength;nt.links.new(tx.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs[0],bs.inputs['Normal']);m['physical_texture_repeat_m']=.0256
 sc=bpy.context.scene;sc.eevee.use_gtao=True;sc.eevee.gtao_distance=.025;sc.eevee.gtao_factor=1.25;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
 # Studio lighting changes are retained; no additional color/compositing affects exported model.
 all_uv()
 for ob in sc.objects:ob.select_set(False)
 for f in ['build_c6420_v2.py','normal_carriers_v2.py','rear_v2.py','psu_and_labels_v2.py','finish_external_v2.py','studio_v2.py','refine_studio_materials.py']:
  tx=bpy.data.texts.get(f) or bpy.data.texts.new(f);tx.clear();tx.write((P/'scripts'/f).read_text())
 viewport((.85,-1.8,.40),1.22,shading='MATERIAL');save('07-photographic-exterior-complete.blend')
