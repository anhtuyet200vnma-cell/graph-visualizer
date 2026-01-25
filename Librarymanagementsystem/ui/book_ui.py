class BookUI:
    def __init__(self):
        # Demo data
        self.books = [
            {"book_id": "B001", "title": "Clean Code"},
            {"book_id": "B002", "title": "Python Crash Course"},
            {"book_id": "B003", "title": "Database System Concepts"},
        ]

    def show_books(self):
        print("\n========== DANH SÁCH SÁCH ==========")
        for b in self.books:
            print(f"- {b['book_id']} | {b['title']}")

    def search_books(self):
        keyword = input("Nhập từ khóa tìm kiếm: ").strip().lower()
        results = [b for b in self.books if keyword in b["title"].lower()]

        print("\n========== KẾT QUẢ ==========")
        if not results:
            print("❌ Không tìm thấy sách.")
        else:
            for b in results:
                print(f"- {b['book_id']} | {b['title']}")
