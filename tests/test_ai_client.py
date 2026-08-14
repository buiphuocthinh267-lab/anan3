"""Kiểm thử client OpenAI `src.ai_client` (không gọi API thật)."""

from src.ai_client import analyze_with_ai


def test_thieu_api_key_tra_ve_none():
    assert analyze_with_ai("văn bản gì đó", "") is None
    assert analyze_with_ai("văn bản gì đó", "   ") is None


def test_van_ban_rong_tra_ve_none():
    assert analyze_with_ai("   ", "sk-fake") is None


def test_parse_ket_qua_tu_openai(monkeypatch):
    """Giả lập phản hồi của OpenAI và kiểm tra việc chuẩn hóa kết quả."""
    import src.ai_client as ai_client

    class FakeResponse:
        status_code = 200

        def json(self):
            return {
                "results": [
                    {
                        "flagged": True,
                        "category_scores": {
                            "violence": 0.42,
                            "sexual": 0.95,
                            "hate": 0.01,
                        },
                    }
                ]
            }

    def fake_post(url, headers=None, json=None, timeout=None):
        assert url == "https://api.openai.com/v1/moderations"
        assert headers["Authorization"].startswith("Bearer ")
        assert json["input"] == "nội dung cần duyệt"
        return FakeResponse()

    monkeypatch.setattr(ai_client.requests, "post", fake_post)

    result = ai_client.analyze_with_ai("nội dung cần duyệt", "sk-fake")
    assert result is not None
    # Danh mục điểm cao nhất là "sexual" (0.95) -> pornography, severity 95
    assert result["severity"] == 95
    assert result["category"] == "pornography"
    assert result["excerpt"] == "nội dung cần duyệt"  # flagged -> giữ nguyên văn bản


def test_loi_mang_tra_ve_none(monkeypatch):
    import src.ai_client as ai_client

    def fake_post(url, headers=None, json=None, timeout=None):
        raise ai_client.requests.RequestException("mất kết nối")

    monkeypatch.setattr(ai_client.requests, "post", fake_post)
    assert ai_client.analyze_with_ai("văn bản", "sk-fake") is None
