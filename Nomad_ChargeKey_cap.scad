/*
  Nomad ChargeKey 240W double USB-C cap, revision 6. OpenSCAD 2021.01 or newer.
  Units: mm. No libraries or external files.
  Same model as build_cap.py. Design notes and history: KNOWLEDGE_BASE.md.
  Customizer: change values, F6 to render, F7 to export STL.
  Print at 100 % with the floor on the bed and the openings up.
*/

/* [Body] */
// Body width
cap_width = 13.4; // [13.2:0.1:18]
// Body height
cap_height = 15.8; // [14.2:0.1:18]
// Body depth
cap_depth = 11.5; // [10:0.1:15]

/* [USB-C fit] */
// Plug pitch, centre to centre (gauged 6.8-6.95)
connector_pitch = 6.8; // [5.8:0.05:7.5]
// Clearance per side across the plug width
width_clearance = 0.10; // [0.05:0.01:0.50]
// Clearance per side across the plug thickness
height_clearance = 0.10; // [0.05:0.01:0.40]
// Leaf grip on the plug shell
grip_interference = 0.36; // [0.05:0.01:0.45]
// Front recess depth for the plug housings
front_recess = 0.60; // [0:0.1:1.0]

/* [Surface] */
// Wave texture on four walls
wave_texture = true;
// Groove depth
groove_depth = 0.30; // [0.15:0.05:0.40]
// Wave rows per wall
wave_rows = 5; // [3:1:6]
// Wave period
wave_period = 2.65; // [2.2:0.05:4.0]

/* [Quality] */
// Curve segments; 48 is enough for a 0.4 mm nozzle
curve_segments = 48; // [32:Fast,48:Normal,64:Smooth]

/* [Hidden] */
eps = 0.02;
$fn = curve_segments;
corner_r = 2.10;
edge_r = 0.35;
bottom = 1.20;
usb_w = 8.25;
usb_h = 2.40;
usb_l = 6.65;
slot_w = usb_w + 2 * width_clearance;
slot_h = usb_h + 2 * height_clearance;
shoulder_z = cap_depth - front_recess;
recess_w = 11.85;
recess_h = 14.20;
finger_w = 3.00;
finger_t = 0.80;
finger_inner_y = connector_pitch/2 + slot_h/2;
finger_grip_y = connector_pitch/2 + usb_h/2 - grip_interference;
finger_root_z = 2.0;
well_top_z = shoulder_z - 0.75;
finger_tip_z = well_top_z - 0.55;
well_w = 4.20;
well_inner_y = finger_inner_y - 0.55;
well_outer_y = finger_inner_y + finger_t + 0.65;
groove_w = 0.55;
wave_amp = 0.34;
wave_samples = 72;
z_first = 1.60;
z_last = cap_depth - 1.90;

assert(cap_width >= recess_w + 2*(edge_r+0.4), "Rim too thin: increase cap_width.");
assert(cap_height >= recess_h + 2*(edge_r+0.4), "Rim too thin: increase cap_height.");
assert(cap_height/2-well_outer_y-groove_depth >= 0.75,
       "Wall behind the leaf too thin: increase cap_height or reduce clearance, pitch or groove_depth.");
assert(slot_w/2 + 0.5 < cap_width/2, "Channel too wide for the body: increase cap_width.");
assert(shoulder_z-usb_l-bottom >= 0.4, "No room below the plug: increase cap_depth.");

module capsule_2d(w,h) {
  hull() for(x=[-(w-h)/2,(w-h)/2]) translate([x,0]) circle(d=h);
}

module rounded_rect_2d(w,h,r) {
  hull() for(x=[-w/2+r,w/2-r]) for(y=[-h/2+r,h/2-r])
    translate([x,y]) circle(r=r);
}

// A convex column with circular vertical corners and small rounded end edges.
module rounded_column() {
  rotate_extrude(convexity=8)
    hull() {
      square([corner_r-edge_r,cap_depth]);
      translate([corner_r-edge_r,edge_r]) circle(r=edge_r,$fn=16);
      translate([corner_r-edge_r,cap_depth-edge_r]) circle(r=edge_r,$fn=16);
    }
}

