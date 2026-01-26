from utils.file_handler import read_json, write_json
from services.borrow_service import BorrowService


class AdminService:

    def __init__(self):
        self.users = read_json("data/user.json")
        self.books = read_json("data/book.json")
        self.borrow_service = BorrowService()

    # ==================================================
    # MEMBER MANAGEMENT
    # ==================================================

    def get_all_members(self):
        return [u for u in self.users if u.get("role") == "MEMBER"]

    def add_member(self, user_data):
        new_id = max(u["user_id"] for u in self.users) + 1

        user_data["user_id"] = new_id
        user_data["role"] = "MEMBER"
        user_data["status"] = "ACTIVE"

        self.users.append(user_data)
        write_json("data/user.json", self.users)
        return True

    def update_member(self, user_id, new_data):
        for u in self.users:
            if u["user_id"] == user_id and u["role"] == "MEMBER":
                u.update(new_data)
                write_json("data/user.json", self.users)
                return True
        return False

    def delete_member(self, user_id):
        self.users = [u for u in self.users if u["user_id"] != user_id]
        write_json("data/user.json", self.users)
        return True

    # ==================================================
    # BOOK MANAGEMENT
    # ==================================================

    def get_all_books(self):
        return self.books

    def add_book(self, book_data):
        new_id = max(b["book_id"] for b in self.books) + 1
        book_data["book_id"] = new_id
        self.books.append(book_data)
        write_json("data/book.json", self.books)
        return True

    def update_book(self, book_id, new_data):
        for b in self.books:
            if b["book_id"] == book_id:
                b.update(new_data)
                write_json("data/book.json", self.books)
                return True
        return False

    def delete_book(self, book_id):
        self.books = [b for b in self.books if b["book_id"] != book_id]
        write_json("data/book.json", self.books)
        return True

    # ==================================================
    # BORROW REQUEST PROCESS
    # ==================================================

    def approve_request(self, request_id):
        return self.borrow_service.approve_request(request_id)

    def reject_request(self, request_id, reason="Rejected"):
        return self.borrow_service.reject_request(request_id, reason)
