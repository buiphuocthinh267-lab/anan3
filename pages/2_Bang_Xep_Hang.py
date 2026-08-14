"""Bảng xếp hạng (Bảng Vàng) - vinh danh các cao thủ toán học."""

import pandas as pd
import streamlit as st

from src.api_client import post_action
from src.auth import require_login

st.set_page_config(page_title="Bảng Xếp Hạng", page_icon="🏆")

require_login()

st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
st.markdown("---")

st.title("🏆 BẢNG VÀNG VINH DANH")
st.markdown("Nơi tụ hội của những cao thủ Toán học đỉnh nhất trường!")
st.markdown("---")


def get_rank_info(score: int) -> tuple[str, str]:
    """Quy đổi tổng điểm thành danh hiệu rank kèm icon."""
    if score <= 100:
        return "Tân binh", "🥉"
    if score <= 300:
        return "Học giả", "🥈"
    if score <= 600:
        return "Tinh anh", "🥇"
    return "Thách đấu", "💎"


# Lấy dữ liệu xếp hạng từ backend
with st.spinner("Đang tải dữ liệu Bảng xếp hạng..."):
    response = post_action("get_leaderboard")

if response is None:
    st.stop()

if response.get("status") != "success":
    st.error(f"Lỗi hệ thống: {response.get('message')}")
    st.stop()

leaderboard_data = response.get("data", [])
if not leaderboard_data:
    st.info("Chưa có cao thủ nào ghi danh trên bảng xếp hạng!")
    st.stop()

# --- TOP 3 CAO THỦ ---
st.subheader("🌟 TOP 3 CAO THỦ XUẤT SẮC NHẤT 🌟")
top3_cols = st.columns(3)

for i in range(min(3, len(leaderboard_data))):
    player = leaderboard_data[i]
    rank_name, rank_icon = get_rank_info(player["score"])
    medal = ["🥇 TOP 1", "🥈 TOP 2", "🥉 TOP 3"][i]

    with top3_cols[i]:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 15px; border-radius: 10px;
                        background-color: #262730; border: 1px solid #4CAF50;'>
                <h3 style='color: #FFD700;'>{medal}</h3>
                <h4>{player['fullname']}</h4>
                <h2 style='color: #4CAF50;'>{player['score']} đ</h2>
                <p style='font-size: 18px;'>{rank_icon} {rank_name}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
st.write("")

# --- DANH SÁCH TOÀN BỘ ---
st.subheader("📜 Danh sách anh tài")

table_data = []
for idx, player in enumerate(leaderboard_data):
    rank_name, rank_icon = get_rank_info(player["score"])
    table_data.append(
        {
            "Hạng": f"#{idx + 1}",
            "Họ và Tên": player["fullname"],
            "Điểm số": player["score"],
            "Danh hiệu": f"{rank_icon} {rank_name}",
        }
    )

st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
