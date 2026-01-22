from models.user import User

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
        self.borrowed_books = []   # chỉ lưu dữ liệu