from datetime import date
import uuid
ORDER_STATUS = {
    'BORROWED': 'BORROWED',
    'RETURNED': 'RETURNED',
    'LOST': 'LOST',
    'DAMAGED': 'DAMAGED'
}
FINE_PER_DAY = 5000   

def generate_id():
    return uuid.uuid4().hex[:8] 

class BorrowOrderDetail:
    """Chi tiết từng cuốn sách trong đơn mượn"""
    
    def __init__(self, book_id, item_status=ORDER_STATUS['BORROWED'],
                 condition=None, actual_return_date=None, borrow_order_detail_id=None):
        self.borrow_order_detail_id = borrow_order_detail_id or generate_id()
        self.book_id = book_id
        self.item_status = item_status
        self.condition = condition
        self.actual_return_date = actual_return_date
    
    def mark_as_returned(self, return_date, condition):
        self.item_status = ORDER_STATUS['RETURNED']
        self.actual_return_date = return_date
        self.condition = condition
        if condition == 'LOST':
            self.item_status = 'LOST'
        elif condition == 'DAMAGED':
            self.item_status = 'DAMAGED'
        else:
            self.item_status = 'RETURNED'
        return True, None
    
    def calculate_overdue_days(self, due_date: date) -> int:
        """Tính số ngày trễ dựa trên hạn trả (due_date)"""
        compare_date = self.actual_return_date if self.actual_return_date else date.today()
        
        if compare_date <= due_date:
            return 0
        
        delta = compare_date - due_date
        return delta.days
    
    def calculate_fines(self, overdue_days):
        """
        Tính toán tiền phạt và lý do dựa trên tình trạng sách.
        Trả về: (amount, reason_string)
        """
        amount = 0.0
        reasons = []
        if overdue_days > 0:
            overdue_fine = overdue_days * FINE_PER_DAY
            amount += overdue_fine
            reasons.append(f"Trả trễ {overdue_days} ngày: {overdue_fine:,.0f} VND")
        if self.condition == 'DAMAGED':
            damage_fine = 50000
            amount += damage_fine
            reasons.append(f"Sách bị hư hỏng: {damage_fine:,.0f} VND")
        elif self.condition == 'TORN':
            torn_fine = 100000 
            amount += torn_fine
            reasons.append(f"Sách bị rách: {torn_fine:,.0f} VND")
        elif self.condition == 'LOST':
            lost_fine = 500000
            amount += lost_fine
            reasons.append(f"Mất sách: {lost_fine:,.0f} VND")
        reason_str = "; ".join(reasons) if reasons else ""
        return amount, reason_str

    def to_dict(self):
        return {
            'borrow_order_detail_id': self.borrow_order_detail_id,
            'book_id': self.book_id,
            'item_status': self.item_status,
            'condition': self.condition,
            'actual_return_date': self.actual_return_date
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def __str__(self):
        return f"OrderDetail(book={self.book_id}, status={self.item_status})"
    
    def __repr__(self):
        return f"BorrowOrderDetail(book_id='{self.book_id}', status='{self.item_status}')"