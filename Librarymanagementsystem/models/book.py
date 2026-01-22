from models.user import Author

class Book:
    def __init__(
        self,
        book_id: str,
        title: str,
        description: str,
        publication_year: int,
        quantity: int,
        available_quantity: int,
        status: str,
        author: Author
    ):
        self.book_id = book_id
        self.title = title
        self.description = description
        self.publication_year = publication_year
        self.quantity = quantity
        self.available_quantity = available_quantity
        self.status = status
        self.author = author

    def isAvailable(self) -> bool:
        return self.available_quantity > 0 and self.status == "AVAILABLE"

    def borrow(self) -> bool:
        if self.isAvailable():
            self.available_quantity -= 1
            if self.available_quantity == 0:
                self.status = "UNAVAILABLE"
            return True
        return False

    def returnBook(self):
        self.available_quantity += 1
        if self.available_quantity > 0:
            self.status = "AVAILABLE"

    def getDetails(self) -> dict:
        return {
            "bookId": self.book_id,
            "title": self.title,
            "availableQuantity": self.available_quantity,
            "status": self.status,
            "author": self.author.getAuthorName()
        }
