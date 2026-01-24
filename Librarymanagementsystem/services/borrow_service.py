from utils.file_handler import load_json, save_json
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

    def borrow_book(self, user_id: int, book_id: int) -> bool:
        borrows = load_json(self.borrow_path)
        books = load_json(self.book_path)
        users = load_json(self.user_path)

        user = next((u for u in users if u["user_id"] == user_id), None)
        if not user or user["status"] != "ACTIVE":
            return False

        current = [
            b for b in borrows
            if b["user_id"] == user_id and b["status"] == "BORROWED"
        ]
        if len(current) >= user["borrowing_limit"]:
            return False

        book = next((b for b in books if b["book_id"] == book_id), None)
        if not book or book["available_copies"] <= 0:
            return False

        book["available_copies"] -= 1

        borrows.append({
            "borrow_id": str(uuid.uuid4()),
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=MAX_BORROW_DAYS)).isoformat(),
            "return_date": None,
            "status": "BORROWED"
        })

        save_json(self.book_path, books)
        save_json(self.borrow_path, borrows)
        return True
