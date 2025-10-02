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
WIN_SCORE = 1000  # Score needed to win flight mission

OBSTACLE_TYPES = {
    "meteor": {"size": 20, "speed": 25, "color": "red", "damage": 20},
    "satellite": {"size": 50, "speed": 10, "color": "gray", "damage": 30}
}

# ===== SESSION STATE INIT =====
if "points" not in st.session_state:
    st.session_state.points = 0
    st.session_state.upgrades = {"armor": 0, "maneuver": 0, "laser": 0}
if "scene" not in st.session_state:
    st.session_state.scene = "menu"

# ===== MENU =====
st.sidebar.title("🌌 TrashSpace Menu")
st.sidebar.write(f"💰 Total Points: **{st.session_state.points}**")
st.sidebar.write("---")
choice = st.sidebar.radio("Chọn giao diện", ["🏠 Menu chính", "🚀 Lái tàu", "🔫 Thu thập rác", "🛠️ Nâng cấp tàu"])

st.session_state.scene = choice

# Display current upgrades in sidebar
st.sidebar.write("---")
st.sidebar.write("**🎯 Nâng cấp hiện tại:**")
st.sidebar.write(f"🛡️ Giáp: {st.session_state.upgrades['armor']}")
st.sidebar.write(f"🎮 Điều hướng: {st.session_state.upgrades['maneuver']}")
st.sidebar.write(f"🔫 Laser: {st.session_state.upgrades['laser']}")

