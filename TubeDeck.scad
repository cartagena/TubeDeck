// =====================================================================
//  TubeDeck - a retro CRT-TV housing for a Raspberry Pi 4 and a 10.5"
//  portable monitor. Magnets only, no screws.
//
//  The same design is built in Fusion 360 by TubeDeck.py.
//
//  Rounded-rect front outline, back tapering in like a picture tube;
//  faceplate recessed inside the front rim with a rounded screen window
//  and a raised bead; a control strip under the screen with two dual-USB
//  panels either side of a speaker grille; louvre vents on both sides; a
//  power button in a "tuning knob" collar on the left; stubby feet that can
//  tip the TV back.
//
//  Every part is a separate print, so each can be its own filament colour
//  (no multi-material printer needed).
//
//  PARTS - set `part`, render, export the STL. Every part is exported in its
//  print orientation, and none need supports:
//    "shell"      the TV body, printed back-rim down (255 x 241 footprint,
//                 150 tall - fills a 256mm bed)
//    "faceplate"  screen mask + control strip, printed back-face down
//    "collar"     "tuning knob" ring round the power button, glued into a
//                 groove on the left wall
//    "cradle"     holds the monitor behind the faceplate, printed flat
//    "rear"       back cover: a flush plug in the rear opening with the Pi 4
//                 standoffs, USB-C power hole and exhaust vents, printed
//                 outer face down
//    "foot_front" print 2 - taller than the rear pair when lean > 0
//    "foot_rear"  print 2   (both print standing on their cut bottom face)
//    "test_plate" one plate to print before the full parts: three USB-A panel
//                 widths, the USB-C power hole, the power button with its
//                 collar groove, and magnet pockets at 3 diameters each for
//                 3x3mm and 8x3mm magnets. Its collar comes alongside.
//    "all"        assembled preview   "exploded"  parts pulled apart
//
//  ASSEMBLY: the monitor drops into the cradle and the faceplate closes it
//  (5 8x3mm magnets). That sandwich slides into the shell from the front and
//  seats on an internal 45-degree ledge (4 8x3mm magnets, on pads). The rear
//  cover is a flush plug in the rear opening, seated on 4 corner gussets
//  (4 8x3mm magnets) and levered out through a notch in the bottom rim.
//  Zip-tie loops on the shell floor anchor the front USB cables. Feet are
//  glued in, located by a short peg.
//
//  Coordinates: X = width (centred), Y = depth (0 = front edge, +Y = back),
//  Z = up (0 = underside of the shell). All dimensions in mm.
// =====================================================================

part = "all";
lean = 0;                 // tip the TV back this many degrees (0-15) via taller front feet
badge_text = "PIXELDECK"; // "" to leave the badge off

// preview colours only - each part prints in a single filament
c_shell  = "#e8622c";
c_face   = "#1d1d1f";
c_accent = "#c9ccd1";
c_feet   = "#1d1d1f";
c_cradle = "#555555";

$fa = 4; $fs = 0.8;

/* ---------- components ---------- */
screen_w = 236; screen_h = 168; screen_t = 9.5;
active_w = 225; active_h = 152; active_off_v = 3.8;
sx = 0;                          // monitor centred left-right
fit = 0.3;
port_from = 21; port_len = 63;   // flat USB-C + mini-HDMI cables, left edge
btn_from = 46; btn_len = 32;     // wheel + power button, right edge
usb_cut = [25, 22];              // USB-A panel cut-out, w x h
usb_flange = [29, 26];           // USB-A panel front flange, w x h
usb_clip_pocket = [34, 24];      // recess behind the cut-out: 3mm panel, clears the 29.5mm clips
power_conn_d = 24;               // USB-C panel-mount barrel
button_d = 16;
magnet_d = 3; magnet_t = 3; magnet_fit = 0.35; pocket_over = 0.3;
mag_pocket_h = magnet_t + pocket_over;
big_magnet_d = 8; big_magnet_t = 3;   // all magnet joints in the TV
big_mag_pocket_d = big_magnet_d + magnet_fit; big_mag_pocket_h = big_magnet_t + pocket_over;
pi_holes = [58, 49];
standoff_h = 6; standoff_d = 6.5; standoff_base_d = 8; standoff_hole = 4.0;   // M2.5 heat-set inserts

