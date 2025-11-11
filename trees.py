import streamlit as st
import matplotlib.pyplot as plt
import math
import random
import time

st.set_page_config(page_title="Tree Generator", layout="centered")
st.title("🌳 Tree Generator (p5-style)")
st.write("Use the sliders, then either **Generate tree** or **Grow tree** to animate it.")

# ---------------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------------
st.sidebar.header("Tree Settings")

max_depth = st.sidebar.slider("Max depth (levels)", min_value=2, max_value=12, value=8)
initial_length = st.sidebar.slider("Initial branch length", 40, 200, 120)
branch_scale = st.sidebar.slider("Branch scale (shrink per level)", 0.4, 0.9, 0.7, step=0.05)
base_angle_deg = st.sidebar.slider("Base angle (degrees)", 5, 60, 25)
randomness = st.sidebar.slider("Random angle jitter", 0.0, 25.0, 6.0, step=0.5)

# keep seed around so animation is consistent
if "tree_seed" not in st.session_state:
    st.session_state.tree_seed = 0

col1, col2 = st.columns(2)
generate_clicked = col1.button("🌱 Generate tree")
grow_clicked = col2.button("🌱➡️🌳 Grow tree")

def draw_branch(ax, x, y, length, angle, depth, current_depth):
    """
    depth = total depth allowed
    current_depth = how far we are rendering in this frame
    we only draw until current_depth!
    """
    if depth == 0 or length < 2:
        return
    if current_depth == 0:
        return

    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    linewidth = max(1.0, depth * 0.5)
    ax.plot([x, x2], [y, y2], linewidth=linewidth, color="black")

    next_length = length * branch_scale
    jitter = random.uniform(-randomness, randomness)

    # left
    draw_branch(
        ax,
        x2,
        y2,
        next_length,
        angle - base_angle_deg + jitter,
        depth - 1,
        current_depth - 1,
    )
    # right
    draw_branch(
        ax,
        x2,
        y2,
        next_length,
        angle + base_angle_deg + jitter,
        depth - 1,
        current_depth - 1,
    )

def make_figure(depth_to_render, seed):
    random.seed(seed)
    fig, ax = plt.subplots(figsize=(5, 7))
    start_x, start_y = 0, 0
    draw_branch(ax, star_
