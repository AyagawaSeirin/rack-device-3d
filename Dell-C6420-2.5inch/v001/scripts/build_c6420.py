"""Dell PowerEdge C6420 four-node / 24SFF exterior. Execute through Blender MCP.
Units: m. Sources and confidence: ../DIMENSIONS.md and ../CONFIGURATION.md.
Run staged functions via MCP; build_all() reproduces the same scene.
"""
import bpy, bmesh, math, json
from mathutils import Vector, Matrix
from pathlib import Path
P=Path('/root/Blender/DELL-C6420/v001')
CFG=json.loads((P/'model/parameters.json').read_text())
W,H,D=[CFG[k]/1000 for k in ['body_width_mm','body_height_mm','body_depth_from_mount_mm']]
F,R=-D/2,D/2
FRONT=((1,0,0),(0,0,1),(0,-1,0))
REAR=((-1,0,0),(0,0,1),(0,1,0))
TOP=((1,0,0),(0,1,0),(0,0,1))
BOTTOM=((-1,0,0),(0,1,0),(0,0,-1))
MAT={}; COL=None; PART=None

def collection(name):
    global COL,PART
    COL=bpy.data.collections.get(name)
    if COL is None:
        COL=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(COL)
    PART=None
    return COL

def group(name,kind):
    global PART
    ob=bpy.data.objects.new(name,None);COL.objects.link(ob)
    ob.empty_display_type='PLAIN_AXES';ob.empty_display_size=.01
    ob['component_type']=kind;PART=ob
    return ob

def material(name,color,metal=0,rough=.45):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
    bs.inputs['Alpha'].default_value=1;bs.inputs['Transmission Weight'].default_value=0
    m.blend_method='OPAQUE';m.use_backface_culling=True;MAT[name]=m
    return m

def mesh(name,verts,faces,mat):
    me=bpy.data.meshes.new(name+'_mesh');me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);COL.objects.link(ob)
    if PART:ob.parent=PART
    if mat:me.materials.append(MAT[mat] if isinstance(mat,str) else mat)
    ob['source_basis']='Official dimensions; photo-estimated exterior detail'
    return ob

def bevel(ob,width=.0004,segments=2):
    if width:
        mod=ob.modifiers.new('Manufactured edge radius','BEVEL');mod.width=width;mod.segments=segments;mod.limit_method='ANGLE'
        mod.profile=.5
        norm=ob.modifiers.new('Corner normals','WEIGHTED_NORMAL');norm.keep_sharp=True;norm.weight=50
    return ob

def box(name,loc,size,mat='Steel',edge=.0003):
    x,y,z=[v/2 for v in size]
    vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
    fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    ob=mesh(name,vs,fs,mat);ob.location=loc
    bevel(ob,min(edge,min(size)*.23) if edge else 0)
    return ob

def basis(ob,pos,axes):
    u,v,n=[Vector(a) for a in axes]
    ob.matrix_world=Matrix(((u.x,v.x,n.x,pos[0]),(u.y,v.y,n.y,pos[1]),(u.z,v.z,n.z,pos[2]),(0,0,0,1)))
    return ob

