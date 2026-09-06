"""Photographic exterior rebuild, v002. Executed in the existing Blender via MCP.
All lengths m. Geometry follows NSL/ETB locked photographs and official dimensions.
AI references are excluded from geometric measurement and logo textures.
"""
import bpy,bmesh,math,json,random
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.geometry import delaunay_2d_cdt,tessellate_polygon
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002')
W,H,D=.448,.0868,.7632;F,R=-D/2,D/2
FRONT=((1,0,0),(0,0,1),(0,-1,0));REAR=((-1,0,0),(0,0,1),(0,1,0));TOP=((1,0,0),(0,1,0),(0,0,1));BOTTOM=((-1,0,0),(0,1,0),(0,0,-1))
RIGHT=((0,1,0),(0,0,1),(1,0,0));LEFT=((0,-1,0),(0,0,1),(-1,0,0))
MAT={};COL=None;PART=None

def collection(name):
 global COL,PART
 COL=bpy.data.collections.get(name)
 if COL is None:COL=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(COL)
 PART=None;return COL

def group(name,kind):
 global PART
 ob=bpy.data.objects.new(name,None);COL.objects.link(ob);ob.empty_display_size=.006
 ob['component_type']=kind;PART=ob;return ob

def mesh(name,verts,faces,mat='Zinc'):
 me=bpy.data.meshes.new(name+'_mesh');me.from_pydata(verts,[],faces);me.update()
 ob=bpy.data.objects.new(name,me);COL.objects.link(ob)
 if PART:ob.parent=PART
 if mat:me.materials.append(MAT[mat] if isinstance(mat,str) else mat)
 ob['source_basis']='NSL/ETB 24SFF four-node photographs; local detail estimated from pixels'
 return ob

def basis(ob,pos,axes):
 u,v,n=map(Vector,axes);ob.matrix_world=Matrix(((u.x,v.x,n.x,pos[0]),(u.y,v.y,n.y,pos[1]),(u.z,v.z,n.z,pos[2]),(0,0,0,1)));return ob

def bevel(ob,w=.00015,n=3):
 if w:
  m=ob.modifiers.new('Small manufactured edge radius','BEVEL');m.width=w;m.segments=n;m.limit_method='ANGLE';m.angle_limit=.28
  m=ob.modifiers.new('Face weighted corner normals','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=35
 return ob

def box(name,loc,size,mat='Zinc',edge=.00012):
 x,y,z=[v/2 for v in size];vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
 ob=mesh(name,vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat);ob.location=loc
 return bevel(ob,min(edge,min(size)*.24),3)

def rounded(w,h,r=.001,c=(0,0),steps=4):
 r=min(r,w*.49,h*.49);out=[]
 for x,y,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for i in range(steps+1):
   a=math.radians(start+i*90/steps);out.append((c[0]+x+r*math.cos(a),c[1]+y+r*math.sin(a)))
 return out

def circle(r,c=(0,0),n=32):return [(c[0]+r*math.cos(i*math.tau/n),c[1]+r*math.sin(i*math.tau/n)) for i in range(n)]
def inside(p,poly):
 x,y=p;v=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if ((a[1]>y)!=(b[1]>y)) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:v=not v
 return v

def fillet(poly,r=.002,n=4):
 out=[]
 for i,p in enumerate(poly):
  p=Vector(p);a=Vector(poly[i-1]);b=Vector(poly[(i+1)%len(poly)]);rr=min(r,(a-p).length*.3,(b-p).length*.3);q=p+(a-p).normalized()*rr;s=p+(b-p).normalized()*rr
  for j in range(n+1):t=j/n;v=(1-t)**2*q+2*t*(1-t)*p+t*t*s;out.append(tuple(v))
 return out

def inset(poly,d):
 out=[]
 for i,p in enumerate(poly):
  p=Vector(p);a=(p-Vector(poly[i-1])).normalized();b=(Vector(poly[(i+1)%len(poly)])-p).normalized();n1=Vector((-a.y,a.x));n2=Vector((-b.y,b.x));bis=(n1+n2).normalized();den=bis.dot(n1)
  out.append(tuple(p+bis*d/max(.15,den)))
 return out

def surface_2d(outer,holes):
 loops=[outer]+holes;vs=[];es=[]
 for loop in loops:
  k=len(vs);vs.extend(Vector(p) for p in loop);es.extend((k+i,k+(i+1)%len(loop)) for i in range(len(loop)))
 ov,oe,of,*_=delaunay_2d_cdt(vs,es,[],1,1e-8,False)
 faces=[]
 for f in of:
  q=sum((ov[i] for i in f),Vector((0,0)))/len(f)
  if inside(q,outer) and not any(inside(q,h) for h in holes):faces.append(tuple(f))
 return [(v.x,v.y,0) for v in ov],faces

def plate(name,outer,holes,pos,mat='Zinc',axes=REAR,t=.00085,pockets=None,edge=.00008):
 """One continuous stamped sheet: real rounded through-apertures and integrated pressed recesses."""
 pockets=pockets or [];allholes=holes+[p[0] for p in pockets];vs,fs=surface_2d(outer,allholes)
 for contour,depth,shoulder in pockets:
  inner=inset(contour,shoulder);k=len(vs);vs += [(x,y,0) for x,y in contour]+[(x,y,-depth) for x,y in inner];n=len(contour)
  for i in range(n):j=(i+1)%n;fs.append((k+i,k+j,k+n+j,k+n+i))
  subholes=[h for h in holes if inside(h[0],inner)];sv,sf=surface_2d(inner,subholes);k=len(vs);vs += [(x,y,-depth) for x,y,z in sv];fs += [tuple(k+i for i in f) for f in sf]
 ob=basis(mesh(name,vs,fs,mat),pos,axes)
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=2e-8);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
 so=ob.modifiers.new('Physical formed sheet thickness','SOLIDIFY');so.thickness=t;so.offset=-1;so.use_even_offset=True
 bevel(ob,edge,2);ob['actual_through_holes']=len(holes);ob['integrated_stamped_recesses']=len(pockets)
 return ob

