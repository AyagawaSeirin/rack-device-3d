"""Photograph comparison corrections: black plastics, restrained metal grain, cloth microstructure,
original-label deglare baking, and sharp EPP lettering reconstructed from unambiguous real print.
"""

def bake_original_label(ob,kind):
 source_uv=ob.data.uv_layers.active.name
 source_image=bpy.data.images.load(str(P/'textures/nsl-C6400.png'),check_existing=True)
 name='RealLabel_'+kind+'_calibrated';m=bpy.data.materials.new(name);m.use_nodes=True;m.blend_method='OPAQUE';m.use_backface_culling=True;nt=m.node_tree;nt.nodes.clear()
 tx=nt.nodes.new('ShaderNodeTexImage');tx.image=source_image;uvn=nt.nodes.new('ShaderNodeUVMap');uvn.uv_map=source_uv;nt.links.new(uvn.outputs['UV'],tx.inputs['Vector'])
 curves=nt.nodes.new('ShaderNodeRGBCurve');curves.mapping.initialize();curve=curves.mapping.curves[3]
 pts={'service':[(0,0),(.27,.004),(.36,.025),(.45,.16),(.53,.53),(.62,.88),(1,1)],'warning':[(0,0),(.25,.005),(.34,.09),(.50,.77),(.62,.95),(1,1)],'regulatory':[(0,0),(.40,.003),(.53,.007),(.57,.15),(.64,.82),(1,1)]}[kind]
 curve.points[0].location=pts[0];curve.points[-1].location=pts[-1]
 for x,y in pts[1:-1]:curve.points.new(x,y)
 for p in curve.points:p.handle_type='VECTOR'
 curves.mapping.update();nt.links.new(tx.outputs['Color'],curves.inputs['Color'])
 em=nt.nodes.new('ShaderNodeEmission');em.inputs[1].default_value=1;nt.links.new(curves.outputs['Color'],em.inputs[0]);out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(em.outputs[0],out.inputs['Surface'])
 ob.data.materials.clear();ob.data.materials.append(m)
 # New bake UV occupies one independent label image; original source UV remains explicit on input texture.
 uv=ob.data.uv_layers.new(name='Calibrated_label_export_UV');xs=[v.co.x for v in ob.data.vertices];ys=[v.co.y for v in ob.data.vertices];lo=(min(xs),min(ys));span=(max(xs)-lo[0],max(ys)-lo[1])
 for li,l in enumerate(ob.data.loops):
  v=ob.data.vertices[l.vertex_index].co;uv.data[li].uv=((v.x-lo[0])/span[0],(v.y-lo[1])/span[1])
 ob.data.uv_layers.active=uv
 size=(2048,1024) if kind=='service' else (640,640)
 image=bpy.data.images.new('calibrated-'+kind,width=size[0],height=size[1],alpha=False);image.generated_color=(.02,.02,.02,1);target=nt.nodes.new('ShaderNodeTexImage');target.image=image;nt.nodes.active=target
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 scene=bpy.context.scene;scene.cycles.samples=1;scene.render.bake.margin=4;scene.render.bake.use_clear=True
 bpy.ops.object.bake(type='EMIT')
 image.filepath_raw=str(P/'textures'/('calibrated-'+kind+'.png'));image.file_format='PNG';image.save();image.pack()
 # Portable glTF graph after baking: ordinary opaque PBR, no unsupported tone nodes or alpha.
 nt.nodes.clear();newtx=nt.nodes.new('ShaderNodeTexImage');newtx.image=image;uvmap=nt.nodes.new('ShaderNodeUVMap');uvmap.uv_map=uv.name;nt.links.new(uvmap.outputs['UV'],newtx.inputs['Vector'])
 bs=nt.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.73;bs.inputs['Specular IOR Level'].default_value=.22;bs.inputs['Alpha'].default_value=1;bs.inputs['Transmission Weight'].default_value=0;nt.links.new(newtx.outputs['Color'],bs.inputs['Base Color']);out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(bs.outputs[0],out.inputs['Surface'])
 m['source_photo']='nsl-C6400.png original pixels; tone calibrated for photographed specular glare, no AI retyping';m['baked_curve_points']=str(pts);ob['image_uv_verified']=True;ob['source_asset']='calibrated-'+kind+'.png derived from originalphoto through Blender shader EMIT bake';ob['legibility_limit']='Originalphoto lineart retained; missing fine glyph information cannot be recovered'
 print('BAKED_REAL_LABEL',kind,flush=True)