/* ---------- housing ---------- */
W         = 255;  // one-piece shell, at the limit of a 256mm bed
wall      = 3;
depth     = 150;
straight  = 62;   // untapered front section
taper_x   = 22;   // each side pulls in by this much at the back
taper_top = 28;   // top drops by this much at the back
R_front   = 30;
R_rear    = 22;
front_fillet = 2; // rounds the shell's front rim
strip_h   = 44;   // control strip below the monitor
top_gap   = 22;   // monitor top to inner top (rounded corners need >= ~20)
recess    = 6;    // faceplate sits this far inside the front rim
face_t    = 5;
ledge_t   = 3.5;  // cradle material behind the monitor
ledge_w   = 6;    // how far that ledge reaches in under the monitor's edge
lip_w     = 6;    // shell's internal seat for the cradle
lip_d     = 3;    // flat part of that seat before its 45-degree underside
clear     = 0.4;  // part-to-part clearance
rear_t    = 5;
window_r  = 10;   // screen window corner radius
win_ch    = 1.2;  // 45-degree chamfer on the window edge
bead_gap  = 0.3; bead_w = 2.8; bead_h = 1.5;   // raised bead round the window
usb_x     = 80;
usb_panel_t = 3;  // wall thickness the snap-in USB panels clip onto
knob_y    = 47; knob_z_from_top = 70;   // power button, left side
foot_h    = 14;

/* ---------- derived ---------- */
Hs       = wall + strip_h + (screen_h + 2*fit) + top_gap + wall;
Wr       = W - 2*taper_x;
Hr       = Hs - taper_top;
mon_z0   = wall + strip_h;                     // monitor pocket bottom
mon_cz   = mon_z0 + fit + screen_h/2;
win_cz   = mon_cz + active_off_v;
win_z0   = win_cz - active_h/2;
cradle_t = screen_t + fit + ledge_t;
y_face   = recess;
y_cradle = y_face + face_t;
y_lip    = y_cradle + cradle_t;
usb_z    = wall + strip_h/2;
knob_z   = Hs - knob_z_from_top;
adapt_z0 = mon_z0 + fit + port_from;
btn_z0   = mon_z0 + fit + btn_from;

echo(str("TubeDeck: ", W, " x ", depth, " x ", Hs, " mm shell (W x D x H), + ", foot_h, " mm feet"));

// the monitor's top corners must sit inside the cradle's rounded outline
function in_rr(p, w, h, z0, r) =
    let(cx = max(abs(p[0]) - (w/2 - r), 0),
        cz = max(max(z0 + r - p[1], p[1] - (z0 + h - r)), 0))
    cx*cx + cz*cz <= r*r && abs(p[0]) <= w/2 && p[1] >= z0 && p[1] <= z0 + h;
cw = W - 2*wall - 2*clear; ch = Hs - 2*wall - 2*clear; cr = R_front - wall - clear;
for (p = [[sx + screen_w/2 + fit, mon_z0 + screen_h + 2*fit],
          [sx - screen_w/2 - fit, mon_z0 + screen_h + 2*fit]])
    assert(in_rr(p, cw, ch, wall + clear, cr),
           str("monitor corner ", p, " pokes through the rounded shell corner - raise top_gap"));

/* =====================================================================
   helpers
   ===================================================================== */

// rounded rectangle in the XZ plane (2D coords are (x, z)), centred in x,
// bottom edge at z = 0
module rr(w, h, r) { translate([0, h/2]) offset(r = r) square([w - 2*r, h - 2*r], center = true); }

// extrude a 2D (x, z) shape into a slab spanning world Y in [y0, y0 + t]
module slab(y0, t) { translate([0, y0 + t, 0]) rotate([90, 0, 0]) linear_extrude(t) children(); }