def extrude(name,poly,pos,axes,depth,mat='Zinc',edge=.00015):
 n=len(poly);vs=[(x,y,z) for z in [0,-depth] for x,y in poly];fs=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
 return bevel(basis(mesh(name,vs,fs,mat),pos,axes),edge,3)

def cyl(name,pos,r,depth,mat='Nickel',axes=TOP,n=40,edge=.00008):
 ob=extrude(name,circle(r,n=n),pos,axes,depth,mat,edge)
 for f in ob.data.polygons:
  if len(f.vertices)==4:f.use_smooth=True
 return ob

def ring(name,pos,ro,ri,depth,mat='Nickel',axes=REAR,n=48):return plate(name,circle(ro,n=n),[circle(ri,n=n)],pos,mat,axes,depth,edge=.00005)

def curve(name,points,r,mat='Nickel',cyclic=False):
 cu=bpy.data.curves.new(name+'_curve','CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=r;cu.bevel_resolution=3;cu.use_fill_caps=True
 sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,q in zip(sp.points,points):p.co=(*q,1)
 sp.use_cyclic_u=cyclic;ob=bpy.data.objects.new(name,cu);COL.objects.link(ob);cu.materials.append(MAT[mat])
 if PART:ob.parent=PART
 return ob

def text(name,body,pos,size,mat='InkWhite',axes=REAR,align='CENTER',rotate=0):
 cu=bpy.data.curves.new(name+'_font','FONT');cu.body=body;cu.size=size;cu.align_x=align;cu.align_y='CENTER';cu.extrude=0;cu.resolution_u=5
 font=bpy.data.fonts.get('DejaVuSansCondensed.ttf')
 if not font:
  try:font=bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf')
  except:pass
 if font:cu.font=font
 ob=bpy.data.objects.new(name,cu);COL.objects.link(ob);cu.materials.append(MAT[mat]);basis(ob,pos,axes)
 if rotate:ob.matrix_world=ob.matrix_world@Matrix.Rotation(rotate,4,'Z')
 if PART:ob.parent=PART
 ob['readable_text']=body;ob['intentional_open_surface']='Opaque printed mark; correct face normal and independent UV/orientation';return ob

def material(name,color,metal=0,rough=.45,texture=None,repeat=.04):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1);m.blend_method='OPAQUE';m.use_backface_culling=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;bs.inputs['Alpha'].default_value=1;bs.inputs['Transmission Weight'].default_value=0
 if texture:
  for typ,socket in [('base','Base Color'),('rough','Roughness'),('normal','Normal')]:
   tx=m.node_tree.nodes.new('ShaderNodeTexImage');im=bpy.data.images.load(str(P/'textures'/f'{texture}-{typ}.png'),check_existing=True);im.colorspace_settings.name='sRGB' if typ=='base' else 'Non-Color';im.pack();tx.image=im;tx.interpolation='Linear';tx.extension='REPEAT'
   if typ=='normal':
    nm=m.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=1;m.node_tree.links.new(tx.outputs['Color'],nm.inputs['Color']);m.node_tree.links.new(nm.outputs[0],bs.inputs[socket])
   else:m.node_tree.links.new(tx.outputs['Color'],bs.inputs[socket])
 m['physical_texture_repeat_m']=repeat;MAT[name]=m;return m

