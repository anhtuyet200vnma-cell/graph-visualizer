# models/user.py
from datetime import datetime

class User:
    def __init__(self, user_id, username, email, password, full_name, 
                 phone="", status="active", role="member"):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.full_name = full_name
        self.phone = phone
        self.status = status  # active, inactive, suspended
        self.role = role
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Chuyển object thành dictionary để lưu JSON"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "full_name": self.full_name,
            "phone": self.phone,
            "status": self.status,
            "role": self.role,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Tạo object từ dictionary (khi đọc từ JSON)"""
        return cls(
            user_id=data["user_id"],
            username=data["username"],
            email=data["email"],
            password=data["password"],
            full_name=data["full_name"],
            phone=data.get("phone", ""),
            status=data.get("status", "active"),
            role=data.get("role", "member")
        )
    
    def display_info(self):
        """Hiển thị thông tin user"""
        return f"ID: {self.user_id} | Tên: {self.full_name} | Email: {self.email} | Vai trò: {self.role}"