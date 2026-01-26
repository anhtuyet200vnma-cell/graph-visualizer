class Author:
    def __init__(self, author_id: int, author_name: str):
        self.author_id = author_id
        self.author_name = author_name

    def getAuthorName(self) -> str:
        return self.author_name
    
    def setAuthorName(self, name: str) -> None:
        self.author_name = name
    
    def to_dict(self):
        return {
            "author_id": self.author_id,
            "author_name": self.author_name
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            author_id=data.get("author_id", 0),
            author_name=data.get("author_name", "")
        )
    
    def __str__(self):
        return f"Author(id={self.author_id}, name={self.author_name})"