from utils.file_handler import FileHandler
from utils.session_manager import SessionManager
from utils.helpers import get_current_date

from models.user import User
from models.member import Member
from models.admin import Admin
from models.book import Book
from models.borrow_order import BorrowOrder
from models.waiting_list import WaitingList
from models.book_author import BookAuthor

from services.book_service import BookService
from services.borrow_service import BorrowService
from services.admin_service import AdminService

class LibraryController:
    def __init__(self):
        print(" [System] Đang khởi động LibraryController...")
        self.file_handler = FileHandler()
        self.session_mgr = SessionManager()

        self.users = self._load_users()
        self.books = self._load_books()
        self.borrow_orders = self._load_borrow_orders()
        self.waiting_lists = self._load_waiting_lists()
        self.book_authors = self._load_book_authors()
        
        print(" [System] Đã tải dữ liệu thành công.")

    # QUẢN LÝ DỮ LIỆU & LOAD FILE
    def _load_users(self):
        data = self.file_handler.read_json("data/users.json")
        users_list = []
        for item in data:
        
            if item.get("role") == "admin":

                users_list.append(Admin(**item) if hasattr(Admin, 'from_dict') else User.from_dict(item))
            else:
                users_list.append(Member(**item) if hasattr(Member, 'from_dict') else User.from_dict(item))
        return users_list

    def _load_books(self):
        data = self.file_handler.read_json("data/books.json")
        books_list = []
        for item in data:
            books_list.append(Book.from_dict(item))
        return books_list

    def _load_book_authors(self):
        data = self.file_handler.read_json("data/book_authors.json")
        rels = []
        for item in data:
            rels.append(BookAuthor.from_dict(item))
        return rels

    def _load_borrow_orders(self):
        return []

    def _load_waiting_lists(self):
        return []

    def save_all_data(self):
        """Lưu toàn bộ dữ liệu từ RAM xuống ổ cứng"""
        self.file_handler.write_json("data/users.json", [u.to_dict() for u in self.users])
        self.file_handler.write_json("data/books.json", [b.to_dict() for b in self.books])
        self.file_handler.write_json("data/book_authors.json", [ba.to_dict() for ba in self.book_authors])
        print(" [System] Đã lưu dữ liệu.")

    # XÁC THỰC (AUTHENTICATION)
    def login(self, username, password):
        """Xử lý đăng nhập"""
        user = next((u for u in self.users if u.username == username), None)
        if not user:
            return False, "Tài khoản không tồn tại."
        if user.password != password:
            return False, "Mật khẩu không đúng."
        self.session_mgr.login(user)
        return True, f"Xin chào {user.full_name} ({user.role})!"

    def logout(self):
        self.session_mgr.logout()
        return True, "Đã đăng xuất."
    
    def get_current_user(self):
        return self.session_mgr.get_current_user()

    # QUẢN LÝ SÁCH (BOOK SERVICE)
    def search_books(self, keyword):
        """Tìm sách qua BookService"""
        return BookService.searchBooks(self.books, keyword)

    def get_all_books(self):
        return self.books
    
    def view_book_details(self, book_id):
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book:
            return BookService.viewBookDetails(book)
        return None

    # MƯỢN TRẢ (BORROW SERVICE)
    def borrow_book(self, book_id):
        """Xử lý mượn sách"""
        user = self.session_mgr.get_current_user()
        if not user:
            return False, "Vui lòng đăng nhập để mượn sách."
        book = next((b for b in self.books if b.book_id == book_id), None)
        if not book:
            return False, "Sách không tồn tại."
        if BorrowService.checkBorrowingConditions(user, book):
            BorrowService.borrowBook(user, book) 
            return True, f"Mượn thành công: {book.title}"
        else:
            return False, "Không đủ điều kiện mượn (Hết sách hoặc bị phạt)."

    def return_book(self, book_id):
        """Xử lý trả sách"""
        user = self.session_mgr.get_current_user()
        if not user: return False, "Chưa đăng nhập."
        book = next((b for b in self.books if b.book_id == book_id), None)
        if not book: return False, "Sách không tồn tại."
        if BorrowService.returnBook(user, book):
            return True, f"Đã trả sách: {book.title}"
        return False, "Lỗi: Sách này không nằm trong danh sách đang mượn của bạn."

    # ADMIN (ADMIN SERVICE)
    def admin_add_book(self, book_id, title, description, publication_year, quantity, author_id, category_id):
        """Admin thêm sách mới"""
        user = self.session_mgr.get_current_user()
        if not user or user.role != "admin":
            return False, "Truy cập bị từ chối. Cần quyền Admin."
        return True, "Thêm sách thành công."

        if any(int(b.book_id) == str(book_id) for b in self.books):
            return False, "Book ID đã tồn tại."
        
        quantity = int(quantity)

        new_book = Book(
            book_id=int(book_id),
            title=title,
            publication_year=int(publication_year),
            quantity=quantity,
            available_quantity=quantity,
            status="AVAILABLE",
            author_id=int(author_id),
            category_id=int(category_id)
        )

        self.books.append(new_book)
        
        new_rel = BookAuthor(book_id=str(book_id), author_id=int(author_id))
        self.book_authors.append(new_rel)

        self.save_all_data()
        return True, f"Đã thêm sách: {title}"
    
    def admin_delete_book(self, book_id):
        """Admin xóa sách"""
        user = self.session_mgr.get_current_user()
        if not user or user.role != 'admin':
            return False, "Cần quyền Admin."
            
        book = next((b for b in self.books if b.book_id == book_id), None)
        if book:
            AdminService.deleteBook(self.books, book)
            return True, "Đã xóa sách."
        return False, "Không tìm thấy sách."