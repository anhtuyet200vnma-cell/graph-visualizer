from models.author import Author

class Book:
    def __init__(self, book_id, title, description, publication_year, quantity, available_quantity, status, author, category_id):
        self.book_id = book_id
        self.title = title
        self.description = description
        self.publication_year = publication_year
        self.quantity = quantity
        self.available_quantity = available_quantity
        self.status = status
        self.author = author
        self.category_id = category_id
    
    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "description": self.description,
            "publication_year": self.publication_year,
            "quantity": self.quantity,
            "available_quantity": self.available_quantity,
            "status": self.status,
            "category_id": self.category_id
        }

    @staticmethod
    def from_dict(data: dict):
        # Tạo một đối tượng Author tạm nếu cần
        author_data = data.get("author")
        if isinstance(author_data, dict):
            author = Author(author_id=author_data.get("author_id", 0), 
                          author_name=author_data.get("author_name", ""))
        elif isinstance(author_data, Author):
            author = author_data
        else:
            author = Author(author_id=0, author_name="Unknown")
            
        return Book(
            book_id=data.get("book_id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            publication_year=int(data.get("publication_year", 0)),
            quantity=int(data.get("quantity", 0)),
            available_quantity=int(data.get("available_quantity", 0)),
            status=data.get("status", "AVAILABLE"),
            author=author,
            category_id=int(data.get("category_id", 0))
        )
    
    def decreaseAvailable(self):
        if self.available_quantity > 0:
            self.available_quantity -= 1
            if self.available_quantity <= 0:
                self.status = "UNAVAILABLE"

    def increaseAvailable(self):
        self.available_quantity += 1
        if self.available_quantity > 0 and self.status == "UNAVAILABLE":
            self.status = "AVAILABLE"

    def getDetails(self):
        author_name = self.author.getAuthorName() if hasattr(self.author, 'getAuthorName') else "Unknown"
        return {
            "bookId": self.book_id,
            "title": self.title,
            "availableQuantity": self.available_quantity,
            "status": self.status,
            "author": author_name
        }