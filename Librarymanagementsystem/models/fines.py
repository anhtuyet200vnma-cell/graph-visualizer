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
    
    @classmethod
    def calculate_fine(cls, overdue_days, book_condition=None):
        """
        Tính toán số tiền phạt dựa trên số ngày quá hạn và tình trạng sách
        Trả về: (Đối tượng Tiền phạt, thông báo lỗi)
        """
        amount = 0.0
        reasons = []
        
        # Fine for overdue
        if overdue_days > 0:
            overdue_fine = overdue_days * FINE_PER_DAY
            amount += overdue_fine
            reasons.append(f"Trả trễ {overdue_days} ngày: {overdue_fine:,.0f} VND")
        
        # Fine for damaged/lost book
        if book_condition == 'DAMAGED':
            damage_fine = 50000  # 50k for damaged
            amount += damage_fine
            reasons.append(f"Sách bị hư hỏng: {damage_fine:,.0f} VND")
        elif book_condition == 'TORN':
            torn_fine = 100000  # 100k for torn pages
            amount += torn_fine
            reasons.append(f"Sách bị rách: {torn_fine:,.0f} VND")
        elif book_condition == 'LOST':
            lost_fine = 500000  # 500k for lost book
            amount += lost_fine
            reasons.append(f"Mất sách: {lost_fine:,.0f} VND")
        
        if amount == 0:
            return None, None
        
        reason = "; ".join(reasons)
        fine = cls(amount=amount, reason=reason)
        
        return fine, None
    
    def pay_fine(self):
        """
        Mark fine as paid
        Returns: (success, error_message)
        """
        if self.paid_status:
            return False, "Phạt đã được thanh toán"
        
        self.paid_status = True
        return True, None
    
    def get_amount_formatted(self):
        """Get formatted amount string"""
        return f"{self.amount:,.0f} VND"
    
    def to_dict(self):
        """Convert to dictionary"""
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
        """Create Fine from dictionary"""
        return cls(**data)
    
    def __str__(self):
        status = "Đã thanh toán" if self.paid_status else "Chưa thanh toán"
        return f"Fine({self.get_amount_formatted()} - {status})"
    
    def __repr__(self):
        return f"Fine(id={self.fine_id}, amount={self.amount}, paid={self.paid_status})"