def cylinder(name,loc,radius,depth,mat='Steel',axis=(0,0,1),N=24,edge=.00015):
    vs=[]
    for z in [-depth/2,depth/2]:
        vs.extend([(radius*math.cos(i*2*math.pi/N),radius*math.sin(i*2*math.pi/N),z) for i in range(N)])
    fs=[tuple(range(N-1,-1,-1)),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
    ob=mesh(name,vs,fs,mat);ob.location=loc
    ob.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();bevel(ob,edge,2)
    for p in ob.data.polygons:
        if len(p.vertices)==4:p.use_smooth=True
    return ob

def tube_curve(name,points,r,mat='Steel',closed=False):
    cu=bpy.data.curves.new(name+'_curve','CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=r;cu.bevel_resolution=2;cu.use_fill_caps=True
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points):p.co=(*co,1)
    sp.use_cyclic_u=closed
    ob=bpy.data.objects.new(name,cu);COL.objects.link(ob);cu.materials.append(MAT[mat])
    if PART:ob.parent=PART
    return ob

def annulus(name,loc,outer,inner,mat='Steel',axes=FRONT,depth=.0005,N=32):
    vs=[(rad*math.cos(i*2*math.pi/N),rad*math.sin(i*2*math.pi/N),z) for z in [0,-depth] for rad in [outer,inner] for i in range(N)]
    fs=[]
    for i in range(N):
        j=(i+1)%N
        fs.extend([(i,j,N+j,N+i),(2*N+i,3*N+i,3*N+j,2*N+j),(i,2*N+i,2*N+j,j),(N+i,N+j,3*N+j,3*N+i)])
    return basis(mesh(name,vs,fs,mat),loc,axes)

def panel(name,width,height,holes,pos,mat='Steel',axes=REAR,thickness=.001):
    """Connected planar grid with actual apertures; solidify creates hole walls.
    holes are (u_center,v_center,width,height). No alpha-cutout material.
    """
    xs=sorted(set(round(x,7) for x in [-width/2,width/2]+[a for u,v,w,h in holes for a in (max(-width/2,u-w/2),min(width/2,u+w/2))]))
    ys=sorted(set(round(y,7) for y in [-height/2,height/2]+[a for u,v,w,h in holes for a in (max(-height/2,v-h/2),min(height/2,v+h/2))]))
    vs=[];fs=[];indices={}
    def vid(i,j):
        key=(i,j)
        if key not in indices:indices[key]=len(vs);vs.append((xs[i],ys[j],0))
        return indices[key]
    for i in range(len(xs)-1):
        for j in range(len(ys)-1):
            cx=(xs[i]+xs[i+1])/2;cy=(ys[j]+ys[j+1])/2
            if any(abs(cx-u)<w/2-1e-9 and abs(cy-v)<h/2-1e-9 for u,v,w,h in holes):continue
            fs.append((vid(i,j),vid(i+1,j),vid(i+1,j+1),vid(i,j+1)))
    ob=basis(mesh(name,vs,fs,mat),pos,axes)
    so=ob.modifiers.new('Physical panel thickness','SOLIDIFY');so.thickness=thickness;so.offset=-1;so.use_even_offset=True
    bevel(ob,min(thickness*.2,.00018),2)
    ob['actual_through_holes']=len(holes)
    return ob

def text_obj(name,body,loc,size,mat='MarkWhite',axes=FRONT,align='CENTER'):
    cu=bpy.data.curves.new(name+'_text','FONT');cu.body=body;cu.size=size;cu.align_x=align;cu.align_y='CENTER';cu.extrude=.000035;cu.resolution_u=4
    ob=bpy.data.objects.new(name,cu);COL.objects.link(ob);cu.materials.append(MAT[mat])
    if PART:ob.parent=PART
    basis(ob,loc,axes);ob['readable_text']=body;ob['mirror_policy']='Independent positive-determinant transform'
    return ob

def decal(name,path,loc,size,axes=FRONT):
    m=bpy.data.materials.new(name+'_OpaqueInk');m.use_nodes=True;m.blend_method='OPAQUE';m.use_backface_culling=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.58;bs.inputs['Alpha'].default_value=1;bs.inputs['Transmission Weight'].default_value=0
    tx=m.node_tree.nodes.new('ShaderNodeTexImage');tx.image=bpy.data.images.load(str(P/'textures'/path),check_existing=True);tx.image.pack()
    m.node_tree.links.new(tx.outputs['Color'],bs.inputs['Base Color'])
    w,h=size;ob=mesh(name,[(-w/2,-h/2,0),(w/2,-h/2,0),(w/2,h/2,0),(-w/2,h/2,0)],[(0,1,2,3)],m)
    uv=ob.data.uv_layers.new(name='Verified_non_mirrored_UV')
    for i,co in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[i].uv=co
    basis(ob,loc,axes);ob['intentional_open_surface']='Opaque printed label; front-facing plane offset from substrate';ob['source_asset']=path
    return ob

def save(name):
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=str(P/'model'/name))
    print('Saved',name,'objects',len(bpy.context.scene.objects))

def viewport():
    for screen in bpy.data.screens:
        for a in screen.areas:
            if a.type=='VIEW_3D':
                s=a.spaces.active;s.clip_start=.001;s.clip_end=20;s.overlay.show_floor=False;s.overlay.show_axis_x=False;s.overlay.show_axis_y=False
                s.shading.type='SOLID';s.shading.color_type='MATERIAL';s.shading.light='STUDIO';s.shading.studiolight_rotate_z=.4
                s.region_3d.view_distance=1.3;s.region_3d.view_location=Vector((0,0,.04))
                s.region_3d.view_rotation=Vector((1,-1.4,.8)).to_track_quat('Z','Y');s.region_3d.view_perspective='PERSP'

