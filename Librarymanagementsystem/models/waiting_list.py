import uuid
from datetime import datetime
from waiting_list_item import WaitingListItem

def generate_id():
    return uuid.uuid4().hex[:8]

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class WaitingList:
    """Waiting List - giỏ sách của member"""
    
    def __init__(self, waiting_list_id=None, user_id=None, 
                 created_date=None, items=None):
        self.waiting_list_id = waiting_list_id or generate_id()
        self.user_id = user_id
        self.created_date = created_date or get_current_datetime()
        self.items = items or []  
    
    def add_book(self, book_id, quantity=1):
        """
        Thêm sách vào danh sách chờ
        Trả về: (thành công, thông báo lỗi)
        """
        if quantity <= 0:
            return False, "Số lượng phải lớn hơn 0"
        
        # Kiểm tra xem sách đã có trong danh sách chưa.
        for item in self.items:
            if item.book_id == book_id:
                item.quantity += quantity
                return True, None
        
        # Thêm mục mới
        new_item = WaitingListItem(waiting_list_id=self.waiting_list_id, book_id=book_id, quantity=quantity)
        self.items.append(new_item)
        return True, None
    
    def remove_book(self, book_id):
        """
        Xóa sách khỏi danh sách chờ
        Trả về: (thành công, thông báo lỗi)
        """
        for i, item in enumerate(self.items):
            if item.book_id == book_id:
                self.items.pop(i)
                return True, None
        
        return False, "Sách không có trong danh sách chờ"
    
    def update_quantity(self, book_id, new_quantity):
        """
        Cập nhật số lượng sách trong danh sách chờ
        Trả về: (thành công, thông báo lỗi)
        """
        if new_quantity <= 0:
            return False, "Số lượng phải lớn hơn 0"
        
        for item in self.items:
            if item.book_id == book_id:
                item.quantity = new_quantity
                return True, None
        
        return False, "Sách không có trong danh sách chờ"
    
    def clear_list(self):
        """Xóa tất cả các mục"""
        self.items = []
        return True, None
    
    def get_items(self):
        """Lấy tất cả các mục"""
        return self.items
    
    def get_book_ids(self):
        """Lấy danh sách ID sách trong danh sách chờ"""
        return [item.book_id for item in self.items]
    
    def get_total_books(self):
        """Tính tổng số lượng sách trong danh sách chờ"""
        return sum(item.quantity for item in self.items)
    
    def is_empty(self):
        """Kiểm tra xem danh sách chờ có trống không"""
        return len(self.items) == 0
    
    def create_borrow_request(self):
        if self.is_empty():
            return None, "Danh sách chờ trống"
        # Lấy danh sách ID sách ra để chuẩn bị tạo đơn
        requested_books = [item.book_id for item in self.items]
        self.clear_list()
        return requested_books, None
    
    def to_dict(self):
        """Chuyển thành từ điển"""
        return {
            'waiting_list_id': self.waiting_list_id,
            'user_id': self.user_id,
            'created_date': self.created_date,
            'items': [item.to_dict() for item in self.items]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create WaitingList from dictionary"""
        items_data = data.pop('items', [])
        waiting_list = cls(**data)
        waiting_list.items = [WaitingListItem.from_dict(item) for item in items_data]
        return waiting_list
    
    def __str__(self):
        return f"WaitingList(member={self.member_id}, items={len(self.items)})"
    
    def __repr__(self):
        return f"WaitingList(id={self.waiting_list_id}, member_id='{self.member_id}', items={len(self.items)})"