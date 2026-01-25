import uuid
from datetime import datetime

def generate_id():
    return uuid.uuid4().hex[:8] 

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

FINE_PER_DAY = 5000   

class Fine:
    """Fine class - Phạt"""
    
    def __init__(self, fine_id=None, borrow_order_detail_id=None,
                 amount=0.0, reason=None, paid_status=False,
                 created_date=None):
        self.fine_id = fine_id or generate_id()
        self.borrow_order_detail_id = borrow_order_detail_id
        self.amount = amount
        self.reason = reason
        self.paid_status = paid_status
        self.created_date = created_date or get_current_datetime()
    

    def calculate_fines(self, base_amount):
        self.amount = base_amount
        return self.amount
    
    @classmethod
    def create_fine(cls, detail_obj, overdue_days):
        base_amount, reason_str = detail_obj.calculate_fines(overdue_days)
        if base_amount <= 0:
            return None, None
        new_fine = cls(
            borrow_order_detail_id=detail_obj.borrow_order_detail_id,
            reason=reason_str,
            amount=0.0 
        )
        new_fine.calculate_fines(base_amount)
        return new_fine, None
    
    def pay_fine(self):
        if self.paid_status:
            return False, "Phạt đã được thanh toán"
        
        self.paid_status = True
        return True, None
    
    def get_amount_formatted(self):
        return f"{self.amount:,.0f} VND"
    
    def to_dict(self):
        return {
            'fine_id': self.fine_id,
            'borrow_order_detail_id': self.borrow_order_detail_id,
            'amount': self.amount,
            'reason': self.reason,
            'paid_status': self.paid_status,
            'created_date': self.created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def __str__(self):
        status = "Đã thanh toán" if self.paid_status else "Chưa thanh toán"
        return f"Fine({self.get_amount_formatted()} - {status})"
    
    def __repr__(self):
        return f"Fine(id={self.fine_id}, amount={self.amount}, paid={self.paid_status})"