# ===== SCENE: MENU =====
if st.session_state.scene == "🏠 Menu chính":
    st.title("🌌 TrashSpace")
    st.write("### Welcome to the ultimate space cleanup game!")
    
    st.write("---")
    st.write("### 📖 Cách chơi:")
    st.write("**🚀 Lái tàu:** Né chướng ngại vật để bay đến Sao Hỏa. Đạt 1000 điểm để thắng!")
    st.write("**🔫 Thu thập rác:** Sử dụng tọa độ để bắn laser và dọn rác vũ trụ.")
    st.write("**🛠️ Nâng cấp:** Dùng điểm kiếm được để nâng cấp tàu của bạn.")
    
    st.write("---")
    st.write("### 🎮 Điều khiển Lái tàu:")
    st.write("- ⬅️➡️: Di chuyển tàu sang trái/phải")
    st.write("- ⏫ Boost: Tăng tốc độ game (nguy hiểm hơn!)")
    st.write("- ⏬ Slow: Giảm tốc độ game (dễ hơn!)")
    st.write("- ⏹ Stop: Dừng game")
    
    st.write("---")
    st.info("👉 Chọn nhiệm vụ từ sidebar bên trái để bắt đầu!")

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
        st.session_state.game_won = False
        st.session_state.hit_obstacles = set()  # Track hit obstacles to prevent double damage

    # Clamp ship position
    st.session_state.ship_x = max(0, min(CANVAS_WIDTH - SHIP_SIZE, st.session_state.ship_x))

    # Controls
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️ Left"):
            movement = 20 + st.session_state.upgrades["maneuver"] * 3
            st.session_state.ship_x -= movement
            st.rerun()
    with col2:
        if st.button("➡️ Right"):
            movement = 20 + st.session_state.upgrades["maneuver"] * 3
            st.session_state.ship_x += movement
            st.rerun()
    with col3:
        if st.button("⏫ Boost"):
            st.session_state.speed_factor = 2
            st.rerun()
    with col4:
        if st.button("⏬ Slow"):
            st.session_state.speed_factor = 0.5
            st.rerun()
    with col5:
        if st.button("⏹ Stop"):
            st.session_state.running = False
            st.rerun()

    if st.button("🚀 Start/Reset Game"):
        st.session_state.running = True
        st.session_state.hp = 100 + st.session_state.upgrades["armor"] * 20
        st.session_state.score_flight = 0
        st.session_state.obstacles = []
        st.session_state.ship_x = CANVAS_WIDTH // 2
        st.session_state.game_won = False
        st.session_state.hit_obstacles = set()
        st.rerun()

    # Display stats
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("❤️ HP", st.session_state.hp)
    with col_stat2:
        st.metric("⭐ Score", st.session_state.score_flight)
    with col_stat3:
        st.metric("🎯 Target", WIN_SCORE)

    placeholder = st.empty()

    # Game logic
    if st.session_state.running and not st.session_state.game_won:
        # Spawn obstacles
        if random.random() < 0.15:
            o_type = random.choice(list(OBSTACLE_TYPES.keys()))
            spec = OBSTACLE_TYPES[o_type]
            new_obstacle = {
                "x": random.randint(0, CANVAS_WIDTH - spec["size"]),
                "y": 0,
                "type": o_type,
                "id": time.time()  # Unique ID for each obstacle
            }
            st.session_state.obstacles.append(new_obstacle)

        # Move obstacles
        new_obs = []
        for obs in st.session_state.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            obs["y"] += int(spec["speed"] * st.session_state.speed_factor)
            if obs["y"] < CANVAS_HEIGHT:
                new_obs.append(obs)
            else:
                # Remove from hit tracking when off screen
                st.session_state.hit_obstacles.discard(obs["id"])
        st.session_state.obstacles = new_obs

        # Collision detection (only once per obstacle)
        for obs in st.session_state.obstacles:
            if obs["id"] not in st.session_state.hit_obstacles:
                spec = OBSTACLE_TYPES[obs["type"]]
                ship_center_x = st.session_state.ship_x + SHIP_SIZE // 2
                ship_center_y = st.session_state.ship_y + SHIP_SIZE // 2
                obs_center_x = obs["x"] + spec["size"] // 2
                obs_center_y = obs["y"] + spec["size"] // 2
                
                # Better collision detection
                if (abs(ship_center_x - obs_center_x) < (SHIP_SIZE + spec["size"]) // 2 and
                    abs(ship_center_y - obs_center_y) < (SHIP_SIZE + spec["size"]) // 2):
                    st.session_state.hp -= spec["damage"]
                    st.session_state.hit_obstacles.add(obs["id"])  # Mark as hit
                    
                    if st.session_state.hp <= 0:
                        st.session_state.running = False

        # Update score
        st.session_state.score_flight += 1

        # Check win condition
        if st.session_state.score_flight >= WIN_SCORE:
            st.session_state.game_won = True
            st.session_state.running = False
            reward = 50 + st.session_state.hp // 2  # Bonus for remaining HP
            st.session_state.points += reward

        # Draw game
        img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "black")
        draw = ImageDraw.Draw(img)
        
        # Draw ship
        draw.rectangle([st.session_state.ship_x, st.session_state.ship_y,
                        st.session_state.ship_x + SHIP_SIZE, st.session_state.ship_y + SHIP_SIZE],
                       fill="blue", outline="cyan")

        # Draw obstacles
        for obs in st.session_state.obstacles:
            spec = OBSTACLE_TYPES[obs["type"]]
            draw.ellipse([obs["x"], obs["y"], obs["x"] + spec["size"], obs["y"] + spec["size"]],
                         fill=spec["color"], outline="white")

        placeholder.image(img, use_container_width=True)

        # Auto-rerun for animation
        time.sleep(0.05)
        st.rerun()

    # Game over / won messages
    if not st.session_state.running and st.session_state.score_flight > 0:
        if st.session_state.game_won:
            st.success(f"🎉 Chiến thắng! Bạn đã đến Sao Hỏa! Nhận {50 + st.session_state.hp // 2} điểm!")
        else:
            st.error(f"💥 Game Over! Điểm: {st.session_state.score_flight}")
            reward = st.session_state.score_flight // 10
            st.session_state.points += reward
            st.info(f"Nhận {reward} điểm!")


