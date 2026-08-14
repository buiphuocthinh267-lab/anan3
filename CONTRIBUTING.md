# 🤝 Hướng dẫn đóng góp

Cảm ơn bạn quan tâm đóng góp cho ANAN! Tài liệu này giúp bạn bắt đầu nhanh chóng.

## 🚀 Quy trình đóng góp

1. **Fork** repository và **clone** về máy của bạn.
2. Tạo nhánh mới từ `main`:
   ```bash
   git checkout -b feat/ten-tinh-nang   # tính năng mới
   git checkout -b fix/ten-loi          # sửa lỗi
   git checkout -b docs/ten-thay-doi    # tài liệu
   ```
3. Thực hiện thay đổi, đảm bảo chất lượng (xem bên dưới).
4. Commit và push lên fork của bạn.
5. Tạo **Pull Request** về nhánh `main` của repo gốc (theo template).

## 📏 Chuẩn mã nguồn

- **Quy ước đặt tên:**
  - Module/biến/hàm tiếng Anh, `snake_case`.
  - Chuỗi hiển thị trên UI giữ nguyên tiếng Việt.
  - Hằng số viết hoa: `QUIZ_TIME_SECONDS`.
- **Kiểm duyệt nội dung:** mọi logic nghiệp vụ nằm trong `src/`, các file trong `pages/` chỉ chứa giao diện.
- **Bí mật:** KHÔNG BAO GIỜ hard-code API key/mật khẩu/URL bí mật trong mã. Luôn đọc qua `src/config.py` (st.secrets → biến môi trường).
- **Docstrings:** mọi hàm/module trong `src/` cần có docstring ngắn gọn (tiếng Việt OK).

## ✅ Checklist trước khi tạo PR

```bash
# Cài dependencies phát triển (lần đầu)
pip install -r requirements-dev.txt

# 1. Lint - không được có lỗi mới
ruff check .

# 2. Tests - toàn bộ phải pass
pytest
```

- [ ] `ruff check .` không có lỗi
- [ ] `pytest` pass (thêm test mới nếu thay đổi logic trong `src/`)
- [ ] Không chứa bí mật trong commit (kiểm tra kỹ trước khi push)
- [ ] Đã cập nhật README nếu thay đổi hành vi/cấu trúc

## 📝 Chuẩn commit (Conventional Commits)

```
feat: thêm trang trắc nghiệm AI
fix: sửa lỗi đếm ngược sàn đấu tự reset
docs: cập nhật hướng dẫn deploy
refactor: tách api_client khỏi các trang
test: thêm test cho decision_engine
chore: nâng cấp ruff lên 0.6
```

## 🐛 Báo lỗi

Mở issue theo template **🐛 Báo lỗi** — mô tả rõ các bước tái hiện để chúng tôi xử lý nhanh nhất.

## ❓ Câu hỏi khác

Mở issue với label `question`, chúng tôi sẽ trả lời sớm nhất có thể.
