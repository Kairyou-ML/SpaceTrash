import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# --- Config game ---
MAP_SIZE = 100  # map 100x100
NUM_TRASH = 15
GAME_TIME = 60  # seconds
LASER_RADIUS = st.sidebar.slider("Bán kính laser (r)", 2, 15, 5)
COOLDOWN = 2  # giây

# --- Session state ---
if "trash" not in st.session_state:
    st.session_state.trash = np.random.randint(-MAP_SIZE, MAP_SIZE, (NUM_TRASH, 2))
    st.session_state.start_time = time.time()
    st.session_state.score = 0
    st.session_state.shots = 0
    st.session_state.hits = 0
    st.session_state.last_shot = 0

# --- UI ---
st.title("🚀 Game thu thập rác bằng laser")
st.write("Tàu luôn ở (0,0). Nhập tọa độ X Y hoặc X,Y để bắn laser.")

# Input tọa độ
coord_str = st.text_input("Nhập tọa độ (X Y hoặc X,Y):", "")

if st.button("🔫 Bắn laser!"):
    now = time.time()
    if now - st.session_state.last_shot < COOLDOWN:
        st.warning("⏳ Laser đang nạp, chờ thêm chút!")
    else:
        try:
            # Chuẩn hóa chuỗi: thay dấu phẩy bằng khoảng trắng
            coord_clean = coord_str.replace(",", " ")
            parts = coord_clean.split()
            if len(parts) != 2:
                raise ValueError("Sai định dạng, hãy nhập X Y hoặc X,Y")

            x_input, y_input = map(int, parts)

            st.session_state.last_shot = now
            st.session_state.shots += 1

            # Kiểm tra trúng rác
            hit_indices = []
            for i, (tx, ty) in enumerate(st.session_state.trash):
                dist = np.sqrt((x_input - tx)**2 + (y_input - ty)**2)
                if dist <= LASER_RADIUS:
                    hit_indices.append(i)

            if hit_indices:
                st.session_state.hits += 1
                st.session_state.score += len(hit_indices)
                st.success(f"🎯 Trúng {len(hit_indices)} mảnh rác!")
                st.session_state.trash = np.delete(st.session_state.trash, hit_indices, axis=0)
            else:
                st.error("💨 Trượt rồi!")

            # Lưu tọa độ bắn cuối để vẽ laser
            st.session_state.last_target = (x_input, y_input)

        except Exception as e:
            st.error(f"⚠️ Lỗi nhập tọa độ: {e}")

# --- Cập nhật di chuyển rác ---
new_positions = []
for (tx, ty) in st.session_state.trash:
    tx += random.choice([-1, 0, 1])
    ty += random.choice([-1, 0, 1])
    tx = np.clip(tx, -MAP_SIZE, MAP_SIZE)
    ty = np.clip(ty, -MAP_SIZE, MAP_SIZE)
    new_positions.append([tx, ty])
st.session_state.trash = np.array(new_positions)

# --- Countdown ---
time_left = GAME_TIME - int(time.time() - st.session_state.start_time)
if time_left <= 0:
    st.error("⏱️ Hết giờ! Phiên thu thập kết thúc.")
else:
    st.info(f"⏳ Thời gian còn lại: {time_left}s")

# --- Radar hiển thị ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-MAP_SIZE, MAP_SIZE)
ax.set_ylim(-MAP_SIZE, MAP_SIZE)
ax.set_facecolor("black")
ax.grid(color="gray", linestyle="--", linewidth=0.5)

# Tàu ở giữa
ax.scatter(0, 0, c="cyan", marker="^", s=150, label="Tàu")

# Vẽ rác
if len(st.session_state.trash) > 0:
    ax.scatter(st.session_state.trash[:, 0], st.session_state.trash[:, 1],
               c="white", marker="o", s=50, label="Rác")

# Vẽ laser nếu vừa bắn
if "last_target" in st.session_state:
    tx, ty = st.session_state.last_target
    if time.time() - st.session_state.last_shot < 1.5:
        ax.plot([0, tx], [0, ty], "r-", linewidth=2)
        circle = plt.Circle((tx, ty), LASER_RADIUS, color="red", fill=False, linestyle="--")
        ax.add_patch(circle)

ax.legend(loc="upper right")
st.pyplot(fig)

# --- Stats ---
st.subheader("📊 Thống kê")
st.write(f"- 🔫 Tổng số lần bắn: {st.session_state.shots}")
st.write(f"- 🎯 Số lần trúng: {st.session_state.hits}")
st.write(f"- 🗑️ Số rác thu được: {st.session_state.score}")
