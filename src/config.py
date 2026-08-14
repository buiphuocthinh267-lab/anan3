"""Cấu hình tập trung của ứng dụng.

Mọi bí mật (URL backend, API key, mật khẩu admin) được đọc theo thứ tự ưu tiên:
    1. Streamlit secrets - file `.streamlit/secrets.toml` cục bộ
       hoặc Secrets Manager khi deploy lên Streamlit Community Cloud.
    2. Biến môi trường (environment variables) - hữu ích khi chạy CI/Docker.

Nguyên tắc: KHÔNG BAO GIỜ hard-code bí mật trong mã nguồn.
Xem `.streamlit/secrets.example.toml` để biết danh sách các khóa cần thiết.
"""

import os

import streamlit as st


def _get_secret(key: str, default: str = "") -> str:
    """Đọc giá trị cấu hình từ st.secrets, nếu không có thì lấy từ env.

    Hàm bọc try/except để ứng dụng vẫn chạy bình thường khi chưa có
    file secrets.toml (ví dụ trong môi trường CI).
    """
    try:
        if key in st.secrets:
            value = st.secrets[key]
            if value:  # Bỏ qua giá trị rỗng trong secrets
                return str(value).strip()
    except Exception:  # noqa: BLE001 - st.secrets có thể lỗi khi chạy ngoài Streamlit
        pass
    return os.environ.get(key, default).strip()


#: URL Web App của Google Apps Script - backend chính của hệ thống (BẮT BUỘC).
GSHEETS_URL: str = _get_secret("GSHEETS_URL")

#: Mật khẩu bảo vệ các trang quản trị (BẮT BUỘC để dùng trang Admin).
ADMIN_PASSWORD: str = _get_secret("ADMIN_PASSWORD")

#: API key OpenAI cho lớp kiểm duyệt AI (tùy chọn).
OPENAI_API_KEY: str = _get_secret("OPENAI_API_KEY")

#: URL script chat Botpress nhúng ở Trang chủ (tùy chọn).
BOTPRESS_SCRIPT_URL: str = _get_secret("BOTPRESS_SCRIPT_URL")

#: Thời gian chờ (giây) khi gọi API backend.
REQUEST_TIMEOUT_SECONDS: int = 10

#: Thời gian sống của cache danh sách bài viết diễn đàn (giây).
POSTS_CACHE_TTL_SECONDS: int = 5
