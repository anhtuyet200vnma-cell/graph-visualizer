
from datetime import date


class BorrowOrder:
    """
    Lớp BorrowOrder đại diện cho 1 phiếu mượn.

    Thuộc tính:
    - borrow_id: mã phiếu mượn
    - borrow_date: ngày mượn
    - due_date: hạn trả
    - return_date: (GIỮ LẠI nullable để đúng sơ đồ DB, nhưng không xử lý mark_as_returned tại đây)
    - status: Borrowed / Returned / Overdue
    - books: list book_id đơn giản (tạm), hoặc list BorrowOrderDetail ở mức chuẩn hơn
    """

    def __init__(self, borrow_id: int, borrow_date: date, due_date: date):
        if not isinstance(borrow_id, int) or borrow_id <= 0:
            raise ValueError("borrow_id phải là số nguyên dương (> 0)")

        if not isinstance(borrow_date, date):
            raise ValueError("borrow_date phải là kiểu datetime.date")

        if not isinstance(due_date, date):
            raise ValueError("due_date phải là kiểu datetime.date")

        if due_date < borrow_date:
            raise ValueError("due_date không được nhỏ hơn borrow_date")

        self.borrow_id = borrow_id
        self.borrow_date = borrow_date
        self.due_date = due_date

        # Có trong sơ đồ data model nên vẫn giữ
        self.return_date = None

        self.status = "Borrowed"
        self.books = []  # list book_id

    def create_order(self):
        """
        Tạo phiếu mượn (trạng thái ban đầu).
        """
        self.status = "Borrowed"
        self.return_date = None
        return True

    def mark_as_borrowed(self):
        """
        Đánh dấu đang mượn.
        """
        self.status = "Borrowed"
    def add_book(self, book_id: str):
        """
        Thêm sách vào đơn mượn (dạng đơn giản).
        """
        if not book_id or not isinstance(book_id, str):
            raise ValueError("book_id phải là string hợp lệ")

        self.books.append(book_id)

    def is_overdue(self, current_date: date = None) -> bool:
        """
        Kiểm tra đơn có quá hạn không (theo logic header).

        - Nếu return_date có (dữ liệu DB) → so sánh return_date với due_date
        - Nếu chưa có return_date → so current_date với due_date
        """
        if current_date is None:
            current_date = date.today()

        if self.return_date is not None:
            return self.return_date > self.due_date

        return current_date > self.due_date

    def calculate_overdue_days(self, current_date: date = None) -> int:
        """
        Tính số ngày quá hạn (ở level BorrowOrder header).
        """
        if current_date is None:
            current_date = date.today()

        end_date = self.return_date if self.return_date else current_date

        if end_date <= self.due_date:
            return 0

        return (end_date - self.due_date).days

    def get_status(self, current_date: date = None) -> str:
        """
        Trả về trạng thái đơn:
        - Nếu return_date có → Returned
        - Nếu quá hạn → Overdue
        - Còn lại → Borrowed
        """
        if self.return_date is not None:
            return "Returned"

        if self.is_overdue(current_date):
            return "Overdue"

        return "Borrowed"

    def __str__(self):
        return f"BorrowOrder(id={self.borrow_id}, status={self.get_status()}, books={len(self.books)})"
