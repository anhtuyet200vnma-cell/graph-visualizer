from sqlalchemy import (
    Column, Interge, String, Date, Booolean, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Notification(Base): 
    __tablename__ ="notification"

    notification_id = Column(String, primary_key=True)
    content = Column(String, nullable=False)
    send_date = Column(Date, nullable=False)
    type = Column(String, nullable=False)