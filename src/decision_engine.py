"""Động cơ ra quyết định - đổi điểm vi phạm thành hành động xử phạt."""


def determine_action(severity: int, category: str, strikes: int = 0) -> str:
    """Quyết định hành động xử phạt cuối cùng.

    Args:
        severity: Điểm vi phạm 0-100 từ các lớp kiểm duyệt.
        category: Danh mục vi phạm (vd: spam, pornography, insult...).
        strikes: Số lần vi phạm trước đó của người dùng (mỗi lần +15 điểm).

    Returns:
        Một trong: allow | review | warn | remove | ban_temp | ban_perm.
    """
    # Cộng dồn điểm nếu học sinh đã có tiền sử vi phạm
    adjusted_severity = min(100, severity + strikes * 15)

    if adjusted_severity < 20:
        return "allow"
    if adjusted_severity < 40:
        return "review"
    if adjusted_severity < 60:
        # Spam/whenêu dâm bị xóa ngay, danh mục khác chỉ nhắc nhở
        return "remove" if category in ("spam", "pornography") else "warn"
    if adjusted_severity < 80:
        return "ban_temp"
    return "ban_perm"


def determine_label(action: str) -> str:
    """Đổi hành động thành nhãn dễ hiển thị trên giao diện."""
    if action == "allow":
        return "SAFE"
    if action == "review":
        return "SUSPICIOUS"
    return "VIOLATION"
