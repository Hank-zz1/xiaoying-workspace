# -*- coding: utf-8 -*-
"""
Test part: mounting bracket with 4 holes
ZWCAD-compatible DXF output
"""
from build123d import *

# -- Parameters --
width = 100.0  # mm
depth = 60.0   # mm
thickness = 8.0
hole_dia = 5.5  # M5 clearance
hole_offset = 10.0  # from each corner

def gen_step():
    """Generate a mounting bracket with 4 corner holes."""
    with BuildPart() as p:
        # Base plate
        Box(width, depth, thickness)
        # 4 corner through-holes
        hw = width / 2 - hole_offset
        hd = depth / 2 - hole_offset
        for x in (-hw, hw):
            for y in (-hd, hd):
                with Locations((x, y, 0)):
                    Hole(hole_dia / 2, thickness)
        p.part.label = "mounting_bracket"
    return p.part

def gen_dxf():
    """Export top-down projection as DXF."""
    import ezdxf
    doc = ezdxf.new()
    msp = doc.modelspace()
    # Outer rectangle (top view)
    hw = width / 2
    hd = depth / 2
    msp.add_lwpolyline([
        (-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)
    ], close=True)
    # 4 holes as circles
    hh = hole_offset
    for cx in (-(hw - hh), (hw - hh)):
        for cy in (-(hd - hh), (hd - hh)):
            msp.add_circle((cx, cy), hole_dia / 2)
    return doc