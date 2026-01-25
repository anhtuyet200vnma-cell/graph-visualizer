import tkinter as tk
from tkinter import messagebox
import json
import os


class AuthUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.mode = "login"  # login | register

        # Đọc đúng file data/user.json của nhóm
        self.users_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # Librarymanagementsystem/
            "data",
            "user.json"
        )

        self.build_ui()

    # ===== JSON Helpers =====
    def load_users(self):
        if not os.path.exists(self.users_file):
            messagebox.showerror("Error", f"Không tìm thấy file: {self.users_file}")
            return []

        with open(self.users_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "File user.json bị lỗi định dạng JSON.")
                return []

    def save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def user_exists(self, username):
        users = self.load_users()
        return any(u["username"] == username for u in users)

    def register_user(self, username, password):
        users = self.load_users()

        if self.user_exists(username):
            return False, "Username đã tồn tại."

        # Tạo user_id mới
        new_id = max([u.get("user_id", 0) for u in users], default=0) + 1

        new_user = {
            "user_id": new_id,
            "username": username,
            "email": f"{username}@example.com",
            "password": password,
            "full_name": username,
            "phone_number": "",
            "status": "ACTIVE",
            "role": "MEMBER",
            "created_at": "2026-01-25T00:00:00"
        }

        users.append(new_user)
        self.save_users(users)
        return True, "Đăng ký thành công!"

    def login_user(self, username, password):
        users = self.load_users()

        for u in users:
            if u["username"] == username and u["password"] == password:
                return True, f"Xin chào {u.get('full_name', username)}!"
        return False, "Sai username hoặc password."

    # ===== UI =====
    def build_ui(self):
        self.title_label = tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        self.box = tk.Frame(self)
        self.box.pack(pady=10)

        tk.Label(self.box, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.box, width=35)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.box, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.box, width=35, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        self.confirm_label = tk.Label(self.box, text="Confirm:")
        self.confirm_entry = tk.Entry(self.box, width=35, show="*")

        self.action_btn = tk.Button(self, text="Login", width=20, command=self.handle_action)
        self.action_btn.pack(pady=10)

        self.switch_btn = tk.Button(self, text="Chưa có tài khoản? Đăng ký", command=self.switch_mode)
        self.switch_btn.pack(pady=5)

        self.info = tk.Label(self, text="", fg="blue")
        self.info.pack(pady=5)

    def switch_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.title_label.config(text="ĐĂNG KÝ")
            self.action_btn.config(text="Register")
            self.switch_btn.config(text="Đã có tài khoản? Đăng nhập")

            self.confirm_label.grid(row=2, column=0, sticky="w", pady=5)
            self.confirm_entry.grid(row=2, column=1, pady=5)
        else:
            self.mode = "login"
            self.title_label.config(text="ĐĂNG NHẬP")
            self.action_btn.config(text="Login")
            self.switch_btn.config(text="Chưa có tài khoản? Đăng ký")

            self.confirm_label.grid_forget()
            self.confirm_entry.grid_forget()

        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)
        self.info.config(text="")

    def handle_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Vui lòng nhập đầy đủ username và password.")
            return

        # ===== REGISTER =====
        if self.mode == "register":
            confirm = self.confirm_entry.get().strip()

            if not confirm:
                messagebox.showerror("Error", "Vui lòng nhập Confirm Password.")
                return

            if password != confirm:
                messagebox.showerror("Error", "Password và Confirm Password không khớp.")
                return

            ok, msg = self.register_user(username, password)
            if ok:
                messagebox.showinfo("Register", msg)
                self.switch_mode()
            else:
                messagebox.showerror("Register failed", msg)
            return

        # ===== LOGIN =====
        ok, msg = self.login_user(username, password)
        if ok:
            messagebox.showinfo("Login", msg)
            self.info.config(text=msg)
            self.app.show("main")

            # nếu có màn hình sau login thì mở tiếp
            # self.app.show("books")
        else:
            messagebox.showerror("Login failed", msg)
            self.info.config(text=msg)
