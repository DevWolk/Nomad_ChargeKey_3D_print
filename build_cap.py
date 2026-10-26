"""Nomad ChargeKey 240W double USB-C cap, revision 6. Units: mm. CadQuery 2.8.

USB-C shell: 8.25 x 2.40 x 6.65 (USB-IF Type-C Compliance Document Rev 2.1b, Table B-1).
Print with Z=0 on the bed and the openings facing up.

Usage: python build_cap.py [NAME [key=value ...]]  (keys from P, NAME defaults to v6)
Earlier variants:
  v4_1 pitch_estimated=6.9 height_clearance=0.12 grip_interference=0.32 finger_width=2.4 relief_width=3.6
  v5_1 pitch_estimated=6.9 grip_interference=0.36 finger_width=2.4 relief_width=3.6
Design notes and history: KNOWLEDGE_BASE.md.
"""
from pathlib import Path
import json
import math
import cadquery as cq

OUT=Path(__file__).resolve().parent
P={
 'width':13.4, 'height':15.8, 'depth':11.5, 'corner_radius':2.1,
 'edge_radius':0.35, 'floor':1.2,
 # Joined housings by ruler: ~11.4 wide, ~13.5 thick together.
 # 11.85 is the widest recess that keeps a 0.75 rim on the 13.4 body.
 'front_recess':0.6, 'recess_width':11.85, 'recess_height':14.2,
 'housing_width':11.4, 'housing_thickness':6.75,
 'usb_width':8.25, 'usb_thickness':2.4, 'usb_length':6.65,
 # Gauged pitch is 6.8-6.95; the low end makes the leaves press harder.
 'pitch_estimated':6.8,
 # Clearances are per side. The joined housings stop the plugs moving away from
 # the leaves, so on the ChargeKey a leaf bends by grip + (real pitch - pitch)/2.
 'width_clearance':0.10, 'height_clearance':0.10, 'grip_interference':0.36,
 # A wider leaf adds force without bending further.
 'finger_width':3.0, 'finger_thickness':0.8,
 'finger_root_z':2.0, 'finger_tip_z':9.6,
 'relief_width':4.20, 'relief_top_z':10.15,
 'texture_depth':0.30, 'texture_width':0.55,
 'texture_amplitude':0.34, 'texture_period':2.65,
}
def derive():
 P['channel_width']=P['usb_width']+2*P['width_clearance']
 P['channel_height']=P['usb_thickness']+2*P['height_clearance']
 P['finger_inner_y']=P['pitch_estimated']/2+P['channel_height']/2
 P['finger_grip_y']=P['pitch_estimated']/2+P['usb_thickness']/2-P['grip_interference']
 P['relief_inner_y']=P['finger_inner_y']-.55
 P['relief_outer_y']=P['finger_inner_y']+P['finger_thickness']+.65
derive()

def box(x0,x1,y0,y1,z0,z1):
 return (cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(False,False,False))
         .translate((x0,y0,z0)))

def wave(plane,span,level,phase):
 lo=[]; hi=[]; w=P['texture_width']/2
 for i in range(45):
  u=-span+2*span*i/44
  a=2*math.pi*u/P['texture_period']+phase
  v=level+P['texture_amplitude']*math.sin(a)
  dv=P['texture_amplitude']*2*math.pi/P['texture_period']*math.cos(a)
  nx=-dv/math.sqrt(1+dv*dv);ny=1/math.sqrt(1+dv*dv)
  lo.append((u-w*nx,v-w*ny));hi.append((u+w*nx,v+w*ny))
 end=(span+w,level+P['texture_amplitude']*math.sin(2*math.pi*span/P['texture_period']+phase))
 start=(-span-w,level+P['texture_amplitude']*math.sin(-2*math.pi*span/P['texture_period']+phase))
 return (cq.Workplane(plane).moveTo(*lo[0]).spline(lo[1:],includeCurrent=True)
         .threePointArc(end,hi[-1]).spline(list(reversed(hi[:-1])),includeCurrent=True)
         .threePointArc(start,lo[0]).close().extrude(P['texture_depth']+.12))

def stems(pitch=6.0):
 result=None
 for y in (-pitch/2,pitch/2):
  q=(cq.Workplane('XY',origin=(0,y,P['depth']-P['front_recess']-P['usb_length']))
     .slot2D(P['usb_width'],P['usb_thickness']).extrude(P['usb_length']))
  result=q if result is None else result.union(q)
 return result