# ===== SCENE: THU THẬP RÁC =====
elif st.session_state.scene == "🔫 Thu thập rác":
    st.title("🔫 Nhiệm vụ: Thu thập rác bằng laser")
    
    LASER_RADIUS = 5 + st.session_state.upgrades["laser"] * 2

    if "trash" not in st.session_state or st.button("🔄 Reset Mission"):
        st.session_state.trash = np.random.randint(-MAP_SIZE, MAP_SIZE, (NUM_TRASH, 2))
        st.session_state.start_time = time.time()
        st.session_state.score_trash = 0
        st.session_state.shots_fired = 0
        st.session_state.last_target = None
        st.session_state.mission_complete = False

    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Rác còn lại", len(st.session_state.trash))
    with col2:
        st.metric("⭐ Điểm", st.session_state.score_trash)
    with col3:
        st.metric("🔫 Bắn", st.session_state.shots_fired)

    st.write(f"📡 Bán kính laser: **{LASER_RADIUS}** đơn vị")
    st.write("---")

    # Input and fire
    coord_str = st.text_input("Nhập tọa độ (X Y hoặc X,Y):", "", key="laser_input")
    
    col_fire, col_hint = st.columns([1, 2])
    with col_fire:
        fire_button = st.button("🔫 Bắn laser", use_container_width=True)
    with col_hint:
        if len(st.session_state.trash) > 0:
            nearest = st.session_state.trash[0]
            st.info(f"💡 Gợi ý: Rác gần nhất tại ({nearest[0]}, {nearest[1]})")

    if fire_button and coord_str:
        try:
            coord_clean = coord_str.replace(",", " ")
            x_input, y_input = map(int, coord_clean.split())
            
            st.session_state.shots_fired += 1
            hit_indices = []
            
            for i, (tx, ty) in enumerate(st.session_state.trash):
                dist = np.sqrt((x_input - tx) ** 2 + (y_input - ty) ** 2)
                if dist <= LASER_RADIUS:
                    hit_indices.append(i)
            
            if hit_indices:
                st.session_state.score_trash += len(hit_indices) * 5
                st.success(f"✅ Trúng {len(hit_indices)} mảnh rác! +{len(hit_indices) * 5} điểm")
                st.session_state.trash = np.delete(st.session_state.trash, hit_indices, axis=0)
            else:
                st.warning("❌ Trượt!")
            
            st.session_state.last_target = (x_input, y_input)
            
            # Check completion
            if len(st.session_state.trash) == 0 and not st.session_state.mission_complete:
                st.session_state.mission_complete = True
                accuracy = (st.session_state.score_trash // 5) / st.session_state.shots_fired if st.session_state.shots_fired > 0 else 0
                bonus = int(50 * accuracy)
                total_reward = st.session_state.score_trash + bonus
                st.session_state.points += total_reward
                st.balloons()
                st.success(f"🎉 Nhiệm vụ hoàn thành! Độ chính xác: {accuracy:.1%}")
                st.info(f"💰 Tổng điểm nhận: {total_reward} (Điểm cơ bản: {st.session_state.score_trash} + Bonus: {bonus})")
            
            st.rerun()
        except:
            st.error("⚠️ Sai định dạng! Nhập như: '10 20' hoặc '10,20'")

    # Display radar with coordinate axes
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-MAP_SIZE, MAP_SIZE)
    ax.set_ylim(-MAP_SIZE, MAP_SIZE)
    ax.set_facecolor("black")
    ax.set_aspect('equal')

    # Draw origin axes
    ax.axhline(0, color="white", linewidth=1.2, alpha=0.8)
    ax.axvline(0, color="white", linewidth=1.2, alpha=0.8)

    # Ticks and grid
    ax.set_xticks(np.arange(-MAP_SIZE, MAP_SIZE+1, 20))
    ax.set_yticks(np.arange(-MAP_SIZE, MAP_SIZE+1, 20))
    ax.grid(color="gray", linestyle="--", linewidth=0.3, alpha=0.5)
    ax.set_xlabel("X", color="white", fontsize=12)
    ax.set_ylabel("Y", color="white", fontsize=12)
    ax.tick_params(colors="white")

    # Ship at origin
    ax.scatter(0, 0, c="cyan", marker="^", s=200, label="Tàu", edgecolors="white", linewidths=2)

    # Trash
    if len(st.session_state.trash) > 0:
        ax.scatter(st.session_state.trash[:, 0], st.session_state.trash[:, 1],
                   c="lime", marker="o", s=80, label="Rác", edgecolors="white", linewidths=1, alpha=0.8)

    # Last laser shot
    if st.session_state.last_target is not None:
        tx, ty = st.session_state.last_target
        ax.plot([0, tx], [0, ty], "r-", linewidth=2, alpha=0.7, label="Laser shot")
        circle = plt.Circle((tx, ty), LASER_RADIUS, color="red", fill=False, linestyle="--", linewidth=2)
        ax.add_patch(circle)
        ax.scatter(tx, ty, c="red", marker="x", s=100)

    ax.legend(loc="upper right", facecolor="black", edgecolor="white", labelcolor="white")
    ax.set_title("🛰️ Radar Thu Thập Rác", color="white", fontsize=14, fontweight="bold")
    
    st.pyplot(fig)


