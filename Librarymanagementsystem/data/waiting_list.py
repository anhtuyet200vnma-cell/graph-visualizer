from sqlalchemy import (
    Column, Interger, String, Date, Booolean, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
class Waiting(Base): 
    __tablename__ = "waiting_list" 

    waiting_list_id = Column(String, primary_key=True)
    created_date = Column(Date, nullable=False)

    user_id = Column(Interger, ForeignKey("user.user_id"), nullable=False)

    # relationship
    user = relationship("User", back_populates="waiting_list")
    items = relationship("WaitingListItem", back_populates="waiting_list")
    