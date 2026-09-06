"""Rear external detail traced from ETB/NSL original four-node photo, never mirrored."""

def socket_profile(name,poly,pos,depth=.007,lip=.00042,mat='Nickel'):
 outer=inset(poly,-lip)
 ob=plate(name+'_metal_cavity',outer,[poly],pos,mat,REAR,depth,edge=.00005)
 c=Vector(pos)-Vector((0,depth+.0006,0))
 xs=[x for x,y in poly];zs=[y for x,y in poly]
 box(name+'_dark_back',c,(max(xs)-min(xs)+.001,.001,max(zs)-min(zs)+.001),'DarkCavity',.00008)
 return ob

def rear_symbol_usb(name,x,y,z):
 # Tiny embossed/printed trident with circle/square/arrow endpoints.
 curve(name+'_stem',[(x,y,z-.0019),(x,y,z+.0018)],.00010,'InkWhite')
 curve(name+'_branchA',[(x,y,z-.0002),(x+.0007,y,z+.0004),(x+.0007,y,z+.0011)],.00010,'InkWhite')
 curve(name+'_branchB',[(x,y,z+.0002),(x-.0006,y,z+.0009),(x-.0006,y,z+.0013)],.00010,'InkWhite')
 cyl(name+'_circle',(x+.0007,y,z+.0013),.00019,.00004,'InkWhite',REAR,20,0)
 box(name+'_square',(x-.0006,y,z+.0015),(.00034,.00004,.00034),'InkWhite',0)
 extrude(name+'_arrow',[(-.00028,0),(.00028,0),(0,.00045)],(x,y,z+.0018),REAR,.00004,'InkWhite',0)
 cyl(name+'_root',(x,y,z-.0019),.00024,.00004,'InkWhite',REAR,20,0)

