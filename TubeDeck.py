"""
TubeDeck - a retro CRT-TV housing for a Raspberry Pi 4 and a 10.5" portable monitor.

Fusion 360 script: run it from Scripts and Add-Ins, pick an option in the dialog.

  Full case         Shell, Faceplate, Collar, Cradle, Rear and Feet, each a
                    separate component in its assembled position, with an
                    optional lean-back (0-15 degrees) made by taller front feet.
  Test plate        USB-A panel, USB-C power and button cut-outs with the
                    real parts' frames and pockets, plus 3x3mm and 8x3mm
                    magnet pockets at three diameters each - print it to
                    check the fits.

Coordinates: X = width (centred on 0), Y = depth (0 = front edge, +Y = back),
Z = up. All parameters are millimetres.
"""

import adsk.core, adsk.fusion, traceback, math

# =====================================================================
# PARAMETERS
# =====================================================================

def build_params():
    T = dict(
        # monitor
        screen_w=236.0, screen_h=168.0, screen_t=9.5,
        active_w=225.0, active_h=152.0, active_off_v=3.8,
        fit=0.3, sx=0.0,
        # monitor side cut-outs: cables on the left edge, wheel + button on the right
        port_from=21.0, port_len=63.0, btn_from=46.0, btn_len=32.0,
        # front USB-A panels (snap-in) and their clip pocket
        usb_cut=(25.0, 22.0), usb_flange=(29.0, 26.0), usb_clip_pocket=(34.0, 24.0),
        usb_x=80.0, usb_panel_t=3.0,
        # power input, power button
        power_conn_d=24.0, button_d=16.0, knob_y=47.0, knob_z_from_top=70.0,
        # Pi 4 mount (heat-set inserts)
        pi_holes=(58.0, 49.0), standoff_h=6.0, standoff_d=6.5, standoff_base_d=8.0, standoff_hole=4.0,
        # magnets
        magnet_d=3.0, magnet_t=3.0, magnet_fit=0.35, pocket_over=0.3,
        big_magnet_d=8.0, big_magnet_t=3.0,
        # shell
        W=255.0, wall=3.0, depth=150.0, straight=62.0, taper_x=22.0, taper_top=28.0,
        R_front=30.0, R_rear=22.0, front_fillet=2.0, strip_h=44.0, top_gap=22.0,
        recess=6.0, face_t=5.0, ledge_t=3.5, ledge_w=6.0, lip_w=6.0, lip_d=3.0, clear=0.4,
        rear_t=5.0, window_r=10.0, win_ch=1.2, bead_gap=0.3, bead_w=2.8, bead_h=1.5,
        foot_h=14.0, lean=0.0, grille_w=100.0, grille_h=28.0,
        collar_od=36.0, collar_id=25.0, collar_groove=1.0, collar_proud=2.5,
        lip_pad_w=13.0, lip_pad_len=14.0,
        rear_mag_inset=7.0, rear_gusset_dc=5.8, rear_gusset_t=8.0, pry_notch_w=20.0,
        tie_slot=(5.2, 2.0), power_pos=(70.0, 40.0), pi_hole0=(-73.0, 57.0),
        badge_text='PIXELDECK')

    wall, fit = T['wall'], T['fit']
    T['mag_pocket_h'] = T['magnet_t'] + T['pocket_over']
    T['big_mag_pocket_d'] = T['big_magnet_d'] + T['magnet_fit']
    T['big_mag_pocket_h'] = T['big_magnet_t'] + T['pocket_over']

    T['Hs'] = wall + T['strip_h'] + (T['screen_h'] + 2 * fit) + T['top_gap'] + wall
    T['Wr'] = T['W'] - 2 * T['taper_x']
    T['Hr'] = T['Hs'] - T['taper_top']
    T['mon_z0'] = wall + T['strip_h']
    T['win_cz'] = T['mon_z0'] + fit + T['screen_h'] / 2 + T['active_off_v']
    T['win_z0'] = T['win_cz'] - T['active_h'] / 2
    T['cradle_t'] = T['screen_t'] + fit + T['ledge_t']
    T['y_face'] = T['recess']
    T['y_cradle'] = T['y_face'] + T['face_t']
    T['y_lip'] = T['y_cradle'] + T['cradle_t']
    T['usb_z'] = wall + T['strip_h'] / 2
    T['knob_z'] = T['Hs'] - T['knob_z_from_top']
    T['adapt_z0'] = T['mon_z0'] + fit + T['port_from']
    T['btn_z0'] = T['mon_z0'] + fit + T['btn_from']
    T['grille_z0'] = T['usb_z'] - T['grille_h'] / 2

    W, Hs, Wr, Hr, R_rear, lip_w = T['W'], T['Hs'], T['Wr'], T['Hr'], T['R_rear'], T['lip_w']
    pw = T['lip_pad_w']
    T['lip_mag_pts'] = [(-60.0, Hs - wall - pw / 2), (60.0, Hs - wall - pw / 2),
                        (-56.0, wall + pw / 2), (56.0, wall + pw / 2)]

    # the rear cover is a plug flush with the rim, seated on four corner gussets
    T['rear_y0'] = T['depth'] - T['rear_t']
    rb_off = (R_rear - wall - T['rear_mag_inset']) / math.sqrt(2)
    T['rear_mag_pts'] = [(s * (Wr / 2 - R_rear + rb_off), R_rear - rb_off if t == 0 else Hr - R_rear + rb_off)
                         for s in (-1, 1) for t in (0, 1)]

    top = Hs - wall - T['clear'] - 8
    T['face_mag_pts'] = [(-90.0, top), (0.0, top), (90.0, top), (-56.5, T['usb_z']), (56.5, T['usb_z'])]
    T['tie_pts'] = [(-80.0, 50.0), (80.0, 50.0), (-40.0, 100.0), (40.0, 100.0)]

    rear_foot_y = T['depth'] - 22
    rear_half = W / 2 - T['taper_x'] * (rear_foot_y - T['straight']) / (T['depth'] - T['straight'])
    T['foot_pts'] = [(s * (W / 2 - 32), 28.0) for s in (-1, 1)] + \
                    [(s * (rear_half - 30), rear_foot_y) for s in (-1, 1)]
    T['pi_pts'] = [(T['pi_hole0'][0] + i * T['pi_holes'][0], T['pi_hole0'][1] + j * T['pi_holes'][1])
                   for i in (0, 1) for j in (0, 1)]

    # the monitor's top corners must sit inside the cradle's rounded outline
    cw, ch, cr = W - 2 * wall - 2 * T['clear'], Hs - 2 * wall - 2 * T['clear'], T['R_front'] - wall - T['clear']
    z0 = wall + T['clear']
    for x in (T['sx'] + T['screen_w'] / 2 + fit, T['sx'] - T['screen_w'] / 2 - fit):
        z = T['mon_z0'] + T['screen_h'] + 2 * fit
        dx = max(abs(x) - (cw / 2 - cr), 0)
        dz = max(z - (z0 + ch - cr), 0)
        assert dx * dx + dz * dz <= cr * cr, 'monitor corner pokes through the rounded shell corner - raise top_gap'
    return T