// shell outline at taper fraction k (0 = front section, 1 = rear rim)
module outer2d(k) rr(W - 2*taper_x*k, Hs - taper_top*k, R_front + (R_rear - R_front)*k);
module inner2d(k) translate([0, wall])
    rr(W - 2*taper_x*k - 2*wall, Hs - taper_top*k - 2*wall, R_front + (R_rear - R_front)*k - wall);
// outline of the parts that slide into the front section
module insert2d() offset(delta = -clear) inner2d(0);

// screen window grown by e on every side
module win2d(e) translate([sx, win_z0 - e]) rr(active_w + 2*e, active_h + 2*e, window_r + e);

module stadium(a, b, d) hull() { translate(a) circle(d = d); translate(b) circle(d = d); }

/* =====================================================================
   SHELL
   ===================================================================== */

module shell_outer() hull() {
    f = front_fillet;   // quarter-round on the front rim, sampled at 3 depths
    for (s = [[0, f], [0.13*f, 0.51*f], [0.5*f, 0.134*f]])
        slab(s[0], 0.01) offset(delta = -s[1]) outer2d(0);
    slab(f, 0.01) outer2d(0);
    slab(straight, 0.01) outer2d(0);
    slab(depth - 0.01, 0.01) outer2d(1);
}

module shell_hollow() {
    hull() {
        slab(-1, 0.01) inner2d(0);
        slab(straight, 0.01) inner2d(0);
        slab(depth - 0.01, 0.01) inner2d(1);
    }
    slab(depth - 0.02, 1.02) inner2d(1);
}

// internal seat for the cradle: flat front face, 45-degree underside so the
// shell prints back-down with no supports, notched on the left where the
// monitor's cables run back along the wall
module seat_lip() difference() {
    slab(y_lip, lip_d + lip_w) offset(delta = 0.5) inner2d(0);
    slab(y_lip - 0.01, lip_d + 0.02) offset(delta = -lip_w) inner2d(0);
    hull() {
        slab(y_lip + lip_d, 0.01) offset(delta = -lip_w) inner2d(0);
        slab(y_lip + lip_d + lip_w + 0.3, 0.01) inner2d(0);
    }
    translate([-W/2 - 1, y_lip - 1, adapt_z0 - 3])
        cube([wall + lip_w + 2, lip_d + lip_w + 2, port_len + 6]);
}

// The seat is widened to lip_pad_w only at the 4 magnet spots: a full-width
// ledge would foul the power button's nut, the USB panel bodies and the
// grille's sound path. The bottom pair sits at x = 56, clear of the grille
// (x 50) and USB (x 63) openings in the cradle.
lip_pad_w = 13; lip_pad_len = 14;
lip_mag_pts = [[-60, Hs - wall - lip_pad_w/2], [60, Hs - wall - lip_pad_w/2],
               [-56, wall + lip_pad_w/2],      [56, wall + lip_pad_w/2]];
module lip_pad(p) {   // flat front face lip_d deep, 45-degree underside back to the wall
    top = p[1] > Hs/2; zw = top ? Hs - wall : wall; s = top ? -1 : 1;
    yd = y_lip + lip_d;
    translate([p[0], 0, 0]) rotate([90, 0, 90]) linear_extrude(lip_pad_len, center = true)
        polygon([[y_lip, zw - s*0.5], [y_lip, zw + s*lip_pad_w], [yd, zw + s*lip_pad_w],
                 [yd + lip_pad_w, zw], [yd + lip_pad_w, zw - s*0.5]]);
}