def node_v2(num,x,z0):
 collection('04_NODE_'+str(num));root=group('C6420_Node_'+str(num),'C6420 node');root['official_dimensions_mm']=[174.4,40.5,574.5]
 root['source']='ETB rear complete4-node photo;2USB+2SFP+microUSB+miniDP+RJ45; identical handedness'
 def wx(u):return x+.0872-u
 def pt(u,z,y=R):return (wx(u),y,z0+z)
 def polyat(w,h,u,z,r=.00065):return rounded(w,h,r,c=(u-.0872,z-.02025))
 def cirat(r,u,z):return circle(r,(u-.0872,z-.02025),28)
 front=R+.014325-.5745
 box(f'Node{num}_floor',(x,(front+R-.002)/2,z0+.00045),(.1744,R-.002-front,.0009),'DarkSteel',.00008)
 for s in [-1,1]:box(f'Node{num}_tray_side_{s}',(x+s*.08675,(front+R-.002)/2,z0+.02025),(.0009,R-.002-front,.0405),'Zinc',.00007)
 box(f'Node{num}_internal_air_shade',(x,R-.024,z0+.02025),(.171,.001,.037),'DarkCavity',.0001)
 box(f'Node{num}_visible_PCB_edge',(x,R-.020,z0+.0031),(.159,.035,.0012),'PCB',.00008)
 # Rounded punch pattern: two square rows plus short horizontal slots, traced from real photo.
 holes=[]
 for k in range(15):
  u=.0048+k*.00560
  for z in [.0343,.0287]:holes.append(polyat(.00375,.00375,u,z,.00048))
  if k not in [3,4]:holes.append(polyat(.00375,.00165,u,.0234,.00075))
  holes.append(polyat(.0038,.0013,u,.0392,.0005))
 # Separate connector-plate openings and long removable grip/blank assembly.
 holes += [polyat(.0222,.0204,.013,.0115,.0005),polyat(.046,.0148,.0545,.0116,.0005),polyat(.0795,.020,.130,.0288,.0005),polyat(.0087,.0038,.091,.0057,.0007),polyat(.0084,.0065,.121,.008,.001),polyat(.0163,.0137,.141,.0085,.00065),cirat(.0031,.1575,.0095)]
 for u in [.025,.084,.101,.1066,.1122,.165,.1706]:
  for z in [.0057,.0113]:
   if u==.025:holes.append(polyat(.00165,.00365,u,z,.0007))
   else:holes.append(polyat(.00365,.00365,u,z,.00045))
 for u in [.117,.174]:
  if u>.172:continue
  for z in [.0057,.0113]:holes.append(polyat(.00155,.0036,u,z,.00065))
 for u in [.037,.045,.053,.061,.069,.077,.091,.099,.167]:holes.append(polyat(.0037,.0016,u,.0189,.0007))
 for k in range(29):
  u=.0043+k*.0058
  if u<.172 and not .043<u<.076:holes.append(polyat(.0039,.00155,u,.0015,.0006))
 panel=plate(f'Node{num}_punched_rear_skin',rounded(.1744,.0405,.0008),holes,(x,R,z0+.02025),'Zinc',REAR,.00080,edge=.00006)
 panel['punch_basis']='ETB photo upperleft rear node; rounded square/oblong pattern, px scale174.4mm/644px'
 # Real returned lips around each tray; each bends inward, leaving assembly gap between nodes.
 for z in [.00065,.03985]:box(f'Node{num}_horizontal_rear_return',(x,R-.0032,z0+z),(.1726,.0064,.0008),'Nickel',.0001)
 for u in [.00055,.17385]:box(f'Node{num}_vertical_rear_return',pt(u,.02025,R-.0032),(.0008,.0064,.0378),'Nickel',.0001)
 # USB daughter frame and two distinct metal receptacles with actual blue tongues.
 plate(f'Node{num}_USB_black_mask',rounded(.0214,.0198,.0004),[rounded(.0143,.0062,.00055,c=(-.0011,z)) for z in [-.0038,.0049]],pt(.013,.0115,R+.00015),'ButtonBlack',REAR,.00035,edge=.00004)
 for j,z in enumerate([.0077,.0164]):
  u=.0119;pos=pt(u,z,R+.0007);socket_profile(f'Node{num}_USB3A_{j}',rounded(.0134,.00545,.0004),pos,.009,.00038)
  box(f'Node{num}_USB3A_{j}_blue_tongue',pt(u,z+.0010,R-.0028),(.0117,.0053,.0015),'USBBlue',.00012)
  for k in range(4):box(f'Node{num}_USB3A_{j}_front_contact_{k}',(wx(u)+(k-1.5)*.00235,R-.0024,z0+z-.00013),(.0008,.0029,.00018),'GoldContact',.00003)
  for k in range(5):box(f'Node{num}_USB3A_{j}_rear_contact_{k}',(wx(u)+(k-2)*.0019,R-.0063,z0+z+.00027),(.00048,.0019,.0002),'Nickel',.00003)
  for dx in [-.0041,.0041]:box(f'Node{num}_USB_retention_spring',(wx(u)+dx,R-.0012,z0+z-.00235),(.0012,.002,.00025),'Nickel',.00007)
 rear_symbol_usb(f'Node{num}_USB_icon',wx(.020),R+.00056,z0+.0128)
 screw(f'Node{num}_USB_plate_fastener',pt(.0256,.0204,R+.0006),.0021,REAR,angle=.3)
 # Network daughterplate has its own little retention cut-outs and spring tongues.
 localholes=[rounded(.01575,.0102,.0004,c=(du,0)) for du in [-.0021,.0152]]+[rounded(.0033,.0058,.0003,c=(-.0202,-.0008)),rounded(.0037,.0038,.0004,c=(-.0148,.0013))]
 plate(f'Node{num}_dual_SFP_adapter_face',rounded(.0461,.0145,.0005),localholes,pt(.0545,.0112,R+.00048),'Nickel',REAR,.00055,edge=.00005)
 for j,u in enumerate([.0524,.0697]):
  socket_profile(f'Node{num}_SFP_cage_{j}',rounded(.0145,.0089,.00018),pt(u,.0112,R+.00105),.027,.00033)
  # Thin folded retention flange, seam and visible captive springs around cage mouth.
  for dx in [-.00665,.00665]:
   box(f'Node{num}_SFP_{j}_side_spring', (wx(u)+dx,R-.0019,z0+.0113),(.00022,.0049,.0055),'Nickel',.00003)
  for dx in [-.0046,.0046]:box(f'Node{num}_SFP_{j}_top_tang',(wx(u)+dx,R-.0003,z0+.01555),(.0021,.0024,.00028),'Nickel',.00006)
  box(f'Node{num}_SFP_{j}_lower_flange',pt(u,.00625,R+.001),(.0105,.0014,.00055),'Nickel',.0001)
  box(f'Node{num}_SFP_{j}_connector_insert',pt(u,.0108,R-.019),(.011,.003,.0044),'ButtonBlack',.0001)
  for k in range(10):box(f'Node{num}_SFP_{j}_contact_{k}',(wx(u)+(k-4.5)*.0008,R-.0175,z0+.0101),(.0003,.0032,.00022),'GoldContact',.00002)
  text(f'Node{num}_SFP_index_{j}',str(2-j),pt(u,.0035,R+.00082),.0016,'InkBlack',REAR)
 # Micro USB trapezoidal keyed port and MiniDP, distinct profiles instead of generic boxes.
 micro=[(-.0037,.00115),(.0037,.00115),(.0035,-.00025),(.00255,-.00135),(-.00255,-.00135),(-.0035,-.00025)]
 micro.reverse();socket_profile(f'Node{num}_MicroUSB',fillet(micro,.00025,3),pt(.091,.0057,R+.0005),.006,.00032)
 box(f'Node{num}_MicroUSB_tongue',pt(.091,.0060,R-.0022),(.0053,.003,.00055),'ButtonBlack',.00008)
 dp=rounded(.0071,.0052,.0008)
 socket_profile(f'Node{num}_MiniDisplayPort',dp,pt(.121,.008,R+.00035),.007,.00045,'ButtonBlack')
 socket_profile(f'Node{num}_MiniDP_inner_shield',rounded(.0059,.0039,.0006),pt(.121,.008,R+.00048),.006,.00015,'Nickel')
 box(f'Node{num}_MiniDP_tongue',pt(.121,.008,R-.002),(.0048,.0038,.00055),'ButtonBlack',.00007)
 # RJ45 lip follows the keyed stepped profile. Eight separate spring contacts are visible inside.
 jack=[(-.0067,-.0055),(.0067,-.0055),(.0067,.0032),(.0043,.0032),(.0043,.0045),(.0028,.0045),(.0028,.0056),(-.0028,.0056),(-.0028,.0045),(-.0043,.0045),(-.0043,.0032),(-.0067,.0032)]
 socket_profile(f'Node{num}_iDRAC_RJ45',jack,pt(.141,.0085,R+.00062),.0105,.0006,'Nickel')
 for k in range(8):
  xx=wx(.141)+(k-3.5)*.00105
  curve(f'Node{num}_RJ45_spring_contact_{k}',[(xx,R-.0017,z0+.0036),(xx,R-.0068,z0+.0052),(xx,R-.0081,z0+.0070)],.000125,'GoldContact')
 for du,m in [(-.0062,'InkGray'),(.0062,'LEDGreenOff')]:box(f'Node{num}_RJ45_LED_lens',(wx(.141+du),R+.00055,z0+.0133),(.00165,.0006,.0018),m,.00022)
 ring(f'Node{num}_power_metal_rim',pt(.1575,.0095,R+.0004),.0030,.00256,.00045,'Nickel',REAR,48)
 cyl(f'Node{num}_power_button_lens',pt(.1575,.0095,R+.0007),.00254,.00085,'PowerLens',REAR,48,.00014)
 # Long recessed black module/grip with an irregular folded metal perimeter.
 outer=fillet([(-.040,-.0104),(.036,-.0104),(.036,-.007),(.041,-.007),(.041,.0104),(-.040,.0104)],.0006,3)
 plate(f'Node{num}_long_grip_folded_frame',outer,[rounded(.0698,.0134,.00032,c=(0,.0006))],pt(.130,.0288,R+.0015),'Nickel',REAR,.00085,edge=.00010)
 # Inset dark face plus real recess side walls, shadow is geometric.
 socket_profile(f'Node{num}_long_black_grip',rounded(.0698,.0134,.00032),pt(.130,.0294,R+.0006),.0075,.00032,'ButtonBlack')
 for z in [.0190,.0392]:box(f'Node{num}_grip_edge_fold',pt(.130,z,R-.00025),(.075,.0038,.0008),'Nickel',.00018)
 for u in [.1639,.096]:
  box(f'Node{num}_grip_press_lug',pt(u,.029,R+.0017),(.0011,.0011,.0148),'Zinc',.00036)
 cyl(f'Node{num}_grip_hinge_pin',pt(.167,.0188,R+.0015),.0017,.0014,'Nickel',REAR,32,.00009)
 # Pale blue injection-molded C-shaped extraction hook, plain face per locked photograph.
 bluepoly=fillet([(-.0085,-.010),(-.0085,.008),(-.0052,.012),(.0068,.012),(.0068,-.014),(-.0042,-.014)],.0020,7)
 extrude(f'Node{num}_blue_paddle_face',bluepoly,pt(.080,.0265,R+.014325),REAR,.00185,'BlueLatch',.00048)
 # Right return provides the actual hollow recess behind front paddle rather than a solid cube.
 box(f'Node{num}_blue_hook_return',pt(.0861,.0261,R+.0070),(.0020,.0125,.0230),'BlueLatch',.00055)
 for z in [.0158,.0372]:box(f'Node{num}_blue_hook_cross_return',pt(.0837,z,R+.0051),(.0060,.0094,.0018),'BlueLatch',.0005)
 screw(f'Node{num}_blue_latch_mount',pt(.0884,.0375,R+.0012),.00175,REAR,angle=.45)
 box(f'Node{num}_latch_steel_back',pt(.0881,.0260,R-.0012),(.0013,.0042,.024),'Nickel',.0002)
 # Printed interface marks; all are independently oriented on rear +Y plane.
 text(f'Node{num}_DP_mark','DP',pt(.121,.0151,R+.00020),.0025,'InkBlack',REAR)
 text(f'Node{num}_iDRAC_mark','iDRAC',pt(.1312,.0087,R+.0002),.00155,'InkBlack',REAR,rotate=math.pi/2)
 text(f'Node{num}_MicroUSB_service_mark','USB',pt(.091,.0101,R+.0002),.00145,'InkBlack',REAR)
 box(f'Node{num}_EST_tag',pt(.0568,.0017,R+.0007),(.019,.0005,.0026),'ButtonBlack',.0001)
 box(f'Node{num}_EST_blue_print',pt(.0568,.0017,R+.00097),(.011,.00008,.0023),'BlueLatch',.00003)
 text(f'Node{num}_EST_letters','EST',pt(.0568,.0017,R+.00105),.00163,'InkWhite',REAR)
 return root

def stage3_nodes():
 for num,x,z in [(1,-.1328,.0443),(2,-.1328,.002),(3,.1328,.0443),(4,.1328,.002)]:node_v2(num,x,z)
 all_uv();viewport((-.55,1.6,.25),1.15,shading='MATERIAL');save('04-four-C6420-detailed-nodes.blend')
