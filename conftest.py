"""Đảm bảo thư mục gốc của dự án nằm trên sys.path khi chạy pytest.

Giúp các test import gói `src` bất kể vị trí gọi lệnh pytest.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
