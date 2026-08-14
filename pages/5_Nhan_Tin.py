"""Nhắn tin riêng giữa hai bạn bè (chat 1-1 qua Google Sheets backend)."""

from datetime import datetime

import streamlit as st

from src.api_client import post_action
from src.auth import get_username, require_login

st.set_page_config(page_title="Nhắn Tin", page_icon="💬", layout="centered")

require_login()

# Phải chọn người nhận từ trang Kết Bạn trước khi vào đây
if "chat_with" not in st.session_state:
    st.warning("Vui lòng chọn một người bạn để bắt đầu trò chuyện.")
    st.page_link("pages/4_Ket_Ban.py", label="Quay lại trang Kết Bạn", icon="⬅️")
    st.stop()

friend_name = st.session_state.chat_with
current_user = get_username()

if st.button("⬅️ Quay lại trang Kết bạn"):
    st.switch_page("pages/4_Ket_Ban.py")

st.title(f"💬 Trò chuyện với {friend_name}")
st.divider()

# ==========================================
# 1. LẤY LỊCH SỬ TIN NHẮN
# ==========================================
res = post_action("get_messages", user1=current_user, user2=friend_name)
chat_history = (res or {}).get("messages", [])

# ==========================================
# 2. HIỂN THỊ TIN NHẮN
# ==========================================
for msg in chat_history:
    role = "user" if msg.get("sender") == current_user else "assistant"
    with st.chat_message(role):
        st.write(msg.get("content", ""))
        # Bật dòng dưới nếu muốn hiển thị thời gian gửi
        # st.caption(f"🕒 {msg.get('timestamp', '')}")

# ==========================================
# 3. Ô NHẬP TIN NHẮN MỚI
# ==========================================
if prompt := st.chat_input(f"Nhắn tin cho {friend_name}..."):
    with st.chat_message("user"):
        st.write(prompt)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post_action(
        "send_message",
        sender=current_user,
        receiver=friend_name,
        content=prompt,
        timestamp=timestamp,
    )
    st.rerun()
