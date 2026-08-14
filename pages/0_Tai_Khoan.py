"""Trang quản lý tài khoản: xem thông tin phiên hiện tại và đăng xuất.

Việc đăng nhập/đăng ký được thực hiện ở Trang chủ (app.py);
trang này chỉ khả dụng khi đã đăng nhập.
"""

import streamlit as st

from src.auth import get_fullname, get_username, logout, require_login

st.set_page_config(page_title="Tài Khoản", page_icon="👤", layout="centered")

require_login()

st.title("👤 Quản lý Tài Khoản")
st.page_link("app.py", label="🏠 Quay về Trang Chủ")
st.divider()

st.success(f"🎉 Xin chào, **{get_fullname()}**! Bạn đã đăng nhập thành công.")
st.info(
    f"Tài khoản: **{get_username()}**\n\n"
    "Bây giờ bạn có thể vào Diễn đàn để đăng bài và bình luận "
    "bằng tên thật của mình."
)

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Dien_Dan.py", label="💬 Vào Diễn Đàn ngay", icon="👉")
with col2:
    if st.button("🚪 Đăng xuất", use_container_width=True):
        logout()
        st.rerun()
