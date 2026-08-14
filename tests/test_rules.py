"""Kiểm thử bộ lọc tĩnh `src.rules`."""

from src.rules import analyze_rules


def test_van_ban_an_toan():
    severity, category, excerpt = analyze_rules("Cho mình hỏi bài tập toán trang 15 với ạ")
    assert severity == 0
    assert category == "none"
    assert excerpt == ""


def test_phat_hien_xuc_pham_khong_dau():
    severity, category, _ = analyze_rules("thằng kia dm quá")
    assert severity == 85
    assert category == "insult"


def test_phat_hien_xuc_pham_co_dau():
    severity, category, excerpt = analyze_rules("đồ chó này")
    assert severity == 85
    assert category == "insult"
    assert excerpt != ""


def test_phat_hien_bao_luc():
    severity, category, _ = analyze_rules("tao sẽ đâm nó bây giờ")
    assert severity == 90
    assert category == "violence"


def test_phat_hien_spam():
    severity, category, _ = analyze_rules("kiếm tiền tại nhà nè mọi người")
    assert severity == 60
    assert category == "spam"


def test_khong_phan_biet_chu_hoa_chu_thuong():
    severity, category, _ = analyze_rules("ĐM")
    assert severity == 85
    assert category == "insult"


def test_lay_vi_pham_nang_nhat_khi_nhieu_loi():
    # Câu chứa cả spam (60đ) và bạo lực (90đ) -> lấy 90đ
    severity, category, _ = analyze_rules("nhấp vào link kiếm tiền hoặc tao chém")
    assert severity == 90
    assert category == "violence"


def test_khong_bao_loi_nham_tu_la_tu_khoa_con():
    # "dm" nằm trong "admin", "dit" nằm trong "edit" -> KHÔNG bị phạt
    severity, category, _ = analyze_rules("admin edit bài viết giúp tôi với")
    assert severity == 0
    assert category == "none"
