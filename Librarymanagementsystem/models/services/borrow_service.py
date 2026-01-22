from models.book import Book
from models.member import Member

class BorrowService:

    @staticmethod
    def checkBorrowingConditions(member: Member, book: Book) -> bool:
        if member.penalty_status:
            print("Member is under penalty.")
            return False

        if len(member.borrowed_books) >= member.borrowing_limit:
            print("Borrowing limit reached.")
            return False

        if book.available_quantity <= 0:
            print("Book is not available.")
            return False

        if book.status != "AVAILABLE":
            print("Book status is not AVAILABLE.")
            return False

        return True

    @staticmethod
    def borrowBook(member: Member, book: Book) -> bool:
        if not BorrowService.checkBorrowingConditions(member, book):
            return False

        book.decreaseAvailable()
        member.borrowed_books.append(book)

        print(f"{member.full_name} borrowed '{book.title}'")
        return True

    @staticmethod
    def returnBook(member: Member, book: Book) -> bool:
        if book not in member.borrowed_books:
            print("This book was not borrowed by the member.")
            return False

        book.increaseAvailable()
        member.borrowed_books.remove(book)

        print(f"{member.full_name} returned '{book.title}'")
        return True
