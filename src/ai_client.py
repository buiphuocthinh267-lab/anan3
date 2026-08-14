"""Lớp kiểm duyệt AI (Layer 2) - gọi OpenAI Moderation API.

Chỉ được gọi khi bộ lọc tĩnh trả kết quả mơ hồ (0 < severity < 80)
hoặc admin ép dùng AI, để tiết kiệm số lần gọi API.
"""

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

_MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"

#: Ánh xạ danh mục vi phạm của OpenAI sang danh mục nội bộ của hệ thống.
_CATEGORY_MAPPING: dict[str, str] = {
    "hate": "hate_speech",
    "hate/threatening": "hate_speech",
    "harassment": "harassment",
    "harassment/threatening": "harassment",
    "self-harm": "violence",
    "sexual": "pornography",
    "sexual/minors": "pornography",
    "violence": "violence",
    "violence/graphic": "violence",
}


def analyze_with_ai(
    text: str,
    api_key: str,
    model_name: str = "omni-moderation-latest",
) -> dict[str, Any] | None:
    """Gửi văn bản tới OpenAI Moderation API và chuẩn hóa kết quả.

    Args:
        text: Văn bản cần phân tích.
        api_key: API key OpenAI (bỏ qua nếu rỗng).
        model_name: Tên model moderation của OpenAI.

    Returns:
        Dict đúng cấu trúc mà `moderation.moderate_content` tiêu thụ:
        {"severity": int, "category": str, "reason": str, "excerpt": str},
        hoặc None nếu không gọi được API.
    """
    if not api_key or not text.strip():
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key.strip()}",
    }
    payload = {"model": model_name, "input": text.strip()}

    try:
        response = requests.post(
            _MODERATION_ENDPOINT, headers=headers, json=payload, timeout=10
        )
        if response.status_code != 200:
            logger.error("[OpenAI Error] Mã lỗi %s - %s", response.status_code, response.text)
            return None

        results = response.json().get("results", [])
        if not results:
            return None

        flagged = results[0].get("flagged", False)
        category_scores = results[0].get("category_scores", {})

        # Tìm danh mục vi phạm có điểm số cao nhất OpenAI trả về
        max_cat = "none"
        max_score = 0.0
        for cat, score in category_scores.items():
            if score > max_score:
                max_score = score
                max_cat = cat

        # Quy đổi điểm OpenAI (0.0-1.0) sang thang hệ thống (0-100)
        severity = int(max_score * 100)
        mapped_category = _CATEGORY_MAPPING.get(max_cat, "insult" if flagged else "none")

        # OpenAI đánh dấu vi phạm nhưng điểm thấp -> nâng lên 60 để đủ khung xử phạt
        if flagged and severity < 60:
            severity = 60

        reason = (
            f"OpenAI Moderation phát hiện vi phạm nhóm: '{max_cat}'"
            if flagged
            else "Nội dung an toàn theo đánh giá của OpenAI."
        )

        return {
            "severity": severity,
            "category": mapped_category,
            "reason": reason,
            "excerpt": text if flagged else "",
        }

    except requests.RequestException as exc:
        logger.error("[OpenAI Client] Lỗi kết nối: %s", exc)
        return None
