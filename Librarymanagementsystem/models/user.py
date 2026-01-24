# models/user.py
import re
from enum import Enum
from datetime import datetime


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Role(Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


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
        phone_number: str,
        role: Role,
        status: AccountStatus = AccountStatus.ACTIVE,
        created_at: str | None = None
    ):
        if not isinstance(user_id, int):
            raise ValueError("user_id phải là số nguyên")

        if not (3 <= len(username) <= 50):
            raise ValueError("username 3–50 ký tự")

        if len(password) < 8:
            raise ValueError("password ≥ 8 ký tự")

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValueError("email không hợp lệ")

        if not (2 <= len(full_name) <= 100):
            raise ValueError("full_name 2–100 ký tự")

        if not re.match(r'^\d{9,11}$', phone_number):
            raise ValueError("phone_number không hợp lệ")

        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.full_name = full_name
        self.phone_number = phone_number
        self.role = role
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()

    # ===== Methods theo đặc tả =====

    def update_profile(self, email=None, full_name=None, phone_number=None) -> bool:
        if email:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                raise ValueError("email không hợp lệ")
            self.email = email

        if full_name:
            self.full_name = full_name

        if phone_number:
            if not re.match(r'^\d{9,11}$', phone_number):
                raise ValueError("phone_number không hợp lệ")
            self.phone_number = phone_number

        return True

    def reset_password(self, new_password: str) -> bool:
        if len(new_password) < 8:
            raise ValueError("password ≥ 8 ký tự")
        self.password = new_password
        return True

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "role": self.role.value,
            "status": self.status.value,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=data["user_id"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            full_name=data["full_name"],
            phone_number=data["phone_number"],
            role=Role(data["role"]),
            status=AccountStatus(data["status"]),
            created_at=data.get("created_at")
        )
