# models/admin.py
from models.user import User, AccountStatus, Role


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
        phone_number: str,
        status: AccountStatus = AccountStatus.ACTIVE,
        created_at: str | None = None
    ):
        super().__init__(
            user_id=user_id,
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            role=Role.ADMIN,
            status=status,
            created_at=created_at
        )

    def __str__(self):
        return f"Admin(id={self.user_id}, username={self.username})"
