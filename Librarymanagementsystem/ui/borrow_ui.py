import tkinter as tk
from tkinter import messagebox


class BorrowUI(tk.Frame):
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

        tk.Label(self, text="MƯỢN / TRẢ SÁCH", font=("Arial", 22, "bold")).pack(pady=10)

        # ===== FORM MƯỢN SÁCH =====
        frame_borrow = tk.LabelFrame(self, text="Mượn sách (Demo)", padx=15, pady=10)
        frame_borrow.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_borrow, text="User ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_user = tk.Entry(frame_borrow, width=40)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_borrow, text="Book ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_book = tk.Entry(frame_borrow, width=40)
        self.entry_book.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame_borrow, text="Borrow", width=15, command=self.borrow_demo).grid(
            row=2, column=1, sticky="w", padx=5, pady=10
        )

        # ===== FORM TRẢ SÁCH =====
        frame_return = tk.LabelFrame(self, text="Trả sách (Demo)", padx=15, pady=10)
        frame_return.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_return, text="User ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_user_return = tk.Entry(frame_return, width=40)
        self.entry_user_return.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_return, text="Book ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_book_return = tk.Entry(frame_return, width=40)
        self.entry_book_return.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame_return, text="Return", width=15, command=self.return_demo).grid(
            row=2, column=1, sticky="w", padx=5, pady=10
        )

    def borrow_demo(self):
        user_id = self.entry_user.get().strip()
        book_id = self.entry_book.get().strip()

        if not user_id or not book_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập User ID và Book ID.")
            return

        messagebox.showinfo("Thành công (Demo)", f"Đã tạo yêu cầu mượn sách (demo)\nUser: {user_id}\nBook: {book_id}")
        self.entry_user.delete(0, tk.END)
        self.entry_book.delete(0, tk.END)

    def return_demo(self):
        user_id = self.entry_user_return.get().strip()
        book_id = self.entry_book_return.get().strip()

        if not user_id or not book_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập User ID và Book ID.")
            return

        messagebox.showinfo("Thành công (Demo)", f"Đã trả sách (demo)\nUser: {user_id}\nBook: {book_id}")
        self.entry_user_return.delete(0, tk.END)
        self.entry_book_return.delete(0, tk.END)
