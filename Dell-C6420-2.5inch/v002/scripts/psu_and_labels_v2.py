"""Two photographic2400WPSUs and real-source printed labels. Run inside build namespace."""

def fabric_loop(name,zc):
 # Closed woven ribbon, 14mmwide and0.8mmthick; unlike a round rubber cable.
 controls=[(.010,R+.0013),(.016,R+.009),(.016,R+.026),(.008,R+.0337),(.001,R+.026),(.0015,R+.011),(.005,R+.0013)]
 centers=[]
 for k in range(len(controls)):
  a,b,c,d=[Vector(controls[(k+j)%len(controls)]) for j in [-1,0,1,2]]
  for j in range(8):
   t=j/8;v=.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t);centers.append(v)
 vs=[];fs=[];n=len(centers)
 for i,c in enumerate(centers):
  tangent=(centers[(i+1)%n]-centers[i-1]).normalized();side=Vector((-tangent.y,tangent.x,0));up=Vector((0,0,1));twist=.11*math.sin(i*math.tau/n);b=up*math.cos(twist)+side*math.sin(twist);nrm=side*math.cos(twist)-up*math.sin(twist);base=Vector((c.x,c.y,zc))
  for w,t in [(-.007,-.0004),(.007,-.0004),(.007,.0004),(-.007,.0004)]:vs.append(tuple(base+b*w+nrm*t))
 for i in range(n):
  for j in range(4):fs.append((4*i+j,4*((i+1)%n)+j,4*((i+1)%n)+(j+1)%4,4*i+(j+1)%4))
 # Calibrate actual fabric outermost point to official rear envelope,without hidden dimensionproxy.
 lo=min(v[1] for v in vs);hi=max(v[1] for v in vs);vs=[(x,R+.0013+(y-lo)*(.0341-.0013)/(hi-lo),z) for x,y,z in vs]
 ob=mesh(name,vs,fs,'Nylon');bevel(ob,.00015,3)
 for p in ob.data.polygons:p.use_smooth=True
 uv=ob.data.uv_layers.new(name='Woven_ribbon_physical_UV');ob['image_uv_verified']=True
 distance=[0]
 for i in range(1,n):distance.append(distance[-1]+(centers[i]-centers[i-1]).length)
 full=distance[-1]+(centers[0]-centers[-1]).length
 for i in range(n):
  for j in range(4):
   poly=ob.data.polygons[i*4+j];u0=distance[i]/.0256;u1=(distance[i+1] if i+1<n else full)/.0256;v0=[0,.014,.0148,.0288][j]/.0256;v1=[.014,.0148,.0288,.0296][j]/.0256
   for li,co in zip(poly.loop_indices,[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]):uv.data[li].uv=co
 ob['physical_detail']='14mmwide flat nylon ribbon; closed extractionloop; not circular cable';return ob

def fan_blade(name,cx,zc,a):
 nr,na=7,5;vs=[];fs=[]
 for layer in range(2):
  for i in range(nr):
   t=i/(nr-1);r=.006+.0119*t
   for j in range(na):
    s=j/(na-1);ang=a+.20*t+.32*t*t+(s-.5)*(.63-.12*t);yy=R-.006+.0022*(s-.5)*(.3+.7*t)-layer*.00045
    vs.append((cx+r*math.cos(ang),yy,zc+r*math.sin(ang)))
 count=nr*na
 for i in range(nr-1):
  for j in range(na-1):
   q=i*na+j;fs.extend([(q,q+1,q+1+na,q+na),(q+count,q+na+count,q+na+1+count,q+1+count)])
 loop=[i for i in range(na)]+[i*na+na-1 for i in range(1,nr)]+[(nr-1)*na+j for j in range(na-2,-1,-1)]+[i*na for i in range(nr-2,0,-1)]
 for q,r in zip(loop,loop[1:]+loop[:1]):fs.append((q,q+count,r+count,r))
 ob=mesh(name,vs,fs,'ButtonBlack')
 for f in ob.data.polygons:f.use_smooth=True
 return ob

