from utils.file_handler import load_json, save_json
from datetime import datetime
import uuid


class NotificationService:
    def __init__(self, path="data/notifications.json"):
        self.path = path

    def send_notification(self, user_id: int, content: str) -> bool:
        notifications = load_json(self.path)

        notifications.append({
            "notification_id": str(uuid.uuid4()),
            "user_id": user_id,
            "content": content,
            "created_date": datetime.now().isoformat(),
            "status": "SENT"
        })

        save_json(self.path, notifications)
        return True
