from models.user import User

class UserService:

    @staticmethod
    def registerAccount(user: User):
        print(f"User {user.username} registered successfully.")

    @staticmethod
    def login(user: User, password: str) -> bool:
        if user.password == password:
            print("Login successful.")
            return True
        print("Invalid credentials.")
        return False

    @staticmethod
    def logout(user: User):
        print(f"User {user.username} logged out.")

    @staticmethod
    def updateProfile(user: User, email: str, phone: str):
        user.email = email
        user.phone_number = phone
        print("Profile updated.")

    @staticmethod
    def resetPassword(user: User, new_password: str):
        user.password = new_password
        print("Password reset successful.")