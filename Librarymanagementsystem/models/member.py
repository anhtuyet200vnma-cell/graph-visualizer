from models.user import User
from models.book import Book

class Member(User):
    def __init__(
        self,
        user_id: int,
        username: str,
        password: str,
        email: str,
        full_name: str,
        phone_number: str,
        status: str,
        borrowing_limit: int,
        penalty_status: bool
    ):
        super().__init__(
            user_id,
            username,
            password,
            email,
            full_name,
            phone_number,
            status
        )
        self.borrowing_limit = borrowing_limit
        self.penalty_status = penalty_status
        self.borrowed_books: list[Book] = []

    def borrowBooks(self, book: Book) -> bool:
        if self.penalty_status:
            print("Cannot borrow books due to penalty.")
            return False

        if len(self.borrowed_books) >= self.borrowing_limit:
            print("Borrowing limit reached.")
            return False

        if book.borrow():
            self.borrowed_books.append(book)
            print(f"Borrowed book: {book.title}")
            return True

        print("Book is not available.")
        return False

    def returnBooks(self, book: Book) -> bool:
        if book in self.borrowed_books:
            book.returnBook()
            self.borrowed_books.remove(book)
            print(f"Returned book: {book.title}")
            return True

        print("This book was not borrowed by the member.")
        return False

    def viewBorrowingHistory(self):
        if not self.borrowed_books:
            print("No books currently borrowed.")
            return

        print("Borrowed books:")
        for book in self.borrowed_books:
            print(f"- {book.title}")
