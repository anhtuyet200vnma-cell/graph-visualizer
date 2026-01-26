class BookAuthor:
    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "author_id": self.author_id
        }

    def from_dict(data: dict):
        return BookAuthor(
            book_id=data.get("book_id"),
            author_id=int(data.get("author_id", 0))
        )