def stage1():
    global MAT
    for ob in list(bpy.data.objects):bpy.data.objects.remove(ob,do_unlink=True)
    for co in list(bpy.data.collections):bpy.data.collections.remove(co)
    scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='MILLIMETERS'
    scene['project']='DELL PowerEdge C6420 / four C6420 nodes / 24x2.5-inch';scene['axes']='front -Y; rear +Y; right +X; up +Z';scene['base_assumed']=True
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=12
    MAT={}
    for args in [('Steel',(.52,.55,.57),.8,.38),('SteelDark',(.19,.215,.23),.7,.46),('Chrome',(.7,.73,.75),.92,.24),('Plastic',(.018,.021,.024),0,.5),('Rubber',(.009,.011,.013),0,.72),('Blue',(.19,.43,.68),0,.4),('Orange',(.92,.24,.025),0,.42),('USBBlue',(.025,.12,.4),0,.4),('Gold',(.55,.37,.12),.72,.3),('Green',(.06,.47,.22),.1,.4),('MarkWhite',(.83,.86,.86),0,.55),('MarkBlack',(.014,.018,.02),0,.6)]:material(*args)
    collection('01_CHASSIS')
    ob=box('Chassis_bottom_INFERRED',(0,0,.0005),(W,D,.001));ob['assumption']='Generic continuous base; underside photos unavailable'
    for s in [-1,1]:box('Side_wall_'+('LEFT' if s<0 else 'RIGHT'),(s*(W/2-.0005),0,H/2),(.001,D,H-.002))
    box('Front_top_cover',(0,-.31,H-.0005),(W,.1432,.001))
    box('Main_top_cover',(0,-.0076,H-.0005),(W,.4596,.001))
    box('Rear_top_cover',(0,.3029,H-.0005),(W,.1574,.001))
    for s in [-1,1]:
        box('Side_inner_upper_fold', (s*.2195,0,.0839),(.007,D,.0012))
        box('Side_inner_lower_fold', (s*.2195,0,.0022),(.007,D,.0012))
    # Two column sled shelves and central PSU rails, hidden behind exterior apertures.
    for x in [-.1328,.1328]:box('Node_shelf',(x,.102,.0434),(.1746,.557,.0012),'SteelDark')
    for x in [-.0448,.0448]:box('PSU_channel_wall',(x,.102,.0434),(.0012,.557,.082),'SteelDark')
    collection('02_FRONT_ASSEMBLY')
    box('Front_lower_fold',(0,F-.010,.0007),(W,.020,.0014))
    box('Front_upper_fold',(0,F-.010,H-.0007),(W,.020,.0014))
    for s in [-1,1]:
        box('Rack_ear_'+str(s),(s*.23265,F-.004,.0434),(.0173,.008,.08),'Steel',.0006)
        box('Control_housing_'+str(s),(s*.23265,F-.010,.0545),(.0148,.010,.061),'Plastic',.0007)
        box('Captive_screw_base_'+str(s),(s*.23265,F-.010,.013),(.0148,.010,.016),'Plastic',.0007)
        # Rack handle reaches the official front outer plane F-26.8 mm.
        pts=[]
        for j in range(17):
            t=j/16;z=.016+.059*t;y=F-.004-.0208*math.sin(math.pi*t)
            pts.append((s*.2187,y,z))
        tube_curve('Steel_rack_handle_'+str(s),pts,.002,'Chrome')
    box('Drive_cage_rear_shade',(0,-.264,.042),(W-.008,.002,.076),'Rubber')
    for k,x in enumerate([-.1044,0,.1044]):box('Drive_bank_separator_'+str(k),(x,F-.014,.043),( .001,.017,.081),'SteelDark',.00015)
    # Dimension proxies are visible physical node trays, retained in later stages.
    for num,x,z0 in [(1,-.1328,.0443),(2,-.1328,.002),(3,.1328,.0443),(4,.1328,.002)]:
        collection('04_NODE_'+str(num));root=group('C6420_Node_'+str(num),'C6420 node');root['official_dimensions_mm']=[174.4,40.5,574.5]
        front=R+.014325-.5745
        box('Node'+str(num)+'_floor',(x,(front+R)/2,z0+.0005),(.1744,R-front,.001),'SteelDark')
        for s in [-1,1]:box('Node'+str(num)+'_side_rail',(x+s*.0867,(front+R)/2,z0+.02025),(.001,R-front,.0405),'SteelDark')
        box('Node'+str(num)+'_internal_air_baffle',(x,R-.018,z0+.02025),(.172,.002,.037),'Rubber')
    collection('05_POWER_SUPPLIES')
    for i,z in enumerate([.02225,.06455],1):box('PSU'+str(i)+'_body',(0,.192,z),(.087,.374,.0405),'SteelDark')
    viewport();save('01-body.blend')

# Detailed stage functions follow below. Each is executed once through MCP and checkpointed.

def honeycomb(name,pos):
    radius=.00215;inner=.00169;verts=[];faces=[]
    for column in [-1,0,1]:
        cx=column*1.5*radius
        for row in range(-5,6):
            cy=row*math.sqrt(3)*radius+(math.sqrt(3)*radius/2 if column%2 else 0)
            start=len(verts)
            for r in [radius,inner]:
                verts.extend([(cx+r*math.cos(k*math.pi/3),cy+r*math.sin(k*math.pi/3),0) for k in range(6)])
            for k in range(6):faces.append((start+k,start+(k+1)%6,start+6+(k+1)%6,start+6+k))
    ob=mesh(name,verts,faces,'Plastic')
    bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    basis(ob,pos,FRONT);so=ob.modifiers.new('Molded honeycomb thickness','SOLIDIFY');so.thickness=.0018;so.offset=-1
    ob['actual_through_holes']=33
    return ob