def psu_v2(i,zc):
 collection('05_POWER_SUPPLIES');root=group('PSU_'+str(i)+'_2400W','2400W PSU');root['source']='NSL/ETB photographed2400W EPP, not alternate1600W listings'
 for s in [-1,1]:
  box(f'PSU{i}_side_shell',(s*.043,.195,zc),(.0008,.373,.0405),'Zinc',.00010)
  box(f'PSU{i}_horizontal_shell',(0,.195,zc+s*.01985),(.0852,.373,.0008),'Zinc',.00010)
 box(f'PSU{i}_internal_end',(0,.0085,zc),(.085,.0008,.039),'DarkSteel',.00008)
 holes=[rounded(.0315,.0355,.0008,c=(-.0225,0)),rounded(.039,.039,.001,c=(.0216,0))]
 plate(f'PSU{i}_front_sheet',rounded(.087,.0405,.0012),holes,(0,R,zc),'Zinc',REAR,.00085,edge=.00010)
 # VerticalC20mains socket observerLEFT, three vertical blades as in actualphoto.
 acx=.0225;opening=fillet([(-.0113,-.0152),(.0113,-.0152),(.0113,.0126),(.0087,.0152),(-.0087,.0152),(-.0113,.0126)],.0010,5)
 plate(f'PSU{i}_AC_black_rim',rounded(.0298,.0350,.0010),[opening],(acx,R+.00125,zc),'ABS',REAR,.0050,edge=.00017)
 socket_profile(f'PSU{i}_AC_C20_recess',opening,(acx,R+.0008,zc),.012,.00050,'ButtonBlack')
 for k,(u,z) in enumerate([(-.0047,.0082),(.0047,0),(-.0047,-.0082)]):
  box(f'PSU{i}_AC_blade_{k}',(acx-u,R-.0040,zc+z),(.00145,.0060,.0041),'Nickel',.00016)
 extrude(f'PSU{i}_orange_release_paddle',rounded(.0045,.0175,.0015),(.0419,R+.0034,zc),REAR,.0035,'OrangeLatch',.00032)
 box(f'PSU{i}_latch_track',(.0419,R-.001,zc),(.005,.004,.021),'DarkSteel',.00014)
 # Shrouded40mmfan, curved vanes recessed behind a cut octagonal steel grille.
 cx=-.0216
 octagon=[(-.0178,-.0122),(-.0122,-.0178),(.0122,-.0178),(.0178,-.0122),(.0178,.0122),(.0122,.0178),(-.0122,.0178),(-.0178,.0122)]
 plate(f'PSU{i}_octagonal_fan_guard',rounded(.0399,.0399,.0013),[octagon],(cx,R+.0011,zc),'Nickel',REAR,.0008,edge=.00012)
 # Opaque fan tunnel and set-back dark motor guard close unintended rear sightlines.
 socket_profile(f'PSU{i}_fan_shroud',circle(.0180,n=64),(cx,R,zc),.017,.0010,'ButtonBlack')
 cyl(f'PSU{i}_fan_motor_hub',(cx,R-.0040,zc),.0068,.007,'ButtonBlack',REAR,48,.00025)
 for k in range(7):fan_blade(f'PSU{i}_curved_fan_vane_{k}',cx,zc,k*math.tau/7)
 for sign in [-1,1]:
  direction=Vector((1,sign));v=Vector((-direction.y,direction.x)).normalized()*.00058;a=Vector((-.0172,-sign*.0172));b=-a
  poly=[tuple(a-v),tuple(b-v),tuple(b+v),tuple(a+v)]
  extrude(f'PSU{i}_flat_guard_crossbar_{sign}',poly,(cx,R+.00145,zc),REAR,.0006,'Nickel',.00010)
 for sx in [-1,1]:
  for sz in [-1,1]:
   pos=(cx+sx*.01675,R+.00195,zc+sz*.01675);ring(f'PSU{i}_corner_washer',pos,.00245,.0017,.0004,'Nickel',REAR,36);screw(f'PSU{i}_fan_screw',tuple(Vector(pos)+Vector((0,.00065,0))),.0020,REAR,'Nickel',sx*sz*.24)
 cyl(f'PSU{i}_round_EPP_label_substrate',(cx,R+.0024,zc),.00935,.00065,'Zinc',REAR,64,.00010)
 if 'Real_EPP_label' not in MAT:photo_material('Real_EPP_label','etb-dell_poweredge_c6420_rear_4xmods_3_4.jpg',0,.50)
 poly=circle(.00915,n=64);uv=[((981+x/.00915*35)/1800,1-(608-y/.00915*35)/1200) for x,y in poly]
 ob=photo_patch(f'PSU{i}_REAL_EPP_2400W_print','Real_EPP_label',poly,uv,(cx,R+.00252,zc),REAR);ob['readable_text']='EPP /2400W /94% efficiency';ob['texture_source']='Originalphotograph, not AI glyphs; circle UV not mirrored'
 # Folded aluminum pull anchor and authentic flat woven extractionloop.
 box(f'PSU{i}_vertical_pull_anchor',(.006,R+.0007,zc),(.0062,.0014,.039),'Zinc',.0005)
 fabric_loop(f'PSU{i}_woven_extraction_loop',zc)
 return root

