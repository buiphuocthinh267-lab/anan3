"""Hòm thư góp ý & báo lỗi.

Phần 1: Học sinh gửi góp ý (lưu vào file `data/danh_sach_gop_y.txt`).
Phần 2: Quản trị viên xem hòm thư (bảo vệ bằng mật khẩu từ secrets).

Lưu ý: lưu file phù hợp khi self-host có ổ đĩa cố định; nếu deploy lên
Streamlit Community Cloud (ổ đĩa tạm), dữ liệu sẽ mất khi restart -
xem "Known Limitations" trong README.
"""

import hmac
from datetime import datetime
from pathlib import Path

import streamlit as st

from src.auth import require_login
from src.config import ADMIN_PASSWORD

st.set_page_config(page_title="Hòm Thư Góp Ý", page_icon="📮", layout="centered")

require_login()

st.title("📮 Hòm Thư Góp Ý & Báo Lỗi")
st.markdown("Mọi ý kiến đóng góp của bạn sẽ được gửi trực tiếp và bảo mật với quản trị viên.")
st.divider()

#: File lưu trữ góp ý trên server.
FEEDBACK_FILE = Path("data") / "danh_sach_gop_y.txt"

# ==========================================
# PHẦN 1: NGƯỜI DÙNG GỬI GÓP Ý
# ==========================================
with st.form("form_gop_y"):
    st.write(f"📝 Góp ý với tên: **{st.session_state.get('fullname', 'Người dùng')}**")

    feedback = st.text_area(
        "Nhập nội dung góp ý hoặc báo lỗi:",
        placeholder="Ví dụ: Trang web chạy rất mượt, thầy/cô bổ sung thêm...",
    )

    submitted = st.form_submit_button(
        "🚀 Gửi Góp Ý Ngay", type="primary", use_container_width=True
    )

    if submitted:
        if not feedback.strip():
            st.warning("Vui lòng nhập nội dung trước khi gửi!")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sender = st.session_state.get("fullname", "Ẩn danh")
            entry = (
                f"[{timestamp}] Người gửi: {sender}\n"
                f"Nội dung: {feedback.strip()}\n" + "-" * 40 + "\n"
            )
            try:
                FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
                with FEEDBACK_FILE.open("a", encoding="utf-8") as f:
                    f.write(entry)
                st.success("🎉 Cảm ơn bạn! Góp ý của bạn đã được gửi thành công đến quản trị viên.")
            except OSError as exc:
                st.error(f"Có lỗi xảy ra khi lưu góp ý: {exc}")

st.divider()

# ==========================================
# PHẦN 2: KHU VỰC QUẢN TRỊ VIÊN (MẬT KHẨU)
# ==========================================
with st.expander("🔒 Dành cho Quản trị viên (Xem hòm thư)"):
    if not ADMIN_PASSWORD:
        st.warning(
            "🔒 Chưa cấu hình mật khẩu admin (`ADMIN_PASSWORD` trong "
            "`.streamlit/secrets.toml`). Khu vực này đang bị khóa."
        )
    else:
        admin_input = st.text_input(
            "Nhập mật khẩu quản trị viên để xem góp ý:", type="password"
        )

        # So sánh không phụ thuộc thời gian để chống tấn công timing
        if hmac.compare_digest(admin_input, ADMIN_PASSWORD):
            st.success("🔓 Đăng nhập quyền quản trị thành công!")

            if FEEDBACK_FILE.exists():
                inbox = FEEDBACK_FILE.read_text(encoding="utf-8")
                if inbox.strip():
                    st.text_area("Hòm thư góp ý hiện tại:", value=inbox, height=350)

                    if st.button("🗑️ Xóa sạch tất cả hòm thư"):
                        FEEDBACK_FILE.write_text("", encoding="utf-8")
                        st.success("Đã dọn sạch hòm thư!")
                        st.rerun()
                else:
                    st.info("Hòm thư hiện đang trống, chưa có ai góp ý.")
            else:
                st.info("Chưa có file dữ liệu góp ý nào được tạo.")
        elif admin_input:
            st.error("❌ Sai mật khẩu quản trị viên!")

st.divider()
st.page_link("app.py", label="🏠 Quay về Trang chủ", icon="⬅️")