// The rear cover is a plug in the rear opening, flush with the rim. It seats
// on 4 corner gussets whose faces stop rear_t short of the rim. Each gusset
// fills its rounded corner beyond a chord rear_gusset_dc out from the corner's
// arc centre, so with the shell printed rear-down its seat face is a ~42mm
// bridge anchored on both walls (a round boss there would need supports).
// Magnets sit rear_mag_inset in from the inner wall, leaving >= 2mm around each
// pocket inside the plug (which is `clear` smaller than the opening).
rear_y0 = depth - rear_t;           // plug's inner face = gusset faces
rear_mag_inset = 7;
rear_gusset_dc = 5.8; rear_gusset_t = 8;
pry_notch_w = 20;                   // notch in the bottom rim to lever the cover out
rb_off = (R_rear - wall - rear_mag_inset) / sqrt(2);
rear_mag_pts = [for (s = [-1, 1], t = [0, 1])
    [s * (Wr/2 - R_rear + rb_off), t == 0 ? R_rear - rb_off : Hr - R_rear + rb_off]];
module rear_gussets() for (s = [-1, 1], top = [false, true]) {   // clipped to shell_outer() by the caller
    c = [s * (Wr/2 - R_rear), top ? Hr - R_rear : R_rear];
    u = [s, top ? 1 : -1] / sqrt(2);
    translate([c[0] + rear_gusset_dc*u[0], rear_y0 - rear_gusset_t, c[1] + rear_gusset_dc*u[1]])
        rotate([0, atan2(-u[1], u[0]), 0]) translate([0, 0, -40]) cube([40, rear_gusset_t, 80]);
}

// "tuning knob" collar round the power button: a separate part glued into a
// 1mm groove rather than raised on the shell, which is already the full
// 255mm wide
collar_od = 36; collar_id = 25; collar_groove = 1; collar_proud = 2.5;
module collar_groove() translate([-W/2 - 1, knob_y, knob_z]) rotate([0, 90, 0])
    difference() {
        cylinder(h = 1 + collar_groove, d = collar_od + 0.4);
        translate([0, 0, -1]) cylinder(h = collar_groove + 3, d = collar_id - 0.4);
    }
module collar_local() difference() {   // groove face at z = 0
    union() {
        cylinder(h = collar_groove, d = collar_od);
        translate([0, 0, collar_groove - 0.01]) cylinder(h = collar_proud, d1 = collar_od, d2 = collar_od - 3);
    }
    translate([0, 0, -1]) cylinder(h = collar_groove + collar_proud + 2, d = collar_id);
}
module collar() translate([-W/2 + collar_groove, knob_y, knob_z]) rotate([0, -90, 0]) collar_local();

module side_louvres()   // both walls in one cut, in the tapered section
    for (i = [0:6]) translate([-W/2 - 5, 0, 0]) rotate([90, 0, 90])
        linear_extrude(W + 10) stadium([80, 100 + i*11], [128, 100 + i*11], 5);

foot_pts = [for (s = [-1, 1]) [s * (W/2 - 32), 28],
            for (s = [-1, 1]) [s * (W/2 - taper_x*(depth - 22 - straight)/(depth - straight) - 30), depth - 22]];

// Zip-tie loops on the floor (x, y of the slot centre): one behind each front
// USB panel, one halfway back toward the Pi. They anchor the stiff USB cables
// to the shell so the cables don't push the faceplate forward. 2.5mm walls
// either side of the slot, 2mm roof and a 45-degree back, so the shell still
// prints back-down without supports (the slot ceiling is a 2mm bridge).
tie_pts = [[-80, 50], [80, 50], [-40, 100], [40, 100]];
tie_slot = [5.2, 2];   // slot along Y x height: takes ties up to 4.8 x 1.5
module tie_loop(p) {
    ya = p[1] - tie_slot[0]/2 - 2.5; yb = p[1] + tie_slot[0]/2 + 2.5;
    z0 = wall - 0.5; zt = wall + tie_slot[1] + 2;
    translate([p[0], 0, 0]) rotate([90, 0, 90]) linear_extrude(6, center = true)
        polygon([[ya, z0], [ya, zt], [yb, zt], [yb + zt - wall, wall], [yb + zt - wall, z0]]);
}

