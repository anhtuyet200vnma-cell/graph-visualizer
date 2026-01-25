class AdminUI:
    def __init__(self):
        pass

    def admin_menu(self):
        print("\n========== ADMIN MENU ==========")
        print("1. Thêm sách")
        print("2. Xóa sách")
        print("3. Quay lại")

    def run(self):
        while True:
            self.admin_menu()
            choice = input("Chọn chức năng admin: ").strip()

            if choice == "1":
                isbn = input("ISBN: ").strip()
                title = input("Title: ").strip()
                print(f"✅ (Demo) Đã thêm sách: {isbn} - {title}")

            elif choice == "2":
                book_id = input("Book ID: ").strip()
                print(f"✅ (Demo) Đã xóa sách: {book_id}")

            elif choice == "3":
                break
            else:
                print("❌ Lựa chọn không hợp lệ.")
