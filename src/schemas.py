"""Các model dữ liệu chuẩn (Pydantic) dùng chung trong hệ thống."""

from pydantic import BaseModel, Field


class ModerationResult(BaseModel):
    """Kết quả cuối cùng của một lượt kiểm duyệt nội dung."""

    label: str = Field(description="SAFE, SUSPICIOUS, hoặc VIOLATION")
    severity: int = Field(description="Điểm vi phạm từ 0 đến 100")
    category: str = Field(description="Loại vi phạm (vd: none, insult, hate_speech...)")
    action: str = Field(
        description="Hành động: allow, review, remove, warn, ban_temp, ban_perm"
    )
    reason: str = Field(description="Lý do ngắn gọn")
    excerpt: str = Field(default="", description="Trích đoạn vi phạm (nếu có)")
    used_ai: bool = Field(default=False, description="Đánh dấu có dùng lớp AI để duyệt không")