def screw(name,loc,axis=(0,0,1),radius=.0019):
    ob=cylinder(name,loc,radius,.0007,'Steel',axis,16,.00012)
    # Recessed-looking cross slots are raised only 0.03mm above head, isolated from the shell.
    n=Vector(axis);u=n.orthogonal().normalized();v=n.cross(u).normalized()
    for a in [u,v]:
        c=Vector(loc)+n*.00037
        part=box(name+'_cross',c,(radius*1.15,.00038,.00006),'SteelDark',0)
        basis(part,c,(tuple(a),tuple(n.cross(a)),tuple(n)))
    return ob

def stage2():
    global PART
    for i in range(24):
        collection('03_DRIVE_CARRIERS');root=group('Drive_'+str(i).zfill(2),'2.5-inch hot-swap carrier')
        root['bay_index']=i;root['mapped_node']=i//6+1
        x=(i-11.5)*.0174;cy=F-.017;cz=.0434
        # A full-depth physical carrier and disk shell behind the air intake.
        box('Drive%02d_drive_enclosure'%i,(x,-.326,.0434),(.014,.102,.0698),'SteelDark',.0005)
        for s in [-1,1]:box('Drive%02d_tray_side'%i,(x+s*.00735,-.331,.0434),(.0007,.116,.071),'Steel',.00015)
        panel('Drive%02d_molded_front'%i,.016,.075,[(0,-.0044,.0108,.047)],(x,cy,cz),'Plastic',FRONT,.003)
        honeycomb('Drive%02d_honeycomb'%i,(x,cy+.001,.038))
        for s in [-1,1]:box('Drive%02d_silver_lever_rail'%i,(x+s*.00665,cy-.0009,.039),(.00115,.0018,.056),'Chrome',.00025)
        box('Drive%02d_release_block'%i,(x,cy-.0004,.0708),(.0125,.002,.0116),'Plastic',.0006)
        cylinder('Drive%02d_release_button'%i,(x,cy-.00155,.071),.00325,.0013,'SteelDark',(0,-1,0),24,.0002)
        annulus('Drive%02d_orange_release_ring'%i,(x,cy-.00223,.071),.0031,.00272,'Orange',FRONT,.00015,24)
        box('Drive%02d_lower_silver_tab'%i,(x,cy-.00125,.0125),(.0108,.0025,.0107),'Chrome',.0007)
        for z in [.026,.041,.056]:box('Drive%02d_grille_crossbrace'%i,(x,cy+.0006,z),(.0102,.0012,.0007),'Plastic',.0001)
        for j,z in enumerate([.0777,.0802]):
            box('Drive%02d_indicator_lens_%d'%(i,j),(x+.005,cy-.0011,z),(.00125,.0005,.0011),'Green' if j==0 else 'Rubber',.00015)
        text_obj('Drive%02d_bay_number'%i,f'{i//6+1}-{i%6}',(x,F-.0182,.0034),.00175,'MarkWhite')
    collection('02_FRONT_ASSEMBLY')
    for s in [-1,1]:
        holes=[(0,-.034+j*.005,.0025,.0034) for j in range(14)]
        panel('Front_side_perforated_flange_'+str(s),.0095,.082,holes,(s*.2158,F-.018,.0434),'Steel',FRONT,.001)
        x=s*.23265
        cylinder('Rack_captive_thumb_screw_'+str(s),(x,F-.0185,.013),.0064,.005,'Plastic',(0,-1,0),32,.0006)
        for size in [(.0064,.0003,.0014),(.0014,.0003,.0064)]:box('Captive_cross_recess',(x,F-.0211,.013),size,'Rubber',.00015)
    # Right ear information tag, visibly separate from chassis and never mirrored.
    box('Front_EST_pull_tab',(.223,F-.012,.020),(.0018,.011,.014),'Blue',.0002)
    viewport();save('02-front-24SFF.blend')

def rear_socket(name,x,z,width,height,depth=.007,tongue=None):
    # Real five-sided port cavity. Front is +Y, opaque back at -depth.
    y=R+.00065;t=.00055
    box(name+'_recess_back',(x,y-depth,z),(width,.0007,height),'Rubber',.0001)
    for s in [-1,1]:
        box(name+'_sidewall',(x+s*(width/2+t/2),y-depth/2,z),(t,depth,height+2*t),'Chrome',.00012)
        box(name+'_horizontalwall',(x,y-depth/2,z+s*(height/2+t/2)),(width,depth,t),'Chrome',.00012)
    if tongue:
        box(name+'_tongue',(x,y-.002,z+.0002),(width*.85,.003,.001),'USBBlue' if tongue=='USB' else 'Plastic',.00015)
    return y

def node_detail(num,x,z0):
    global PART
    collection('04_NODE_'+str(num));PART=bpy.data.objects['C6420_Node_'+str(num)]
    zc=z0+.02025
    def uv(u,z):return (-.0872+u,z-.02025)
    def wx(u):return x+.0872-u
    major=[(12,.009,.0148,.0056),(12,.0173,.0148,.0056),(52,.0103,.0156,.009),(69,.0103,.0156,.009),(89,.006,.008,.0036),(117,.008,.0072,.005),(137,.009,.015,.013),(129,.029,.074,.018)]
    # u is in mm for readability; all geometric lengths are meters.
    holes=[(-.0872+u/1000,z-.02025,w,h) for u,z,w,h in major]
    for col in range(15):
        for zz in [.024,.029,.034,.038]:
            holes.append((-.0872+.004+col*.0049,zz-.02025,.0033,.0029))
    for u in [.028,.034,.039,.097,.103,.109,.154,.161,.167]:
        for zz in [.006,.012,.017]:
            if not (u==.154 and zz==.012):holes.append((-.0872+u,zz-.02025,.0033,.0029))
    panel('Node%d_perforated_rear'%num,.1744,.0405,holes,(x,R,zc),'Steel',REAR,.001)
    # Perimeter steel return lips.
    for z in [z0+.0007,z0+.0398]:box('Node%d_rear_horizontal_lip'%num,(x,R-.002,z),(.173,.004,.0008),'Chrome',.0001)
    for uu in [.0006,.1738]:box('Node%d_rear_vertical_lip'%num,(wx(uu),R-.002,zc),(.0008,.004,.039),'Chrome',.0001)
    for j,zz in enumerate([.009,.0173]):
        xx=wx(.012);y=rear_socket('Node%d_USB3_%d'%(num,j),xx,z0+zz,.0134,.0047,tongue='USB')
        for k in range(4):box('Node%d_USB_contact'%num,(xx+(k-1.5)*.0022,y-.0016,z0+zz-.0004),(.0006,.0018,.00018),'Gold',0)
    for j,uu in enumerate([.052,.069]):
        xx=wx(uu);y=rear_socket('Node%d_SFP_%d'%(num,j),xx,z0+.0103,.0145,.008,.011)
        box('Node%d_SFP_retention'%num,(xx,y+.0001,z0+.0051),(.010,.0012,.0007),'Chrome',.00012)
        for k in range(4):box('Node%d_SFP_inner_contact'%num,(xx+(k-1.5)*.0018,y-.006,z0+.008),(.00035,.002,.0004),'Gold',0)
    rear_socket('Node%d_micro_USB'%num,wx(.089),z0+.006,.0073,.0028,.005,'black')
    rear_socket('Node%d_mini_DisplayPort'%num,wx(.117),z0+.008,.0064,.0043,.005,'black')
    xx=wx(.137);y=rear_socket('Node%d_iDRAC_RJ45'%num,xx,z0+.009,.0138,.0118,.009)
    for k in range(8):box('Node%d_RJ45_contact'%num,(xx+(k-3.5)*.0011,y-.0038,z0+.0048),(.00026,.004,.0008),'Gold',0)
    for ss in [-1,1]:box('Node%d_RJ45_indicator'%num,(xx+ss*.0066,y+.00005,z0+.014),(.0012,.00055,.0013),'Green' if ss<0 else 'MarkWhite',.00015)
    # Long sled release lever forms a genuinely recessed grip.
    yy=rear_socket('Node%d_long_grip'%num,wx(.129),z0+.029,.072,.016,.009)
    box('Node%d_grip_lower_rail'%num,(wx(.129),R+.002,z0+.019),(.076,.005,.0017),'Chrome',.00035)
    box('Node%d_grip_upper_rail'%num,(wx(.129),R+.002,z0+.039),(.076,.005,.0015),'Chrome',.0003)
    bx=wx(.080)
    box('Node%d_blue_release_paddle'%num,(bx,R+.0085,z0+.0275),(.015,.011,.025),'Blue',.0022)
    box('Node%d_paddle_inner_grip'%num,(bx-.003,R+.01415,z0+.0275),(.0043,.00035,.018),'Rubber',.0008)
    cylinder('Node%d_handle_hinge'%num,(wx(.0865),R+.0025,z0+.0365),.002,.0016,'Steel',(0,1,0),20)
    cylinder('Node%d_rear_power'%num,(wx(.155),R+.001,z0+.01),.00265,.0018,'Gold',(0,1,0),24,.00025)
    cylinder('Node%d_outer_release_lock'%num,(wx(.173),R-.004,z0+.008),.0032,.0018,'Blue',(-1,0,0),20,.0002)
    text_obj('Node%d_iDRAC_mark'%num,'iDRAC',(wx(.137),R+.00125,z0+.019),.0015,'MarkBlack',REAR)
    text_obj('Node%d_DP_mark'%num,'DP',(wx(.117),R+.00125,z0+.014),.0016,'MarkBlack',REAR)
    text_obj('Node%d_EST_mark'%num,'EST',(wx(.060),R+.00125,z0+.0018),.0015,'MarkWhite',REAR)
    # Tiny service-tag pull strip, model does not fabricate a serial number.
    box('Node%d_EST_strip'%num,(wx(.060),R+.0008,z0+.0018),(.022,.00045,.0028),'Blue',.0001)

