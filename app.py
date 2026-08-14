"""Điểm vào chính của ứng dụng ANAN - Cổng Học Tập THCS.

Khi CHƯA đăng nhập: hiển thị màn hình Đăng nhập / Đăng ký.
Khi ĐÃ đăng nhập: hiển thị sidebar điều hướng + Trợ lý AI chat (Botpress).

Chạy ứng dụng:  streamlit run app.py  (từ thư mục gốc của dự án)
"""

import streamlit as st
import streamlit.components.v1 as components

from src.api_client import post_action
from src.auth import get_fullname, init_session_state, is_logged_in, login, logout
from src.config import BOTPRESS_SCRIPT_URL

# Cấu hình trang (bắt buộc phải là lệnh Streamlit đầu tiên của app)
st.set_page_config(page_title="EVN by AN,DŨNG - Cổng Học Tập", page_icon="⚡", layout="wide")

# --- CSS giao diện xanh - trắng hiện đại ---
st.markdown(
    """
    <style>
    .stApp { background-color: #F4F6F9; }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background: #1E88E5;
        color: white;
        border: none;
    }
    .stButton > button:hover { background: #1565C0; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

init_session_state()

# ==========================================
# 1. MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ
# ==========================================
if not is_logged_in():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(
            "<h2 style='text-align: center; color: #1E88E5;'>⚡ EVN by AN,DŨNG</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align: center; color: #666;'>"
            "Đăng nhập để trải nghiệm không gian học tập thông minh.</p>",
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])

        with tab1:
            log_user = st.text_input("Tên đăng nhập", key="log_user")
            log_pass = st.text_input("Mật khẩu", type="password", key="log_pass")
            if st.button("🚀 Đăng nhập ngay", use_container_width=True):
                if not log_user or not log_pass:
                    st.warning("Vui lòng điền đủ thông tin!")
                else:
                    res = post_action(
                        "login", username=log_user.strip(), password=log_pass
                    )
                    if res and res.get("status") == "success":
                        login(log_user.strip(), res.get("fullname", log_user))
                        st.success("Đăng nhập thành công!")
                        st.rerun()
                    elif res:
                        st.error(res.get("message", "Sai tài khoản hoặc mật khẩu!"))

        with tab2:
            reg_user = st.text_input("Tên đăng nhập (không dấu)", key="reg_user")
            reg_name = st.text_input("Họ và tên thật", key="reg_name")
            reg_pass = st.text_input("Mật khẩu", type="password", key="reg_pass")
            reg_pass2 = st.text_input("Nhập lại mật khẩu", type="password", key="reg_pass2")
            if st.button("✨ Tạo tài khoản", use_container_width=True):
                if not reg_user or not reg_name or not reg_pass:
                    st.warning("Vui lòng điền đủ thông tin!")
                elif reg_pass != reg_pass2:
                    st.error("Mật khẩu không khớp!")
                else:
                    res = post_action(
                        "register",
                        username=reg_user.strip(),
                        password=reg_pass,
                        fullname=reg_name.strip(),
                    )
                    if res and res.get("status") == "success":
                        st.success("Đăng ký thành công! Hãy chuyển sang tab Đăng nhập.")
                    elif res:
                        st.error(res.get("message", "Lỗi đăng ký!"))

# ==========================================
# 2. KHÔNG GIAN HỌC TẬP (ĐÃ ĐĂNG NHẬP)
# ==========================================
else:
    current_fullname = get_fullname()

    # --- Sidebar điều hướng ---
    with st.sidebar:
        st.markdown(f"### 👋 Chào, **{current_fullname}**")
        st.info("Trạng thái: Hoạt động 🟢")
        st.markdown("---")
        st.markdown("### 🧭 Menu Điều Hướng")
        st.page_link("app.py", label="🏠 Trang Chủ (AI Chat)", icon="⚡")
        st.page_link("pages/0_Tai_Khoan.py", label="👤 Tài Khoản", icon="👤")
        st.page_link("pages/1_Dien_Dan.py", label="💬 Diễn Đàn Thảo Luận", icon="🗣️")
        st.page_link("pages/2_Bang_Xep_Hang.py", label="🏆 Bảng Xếp Hạng", icon="📊")
        st.page_link("pages/3_Gop_Y.py", label="📮 Hòm Thư Góp Ý", icon="📥")
        st.page_link("pages/4_Ket_Ban.py", label="👥 Quản Lý Kết Ban", icon="🤝")
        st.page_link("pages/6_San_Dau.py", label="⚔️ Vào Sàn Đấu Toán Học", icon="🔥")
        st.page_link("pages/7_Kiem_Duyet_Admin.py", label="🛡️ Kiểm Duyệt Admin", icon="🔒")
        # Trang 5_Nhan_Tin vào từ trang Kết Bạn (chọn bạn -> Nhắn tin).
        st.markdown("---")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            logout()
            st.rerun()

    # --- Nội dung Trang chủ: Trợ lý AI chat (Botpress) ---
    st.title("🤖 Trợ Giúp AI & Không Gian Học Tập")
    st.markdown(f"Chào mừng **{current_fullname}** đã đăng nhập thành công!")
    st.markdown("---")
    st.subheader("💬 Trò chuyện trực tiếp với Trợ lý AI:")

    if BOTPRESS_SCRIPT_URL:
        botpress_code = f"""
        <div style="height: 600px; width: 100%; position: relative;
             border-radius: 12px; overflow: hidden;
             box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <script src="https://cdn.botpress.cloud/webchat/v5.0/inject.js"></script>
            <script src="{BOTPRESS_SCRIPT_URL}" defer></script>
        </div>
        """
        components.html(botpress_code, height=630, scrolling=True)
    else:
        st.info(
            "🤖 Chưa cấu hình chat AI. Thêm `BOTPRESS_SCRIPT_URL` vào "
            "`.streamlit/secrets.toml` để bật trợ lý Botpress."
        )
