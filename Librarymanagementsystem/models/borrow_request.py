
from datetime import date


REQUEST_STATUS = {
    "PENDING": "PENDING",
    "APPROVED": "APPROVED",
    "REJECTED": "REJECTED",
    "CANCELLED": "CANCELLED",
}


class BorrowRequest:
    """
    Lớp BorrowRequest đại diện cho 1 yêu cầu mượn sách.

    Thuộc tính:
    - request_id: mã yêu cầu
    - request_date: ngày tạo yêu cầu
    - status: trạng thái (PENDING / APPROVED / REJECTED / CANCELLED)
    - requested_by: người tạo request (Member hoặc id/string tạm)
    - books: danh sách book_id
    - approval_date: ngày duyệt
    - approver: admin duyệt
    - reject_reason: lý do từ chối (nếu có)
    """

    def __init__(self, request_id: int, requested_by, books: list, request_date: date = None):
        # validate request_id
        if not isinstance(request_id, int) or request_id <= 0:
            raise ValueError("request_id phải là số nguyên dương (> 0)")

        # validate books
        if not isinstance(books, list) or len(books) == 0:
            raise ValueError("books phải là list và có ít nhất 1 sách")

        self.request_id = request_id
        self.requested_by = requested_by
        self.books = books

        self.request_date = request_date if request_date else date.today()
        self.status = REQUEST_STATUS["PENDING"]

        self.approval_date = None
        self.approver = None
        self.reject_reason = None


    def createRequest(self):
        """
        Tạo request mới (reset trạng thái về PENDING).
        """
        self.status = REQUEST_STATUS["PENDING"]
        self.approval_date = None
        self.approver = None
        self.reject_reason = None
        return True

    def checkBorrowingCondition(self):
        """
        ✅ Theo sơ đồ Class Diagram: checkBorrowingCondition()
        Mục tiêu: kiểm tra điều kiện mượn trước khi duyệt.

        Ở level hiện tại (chưa có service/database đầy đủ),
        hàm này trả về tuple (is_valid, message).

        Sau này có thể mở rộng:
        - check member penaltyStatus
        - check borrowing limit (max 5)
        - check book availability
        """
        # Nếu chưa có hệ thống Member thật → cho pass mặc định
        # Nhưng vẫn validate logic cơ bản:
        if self.status != REQUEST_STATUS["PENDING"]:
            return False, "Chỉ request trạng thái PENDING mới được kiểm tra điều kiện"

        if len(self.books) == 0:
            return False, "Request không có sách để mượn"

        # Rule demo: không được mượn quá 5 sách/lần
        if len(self.books) > 5:
            return False, "Vượt quá số lượng sách mượn tối đa (5)"

        return True, "OK"

    def approve(self, admin):
        """
        Admin duyệt request.

        Quy tắc:
        - Chỉ duyệt khi đang PENDING
        - CheckBorrowingCondition() phải pass
        """
        if self.status != REQUEST_STATUS["PENDING"]:
            raise ValueError("Chỉ request PENDING mới được approve")

        valid, msg = self.checkBorrowingCondition()
        if not valid:
            raise ValueError(f"Không đủ điều kiện mượn: {msg}")

        self.status = REQUEST_STATUS["APPROVED"]
        self.approver = admin
        self.approval_date = date.today()
        return True

    def reject(self, admin, reason: str = "No reason"):
        """
        Admin từ chối request.
        """
        if self.status != REQUEST_STATUS["PENDING"]:
            raise ValueError("Chỉ request PENDING mới được reject")

        self.status = REQUEST_STATUS["REJECTED"]
        self.approver = admin
        self.approval_date = date.today()
        self.reject_reason = reason
        return True

    def cancelRequest(self, member):
        """
        Member huỷ request khi còn PENDING.
        """
        if self.status != REQUEST_STATUS["PENDING"]:
            raise ValueError("Chỉ request PENDING mới được cancel")

        # Check đúng người tạo
        if member != self.requested_by:
            raise ValueError("Chỉ người tạo request mới có quyền cancel")

        self.status = REQUEST_STATUS["CANCELLED"]
        return True

    def get_status(self):
        return self.status

    def __str__(self):
        return f"BorrowRequest(id={self.request_id}, status={self.status}, books={len(self.books)})"