def build():
 W,H,D=P['width'],P['height'],P['depth']
 shoulder=D-P['front_recess']
 m=(cq.Workplane('XY').box(W,H,D,centered=(True,True,False))
    .edges('|Z').fillet(P['corner_radius']).edges('not |Z').fillet(P['edge_radius']))
 for y in (-P['pitch_estimated']/2,P['pitch_estimated']/2):
  channel=(cq.Workplane('XY',origin=(0,y,P['floor']))
           .slot2D(P['channel_width'],P['channel_height']).extrude(D))
  m=m.cut(channel)
  entry=(cq.Workplane('XY',origin=(0,y,shoulder-.25))
         .slot2D(P['channel_width'],P['channel_height']).workplane(offset=.3)
         .slot2D(P['channel_width']+.5,P['channel_height']+.5).loft(combine=True))
  m=m.cut(entry)
 # Shallow common recess for the plug housings, with a rim around it.
 recess=(cq.Workplane('XY',origin=(0,0,shoulder))
         .rect(P['recess_width'],P['recess_height']).extrude(P['front_recess']+.4)
         .edges('|Z').fillet(1.9))
 m=m.cut(recess)
 # Hidden wells: 0.75 mm ceilings beneath the inset face keep the gaps concealed.
 for side in (-1,1):
  y0,y1=P['relief_inner_y'],P['relief_outer_y']
  if side<0:y0,y1=-y1,-y0
  m=m.cut(box(-P['relief_width']/2,P['relief_width']/2,y0,y1,
              P['finger_root_z'],P['relief_top_z']))
 # Four patterned exterior walls; no openings or relief slits on the outside.
 planes=[
  (cq.Plane(origin=(0,-H/2-.12,0),xDir=(1,0,0),normal=(0,1,0)),W/2-P['corner_radius']-.6),
  (cq.Plane(origin=(0,H/2+.12,0),xDir=(-1,0,0),normal=(0,-1,0)),W/2-P['corner_radius']-.6),
  (cq.Plane(origin=(-W/2-.12,0,0),xDir=(0,-1,0),normal=(1,0,0)),H/2-P['corner_radius']-.55),
  (cq.Plane(origin=(W/2+.12,0,0),xDir=(0,1,0),normal=(-1,0,0)),H/2-P['corner_radius']-.55),
 ]
 for plane,span in planes:
  if plane.yDir.z<0:plane=cq.Plane(origin=plane.origin,xDir=-plane.xDir,normal=plane.zDir)
  for j,z in enumerate((1.6,3.6,5.6,7.6,9.6)):
   m=m.cut(wave(plane,span,z,(j%2)*math.pi))
 static=m
 leaves=[]
 for side in (-1,1):
  y0=P['finger_inner_y'];y1=y0+P['finger_thickness'];fw=P['finger_width']
  leaf=box(-fw/2,fw/2,y0,y1,P['finger_root_z']-.4,P['finger_tip_z'])
  pad=(cq.Workplane('YZ',origin=(-fw/2,0,0))
       .polyline([(y0,6.7),(P['finger_grip_y'],8.0),
                  (P['finger_grip_y'],8.7),(y0,9.6)])
       .close().extrude(fw))
  leaf=leaf.union(pad)
  if side<0:leaf=leaf.mirror('XZ')
  leaves.append(leaf)
  m=m.union(leaf)
 return m.clean(),static,leaves

def validate(m,static):
 s=m.val();assert s.isValid();assert len(s.Solids())==1
 p=P['pitch_estimated']
 for pitch in (p-.2,p,p+.2):
  assert static.intersect(stems(pitch)).val().Volume()<1e-6
  for y in (-pitch/2,pitch/2):
   housing=(cq.Workplane('XY',origin=(0,y,P['depth']-P['front_recess']))
            .rect(P['housing_width'],P['housing_thickness']).extrude(5.0).edges('|Z').fillet(2.2))
   assert m.intersect(housing).val().Volume()<1e-6
 # The only intentional interference is the small grip pad on the OUTSIDE shell.
 bb=s.BoundingBox()
 grip,free=P['grip_interference'],P['height_clearance']
 return {
  'revision':'6', 'cad_valid':s.isValid(), 'connected_solids':len(s.Solids()),
  'dimensions_mm':[bb.xlen,bb.ylen,bb.zlen],
  'volume_mm3':s.Volume(), 'estimated_mass_PLA_g':s.Volume()*.00124,
  'channel_mm':[P['channel_width'],P['channel_height']],
  'pitch_mm':p,
  'rigid_wall_interference_at_pitch_plus_minus_0_2_mm':False,
  # Low end: a single loose plug shifts across its clearance; high end: the
  # joined ChargeKey plugs cannot, so the leaf bends by the full grip.
  'finger_deflection_range_mm':[round(grip-free,3),grip],
  'closed_bottom_thickness_mm':P['floor'],
  'nominal_tip_floor_gap_mm':P['depth']-P['front_recess']-P['usb_length']-P['floor'],
  'front_recess_mm':P['front_recess'],
  'nominal_housing_interference_mm3':0.0,
  'dimensions_from_photos_are_estimates':True,
  'retention':'Two compliant leaves on exterior metal USB shells; no internal pins',
  'physical_fit_tested':False,
 }

if __name__=='__main__':
 import sys
 name=sys.argv[1] if len(sys.argv)>1 else 'v6'
 for kv in sys.argv[2:]:
  k,v=kv.split('=');assert k in P,k;P[k]=float(v)
 derive()
 print(f'Building {name}...',flush=True)
 model,static,leaves=build()
 report=validate(model,static)
 report['variant']=name
 cq.exporters.export(model,str(OUT/f'Nomad_ChargeKey_cap_black_{name}.stl'),tolerance=.015,angularTolerance=.08)
 cq.exporters.export(model,str(OUT/f'Nomad_ChargeKey_cap_{name}.step'))
 (OUT/'parameters.json').write_text(json.dumps(P,indent=2)+'\n')
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)