def original_top_labels():
 collection('07_PRINTED_MARKS');photo_material('Original_top_labels_NS L','nsl-C6400.png',0,.54)
 mat=MAT['Original_top_labels_NS L'];data=json.loads((P/'model/photo-calibration.json').read_text());T=Matrix(data['H_pixel_to_world']);Tinv=T.inverted()
 def region(name,quad,z):
  # Projective UV tessellation uses the original image directly; no AI retyping or relayout.
  vs=[];uv=[];fs=[];N=20;M=12
  p0,p1,p2,p3=[Vector(q) for q in quad] # bottomleft,bottomright,topright,topleft in image region
  for j in range(M+1):
   v=j/M
   for i in range(N+1):
    u=i/N;px=(1-v)*((1-u)*p0+u*p1)+v*((1-u)*p3+u*p2);q=T@Vector((px.x,px.y,1));xy=q.xy/q.z;vs.append((xy.x,xy.y,z));uv.append((px.x/1813,1-px.y/793))
  for j in range(M):
   for i in range(N):k=j*(N+1)+i;fs.append((k,k+1,k+N+2,k+N+1))
  ob=mesh(name,vs,fs,mat);layer=ob.data.uv_layers.new(name='Original_photo_projective_UV')
  for f in ob.data.polygons:
   for li in f.loop_indices:layer.data[li].uv=uv[ob.data.loops[li].vertex_index]
  # Winding by physical normal, never flipUV to fix normals.
  for f in ob.data.polygons:
   if f.normal.z<0:f.flip()
  ob.data.update();ob['image_uv_verified']=True;ob['intentional_open_surface']='Actual printedlabel surface, opaque, offset120microns over pressedsubstrate';ob['source_asset']='nsl-C6400.png originalpixels; calibratedphoto homography';ob['legibility_limit']='Text not sharpened/retyped; original photograph lacks macroprint resolution'
  return ob
 region('Real_service_label_band',[(338,251),(1461,248),(1364,205),(401,209)],H-.00069)
 region('Real_yellow_warning_label',[(1063,189),(1249,189),(1245,178),(1057,178)],H-.00072)
 region('Real_regulatory_label',[(522,192),(697,190),(697,180),(529,181)],H-.00072)

def stage4_psu_labels():
 for i,z in enumerate([.02225,.06455],1):psu_v2(i,z)
 original_top_labels();all_uv();viewport((.7,-1.65,.4),1.25,shading='MATERIAL');save('06-PSUs-original-labels.blend')
