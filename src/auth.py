"""Quản lý phiên đăng nhập (session state) và cổng bảo vệ các trang con.

Trước đây khối kiểm tra "đã đăng nhập chưa?" bị copy-paste vào đầu
mỗi trang; giờ chỉ cần gọi `require_login()` một dòng.
"""

import streamlit as st


def init_session_state() -> None:
    """Khởi tạo các khóa session state mặc định (idempotent - gọi nhiều lần vô hại)."""
    defaults: dict = {"logged_in": False, "username": "", "fullname": ""}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def is_logged_in() -> bool:
    """Trạng thái đăng nhập của phiên hiện tại."""
    return bool(st.session_state.get("logged_in", False))


def get_username() -> str:
    """Tên đăng nhập của người dùng hiện tại ('' nếu chưa đăng nhập)."""
    return st.session_state.get("username", "")


def get_fullname() -> str:
    """Họ tên hiển thị của người dùng hiện tại."""
    return st.session_state.get("fullname", "Thành viên")


def login(username: str, fullname: str) -> None:
    """Lưu thông tin người dùng vào phiên sau khi xác thực thành công."""
    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["fullname"] = fullname


def logout() -> None:
    """Xóa toàn bộ thông tin phiên, đưa người dùng về màn hình đăng nhập."""
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["fullname"] = ""
    st.session_state.pop("chat_with", None)  # Xóa luôn người đang chat nếu có


def require_login() -> None:
    """Cổng bảo vệ trang: nếu chưa đăng nhập thì báo lỗi và dừng trang (st.stop()).

    Cách dùng ở đầu mỗi trang con:
        require_login()
    """
    if not is_logged_in():
        st.error(
            "⚠️ Bạn chưa đăng nhập! Vui lòng quay lại trang chính để đăng nhập "
            "trước khi sử dụng tính năng này."
        )
        st.page_link("app.py", label="🔑 Quay lại Trang chủ để Đăng nhập", icon="👉")
        st.stop()
