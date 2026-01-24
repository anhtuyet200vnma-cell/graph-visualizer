from utils.file_handler import load_json, save_json
from config import FINE_PER_DAY
from datetime import datetime
import uuid


class FineService:
    def __init__(self, path="data/fines.json"):
        self.path = path

    def calculate_fine(self, overdue_days: int) -> int:
        if overdue_days <= 0:
            return 0
        return overdue_days * FINE_PER_DAY

    def add_fine(self, user_id: int, amount: int) -> bool:
        fines = load_json(self.path)

        fines.append({
            "fine_id": str(uuid.uuid4()),
            "user_id": user_id,
            "amount": amount,
            "status": "UNPAID",
            "created_date": datetime.now().isoformat()
        })

        save_json(self.path, fines)
        return True
