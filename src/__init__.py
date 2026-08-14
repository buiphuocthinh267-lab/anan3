"""Gói `src` chứa toàn bộ logic nghiệp vụ của ứng dụng ANAN.

Các module chính:
    - config:          Đọc cấu hình/bí mật tập trung (secrets + env).
    - api_client:      Client gọi backend Google Apps Script (Google Sheets).
    - auth:            Quản lý phiên đăng nhập và cổng bảo vệ các trang.
    - moderation:      Luồng kiểm duyệt nội dung đa lớp (điểm vào chính).
    - rules:           Bộ lọc tĩnh dựa trên từ khóa vi phạm tiếng Việt.
    - static_filter:   Bộ chấm điểm từ ngữ (thang 0-100) cho diễn đàn.
    - ai_client:       Gọi OpenAI Moderation API (lớp kiểm duyệt AI).
    - decision_engine: Quyết định hành động phạt dựa trên điểm vi phạm.
    - schemas:         Các model Pydantic dùng chung.
"""

__version__ = "1.0.0"
