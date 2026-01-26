# services/user_service.py
from models.user import User, AccountStatus, Role
from models.member import Member
from utils.file_handler_fix import load_json, save_json
from datetime import datetime
import re


class UserService:
    def __init__(self, user_path="data/users.json"):
        self.user_path = user_path

    # ... phần còn lại của code ...

    def register(self, user_data: dict) -> dict:
        """Đăng ký tài khoản mới"""
        try:
            users = load_json(self.user_path)
            
            # Kiểm tra username tồn tại
            existing_user = next(
                (u for u in users if u.get("username") == user_data.get("username")), 
                None
            )
            if existing_user:
                return {"success": False, "message": "Username đã tồn tại"}
            
            # Kiểm tra email tồn tại
            existing_email = next(
                (u for u in users if u.get("email") == user_data.get("email")), 
                None
            )
            if existing_email:
                return {"success": False, "message": "Email đã được sử dụng"}
            
            # Validate dữ liệu
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', user_data.get("email", "")):
                return {"success": False, "message": "Email không hợp lệ"}
            
            if len(user_data.get("password", "")) < 8:
                return {"success": False, "message": "Mật khẩu phải có ít nhất 8 ký tự"}
            
            if len(user_data.get("username", "")) < 3:
                return {"success": False, "message": "Username phải có ít nhất 3 ký tự"}
            
            # Tạo user_id mới
            user_id = len(users) + 1 if users else 1
            
            # Tạo user object
            new_user = {
                "user_id": user_id,
                "username": user_data.get("username"),
                "password": user_data.get("password"),
                "email": user_data.get("email"),
                "full_name": user_data.get("full_name", ""),
                "phone_number": user_data.get("phone_number", ""),
                "role": "MEMBER",
                "status": "ACTIVE",
                "borrowing_limit": 5,
                "penalty_status": False,
                "created_at": datetime.now().isoformat()
            }
            
            users.append(new_user)
            save_json(self.user_path, users)
            
            return {
                "success": True, 
                "message": "Đăng ký thành công", 
                "user_id": user_id
            }
            
        except Exception as e:
            print(f"Error registering user: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def login(self, username: str, password: str) -> dict:
        """Đăng nhập"""
        try:
            users = load_json(self.user_path)
            
            user_data = next(
                (u for u in users if u.get("username") == username), 
                None
            )
            
            if not user_data:
                return {"success": False, "message": "Username không tồn tại"}
            
            if user_data.get("password") != password:
                return {"success": False, "message": "Mật khẩu không đúng"}
            
            if user_data.get("status") != "ACTIVE":
                status = user_data.get("status", "UNKNOWN")
                return {"success": False, "message": f"Tài khoản đang ở trạng thái: {status}"}
            
            # Tạo user object
            if user_data.get("role") == "ADMIN":
                from models.admin import Admin
                user = Admin(
                    user_id=user_data.get("user_id"),
                    username=user_data.get("username"),
                    password=user_data.get("password"),
                    email=user_data.get("email"),
                    full_name=user_data.get("full_name"),
                    phone_number=user_data.get("phone_number"),
                    status=AccountStatus(user_data.get("status")),
                    created_at=user_data.get("created_at")
                )
            else:
                user = Member(
                    user_id=user_data.get("user_id"),
                    username=user_data.get("username"),
                    password=user_data.get("password"),
                    email=user_data.get("email"),
                    full_name=user_data.get("full_name"),
                    phone_number=user_data.get("phone_number"),
                    status=AccountStatus(user_data.get("status")),
                    borrowing_limit=user_data.get("borrowing_limit", 5),
                    penalty_status=user_data.get("penalty_status", False)
                )
            
            return {
                "success": True, 
                "message": "Đăng nhập thành công", 
                "user": user
            }
            
        except Exception as e:
            print(f"Error logging in: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def update_profile(self, user_id: int, update_data: dict) -> dict:
        """Cập nhật thông tin cá nhân"""
        try:
            users = load_json(self.user_path)
            
            for i, user in enumerate(users):
                if user.get("user_id") == user_id:
                    # Validate email nếu có
                    if "email" in update_data:
                        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', update_data["email"]):
                            return {"success": False, "message": "Email không hợp lệ"}
                        
                        # Kiểm tra email trùng
                        existing_email = next(
                            (u for u in users 
                             if u.get("email") == update_data["email"] and u.get("user_id") != user_id), 
                            None
                        )
                        if existing_email:
                            return {"success": False, "message": "Email đã được sử dụng"}
                    
                    # Validate phone nếu có
                    if "phone_number" in update_data:
                        if not re.match(r'^\d{9,11}$', update_data["phone_number"]):
                            return {"success": False, "message": "Số điện thoại không hợp lệ"}
                    
                    # Cập nhật thông tin
                    for key, value in update_data.items():
                        if key in ["email", "full_name", "phone_number"]:
                            users[i][key] = value
                    
                    save_json(self.user_path, users)
                    
                    return {"success": True, "message": "Cập nhật thành công"}
            
            return {"success": False, "message": "Không tìm thấy user"}
            
        except Exception as e:
            print(f"Error updating profile: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def reset_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        """Đổi mật khẩu"""
        try:
            if len(new_password) < 8:
                return {"success": False, "message": "Mật khẩu mới phải có ít nhất 8 ký tự"}
            
            users = load_json(self.user_path)
            
            for i, user in enumerate(users):
                if user.get("user_id") == user_id:
                    if user.get("password") != old_password:
                        return {"success": False, "message": "Mật khẩu cũ không đúng"}
                    
                    users[i]["password"] = new_password
                    save_json(self.user_path, users)
                    
                    return {"success": True, "message": "Đổi mật khẩu thành công"}
            
            return {"success": False, "message": "Không tìm thấy user"}
            
        except Exception as e:
            print(f"Error resetting password: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def get_user_by_id(self, user_id: int):
        """Lấy thông tin user theo ID"""
        try:
            users = load_json(self.user_path)
            
            user_data = next((u for u in users if u.get("user_id") == user_id), None)
            if not user_data:
                return None
            
            if user_data.get("role") == "ADMIN":
                from models.admin import Admin
                return Admin(
                    user_id=user_data.get("user_id"),
                    username=user_data.get("username"),
                    password=user_data.get("password"),
                    email=user_data.get("email"),
                    full_name=user_data.get("full_name"),
                    phone_number=user_data.get("phone_number"),
                    status=AccountStatus(user_data.get("status")),
                    created_at=user_data.get("created_at")
                )
            else:
                return Member(
                    user_id=user_data.get("user_id"),
                    username=user_data.get("username"),
                    password=user_data.get("password"),
                    email=user_data.get("email"),
                    full_name=user_data.get("full_name"),
                    phone_number=user_data.get("phone_number"),
                    status=AccountStatus(user_data.get("status")),
                    borrowing_limit=user_data.get("borrowing_limit", 5),
                    penalty_status=user_data.get("penalty_status", False)
                )
                
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    def search_users(self, keyword: str):
        """Tìm kiếm user"""
        try:
            users = load_json(self.user_path)
            
            results = []
            keyword_lower = keyword.lower()
            
            for user in users:
                username = user.get("username", "").lower()
                email = user.get("email", "").lower()
                full_name = user.get("full_name", "").lower()
                
                if (keyword_lower in username or 
                    keyword_lower in email or 
                    keyword_lower in full_name):
                    results.append(user)
            
            return results
        except Exception as e:
            print(f"Error searching users: {e}")
            return []

    def change_user_status(self, user_id: int, status: str) -> dict:
        """Thay đổi trạng thái user (Admin only)"""
        try:
            if status not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
                return {"success": False, "message": "Trạng thái không hợp lệ"}
            
            users = load_json(self.user_path)
            
            for i, user in enumerate(users):
                if user.get("user_id") == user_id:
                    users[i]["status"] = status
                    save_json(self.user_path, users)
                    return {"success": True, "message": f"Cập nhật trạng thái thành {status}"}
            
            return {"success": False, "message": "Không tìm thấy user"}
            
        except Exception as e:
            print(f"Error changing user status: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}