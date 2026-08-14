"""Bộ lọc tĩnh (Layer 1) - nhận diện từ khóa vi phạm tiếng Việt.

Sử dụng khớp từ khóa có ranh giới từ (lookaround) thay vì substring thuần
để tránh báo lỗi nhầm, ví dụ: "dm" không còn khớp bên trong từ "admin".
"""

import re
from collections.abc import Mapping

#: Từ điển từ khóa vi phạm, nhóm theo danh mục.
VIOLATION_KEYWORDS: Mapping[str, list[str]] = {
    "insult": [
        "địt", "dit", "địt mẹ", "địt má", "dịt", "con cặc", "cặc", "cak", "lồn", "lon",
        "vãi lồn", "vãi l", "đm", "dm", "dmm", "dcm", "clm", "đclm", "vcl", "vl",
        "đmẹ", "dme", "súc vật", "con đĩ", "thằng chó", "cặn bã", "ngu dốt", "đồ chó",
        "óc chó", "thằng lồn", "con điếm",
    ],
    "political_insult": [
        "lăng mạ", "lăng mạ lãnh đạo", "xúc phạm lãnh đạo", "chống phá nhà nước",
        "phản động", "xúc phạm bác", "xúc phạm anh hùng", "xuyên tạc lịch sử",
        "đu càng", "ba sọc", "3 sọc",
    ],
    "violence": [
        "giết", "đâm", "chém", "đập phá", "bom", "khủng bố", "súng đạn", "cắt cổ",
    ],
    "doxxing": ["cccd", "cmnd", "địa chỉ nhà", "số điện thoại của"],
    "spam": [
        "nhấp vào link", "kiếm tiền tại nhà", "nổ hũ", "đăng ký ngay để nhận",
        "tài xỉu", "lô đề",
    ],
    "pornography": [
        "phim heo", "lộ clip", "ảnh nóng", "18+", "thủ dâm", "phim jav", "xvideos",
    ],
}

#: Điểm phạt theo danh mục (càng nghiêm trọng điểm càng cao).
CATEGORY_SCORES: Mapping[str, int] = {
    "violence": 90,
    "doxxing": 90,
    "pornography": 90,
    "political_insult": 90,
    "insult": 85,
    "spam": 60,
}

# Ranh giới từ: không khớp nếu từ khóa nằm giữa các ký tự chữ/số
# (vd: "dm" không khớp trong "admin", "dit" không khớp trong "edit").
_WORD_BOUNDARY = r"(?<!\w){}(?!\w)"


def _compile_patterns(keywords: list[str]) -> list[tuple[str, re.Pattern[str]]]:
    """Biên dịch danh sách từ khóa thành các regex đã compile sẵn (tối ưu tốc độ)."""
    return [(word, re.compile(_WORD_BOUNDARY.format(re.escape(word)), re.UNICODE))
            for word in keywords]


_COMPILED_KEYWORDS: list[tuple[str, str, re.Pattern[str]]] = [
    (category, word, pattern)
    for category, keywords in VIOLATION_KEYWORDS.items()
    for word, pattern in _compile_patterns(keywords)
]


def analyze_rules(text: str) -> tuple[int, str, str]:
    """Quét văn bản tiếng Việt dựa trên bộ từ khóa.

    Args:
        text: Văn bản cần kiểm tra (có dấu hoặc không dấu).

    Returns:
        Tuple (severity, category, excerpt):
            - severity: điểm vi phạm nặng nhất tìm thấy (0-100).
            - category: danh mục của vi phạm nặng nhất ("none" nếu an toàn).
            - excerpt: đoạn trích quanh từ khóa vi phạm làm bằng chứng.
    """
    text_lower = text.lower()
    max_severity = 0
    detected_category = "none"
    excerpt = ""

    for category, word, pattern in _COMPILED_KEYWORDS:
        match = pattern.search(text_lower)
        if match:
            score = CATEGORY_SCORES.get(category, 20)
            # Chỉ cập nhật khi tìm thấy vi phạm nặng hơn (nếu câu có nhiều lỗi)
            if score > max_severity:
                max_severity = score
                detected_category = category

                # Cắt đoạn văn bản quanh vị trí vi phạm (trước/sau 15 ký tự)
                start = max(0, match.start() - 15)
                end = min(len(text), match.end() + 15)
                excerpt = f"...{text[start:end]}..."

    return max_severity, detected_category, excerpt