def photo_material(name,path,metal=0,rough=.52):
 m=material(name,(.4,.4,.4),metal,rough);tx=m.node_tree.nodes.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(P/'textures'/path),check_existing=True);tx.image.pack();tx.interpolation='Linear';m.node_tree.links.new(tx.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color']);m['source_photo']=path;return m

def photo_patch(name,mat,poly,uv,pos,axes=TOP):
 ob=basis(mesh(name,[(x,y,0) for x,y in poly],[tuple(range(len(poly)))],mat),pos,axes);layer=ob.data.uv_layers.new(name='PHOTO_verified_handedness')
 for l,co in zip(layer.data,uv):l.uv=co
 ob['intentional_open_surface']='Opaque printed/photo label region only; physical substrate separate';ob['image_uv_verified']=True;return ob

def save(name):
 bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(P/'model'/name));print('V002_SAVED',name,len(bpy.context.scene.objects),flush=True)

def viewport(direction=(.65,-1.5,.65),distance=1.25,center=(0,0,.04),shading='MATERIAL'):
 for screen in bpy.data.screens:
  for a in screen.areas:
   if a.type=='VIEW_3D':
    s=a.spaces.active;s.clip_start=.001;s.clip_end=20;s.overlay.show_overlays=False;s.shading.type=shading
    if shading=='MATERIAL':s.shading.studiolight_rotate_z=.6;s.shading.studiolight_intensity=.8
    s.region_3d.view_distance=distance;s.region_3d.view_location=Vector(center);s.region_3d.view_rotation=Vector(direction).to_track_quat('Z','Y');s.region_3d.view_perspective='PERSP'

# Stage functions appended below; each is executed once through MCP with a checkpoint.

def uv_physical(ob):
 if ob.type!='MESH' or ob.get('image_uv_verified') or ob.get('readable_text'):return
 if not ob.data.materials:return
 m=ob.data.materials[0];repeat=m.get('physical_texture_repeat_m',.04)
 uv=ob.data.uv_layers.get('Physical_scale_UV') or ob.data.uv_layers.new(name='Physical_scale_UV')
 for f in ob.data.polygons:
  n=f.normal;a=max(range(3),key=lambda j:abs(n[j]));sg=1 if n[a]>=0 else -1
  for li in f.loop_indices:
   p=ob.data.vertices[ob.data.loops[li].vertex_index].co
   co=(sg*p.x,p.y) if a==2 else ((-sg*p.x,p.z) if a==1 else (sg*p.y,p.z))
   uv.data[li].uv=(co[0]/repeat,co[1]/repeat)

def all_uv():
 for o in bpy.context.scene.objects:uv_physical(o)

def screw(name,pos,r=.0018,axes=TOP,mat='Nickel',angle=0):
 w=r*.28;a=r*.67
 cross=[(-w,-a),(w,-a),(w,-w),(a,-w),(a,w),(w,w),(w,a),(-w,a),(-w,w),(-a,w),(-a,-w),(-w,-w)]
 cross=[(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle)) for x,y in cross]
 ob=plate(name+'_recessed_head',circle(r,n=40),[fillet(cross,r*.06,2)],pos,mat,axes,.00065,edge=.00007)
 n=Vector(axes[2]);cyl(name+'_recess_floor',Vector(pos)-n*.00072,r*.78,.0004,'DarkSteel',axes,32,0)
 return ob

