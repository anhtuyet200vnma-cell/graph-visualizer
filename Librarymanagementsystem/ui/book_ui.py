import tkinter as tk
from tkinter import ttk


class BookUI(tk.Frame):
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

        tk.Label(self, text="QUẢN LÝ SÁCH", font=("Arial", 22, "bold")).pack(pady=10)

        # ===== DANH SÁCH SÁCH (DEMO - 5 CUỐN VIỆT NAM) =====
        self.demo_books = [
            ("VN001", "Dế Mèn Phiêu Lưu Ký", "Tô Hoài", 10),
            ("VN002", "Tắt Đèn", "Ngô Tất Tố", 7),
            ("VN003", "Lão Hạc", "Nam Cao", 8),
            ("VN004", "Số Đỏ", "Vũ Trọng Phụng", 5),
            ("VN005", "Tuổi Thơ Dữ Dội", "Phùng Quán", 6),
        ]

        # ===== BẢNG HIỂN THỊ =====
        frame_table = tk.Frame(self)
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("book_id", "title", "author", "qty")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)

        self.tree.heading("book_id", text="Book ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("qty", text="Quantity")

        self.tree.column("book_id", width=120, anchor="center")
        self.tree.column("title", width=350)
        self.tree.column("author", width=220)
        self.tree.column("qty", width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # ===== NÚT REFRESH =====
        tk.Button(self, text="Refresh danh sách (Demo)", width=25, command=self.load_demo_books).pack(pady=10)

    def load_demo_books(self):
        # Xóa dữ liệu cũ trong bảng
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Load dữ liệu demo
        for row in self.demo_books:
            self.tree.insert("", tk.END, values=row)
