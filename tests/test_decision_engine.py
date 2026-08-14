"""Kiểm thử động cơ ra quyết định `src.decision_engine`."""

import pytest

from src.decision_engine import determine_action, determine_label


class TestDetermineAction:
    def test_diem_thap_duoc_dang(self):
        assert determine_action(0, "none") == "allow"
        assert determine_action(19, "none") == "allow"

    def test_diem_mo_ho_can_duyet_lai(self):
        assert determine_action(20, "none") == "review"
        assert determine_action(39, "none") == "review"

    def test_spam_va_porn_nhiem_bi_xoa(self):
        assert determine_action(50, "spam") == "remove"
        assert determine_action(50, "pornography") == "remove"

    def test_danh_muc_khac_chi_canh_bao(self):
        assert determine_action(50, "insult") == "warn"
        assert determine_action(59, "harassment") == "warn"

    def test_diem_cao_bi_khoa_tam_thoi(self):
        assert determine_action(60, "insult") == "ban_temp"
        assert determine_action(79, "insult") == "ban_temp"

    def test_diem_rat_cao_bi_khoa_vinh_vien(self):
        assert determine_action(80, "insult") == "ban_perm"
        assert determine_action(100, "violence") == "ban_perm"

    def test_tien_su_vi_pham_cong_don_diem(self):
        # 30đ + 3 lần vi phạm x 15đ = 75đ -> ban_temp
        assert determine_action(30, "insult", strikes=3) == "ban_temp"

    def test_diem_cong_don_bi_gioi_han_100(self):
        assert determine_action(100, "insult", strikes=5) == "ban_perm"


class TestDetermineLabel:
    @pytest.mark.parametrize(
        ("action", "expected_label"),
        [
            ("allow", "SAFE"),
            ("review", "SUSPICIOUS"),
            ("warn", "VIOLATION"),
            ("remove", "VIOLATION"),
            ("ban_temp", "VIOLATION"),
            ("ban_perm", "VIOLATION"),
        ],
    )
    def test_doi_nhan(self, action, expected_label):
        assert determine_label(action) == expected_label
