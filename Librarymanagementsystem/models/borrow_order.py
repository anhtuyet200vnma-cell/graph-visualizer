"""
- Mục đích: Quản lý phiếu mượn sách (Borrow Order)
- Phiếu mượn là 1 "đơn" chứa thông tin mượn ngày nào, hạn trả ngày nào, đã trả hay chưa.
"""
from datetime import date

class BorrowOrder:
    """
    Lớp BorrowOrder đại diện cho 1 phiếu mượn.

    Thuộc tính:
    - borrow_id: mã phiếu mượn (số nguyên dương)
    - borrow_date: ngày mượn (date)
    - due_date: hạn trả (date)
    - return_date: ngày trả thực tế (date hoặc None nếu chưa trả)
    - status: trạng thái hiện tại (Borrowed / Returned / Overdue)
    """

    def __init__(self, borrow_id: int, borrow_date: date, due_date: date):
        # 1) Kiểm tra borrow_id hợp lệ
        if not isinstance(borrow_id, int) or borrow_id <= 0:
            raise ValueError("borrow_id phải là số nguyên dương (> 0)")

        # 2) Kiểm tra borrow_date phải là kiểu date
        if not isinstance(borrow_date, date):
            raise ValueError("borrow_date phải là kiểu datetime.date")

        # 3) Kiểm tra due_date phải là kiểu date
        if not isinstance(due_date, date):
            raise ValueError("due_date phải là kiểu datetime.date")

        # 4) Hạn trả không được nhỏ hơn ngày mượn
        if due_date < borrow_date:
            raise ValueError("due_date không được nhỏ hơn borrow_date")

        # 5) Gán thuộc tính
        self.borrow_id = borrow_id
        self.borrow_date = borrow_date
        self.due_date = due_date

        # Khi mới tạo phiếu mượn: chưa có ngày trả
        self.return_date = None

        # Khi mới tạo phiếu mượn: trạng thái là Borrowed
        self.status = "Borrowed"

    def create_order(self):
        """
        Tạo phiếu mượn (khởi tạo trạng thái ban đầu).

        Thực tế tạo phiếu mượn thường là:
        - status = Borrowed
        - return_date = None
        """
        self.status = "Borrowed"
        self.return_date = None
        return True

    def mark_as_borrowed(self):
        """
        Đánh dấu phiếu đang mượn.
        """
        self.status = "Borrowed"

    def mark_as_returned(self, return_date: date = None):
        """
        Đánh dấu đã trả sách.

        return_date:
        - Nếu không truyền vào: hệ thống lấy ngày hiện tại (date.today())
        - Nếu truyền vào: phải là kiểu date
        """
        if return_date is None:
            return_date = date.today()

        if not isinstance(return_date, date):
            raise ValueError("return_date phải là kiểu datetime.date")

        # Ngày trả không được trước ngày mượn
        if return_date < self.borrow_date:
            raise ValueError("return_date không được nhỏ hơn borrow_date")

        # Gán ngày trả thực tế + đổi trạng thái
        self.return_date = return_date
        self.status = "Returned"

    def is_overdue(self, current_date: date = None) -> bool:
        """
        Kiểm tra phiếu có quá hạn không.

        Quy tắc:
        - Nếu đã trả: so return_date với due_date
        - Nếu chưa trả: so current_date với due_date
        """
        if current_date is None:
            current_date = date.today()

        # Nếu đã trả, xét dựa trên ngày trả
        if self.return_date is not None:
            return self.return_date > self.due_date

        # Nếu chưa trả, xét dựa trên ngày hiện tại
        return current_date > self.due_date

    def calculate_overdue_days(self, current_date: date = None) -> int:
        """
        Tính số ngày quá hạn.

        Quy tắc:
        - Nếu đã trả: dùng return_date
        - Nếu chưa trả: dùng current_date
        - Nếu chưa quá hạn: trả về 0
        """
        if current_date is None:
            current_date = date.today()

        # end_date là mốc để tính trễ hạn
        # nếu đã trả -> end_date = return_date
        # nếu chưa trả -> end_date = current_date
        end_date = self.return_date if self.return_date else current_date

        # Nếu end_date <= due_date thì chưa trễ
        if end_date <= self.due_date:
            return 0

        # Nếu trễ: tính số ngày chênh lệch
        return (end_date - self.due_date).days

    def get_status(self, current_date: date = None) -> str:
        """
        Lấy trạng thái phiếu mượn theo logic chuẩn:

        - Nếu đã trả -> Returned
        - Nếu chưa trả mà quá hạn -> Overdue
        - Nếu chưa trả và chưa quá hạn -> Borrowed
        """
        if self.return_date is not None:
            return "Returned"

        if self.is_overdue(current_date):
            return "Overdue"

        return "Borrowed"

    def __str__(self):
        """
        In object BorrowOrder rõ ràng hơn.
        """
        return (
            f"BorrowOrder(id={self.borrow_id}, borrow_date={self.borrow_date}, "
            f"due_date={self.due_date}, return_date={self.return_date}, status={self.get_status()})"
        )
