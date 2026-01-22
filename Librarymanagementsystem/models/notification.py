from __future__ import annotations 
from dataclasses import dataclass 
from datetime import date 
from enum import Enum 

class NotificationType(str, Enum): 
    SYSTEM = "system"
    DUE_DATE = "due_date"
    WAITING_LIST = "waiting_list"
    BORROW_REQUEST = "borrow_request"


@dataclass
class Notification: 
    notification_id: str 
    content:str 
    send_date: date 
    type: NotificationType
    user_id: int 

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.notification_id, str) or not self.notification_id.strip():
            raise ValueError("notification_id không được rỗng.")

        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content không được rỗng.")

        if not isinstance(self.send_date, date):
            raise TypeError("send_date phải là kiểu datetime.date.")

        if not isinstance(self.type, NotificationType):
            raise TypeError("type phải thuộc enum NotificationType.")

        if not isinstance(self.user_id, int) or self.user_id <= 0:
            raise ValueError("user_id phải là số nguyên dương (>0).")

    # ===== UML Method =====
    def sendNotification(self) -> str:
        self.is_sent = True
        return f"[SENT] ({self.type.value}) To user_id={self.user_id}: {self.content}"
    def mark_unsent(self) -> None:
        self.is_sent = False

    def update_content(self, new_content: str) -> None:
        if not isinstance(new_content, str) or not new_content.strip():
            raise ValueError("new_content không được rỗng.")
        self.content = new_content.strip()

    def change_type(self, new_type: NotificationType) -> None:
        if not isinstance(new_type, NotificationType):
            raise TypeError("new_type phải thuộc NotificationType.")
        self.type = new_type

    def reschedule(self, new_date: date) -> None:
        if not isinstance(new_date, date):
            raise TypeError("new_date phải là datetime.date.")
        self.send_date = new_date

    def to_dict(self) -> dict:
        return {
            "notification_id": self.notification_id,
            "content": self.content,
            "send_date": self.send_date.isoformat(),
            "type": self.type.value,
            "user_id": self.user_id,
            "is_sent": self.is_sent
        }