class Author:
    def __init__(self, author_id: int, author_name: str):
        self.author_id = author_id
        self.author_name = author_name

    def getAuthorName(self) -> str:
        return self.author_name