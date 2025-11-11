import streamlit as st
import matplotlib.pyplot as plt
import random
import math

st.set_page_config(page_title="Tree Generator", layout="wide")

st.title("🌳 Parametric Tree Generator")

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Structure")
max_depth = st.sidebar.slider("Max depth", 1, 10, 5)
base_length = st.sidebar.slider("Base branch length", 30, 200, 90)
length_decay = st.sidebar.slider("Length decay per depth", 0.4, 0.95, 0.7)
branch_prob = st.sidebar.slider("Probability to branch (per node)", 0.0, 1.0, 0.9)
max_children = st.sidebar.slider("Max children per node", 1, 6, 3)

st.sidebar.header("Angles")
base_angle = st.sidebar.slider("Base angle (deg)", -90, 90, -90)  # -90 = straight up
spread = st.sidebar.slider("Spread (deg)", 0, 120, 40)
angle_jitter = st.sidebar.slider("Random angle jitter (deg)", 0, 50, 10)

st.sidebar.header("Leaves")
leaf_on_end = st.sidebar.checkbox("Draw leaves only on terminal branches", True)
leaf_size = st.sidebar.slider("Leaf size", 3, 40, 14)

st.sidebar.header("Style")
branch_thickness = st.sidebar.slider("Base branch thickness", 1.0, 15.0, 6.0)
branch_decay = st.sidebar.slider("Thickness decay per depth", 0.2, 1.0, 0.6)
palette_name = st.sidebar.selectbox("Palette", ["Warm", "Forest", "Mono"])
bg_color = "#fefae0"
branch_color = "#6d4c41"
leaf_color = "#4CB944"

if palette_name == "Forest":
    bg_color = "#e0f2f1"
    branch_color = "#37474f"
    leaf_color = "#2e7d32"
elif palette_name == "Mono":
    bg_color = "#f8f9fa"
    branch_color = "#212529"
    leaf_color = "#a22c29"
# Warm is default above

# -----------------------------
# Tree generation
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.set_xlim(0, 800)
ax.set_ylim(0, 800)
ax.set_aspect("equal")
ax.axis("off")


def draw_branch(x, y, length, angle_deg, depth, thickness):
    """
    Recursively draw a branch.
    x, y: starting point
    length: length of this segment
    angle_deg: direction in degrees
    depth: current depth
    thickness: current line thickness
    """
    # Convert angle to radians
    angle_rad = math.radians(angle_deg)
    x2 = x + length * math.cos(angle_rad)
    y2 = y + length * math.sin(angle_rad)

    # draw the branch segment
    ax.plot([x, x2], [y, y2], color=branch_color, linewidth=thickness, solid_capstyle="round")

    # If we've reached max depth, draw a leaf (terminal)
    if depth >= max_depth:
        if leaf_on_end:
            leaf = plt.Circle((x2, y2), leaf_size, color=leaf_color, fill=True)
            ax.add_patch(leaf)
        return

    # Decide if this node will branch at all (stochastic rule)
    if random.random() > branch_prob:
        # no children; maybe leaf here
        if leaf_on_end:
            leaf = plt.Circle((x2, y2), leaf_size, color=leaf_color, fill=True)
            ax.add_patch(leaf)
        return

    # number of children this node will try to make
    num_children = random.randint(1, max_children)

    # new length and thickness decay with depth
    new_length = length * length_decay
    new_thickness = max(thickness * branch_decay, 0.5)

    for i in range(num_children):
        # spread children around the main direction
        # e.g. base_angle = -90 (up), spread = 40 → children around -90 ± 20
        # we also add a little random jitter
        offset = (i - (num_children - 1) / 2.0)  # centered
        child_angle = angle_deg + offset * (spread / max(num_children, 1))
        child_angle += random.uniform(-angle_jitter, angle_jitter)

        draw_branch(
            x2,
            y2,
            new_length,
            child_angle,
            depth + 1,
            new_thickness
        )

# -----------------------------
# root call
# -----------------------------
# Start from bottom center, pointing "up" (in our coord system y increases downward,
# so up is angle -90 by default)
draw_branch(400, 60, base_length, base_angle, 1, branch_thickness)

st.pyplot(fig)

st.markdown("""
**How this maps to your p5.js version:**

- Generations → `max_depth`
- Depth-based radius → `length_decay` and `branch_decay`
- Stochastic branching → `branch_prob` + `max_children`
- Leaf-on-end → checkbox
- Angle control → `base_angle`, `spread`, `angle_jitter`
""")