module outer_body() {
  hull() for(x=[-cap_width/2+corner_r,cap_width/2-corner_r])
    for(y=[-cap_height/2+corner_r,cap_height/2-corner_r])
      translate([x,y,0]) rounded_column();
}

module plug_channels() {
  for(y=[-connector_pitch/2,connector_pitch/2]) {
    translate([0,y,bottom]) linear_extrude(height=cap_depth+eps)
      capsule_2d(slot_w,slot_h);
    // Short insertion chamfer at the inset front face.
    hull() {
      translate([0,y,shoulder_z-0.25]) linear_extrude(height=eps)
        capsule_2d(slot_w,slot_h);
      translate([0,y,shoulder_z+0.05]) linear_extrude(height=eps)
        capsule_2d(slot_w+0.5,slot_h+0.5);
    }
  }
  if(front_recess>0) translate([0,0,shoulder_z])
    linear_extrude(height=front_recess+eps)
      rounded_rect_2d(recess_w,recess_h,1.90);
}

module leaf_well() {
  translate([-well_w/2,well_inner_y,finger_root_z])
    cube([well_w,well_outer_y-well_inner_y,well_top_z-finger_root_z]);
}

module positive_leaf() {
  union() {
    translate([-finger_w/2,finger_inner_y,finger_root_z-0.4])
      cube([finger_w,finger_t,finger_tip_z-finger_root_z+0.4]);
    // Local profile coordinates are Y,Z; extrusion runs along world X.
    multmatrix([[0,0,1,-finger_w/2],[1,0,0,0],[0,1,0,0],[0,0,0,1]])
      linear_extrude(height=finger_w)
        polygon([[finger_inner_y+eps,finger_tip_z-2.9],
                 [finger_grip_y,finger_tip_z-1.6],
                 [finger_grip_y,finger_tip_z-0.9],
                 [finger_inner_y+eps,finger_tip_z]]);
  }
}

function wave_v(u,level,phase) = level+wave_amp*sin(360*u/wave_period+phase);
function wave_d(u,phase) = wave_amp*2*PI/wave_period*cos(360*u/wave_period+phase);
function ribbon_point(u,level,phase,side) =
  let(d=wave_d(u,phase), n=sqrt(1+d*d), w=groove_w/2)
  [u-side*w*d/n, wave_v(u,level,phase)+side*w/n];

module wave_ribbon(span,level,phase) {
  union() {
    polygon(concat(
      [for(i=[0:wave_samples]) ribbon_point(-span+2*span*i/wave_samples,level,phase,-1)],
      [for(i=[wave_samples:-1:0]) ribbon_point(-span+2*span*i/wave_samples,level,phase,1)]
    ));
    for(u=[-span,span]) translate([u,wave_v(u,level,phase)]) circle(d=groove_w,$fn=20);
  }
}

module face_waves(span) {
  for(i=[0:wave_rows-1]) {
    z=z_first+(z_last-z_first)*i/(wave_rows-1);
    linear_extrude(height=groove_depth+0.12,convexity=12)
      wave_ribbon(span,z,(i%2)*180);
  }
}

module texture_cutters() {
  if(wave_texture) for(s=[-1,1]) {
    // Local X runs along the face, local Y points upward, local Z cuts inward.
    scale([1,s,1]) translate([0,cap_height/2+0.12,0])
      rotate([90,0,0]) face_waves(cap_width/2-corner_r-0.6);
    scale([s,1,1])
      multmatrix([[0,0,-1,cap_width/2+0.12],[-1,0,0,0],[0,1,0,0],[0,0,0,1]])
        face_waves(cap_height/2-corner_r-0.55);
  }
}

module cap() {
  union() {
    difference() {
      outer_body();
      plug_channels();
      for(s=[-1,1]) scale([1,s,1]) leaf_well();
      texture_cutters();
    }
    for(s=[-1,1]) scale([1,s,1]) positive_leaf();
  }
}

color([0.20,0.21,0.23]) cap();