# =====================================================================
# COORDINATE FRAMES
# =====================================================================

def x_rot_axes(angle_deg):
    a = math.radians(angle_deg)
    return ((1.0, 0.0, 0.0),
            (0.0, math.cos(a), math.sin(a)),
            (0.0, -math.sin(a), math.cos(a)))


FLAT_AXES = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
AXES_PX = ((0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0))    # local Z -> world +X
AXES_NX = ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (-1.0, 0.0, 0.0))   # local Z -> world -X
AXES_PY = x_rot_axes(-90)                                          # local Z -> world +Y
AXES_NY = x_rot_axes(90)                                           # local Z -> world -Y
TEXT_AXES = ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, -1.0, 0.0))  # raised text on the front face


# =====================================================================
# BUILDER - geometry primitives for one component. Each primitive is built
# at the origin, then moved into place with a free-move matrix.
# =====================================================================

class CaseBuilder:
    def __init__(self, comp):
        self.comp = comp

    @staticmethod
    def cm(v_mm):
        return v_mm / 10.0

    def _matrix(self, origin, axes):
        m = adsk.core.Matrix3D.create()
        m.setWithCoordinateSystem(
            adsk.core.Point3D.create(self.cm(origin[0]), self.cm(origin[1]), self.cm(origin[2])),
            adsk.core.Vector3D.create(*axes[0]),
            adsk.core.Vector3D.create(*axes[1]),
            adsk.core.Vector3D.create(*axes[2]),
        )
        return m

    def _move(self, body, origin, axes):
        coll = adsk.core.ObjectCollection.create()
        coll.add(body)
        mfs = self.comp.features.moveFeatures
        mi = mfs.createInput2(coll)
        mi.defineAsFreeMove(self._matrix(origin, axes))
        mfs.add(mi)

    def _rect_extrude(self, sx_mm, sy_mm, sz_mm):
        sk = self.comp.sketches.add(self.comp.xYConstructionPlane)
        p1 = adsk.core.Point3D.create(0, 0, 0)
        p2 = adsk.core.Point3D.create(self.cm(sx_mm), self.cm(sy_mm), 0)
        sk.sketchCurves.sketchLines.addTwoPointRectangle(p1, p2)
        prof = sk.profiles.item(0)
        ext = self.comp.features.extrudeFeatures.addSimple(
            prof, adsk.core.ValueInput.createByReal(self.cm(sz_mm)),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        return ext.bodies.item(0)

    def box(self, origin, size, axes=FLAT_AXES):
        body = self._rect_extrude(*size)
        self._move(body, origin, axes)
        return body

    def cyl(self, origin, d, h, axes=FLAT_AXES):
        sk = self.comp.sketches.add(self.comp.xYConstructionPlane)
        sk.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), self.cm(d / 2.0))
        prof = sk.profiles.item(0)
        ext = self.comp.features.extrudeFeatures.addSimple(
            prof, adsk.core.ValueInput.createByReal(self.cm(h)),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        body = ext.bodies.item(0)
        self._move(body, origin, axes)
        return body

    def cone(self, origin, d1, d2, h, axes=FLAT_AXES):
        """Truncated cone: d1 at the origin, d2 at local z = h."""
        body = self.circle_loft((0.0, 0.0), d1, 0.0, (0.0, 0.0), d2, h)
        self._move(body, origin, axes)
        return body

    def profile_body(self, pts_2d, width_mm, x0=0.0):
        """Polygon in the (Y, Z) plane extruded along X, centred on x0."""
        sk = self.comp.sketches.add(self.comp.xYConstructionPlane)
        lines = sk.sketchCurves.sketchLines
        pts3d = [adsk.core.Point3D.create(self.cm(p[0]), self.cm(p[1]), 0) for p in pts_2d]
        n = len(pts3d)
        for i in range(n):
            lines.addByTwoPoints(pts3d[i], pts3d[(i + 1) % n])
        prof = sk.profiles.item(0)
        ext = self.comp.features.extrudeFeatures.addSimple(
            prof, adsk.core.ValueInput.createByReal(self.cm(width_mm)),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        body = ext.bodies.item(0)
        self._move(body, (x0 - width_mm / 2.0, 0.0, 0.0), AXES_PX)
        return body

    def _combine(self, target, tools, operation):
        coll = adsk.core.ObjectCollection.create()
        for t in tools:
            coll.add(t)
        ci = self.comp.features.combineFeatures.createInput(target, coll)
        ci.operation = operation
        self.comp.features.combineFeatures.add(ci)
        return target

    def union(self, bodies):
        bodies = [b for b in bodies if b is not None]
        if len(bodies) > 1:
            self._combine(bodies[0], bodies[1:], adsk.fusion.FeatureOperations.JoinFeatureOperation)
        return bodies[0]

    def cut(self, target, tools):
        tools = [t for t in tools if t is not None]
        if not tools:
            return target
        return self._combine(target, tools, adsk.fusion.FeatureOperations.CutFeatureOperation)

    def intersect(self, target, tools):
        return self._combine(target, tools, adsk.fusion.FeatureOperations.IntersectFeatureOperation)

    # Fusion's construction-plane offset direction and sketch orientation differ
    # per plane, so nothing below trusts them: planes are checked against the
    # requested coordinate and flipped if needed, sketch points go through
    # modelToSketchSpace(), and the extrude direction follows the sketch normal.

    def _offset_plane(self, base, coord_mm, axis):
        planes = self.comp.constructionPlanes
        for sign in (1.0, -1.0):
            pi = planes.createInput()
            pi.setByOffset(base, adsk.core.ValueInput.createByReal(self.cm(coord_mm) * sign))
            plane = planes.add(pi)
            got = getattr(plane.geometry.origin, axis)
            if abs(got - self.cm(coord_mm)) < 1e-6:
                plane.isLightBulbOn = False
                return plane
            plane.deleteMe()
        raise RuntimeError('could not place a construction plane at {}={}'.format(axis, coord_mm))

    def _y_plane(self, y_mm):
        return self._offset_plane(self.comp.xZConstructionPlane, y_mm, 'y')

    def _z_plane(self, z_mm):
        return self._offset_plane(self.comp.xYConstructionPlane, z_mm, 'z')

    def _sp(self, sk, x, y, z):
        return sk.modelToSketchSpace(adsk.core.Point3D.create(self.cm(x), self.cm(y), self.cm(z)))

    def _rr_sketch(self, rr, y_mm):
        # rr = (cx, z0, w, h, r): rounded rectangle in the XZ plane, centred on
        # x = cx, bottom edge at z = z0
        cx, z0, w, h, r = rr
        x0, x1, z1 = cx - w / 2, cx + w / 2, z0 + h
        sk = self.comp.sketches.add(self._y_plane(y_mm))
        sk.isVisible = False
        P = lambda x, z: self._sp(sk, x, y_mm, z)
        lines, arcs = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
        bot = lines.addByTwoPoints(P(x0 + r, z0), P(x1 - r, z0))
        rgt = lines.addByTwoPoints(P(x1, z0 + r), P(x1, z1 - r))
        top = lines.addByTwoPoints(P(x1 - r, z1), P(x0 + r, z1))
        lft = lines.addByTwoPoints(P(x0, z1 - r), P(x0, z0 + r))
        k = r * (1 - 1 / math.sqrt(2))
        arcs.addByThreePoints(bot.endSketchPoint, P(x1 - k, z0 + k), rgt.startSketchPoint)
        arcs.addByThreePoints(rgt.endSketchPoint, P(x1 - k, z1 - k), top.startSketchPoint)
        arcs.addByThreePoints(top.endSketchPoint, P(x0 + k, z1 - k), lft.startSketchPoint)
        arcs.addByThreePoints(lft.endSketchPoint, P(x0 + k, z0 + k), bot.startSketchPoint)
        return sk, sk.profiles.item(0)

    def _extrude(self, sk, prof, t_mm, axis_vec):
        _, _, _, normal = sk.transform.getAsCoordinateSystem()
        along = normal.x * axis_vec[0] + normal.y * axis_vec[1] + normal.z * axis_vec[2]
        direction = (adsk.fusion.ExtentDirections.PositiveExtentDirection if along > 0
                     else adsk.fusion.ExtentDirections.NegativeExtentDirection)
        exts = self.comp.features.extrudeFeatures
        ei = exts.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ei.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(
            adsk.core.ValueInput.createByReal(self.cm(t_mm))), direction)
        return exts.add(ei).bodies.item(0)

    def rr_slab(self, rr, y0, t):
        """Rounded rect extruded over world Y in [y0, y0 + t]."""
        sk, prof = self._rr_sketch(rr, y0)
        return self._extrude(sk, prof, t, (0.0, 1.0, 0.0))

    def rr_ring(self, rr_out, rr_in, y0, t):
        return self.cut(self.rr_slab(rr_out, y0, t), [self.rr_slab(rr_in, y0 - 1, t + 2)])

    def _loft(self, profiles):
        lofts = self.comp.features.loftFeatures
        li = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        for p in profiles:
            li.loftSections.add(p)
        li.isSolid = True
        return lofts.add(li).bodies.item(0)

    def rr_loft(self, rr_a, y_a, rr_b, y_b):
        """Solid lofted between two rounded rects at world Y = y_a and y_b."""
        return self._loft([self._rr_sketch(rr_a, y_a)[1], self._rr_sketch(rr_b, y_b)[1]])

    def circle_loft(self, c_a, d_a, z_a, c_b, d_b, z_b):
        """Solid lofted between circle (centre (x, y), dia) at world Z = z_a and z_b."""
        profs = []
        for (cx, cy), d, z in ((c_a, d_a, z_a), (c_b, d_b, z_b)):
            sk = self.comp.sketches.add(self._z_plane(z))
            sk.isVisible = False
            sk.sketchCurves.sketchCircles.addByCenterRadius(self._sp(sk, cx, cy, z), self.cm(d / 2))
            profs.append(sk.profiles.item(0))
        return self._loft(profs)

    def fillet_face_at_y(self, body, y_mm, r_mm):
        """Round every edge of the planar face lying at world Y = y_mm."""
        edges = adsk.core.ObjectCollection.create()
        for f in body.faces:
            if (f.geometry.surfaceType == adsk.core.SurfaceTypes.PlaneSurfaceType
                    and abs(f.centroid.y - self.cm(y_mm)) < 1e-4):
                for e in f.edges:
                    edges.add(e)
        fillets = self.comp.features.filletFeatures
        fi = fillets.createInput()
        radius = adsk.core.ValueInput.createByReal(self.cm(r_mm))
        if hasattr(fi, 'edgeSetInputs'):
            fi.edgeSetInputs.addConstantRadiusEdgeSet(edges, radius, True)
        else:
            fi.addConstantRadiusEdgeSet(edges, radius, True)
        fillets.add(fi)

    def text_bodies(self, text, size_mm, height_mm, origin, axes):
        """Raised text centred on `origin`: local X reads left to right, local Y
        is up the letters, local Z is the extrusion."""
        sk = self.comp.sketches.add(self.comp.xYConstructionPlane)
        sk.isVisible = False
        texts = sk.sketchTexts
        ti = texts.createInput2(text, self.cm(size_mm))
        half = self.cm(size_mm * len(text))
        ti.setAsMultiLine(adsk.core.Point3D.create(-half, -self.cm(size_mm), 0),
                          adsk.core.Point3D.create(half, self.cm(size_mm), 0),
                          adsk.core.HorizontalAlignments.CenterHorizontalAlignment,
                          adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
        ti.fontName = 'Arial'
        st = texts.add(ti)
        ext = self.comp.features.extrudeFeatures.addSimple(
            st, adsk.core.ValueInput.createByReal(self.cm(height_mm)),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        bodies = [ext.bodies.item(i) for i in range(ext.bodies.count)]
        coll = adsk.core.ObjectCollection.create()
        for bd in bodies:
            coll.add(bd)
        mfs = self.comp.features.moveFeatures
        mi = mfs.createInput2(coll)
        mi.defineAsFreeMove(self._matrix(origin, axes))
        mfs.add(mi)
        return bodies


# =====================================================================
# SHARED SHAPES
# =====================================================================

def tv_outer(T, k):
    # rounded-rect outline (cx, z0, w, h, r) of the shell at taper fraction k
    return (0.0, 0.0, T['W'] - 2 * T['taper_x'] * k, T['Hs'] - T['taper_top'] * k,
            T['R_front'] + (T['R_rear'] - T['R_front']) * k)


def rr_grow(rr, d):
    cx, z0, w, h, r = rr
    return (cx, z0 - d, w + 2 * d, h + 2 * d, r + d)


def tv_inner(T, k):
    return rr_grow(tv_outer(T, k), -T['wall'])


def tv_insert(T):
    # outline of the parts that slide into the shell's front section
    return rr_grow(tv_inner(T, 0), -T['clear'])


def tv_window(T, e):
    return (T['sx'], T['win_z0'] - e, T['active_w'] + 2 * e, T['active_h'] + 2 * e, T['window_r'] + e)


def tv_grille(T):
    return (0.0, T['grille_z0'], T['grille_w'], T['grille_h'], 8.0)


def stadium_x(b, y1, y2, z, d, x0, x1):
    # slot running along Y at height z, cut straight through X
    return [b.box((x0, y1, z - d / 2), (x1 - x0, y2 - y1, d)),
            b.cyl((x0, y1, z), d, x1 - x0, axes=AXES_PX),
            b.cyl((x0, y2, z), d, x1 - x0, axes=AXES_PX)]


def stadium_x_vert(b, y, z1, z2, d, x0, x1):
    # slot running along Z, cut straight through X
    return [b.box((x0, y - d / 2, z1), (x1 - x0, d, z2 - z1)),
            b.cyl((x0, y, z1), d, x1 - x0, axes=AXES_PX),
            b.cyl((x0, y, z2), d, x1 - x0, axes=AXES_PX)]


def stadium_y(b, x1, x2, z, d, y0, y1):
    # slot running along X at height z, cut straight through Y
    return [b.box((x1, y0, z - d / 2), (x2 - x1, y1 - y0, d)),
            b.cyl((x1, y0, z), d, y1 - y0, axes=AXES_PY),
            b.cyl((x2, y0, z), d, y1 - y0, axes=AXES_PY)]


def rear_gussets(b, T):
    # Corner blocks behind a chord across each rounded rear corner, clipped to
    # the shell's outer solid. The rear cover seats on their front faces; each
    # face spans wall to wall, so it prints as a bridge with the shell rear-down.
    depth, straight, t, dc = T['depth'], T['straight'], T['rear_gusset_t'], T['rear_gusset_dc']
    y0 = T['rear_y0'] - t
    k = lambda y: (y - straight) / (depth - straight)
    Wr, Hr, R = T['Wr'], T['Hr'], T['R_rear']
    out = []
    for s in (-1, 1):
        for top in (False, True):
            cx, cz = s * (Wr / 2 - R), (Hr - R) if top else R
            ux, uz = s / math.sqrt(2), (1 if top else -1) / math.sqrt(2)
            vx, vz = -uz, ux
            blk = b.box((cx + dc * ux - 40 * vx, y0, cz + dc * uz - 40 * vz), (40, t, 80),
                        axes=((ux, 0.0, uz), (0.0, 1.0, 0.0), (vx, 0.0, vz)))
            out.append(b.intersect(blk, [b.rr_loft(tv_outer(T, k(y0)), y0, tv_outer(T, k(T['rear_y0'])),
                                                   T['rear_y0'])]))
    return out


def lip_pad_profile(T, top):
    # (y, z) outline of a magnet pad that widens the cradle seat against the top
    # or bottom wall: flat front face, 45-degree underside back to the wall
    pw, y0, yd = T['lip_pad_w'], T['y_lip'], T['y_lip'] + T['lip_d']
    zw, s = (T['Hs'] - T['wall'], -1.0) if top else (T['wall'], 1.0)
    return [(y0, zw - s * 0.5), (y0, zw + s * pw), (yd, zw + s * pw), (yd + pw, zw), (yd + pw, zw - s * 0.5)]


def tie_loop_profile(T, y):
    # (y, z) outline of a zip-tie loop on the floor, slot centred on y, with a
    # 45-degree back so it prints without supports
    sw, sh = T['tie_slot']
    z0, zt = T['wall'] - 0.5, T['wall'] + sh + 2.0
    ya = y - sw / 2 - 2.5
    yb = y + sw / 2 + 2.5
    return [(ya, z0), (ya, zt), (yb, zt), (yb + (zt - T['wall']), T['wall']), (yb + (zt - T['wall']), z0)]


# =====================================================================
# PARTS
# =====================================================================

def build_tv_shell(b, T, warnings):
    W, wall, depth, straight = T['W'], T['wall'], T['depth'], T['straight']
    y_lip, lip_w, lip_d = T['y_lip'], T['lip_w'], T['lip_d']
    ky, kz = T['knob_y'], T['knob_z']
    inner0 = tv_inner(T, 0)

    # straight front section, then the picture-tube taper to the rear rim
    outer = b.union([b.rr_slab(tv_outer(T, 0), 0, straight),
                     b.rr_loft(tv_outer(T, 0), straight, tv_outer(T, 1), depth)])
    try:
        b.fillet_face_at_y(outer, 0, T['front_fillet'])
    except Exception:
        warnings.append('front rim fillet failed - shell built with a sharp front edge')
    hollow = b.union([b.rr_slab(inner0, -1, straight + 1),
                      b.rr_loft(inner0, straight, tv_inner(T, 1), depth),
                      b.rr_slab(tv_inner(T, 1), depth - 0.02, 1.02)])
    shell = b.cut(outer, [hollow])

    # seat for the cradle: flat front face, 45-degree underside, notched on the
    # left where the monitor's cables run back
    lip = b.cut(b.rr_slab(rr_grow(inner0, 0.5), y_lip, lip_d + lip_w), [
        b.rr_slab(rr_grow(inner0, -lip_w), y_lip - 0.01, lip_d + 0.02),
        b.rr_loft(rr_grow(inner0, -lip_w), y_lip + lip_d, inner0, y_lip + lip_d + lip_w + 0.3),
        b.box((-W / 2 - 1, y_lip - 1, T['adapt_z0'] - 3), (wall + lip_w + 2, lip_d + lip_w + 2, T['port_len'] + 6))])
    gussets = rear_gussets(b, T)
    loops = [b.profile_body(tie_loop_profile(T, p[1]), 6.0, x0=p[0]) for p in T['tie_pts']]
    pads = [b.profile_body(lip_pad_profile(T, p[1] > T['Hs'] / 2), T['lip_pad_len'], x0=p[0])
            for p in T['lip_mag_pts']]
    shell = b.union([shell, lip, *gussets, *loops, *pads])

    mag_d, mag_h = T['big_mag_pocket_d'], T['big_mag_pocket_h']
    cutters = []
    for p in T['lip_mag_pts']:
        cutters.append(b.cyl((p[0], y_lip - 0.01, p[1]), mag_d, mag_h, axes=AXES_PY))
    for p in T['rear_mag_pts']:
        cutters.append(b.cyl((p[0], T['rear_y0'] + 0.01, p[1]), mag_d, mag_h + 0.01, axes=AXES_NY))
    # notch in the bottom rim to lever the rear cover out
    nw = T['pry_notch_w']
    cutters.append(b.box((-nw / 2, T['rear_y0'] - 1, -1), (nw, T['rear_t'] + 2, wall + 1.01)))
    # power button through the left wall, and the groove its collar glues into
    cutters.append(b.cyl((-W / 2 - 5, ky, kz), T['button_d'], wall + 10, axes=AXES_PX))
    cutters.append(b.cut(b.cyl((-W / 2 - 1, ky, kz), T['collar_od'] + 0.4, 1 + T['collar_groove'], axes=AXES_PX),
                         [b.cyl((-W / 2 - 2, ky, kz), T['collar_id'] - 0.4, T['collar_groove'] + 4, axes=AXES_PX)]))
    # finger access to the monitor's wheel and button, right wall
    cutters += stadium_x_vert(b, T['y_cradle'] + 5, T['btn_z0'] + 2, T['btn_z0'] + T['btn_len'] - 2, 14,
                              W / 2 - wall - 1, W / 2 + 1)
    for i in range(7):   # side louvres
        cutters += stadium_x(b, 80, 128, 100 + i * 11, 5, -W / 2 - 5, W / 2 + 5)
    for p in T['foot_pts']:
        cutters.append(b.cyl((p[0], p[1], -1), 8.4, 3))
    sw, sh = T['tie_slot']
    for x, y in T['tie_pts']:
        cutters.append(b.box((x - 4, y - sw / 2, wall), (8, sw, sh)))
    shell = b.cut(shell, cutters)
    shell.name = 'TV Shell'
    return shell


def build_tv_faceplate(b, T, warnings):
    y_face, face_t, usb_x, usb_z = T['y_face'], T['face_t'], T['usb_x'], T['usb_z']
    grille = tv_grille(T)
    plate = b.rr_slab(tv_insert(T), y_face, face_t)

    adds = []
    # raised frame round each USB panel, 1mm clear of its flange
    fw, fh = T['usb_flange']
    for s in (-1, 1):
        inner = (s * usb_x, usb_z - (fh + 2) / 2, fw + 2, fh + 2, 3.0)
        adds.append(b.rr_ring(rr_grow(inner, 2.5), inner, y_face - 1.5, 1.51))
    adds.append(b.rr_ring(rr_grow(grille, 2), grille, y_face - 1.2, 1.21))
    # raised bead round the screen window
    ch, gap, bw = T['win_ch'], T['bead_gap'], T['bead_w']
    adds.append(b.rr_ring(tv_window(T, ch + gap + bw), tv_window(T, ch + gap), y_face - T['bead_h'], T['bead_h'] + 0.01))
    if T['badge_text']:
        badge_z = (T['grille_z0'] + T['grille_h'] + 2 + T['win_z0'] - T['win_ch'] - T['bead_gap'] - T['bead_w']) / 2
        try:
            adds += b.text_bodies(T['badge_text'], 5.5, 1.01, (T['sx'], y_face + 0.01, badge_z), TEXT_AXES)
        except Exception:
            warnings.append('badge text failed - faceplate built without it')
    plate = b.union([plate, *adds])

    # screen window with a 45-degree chamfer on its front edge
    cutters = [b.rr_slab(tv_window(T, 0), y_face - 1, face_t + 2),
               b.rr_loft(tv_window(T, ch), y_face - 0.01, tv_window(T, 0), y_face + ch)]
    uw = T['usb_cut']
    pw, ph = T['usb_clip_pocket']
    for s in (-1, 1):   # USB cut-out, and the panel thinned from behind
        cutters.append(b.box((s * usb_x - uw[0] / 2, y_face - 2, usb_z - uw[1] / 2), (uw[0], face_t + 3, uw[1])))
        cutters.append(b.box((s * usb_x - pw / 2, y_face + T['usb_panel_t'], usb_z - ph / 2), (pw, face_t, ph)))
    # speaker grille; each slot is clipped separately because the slots don't touch
    for i in range(6):
        slot = b.union(stadium_y(b, -T['grille_w'] / 2, T['grille_w'] / 2, T['grille_z0'] + 5 + i * 3.6, 2,
                                 y_face - 1, y_face + face_t + 1))
        cutters.append(b.intersect(slot, [b.rr_slab(rr_grow(grille, -2.5), y_face - 1, face_t + 2)]))
    for p in T['face_mag_pts']:
        cutters.append(b.cyl((p[0], y_face + face_t + 0.01, p[1]), T['big_mag_pocket_d'], T['big_mag_pocket_h'] + 0.01,
                             axes=AXES_NY))
    plate = b.cut(plate, cutters)
    plate.name = 'TV Faceplate'
    return plate


def build_tv_collar(b, T):
    x0 = -T['W'] / 2 + T['collar_groove']
    ky, kz = T['knob_y'], T['knob_z']
    collar = b.cut(b.cyl((x0, ky, kz), T['collar_od'], T['collar_groove'] + T['collar_proud'], axes=AXES_NX),
                   [b.cyl((x0 + 1, ky, kz), T['collar_id'], T['collar_groove'] + T['collar_proud'] + 2, axes=AXES_NX)])
    collar.name = 'TV Collar'
    return collar


def build_tv_cradle(b, T):
    W, sx, fit = T['W'], T['sx'], T['fit']
    sw, sh, y0, t = T['screen_w'], T['screen_h'], T['y_cradle'], T['cradle_t']
    mon_z0, lw = T['mon_z0'], T['ledge_w']
    plate = b.rr_slab(tv_insert(T), y0, t)
    cutters = [
        # monitor pocket, open to the front
        b.box((sx - sw / 2 - fit, y0 - 1, mon_z0), (sw + 2 * fit, 1 + T['screen_t'] + fit, sh + 2 * fit)),
        # window behind the panel, leaving a ledge for it to sit on
        b.box((sx - sw / 2 + lw, y0 - 1, mon_z0 + fit + lw), (sw - 2 * lw, t + 2, sh - 2 * lw)),
        # cable run (left) and button access (right)
        b.box((-W / 2 - 1, y0 - 1, T['adapt_z0'] - 1), (W / 2 + 1 + sx - sw / 2 - fit + 1, t + 2, T['port_len'] + 2)),
        b.box((sx + sw / 2 + fit - 1, y0 - 1, T['btn_z0'] - 1), (W, t + 2, T['btn_len'] + 2)),
        b.rr_slab(tv_grille(T), y0 - 1, t + 2),
    ]
    for s in (-1, 1):   # room behind the USB panels
        cutters.append(b.box((s * T['usb_x'] - 17, y0 - 1, T['usb_z'] - 17), (34, t + 2, 34)))
    for p in T['face_mag_pts']:
        cutters.append(b.cyl((p[0], y0 - 0.01, p[1]), T['big_mag_pocket_d'], T['big_mag_pocket_h'], axes=AXES_PY))
    for p in T['lip_mag_pts']:
        cutters.append(b.cyl((p[0], y0 + t + 0.01, p[1]), T['big_mag_pocket_d'], T['big_mag_pocket_h'] + 0.01,
                             axes=AXES_NY))
    plate = b.cut(plate, cutters)
    plate.name = 'TV Cradle'
    return plate


def build_tv_rear(b, T):
    # A plug in the rear opening: its outer face is level with the rim, with a
    # lead-in chamfer on the inner edge. It seats on the shell's corner gussets.
    rear_t, y0 = T['rear_t'], T['rear_y0']
    plug = rr_grow(tv_inner(T, 1), -T['clear'])
    cover = b.union([b.rr_loft(rr_grow(plug, -0.6), y0, plug, y0 + 0.6),
                     b.rr_slab(plug, y0 + 0.6, rear_t - 0.6)])
    standoffs = [b.cone((p[0], y0 + 0.5, p[1]), T['standoff_base_d'], T['standoff_d'], T['standoff_h'] + 0.5,
                        axes=AXES_NY)
                 for p in T['pi_pts']]
    cover = b.union([cover, *standoffs])
    cutters = [b.cyl((p[0], y0 - T['standoff_h'] - 0.01, p[1]), T['standoff_hole'], T['standoff_h'] + rear_t - 1,
                     axes=AXES_PY) for p in T['pi_pts']]
    px, pz = T['power_pos']
    cutters.append(b.cyl((px, y0 - 1, pz), T['power_conn_d'], rear_t + 2, axes=AXES_PY))
    for i in range(7):   # exhaust louvres, high up where the warm air collects
        cutters += stadium_y(b, -72, 72, 122 + i * 10, 4.5, y0 - 1, y0 + rear_t + 1)
    for p in T['rear_mag_pts']:
        cutters.append(b.cyl((p[0], y0 - 0.01, p[1]), T['big_mag_pocket_d'], T['big_mag_pocket_h'], axes=AXES_PY))
    cover = b.cut(cover, cutters)
    cover.name = 'TV Rear'
    return cover


def tv_table_z(T, y):
    # The table surface in the TV's frame: the rear feet stay foot_h tall and the
    # plane rises toward the back at `lean` degrees, so the front feet come out
    # taller and the TV tips back.
    rear_y = T['foot_pts'][-1][1]
    return -T['foot_h'] - (rear_y - y) * math.tan(math.radians(T['lean']))


def build_tv_feet(b, T):
    # Each foot's bottom is cut parallel to the table so all four sit flat;
    # print each one standing on that cut face.
    lean, W = T['lean'], T['W']
    a = math.radians(lean)
    y0, depth = -200.0, 60.0
    feet = []
    for px, py in T['foot_pts']:
        cone = b.circle_loft((px, py), 24, 0, (px, py), 16, tv_table_z(T, py) - 3)
        foot = b.union([cone, b.cyl((px, py, 0), 8, 1.8)])
        # half-space below the table plane: local Y runs along the plane, local Z is its normal
        below = b.box((-W, y0 + depth * math.sin(a), tv_table_z(T, y0) - depth * math.cos(a)),
                      (2 * W, 600, depth), axes=x_rot_axes(lean))
        foot = b.cut(foot, [below])
        foot.name = 'Foot front' if py < T['depth'] / 2 else 'Foot rear'
        feet.append(foot)
    return feet


# =====================================================================
# TEST PLATES
# =====================================================================

def build_test_plate(b, T, usb_widths=(25.0, 26.0, 27.0), mag_fits=(0.25, 0.35, 0.45)):
    """One plate to print before the full parts. It reproduces the real parts'
    frames, pockets and panel thicknesses:
      USB  three candidate widths for the front USB-A panels
      PWR  the USB-C power hole
      BTN  the power button hole with its collar groove
      MAG  magnet pockets: three diameters (nominal + fit) for each magnet size,
           3x3mm on the left and 8x3mm on the right; the lower row opens on
           the bed side, where first-layer squish narrows the hole, the upper
           row opens upward
    Print it back-face down; its collar is a second body."""
    ty, t, cz, ph_total = -100.0, T['face_t'], 33.0, 88.0
    usb_xs = (-88.0, -48.0, -8.0)
    xp, xb = 34.0, 80.0
    mag_z = 58.0
    # per magnet size: (centre x, column pitch, nominal diameter, pocket depth)
    mag_groups = ((-40.0, 13.0, T['magnet_d'], T['mag_pocket_h']),
                  (40.0, 16.0, T['big_magnet_d'], T['big_mag_pocket_h']))
    mags = [(cx + (i - (len(mag_fits) - 1) / 2) * pitch, d + f, h)
            for cx, pitch, d, h in mag_groups for i, f in enumerate(mag_fits)]
    od, idd, g, proud = T['collar_od'], T['collar_id'], T['collar_groove'], T['collar_proud']
    plate = b.rr_slab((0.0, 0.0, 222.0, ph_total, 4.0), ty, t)

    fw, fh = T['usb_flange']
    pw, ph = T['usb_clip_pocket']
    uh = T['usb_cut'][1]
    adds, cutters = [], []
    labels = [(xp, 7.5, 'PWR', 5), (xb, 7.5, 'BTN', 5)]
    for x, uw in zip(usb_xs, usb_widths):
        inner = (x, cz - (fh + 2) / 2, fw + 2, fh + 2, 3.0)
        adds.append(b.rr_ring(rr_grow(inner, 2.5), inner, ty - 1.5, 1.51))
        cutters.append(b.box((x - uw / 2, ty - 2, cz - uh / 2), (uw, t + 3, uh)))
        cutters.append(b.box((x - pw / 2, ty + T['usb_panel_t'], cz - ph / 2), (pw, t, ph)))
        labels.append((x, 7.5, '{:g}'.format(uw), 5))
    for x, d, h in mags:
        cutters.append(b.cyl((x, ty + t - h, mag_z), d, h + 1, axes=AXES_PY))    # opens on the bed side
        cutters.append(b.cyl((x, ty - 1, mag_z + 13), d, h + 1, axes=AXES_PY))    # opens upward
        labels.append((x, mag_z + 23, '{:.2f}'.format(d), 3.5))
    try:
        for x, z, label, size in labels:
            adds += b.text_bodies(label, size, 0.61, (x, ty + 0.01, z), TEXT_AXES)
    except Exception:
        pass
    plate = b.union([plate, *adds])

    plate = b.cut(plate, cutters + [
        b.cyl((xp, ty - 1, cz), T['power_conn_d'], t + 2, axes=AXES_PY),
        b.cyl((xb, ty - 1, cz), T['button_d'], t + 2, axes=AXES_PY),
        b.cyl((xb, ty + T['wall'], cz), 40, t, axes=AXES_PY),
        b.cut(b.cyl((xb, ty - 1, cz), od + 0.4, 1 + g, axes=AXES_PY),
              [b.cyl((xb, ty - 2, cz), idd - 0.4, g + 4, axes=AXES_PY)]),
    ])
    plate.name = 'TestPlate'
    collar = b.cut(b.cyl((xb, ty + g, cz), od, g + proud, axes=AXES_NY),
                   [b.cyl((xb, ty + g + 1, cz), idd, g + proud + 2, axes=AXES_NY)])
    collar.name = 'TestPlate Collar'
    return plate, collar


# =====================================================================
# ENTRY POINT
# =====================================================================

OPTION_CASE = 'Full case'
OPTION_TEST = 'Test plate only (USB / USB-C / button / magnet fits)'
CMD_ID = 'TubeDeckChooser'
TEST_PLATE_NOTE = ('\nTestPlate: print-test plate (USB frames + thinned panels, USB-C, button + collar '
                   'groove, magnet pockets) off to the side at y=-100; print it and TestPlate Collar '
                   'before the full parts.')
_handlers = []   # Fusion only keeps event handlers alive while Python holds a reference


def new_component(root, name):
    occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    return occ.component


def generate_case(root, lean_deg, with_test_plate):
    T = build_params()
    T['lean'] = float(lean_deg)
    warnings = []
    build_tv_shell(CaseBuilder(new_component(root, 'TV Shell')), T, warnings)
    build_tv_faceplate(CaseBuilder(new_component(root, 'TV Faceplate')), T, warnings)
    build_tv_collar(CaseBuilder(new_component(root, 'TV Collar')), T)
    build_tv_cradle(CaseBuilder(new_component(root, 'TV Cradle')), T)
    build_tv_rear(CaseBuilder(new_component(root, 'TV Rear')), T)
    build_tv_feet(CaseBuilder(new_component(root, 'TV Feet')), T)
    msg = ('Done: Shell / Faceplate / Collar / Cradle / Rear / Feet created, assembled.\n'
           'Shell: {:.0f} x {:.0f} x {:.1f} mm (W x D x H), plus {} underneath.\n'
           'Each component is a separate print (and can be its own filament colour).').format(
        T['W'], T['depth'], T['Hs'],
        '{:.0f} mm feet'.format(T['foot_h']) if T['lean'] == 0 else
        'feet for a {:.0f} deg lean-back (front {:.1f} mm, rear {:.0f} mm tall)'.format(
            T['lean'], -tv_table_z(T, T['foot_pts'][0][1]), T['foot_h']))
    if with_test_plate:
        build_test_plate(CaseBuilder(new_component(root, 'TestPlate')), T)
        msg += TEST_PLATE_NOTE
    if warnings:
        msg += '\n\nWarnings:\n- ' + '\n- '.join(warnings)
    return msg


class _ChooserCreated(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        try:
            cmd = args.command
            cmd.okButtonText = 'Generate'
            inputs = cmd.commandInputs
            option = inputs.addDropDownCommandInput('option', 'Build', adsk.core.DropDownStyles.TextListDropDownStyle)
            option.listItems.add(OPTION_CASE, True, '')
            option.listItems.add(OPTION_TEST, False, '')
            lean = inputs.addIntegerSpinnerCommandInput('lean', 'Lean back (deg)', 0, 15, 1, 0)
            lean.tooltip = 'Tips the TV back by making the front feet taller. 0 = upright.'
            inputs.addBoolValueInput('test_plate', 'Also build the test plate', True, '', False)

            for event, handler in ((cmd.inputChanged, _ChooserChanged()), (cmd.execute, _ChooserExecute()),
                                   (cmd.destroy, _ChooserDestroy())):
                event.add(handler)
                _handlers.append(handler)
        except Exception:
            adsk.core.Application.get().userInterface.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class _ChooserChanged(adsk.core.InputChangedEventHandler):
    def notify(self, args):
        if args.input.id == 'option':
            full = args.input.selectedItem.name == OPTION_CASE
            args.inputs.itemById('lean').isVisible = full
            args.inputs.itemById('test_plate').isVisible = full


class _ChooserExecute(adsk.core.CommandEventHandler):
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        try:
            inputs = args.command.commandInputs
            choice = inputs.itemById('option').selectedItem.name
            lean = inputs.itemById('lean').value
            with_test_plate = inputs.itemById('test_plate').value
            root = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct).rootComponent
            if choice == OPTION_TEST:
                build_test_plate(CaseBuilder(new_component(root, 'TestPlate')), build_params())
                msg = 'Done: TestPlate + TestPlate Collar created.' + TEST_PLATE_NOTE
            else:
                msg = generate_case(root, lean, with_test_plate)
            ui.messageBox(msg)
        except Exception:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class _ChooserDestroy(adsk.core.CommandEventHandler):
    def notify(self, args):
        adsk.terminate()


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        if not adsk.fusion.Design.cast(app.activeProduct):
            ui.messageBox('Create or open a design (a Fusion document) first, then run this script.')
            return
        cmd_def = ui.commandDefinitions.itemById(CMD_ID)
        if cmd_def:
            cmd_def.deleteMe()
        cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, 'TubeDeck', 'Generate the TubeDeck case')
        on_created = _ChooserCreated()
        cmd_def.commandCreated.add(on_created)
        _handlers.append(on_created)
        cmd_def.execute()
        adsk.autoTerminate(False)   # keep the script alive until the dialog closes
    except Exception:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    cmd_def = adsk.core.Application.get().userInterface.commandDefinitions.itemById(CMD_ID)
    if cmd_def:
        cmd_def.deleteMe()
