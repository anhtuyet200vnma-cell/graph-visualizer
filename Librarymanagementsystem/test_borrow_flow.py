from datetime import date
from Librarymanagementsystem.models import BorrowRequest, BorrowOrder

# giả lập Member/Admin bằng string (sau này nhóm có class Member/Admin thì thay)
member = "member_01"
admin = "admin_01"

# 1) Member tạo request
req = BorrowRequest(request_id=1, requested_by=member, books=["B001", "B002"])
print(req)

# 2) Admin approve
req.approve(admin)
print(req.get_status())

# 3) Tạo order sau khi approve
order = BorrowOrder(borrow_id=1, borrow_date=date.today(), due_date=date(2026, 2, 1), request_id=req.request_id)
order.add_book("B001")
order.add_book("B002")

print(order)
