import tkinter as tk
from tkinter import Menu

from .auth_ui import AuthUI
from .main_ui import MainUI
from .book_ui import BookUI
from .borrow_ui import BorrowUI
from .admin_ui import AdminUI


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x500")

        # ===== Tạo sẵn menu nhưng CHƯA hiện =====
        self.menubar = Menu(self)

        self.menubar.add_command(label="Trang chính", command=lambda: self.show("main"))
        self.menubar.add_command(label="Quản lý sách", command=lambda: self.show("books"))
        self.menubar.add_command(label="Mượn / Trả", command=lambda: self.show("borrow"))
        self.menubar.add_command(label="Admin", command=lambda: self.show("admin"))
        self.menubar.add_command(label="Đăng xuất", command=lambda: self.logout())

        # ===== Khung chứa các màn hình =====
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # ===== Khởi tạo màn hình =====
        self.frames["auth"] = AuthUI(container, self)
        self.frames["main"] = MainUI(container, self)
        self.frames["books"] = BookUI(container, self)
        self.frames["borrow"] = BorrowUI(container, self)
        self.frames["admin"] = AdminUI(container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        # ===== Mặc định vào login -> menu ẨN =====
        self.hide_menu()
        self.show("auth")

    # ===== 2 hàm điều khiển menu =====
    def show_menu(self):
        self.config(menu=self.menubar)

    def hide_menu(self):
        self.config(menu="")

    # ===== Điều hướng =====
    def show(self, name):
        if name not in self.frames:
            print(f"[WARN] Không có màn hình: {name}")
            return

        # Nếu vào màn login -> ẩn menu
        if name == "auth":
            self.hide_menu()
        else:
            # Các màn còn lại là sau login -> hiện menu
            self.show_menu()

        self.frames[name].tkraise()

    # ===== Logout chuẩn =====
    def logout(self):
        self.hide_menu()
        self.show("auth")
