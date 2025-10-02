import streamlit as st
from PIL import Image, ImageDraw
import random
import time

# ===== GAME SETTINGS =====
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
SHIP_SIZE = 40

OBSTACLE_TYPES = {
    "meteor": {"size": 20, "speed": 25, "color": "red", "damage": 20},
    "satellite": {"size": 50, "speed": 10, "color": "gray", "damage": 30}
}

# ===== INIT STATE =====
if "ship_x" not in st.session_state:
    st.session_state.ship_x = CANVAS_WIDTH // 2
    st.session_state.ship_y = CANVAS_HEIGHT - 80
    st.session_state.obstacles = []
    st.session_state.running = False
    st.session_state.hp = 100
    st.session_state.score = 0
    st.session_state.speed_factor = 1

st.title("🚀 TrashSpace Prototype (Streamlit Demo)")

# ===== CONTROL BUTTONS =====
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("⬅️"):
        st.session_state.ship_x -= 20
with col2:
    if st.button("➡️"):
        st.session_state.ship_x += 20
with col3:
    if st.button("⏫ Boost (Space)"):
        st.session_state.speed_factor = 2
with col4:
    if st.button("⏬ Slow (Ctrl)"):
        st.session_state.speed_factor = 0.5
with col5:
    if st.button("⏹ Stop"):
        st.session_state.running = False

# reset speed nếu không bấm boost/slow
if not (st.session_state.speed_factor in [2, 0.5]):
    st.session_state.speed_factor = 1

# ===== START BUTTON =====
if st.button("🚀 Start/Reset Game"):
    st.session_state.running = True
    st.session_state.hp = 100
    st.session_state.score = 0
    st.session_state.obstacles = []
    st.session_state.ship_x = CANVAS_WIDTH // 2

# ===== GAME LOOP =====
placeholder = st.empty()

if st.session_state.running:
    for _ in range(200):  # chạy tạm 200 tick
        # spawn obstacle
        if random.random() < 0.15:
            o_type = random.choice(list(OBSTACLE_TYPES.keys()))
            spec = OBSTACLE_TYPES[o_type]
            st.session_state.obstacles.append(
                {"x": random.randint(0, CANVAS_WIDTH - spec["size"]),
                 "y": 0, "type": o_type}
            )

        # move obstacle
        new_obs = []
        for obs in st.session_state.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            obs["y"] += int(spec["speed"] * st.session_state.speed_factor)
            if obs["y"] < CANVAS_HEIGHT:
                new_obs.append(obs)
        st.session_state.obstacles = new_obs

        # collision check
        for obs in st.session_state.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            if (abs(obs["x"] - st.session_state.ship_x) < SHIP_SIZE and
                abs(obs["y"] - st.session_state.ship_y) < SHIP_SIZE):
                st.session_state.hp -= spec["damage"]
                if st.session_state.hp <= 0:
                    st.session_state.running = False

        st.session_state.score += 1

        # draw
        img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "black")
        draw = ImageDraw.Draw(img)

        draw.rectangle([st.session_state.ship_x, st.session_state.ship_y,
                        st.session_state.ship_x + SHIP_SIZE, st.session_state.ship_y + SHIP_SIZE],
                       fill="blue")

        for obs in st.session_state.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            draw.ellipse([obs["x"], obs["y"], obs["x"] + spec["size"], obs["y"] + spec["size"]],
                         fill=spec["color"])

        placeholder.image(img)
        st.sidebar.write(f"❤️ HP: {st.session_state.hp}")
        st.sidebar.write(f"⭐ Score: {st.session_state.score}")

        if not st.session_state.running or st.session_state.hp <= 0:
            st.error("💥 Game Over!")
            break

        time.sleep(0.2)  # refresh rate ~5 FPS
