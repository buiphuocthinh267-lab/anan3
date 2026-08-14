"""Quản lý kết bạn: tìm bạn, gửi/chấp nhận lời mời, danh sách bạn bè."""

import streamlit as st

from src.api_client import post_action
from src.auth import get_username, require_login

st.set_page_config(page_title="Quản Lý Kết Bạn", page_icon="👥", layout="wide")

require_login()

current_user = get_username()

st.title("👥 Kết Nối & Quản Lý Bạn Bè")
st.markdown("Tìm kiếm bạn học, gửi lời mời kết bạn và mở rộng vòng kết nối học tập của bạn.")
st.divider()


def get_friend_data() -> dict:
    """Lấy lời mời kết bạn chờ duyệt + danh sách bạn bè của người dùng hiện tại."""
    res = post_action("get_friends", username=current_user, show_errors=False)
    if res and res.get("status") == "success":
        return res
    return {"status": "error", "pending": [], "friends": []}


col1, col2 = st.columns([1, 1])

# ==========================================
# CỘT TRÁI: TÌM BẠN + LỜI MỜI CHỜ
# ==========================================
with col1:
    st.subheader("🔍 Tìm kiếm bạn bè")
    search_user = st.text_input("Nhập tên đăng nhập (Username) của bạn bè:")

    if st.button("Gửi lời mời kết bạn", type="primary", use_container_width=True):
        if not search_user.strip():
            st.warning("Vui lòng nhập tên tài khoản cần tìm!")
        elif search_user.strip() == current_user:
            st.error("Bạn không thể tự kết bạn với chính mình!")
        else:
            with st.spinner("Đang gửi lời mời..."):
                res = post_action(
                    "send_friend_request",
                    sender=current_user,
                    receiver=search_user.strip(),
                )
            if res and res.get("status") == "success":
                st.success("✅ Đã gửi lời mời kết bạn thành công!")
                st.rerun()
            elif res:
                st.error(res.get("message", "Không thể gửi lời mời."))

    st.markdown("---")
    st.subheader("📥 Lời mời kết bạn đang chờ")

    friend_data = get_friend_data()
    pending_list = friend_data.get("pending", [])

    if not pending_list:
        st.info("Chưa có lời mời kết bạn nào mới.")
    else:
        for request in pending_list:
            request_id = request.get("id")
            sender_name = request.get("sender")

            with st.container(border=True):
                st.write(f"👤 **{sender_name}** muốn kết bạn với bạn.")
                if st.button("✅ Chấp nhận", key=f"accept_{request_id}"):
                    with st.spinner("Đang xử lý..."):
                        res = post_action("accept_friend", request_id=request_id)
                    if res and res.get("status") == "success":
                        st.success("Đã đồng ý kết bạn!")
                        st.rerun()
                    elif res:
                        st.error(res.get("message"))

# ==========================================
# CỘT PHẢI: DANH SÁCH BẠN BÈ
# ==========================================
with col2:
    st.subheader("🤝 Danh sách bạn bè của bạn")

    friends_list = friend_data.get("friends", [])
    if not friends_list:
        st.info("Bạn chưa có người bạn nào trong danh sách.")
    else:
        for friend in friends_list:
            friend_name = friend.get("friend")
            with st.container(border=True):
                name_col, chat_col = st.columns([3, 1])

                with name_col:
                    st.write(f"👤 **{friend_name}** (Bạn bè)")

                with chat_col:
                    if st.button("💬 Nhắn", key=f"chat_{friend_name}"):
                        st.session_state.chat_with = friend_name
                        st.switch_page("pages/5_Nhan_Tin.py")

st.markdown("---")
st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
