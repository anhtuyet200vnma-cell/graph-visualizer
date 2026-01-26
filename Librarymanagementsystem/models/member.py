from models.user import User, AccountStatus, Role

class Member(User):
    def __init__(
        self,
        user_id: int,
        username: str,
        password: str,
        email: str,
        full_name: str,
        phone_number: str,
        status: AccountStatus = AccountStatus.ACTIVE,
        borrowing_limit: int = 5,
        penalty_status: bool = False,
        created_at: str | None = None
    ):
        super().__init__(
            user_id=user_id,
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            role=Role.MEMBER,
            status=status,
            created_at=created_at
        )
        self.borrowing_limit = borrowing_limit
        self.penalty_status = penalty_status
        self.borrowed_books = []
    
    def __str__(self):
        return f"Member(id={self.user_id}, username={self.username}, borrowed={len(self.borrowed_books)})"
    
    def can_borrow(self):
        return not self.penalty_status and len(self.borrowed_books) < self.borrowing_limit
    
    def add_borrowed_book(self, book_id):
        if self.can_borrow():
            self.borrowed_books.append(book_id)
            return True
        return False
    
    def remove_borrowed_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False