"""Bộ chấm điểm từ ngữ (thang 0-100) dùng cho bài đăng diễn đàn.

Đây là lớp kiểm duyệt "nhẹ" riêng của diễn đàn: mỗi từ ngữ vi phạm
được phạt theo trọng số, cộng dồn và giới hạn ở 100 điểm, sau đó
quy đổi thành nhãn đánh giá + hành động đề xuất.

Đổi tên từ `bo_loc_tu_ngu.py` sang `static_filter.py` theo quy ước
đặt tên module tiếng Anh, đồng bộ với phần còn lại của `src/`.
"""

import re
from collections.abc import Mapping

#: Từ điển: từ khóa -> điểm phạt mỗi lần xuất hiện.
KEYWORD_PENALTIES: Mapping[str, int] = {
    # Nặng (50 điểm/lần)
    "đm": 50, "địt": 50, "cút": 50, "chó": 50, "ngu": 50, "cặc": 50, "lồn": 50,
    # Trung bình (30 điểm/lần)
    "vcl": 30, "vl": 30, "vãi": 30, "cmn": 30, "đậu xanh": 30, "mẹ bà": 30,
    # Nhẹ (15 điểm/lần)
    "mày": 15, "tao": 15, "thằng": 15, "con kia": 15, "tụi bay": 15,
}

# Ranh giới từ: tránh khớp từ khóa nằm giữa một từ khác (vd "ngu" trong "người").
_WORD_BOUNDARY = r"(?<!\w){}(?!\w)"

_COMPILED_PENALTIES: list[tuple[str, int, re.Pattern[str]]] = [
    (word, penalty, re.compile(_WORD_BOUNDARY.format(re.escape(word)), re.UNICODE))
    for word, penalty in KEYWORD_PENALTIES.items()
]


def score_text(text: str) -> dict:
    """Chấm điểm mức độ vi phạm từ ngữ của một đoạn văn bản.

    Args:
        text: Nội dung cần chấm điểm.

    Returns:
        Dict gồm:
            - score (int): điểm vi phạm 0-100.
            - verdict (str): nhãn đánh giá ("An Toàn", "Cảnh Cáo Nhẹ"...).
            - recommended_action (str): hành động đề xuất.
            - details (dict): từ khóa vi phạm -> mô tả số lần và điểm phạt.
    """
    if not text:
        return {
            "score": 0,
            "verdict": "An Toàn",
            "recommended_action": "Cho phép đăng",
            "details": {},
        }

    total = 0
    details: dict[str, str] = {}
    text_lower = text.lower()

    for word, penalty, pattern in _COMPILED_PENALTIES:
        matches = pattern.findall(text_lower)
        if matches:
            added = len(matches) * penalty
            total += added
            details[word] = f"{len(matches)} lần (Phạt {added}đ)"

    total = min(100, total)

    if total == 0:
        verdict, action = "An Toàn", "Cho phép đăng"
    elif total <= 30:
        verdict, action = "Cảnh Cáo Nhẹ", "Nhắc nhở điều chỉnh ngôn từ"
    elif total <= 70:
        verdict, action = "Vi Phạm Nặng", "Ẩn bài viết, thông báo quản trị"
    else:
        verdict, action = "Rất Độc Hại", "Cấm đăng, khóa tài khoản"

    return {
        "score": total,
        "verdict": verdict,
        "recommended_action": action,
        "details": details,
    }
