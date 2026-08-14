"""Kiểm thử bộ chấm điểm từ ngữ `src.static_filter`."""

from src.static_filter import score_text


def test_van_ban_rong():
    result = score_text("")
    assert result["score"] == 0
    assert result["verdict"] == "An Toàn"
    assert result["details"] == {}


def test_van_ban_sach():
    result = score_text("Em chào thầy cô, cho em hỏi bài văn ạ")
    assert result["score"] == 0
    assert result["verdict"] == "An Toàn"


def test_tu_nghe_trong_bai_toan_khong_bi_phat():
    # "ngu" xuất hiện trong "người" -> KHÔNG bị tính là vi phạm
    result = score_text("Người ta giải phương trình bằng cách đặt ẩn phụ")
    assert result["score"] == 0
    assert result["verdict"] == "An Toàn"


def test_tu_vi_pham_nhe():
    result = score_text("Mày đã làm bài tập chưa?")
    assert result["score"] == 15
    assert result["verdict"] == "Cảnh Cáo Nhẹ"
    assert "mày" in result["details"]


def test_tu_vi_pham_nang():
    result = score_text("đm")
    assert result["score"] == 50
    assert result["verdict"] == "Vi Phạm Nặng"


def test_diem_cong_don_va_gioi_han_100():
    # Lặp từ nặng nhiều lần: 50đ x nhiều lần -> bị chặn ở 100
    result = score_text("đm đm đm đm đm")
    assert result["score"] == 100
    assert result["verdict"] == "Rất Độc Hại"
    assert result["recommended_action"] == "Cấm đăng, khóa tài khoản"


def test_chi_tiet_dem_so_lan():
    result = score_text("mày và tao cùng làm bài")
    # "mày" 15đ + "tao" 15đ = 30đ
    assert result["score"] == 30
    assert "mày" in result["details"]
    assert "tao" in result["details"]
