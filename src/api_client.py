"""Client duy nhất gọi backend Google Apps Script (Web App -> Google Sheets).

Trước đây URL và logic gọi API bị lặp lại trong 6 file khác nhau;
giờ toàn bộ tập trung tại đây để sửa một chỗ, dùng mọi nơi.

Backend hoạt động theo mô hình "action":
    POST/GET GSHEETS_URL  với JSON {"action": <tên_hành_động>, ...tham_số}
    và trả về JSON {"status": "success" | "error", ...}.
"""

from typing import Any

import requests
import streamlit as st

from src.config import GSHEETS_URL, POSTS_CACHE_TTL_SECONDS, REQUEST_TIMEOUT_SECONDS


def api_configured() -> bool:
    """Kiểm tra đã cấu hình URL backend hay chưa."""
    return bool(GSHEETS_URL)


def post_action(
    action: str,
    *,
    show_errors: bool = True,
    refresh_cache: bool = False,
    **fields: Any,
) -> dict | None:
    """Gửi một hành động (action) lên backend và trả về JSON đã parse.

    Args:
        action: Tên hành động phía server (vd: "login", "add_post"...).
        show_errors: Hiển thị st.error tự động khi lỗi mạng/JSON (mặc định True).
        refresh_cache: Xóa cache bài viết khi hành động thành công
            (dùng cho các action làm thay đổi dữ liệu như add_post).
        **fields: Các tham số kèm theo của hành động.

    Returns:
        dict dữ liệu backend trả về, hoặc None nếu lỗi kết nối/parse.
    """
    if not api_configured():
        if show_errors:
            st.error(
                "⚙️ Chưa cấu hình backend. Hãy tạo file `.streamlit/secrets.toml` "
                "và điền `GSHEETS_URL` (xem `secrets.example.toml`)."
            )
        return None

    payload = {"action": action, **fields}
    try:
        response = requests.post(GSHEETS_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        try:
            data = response.json()
        except ValueError:
            if show_errors:
                st.error("🚨 Backend không trả về JSON hợp lệ. Kiểm tra lại Web App URL.")
            return None

        if refresh_cache and isinstance(data, dict) and data.get("status") == "success":
            clear_cache()
        return data

    except requests.RequestException as exc:
        if show_errors:
            st.error(f"Lỗi kết nối máy chủ: {exc}")
        return None


@st.cache_data(ttl=POSTS_CACHE_TTL_SECONDS, show_spinner=False)
def fetch_posts() -> list:
    """Lấy danh sách bài viết diễn đàn (GET, có cache ngắn để giảm tải backend)."""
    if not api_configured():
        return []
    try:
        response = requests.get(GSHEETS_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        return response.json() if response.status_code == 200 else []
    except (requests.RequestException, ValueError):
        return []


def clear_cache() -> None:
    """Xóa toàn bộ cache dữ liệu (gọi sau khi ghi dữ liệu mới)."""
    st.cache_data.clear()
