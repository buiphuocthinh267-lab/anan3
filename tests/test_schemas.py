"""Kiểm thử model dữ liệu `src.schemas`."""

from src.schemas import ModerationResult


def test_tao_ket_qua_day_du():
    result = ModerationResult(
        label="VIOLATION",
        severity=85,
        category="insult",
        action="warn",
        reason="Phát hiện từ khóa vi phạm",
        excerpt="...đồ chó...",
    )
    assert result.label == "VIOLATION"
    assert result.severity == 85
    assert result.used_ai is False  # giá trị mặc định


def test_model_dump_chua_du_truong():
    result = ModerationResult(
        label="SAFE", severity=0, category="none", action="allow", reason="An toàn"
    )
    data = result.model_dump()
    assert set(data.keys()) == {
        "label", "severity", "category", "action", "reason", "excerpt", "used_ai",
    }
    assert data["excerpt"] == ""
    assert data["used_ai"] is False


def test_bat_loi_khi_thieu_truong_bat_buoc():
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        ModerationResult(label="SAFE")  # thiếu các trường bắt buộc