def stage1():
 global MAT
 assert (P/'references/SELECTED.txt').exists(),'Finish reviewed reference set before modeling'
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 for c in list(bpy.data.collections):bpy.data.collections.remove(c)
 for m in list(bpy.data.materials):
  if not m.users:bpy.data.materials.remove(m)
 sc=bpy.context.scene;sc.name='C6420_4N_24SFF_v002_MASTER';sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1;sc.unit_settings.length_unit='MILLIMETERS'
 sc['project']='Dell PowerEdge C6420 4-node complete system, C6400 24x2.5-inch chassis';sc['version']='v002 photographic rebuild';sc['front_state']='24 genuine black plastic 2.5-inch fillers as in locked photographs; storage capacity unspecified'
 sc['axes']='front -Y; rear +Y; physical right +X; Z up; floor Z=0';sc['assumptions']='Underside generic inferred; hidden internals external-visibility only; microscopic surfaces not scanned'
 sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=96;sc.cycles.preview_samples=24;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
 sc.render.threads_mode='FIXED';sc.render.threads=10;sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=0
 MAT={}
 material('Zinc',(.58,.59,.60),1,.33,'zinc',.04)
 material('Nickel',(.68,.69,.70),1,.22,'nickel',.032)
 material('ABS',(.014,.016,.019),0,.49,'abs',.0256)
 material('Nylon',(.009,.010,.012),0,.8,'nylon',.0256)
 for args in [('DarkSteel',(.095,.11,.12),.9,.40),('DarkCavity',(.004,.005,.007),0,.83),('ButtonBlack',(.016,.019,.022),0,.32),('BlueLatch',(.19,.38,.66),0,.36),('USBBlue',(.015,.07,.29),0,.33),('OrangeLatch',(.72,.15,.02),0,.42),('GoldContact',(.54,.39,.12),1,.27),('PowerLens',(.27,.25,.09),.35,.34),('LEDGreenOff',(.018,.055,.024),0,.28),('PCB',(.025,.065,.036),.15,.55),('InkWhite',(.75,.77,.78),0,.58),('InkBlack',(.011,.012,.013),0,.65),('InkGray',(.22,.25,.27),0,.62)]:material(*args)
 # Chassis continuous sheet panels, rounded stamped recesses. Missing underside is explicit.
 collection('01_CHASSIS_SHEETMETAL')
 bottom=plate('INFERRED_bottom_formed_sheet',rounded(W,D,.001),[],(0,0,0),'Zinc',BOTTOM,.00085,pockets=[(rounded(.005,.632,.002,c=(x,0)),.0007,.00065) for x in [-.135,-.045,.045,.135]],edge=.00006)
 bottom['assumption']='AI inferred generic underside: four inward pressed strengthening beads, no real bottom photo'
 for s,axes in [(1,RIGHT),(-1,LEFT)]:
  # Right wall is photographed. Opposite-side detail is approximate rather than a flipped photo.
  holes=[]
  for y,z in [(-.338,.022),(-.263,.023),(-.315,.062),(-.235,.057),(-.196,.023),(-.143,.062),(-.071,.024),(-.057,.063),(.031,.023),(.076,.062),(.142,.025),(.204,.062),(.256,.024),(.321,.062),(.351,.025)]:
   holes.append(circle(.00115,(y*s,z-H/2),20))
  side=plate('Right_side_wall' if s>0 else 'Left_side_wall_estimated',rounded(D,H,.0007),holes,(s*W/2,0,H/2),'Zinc',axes,.00085,edge=.00008)
  if s<0:side['assumption']='Left-side hole pattern estimated; photo itself not mirrored'
  box('Side_upper_inward_return_'+str(s),(s*.2198,0,H-.0018),(.0074,D-.002,.00085),'Zinc',.00008)
  box('Side_lower_inward_hem_'+str(s),(s*.219,0,.0015),(.0085,D-.002,.00085),'Nickel',.00009)
  # Cover skirt forms a thin stepped seam, within outer body width.
  box('Top_cover_side_skirt_'+str(s),(s*.2235,-.009,.0818),(.0008,.440,.0094),'Zinc',.00008)
  for y in [-.182,-.095,.051,.173]:screw('Cover_skirt_screw_'+str(s),(s*.22398,y,.0821),.00175,axes)
  for j,(y,z,r) in enumerate([(-.347,.028,.0028),(-.282,.025,.0024),(-.347,.063,.0028),(-.283,.066,.0018),(-.231,.042,.0016),(-.182,.027,.0018),(-.139,.064,.0019),(-.045,.025,.0018),(.076,.025,.0018),(.196,.025,.0018),(.306,.025,.0018)]):
   screw(f'Side_{s}_fastener_{j}',(s*.22422,y,z),r,axes,angle=(j*.37))
  for j,y in enumerate([-.327,-.244,-.196,-.108,.004,.132,.251,.342]):
   # Clinched/pressed fixing dimples, not decorative screw discs.
   ring(f'Side_{s}_clinch_{j}',(s*.22408,y,.052 if j%3==0 else .018),.0015,.00075,.00022,'Zinc',axes,28)
  # Two tiny captive flaps at side rail interfaces.
  plate('Side_rail_latch_outline_'+str(s),rounded(.025,.012,.0008),[rounded(.001,.007,.0003,c=(.009,0))],(s*.22412,.291,.041),'Zinc',axes,.0007,edge=.00006)
 # Front fixed cover: a broad concave stamping with three notch returns, integral to sheet.
 front_end=F-.017;front_back=-.2105
 notch=[(-.207,-.365),(.207,-.365),(.207,-.268),(.119,-.268),(.119,-.306),(.102,-.306),(.102,-.268),(.009,-.268),(.009,-.306),(-.009,-.306),(-.009,-.268),(-.102,-.268),(-.102,-.306),(-.119,-.306),(-.119,-.268),(-.207,-.268)]
 outer=[(-.2234,front_end),(.2234,front_end),(.2234,front_back),(-.2234,front_back)]
 holes=[]
 for x in [-.216,-.111,0,.111,.216]:
  for y in [-.378,-.291]:holes.append(circle(.0015,(x,y),24))
 for x in [-.218,.218]:
  for y in [-.351,-.327,-.268,-.241]:holes.append(rounded(.003,.0018,.0006,c=(x,y)))
 plate('Front_cover_integrated_pressings',outer,holes,(0,0,H-.0003),'Zinc',TOP,.00085,pockets=[(fillet(notch,.003,5),.00065,.00065),(rounded(.416,.011,.005,c=(0,-.228)),.00055,.00065)],edge=.00007)
 # Main cover with authentic central sticker recess. Top printing added later from original photo UV.
 plate('Main_cover_with_label_pressing',rounded(.4468,.4457,.0008),[rounded(.016,.006,.0005,c=(.014,-.056)),rounded(.005,.002,.0003,c=(-.04,-.220)),rounded(.005,.002,.0003,c=(.012,-.220))],(0,.01245,H-.0003),'Zinc',TOP,.00085,pockets=[(rounded(.405,.223,.004,c=(0,.0525)),.00052,.0007)],edge=.00007)
 # Rear fixed cap, shallow stamped trays and two center grip depressions.
 rearcy=(.2358+R)/2;rearh=R-.2358
 plate('Rear_cover_four_pressed_regions',rounded(.4468,rearh,.0007),[],(0,rearcy,H-.0003),'Zinc',TOP,.00085,pockets=[(rounded(.17,.113,.002,c=(-.129,0)),.00055,.0007),(rounded(.17,.113,.002,c=(.129,0)),.00055,.0007),(rounded(.064,.022,.0018,c=(0,-.031)),.0009,.001),(rounded(.064,.022,.0018,c=(0,.027)),.0009,.001)],edge=.00007)
 for y in [-.2102,.2354]:box('Underlapping_cover_seam',(0,y,H-.0025),(.443,.014,.00085),'DarkSteel',.00008)
 for x in [-.195,.195]:box('Cover_traction_pad',(x,-.062,H-.00025),(.017,.012,.00015),'BlueLatch',.00002)
 box('Cover_release_recess_back',(.014,-.04355,H-.0021),(.017,.007,.0009),'DarkCavity',.00012)
 box('Cover_release_metal_tab',(.014,-.0418,H-.00045),(.014,.003,.0006),'Nickel',.00012)
 collection('06_FASTENERS')
 for x in [-.193,-.162,-.111,-.052,0,.052,.111,.162,.193]:
  for y in [-.372,-.338,-.281]:
   if y==-.281 and abs(x) in [.111,0]:continue
   z=H-.00022 if abs(x)==.111 else H-.00071
   screw('Front_cover_flush_screw',(x,y,z),.00125,TOP,angle=x*31+y)
 for x in [-.041,.041]:
  for y in [.257,.285,.329,.357]:screw('Rear_cover_flush_screw',(x,y,H-.00022),.0016,TOP,angle=y*11)
 collection('08_INTERNAL_SHADOW_STRUCTURE')
 for x in [-.1328,.1328]:box('Midheight_sled_shelf',(x,.10,.0434),(.1748,.56,.00085),'DarkSteel',.00006)
 for x in [-.0449,.0449]:box('Central_PSU_channel_divider',(x,.12,.0434),(.0009,.52,.083),'DarkSteel',.00006)
 # Necessary non-precision interior occluders, offset well behind openings.
 box('Front_backplane_shadow',(0,-.260,.0434),(.438,.0015,.078),'DarkCavity',.00008)
 for x in [-.18,-.09,.09,.18]:box('Hidden_backplane_socket',(x,-.270,.0434),(.030,.004,.059),'DarkSteel',.0002)
 # Rack ears, folded perimeter, front cage rails. Detailed molded controls follow in stage2.
 collection('02_FRONT_FRAME_AND_CONTROLS')
 for s in [-1,1]:
  box('Rack_ear_mount_'+str(s),(s*.23265,F+.0001,.0475),(.0173,.002,.0768),'DarkSteel',.00024)
  box('Control_ear_shell_'+str(s),(s*.23265,F-.008,.0599),(.0158,.014,.0545),'ABS',.0008)
  box('Lower_ear_screw_boss_'+str(s),(s*.23265,F-.006,.0217),(.0148,.010,.017),'ABS',.00065)
  # Narrow actual punched metal cheek and its inward return flange.
  holes=[]
  for j in range(12):holes.append(rounded(.0031,.00365,.0007,c=(-.0021,-.034+j*.006)))
  for z in [-.034,-.028,-.022,.004,.010,.016,.022]:holes.append(rounded(.0017,.00365,.0006,c=(.002, z)))
  plate('Front_punched_cheek_'+str(s),rounded(.0095,.0835,.0006),holes,(s*.2155,F-.0173,.0434),'Nickel',FRONT,.00085,edge=.00008)
  box('Front_cage_side_return_'+str(s),(s*.2215,F-.005,.0434),(.001,.025,.0835),'Zinc',.00009)
  # Chrome handle is a flattened solid formed loop: capsule side profile, extruded along X.
  yz=[(-.0015,-.027),(-.015,-.027),(-.0229,-.020),(-.0249,-.010),(-.0249,.011),(-.022,.022),(-.015,.029),(-.0015,.029)]
  # y here is forward relative mounting plane; z relative center. Sweep an oval wire cross-section.
  pts=[]
  for j in range(49):
   t=j/48;z=.026+.052*t;y=F-.004-.0208*math.sin(math.pi*t);pts.append((s*.2198,y,z))
  ob=curve('Chrome_lifting_handle_'+str(s),pts,.002,'Nickel');ob['front_outermost_m']=F-.0268
  # End brackets and real attachment tabs.
  for z in [.026,.078]:box('Handle_flat_anchor_'+str(s),(s*.2198,F-.007,z),(.0035,.010,.006),'Nickel',.0006)
 box('Front_lower_rolled_hem',(0,F-.014,.0011),(.439,.008,.0018),'Nickel',.00035)
 box('Front_upper_rolled_hem',(0,F-.014,H-.0011),(.439,.008,.0018),'Nickel',.00035)
 for k in range(5):
  x=(k-2)*.1044
  box('Drive_bank_divider_%d'%k,(x,F+.014,.0434),(.0007,.069,.0814),'Nickel',.00007)
 all_uv();viewport(shading='SOLID');save('01-photographic-shell.blend')

