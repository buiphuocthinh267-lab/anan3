"""Kiểm thử luồng kiểm duyệt đa lớp `src.moderation` (không gọi API thật)."""

from src.moderation import moderate_content


def test_van_ban_an_toan_khong_dung_ai():
    result = moderate_content("Cho em hỏi cách giải phương trình bậc hai ạ")
    assert result.label == "SAFE"
    assert result.severity == 0
    assert result.category == "none"
    assert result.action == "allow"
    assert result.used_ai is False


def test_van_ban_vi_pham_nang_khong_can_ai():
    # severity >= 80 -> bộ lọc tĩnh quyết luôn, không tốn tiền gọi AI
    result = moderate_content("đồ chó này", api_key="fake-key")
    assert result.label == "VIOLATION"
    assert result.severity == 85
    assert result.category == "insult"
    assert result.used_ai is False
    assert result.excerpt != ""


def test_mo_ho_se_goi_ai(monkeypatch):
    """Kết quả tĩnh mơ hồ (0 < severity < 80) -> gọi lớp AI dự phòng."""

    def fake_analyze(text, api_key, model_name="omni-moderation-latest"):
        return {
            "severity": 95,
            "category": "violence",
            "reason": "AI phát hiện bạo lực",
            "excerpt": text,
        }

    monkeypatch.setattr("src.moderation.analyze_with_ai", fake_analyze)

    # "nổ hũ" -> bộ lọc tĩnh cho 60đ (mơ hồ) -> AI được gọi
    result = moderate_content("nổ hũ đi các bạn ơi", api_key="fake-key")
    assert result.used_ai is True
    assert result.severity == 95
    assert result.category == "violence"
    assert result.reason == "AI phát hiện bạo lực"


def test_force_ai_bat_dau_tu_van_ban_sach(monkeypatch):
    """force_ai=True -> gọi AI kể cả khi bộ lọc tĩnh nói an toàn."""

    def fake_analyze(text, api_key, model_name="omni-moderation-latest"):
        return {
            "severity": 70,
            "category": "harassment",
            "reason": "AI đánh dấu nghi ngờ",
            "excerpt": "",
        }

    monkeypatch.setattr("src.moderation.analyze_with_ai", fake_analyze)

    result = moderate_content(
        "một câu văn hoàn toàn bình thường", api_key="fake-key", force_ai=True
    )
    assert result.used_ai is True
    assert result.severity == 70


def test_khong_api_key_chi_dung_bo_loc_tinh():
    result = moderate_content("nổ hũ đi các bạn")  # không truyền api_key
    assert result.used_ai is False
    assert result.severity == 60
    assert result.action == "remove"  # spam -> xóa
