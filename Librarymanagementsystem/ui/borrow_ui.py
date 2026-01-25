import tkinter as tk
from tkinter import messagebox


class BorrowUI(tk.Frame):
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
        tk.Label(self, text="MƯỢN / TRẢ SÁCH", font=("Arial", 18, "bold")).pack(pady=10)

        box = tk.Frame(self)
        box.pack(pady=10)

        tk.Label(box, text="Nhập Book ID:").grid(row=0, column=0, sticky="w", pady=5)
        self.book_id_entry = tk.Entry(box, width=35)
        self.book_id_entry.grid(row=0, column=1, pady=5)

        btns = tk.Frame(self)
        btns.pack(pady=10)

        tk.Button(btns, text="Mượn sách", width=15, command=self.borrow).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Trả sách", width=15, command=self.return_book).grid(row=0, column=1, padx=5)

        self.result_label = tk.Label(self, text="", fg="blue")
        self.result_label.pack(pady=10)

    def borrow(self):
        book_id = self.book_id_entry.get().strip()
        ok, msg = self.app.controller.borrow_book(book_id)
        if ok:
            messagebox.showinfo("Borrow", msg)
        else:
            messagebox.showerror("Borrow", msg)
        self.result_label.config(text=msg)

    def return_book(self):
        book_id = self.book_id_entry.get().strip()
        ok, msg = self.app.controller.return_book(book_id)
        if ok:
            messagebox.showinfo("Return", msg)
        else:
            messagebox.showerror("Return", msg)
        self.result_label.config(text=msg)