# ===== SCENE: NÂNG CẤP =====
elif st.session_state.scene == "🛠️ Nâng cấp tàu":
    st.title("🛠️ Trạm Nâng cấp")
    
    st.metric("💰 Điểm hiện có", st.session_state.points)
    st.write("---")

    # Armor upgrade
    st.subheader("🛡️ Giáp tàu")
    st.write(f"Cấp độ hiện tại: **{st.session_state.upgrades['armor']}**")
    st.write(f"Hiệu quả: +{st.session_state.upgrades['armor'] * 20} HP tối đa")
    cost_armor = 20 + st.session_state.upgrades["armor"] * 5
    if st.button(f"⬆️ Nâng cấp giáp ({cost_armor} điểm)"):
        if st.session_state.points >= cost_armor:
            st.session_state.upgrades["armor"] += 1
            st.session_state.points -= cost_armor
            st.success("✅ Nâng cấp thành công!")
            st.rerun()
        else:
            st.error("❌ Không đủ điểm!")

    st.write("---")

    # Maneuver upgrade
    st.subheader("🎮 Khả năng điều hướng")
    st.write(f"Cấp độ hiện tại: **{st.session_state.upgrades['maneuver']}**")
    st.write(f"Hiệu quả: +{st.session_state.upgrades['maneuver'] * 3} tốc độ di chuyển")
    cost_maneuver = 15 + st.session_state.upgrades["maneuver"] * 5
    if st.button(f"⬆️ Nâng cấp điều hướng ({cost_maneuver} điểm)"):
        if st.session_state.points >= cost_maneuver:
            st.session_state.upgrades["maneuver"] += 1
            st.session_state.points -= cost_maneuver
            st.success("✅ Nâng cấp thành công!")
            st.rerun()
        else:
            st.error("❌ Không đủ điểm!")

    st.write("---")

    # Laser upgrade
    st.subheader("🔫 Công nghệ Laser")
    st.write(f"Cấp độ hiện tại: **{st.session_state.upgrades['laser']}**")
    st.write(f"Hiệu quả: +{st.session_state.upgrades['laser'] * 2} bán kính laser")
    cost_laser = 10 + st.session_state.upgrades["laser"] * 5
    if st.button(f"⬆️ Nâng cấp laser ({cost_laser} điểm)"):
        if st.session_state.points >= cost_laser:
            st.session_state.upgrades["laser"] += 1
            st.session_state.points -= cost_laser
            st.success("✅ Nâng cấp thành công!")
            st.rerun()
        else:
            st.error("❌ Không đủ điểm!")

    st.write("---")
    st.info("💡 Mẹo: Hoàn thành nhiệm vụ để kiếm điểm nâng cấp!")