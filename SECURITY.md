# 🔒 Bảo mật

## Báo cáo lỗ hổng

Nếu bạn phát hiện lỗ hổng bảo mật, **vui lòng không mở issue công khai**.
Vui lòng liên hệ trực tiếp người bảo trì qua email riêng tư của repository.
Vui lòng đợi phản hồi trước khi công khai thông tin. Chúng tôi cam kết phản hồi trong vòng 72 giờ.

## Nguyên tắc bảo mật của dự án

- **Không commit bí mật:** mọi API key, mật khẩu, URL nội bộ phải nằm trong
  `.streamlit/secrets.toml` (đã gitignore) hoặc biến môi trường — đọc qua `src/config.py`.
- **Mật khẩu admin** được so sánh bằng `hmac.compare_digest` để chống tấn công timing.
- **Kiểm duyệt nội dung:** nội dung người dùng nhập luôn đi qua pipeline trong `src/moderation.py`
  trước khi hiển thị công khai.

## Hạn chế đã biết

| Hạn chế | Mức độ | Kế hoạch |
|---|---|---|
| Mật khẩu người dùng lưu plain-text trên Google Sheets (backend Apps Script) | 🔴 Cao | Băm SHA-256 + salt phía Apps Script |
| Truyền thông tin qua HTTPS của Apps Script Web App — bất kỳ ai có URL có thể gọi trực tiếp | 🟡 Trung bình | Thêm token chia sẻ, giới hạn theo referer |
| Hòm thư góp ý ghi file cục bộ — có thể mất/không riêng tư trên hosting dùng chung | 🟡 Trung bình | Chuyển sang sheet riêng, chỉ admin đọc được |

> ⚠️ Dự án mang tính học tập/demo cho trường học. Không sử dụng cho dữ liệu nhạy cảm
> cho đến khi các mục 🔴 ở trên được khắc phục.
