import streamlit as st
import matplotlib.pyplot as plt
import math
import random

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Tree Generator", layout="centered")

st.title("🌳 Tree Generator (p5-style)")

st.write("Adjust the sliders on the left to change how the tree grows.")

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Tree Settings")

max_depth = st.sidebar.slider("Depth (levels)", min_value=1, max_value=12, value=8)
initial_length = st.sidebar.slider("Initial branch length", 40, 180, 100)
branch_scale = st.sidebar.slider("Branch scale (shrink per level)", 0.4, 0.9, 0.7, step=0.05)
base_angle_deg = st.sidebar.slider("Base angle (degrees)", 5, 60, 25)
randomness = st.sidebar.slider("Random angle jitter", 0.0, 25.0, 6.0, step=0.5)
seed = st.sidebar.number_input("Random seed", min_value=0, value=0, step=1)

random.seed(seed)

# ---------------------------------------------------------
# TREE DRAWING LOGIC
# ---------------------------------------------------------
def draw_branch(ax, x, y, length, angle, depth):
    """Recursive branch drawing, p5.js-style."""
    if depth == 0 or length < 2:
        return

    # end point of this branch
    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    # line thickness gets thinner as we go up
    linewidth = max(1.0, depth * 0.4)

    ax.plot([x, x2], [y, y2], linewidth=linewidth)

    # next branch length
    next_length = length * branch_scale

    # add some jitter to the angle
    jitter = random.uniform(-randomness, randomness)

    # left branch
    draw_branch(
        ax,
        x2,
        y2,
        next_length,
        angle - base_angle_deg + jitter,
        depth - 1,
    )

    # right branch
    draw_branch(
        ax,
        x2,
        y2,
        next_length,
        angle + base_angle_deg + jitter,
        depth - 1,
    )


# ---------------------------------------------------------
# MATPLOTLIB FIGURE
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 7))

# draw from bottom-center upwards
start_x = 0
start_y = 0
draw_branch(ax, start_x, start_y, initial_length, 90, max_depth)

# styling: hide axes
ax.set_aspect("equal")
ax.axis("off")

# set view box so tree is centered
ax.set_xlim(-initial_length * 1.2, initial_length * 1.2)
ax.set_ylim(0, initial_length * 2.2)

st.pyplot(fig)