def filler_geometry(i,x):
 collection('03_24SFF_BLACK_BAY_FILLERS');root=group(f'Bay_{i:02d}_2p5inch_filler','2.5-inch bay filler');root['bay_index']=i;root['mapped_node']=i//6+1
 root['source']='NSL front and ITCreations macro, no orange/silver hot-swap carrier'
 # Actual injection-molded hollow skeleton: two full-depth thin sidewalls and cross ribs.
 for s in [-1,1]:
  box(f'Filler{i:02}_inner_sidewall_{s}',(x+s*.00715,F+.004,.0437),(.0012,.036,.076),'ABS',.00018)
  for z,h in [(.015,.016),(.0445,.0373),(.0737,.017)]:box(f'Filler{i:02}_outer_mold_rail',(x+s*.00665,F-.0149,z),(.0017,.0034,h),'ABS',.0002)
 for z in [.010,.028,.047,.064,.079]:box(f'Filler{i:02}_internal_cross_rib',(x,F+.007,z),(.013,.025,.0012),'ABS',.00018)
 # Raised central pad and two delicate molding ribs (not shiny metal levers).
 extrude(f'Filler{i:02}_long_center_pad',rounded(.0113,.0368,.0004),(x,F-.0158,.0445),FRONT,.0020,'ABS',.00014)
 for s in [-1,1]:
  box(f'Filler{i:02}_fine_vertical_pad_rib',(x+s*.00514,F-.0160,.0445),(.00048,.00055,.0363),'ABS',.00014)
  box(f'Filler{i:02}_mold_parting_land',(x+s*.00760,F-.0116,.0434),(.00032,.002,.0734),'ButtonBlack',.00007)
 # The upper recessed flat rectangular section sits back from the stepped top hook.
 extrude(f'Filler{i:02}_upper_inset_pad',fillet([(-.0055,-.0066),(.0055,-.0066),(.0059,.0066),(-.0059,.0066)],.00025,3),(x,F-.0123,.0716),FRONT,.0016,'ABS',.00012)
 box(f'Filler{i:02}_top_cross_cap',(x,F-.0145,.0805),(.0122,.0052,.0037),'ABS',.00023)
 for s in [-1,1]:box(f'Filler{i:02}_top_hook_cheek',(x+s*.00665,F-.0144,.0798),(.0018,.0054,.0052),'ABS',.00017)
 # Bottom finger-foot with trapezoidal shoulders and separate stepped ledges.
 foot=[(-.0037,-.0065),(.0037,-.0065),(.0037,.0027),(.0025,.0065),(-.0025,.0065),(-.0037,.0027)]
 extrude(f'Filler{i:02}_lower_shaped_foot',fillet(foot,.00055,4),(x,F-.0127,.0145),FRONT,.003,'ABS',.00018)
 box(f'Filler{i:02}_lower_step_top',(x,F-.0152,.0237),(.0095,.0043,.0025),'ABS',.0002)
 box(f'Filler{i:02}_lower_step_bottom',(x,F-.0152,.0069),(.0095,.0042,.0025),'ABS',.0002)
 box(f'Filler{i:02}_frame_bottom_bar',(x,F-.0145,.0040),(.0158,.0055,.0019),'ABS',.00015)
 # The photographic slivers are rear spring steel, not an added silver release handle.
 for s in [-1,1]:
  for z in [.019,.033,.047,.061,.073]:box(f'Filler{i:02}_recessed_contact_sliver',(x+s*.0079,F-.006,z),(.00045,.0014,.0028),'Nickel',.00006)
 box(f'Filler{i:02}_retention_edge',(x,F-.0145,.0256),(.0074,.0005,.00048),'Nickel',.00008)
 return root

