"""Luồng kiểm duyệt nội dung đa lớp (điểm vào chính của hệ thống).

Pipeline gồm 2 lớp:
    1. Bộ lọc tĩnh (`rules.analyze_rules`) - nhanh, miễn phí, bắt từ khóa rõ ràng.
    2. Lớp AI (`ai_client.analyze_with_ai`, OpenAI Moderation) - chỉ gọi khi
       kết quả tĩnh còn mơ hồ (0 < severity < 80) hoặc admin ép dùng AI,
       để tiết kiệm chi phí gọi API.

Kết quả cuối cùng được `decision_engine` quy đổi thành hành động xử phạt.
"""

from src.ai_client import analyze_with_ai
from src.decision_engine import determine_action, determine_label
from src.rules import analyze_rules
from src.schemas import ModerationResult


def moderate_content(
    text: str,
    api_key: str | None = None,
    strikes: int = 0,
    force_ai: bool = False,
) -> ModerationResult:
    """Kiểm duyệt một đoạn văn bản qua pipeline đa lớp.

    Args:
        text: Văn bản cần kiểm duyệt.
        api_key: API key OpenAI (None/'' -> chỉ dùng bộ lọc tĩnh).
        strikes: Số lần vi phạm trước đó của người dùng.
        force_ai: Ép gọi lớp AI bất kể kết quả tĩnh (dùng để test).

    Returns:
        ModerationResult chứa nhãn, điểm, danh mục, hành động và lý do.
    """
    used_ai = False

    # 1. Bộ lọc tĩnh
    severity, category, excerpt = analyze_rules(text)
    reason = "Phát hiện từ khóa vi phạm (Hệ thống tự động)."

    # 2. Lớp AI dự phòng - chỉ gọi khi cần
    if api_key and (force_ai or 0 < severity < 80):
        ai_result = analyze_with_ai(text, api_key)
        if ai_result is not None:
            used_ai = True
            severity = ai_result.get("severity", severity)
            category = ai_result.get("category", category)
            reason = ai_result.get("reason", "Phân tích ngữ cảnh bởi AI.")
            excerpt = ai_result.get("excerpt", excerpt)

    # Văn bản sạch và không dùng AI -> ghi nhận là an toàn
    if severity == 0 and not used_ai:
        category = "none"
        reason = "Nội dung an toàn, không chứa từ khóa vi phạm."

    # 3. Ra quyết định cuối cùng
    action = determine_action(severity, category, strikes)
    label = determine_label(action)

    return ModerationResult(
        label=label,
        severity=severity,
        category=category,
        action=action,
        reason=reason,
        excerpt=excerpt,
        used_ai=used_ai,
    )
