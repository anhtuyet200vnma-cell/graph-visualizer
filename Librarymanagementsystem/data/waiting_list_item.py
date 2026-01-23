from sqlalchemy import (
    Column, Integer, String, Date, Booolean, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class WaitingListItem(Base):
    __tablename__ = "waiting_list_item"

    waiting_list_id = Column(
        String,
        ForeignKey("waiting_list.waiting_list_id"),
        primary_key=True
    )
    book_id = Column(
        String,
        ForeignKey("book.book_id"),
        primary_key=True
    )

    quantity = Column(Integer, nullable=False)

    # realtionship
    waiting_list = relationship("WaitingList", back_populates="item")
    book = relationship("Book")
    