# models/admin.py
from models.user import User, AccountStatus


class Admin(User):
    """
    Admin – Trang 50–51
    """

    def __init__(
        self,
        user_id: int,
        username: str,
        password: str,
        email: str,
        full_name: str,
        status: AccountStatus = AccountStatus.ACTIVE
    ):
        super().__init__(
            user_id,
            username,
            password,
            email,
            full_name,
            status
        )
        self.role = "ADMIN"

    def __str__(self):
        return f"Admin(id={self.user_id}, username={self.username})"
