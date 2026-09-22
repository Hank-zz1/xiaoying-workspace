"""
Female Pin Header Connector - Dual Row 2x5, 2.54mm pitch.
Body: black thermoplastic, 12.7 x 5.0 x 8.5 mm.
Through-hole pins: 0.5 x 0.5 mm square, 3.3 mm protrusion below PCB face.
"""

from build123d import *

# Parameters
body_length = 12.7  # X
body_width = 5.0    # Y
body_height = 8.5   # Z (above PCB face)
pitch = 2.54
rows = 2
cols = 5

pin_sq = 0.5          # square pin cross-section side
pin_protrusion = 3.3  # below PCB face (Z=0)

socket_opening = 1.0  # square socket hole side
socket_depth = 5.0    # recess depth from top face

chamfer_size = 0.3

# Derived values
x_start = -(cols - 1) * pitch / 2  # -5.08
y_start = -(rows - 1) * pitch / 2  # -1.27

# Build plastic body with chamfered top edges
with BuildPart() as body_builder:
    Box(body_length, body_width, body_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN))
    top_face = body_builder.faces().sort_by(Axis.Z)[-1]
    chamfer(top_face.edges(), chamfer_size)

body = body_builder.part
body.label = "plastic_housing"

# Socket openings (recessed squares on top face)
for row in range(rows):
    for col in range(cols):
        cx = x_start + col * pitch
        cy = y_start + row * pitch
        socket = Box(
            socket_opening, socket_opening, socket_depth,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        )
        socket = Pos(cx, cy, body_height) * socket
        body -= socket

# Metal pins (extending below PCB face)
pins_compound = Compound()
for row in range(rows):
    for col in range(cols):
        cx = x_start + col * pitch
        cy = y_start + row * pitch
        pin = Box(pin_sq, pin_sq, pin_protrusion,
                  align=(Align.CENTER, Align.CENTER, Align.MAX))
        pin = Pos(cx, cy, 0) * pin
        pin.label = f"pin_r{row}_c{col}"
        pins_compound += pin
pins_compound.label = "pins"

# Full model = body + pins
model = Compound(children=[body, pins_compound])
model.label = "female_pin_header_2x5"


def gen_step():
    return model


def gen_dxf():
    """Top view (plan view) of the female pin header -- 2D technical drawing."""
    import ezdxf
    from ezdxf.enums import TextEntityAlignment

    doc = ezdxf.new(setup=True, units=ezdxf.units.MM)
    msp = doc.modelspace()

    # Drawing conventions: draw top view centered at origin
    hlx = body_length / 2   # 6.35
    hly = body_width / 2    # 2.5
    ch = chamfer_size       # 0.3
    socket_sz = 0.7         # socket opening side for drawing

    # -- Body outline with chamfered corners --
    # Outer rectangle corners (before chamfer)
    pts_outer = [
        (-hlx, -hly), ( hlx, -hly), ( hlx,  hly), (-hlx,  hly),
    ]
    # Chamfered polygon: offset inward by ch along each edge
    pts_chamfered = [
        (-hlx + ch, -hly),       # left-bottom
        ( hlx - ch, -hly),       # right-bottom
        ( hlx, -hly + ch),       # bottom-right
        ( hlx,  hly - ch),       # top-right
        ( hlx - ch,  hly),       # right-top
        (-hlx + ch,  hly),       # left-top
        (-hlx,  hly - ch),       # top-left
        (-hlx, -hly + ch),       # bottom-left
    ]
    # Draw as an 8-point polygon (octagon-like) using continuous polyline
    msp.add_lwpolyline(pts_chamfered + [pts_chamfered[0]], dxfattribs={"layer": "0"})

    # -- Socket openings: 0.7mm squares --
    half_s = socket_sz / 2
    for row in range(rows):
        for col in range(cols):
            cx = x_start + col * pitch
            cy = y_start + row * pitch
            sq_pts = [
                (cx - half_s, cy - half_s),
                (cx + half_s, cy - half_s),
                (cx + half_s, cy + half_s),
                (cx - half_s, cy + half_s),
            ]
            msp.add_lwpolyline(sq_pts + [sq_pts[0]], dxfattribs={"layer": "0"})

    # -- Center cross marks --
    cross_len = 1.0
    msp.add_line((-cross_len, 0), (cross_len, 0), dxfattribs={"layer": "CENTER"})
    msp.add_line((0, -cross_len), (0, cross_len), dxfattribs={"layer": "CENTER"})

    # -- Dimension: overall length (12.7mm) --
    dim_y = -hly - 4.0
    msp.add_linear_dim(
        base=(-hlx, dim_y),
        p1=(-hlx, dim_y - 1.5),
        p2=( hlx, dim_y - 1.5),
        dimstyle="EZDXF",
    ).render()

    # -- Dimension: overall width (5.0mm) --
    dim_x = -hlx - 4.0
    msp.add_linear_dim(
        base=(dim_x, -hly),
        p1=(dim_x - 1.5, -hly),
        p2=(dim_x - 1.5,  hly),
        dimstyle="EZDXF",
        angle=90,
    ).render()

    # -- Dimension: pitch (2.54mm) between first two pins --
    pitch_y = -hly - 7.0
    pin0_x = x_start
    pin1_x = x_start + pitch
    msp.add_linear_dim(
        base=(pin0_x, pitch_y),
        p1=(pin0_x, pitch_y - 1.5),
        p2=(pin1_x, pitch_y - 1.5),
        dimstyle="EZDXF",
    ).render()

    # -- Dimension: row pitch (2.54mm) --
    row_dim_x = hlx + 4.0
    msp.add_linear_dim(
        base=(row_dim_x, y_start),
        p1=(row_dim_x + 1.5, y_start),
        p2=(row_dim_x + 1.5, y_start + pitch),
        dimstyle="EZDXF",
        angle=90,
    ).render()

    # -- Label: "Top View" --
    label_y = hly + 3.0
    msp.add_text("TOP VIEW", height=1.5, dxfattribs={"layer": "TEXT"}).set_placement(
        (0, label_y), align=TextEntityAlignment.CENTER
    )
    # Sub-label
    msp.add_text(
        "Female Pin Header 2x5  (2.54mm Pitch)",
        height=1.2,
        dxfattribs={"layer": "TEXT"},
    ).set_placement((0, label_y - 2.0), align=TextEntityAlignment.CENTER)

    # -- Layer setup --
    doc.layers.add("CENTER", color=1, linetype="CENTER")
    doc.layers.add("TEXT", color=7)

    return doc


if __name__ == "__main__":
    gen_step()
    export_step(model, "female_pin_header_2x5.step")