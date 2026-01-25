import tkinter as tk
from tkinter import messagebox


class AdminUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        tk.Button(
            self,
            text="⬅ Quay lại",
            width=15,
            command=lambda: app.show("main")
        ).pack(anchor="w", padx=10, pady=5)
        self.app = app
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="ADMIN PANEL", font=("Arial", 18, "bold")).pack(pady=10)

        self.status = tk.Label(self, text="", fg="blue")
        self.status.pack(pady=5)

        form = tk.LabelFrame(self, text="Thêm sách (Demo)")
        form.pack(fill="x", padx=10, pady=10)

        self.isbn_entry = self._row(form, "ISBN:", 0)
        self.title_entry = self._row(form, "Title:", 1)
        self.author_entry = self._row(form, "Author ID:", 2)
        self.category_entry = self._row(form, "Category ID:", 3)
        self.qty_entry = self._row(form, "Quantity:", 4)

        tk.Button(form, text="Add Book", command=self.add_book).grid(row=5, column=0, columnspan=2, pady=8)

        delete_box = tk.LabelFrame(self, text="Xóa sách")
        delete_box.pack(fill="x", padx=10, pady=10)

        self.delete_id_entry = self._row(delete_box, "Book ID:", 0)
        tk.Button(delete_box, text="Delete Book", command=self.delete_book).grid(row=1, column=0, columnspan=2, pady=8)

    def _row(self, parent, label, r):
        tk.Label(parent, text=label).grid(row=r, column=0, sticky="w", padx=5, pady=3)
        e = tk.Entry(parent, width=40)
        e.grid(row=r, column=1, padx=5, pady=3)
        return e

    def refresh_admin_view(self):
        user = self.app.controller.get_current_user()
        if not user:
            self.status.config(text="Bạn chưa đăng nhập.")
        else:
            self.status.config(text=f"Đang đăng nhập: {user.full_name} ({user.role})")

    def add_book(self):
        isbn = self.isbn_entry.get().strip()
        title = self.title_entry.get().strip()
        author_id = self.author_entry.get().strip()
        category_id = self.category_entry.get().strip()
        qty = self.qty_entry.get().strip()

        try:
            author_id = int(author_id)
            category_id = int(category_id)
            qty = int(qty)
        except:
            messagebox.showerror("Lỗi", "Author ID, Category ID, Quantity phải là số!")
            return

        ok, msg = self.app.controller.admin_add_book(isbn, title, author_id, category_id, qty)
        if ok:
            messagebox.showinfo("Admin", msg)
        else:
            messagebox.showerror("Admin", msg)

    def delete_book(self):
        book_id = self.delete_id_entry.get().strip()
        ok, msg = self.app.controller.admin_delete_book(book_id)
        if ok:
            messagebox.showinfo("Admin", msg)
        else:
            messagebox.showerror("Admin", msg)
