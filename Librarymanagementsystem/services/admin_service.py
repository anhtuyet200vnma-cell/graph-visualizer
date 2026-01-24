# services/borrow_service.py
from utils.file_handler import load_json, save_json
from datetime import datetime, timedelta
import uuid
from config import MAX_BORROW_DAYS


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

        # 1. Check user
        user = next((u for u in users if u["user_id"] == user_id), None)
        if not user or user["status"] != "ACTIVE":
            return False

        # 2. Check borrowing limit
        current_borrows = [
            b for b in borrows
            if b["user_id"] == user_id and b["status"] == "BORROWED"
        ]
        if len(current_borrows) >= user["borrowing_limit"]:
            return False

        # 3. Check book
        book = next((b for b in books if b["book_id"] == book_id), None)
        if not book or book["available_copies"] <= 0:
            return False

        # 4. Update book
        book["available_copies"] -= 1

        # 5. Create borrow order
        borrows.append({
            "borrow_id": str(uuid.uuid4()),
            "user_id": user_id,
            "book_id": book_id,
            "borrow_date": datetime.now().isoformat(),
            "due_date": (datetime.now() + timedelta(days=MAX_BORROW_DAYS)).isoformat(),
            "status": "BORROWED"
        })

        save_json(self.book_path, books)
        save_json(self.borrow_path, borrows)
        return True

    def return_book(self, user_id: int, book_id: int) -> bool:
        borrows = load_json(self.borrow_path)
        books = load_json(self.book_path)

        borrow = next(
            (b for b in borrows
             if b["user_id"] == user_id
             and b["book_id"] == book_id
             and b["status"] == "BORROWED"),
            None
        )
        if not borrow:
            return False

        borrow["status"] = "RETURNED"
        borrow["return_date"] = datetime.now().isoformat()

        book = next((b for b in books if b["book_id"] == book_id), None)
        if book:
            book["available_copies"] += 1

        save_json(self.borrow_path, borrows)
        save_json(self.book_path, books)
        return True
