"""User-corrected front:24 NORMAL2.5inch hotswap drive carriers, not blanks.
Official C6400 front and actual BargainHardware front; compatibleDXD9H open-latch photos for construction.
"""

def normal_carrier(i,x):
 collection('03_24SFF_HOTSWAP_CARRIERS');root=group(f'Carrier_{i:02d}_2p5inch','2.5-inch hot-swap carrier');root['bay_index']=i;root['mapped_node']=i//6+1
 root['source']='Official C6400 24SFF front; Bargain front photograph; DXD9H type three-window hinged carrier construction'
 # Actual metal carrier sides and installed disk envelope behind the air gap. No capacity is guessed.
 box(f'Drive{i:02}_metal_enclosure',(x,F+.061,.044),(.0140,.100,.06985),'DarkSteel',.0005)
 for s in [-1,1]:
  box(f'Carrier{i:02}_sheet_side_{s}',(x+s*.0073,F+.044,.044),(.0006,.118,.070),'Zinc',.00012)
  box(f'Carrier{i:02}_folded_runner_{s}',(x+s*.00755,F+.044,.011),(.0008,.118,.0028),'Nickel',.00018)
 # Rear molded bezel carries a real two-column large-cell honeycomb grid.
 holes=[]
 for col in [-1,1]:
  for row in range(9):
   xx=col*.0019125;zz=(row-4)*.0044167+(0 if col<0 else .002208)
   if abs(zz)+.002>.022:continue
   holes.append([(xx+.00220*math.cos(k*math.tau/6),zz+.00220*math.sin(k*math.tau/6)) for k in range(6)])
 grille=plate(f'Carrier{i:02}_setback_honeycomb',rounded(.0118,.0444,.0004),holes,(x,F-.0168,.0416),'ABS',FRONT,.00095,edge=.00007)
 grille['construction']='Set back4.8mm behind lever window face; not flat decorative printed grille'
 # Dark outer rim and two shallow fixed corner lands.
 plate(f'Carrier{i:02}_fixed_outer_bezel',rounded(.0158,.0768,.00055),[rounded(.0124,.0557,.00035,c=(0,-.008))],(x,F-.0142,.0437),'ABS',FRONT,.0025,edge=.00016)
 for s in [-1,1]:box(f'Carrier{i:02}_fixed_vertical_land',(x+s*.0071,F-.0151,.035),(.0009,.002,.058),'ButtonBlack',.00015)
 # The visible handle is a separate stamped U-frame with three rectangular molded openings.
 lever=group(f'Carrier{i:02}_HINGED_HANDLE','carrier release lever');lever.parent=root;lever['hinge_axis']='X';lever['hinge_world_m']=[x,F-.018,.0068]
 metalpoly=fillet([(-.00695,-.0278),(.00695,-.0278),(.00695,.0257),(.00565,.0278),(-.00565,.0278),(-.00695,.0257)],.00035,3)
 plate(f'Carrier{i:02}_silver_handle_frame',metalpoly,[rounded(.0120,.0538,.00025)],(x,F-.0214,.0348),'Nickel',FRONT,.0009,edge=.00012)
 opening_positions=[-.0099,.0034,.0167]
 plate(f'Carrier{i:02}_three_window_handle',rounded(.0120,.0555,.00045),[rounded(.0086,.01155,.00025,c=(0,z)) for z in opening_positions],(x,F-.02175,.0348),'ABS',FRONT,.0021,edge=.00015)
 box(f'Carrier{i:02}_handle_top_thumb_land',(x,F-.0217,.0640),(.0109,.0034,.0047),'ABS',.00045)
 # Bottom label/contact pad: documented neutral patch, no fabricated capacity/serial number.
 labelpoly=fillet([(-.0038,-.0046),(.0038,-.0046),(.0038,.0038),(.0030,.0046),(-.0030,.0046),(-.0038,.0038)],.00025,3)
 extrude(f'Carrier{i:02}_label_inset_pad',labelpoly,(x,F-.02194,.0132),FRONT,.00020,'InkGray',.00005)
 # Hinge axle, small spring winding, and retention pins are proper mechanical parts.
 cyl(f'Carrier{i:02}_hinge_axle',(x+.0063,F-.0190,.0069),.0011,.0126,'Nickel',RIGHT,32,.00008)
 pts=[]
 for j in range(65):
  t=j/64;aa=t*math.tau*4;pts.append((x-.0022+.0044*t,F-.0188+.0010*math.cos(aa),.0069+.0010*math.sin(aa)))
 curve(f'Carrier{i:02}_hinge_return_spring',pts,.00015,'Nickel')
 for s in [-1,1]:box(f'Carrier{i:02}_hinge_end_bracket',(x+s*.0054,F-.0175,.0069),(.0011,.0040,.0033),'Zinc',.00022)
 # Return to main carrier parent for fixed release button and indicator assembly.
 global PART
 PART=root
 box(f'Carrier{i:02}_release_bezel',(x,F-.0178,.0730),(.0126,.0080,.0103),'ButtonBlack',.0005)
 extrude(f'Carrier{i:02}_square_release_pad',rounded(.0098,.00875,.00050),(x,F-.02215,.0730),FRONT,.00135,'ABS',.00023)
 cyl(f'Carrier{i:02}_round_release_button',(x,F-.02245,.0730),.00263,.00065,'ButtonBlack',FRONT,48,.00012)
 ring(f'Carrier{i:02}_orange_release_ring',(x,F-.02257,.0730),.00263,.00226,.00014,'OrangeLatch',FRONT,48)
 cyl(f'Carrier{i:02}_button_inner_face',(x,F-.02260,.0730),.00223,.00013,'ButtonBlack',FRONT,48,.00007)
 box(f'Carrier{i:02}_indicator_strip',(x,F-.0175,.0800),(.0132,.0070,.00345),'ABS',.00035)
 for j,dx in enumerate([-.0037,.0037]):
  extrude(f'Carrier{i:02}_status_lens_{j}',rounded(.00135,.0013,.00030),(x+dx,F-.02114,.0800),FRONT,.00023,'LEDGreenOff',.00005)
 # Small status symbols at the correct top strip, made opaque instead of emissive patches.
 curve(f'Carrier{i:02}_activity_symbol',[(x+.0026,F-.02122,.0799),(x+.0032,F-.02122,.0799),(x+.00345,F-.02122,.08065),(x+.0038,F-.02122,.07945),(x+.0041,F-.02122,.0801),(x+.0047,F-.02122,.0801)],.000055,'InkGray')
 plate(f'Carrier{i:02}_disk_symbol',rounded(.00165,.0015,.0003),[rounded(.00125,.0011,.0002)],(x-.0037,F-.02122,.0800),'InkGray',FRONT,.000035,edge=0)
 # Photographed EMI spring fingers down side of fixed metal bezel, behind the lever rails.
 for s in [-1,1]:
  for j in range(9):
   z=.012+j*.0073
   points=[(x+s*.0077,F-.007,z-.0012),(x+s*.0079,F-.011,z-.0007),(x+s*.0078,F-.013,z+.0008),(x+s*.0075,F-.010,z+.0012)]
   ob=curve(f'Carrier{i:02}_EMI_spring_{s}_{j}',points,.00023,'Nickel')
 return root

def replace_front_with_normal_carriers():
 old=bpy.data.collections.get('03_24SFF_BLACK_BAY_FILLERS')
 if old:
  for ob in list(old.objects):bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.collections.remove(old)
 for i in range(24):normal_carrier(i,(i-11.5)*.0174)
 bpy.context.scene['front_state']='24 NORMAL2.5inch hotswap carriers installed, explicitly requested by user; no plastic blanks'
 all_uv();viewport((.55,-1.5,.30),1.17,shading='MATERIAL');save('05-normal-hotswap-front.blend')