module shell() difference() {
    union() {
        difference() { shell_outer(); shell_hollow(); }
        seat_lip();
        intersection() { shell_outer(); rear_gussets(); }
        for (p = tie_pts) tie_loop(p);
        for (p = lip_mag_pts) lip_pad(p);
    }
    collar_groove();
    for (p = lip_mag_pts)
        translate([p[0], y_lip - 0.01, p[1]]) rotate([-90, 0, 0]) cylinder(d = big_mag_pocket_d, h = big_mag_pocket_h);
    for (p = rear_mag_pts)
        translate([p[0], rear_y0 + 0.01, p[1]]) rotate([90, 0, 0]) cylinder(d = big_mag_pocket_d, h = big_mag_pocket_h + 0.01);
    // pry notch: a fingernail or flat screwdriver goes in behind the cover's edge
    translate([-pry_notch_w/2, rear_y0 - 1, -1]) cube([pry_notch_w, rear_t + 2, wall + 1.01]);
    // power button through the left wall, centred in the collar
    translate([-W/2 - 5, knob_y, knob_z]) rotate([0, 90, 0]) cylinder(d = button_d, h = wall + 10);
    // finger access to the monitor's wheel and button, right wall
    translate([W/2 - wall - 1, 0, 0]) rotate([90, 0, 90]) linear_extrude(wall + 2)
        stadium([y_cradle + 5, btn_z0 + 2], [y_cradle + 5, btn_z0 + btn_len - 2], 14);
    side_louvres();
    for (p = foot_pts) translate([p[0], p[1], -1]) cylinder(d = 8.4, h = 3);
    for (p = tie_pts) translate([p[0] - 4, p[1] - tie_slot[0]/2, wall]) cube([8, tie_slot[0], tie_slot[1]]);
}

/* =====================================================================
   FACEPLATE  (screen mask + control strip)
   ===================================================================== */

grille_w = 100; grille_h = 28; grille_z0 = usb_z - grille_h/2;
module grille2d() translate([0, grille_z0]) rr(grille_w, grille_h, 8);
// the lower pair is centred between the grille (x 50) and USB pass-throughs (x 63)
face_mag_pts = [[-90, Hs - wall - clear - 8], [0, Hs - wall - clear - 8], [90, Hs - wall - clear - 8],
                [-56.5, usb_z], [56.5, usb_z]];

// raised frame round each USB panel, 1mm clear of its flange so the flange
// sits flat on the faceplate. Centred on the origin.
module usb_frame2d() {
    iw = usb_flange[0] + 2; ih = usb_flange[1] + 2;
    difference() {
        translate([0, -ih/2 - 2.5]) rr(iw + 5, ih + 5, 5.5);
        translate([0, -ih/2]) rr(iw, ih, 3);
    }
}