def psu_detail(i,zc):
    global PART
    collection('05_POWER_SUPPLIES');root=group('Power_Supply_'+str(i),'2400W PSU');root['photo_option']='EPP 2400W 94% efficiency'
    # Rear observer left inlet -> physical +X. Right fan -> physical -X.
    panel('PSU%d_front_frame'%i,.087,.0405,[(-.023,0,.029,.033),(.022,0,.037,.037)],(0,R,zc),'Steel',REAR,.0012)
    rear_socket('PSU%d_AC_inlet'%i,.023,zc,.027,.031,.010)
    for dx,dz in [(0,.008),(-.006,-.005),(.006,-.005)]:box('PSU%d_AC_pin'%i,(.023+dx,R-.0035,zc+dz),(.0019,.005,.004),'Chrome',.00015)
    box('PSU%d_inlet_left_border'%i,(.039,R+.001,zc),(.0025,.006,.035),'Plastic',.0005)
    box('PSU%d_orange_release'%i,(.0422,R+.004,zc),(.0035,.007,.018),'Orange',.001)
    cx=-.022
    # Opaque fan tunnel, dark set-back blade geometry, real open guard.
    for s in [-1,1]:
        box('PSU%d_fan_tunnel'%i,(cx+s*.019,R-.007,zc),(.001,.014,.038),'Rubber',.0002)
        box('PSU%d_fan_tunnel'%i,(cx,R-.007,zc+s*.019),(.038,.014,.001),'Rubber',.0002)
    box('PSU%d_fan_recess_back'%i,(cx,R-.015,zc),(.036,.001,.036),'Rubber',.0001)
    cylinder('PSU%d_fan_hub'%i,(cx,R-.005,zc),.007,.005,'Plastic',(0,1,0),32,.0003)
    for k in range(7):
        a=k*math.tau/7;vs=[]
        for yy in [R-.007,R-.008]:
            for rr,aa in [(.006,a),(.017,a+.20),(.0165,a+.67),(.007,a+.6)]:vs.append((cx+rr*math.cos(aa),yy,zc+rr*math.sin(aa)))
        mesh('PSU%d_fan_blade_%d'%(i,k),vs,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Plastic')
    for sx in [-1,1]:
        for sz in [-1,1]:
            endpoint=(cx+sx*.0175,R+.0012,zc+sz*.0175)
            tube_curve('PSU%d_guard_spoke'%i,[(cx,R+.0012,zc),endpoint],.00062,'Chrome')
            screw('PSU%d_guard_fastener'%i,(endpoint[0],R+.0017,endpoint[2]),(0,1,0),.0021)
    cylinder('PSU%d_label_disc'%i,(cx,R+.0025,zc),.0093,.0008,'MarkWhite',(0,1,0),48,.0001)
    # Exact lettering as seen in chosen original photograph, independent nonmirrored geometry.
    text_obj('PSU%d_EPP'%i,'EPP',(cx,R+.00305,zc+.0046),.0033,'Green',REAR)
    text_obj('PSU%d_2400W'%i,'2400W',(cx,R+.00305,zc),.0037,'MarkBlack',REAR)
    text_obj('PSU%d_efficiency'%i,'94% efficiency',(cx,R+.00305,zc-.0036),.00155,'MarkBlack',REAR)
    # Fabric extraction loop reaches documented max rear envelope R+34.1mm.
    pts=[(.011,R+.002,zc),(.011,R+.025,zc),(.009,R+.0323,zc),(.001,R+.0323,zc),(-.001,R+.025,zc),(-.001,R+.004,zc)]
    tube_curve('PSU%d_fabric_extraction_loop'%i,pts,.0018,'Rubber')

def stage3():
    for num,x,z0 in [(1,-.1328,.0443),(2,-.1328,.002),(3,.1328,.0443),(4,.1328,.002)]:node_detail(num,x,z0)
    for i,z in enumerate([.02225,.06455],1):psu_detail(i,z)
    viewport();save('03-four-nodes-and-PSUs.blend')

def stage4():
    global PART
    # Replace solid PSU proxy volumes: they would incorrectly block the fan and AC recesses.
    collection('05_POWER_SUPPLIES')
    for i,zc in enumerate([.02225,.06455],1):
        old=bpy.data.objects.get('PSU%d_body'%i)
        if old:bpy.data.objects.remove(old,do_unlink=True)
        PART=bpy.data.objects['Power_Supply_'+str(i)]
        for s in [-1,1]:
            box('PSU%d_shell_side'%i,(s*.043,.192,zc),(.001,.374,.0405),'SteelDark')
            box('PSU%d_shell_horizontal'%i,(0,.192,zc+s*.01975),(.085,.374,.001),'SteelDark')
        box('PSU%d_shell_inner_end'%i,(0,.0055,zc),(.085,.001,.0385),'SteelDark')
    # Internal seam overlap prevents accidental clear sightlines through cover seams.
    collection('01_CHASSIS')
    main=bpy.data.objects['Main_top_cover'];main.location.y=-.007;main.dimensions.y=.4616
    for y in [-.2381,.224]:box('Top_seam_internal_overlap',(0,y,H-.0018),(.44,.01,.001),'SteelDark',.0001)
    # Inferred stamped bottom is a thick plate with four genuinely recessed grooves.
    bpy.data.objects.remove(bpy.data.objects['Chassis_bottom_INFERRED'],do_unlink=True)
    bottom=panel('Chassis_bottom_INFERRED',W,D,[(x,0,.0044,.635) for x in [-.135,-.045,.045,.135]],(0,0,0),'Steel',BOTTOM,.001)
    bottom['assumption']='AI inferred generic recessed-rib base; no original underside photo'
    for x in [-.135,-.045,.045,.135]:
        ob=box('INFERRED_recessed_bottom_rib',(x,0,.00075),(.0044,.635,.0005),'Steel',.0001);ob['assumption']='Generic stamped groove'
    collection('06_FASTENERS_AND_STAMPING')
    for s in [-1,1]:
        for j,y in enumerate([-.335,-.267,-.19,-.10,0,.095,.184,.27,.34]):
            for z in [.018,.061]:screw('Side_fastener_%s_%d_%s'%(s,j,z),(s*.2242,y,z),(s,0,0),.0017 if j%3 else .0024)
        # Upper rail attachment strip, raised at side only, below nominal height.
        box('Upper_side_rail_strip_'+str(s),(s*.2242,0,.080),(.0008,.747,.009),'Steel',.00016)
    # Shallow authentic-looking embossed channels on top; valleys assembled from thin forms.
    for y in [-.358,-.249,.272,.351]:
        box('Top_stamped_channel',(0,y,H-.00035),(.397,.003,.0008),'Steel',.00018)
    for x in [-.17,-.057,.057,.17]:
        for y in [-.348,-.274]:
            cylinder('Top_flush_fastener',(x,y,H+.00003),.0019,.00013,'SteelDark',(0,0,1),20,.00002)
    for x in [-.075,.075]:
        box('Top_cover_release_tab',(x,-.236,H-.0002),(.014,.006,.0009),'SteelDark',.0002)
    # Printed official service instruction diagrams occupy the evidenced central label area.
    collection('07_LABELS_AND_CONTROLS')
    decal('DELL_EMC_official_brand','dell-emc-official.png',(-.23265,F-.01535,.0792),(.0104,.00726),FRONT)
    decal('C6400_official_enclosure_badge','c6400-official.png',(.23265,F-.01535,.0803),(.0112,.00448),FRONT)
    for s in [-1,1]:
        x=s*.23265
        for level,(zp,zi,zn) in enumerate([(.0689,.0575,.0630),(.0448,.0329,.0386)]):
            y=F-.01545
            cylinder('Ear_control_button',(x,y+.00025,zp),.00225,.0006,'Rubber',(0,-1,0),24,.0001)
            annulus('Power_button_outer_ink',(x,y-.0001,zp),.00235,.00203,'MarkWhite',FRONT,.00008,32)
            pts=[(x+.00145*math.sin(math.radians(a)),y-.0002,zp+.00145*math.cos(math.radians(a))) for a in range(45,316,15)]
            tube_curve('Power_symbol_arc',pts,.00018,'Green')
            tube_curve('Power_symbol_stroke',[(x,y-.00022,zp+.00045),(x,y-.00022,zp+.0019)],.00018,'Green')
            annulus('ID_button_outer_ink',(x,y-.0001,zi),.00215,.00185,'MarkWhite',FRONT,.00008,32)
            text_obj('ID_i_symbol','i',(x,y-.0002,zi),.0029,'MarkWhite',FRONT)
            number=(1 if s<0 else 3)+level
            text_obj('Sled_control_number_'+str(number),str(number),(x+(.0022 if s<0 else -.0022),y-.00015,zn),.00325,'MarkWhite',FRONT)
            # Correct arrows are actual triangles with independent direction, not mirrored text UV.
            ax=x+(-.0029 if s<0 else .0029);sg=1 if s<0 else -1
            mesh('Control_mapping_arrow',[(ax-sg*.0006,y-.00015,zn-.00085),(ax+sg*.0008,y-.00015,zn),(ax-sg*.0006,y-.00015,zn+.00085)],[(0,1,2)] if s<0 else [(2,1,0)],'MarkWhite')['intentional_open_surface']='Printed arrow'
    for x,name,w in [(-.135,'sled-service-label.png',.108),(0,'enclosure-service-label.png',.112),(.137,'drive-cage-service-label.png',.122)]:
        decal('Official_top_'+name,name,(x,.025,H+.00016),(w,.165),TOP)
    material('WarningYellow',(.74,.54,.045),0,.55)
    box('Observed_warning_label_substrate',(.126,.300,H+.00004),(.107,.041,.00016),'WarningYellow',.00002)
    text_obj('Observed_CAUTION_word','CAUTION',(.126,.309,H+.00019),.005,'MarkBlack',TOP)
    # Exact unreadable warning microprint is not fabricated.
    # Camera and lighting, excluded from model exports.
    collection('90_STUDIO')
    scene=bpy.context.scene
    world=bpy.data.worlds.new('C6420_Studio_World');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.78,.80,.83,1);world.node_tree.nodes['Background'].inputs[1].default_value=.55;scene.world=world
    for name,loc,energy,size in [('Key',(.2,-.7,1.5),95,1.1),('Fill',(-1,-.3,.65),65,1.1),('Rim',(.2,1,.9),110,1.0)]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=energy;ld.shape='DISK';ld.size=size
        ob=bpy.data.objects.new(name,ld);COL.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,0,.04))-ob.location).to_track_quat('-Z','Y').to_euler()
    ca=bpy.data.cameras.new('Inspection_Camera');cam=bpy.data.objects.new('Inspection_Camera',ca);COL.objects.link(cam);scene.camera=cam
    cam.location=(.9,-1.25,.69);cam.rotation_euler=(Vector((0,0,.04))-cam.location).to_track_quat('-Z','Y').to_euler();ca.type='ORTHO';ca.ortho_scale=1.13;ca.clip_start=.005;ca.clip_end=20
    scene.render.resolution_x=1600;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='AgX'
    # Apply non-unit positive scaling from the adjusted main cover; no negative transforms exist.
    for ob in scene.objects:
        if ob.type=='MESH' and any(abs(v-1)>1e-7 for v in ob.scale):
            bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for ob in scene.objects:ob.select_set(False)
    # Store the actually executed parameterized source inside the blend.
    old=bpy.data.texts.get('build_c6420.py')
    if old:bpy.data.texts.remove(old)
    tx=bpy.data.texts.new('build_c6420.py');tx.write(Path(__file__).read_text())
    viewport();save('04-detailed-editable.blend')

