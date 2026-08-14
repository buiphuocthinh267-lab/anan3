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
    "https://script.google.com/macros/s/AKfycbw8B_jWJnuKR26j5WWr2Cf1b3svbdN71mrmdA-jOS29IByxqTdbQw90jwJ7L1qyizXE/exec"
)

ADMIN_PASSWORD: str = _get_secret("ADMIN_PASSWORD", "123456")

#: OpenAI API Key đã được cấu hình trực tiếp theo yêu cầu của bạn
OPENAI_API_KEY: str = _get_secret(
    "OPENAI_API_KEY",
    "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"
)

#: Link script Webchat Botpress lấy từ hệ thống của bạn
BOTPRESS_SCRIPT_URL: str = _get_secret(
    "BOTPRESS_SCRIPT_URL",
    "https://files.bpcontent.cloud/2026/08/14/14/20260814140650-AUGBATH4.js"
)

REQUEST_TIMEOUT_SECONDS: int = 10
POSTS_CACHE_TTL_SECONDS: int = 5
