class AuthUI:
    def __init__(self):
        pass

    def login_screen(self):
        print("\n========== ĐĂNG NHẬP ==========")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Demo (sau này nối Controller)
        if username == "admin" and password == "123":
            print(" Đăng nhập thành công (Admin)!")
            return True, {"username": username, "role": "admin"}
        elif username == "member" and password == "123":
            print(" Đăng nhập thành công (Member)!")
            return True, {"username": username, "role": "member"}
        else:
            print(" Sai username hoặc password!")
            return False, None
