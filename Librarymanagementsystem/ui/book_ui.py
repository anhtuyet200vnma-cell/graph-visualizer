import tkinter as tk
from tkinter import messagebox


class BookUI(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        tk.Button(
            self,
            text="⬅ Quay lại",
            width=15,
            command=lambda: app.show("main")
        ).pack(anchor="w", padx=10, pady=5)
        self.app = app
        self.books_cache = []
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="DANH SÁCH SÁCH", font=("Arial", 18, "bold")).pack(pady=10)

        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="Từ khóa:").pack(side="left")
        self.keyword_entry = tk.Entry(search_frame, width=40)
        self.keyword_entry.pack(side="left", padx=5)

        tk.Button(search_frame, text="Tìm", command=self.search).pack(side="left", padx=5)
        tk.Button(search_frame, text="Tải lại", command=self.load_books).pack(side="left", padx=5)

        body = tk.Frame(self)
        body.pack(fill="both", expand=True, pady=10)

        self.listbox = tk.Listbox(body, width=60, height=15)
        self.listbox.pack(side="left", fill="both", expand=True)

        right = tk.Frame(body)
        right.pack(side="left", fill="y", padx=10)

        tk.Button(right, text="Xem chi tiết", width=20, command=self.view_details).pack(pady=5)

        self.detail_text = tk.Text(right, width=35, height=15)
        self.detail_text.pack()

    def load_books(self):
        self.books_cache = self.app.controller.get_all_books()
        self.refresh_list(self.books_cache)

    def refresh_list(self, books):
        self.listbox.delete(0, tk.END)
        for b in books:
            # Book object trong project bạn có thể có book_id và title
            self.listbox.insert(tk.END, f"{b.book_id} - {b.title}")

    def search(self):
        keyword = self.keyword_entry.get().strip()
        if not keyword:
            self.load_books()
            return

        results = self.app.controller.search_books(keyword)
        self.refresh_list(results)

    def view_details(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Bạn chưa chọn sách nào.")
            return

        line = self.listbox.get(selected[0])
        book_id = line.split(" - ")[0].strip()

        detail = self.app.controller.view_book_details(book_id)
        self.detail_text.delete("1.0", tk.END)

        if detail is None:
            self.detail_text.insert(tk.END, "Không tìm thấy chi tiết sách.")
        else:
            # BookService.viewBookDetails(book) có thể trả string
            self.detail_text.insert(tk.END, str(detail))
