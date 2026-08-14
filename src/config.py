"""Cấu hình tập trung của ứng dụng."""

import os
import streamlit as st


def _get_secret(key: str, default: str = "") -> str:
    try:
        if key in st.secrets:
            value = st.secrets[key]
            if value:
                return str(value).strip()
    except Exception:
        pass
    return os.environ.get(key, default).strip()


#: URL Web App của Google Apps Script - backend chính
GSHEETS_URL: str = _get_secret(
    "GSHEETS_URL",
    "https://script.google.com/macros/s/AKfycbw8B_jWJnuKR26j5WWr2Cflb3svbdN71mrmdA-jOS29IByxqTdbQw9OjwJ7LlqyizXE/exec",
)

ADMIN_PASSWORD: str = _get_secret("ADMIN_PASSWORD")
OPENAI_API_KEY: str = _get_secret("OPENAI_API_KEY")
BOTPRESS_SCRIPT_URL: str = _get_secret("BOTPRESS_SCRIPT_URL")
REQUEST_TIMEOUT_SECONDS: int = 10
POSTS_CACHE_TTL_SECONDS: int = 5
