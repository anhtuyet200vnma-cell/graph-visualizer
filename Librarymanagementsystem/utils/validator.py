"""
validator.py
Các hàm kiểm tra dữ liệu (validate) trước khi tạo/ghi dữ liệu.
"""

from datetime import date


class Validator:
    @staticmethod
    def validate_not_empty(value, field_name: str):
        """
        Check dữ liệu không được rỗng.
        """
        if value is None or str(value).strip() == "":
            return False, f"{field_name} không được để trống"
        return True, None

    @staticmethod
    def validate_positive_number(value, field_name: str):
        """
        Check số phải lớn hơn 0.
        """
        try:
            num = int(value)
            if num <= 0:
                return False, f"{field_name} phải lớn hơn 0"
            return True, None
        except:
            return False, f"{field_name} phải là số hợp lệ"

    @staticmethod
    def validate_date_order(start_date: date, end_date: date, field_name: str = "Ngày"):
        """
        Check ngày kết thúc >= ngày bắt đầu.
        """
        if start_date is None or end_date is None:
            return True, None

        if end_date < start_date:
            return False, f"{field_name} không hợp lệ (ngày kết thúc nhỏ hơn ngày bắt đầu)"
        return True, None
