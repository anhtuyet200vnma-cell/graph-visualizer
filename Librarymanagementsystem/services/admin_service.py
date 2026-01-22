from models.book import Book
from models.user import User

class AdminService:
    """
    ADMINISTRATIVE FUNCTIONS (1.3 trong đặc tả)
    """

    @staticmethod
    def addMember(members: list[User], member: User) -> bool:
        """Thêm thành viên mới (1.3)"""
        members.append(member)
        print(f"Member {member.full_name} added.")
        return True

    @staticmethod
    def deleteMember(members: list[User], member: User) -> bool:
        """Xóa thành viên (1.3)"""
        if member in members:
            members.remove(member)
            print(f"Member {member.full_name} deleted.")
            return True
        return False

    @staticmethod
    def addBook(books: list[Book], book: Book) -> bool:
        """Thêm sách mới (1.3)"""
        books.append(book)
        print(f"Book '{book.title}' added.")
        return True

    @staticmethod
    def deleteBook(books: list[Book], book: Book) -> bool:
        """Xóa sách (1.3)"""
        if book in books:
            books.remove(book)
            print(f"Book '{book.title}' deleted.")
            return True
        return False

    # SỬA: Sử dụng dict đơn giản thay vì BorrowRequest model
    @staticmethod
    def approveBorrowRequest(request: dict) -> bool:
        """Phê duyệt yêu cầu mượn (1.3)"""
        request['status'] = "APPROVED"
        print(f"Borrow request approved.")
        return True

    @staticmethod
    def rejectBorrowRequest(request: dict) -> bool:
        """Từ chối yêu cầu mượn (1.3)"""
        request['status'] = "REJECTED"
        print(f"Borrow request rejected.")
        return True