# -*- coding: utf-8 -*-
"""
UK-style electrical terminal block / junction block
"""
from build123d import *
import math

# -- Parameters --
body_len = 50.0      # total length (along X)
body_wid = 42.0      # total width (along Y)
body_hgt = 45.0      # total height (along Z)
wall_thk = 3.0       # wall thickness
screw_dia = 4.0      # M4 terminal screw clearance
wire_hole_dia = 3.5  # wire entry hole
screw_spacing = 20.0 # spacing between terminals

def gen_step():
    """Generate a UK-style electrical terminal block."""
    with BuildPart() as p:
        # -- Main body --
        Box(body_len, body_wid, body_hgt)
        p.part.label = "terminal_block_body"

        # -- Terminal screws on top (3 terminals) --
        num_terminals = 3
        for i in range(num_terminals):
            sx = (i - (num_terminals - 1) / 2) * screw_spacing
            with Locations((sx, 0, body_hgt)):
                Cylinder(screw_dia / 2, wall_thk * 3, mode=Mode.SUBTRACT)

        # -- Wire entry holes front face --
        for i in range(num_terminals):
            sx = (i - (num_terminals - 1) / 2) * screw_spacing
            with Locations((sx, -body_wid / 2, body_hgt * 0.55)):
                Cylinder(wire_hole_dia / 2, wall_thk,
                         rotation=(0, 90, 0), mode=Mode.SUBTRACT)

        # -- Wire entry holes back face --
        for i in range(num_terminals):
            sx = (i - (num_terminals - 1) / 2) * screw_spacing
            with Locations((sx, body_wid / 2, body_hgt * 0.55)):
                Cylinder(wire_hole_dia / 2, wall_thk,
                         rotation=(0, 90, 0), mode=Mode.SUBTRACT)

        # -- Internal conductor channel (subtract) --
        with Locations((0, 0, body_hgt * 0.3)):
            Box(body_len - wall_thk * 4, body_wid + 1, body_hgt * 0.25, mode=Mode.SUBTRACT)

        # -- Mounting holes in base --
        mount_offset = body_len * 0.35
        for mx in (-mount_offset, mount_offset):
            with Locations((mx, 0, 0)):
                Cylinder(3.5 / 2, body_hgt, mode=Mode.SUBTRACT)

        # -- Bottom cutout / DIN rail slot --
        with Locations((0, 0, 0)):
            Box(body_len * 0.7, body_wid * 0.35, wall_thk * 1.5, mode=Mode.SUBTRACT)

        p.part.label = "terminal_block"
    return p.part

def gen_dxf():
    """Multi-view drawing: top + front + side."""
    import ezdxf
    doc = ezdxf.new()
    msp = doc.modelspace()

    spacing = 100.0
    top_origin = (0, 0)
    front_origin = (0, -spacing)
    side_origin = (spacing, -spacing)

    num_terms = 3
    hl = body_len / 2
    hw = body_wid / 2
    hh = body_hgt

    # ----- TOP VIEW -----
    ox, oy = top_origin
    # Body outline
    msp.add_lwpolyline([
        (ox - hl, oy - hw), (ox + hl, oy - hw),
        (ox + hl, oy + hw), (ox - hl, oy + hw)
    ], close=True)
    # Screw holes (top)
    for i in range(num_terms):
        sx = ox + (i - (num_terms - 1) / 2) * screw_spacing
        msp.add_circle((sx, oy), screw_dia / 2)
    # Wire holes (front/back edges)
    for i in range(num_terms):
        sx = ox + (i - (num_terms - 1) / 2) * screw_spacing
        msp.add_circle((sx, oy - hw), wire_hole_dia / 2,
                       dxfattribs={"linetype": "DASHED"})
        msp.add_circle((sx, oy + hw), wire_hole_dia / 2,
                       dxfattribs={"linetype": "DASHED"})
    # Mounting holes
    mo = body_len * 0.35
    msp.add_circle((ox - mo, oy), 3.5 / 2)
    msp.add_circle((ox + mo, oy), 3.5 / 2)

    # ----- FRONT VIEW -----
    ox, oy = front_origin
    msp.add_lwpolyline([
        (ox - hl, oy), (ox + hl, oy),
        (ox + hl, oy + hh), (ox - hl, oy + hh)
    ], close=True)
    # Screw center lines
    for i in range(num_terms):
        sx = ox + (i - (num_terms - 1) / 2) * screw_spacing
        msp.add_line((sx, oy), (sx, oy + hh),
                     dxfattribs={"linetype": "CENTER"})
    # Wire holes (front face)
    for i in range(num_terms):
        sx = ox + (i - (num_terms - 1) / 2) * screw_spacing
        msp.add_circle((sx, oy + hh * 0.55), wire_hole_dia / 2,
                       dxfattribs={"linetype": "DASHED"})
    # DIN rail slot
    slot_d = wall_thk * 1.5
    msp.add_lwpolyline([
        (ox - hl * 0.7, oy), (ox + hl * 0.7, oy),
        (ox + hl * 0.7, oy + slot_d), (ox - hl * 0.7, oy + slot_d)
    ], close=True)
    # Conductor channel (dashed)
    ch_h = body_hgt * 0.25
    ch_y = body_hgt * 0.3
    msp.add_lwpolyline([
        (ox - hl + wall_thk * 2, oy + ch_y),
        (ox + hl - wall_thk * 2, oy + ch_y),
        (ox + hl - wall_thk * 2, oy + ch_y + ch_h),
        (ox - hl + wall_thk * 2, oy + ch_y + ch_h)
    ], close=True, dxfattribs={"linetype": "DASHED"})

    # ----- SIDE VIEW -----
    ox, oy = side_origin
    msp.add_lwpolyline([
        (ox - hw, oy), (ox + hw, oy),
        (ox + hw, oy + hh), (ox - hw, oy + hh)
    ], close=True)
    # Wire holes (side view shows them head-on)
    msp.add_circle((ox, oy + hh * 0.55), wire_hole_dia / 2)
    # Screw position
    msp.add_line((ox, oy + hh - wall_thk * 1.5), (ox, oy + hh),
                 dxfattribs={"linetype": "CENTER"})
    # DIN slot (side)
    msp.add_line((ox - body_wid * 0.35 / 2, oy),
                 (ox - body_wid * 0.35 / 2, oy + slot_d))
    msp.add_line((ox + body_wid * 0.35 / 2, oy),
                 (ox + body_wid * 0.35 / 2, oy + slot_d))

    return doc