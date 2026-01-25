"""
main_cli.py
Điểm khởi đầu cho giao diện dòng lệnh (CLI).
Chức năng: hiển thị menu chính và điều hướng các màn hình con.
"""

# Import các UI màn hình con (phải là CLI, không được là Tkinter/GUIs)
from .auth_ui import AuthUI
from .admin_ui import AdminUI
from .book_ui import BookUI
from .borrow_ui import BorrowUI


class MainCLI:
    def __init__(self):
        # Sau này có thể truyền SessionManager, services vào đây
        pass

    def show_menu(self):
        """Hiển thị menu chính"""
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Đăng nhập")
        print("2. Quản lý sách")
        print("3. Quản lý mượn/trả")
        print("4. Quản trị (Admin)")
        print("5. Thoát")
        print("==============================================")

    def run(self):
        """Chạy vòng lặp chính của chương trình"""
        while True:
            self.show_menu()
            choice = input("Chọn chức năng: ").strip()

            if choice == "1":
                print("Bạn chọn: Đăng nhập")
                try:
                    auth_ui = AuthUI()
                    auth_ui.login()
                except TypeError:
                    print("AuthUI đang thiết kế theo GUI (cần master/app). Hãy đổi về CLI.")
                except Exception as e:
                    print(f"Lỗi khi chạy AuthUI: {e}")

            elif choice == "2":
                print("Bạn chọn: Quản lý sách")
                try:
                    book_ui = BookUI()
                    book_ui.run()
                except Exception as e:
                    print(f"Lỗi khi chạy BookUI: {e}")

            elif choice == "3":
                print("Bạn chọn: Quản lý mượn/trả")
                try:
                    borrow_ui = BorrowUI()
                    borrow_ui.run()
                except Exception as e:
                    print(f"Lỗi khi chạy BorrowUI: {e}")

            elif choice == "4":
                print("Bạn chọn: Quản trị (Admin)")
                try:
                    admin_ui = AdminUI()
                    admin_ui.run()
                except Exception as e:
                    print(f"Lỗi khi chạy AdminUI: {e}")

            elif choice == "5":
                print("Thoát chương trình. Tạm biệt!")
                break

            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
