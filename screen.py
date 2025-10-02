import streamlit as st

# --- Session State Init ---
if "screen" not in st.session_state:
    st.session_state.screen = "menu"
if "score" not in st.session_state:
    st.session_state.score = 0
if "materials" not in st.session_state:
    st.session_state.materials = 0
if "upgrades" not in st.session_state:
    st.session_state.upgrades = {
        "armor": 0,
        "engine": 0,
        "control": 0,
        "weapon": 0
    }

# --- Navigation ---
def goto(screen):
    st.session_state.screen = screen

# --- MENU SCREEN ---
if st.session_state.screen == "menu":
    st.title("🚀 Space Mission Game")
    st.write(f"⭐ Điểm tích lũy: {st.session_state.score}")
    st.write(f"🛰️ Nguyên liệu rác: {st.session_state.materials}")
    st.write("Chọn chế độ:")

    st.button("🚀 Lái tàu", on_click=lambda: goto("flight"))
    st.button("🛰️ Thu thập rác", on_click=lambda: goto("collect"))
    st.button("⚙️ Nâng cấp tàu", on_click=lambda: goto("upgrade"))

# --- FLIGHT SCREEN ---
elif st.session_state.screen == "flight":
    st.title("🚀 Lái tàu tới Sao Hỏa")
    st.write("👉 Đây sẽ là gameplay điều khiển tàu (dùng phím hoặc click).")
    # giả lập điểm nhận được
    if st.button("✅ Thành công (demo)"):
        st.session_state.score += 50
        st.success("Hoàn thành chuyến bay, +50 điểm!")
        goto("menu")
    if st.button("❌ Thất bại (demo)"):
        st.error("Tàu hỏng, cần thu thập rác để tái chế!")
        goto("collect")
    st.button("⬅️ Về Menu", on_click=lambda: goto("menu"))

# --- COLLECT SCREEN ---
elif st.session_state.screen == "collect":
    st.title("🛰️ Thu thập rác bằng laser")
    st.write("👉 Đây là gameplay bắn laser để thu rác (dùng code prototype trước).")
    if st.button("✅ Giả lập thu được 5 nguyên liệu"):
        st.session_state.materials += 5
        st.success("Thu thập thành công, +5 nguyên liệu!")
        goto("menu")
    st.button("⬅️ Về Menu", on_click=lambda: goto("menu"))

# --- UPGRADE SCREEN ---
elif st.session_state.screen == "upgrade":
    st.title("⚙️ Nâng cấp tàu vũ trụ")
    st.write(f"⭐ Điểm: {st.session_state.score} | 🛰️ Nguyên liệu: {st.session_state.materials}")
    st.write("Chọn nâng cấp:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"🛡️ Giáp (Lv.{st.session_state.upgrades['armor']}) - 20 điểm"):
            if st.session_state.score >= 20:
                st.session_state.score -= 20
                st.session_state.upgrades["armor"] += 1
                st.success("Đã nâng cấp Giáp!")
            else:
                st.error("Không đủ điểm!")
        if st.button(f"⚡ Điều khiển (Lv.{st.session_state.upgrades['control']}) - 15 điểm"):
            if st.session_state.score >= 15:
                st.session_state.score -= 15
                st.session_state.upgrades["control"] += 1
                st.success("Đã nâng cấp Điều khiển!")
            else:
                st.error("Không đủ điểm!")

    with col2:
        if st.button(f"🔥 Động cơ (Lv.{st.session_state.upgrades['engine']}) - 25 điểm"):
            if st.session_state.score >= 25:
                st.session_state.score -= 25
                st.session_state.upgrades["engine"] += 1
                st.success("Đã nâng cấp Động cơ!")
            else:
                st.error("Không đủ điểm!")
        if st.button(f"🎯 Vũ khí (Lv.{st.session_state.upgrades['weapon']}) - 10 nguyên liệu"):
            if st.session_state.materials >= 10:
                st.session_state.materials -= 10
                st.session_state.upgrades["weapon"] += 1
                st.success("Đã nâng cấp Vũ khí!")
            else:
                st.error("Không đủ nguyên liệu!")

    st.button("⬅️ Về Menu", on_click=lambda: goto("menu"))
