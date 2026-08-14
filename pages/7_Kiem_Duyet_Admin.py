"""Bảng điều khiển kiểm duyệt (chỉ dành cho Admin).

Công cụ test pipeline kiểm duyệt đa lớp: nhập văn bản, giả lập số lần
vi phạm (strikes), ép dùng AI... và xem kết quả chi tiết trả về.
"""

import hmac

import streamlit as st

from src.auth import require_login
from src.config import ADMIN_PASSWORD, OPENAI_API_KEY
from src.moderation import moderate_content

st.set_page_config(page_title="Admin Kiểm Duyệt", page_icon="🛡️", layout="wide")

require_login()

st.title("🛡️ Bảng Điều Khiển Kiểm Duyệt (Admin)")
st.page_link("app.py", label="🏠 Quay về Trang Chủ", icon="⬅️")
st.divider()

# ==========================================
# Ổ KHÓA BẢO MẬT - CHỈ ADMIN MỚI ĐƯỢC VÀO
# ==========================================
if not ADMIN_PASSWORD:
    st.error(
        "⛔ Chưa cấu hình `ADMIN_PASSWORD` trong `.streamlit/secrets.toml`. "
        "Trang này đang bị khóa."
    )
    st.stop()

password_guess = st.text_input("🔑 Nhập mật khẩu Admin để truy cập:", type="password")

# So sánh không phụ thuộc thời gian để chống tấn công timing
if not hmac.compare_digest(password_guess, ADMIN_PASSWORD):
    st.error("⛔ Bạn không có quyền truy cập trang này. Vui lòng nhập đúng mật khẩu!")
    st.stop()

st.success("✅ Đăng nhập thành công! Chào mừng Admin.")
st.divider()
st.caption("Giao diện UI tách biệt hoàn toàn - Logic kiểm duyệt nằm trong thư mục `src/`")

with st.sidebar:
    st.header("⚙️ Cấu hình hệ thống")
    st.subheader("👤 Giả lập Người dùng")
    user_strikes = st.number_input(
        "Số lần vi phạm trước đó:", min_value=0, max_value=10, value=0
    )
    force_ai = st.checkbox("🤖 Ép dùng AI (Bỏ qua bộ lọc tĩnh)", value=False)
    if not OPENAI_API_KEY:
        st.warning("Chưa cấu hình OPENAI_API_KEY - lớp AI sẽ không hoạt động.")
    st.markdown("---")
    st.page_link("app.py", label="🏠 Về Trang Chủ", icon="⚡")

st.subheader("📝 Nhập bài đăng cần test")
user_input = st.text_area(
    "Nội dung:", height=150, placeholder="Ví dụ: Đăng ký ngay để nhận thưởng, click link..."
)

if st.button("🚀 Chạy Test Hệ Thống", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Vui lòng nhập văn bản!")
    else:
        with st.spinner("Hệ thống đang quét đa lớp..."):
            result = moderate_content(
                text=user_input,
                api_key=OPENAI_API_KEY or None,
                strikes=user_strikes,
                force_ai=force_ai,
            )

        st.divider()
        color = (
            "green" if result.label == "SAFE"
            else "orange" if result.label == "SUSPICIOUS"
            else "red"
        )
        st.markdown(
            f"### 🎯 Kết quả: <span style='color:{color}'>{result.label}</span>",
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Hành động xử lý", result.action.upper())
        c2.metric("Điểm vi phạm", f"{result.severity}/100")
        c3.metric("Phân loại", result.category)
        c4.metric("Engine đã dùng", "AI" if result.used_ai else "Bộ lọc tĩnh")

        with st.container(border=True):
            st.write(f"**Lý do:** {result.reason}")
            if result.excerpt:
                st.write(f"**Đoạn vi phạm:** `{result.excerpt}`")

        st.subheader("📦 Payload JSON (Dữ liệu đầy đủ):")
        st.json(result.model_dump())