def build_all():
    stage1();stage2();stage3();stage4();stage5()
    exec(compile((P/'scripts/repair_geometry.py').read_text(),'repair_geometry.py','exec'),{'__name__':'c6420_repair'})
    exec(compile((P/'scripts/refine_finish.py').read_text(),'refine_finish.py','exec'),{'__name__':'c6420_finish'})
    exec(compile((P/'scripts/prepare_triangles.py').read_text(),'prepare_triangles.py','exec'),{'__name__':'c6420_export_mesh'})



def stage5():
    # Keep cosmetic raised details inside the official 86.8 mm max envelope.
    for name in ['Front_top_cover','Main_top_cover','Rear_top_cover']:bpy.data.objects[name].location.z-=.0004
    for ob in bpy.context.scene.objects:
        if ob.name.startswith(('Top_stamped_','Top_flush_','Top_cover_release_','Official_top_','Observed_')):ob.location.z-=.00035
    # Convert evaluated curves/text with capped ends, then weld split cap vertices.
    # Components remain independently editable; original parameters and readable text are retained.
    bpy.ops.object.select_all(action='DESELECT')
    candidates=[o for o in bpy.context.scene.objects if o.type in {'MESH','CURVE','FONT'}]
    for ob in candidates:ob.select_set(True)
    bpy.context.view_layer.objects.active=candidates[0]
    bpy.ops.object.convert(target='MESH')
    fixes=[]
    for ob in candidates:
        if ob.type!='MESH':continue
        bm=bmesh.new();bm.from_mesh(ob.data)
        before=(len(bm.verts),len(bm.faces),sum(e.is_boundary for e in bm.edges),sum(f.calc_area()<1e-14 for f in bm.faces))
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8)
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        after=(len(bm.verts),len(bm.faces),sum(e.is_boundary for e in bm.edges),sum(f.calc_area()<1e-14 for f in bm.faces))
        if before!=after:fixes.append({'object':ob.name,'before_v_f_boundary_degenerate':before,'after_v_f_boundary_degenerate':after})
        bm.to_mesh(ob.data);bm.free();ob.data.update()
        if ob.name.startswith('PSU') and 'fabric_extraction_loop' in ob.name:
            maxy=max((ob.matrix_world@v.co).y for v in ob.data.vertices);ob.location.y+=.4157-maxy
    bpy.ops.object.select_all(action='DESELECT')
    (P/'qa/mesh-cleanup.json').write_text(json.dumps(fixes,indent=2))
    tx=bpy.data.texts.get('build_c6420.py');tx.clear();tx.write(Path(__file__).read_text())
    bpy.context.scene['mesh_preparation']='Curves/labels converted to editable meshes; split cap vertices welded; degenerate tessellation removed'
    save('05-cleaned-editable.blend')

if __name__=='__main__':build_all()
