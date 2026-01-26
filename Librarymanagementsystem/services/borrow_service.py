# services/borrow_service.py
from utils.file_handler_fix import load_json, save_json
from datetime import datetime, timedelta
from config import MAX_BORROW_DAYS
import uuid


class BorrowService:
    def __init__(
        self,
        borrow_path="data/borrow_orders.json",
        book_path="data/books.json",
        user_path="data/users.json"
    ):
        self.borrow_path = borrow_path
        self.book_path = book_path
        self.user_path = user_path

    def borrow_book(self, user_id: int, book_id: str) -> dict:
        """
        Mượn sách
        Trả về: {"success": bool, "message": str, "borrow_id": str}
        """
        try:
            borrows = load_json(self.borrow_path)
            books = load_json(self.book_path)
            users = load_json(self.user_path)

            # 1. Kiểm tra user
            user = next((u for u in users if u.get("user_id") == user_id), None)
            if not user:
                return {"success": False, "message": "User không tồn tại"}
            
            if user.get("status") != "ACTIVE":
                return {"success": False, "message": "Tài khoản không hoạt động"}

            # 2. Kiểm tra giới hạn mượn
            current_borrows = [
                b for b in borrows
                if b.get("user_id") == user_id and b.get("status") == "BORROWED"
            ]
            
            borrowing_limit = user.get("borrowing_limit", 5)
            if len(current_borrows) >= borrowing_limit:
                return {"success": False, "message": f"Đã đạt giới hạn mượn ({borrowing_limit} sách)"}

            # 3. Kiểm tra sách
            book = next((b for b in books if b.get("book_id") == book_id), None)
            if not book:
                return {"success": False, "message": "Sách không tồn tại"}
            
            available_copies = book.get("available_quantity", book.get("available_copies", 0))
            if available_copies <= 0:
                return {"success": False, "message": "Sách đã hết"}

            # 4. Cập nhật số lượng sách
            book["available_quantity"] = available_copies - 1
            book["available_copies"] = available_copies - 1

            # 5. Tạo đơn mượn
            borrow_id = str(uuid.uuid4())
            borrow_data = {
                "borrow_id": borrow_id,
                "user_id": user_id,
                "book_id": book_id,
                "books": [book_id],
                "borrow_date": datetime.now().isoformat(),
                "due_date": (datetime.now() + timedelta(days=MAX_BORROW_DAYS)).isoformat(),
                "return_date": None,
                "status": "BORROWED"
            }
            
            borrows.append(borrow_data)

            # 6. Lưu dữ liệu
            save_json(self.book_path, books)
            save_json(self.borrow_path, borrows)
            
            return {
                "success": True, 
                "message": "Mượn sách thành công", 
                "borrow_id": borrow_id
            }
            
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def return_book(self, borrow_id: str) -> dict:
        """
        Trả sách
        Trả về: {"success": bool, "message": str}
        """
        try:
            borrows = load_json(self.borrow_path)
            books = load_json(self.book_path)

            # Tìm đơn mượn
            borrow = next((b for b in borrows if b.get("borrow_id") == borrow_id), None)
            if not borrow:
                return {"success": False, "message": "Không tìm thấy đơn mượn"}
            
            if borrow.get("status") != "BORROWED":
                return {"success": False, "message": "Sách đã được trả trước đó"}

            # Cập nhật đơn mượn
            borrow["status"] = "RETURNED"
            borrow["return_date"] = datetime.now().isoformat()

            # Cập nhật số lượng sách
            book_id = borrow.get("book_id")
            if book_id:
                book = next((b for b in books if b.get("book_id") == book_id), None)
                if book:
                    available_copies = book.get("available_quantity", book.get("available_copies", 0))
                    book["available_quantity"] = available_copies + 1
                    book["available_copies"] = available_copies + 1
            else:
                # Nếu borrow có field books (list)
                books_list = borrow.get("books", [])
                for book_id in books_list:
                    book = next((b for b in books if b.get("book_id") == book_id), None)
                    if book:
                        available_copies = book.get("available_quantity", book.get("available_copies", 0))
                        book["available_quantity"] = available_copies + 1
                        book["available_copies"] = available_copies + 1

            # Lưu dữ liệu
            save_json(self.borrow_path, borrows)
            save_json(self.book_path, books)
            
            return {"success": True, "message": "Trả sách thành công"}
            
        except Exception as e:
            print(f"Error returning book: {e}")
            return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}

    def get_user_borrows(self, user_id: int):
        """Lấy danh sách đơn mượn của user"""
        try:
            borrows = load_json(self.borrow_path)
            # Special case: if user_id is 0 or None, return all borrows for admin
            if user_id == 0 or user_id is None:
                return borrows
            user_borrows = [b for b in borrows if b.get("user_id") == user_id]
            return user_borrows
        except Exception as e:
            print(f"Error getting user borrows: {e}")
            return []

    def get_overdue_borrows(self):
        """Lấy danh sách đơn mượn quá hạn"""
        try:
            borrows = load_json(self.borrow_path)
            now = datetime.now()
            
            overdue = []
            for borrow in borrows:
                if borrow.get("status") == "BORROWED":
                    due_date_str = borrow.get("due_date")
                    if due_date_str:
                        try:
                            due_date = datetime.fromisoformat(due_date_str)
                            if due_date < now:
                                overdue.append(borrow)
                        except:
                            pass
            
            return overdue
        except Exception as e:
            print(f"Error getting overdue borrows: {e}")
            return []