def ink_ring(name,pos,r,width,axes=FRONT,mat='InkWhite'):
 # Closed solid ink thickness 50um; readable marks never share mirrored transforms.
 return ring(name,pos,r,r-width,.00005,mat,axes,48)

def stage2():
 for i in range(24):filler_geometry(i,(i-11.5)*.0174)
 collection('02_FRONT_FRAME_AND_CONTROLS')
 photo_material('Official_DELL_EMC_ink','dell-emc-official.png',0,.57);photo_material('Official_C6400_ink','c6400-official.png',0,.57)
 for s in [-1,1]:
  x=s*.23265;yp=F-.01518
  # Fine inset face leaves a visibly separate molded perimeter and a small bottom clip.
  extrude('Control_face_inset_'+str(s),rounded(.0131,.0510,.0009),(x,yp,.0599),FRONT,.00045,'ABS',.00007)
  box('Control_face_bottom_clip_'+str(s),(x,yp-.00012,.0348),(.0029,.00055,.0008),'ButtonBlack',.00008)
  if s<0:
   photo_patch('DELL_EMC_official_badge','Official_DELL_EMC_ink',[(-.00445,-.003115),(.00445,-.003115),(.00445,.003115),(-.00445,.003115)],[(0,0),(1,0),(1,1),(0,1)],(x,yp-.00014,.0809),FRONT)
  else:
   photo_patch('C6400_official_badge','Official_C6400_ink',[(-.0049,-.00196),(.0049,-.00196),(.0049,.00196),(-.0049,.00196)],[(0,0),(1,0),(1,1),(0,1)],(x,yp-.00014,.0809),FRONT)
  for level in range(2):
   zp=.0749-level*.0203;zi=.0650-level*.0203;zn=.0696-level*.0203;num=(1 if s<0 else 3)+level
   cyl('Power_button_lens_'+str(num),(x,yp-.00022,zp),.00212,.00052,'ButtonBlack',FRONT,40,.00007)
   ink_ring('Power_outer_white_print_'+str(num),(x,yp-.0003,zp),.00253,.00030)
   # Power-off icon is gray-white, as in unpowered source photograph, not glowing green.
   pts=[(x+.00154*math.sin(math.radians(a)),yp-.00034,zp+.00154*math.cos(math.radians(a))) for a in range(43,318,7)]
   curve('Power_symbol_arc_'+str(num),pts,.000125,'InkGray')
   curve('Power_symbol_stem_'+str(num),[(x,yp-.00034,zp+.00052),(x,yp-.00034,zp+.0019)],.000125,'InkGray')
   cyl('ID_button_lens_'+str(num),(x,yp-.00022,zi),.00192,.00048,'ButtonBlack',FRONT,40,.00006)
   ink_ring('ID_button_print_'+str(num),(x,yp-.00031,zi),.00243,.0003)
   cyl('ID_inner_white_disc_'+str(num),(x,yp-.00033,zi),.00155,.00005,'InkGray',FRONT,40,0)
   ob=text('ID_information_symbol_'+str(num),'i',(x,yp-.0004,zi),.0030,'InkBlack',FRONT);ob.data.shear=.23
   text('Front_node_number_'+str(num),str(num),(x+(.00215 if s<0 else -.00215),yp-.00034,zn),.00335,'InkWhite',FRONT)
   a=-.0026 if s<0 else .0026;sg=1 if s<0 else -1
   poly=[(a-sg*.0007,-.001),(a+sg*.0009,0),(a-sg*.0007,.001)]
   if s>0:poly.reverse()
   extrude('Front_mapping_arrow_'+str(num),poly,(x,yp-.00034,zn),FRONT,.00005,'InkWhite',0)
  # Captive screw, machined knurled barrel and real Phillips-shaped cavity.
  cyl('Captive_screw_metal_washer_'+str(s),(x,F-.0132,.0207),.0065,.0007,'Nickel',FRONT,64,.00015)
  knurl=[((.0058+.00017*math.cos(i*math.tau*24/144))*math.cos(i*math.tau/144),(.0058+.00017*math.cos(i*math.tau*24/144))*math.sin(i*math.tau/144)) for i in range(144)]
  extrude('Captive_screw_knurled_grip_'+str(s),knurl,(x,F-.0228,.0207),FRONT,.0085,'ABS',.00015)
  screw('Captive_screw_Phillips_'+str(s),(x,F-.0240,.0207),.0051,FRONT,'ButtonBlack',.05)
  ring('Captive_screw_front_bead_'+str(s),(x,F-.0239,.0207),.00565,.00512,.00045,'ButtonBlack',FRONT,64)
 # Actual blue EST pull tag behind right handle and bottom rail markings.
 box('EST_front_tag_blue_edge',(.2225,F-.0154,.025),(.0013,.008,.009),'BlueLatch',.00015)
 collection('07_PRINTED_MARKS')
 for i in range(24):
  x=(i-11.5)*.0174
  text(f'Bay_index_{i:02}',f'{i//6+1}-{i%6}',(x+.0011,F-.0176,.0029),.00166,'InkWhite',FRONT)
  extrude('Bay_mapping_triangle_'+str(i),[(-.0006,.0007),(.0006,.0007),(0,-.0008)],(x-.0035,F-.01755,.0030),FRONT,.00005,'InkWhite',0)
 all_uv();viewport((.32,-1.4,.28),1.16,shading='MATERIAL');save('02-front-photo-matched-fillers.blend')
