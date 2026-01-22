from models.book import Book

class BookService:

    @staticmethod
    def searchBooks(books: list[Book], keyword: str) -> list[Book]:
        return [book for book in books if keyword.lower() in book.title.lower()]

    @staticmethod
    def viewBooksByCategory(books: list[Book], category_name: str) -> list[Book]:
        return [book for book in books if book.category == category_name]

    @staticmethod
    def viewBookDetails(book: Book):
        return book.getDetails()
