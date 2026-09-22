from build123d import *

def gen_step():
    # Parameters (mm)
    total_length = 10.0
    total_width = 5.0
    body_h = 1.2
    terminal_ext = 1.25
    terminal_overlap = 0.5
    cap_h = 1.5
    fillet_r = 0.2

    body_l = total_length - 2 * terminal_ext
    cap_l = terminal_ext + terminal_overlap
    cap_center_x = body_l / 2 + (terminal_ext - terminal_overlap) / 2
    cap_z_offset = (cap_h - body_h) / 2

    # Ceramic body with filleted edges
    with BuildPart() as bp:
        Box(body_l, total_width, body_h)
        fillet(bp.edges().filter_by(Axis.Z), fillet_r)
    body = bp.part
    body.label = "ceramic_body"

    # Metal end caps
    with BuildPart() as bp:
        Box(cap_l, total_width, cap_h)
    cap_template = bp.part

    left_cap = Pos(X=-cap_center_x, Z=cap_z_offset) * cap_template
    left_cap.label = "left_terminal"

    right_cap = Pos(X=cap_center_x, Z=cap_z_offset) * cap_template
    right_cap.label = "right_terminal"

    # Top marking pad (resistance value indicator)
    with BuildPart() as bp:
        Box(4.0, 3.0, 0.05)
    marking = Pos(Z=body_h / 2 + 0.03) * bp.part
    marking.label = "top_marking"

    # Assembly
    resistor = Compound(
        label="resistor_10x5mm",
        children=[body, left_cap, right_cap, marking],
    )
    return resistor