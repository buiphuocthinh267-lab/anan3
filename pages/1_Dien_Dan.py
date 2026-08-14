"""Diễn đàn thảo luận học sinh - tích hợp kiểm duyệt nội dung tự động.

Mỗi bài đăng và bình luận đều được chấm điểm bởi bộ lọc tĩnh
(`src.static_filter`) trước khi lưu lên Google Sheets.
"""

import streamlit as st

from src.api_client import api_configured, clear_cache, fetch_posts, post_action
from src.auth import get_fullname, require_login
from src.static_filter import score_text

st.set_page_config(page_title="Diễn Đàn Học Sinh", page_icon="💬", layout="wide")

# Cổng bảo vệ: bắt buộc đăng nhập
require_login()

#: Danh sách chuyên mục môn học của diễn đàn.
DANH_SACH_MON = [
    "Toán học", "Ngữ văn", "Tiếng Anh", "Khoa học Tự nhiên",
    "Lịch sử & Địa lý", "GDCD", "Khác",
]

# ==========================================
# 1. GIAO DIỆN CHUNG & SIDEBAR
# ==========================================
st.title("💬 Diễn Đàn Thảo Luận Học Sinh")
st.caption("Nơi trao đổi bài học an toàn - Tích hợp bộ lọc tiếng Việt đa lớp")
st.page_link("app.py", label="🏠 Quay về Trang Chủ")
st.divider()

with st.sidebar:
    st.header("⚙️ Cài đặt")
    if st.button("🔄 Tải lại dữ liệu mới"):
        clear_cache()
        st.rerun()

if not api_configured():
    st.warning(
        "⚙️ Chưa cấu hình backend Google Sheets. Xem `.streamlit/secrets.example.toml`."
    )
    st.stop()

# ==========================================
# 2. KHU VỰC ĐĂNG BÀI MỚI
# ==========================================
st.subheader("✍️ Đăng bài thảo luận mới")

col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("📚 Chọn môn học:", DANH_SACH_MON)
with col2:
    content = st.text_area(
        "📝 Nội dung thảo luận:", placeholder="Nhập câu hỏi hoặc ý kiến của bạn..."
    )

if st.button("🚀 Đăng bài ngay", type="primary"):
    if not content.strip():
        st.warning("Vui lòng nhập nội dung bài viết trước khi đăng!")
    else:
        # Chấm điểm kiểm duyệt trước khi đăng
        result = score_text(content)
        score = result["score"]

        if score == 0:
            allowed = True
            st.success(f"✅ Bài viết đạt chuẩn kiểm duyệt - môn {subject}!")
        elif score <= 30:
            allowed = True
            st.warning(
                f"⚠️ Bài viết đã đăng nhưng cần lưu ý: "
                f"{result['recommended_action']} (Điểm: {score}/100)"
            )
        else:
            allowed = False
            st.error(
                f"🚨 Bài viết bị chặn! {result['recommended_action']} "
                f"(Điểm vi phạm: {score}/100)"
            )
            st.write("**Hệ thống phát hiện các từ ngữ sau:**")
            st.json(result["details"])

        if allowed:
            with st.spinner("⚡ Đang tải bài viết lên diễn đàn..."):
                res = post_action(
                    "add_post", subject=subject, content=content, refresh_cache=True
                )
            if res and res.get("status") == "success":
                st.success("✅ Đã đăng bài thành công!")
                st.rerun()

st.divider()

# ==========================================
# 3. BẢNG TIN HIỂN THỊ BÀI VIẾT (THEO TAB)
# ==========================================
st.subheader("📌 Bảng Tin Học Tập")
posts = fetch_posts()

tab_names = ["Tất cả"] + DANH_SACH_MON
tabs = st.tabs(tab_names)

for tab_idx, tab in enumerate(tabs):
    with tab:
        tab_name = tab_names[tab_idx]

        # Phân loại bài viết theo chuyên mục của tab
        if tab_name == "Tất cả":
            visible_posts = posts
        else:
            visible_posts = [p for p in posts if p.get("subject", "Khác") == tab_name]

        if not visible_posts:
            st.info(f"📭 Chưa có bài đăng nào trong chuyên mục {tab_name}.")
        else:
            for post_idx, post in enumerate(visible_posts):
                with st.container():
                    st.markdown(f"### 📘 {post.get('subject', 'Không có tiêu đề')}")
                    st.write(post.get("content", ""))

                    # Hiển thị bình luận hiện có
                    comments = post.get("comments", [])
                    if comments:
                        st.caption("💬 Bình luận:")
                        for comment in comments:
                            st.info(comment)

                    # Khung nhập bình luận
                    with st.expander("📝 Viết câu trả lời"):
                        # Key duy nhất cho từng widget để tránh trùng lặp
                        safe_key = f"comment_{post.get('id', 'blank')}_{post_idx}_{tab_idx}"

                        reply = st.text_input("Viết bình luận...", key=f"input_{safe_key}")
                        if st.button("Gửi bình luận", key=f"btn_{safe_key}"):
                            if reply.strip():
                                # Bình luận cũng được kiểm duyệt trước khi gửi
                                check = score_text(reply)
                                if check["score"] > 70:
                                    st.error(
                                        "🚨 Bình luận chứa từ ngữ không phù hợp "
                                        "nên đã bị chặn!"
                                    )
                                else:
                                    author = get_fullname()
                                    labeled_reply = f"👤 **{author}**: {reply.strip()}"
                                    with st.spinner("Đang gửi..."):
                                        res = post_action(
                                            "add_comment",
                                            post_id=post.get("id"),
                                            comment=labeled_reply,
                                            refresh_cache=True,
                                        )
                                    if res and res.get("status") == "success":
                                        st.toast("✅ Đã gửi câu trả lời!")
                                        st.rerun()
                            else:
                                st.warning("Vui lòng nhập nội dung bình luận!")

                st.divider()
