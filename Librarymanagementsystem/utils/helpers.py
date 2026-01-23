"""
helpers.py
Các hàm tiện ích dùng chung cho toàn bộ hệ thống.
"""

from datetime import datetime, date
import random
import string


def generate_id(prefix: str = "", length: int = 6) -> str:
    """
    Tạo ID ngẫu nhiên.
    Ví dụ: generate_id("B") -> "B5F8K2A"
    """
    chars = string.ascii_uppercase + string.digits
    random_part = "".join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"


def get_current_datetime() -> str:
    """
    Trả về datetime hiện tại dạng chuỗi ISO.
    Ví dụ: 2026-01-23T14:20:30
    """
    return datetime.now().isoformat(timespec="seconds")


def get_current_date() -> str:
    """
    Trả về ngày hiện tại dạng YYYY-MM-DD
    """
    return date.today().isoformat()


def parse_date_str(date_str: str) -> date:
    """
    Chuyển chuỗi YYYY-MM-DD thành đối tượng date.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def format_currency(amount: int) -> str:
    """
    Format tiền Việt Nam (có dấu phẩy ngăn cách).
    Ví dụ: 1500000 -> "1,500,000"
    """
    return f"{amount:,}"
