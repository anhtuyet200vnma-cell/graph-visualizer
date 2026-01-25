class BorrowUI:
    def __init__(self):
        pass

    def borrow_book(self):
        book_id = input("Nhập Book ID muốn mượn: ").strip()
        print(f"✅ Đã gửi yêu cầu mượn sách: {book_id}")

    def return_book(self):
        book_id = input("Nhập Book ID muốn trả: ").strip()
        print(f"✅ Đã gửi yêu cầu trả sách: {book_id}")
