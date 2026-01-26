# services/book_service.py
from models.book import Book
from models.author import Author
from utils.file_handler_fix import load_json, save_json
import uuid

class BookService:
    def __init__(self, book_path="data/books.json", author_path="data/authors.json", 
                 categories_file="data/categories.json"):
        self.book_path = book_path
        self.author_path = author_path
        self.categories_file = categories_file

    def search_books(self, keyword: str) -> list[Book]:
        """Tìm kiếm sách theo từ khóa"""
        try:
            books_data = load_json(self.book_path)
            authors_data = load_json(self.author_path)
            
            results = []
            for book_data in books_data:
                # Kiểm tra keyword trong title, description
                title = book_data.get("title", "").lower()
                description = book_data.get("description", "").lower()
                keyword_lower = keyword.lower()
                
                if (keyword_lower in title or 
                    keyword_lower in description or
                    keyword_lower in str(book_data.get("book_id", "")).lower()):
                    
                    # Tìm tác giả
                    author = None
                    author_id = book_data.get("author_id")
                    if author_id:
                        author_data = next((a for a in authors_data if a.get("author_id") == author_id), None)
                        if author_data:
                            author = Author(
                                author_id=author_data.get("author_id", 0),
                                author_name=author_data.get("author_name", "Unknown")
                            )
                    
                    book = Book(
                        book_id=book_data.get("book_id"),
                        title=book_data.get("title", ""),
                        description=book_data.get("description", ""),
                        publication_year=book_data.get("publication_year", 0),
                        quantity=book_data.get("quantity", 0),
                        available_quantity=book_data.get("available_quantity", 0),
                        status=book_data.get("status", "AVAILABLE"),
                        author=author,
                        category_id=book_data.get("category_id", 0)
                    )
                    results.append(book)
            
            return results
        except Exception as e:
            print(f"Error searching books: {e}")
            return []

    def get_book_by_id(self, book_id: str):
        """Lấy thông tin chi tiết sách"""
        try:
            books_data = load_json(self.book_path)
            authors_data = load_json(self.author_path)
            
            book_data = next((b for b in books_data if b.get("book_id") == book_id), None)
            if not book_data:
                return None
            
            # Tìm tác giả
            author = None
            author_id = book_data.get("author_id")
            if author_id:
                author_data = next((a for a in authors_data if a.get("author_id") == author_id), None)
                if author_data:
                    author = Author(
                        author_id=author_data.get("author_id", 0),
                        author_name=author_data.get("author_name", "Unknown")
                    )
            
            book = Book(
                book_id=book_data.get("book_id"),
                title=book_data.get("title", ""),
                description=book_data.get("description", ""),
                publication_year=book_data.get("publication_year", 0),
                quantity=book_data.get("quantity", 0),
                available_quantity=book_data.get("available_quantity", 0),
                status=book_data.get("status", "AVAILABLE"),
                author=author,
                category_id=book_data.get("category_id", 0)
            )
            
            return book
        except Exception as e:
            print(f"Error getting book: {e}")
            return None

    def get_all_books(self):
        """Lấy tất cả sách"""
        try:
            books_data = load_json(self.book_path)
            authors_data = load_json(self.author_path)
            
            books = []
            for book_data in books_data:
                # Tìm tác giả
                author = None
                author_id = book_data.get("author_id")
                if author_id:
                    author_data = next((a for a in authors_data if a.get("author_id") == author_id), None)
                    if author_data:
                        author = Author(
                            author_id=author_data.get("author_id", 0),
                            author_name=author_data.get("author_name", "Unknown")
                        )
                
                book = Book(
                    book_id=book_data.get("book_id"),
                    title=book_data.get("title", ""),
                    description=book_data.get("description", ""),
                    publication_year=book_data.get("publication_year", 0),
                    quantity=book_data.get("quantity", 0),
                    available_quantity=book_data.get("available_quantity", 0),
                    status=book_data.get("status", "AVAILABLE"),
                    author=author,
                    category_id=book_data.get("category_id", 0)
                )
                books.append(book)
            
            return books
        except Exception as e:
            print(f"Error getting all books: {e}")
            return []

    def view_books_by_category(self, category_id: str) -> list[Book]:
        """Xem sách theo thể loại"""
        try:
            books_data = load_json(self.book_path)
            authors_data = load_json(self.author_path)
            
            results = []
            for book_data in books_data:
                if str(book_data.get("category_id")) == str(category_id):
                    # Tìm tác giả
                    author = None
                    author_id = book_data.get("author_id")
                    if author_id:
                        author_data = next((a for a in authors_data if str(a.get("author_id")) == str(author_id)), None)
                        if author_data:
                            author = Author(
                                author_id=author_data.get("author_id", 0),
                                author_name=author_data.get("author_name", "Unknown")
                            )
                    
                    book = Book(
                        book_id=book_data.get("book_id"),
                        title=book_data.get("title", ""),
                        description=book_data.get("description", ""),
                        publication_year=book_data.get("publication_year", 0),
                        quantity=book_data.get("quantity", 0),
                        available_quantity=book_data.get("available_quantity", 0),
                        status=book_data.get("status", "AVAILABLE"),
                        author=author,
                        category_id=book_data.get("category_id", 0)
                    )
                    results.append(book)
            
            return results
        except Exception as e:
            print(f"Error getting books by category: {e}")
            return []

    def view_book_details(self, book_id: str):
        """Xem chi tiết sách"""
        book = self.get_book_by_id(book_id)
        if book:
            return book.getDetails()
        return None

    def get_categories(self):
        """Lấy danh sách thể loại"""
        try:
            categories = load_json(self.categories_file)
            return categories
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []