# models/user.py
import re
from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class User:
    """
    User – Trang 49–50 (PDF)
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
        if not isinstance(user_id, int):
            raise ValueError("user_id phải là số nguyên")

        if not (5 <= len(username) <= 50):
            raise ValueError("username 5–50 ký tự")

        if len(password) < 8:
            raise ValueError("password ≥ 8 ký tự")

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("email không hợp lệ")

        if not (2 <= len(full_name) <= 100):
            raise ValueError("full_name 2–100 ký tự")

        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.full_name = full_name
        self.status = status

    # ===== Methods theo đặc tả =====

    def update_profile(self, email=None, full_name=None, password=None) -> bool:
        if email:
            self.email = email
        if full_name:
            self.full_name = full_name
        if password:
            if len(password) < 8:
                raise ValueError("password ≥ 8 ký tự")
            self.password = password
        return True

    def reset_password(self, email: str) -> bool:
        return self.email == email

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "full_name": self.full_name,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["user_id"],
            data["username"],
            data["password"],
            data["email"],
            data["full_name"],
            AccountStatus(data["status"])
        )
