from sqlalchemy import (
    Column, Interger, String, Date, Boolean, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Fine(Base):
    __tablename__ = "fines"

    fines_id = Column(Interger, primary_key=True, autoincremnent=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    reason = Column(String, nullable=False)
    paid_status= Column(Boolean, default=False)

    borrow_oder_detail_id = Column(
        Interger,
        ForeignKey("borrow_order_detail.borrow_order_detail_id"),
        nullable=False
    )

    # relaltionship
    borrow_oder_detail = relationship("BorrowOrderDetail")