module faceplate() difference() {
    union() {
        slab(y_face, face_t) insert2d();
        // USB panel frames
        for (s = [-1, 1]) slab(y_face - 1.5, 1.51) translate([s * usb_x, usb_z]) usb_frame2d();
        // frame round the grille
        slab(y_face - 1.2, 1.21) difference() { offset(delta = 2) grille2d(); grille2d(); }
        // raised bead round the window
        slab(y_face - bead_h, bead_h + 0.01) difference() {
            win2d(win_ch + bead_gap + bead_w); win2d(win_ch + bead_gap);
        }
        if (badge_text != "")
            slab(y_face - 1, 1.01) translate([sx, (grille_z0 + grille_h + 2 + win_z0 - win_ch - bead_gap - bead_w) / 2])
                text(badge_text, size = 5.5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
    }
    // screen window, 45-degree chamfer on its front edge
    slab(y_face - 1, face_t + 2) win2d(0);
    hull() { slab(y_face - 0.01, 0.01) win2d(win_ch); slab(y_face + win_ch, 0.01) win2d(0); }
    // USB panels: cut-out, and the plate thinned to usb_panel_t from behind
    for (s = [-1, 1]) {
        slab(y_face - 2, face_t + 3) translate([s * usb_x, usb_z]) square(usb_cut, center = true);
        slab(y_face + usb_panel_t, face_t) translate([s * usb_x, usb_z]) square(usb_clip_pocket, center = true);
    }
    // speaker grille: the monitor's speakers fire out of its short edges into
    // the housing, so this is a real sound path
    slab(y_face - 1, face_t + 2) intersection() {
        offset(delta = -2.5) grille2d();
        for (i = [0:5]) stadium([-grille_w/2, grille_z0 + 5 + i*3.6], [grille_w/2, grille_z0 + 5 + i*3.6], 2);
    }
    for (p = face_mag_pts)
        translate([p[0], y_face + face_t + 0.01, p[1]]) rotate([90, 0, 0]) cylinder(d = big_mag_pocket_d, h = big_mag_pocket_h + 0.01);
}

/* =====================================================================
   CRADLE  (monitor pocket, behind the faceplate)
   ===================================================================== */

module cradle() difference() {
    slab(y_cradle, cradle_t) insert2d();
    // monitor pocket, open to the front
    slab(y_cradle - 1, 1 + screen_t + fit)
        translate([sx - screen_w/2 - fit, mon_z0]) square([screen_w + 2*fit, screen_h + 2*fit]);
    // window behind the panel, leaving a ledge_w lip to sit on
    slab(y_cradle - 1, cradle_t + 2)
        translate([sx - screen_w/2 + ledge_w, mon_z0 + fit + ledge_w]) square([screen_w - 2*ledge_w, screen_h - 2*ledge_w]);
    // cable run (left) and button access (right), straight through
    slab(y_cradle - 1, cradle_t + 2) translate([-W/2 - 1, adapt_z0 - 1])
        square([W/2 + 1 + sx - screen_w/2 - fit + 1, port_len + 2]);
    slab(y_cradle - 1, cradle_t + 2) translate([sx + screen_w/2 + fit - 1, btn_z0 - 1]) square([W, btn_len + 2]);
    // room behind the USB panels and the grille
    for (s = [-1, 1]) slab(y_cradle - 1, cradle_t + 2) translate([s * usb_x, usb_z]) square([34, 34], center = true);
    slab(y_cradle - 1, cradle_t + 2) grille2d();
    for (p = face_mag_pts)
        translate([p[0], y_cradle - 0.01, p[1]]) rotate([-90, 0, 0]) cylinder(d = big_mag_pocket_d, h = big_mag_pocket_h);
    for (p = lip_mag_pts)
        translate([p[0], y_cradle + cradle_t + 0.01, p[1]]) rotate([90, 0, 0]) cylinder(d = big_mag_pocket_d, h = big_mag_pocket_h + 0.01);
}

/* =====================================================================
   REAR COVER
   ===================================================================== */

// lower-left Pi mounting hole (x, z): leaves ~50mm below the board for the
// USB-C power and micro-HDMI plugs on its bottom edge
pi_hole0 = [-73, 57];
pi_pts = [for (i = [0, 1], j = [0, 1]) [pi_hole0[0] + i*pi_holes[0], pi_hole0[1] + j*pi_holes[1]]];
power_pos = [70, 40];   // right side looking from the front

// flush plug: outer face level with the rim (y = depth), 0.6mm lead-in chamfer on the inner edge
module rear_cover() difference() {
    union() {
        hull() {
            slab(rear_y0, 0.01) offset(delta = -clear - 0.6) inner2d(1);
            slab(rear_y0 + 0.6, rear_t - 0.6) offset(delta = -clear) inner2d(1);
        }
        for (p = pi_pts) translate([p[0], rear_y0 + 0.5, p[1]]) rotate([90, 0, 0])
            cylinder(d1 = standoff_base_d, d2 = standoff_d, h = standoff_h + 0.5);
    }
    for (p = pi_pts) translate([p[0], rear_y0 - standoff_h - 0.01, p[1]]) rotate([-90, 0, 0])
        cylinder(d = standoff_hole, h = standoff_h + rear_t - 1);
    translate([power_pos[0], rear_y0 - 1, power_pos[1]]) rotate([-90, 0, 0]) cylinder(d = power_conn_d, h = rear_t + 2);
    // exhaust louvres, high up where the warm air collects
    slab(rear_y0 - 1, rear_t + 2) for (i = [0:6]) stadium([-72, 122 + i*10], [72, 122 + i*10], 4.5);
    for (p = rear_mag_pts)
        translate([p[0], rear_y0 - 0.01, p[1]]) rotate([-90, 0, 0]) cylinder(d = big_mag_pocket_d, h = big_mag_pocket_h);
}

/* =====================================================================
   FEET  (TV frame: z = 0 is the shell's underside, peg upward)
   The table plane rises toward the back at `lean` degrees through the rear
   feet's bottoms, so the rear feet stay foot_h tall, the front ones come out
   taller, and every foot's bottom is cut parallel to the table.
   ===================================================================== */

rear_foot_y = foot_pts[len(foot_pts) - 1][1];
function table_z(y) = -foot_h - (rear_foot_y - y) * tan(lean);
module below_table()   // half-space under the table plane
    translate([0, rear_foot_y, -foot_h]) rotate([lean, 0, 0]) translate([-W, -400, -60]) cube([2*W, 800, 60]);

module foot(p) difference() {
    union() {
        translate([p[0], p[1], table_z(p[1]) - 3]) cylinder(h = 3 - table_z(p[1]), d1 = 16, d2 = 24);
        translate([p[0], p[1], 0]) cylinder(h = 1.8, d = 8);
    }
    below_table();
}
// a foot standing on its cut bottom face, centred at the origin
module foot_on_bed(p) {
    b = [p[0], p[1], table_z(p[1])];   // bottom centre, on the table plane
    rotate([-lean, 0, 0]) translate(-b) foot(p);
}

/* =====================================================================
   TEST PLATE
   Reproduces the real parts' conditions, not just the hole sizes:
     USB - cut-out in a panel thinned to usb_panel_t from behind, with the
           faceplate's flange frame in front; 3 candidate widths (tp_usb_w,
           labelled) to find the one the clips snap into
     PWR - USB-C hole through a 5mm panel (the rear cover)
     BTN - button hole in a 3mm panel (the shell's side wall) + collar groove
     MAG - magnet pockets in the 5mm panel: 3 diameters for each magnet
           size (nominal + tp_mag_fits), 3x3mm on the left and 8x3mm on
           the right. The lower row opens on the bed side, where
           first-layer squish narrows the hole; the upper row opens
           upward. Diameters are raised above the columns.
   Standing up like the faceplate at y = tp_y (off to the side); print it
   back-face down.
   ===================================================================== */

tp_y = -100; tp_cz = 33; tp_h = 88;
tp_usb_x = [-88, -48, -8]; tp_usb_w = [25, 26, 27];
tp_pwr_x = 34; tp_btn_x = 80;
tp_mag_fits = [0.25, 0.35, 0.45];
// per magnet size: [centre x, column pitch, nominal diameter, pocket depth]
tp_mag_groups = [[-40, 13, magnet_d, mag_pocket_h],
                 [ 40, 16, big_magnet_d, big_mag_pocket_h]];
// every pocket column: [x, pocket diameter, pocket depth]
tp_mag = [for (g = tp_mag_groups, i = [0:len(tp_mag_fits) - 1])
    [g[0] + (i - (len(tp_mag_fits) - 1)/2) * g[1], g[2] + tp_mag_fits[i], g[3]]];
tp_mag_z = 58;   // lower row; the upper row is 13 above it, the labels 23 above
module test_plate() difference() {
    union() {
        slab(tp_y, face_t) rr(222, tp_h, 4);
        for (x = tp_usb_x) slab(tp_y - 1.5, 1.51) translate([x, tp_cz]) usb_frame2d();
        for (l = concat([[tp_pwr_x, "PWR"], [tp_btn_x, "BTN"]],
                        [for (i = [0:2]) [tp_usb_x[i], str(tp_usb_w[i])]]))
            slab(tp_y - 0.6, 0.61) translate([l[0], 7.5])
                text(l[1], size = 5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
        for (m = tp_mag)
            slab(tp_y - 0.6, 0.61) translate([m[0], tp_mag_z + 23])
                text(str(m[1]), size = 3.5, halign = "center", valign = "center",
                     font = "Liberation Sans:style=Bold");
    }
    for (i = [0:2]) {
        slab(tp_y - 2, face_t + 3) translate([tp_usb_x[i], tp_cz]) square([tp_usb_w[i], usb_cut[1]], center = true);
        slab(tp_y + usb_panel_t, face_t) translate([tp_usb_x[i], tp_cz]) square(usb_clip_pocket, center = true);
    }
    slab(tp_y - 1, face_t + 2) translate([tp_pwr_x, tp_cz]) circle(d = power_conn_d);
    slab(tp_y - 1, face_t + 2) translate([tp_btn_x, tp_cz]) circle(d = button_d);
    slab(tp_y + wall, face_t) translate([tp_btn_x, tp_cz]) circle(d = 40);
    slab(tp_y - 1, 1 + collar_groove) translate([tp_btn_x, tp_cz])
        difference() { circle(d = collar_od + 0.4); circle(d = collar_id - 0.4); }
    for (m = tp_mag) {
        slab(tp_y + face_t - m[2], m[2] + 1) translate([m[0], tp_mag_z]) circle(d = m[1]);
        slab(tp_y - 1, m[2] + 1) translate([m[0], tp_mag_z + 13]) circle(d = m[1]);
    }
}

/* =====================================================================
   OUTPUT
   ===================================================================== */

module monitor_ghost() {
    color("#222") translate([sx - screen_w/2, y_cradle, mon_z0 + fit]) cube([screen_w, screen_t, screen_h]);
    color("#3a6ea5") translate([sx - 222.7/2, y_cradle - 0.2, win_cz - 75]) cube([222.7, 0.2, 150]);
}
module pi_ghost() color("green")
    translate([pi_hole0[0] - 3.5, rear_y0 - standoff_h - 1.6, pi_hole0[1] - 3.5]) cube([85, 1.6, 56]);

module feet_all() for (p = foot_pts) foot(p);

module assembly(ex = 0) {
    color(c_shell)  shell();
    color(c_face)   translate([0, -ex * 1.2, 0]) faceplate();
    color(c_accent) translate([-ex * 0.5, 0, 0]) collar();
    color(c_cradle) translate([0, -ex * 0.6, 0]) cradle();
    color(c_shell)  translate([0, ex * 0.8, 0]) rear_cover();
    color(c_feet)   translate([0, 0, -ex * 0.4]) feet_all();
    if (ex == 0) { monitor_ghost(); pi_ghost(); }
}

// print orientations - rotate so the chosen face is on the bed
module on_bed(y_down) translate([0, 0, y_down]) rotate([-90, 0, 0]) children();

// assembled preview sits on the table: tip everything back by `lean`
if (part == "all")
    translate([0, 0, rear_foot_y * sin(lean) + foot_h * cos(lean)]) rotate([-lean, 0, 0]) assembly(0);
if (part == "exploded")  assembly(80);
if (part == "shell")     on_bed(depth) shell();
if (part == "faceplate") on_bed(y_face + face_t) faceplate();
if (part == "collar")    collar_local();
// plate back-face down, frame up; its collar printed alongside in the same job
if (part == "test_plate") { on_bed(tp_y + face_t) test_plate(); translate([0, -25, 0]) collar_local(); }
if (part == "cradle")    on_bed(y_cradle + cradle_t) cradle();
if (part == "rear")      on_bed(depth) rear_cover();
if (part == "foot_front") foot_on_bed(foot_pts[0]);
if (part == "foot_rear")  foot_on_bed(foot_pts[len(foot_pts) - 1]);
