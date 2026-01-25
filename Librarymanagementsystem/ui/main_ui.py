import tkinter as tk

class MainUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="GIAO DIỆN CHÍNH", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(self, text="Quản lý sách", width=25,
                  command=lambda: self.app.show("books")).pack(pady=5)

        tk.Button(self, text="Mượn / Trả sách", width=25,
                  command=lambda: self.app.show("borrow")).pack(pady=5)

        tk.Button(self, text="Quản trị (Admin)", width=25,
                  command=lambda: self.app.show("admin")).pack(pady=5)

        tk.Button(self, text="Đăng xuất", width=25,
                  command=lambda: self.app.show("auth")).pack(pady=15)
