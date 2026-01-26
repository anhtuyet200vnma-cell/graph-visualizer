"""
config.py
Cấu hình hệ thống thư viện
"""

# Giới hạn mượn sách
MAX_BORROW_DAYS = 14  # 14 ngày
MAX_BORROW_LIMIT = 5  # Tối đa 5 sách
FINE_PER_DAY = 5000   # 5000 VND/ngày quá hạn

# Đường dẫn file data
DATA_DIR = "data"
BOOKS_FILE = f"{DATA_DIR}/books.json"
AUTHORS_FILE = f"{DATA_DIR}/authors.json"
USERS_FILE = f"{DATA_DIR}/users.json"
BORROW_ORDERS_FILE = f"{DATA_DIR}/borrow_orders.json"
BORROW_REQUESTS_FILE = f"{DATA_DIR}/borrow_requests.json"
CATEGORIES_FILE = f"{DATA_DIR}/categories.json"
FINES_FILE = f"{DATA_DIR}/fines.json"
NOTIFICATIONS_FILE = f"{DATA_DIR}/notifications.json"
WAITING_LISTS_FILE = f"{DATA_DIR}/waiting_lists.json"

# Trạng thái sách
BOOK_STATUS = {
    "AVAILABLE": "AVAILABLE",
    "UNAVAILABLE": "UNAVAILABLE",
    "RESERVED": "RESERVED",
    "LOST": "LOST",
    "DAMAGED": "DAMAGED"
}

# Trạng thái mượn
BORROW_STATUS = {
    "PENDING": "PENDING",
    "BORROWED": "BORROWED",
    "RETURNED": "RETURNED",
    "OVERDUE": "OVERDUE",
    "LOST": "LOST"
}

# Trạng thái user
USER_STATUS = {
    "ACTIVE": "ACTIVE",
    "INACTIVE": "INACTIVE",
    "SUSPENDED": "SUSPENDED"
}

# Role
ROLES = {
    "ADMIN": "ADMIN",
    "MEMBER": "MEMBER"
}

# Mã lỗi
ERROR_CODES = {
    "SUCCESS": 0,
    "VALIDATION_ERROR": 1,
    "NOT_FOUND": 2,
    "PERMISSION_DENIED": 3,
    "SYSTEM_ERROR": 4
}