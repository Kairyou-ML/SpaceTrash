import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random
import time

# ===== CONFIG =====
MAP_SIZE = 100
NUM_TRASH = 15
GAME_TIME = 60
SHIP_SIZE = 40

OBSTACLE_TYPES = {
    "meteor": {"size": 20, "speed": 25, "color": "red", "damage": 20},
    "satellite": {"size": 50, "speed": 10, "color": "gray", "damage": 30}
}

# ===== SESSION STATE INIT =====
if "points" not in st.session_state:
    st.session_state.points = 0  # điểm tích lũy dùng để nâng cấp
    st.session_state.upgrades = {"armor": 0, "maneuver": 0, "laser": 0}
if "scene" not in st.session_state:
    st.session_state.scene = "menu"

# ===== MENU =====
st.sidebar.title("🌌 TrashSpace Menu")
choice = st.sidebar.radio("Chọn giao diện", ["🏠 Menu chính", "🚀 Lái tàu", "🔫 Thu thập rác", "🛠️ Nâng cấp tàu"])

st.session_state.scene = choice

# ===== SCENE: MENU =====
if st.session_state.scene == "🏠 Menu chính":
    st.title("🌌 TrashSpace")
    st.write("Welcome to the game!")
    st.write("👉 Pick mission on sidebar to start.")

# ===== SCENE: LÁI TÀU =====
elif st.session_state.scene == "🚀 Lái tàu":
    st.title("🚀 Nhiệm vụ: Bay tới Sao Hỏa")

    CANVAS_WIDTH, CANVAS_HEIGHT = 400, 600

    # init state
    if "ship_x" not in st.session_state:
        st.session_state.ship_x = CANVAS_WIDTH // 2
        st.session_state.ship_y = CANVAS_HEIGHT - 80
        st.session_state.obstacles = []
        st.session_state.running = False
        st.session_state.hp = 100 + st.session_state.upgrades["armor"] * 20
        st.session_state.score_flight = 0
        st.session_state.speed_factor = 1

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️"):
            st.session_state.ship_x -= 20 - st.session_state.upgrades["maneuver"] * 2
    with col2:
        if st.button("➡️"):
            st.session_state.ship_x += 20 + st.session_state.upgrades["maneuver"] * 2
    with col3:
        if st.button("⏫ Boost"):
            st.session_state.speed_factor = 2
    with col4:
        if st.button("⏬ Slow"):
            st.session_state.speed_factor = 0.5
    with col5:
        if st.button("⏹ Stop"):
            st.session_state.running = False

    if st.button("🚀 Start/Reset Game"):
        st.session_state.running = True
        st.session_state.hp = 100 + st.session_state.upgrades["armor"] * 20
        st.session_state.score_flight = 0
        st.session_state.obstacles = []
        st.session_state.ship_x = CANVAS_WIDTH // 2

    placeholder = st.empty()

    if st.session_state.running:
        for _ in range(150):
            if random.random() < 0.15:
                o_type = random.choice(list(OBSTACLE_TYPES.keys()))
                spec = OBSTACLE_TYPES[o_type]
                st.session_state.obstacles.append(
                    {"x": random.randint(0, CANVAS_WIDTH - spec["size"]),
                     "y": 0, "type": o_type}
                )

            # move
            new_obs = []
            for obs in st.session_state.obstacles:
                spec = OBSTACLE_TYPES[obs["type"]]
                obs["y"] += int(spec["speed"] * st.session_state.speed_factor)
                if obs["y"] < CANVAS_HEIGHT:
                    new_obs.append(obs)
            st.session_state.obstacles = new_obs

            # collision
            for obs in st.session_state.obstacles:
                spec = OBSTACLE_TYPES[obs["type"]]
                if (abs(obs["x"] - st.session_state.ship_x) < SHIP_SIZE and
                    abs(obs["y"] - st.session_state.ship_y) < SHIP_SIZE):
                    st.session_state.hp -= spec["damage"]
                    if st.session_state.hp <= 0:
                        st.session_state.running = False

            st.session_state.score_flight += 1

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
            st.sidebar.write(f"⭐ Điểm chuyến bay: {st.session_state.score_flight}")

            if not st.session_state.running or st.session_state.hp <= 0:
                st.error("💥 Game Over!")
                st.session_state.points += st.session_state.score_flight // 10
                break

            time.sleep(0.2)


