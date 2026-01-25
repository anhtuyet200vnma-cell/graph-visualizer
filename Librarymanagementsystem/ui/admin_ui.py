import tkinter as tk
from tkinter import messagebox


class AdminUI(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # ===== NÚT QUAY LẠI =====
        tk.Button(
            self,
            text="⬅ Quay lại",
            width=15,
            command=lambda: self.app.show("main")
        ).pack(anchor="w", padx=10, pady=5)

        tk.Label(self, text="ADMIN PANEL", font=("Arial", 22, "bold")).pack(pady=10)

        # ===== FORM THÊM SÁCH (DEMO) =====
        frame_add = tk.LabelFrame(self, text="Thêm sách (Demo)", padx=15, pady=10)
        frame_add.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_add, text="ISBN:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_isbn = tk.Entry(frame_add, width=40)
        self.entry_isbn.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Title:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_title = tk.Entry(frame_add, width=40)
        self.entry_title.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Author:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_author = tk.Entry(frame_add, width=40)
        self.entry_author.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_add, text="Quantity:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_quantity = tk.Entry(frame_add, width=40)
        self.entry_quantity.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(frame_add, text="Add Book", width=15, command=self.add_book_demo).grid(
            row=4, column=1, sticky="w", padx=5, pady=10
        )

        # ===== FORM XOÁ SÁCH (DEMO) =====
        frame_del = tk.LabelFrame(self, text="Xóa sách (Demo)", padx=15, pady=10)
        frame_del.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_del, text="Book ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_book_id = tk.Entry(frame_del, width=40)
        self.entry_book_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_del, text="Delete Book", width=15, command=self.delete_book_demo).grid(
            row=1, column=1, sticky="w", padx=5, pady=10
        )

    def add_book_demo(self):
        isbn = self.entry_isbn.get().strip()
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        qty = self.entry_quantity.get().strip()

        if not isbn or not title or not author or not qty:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ ISBN, Title, Author và Quantity.")
            return

        if not qty.isdigit():
            messagebox.showwarning("Sai định dạng", "Quantity phải là số.")
            return

        messagebox.showinfo(
            "Thành công (Demo)",
            f"Đã thêm sách (demo)\nISBN: {isbn}\nTitle: {title}\nAuthor: {author}\nQuantity: {qty}"
        )

        self.entry_isbn.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    def delete_book_demo(self):
        book_id = self.entry_book_id.get().strip()

        if not book_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Book ID để xóa.")
            return

        messagebox.showinfo("Thành công (Demo)", f"Đã xóa sách (demo) có Book ID: {book_id}")
        self.entry_book_id.delete(0, tk.END)
