"""Metre-native mesh construction from millimetre arguments; GUI MCP stages only."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'parameters.json').read_text())
def coll(name):
 c=bpy.data.collections.get(name)
 if not c:c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c)
 return c
def mat(name,color,metal=0,rough=.5):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True
 n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Metallic'].default_value=metal;n.inputs['Roughness'].default_value=rough;n.inputs['Alpha'].default_value=1;n.inputs['Transmission Weight'].default_value=0
 m.diffuse_color=(*color,1);m.blend_method='OPAQUE';m.use_backface_culling=True
 return m
def assign(o,m):
 if m:o.data.materials.append(bpy.data.materials.get(m) if isinstance(m,str) else m)
 o['surface_role']='solid';o['units']='m';return o
def mesh(name,verts,faces,collection,material=None,loc=(0,0,0),solid=True):
 me=bpy.data.meshes.new(name);me.from_pydata([[v/1000 for v in co] for co in verts],[],faces);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 if solid and bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 bm.to_mesh(me);bm.free();me.update()
 o=bpy.data.objects.new(name,me);coll(collection).objects.link(o);o.location=[v/1000 for v in loc];assign(o,material)
 if not solid:o['surface_role']='intentional_print_surface'
 return o
def box(name,size,loc,collection,material=None,bevel=0):
 x,y,z=[v/2 for v in size];vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
 o=mesh(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(2,3,7,6),(3,0,4,7),(1,2,6,5)],collection,material,loc)
 if bevel:bevel_obj(o,bevel)
 return o
def bevel_obj(o,width,segments=2):
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 mod=o.modifiers.new('Physical edge break','BEVEL');mod.width=width/1000;mod.segments=segments;mod.affect='EDGES'
 bpy.ops.object.modifier_apply(modifier=mod.name);o.select_set(False);return o
def empty(name,collection,kind=None):
 o=bpy.data.objects.new(name,None);coll(collection).objects.link(o);o.empty_display_size=.006
 if kind:o['component_type']=kind
 return o
def parent(objects,root):
 for o in objects:o.parent=root
 return root
def instance(src,name,loc,collection,parent_obj=None):
 o=bpy.data.objects.new(name,src.data);coll(collection).objects.link(o);o.location=[v/1000 for v in loc];o.rotation_euler=src.rotation_euler.copy()
 for k in src.keys():o[k]=src[k]
 if parent_obj:o.parent=parent_obj
 return o
def cut(o,cutter):
 if o.data.users>1:o.data=o.data.copy()
 bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('True through cut','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 return o
def axes(u,v,t,plane):
 return (u,v,t) if plane=='XY' else (u,t,v) if plane=='XZ' else (t,u,v)
def cyl(name,radius,depth,loc,collection,material=None,axis='Z',n=32):
 vs=[]
 for t in [-depth/2,depth/2]:
  for i in range(n):
   a=i*2*math.pi/n;u=radius*math.cos(a);v=radius*math.sin(a)
   vs.append((u,v,t) if axis=='Z' else (u,t,v) if axis=='Y' else (t,u,v))
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,collection,material,loc)
def rounded_rect(w,h,r,n=5):
 vs=[]
 for cx,cy,ang in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for i in range(n+1):
   a=math.radians(ang+90*i/n);vs.append((cx+r*math.cos(a),cy+r*math.sin(a)))
 return vs
def prism(name,outline,depth,loc,collection,material=None,plane='XZ'):
 n=len(outline);vs=[axes(u,v,t,plane) for t in [-depth/2,depth/2] for u,v in outline]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,collection,material,loc)
def frame(name,w,h,depth,wall,loc,collection,material,plane='XZ',radius=.3):
 a=rounded_rect(w,h,radius,4);b=rounded_rect(w-2*wall,h-2*wall,max(.05,radius-wall/2),4);n=len(a)
 vs=[axes(u,v,t,plane) for t in [-depth/2,depth/2] for loop in [a,b] for u,v in loop]
 fs=[]
 for i in range(n):
  j=(i+1)%n
  fs.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return mesh(name,vs,fs,collection,material,loc)
def perforated(name,nx,ny,dx,dy,r,depth,loc,collection,material,plane='XY',shape='circle',stagger=0):
 """Shared boundary cells, explicit top/bottom/bore/perimeter faces; no alpha holes."""
 angles=set(round(i*math.pi/6,12) for i in range(12));a=math.atan2(dy,dx)
 angles.update(round(v,12) for v in [a,math.pi-a,math.pi+a,2*math.pi-a]);angles=sorted(angles);n=len(angles)
 vs=[];fs=[]
 for row in range(ny):
  for col in range(nx):
   cx=(col-(nx-1)/2)*dx;cy=(row-(ny-1)/2)*dy;offset=stagger*(1 if row%2 else -1);outer=[];inner=[]
   for a in angles:
    co=math.cos(a);si=math.sin(a);s=min(dx/2/max(abs(co),1e-15),dy/2/max(abs(si),1e-15));outer.append((cx+s*co,cy+s*si))
    if shape=='hex':s=min(r*math.cos(math.pi/6)/max(math.cos(a-k*math.pi/3),1e-15) for k in range(6) if math.cos(a-k*math.pi/3)>1e-6)
    elif shape=='rect':s=min(r[0]/2/max(abs(co),1e-15),r[1]/2/max(abs(si),1e-15))
    else:s=r
    inner.append((cx+offset+s*co,cy+s*si))
   k=len(vs);vs.extend(axes(u,v,t,plane) for t in [-depth/2,depth/2] for loop in [outer,inner] for u,v in loop)
   for i in range(n):
    j=(i+1)%n;fs.extend([(k+i,k+j,k+n+j,k+n+i),(k+2*n+i,k+3*n+i,k+3*n+j,k+2*n+j),(k+n+i,k+n+j,k+3*n+j,k+3*n+i)])
    x1,y1=outer[i];x2,y2=outer[j];edge=(abs(x1+nx*dx/2)<1e-7 and abs(x2+nx*dx/2)<1e-7) or (abs(x1-nx*dx/2)<1e-7 and abs(x2-nx*dx/2)<1e-7) or (abs(y1+ny*dy/2)<1e-7 and abs(y2+ny*dy/2)<1e-7) or (abs(y1-ny*dy/2)<1e-7 and abs(y2-ny*dy/2)<1e-7)
    if edge:fs.append((k+i,k+2*n+i,k+2*n+j,k+j))
 o=mesh(name,vs,fs,collection,material,loc);o['true_holes']=nx*ny;o['sheet_thickness_mm']=depth;o['pattern_estimated']=True;return o
def screw(name,loc,collection,axis='Z',radius=1.7,depth=.55,material='Fastener steel'):
 o=cyl(name,radius,depth,loc,collection,material,axis,24)
 # Two real intersecting shallow recess cuts on the visible head.
 if axis=='Z':cuts=[((radius*1.3,.35,depth),(loc[0],loc[1],loc[2]+depth*.4)),((.35,radius*1.3,depth),(loc[0],loc[1],loc[2]+depth*.4))]
 elif axis=='Y':cuts=[((radius*1.3,depth,.35),(loc[0],loc[1]-depth*.4,loc[2])),((.35,depth,radius*1.3),(loc[0],loc[1]-depth*.4,loc[2]))]
 else:cuts=[((depth,radius*1.3,.35),(loc[0]+depth*.4,loc[1],loc[2])),((depth,.35,radius*1.3),(loc[0]+depth*.4,loc[1],loc[2]))]
 for sz,lc in cuts:cut(o,box('screw_recess_tool',sz,lc,collection))
 return o
def tube(name,points,radius,collection,material,n=10):
 # Continuous capped sweep; centreline supplied in mm.
 vs=[]
 for i,point in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
  tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0));u=tangent.cross(ref).normalized();v=tangent.cross(u).normalized()
  for k in range(n):vs.append(tuple(Vector(point)+radius*(math.cos(2*math.pi*k/n)*u+math.sin(2*math.pi*k/n)*v)))
 fs=[tuple(reversed(range(n))),tuple((len(points)-1)*n+k for k in range(n))]
 for i in range(len(points)-1):
  for k in range(n):j=(k+1)%n;fs.append((i*n+k,i*n+j,(i+1)*n+j,(i+1)*n+k))
 o=mesh(name,vs,fs,collection,material)
 for po in o.data.polygons:
  if len(po.vertices)==4:po.use_smooth=True
 return o
def text_obj(name,body,size,loc,collection,material='Printed black',face='FRONT',align='LEFT'):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size/1000;cu.align_x=align;cu.extrude=0;cu.resolution_u=3
 fp='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
 font=bpy.data.fonts.get('LiberationSans-Bold') or bpy.data.fonts.load(fp);cu.font=font
 o=bpy.data.objects.new(name,cu);coll(collection).objects.link(o);o.location=[v/1000 for v in loc]
 if face=='FRONT':o.rotation_euler=(math.pi/2,0,0)
 elif face=='REAR':o.rotation_euler=(math.pi/2,0,math.pi)
 elif face=='TOP':pass
 o.data.materials.append(bpy.data.materials.get(material));o['surface_role']='intentional_print_surface';o['text_content']=body;o['text_face']=face;o['print_gap_mm']=.025
 return o
def stage_save(name):
 bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model'/name),compress=True)
 (ROOT/'qa'/(name.replace('.blend','')+'-done.json')).write_text(json.dumps({'file':str(Path('model')/name),'objects':len(bpy.context.scene.objects),'mesh_objects':sum(o.type=='MESH' for o in bpy.context.scene.objects)},indent=2))
 print('STAGE_SAVED',name,len(bpy.context.scene.objects))