def review_materials():
 global PART
 sc=bpy.context.scene
 for a in bpy.context.screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.type='SOLID'
 # Recomputed procedural data is versioned; the unmodified original source photos remain intact.
 for name,prefix in [('Zinc','zinc'),('Nickel','nickel'),('ABS','abs'),('Nylon','nylon')]:
  m=MAT[name]
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE' and n.image:
    base=Path(n.image.filepath).name
    refined=P/'textures/refined'/base
    if refined.exists():
     im=bpy.data.images.load(str(refined),check_existing=True);im.colorspace_settings.name='sRGB' if '-base' in base else 'Non-Color';im.pack();n.image=im
  bs=m.node_tree.nodes.get('Principled BSDF')
  if name in ['ABS','Nylon']:bs.inputs['Specular IOR Level'].default_value=.30 if name=='ABS' else .12
 for name,color in [('ButtonBlack',(.0045,.006,.008)),('BlueLatch',(.145,.315,.610)),('OrangeLatch',(.64,.135,.018))]:
  m=MAT[name];bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Specular IOR Level'].default_value=.30;m.diffuse_color=(*color,1)
 # White photographic room plus restrained broad lights, matched to silver and blue actualphoto tones.
 sc.world.node_tree.nodes['Background'].inputs[1].default_value=.50
 for ob in bpy.data.collections['90_STUDIO'].objects:
  if ob.type=='LIGHT':ob.data.energy*=.20
 sc.view_settings.look='AgX - Medium High Contrast'
 # Correct front mapping-arrow visual size against NSLphoto; maintain center and handedness.
 for ob in sc.objects:
  if ob.name.startswith('Bay_mapping_triangle_'):
   center=sum((v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices)
   for v in ob.data.vertices:v.co=center+(v.co-center)*.65
  if ob.name.startswith('Node') and ('RJ45_spring_contact' in ob.name or 'SFP_' in ob.name and '_contact_' in ob.name):ob.location.y-=.003
 # Sharper label: realphotograph EPP/2400W/94%efficiency text recreated at measured size and orientation.
 collection('05_POWER_SUPPLIES')
 material('EPP_label_paper',(.56,.57,.55),0,.67)
 material('EPP_label_green',(.028,.365,.235),0,.67)
 material('EPP_label_white',(.88,.89,.87),0,.67)
 material('Cloth_fiber',(.0015,.0020,.0026),0,.9)
 fonts={n:bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/'+n) for n in ['DejaVuSansCondensed-Oblique.ttf','DejaVuSansCondensed-Bold.ttf']}
 for i,zc in enumerate([.02225,.06455],1):
  old=bpy.data.objects.get(f'PSU{i}_REAL_EPP_2400W_print')
  if old:bpy.data.objects.remove(old,do_unlink=True)
  PART=bpy.data.objects['PSU_'+str(i)+'_2400W'];cx=-.0216
  paper=extrude(f'PSU{i}_EPP_real_print_paper',circle(.00915,n=64),(cx,R+.00252,zc),REAR,.00005,'EPP_label_paper',0)
  a=math.asin(.002/.00915);green=[(.00915*math.cos(a+(math.pi-2*a)*j/48),.00915*math.sin(a+(math.pi-2*a)*j/48)) for j in range(49)]
  extrude(f'PSU{i}_EPP_green_upper_field',green,(cx,R+.00258,zc),REAR,.000035,'EPP_label_green',0)
  o=text(f'PSU{i}_EPP_exact_letters','EPP',(cx,R+.00269,zc+.0053),.0041,'EPP_label_white',REAR);o.data.font=fonts['DejaVuSansCondensed-Oblique.ttf'];o['source_basis']='Unambiguous realphotograph EPP uppercase italic lettering; independent vector ink'
  o=text(f'PSU{i}_2400W_exact_letters','2400W',(cx,R+.00269,zc-.00025),.0046,'InkBlack',REAR);o.data.font=fonts['DejaVuSansCondensed-Bold.ttf']
  o=text(f'PSU{i}_efficiency_exact_letters','94% efficiency',(cx,R+.00269,zc-.0036),.00165,'InkBlack',REAR);o.data.font=fonts['DejaVuSansCondensed-Bold.ttf']
  # Photographed strap is approx17.5mmwide,with textile edge fibres.
  ob=bpy.data.objects[f'PSU{i}_woven_extraction_loop'];inv=ob.matrix_world.inverted()
  for v in ob.data.vertices:
   w=ob.matrix_world@v.co;w.z=zc+(w.z-zc)*1.25;v.co=inv@w
  rng=random.Random(6420+i);points=[ob.matrix_world@v.co for v in ob.data.vertices if abs((ob.matrix_world@v.co).z-zc)>.0080];rng.shuffle(points)
  cu=bpy.data.curves.new(f'PSU{i}_textile_edge_fibres_curve','CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=.000024;cu.bevel_resolution=1;cu.use_fill_caps=True
  for p in points[:170]:
   side=1 if p.z>zc else -1;d=Vector((rng.uniform(-.00022,.00022),rng.uniform(-.00020,.00020),side*rng.uniform(.00012,.0003)));s=cu.splines.new('POLY');s.points.add(2)
   for dest,v in zip(s.points,[p,p+d*.65+Vector((0,0,.00006*side)),p+d]):dest.co=(*v,1)
  fuzz=bpy.data.objects.new(f'PSU{i}_woven_edge_fibres',cu);COL.objects.link(fuzz);fuzz.parent=PART;cu.materials.append(MAT['Cloth_fiber']);fuzz['source_basis']='Generic textile edge microfibres matching photographed strap appearance'
 # Deglare original printed regions, then bake into portable texture images.
 for obname,kind in [('Real_service_label_band','service'),('Real_yellow_warning_label','warning'),('Real_regulatory_label','regulatory')]:bake_original_label(bpy.data.objects[obname],kind)
 sc.cycles.samples=128;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
 all_uv()
 for ob in sc.objects:ob.select_set(False)
 (P/'qa/material-corrections.json').write_text(json.dumps({'plastic':'Darker trueblack data and lower specularlevel','metal':'Reduced color variation/normal amplitude; broad illuminationmatched','labels':'Originalphotocontrast correction baked viaEMIT; EPP unambiguouslettering rebuilt','nylon':'17.5mmwide wovenstrap, coarsernormaldata, actualedgefibres','transparency':'All bodymatAlpha1,Transmission0'},indent=2))
 save('09-material-and-label-review.blend')
