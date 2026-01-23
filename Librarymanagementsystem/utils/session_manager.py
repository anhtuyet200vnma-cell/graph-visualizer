"""
session_manager.py
Quản lý trạng thái đăng nhập trong chương trình.
"""

class SessionManager:
    """
    Class quản lý session (user đang đăng nhập).
    """

    def __init__(self):
        self.current_user = None

    def login(self, user):
        """
        Gán user hiện tại sau khi đăng nhập thành công.
        """
        self.current_user = user

    def logout(self):
        """
        Đăng xuất: xoá user hiện tại.
        """
        self.current_user = None

    def is_logged_in(self) -> bool:
        """
        Kiểm tra có user đang đăng nhập hay không.
        """
        return self.current_user is not None

    def get_current_user(self):
        """
        Lấy user đang đăng nhập.
        """
        return self.current_user