# ===== SCENE: THU THẬP RÁC =====
elif st.session_state.scene == "🔫 Thu thập rác":
    st.title("🔫 Nhiệm vụ: Thu thập rác bằng laser")
    LASER_RADIUS = 5 + st.session_state.upgrades["laser"]

    if "trash" not in st.session_state:
        st.session_state.trash = np.random.randint(-MAP_SIZE, MAP_SIZE, (NUM_TRASH, 2))
        st.session_state.start_time = time.time()
        st.session_state.score_trash = 0

    coord_str = st.text_input("Nhập tọa độ (X Y hoặc X,Y):", "")
    if st.button("Bắn laser"):
        try:
            coord_clean = coord_str.replace(",", " ")
            x_input, y_input = map(int, coord_clean.split())
            hit_indices = []
            for i, (tx, ty) in enumerate(st.session_state.trash):
                dist = np.sqrt((x_input - tx) ** 2 + (y_input - ty) ** 2)
                if dist <= LASER_RADIUS:
                    hit_indices.append(i)
            if hit_indices:
                st.session_state.score_trash += len(hit_indices)
                st.success(f"Trúng {len(hit_indices)} mảnh rác!")
                st.session_state.trash = np.delete(st.session_state.trash, hit_indices, axis=0)
            else:
                st.warning("Trượt!")
            st.session_state.last_target = (x_input, y_input)
        except:
            st.error("Sai định dạng tọa độ!")

    # hiển thị radar với trục tọa độ
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-MAP_SIZE, MAP_SIZE)
    ax.set_ylim(-MAP_SIZE, MAP_SIZE)
    ax.set_facecolor("black")

    # vẽ trục gốc
    ax.axhline(0, color="white", linewidth=0.8)
    ax.axvline(0, color="white", linewidth=0.8)

    # ticks theo bước 10
    ax.set_xticks(np.arange(-MAP_SIZE, MAP_SIZE+1, 10))
    ax.set_yticks(np.arange(-MAP_SIZE, MAP_SIZE+1, 10))
    ax.grid(color="white", linestyle="--", linewidth=0.3, alpha=0.4)

    # tàu
    ax.scatter(0, 0, c="cyan", marker="^", s=150, label="Tàu")

    # rác
    if len(st.session_state.trash) > 0:
        ax.scatter(st.session_state.trash[:, 0], st.session_state.trash[:, 1],
                   c="white", marker="o", s=50, label="Rác")

    # laser
    if "last_target" in st.session_state:
        tx, ty = st.session_state.last_target
        ax.plot([0, tx], [0, ty], "r-", linewidth=2)
        circle = plt.Circle((tx, ty), LASER_RADIUS, color="red", fill=False, linestyle="--")
        ax.add_patch(circle)

    ax.legend()
    st.pyplot(fig)

    st.write(f"Điểm rác: {st.session_state.score_trash}")
    st.session_state.points += st.session_state.score_trash // 5


# ===== SCENE: NÂNG CẤP =====
elif st.session_state.scene == "🛠️ Nâng cấp tàu":
    st.title("🛠️ Nâng cấp tàu")
    st.write(f"Điểm hiện có: {st.session_state.points}")

    if st.button("Tăng giáp (20 điểm)"):
        if st.session_state.points >= 20:
            st.session_state.upgrades["armor"] += 1
            st.session_state.points -= 20
    if st.button("Tăng khả năng điều hướng (15 điểm)"):
        if st.session_state.points >= 15:
            st.session_state.upgrades["maneuver"] += 1
            st.session_state.points -= 15
    if st.button("Nâng cấp laser (10 điểm)"):
        if st.session_state.points >= 10:
            st.session_state.upgrades["laser"] += 1
            st.session_state.points -= 10

    st.write("🎯 Trạng thái nâng cấp hiện tại:")
    st.json(st.session_state.upgrades)
