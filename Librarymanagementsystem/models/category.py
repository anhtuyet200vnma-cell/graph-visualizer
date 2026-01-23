"""
- Mục đích: Quản lý thông tin "Category" (thể loại sách)
- Category thường dùng để phân loại sách: Khoa học, Văn học, Công nghệ, v.v.
"""
class Category:
    """
    Lớp Category đại diện cho 1 thể loại sách trong hệ thống.

    Thuộc tính:
    - category_id: mã thể loại (số nguyên dương)
    - category_name: tên thể loại (chuỗi, không được rỗng)
    """

    def __init__(self, category_id: int, category_name: str):
        # 1) Kiểm tra category_id phải là số nguyên dương
        if not isinstance(category_id, int) or category_id <= 0:
            raise ValueError("category_id phải là số nguyên dương (> 0)")

        # 2) Kiểm tra category_name phải là chuỗi và không được để trống
        if not isinstance(category_name, str) or not category_name.strip():
            raise ValueError("category_name phải là chuỗi và không được rỗng")

        # 3) Gán giá trị hợp lệ vào thuộc tính của object
        self.category_id = category_id
        self.category_name = category_name.strip()

    def get_category_name(self) -> str:
        """
        Trả về tên thể loại.
        Ví dụ: "Engineering", "Science", "Literature"
        """
        return self.category_name

    def set_category_name(self, new_name: str):
        """
        Cập nhật tên thể loại.

        new_name: tên mới của thể loại (không rỗng)
        """
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("new_name phải là chuỗi và không được rỗng")

        self.category_name = new_name.strip()

    def __str__(self):
        """
        Hàm giúp in object ra màn hình dễ đọc hơn.
        """
        return f"Category(id={self.category_id}, name='{self.category_name}')"
