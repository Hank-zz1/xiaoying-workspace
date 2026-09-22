# -*- coding: utf-8 -*-
"""
Circular flange with central bore and bolt-hole pattern
Multi-view DXF: top + front + section
"""
from build123d import *
import math

# -- Parameters --
outer_dia = 120.0       # mm
bore_dia = 40.0         # central bore
thickness = 12.0
bolt_count = 8
bolt_circle_dia = 90.0
bolt_hole_dia = 9.0

def gen_step():
    """Generate a circular flange with bolt holes."""
    with BuildPart() as p:
        Cylinder(outer_dia / 2, thickness)
        Cylinder(bore_dia / 2, thickness, mode=Mode.SUBTRACT)
        r = bolt_circle_dia / 2
        for i in range(bolt_count):
            angle = math.radians(i * 360.0 / bolt_count)
            cx = r * math.cos(angle)
            cy = r * math.sin(angle)
            with Locations((cx, cy, 0)):
                Hole(bolt_hole_dia / 2, thickness)
        p.part.label = "flange"
    return p.part

def gen_dxf():
    """Multi-view drawing: top view + front view + section."""
    import ezdxf

    doc = ezdxf.new()
    msp = doc.modelspace()

    # -- Layout positions --
    spacing = 160.0
    top_origin = (0, 0)
    front_origin = (0, -spacing)
    section_origin = (spacing, -spacing)

    r_outer = outer_dia / 2
    r_bore = bore_dia / 2
    r_bc = bolt_circle_dia / 2
    r_hole = bolt_hole_dia / 2

    # ===== TOP VIEW =====  (top_origin)
    ox, oy = top_origin
    msp.add_circle((ox, oy), r_outer)
    msp.add_circle((ox, oy), r_bore)
    # Bolt circle center line
    msp.add_circle((ox, oy), r_bc, dxfattribs={"linetype": "CENTER"})
    # Bolt holes
    for i in range(bolt_count):
        angle = math.radians(i * 360.0 / bolt_count)
        cx = ox + r_bc * math.cos(angle)
        cy = oy + r_bc * math.sin(angle)
        msp.add_circle((cx, cy), r_hole)

    # ===== FRONT VIEW =====  (front_origin)
    ox, oy = front_origin
    # Outer rectangle
    msp.add_lwpolyline([
        (ox - r_outer, oy), (ox + r_outer, oy),
        (ox + r_outer, oy + thickness), (ox - r_outer, oy + thickness)
    ], close=True)
    # Central bore (dashed)
    msp.add_line((ox - r_bore, oy), (ox - r_bore, oy + thickness),
                 dxfattribs={"linetype": "DASHED"})
    msp.add_line((ox + r_bore, oy), (ox + r_bore, oy + thickness),
                 dxfattribs={"linetype": "DASHED"})
    # Bolt holes (hidden)
    msp.add_line((ox - r_bc, oy), (ox - r_bc, oy + thickness),
                 dxfattribs={"linetype": "DASHED"})
    msp.add_line((ox + r_bc, oy), (ox + r_bc, oy + thickness),
                 dxfattribs={"linetype": "DASHED"})

    # ===== SECTION A-A =====  (section_origin)
    ox, oy = section_origin
    # Top flange (outer segment)
    msp.add_lwpolyline([
        (ox - r_outer, oy), (ox - r_bc, oy),
        (ox - r_bc, oy + thickness), (ox - r_outer, oy + thickness)
    ], close=True)
    # Bottom flange (outer segment)
    msp.add_lwpolyline([
        (ox + r_bc, oy), (ox + r_outer, oy),
        (ox + r_outer, oy + thickness), (ox + r_bc, oy + thickness)
    ], close=True)
    # Bolt hole cutout section (left)
    msp.add_lwpolyline([
        (ox - r_bc - r_hole, oy), (ox - r_bc + r_hole, oy),
        (ox - r_bc + r_hole, oy + thickness), (ox - r_bc - r_hole, oy + thickness)
    ], close=True)
    # Bolt hole cutout section (right)
    msp.add_lwpolyline([
        (ox + r_bc - r_hole, oy), (ox + r_bc + r_hole, oy),
        (ox + r_bc + r_hole, oy + thickness), (ox + r_bc - r_hole, oy + thickness)
    ], close=True)
    # Center bore section
    msp.add_lwpolyline([
        (ox - r_bore, oy), (ox + r_bore, oy),
        (ox + r_bore, oy + thickness), (ox - r_bore, oy + thickness)
    ], close=True)
    # Hatch the section (simple 45 degree lines)
    hatch_step = 3
    for hx_start in [ox - r_outer, ox - r_bc + r_hole, ox + r_bc - r_hole]:
        hx_end = ox + r_outer
        h = 0
        while h <= int(thickness):
            hy = oy + h
            msp.add_line((hx_start, hy), (min(hx_start + 10, hx_end), min(hy + 10, oy + thickness)))
            h += hatch_step

    return doc