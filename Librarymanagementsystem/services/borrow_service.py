from datetime import date, timedelta, datetime

from models.borrow_request import BorrowRequest
from models.borrow_order import BorrowOrder
from models.borrow_order_detail import BorrowOrderDetail
from models.member import Member
from models.fines import Fine
from models.book import Book

from utils.file_handler import read_json, write_json


BORROW_DAYS = 14


class BorrowService:

    def __init__(self):
        self.books = read_json("data/book.json")
        self.users = read_json("data/user.json")
        self.borrow_requests = read_json("data/borrow_requests.json").get("borrow_requests", [])
        self.borrow_orders = read_json("data/borrow_orders.json").get("borrow_orders", [])
        try:
            self.fines = read_json("data/fine.json")
        except:
            self.fines = []

    # ================= LOAD BASIC OBJECT =================

    def _load_member(self, user_id):
        for u in self.users:
            if u["user_id"] == user_id:
                return Member(
                    u["user_id"],
                    u["username"],
                    u["password"],
                    u["email"],
                    u["full_name"],
                    u["phone_number"],
                    u["status"],
                    borrowing_limit=5,
                    penalty_status=False
                )
        return None

    def _load_book(self, book_id):
        for b in self.books:
            if b["book_id"] == book_id:
                return Book(
                    b["book_id"],
                    b["title"],
                    "",
                    b["publication_year"],
                    b["quantity"],
                    b["available_quantity"],
                    b["status"],
                    None
                )
        return None

    # ====================================================
    # 1. MEMBER CREATE BORROW REQUEST
    # ====================================================

    def create_borrow_request(self, user_id, book_id):

        new_id = len(self.borrow_requests) + 1

        req = BorrowRequest(
            request_id=new_id,
            requested_by=user_id,
            books=[book_id]
        )

        self.borrow_requests.append({
            "request_id": new_id,
            "user_id": user_id,
            "book_id": book_id,
            "request_date": str(date.today()),
            "status": "PENDING"
        })

        write_json("data/borrow_requests.json", {"borrow_requests": self.borrow_requests})
        return True, "Tạo yêu cầu mượn thành công"

    # ====================================================
    # 2. ADMIN APPROVE REQUEST
    # ====================================================

    def approve_request(self, request_id):

        for r in self.borrow_requests:
            if r["request_id"] == request_id and r["status"] == "PENDING":

                borrow_id = len(self.borrow_orders) + 1
                borrow_date = date.today()
                due_date = borrow_date + timedelta(days=BORROW_DAYS)

                order = BorrowOrder(borrow_id, borrow_date, due_date)
                order.add_book(r["book_id"])

                self.borrow_orders.append({
                    "borrow_id": borrow_id,
                    "user_id": r["user_id"],
                    "borrow_date": str(borrow_date),
                    "due_date": str(due_date),
                    "status": "BORROWED",
                    "items": [
                        {
                            "book_id": r["book_id"],
                            "item_status": "BORROWED",
                            "condition": "GOOD"
                        }
                    ]
                })

                r["status"] = "APPROVED"

                write_json("data/borrow_orders.json", {"borrow_orders": self.borrow_orders})
                write_json("data/borrow_requests.json", {"borrow_requests": self.borrow_requests})

                return True, "Approve thành công"

        return False, "Không tìm thấy request hoặc request không hợp lệ"

    # ====================================================
    # 3. ADMIN REJECT REQUEST
    # ====================================================

    def reject_request(self, request_id, reason="Rejected"):

        for r in self.borrow_requests:
            if r["request_id"] == request_id and r["status"] == "PENDING":
                r["status"] = "REJECTED"
                r["reason"] = reason
                write_json("data/borrow_requests.json", {"borrow_requests": self.borrow_requests})
                return True, "Đã từ chối request"

        return False, "Không thể reject"

    # ====================================================
    # 4. RETURN BOOK + CREATE FINE
    # ====================================================

    def return_book(self, borrow_id, book_id, condition="GOOD"):

        for order in self.borrow_orders:
            if order["borrow_id"] == borrow_id:

                due_date = datetime.strptime(order["due_date"], "%Y-%m-%d").date()

                for item in order["items"]:
                    if item["book_id"] == book_id:

                        return_date = date.today()
                        item["item_status"] = "RETURNED"
                        item["condition"] = condition
                        item["actual_return_date"] = str(return_date)

                        detail = BorrowOrderDetail(book_id)
                        detail.actual_return_date = return_date
                        detail.condition = condition

                        overdue = detail.calculate_overdue_days(due_date)
                        fine, _ = Fine.create_fine(detail, overdue)

                        if fine:
                            if isinstance(self.fines, list):
                                self.fines.append(fine.to_dict())
                            else:
                                self.fines = [fine.to_dict()]

                            write_json("data/fine.json", self.fines)

                order["status"] = "RETURNED"
                write_json("data/borrow_orders.json", {"borrow_orders": self.borrow_orders})

                return True, "Trả sách thành công"

        return False, "Không tìm thấy borrow order"
