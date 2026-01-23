class NotificationService:
    """
    NOTIFICATION MANAGEMENT (1.4 & 1.5 trong đặc tả)
    """

    @staticmethod
    def sendBorrowingConfirmation(member_name: str, book_title: str) -> str:
        """Send confirmation email (1.4)"""
        message = f"Borrowing confirmed: {book_title}"
        print(f"Notification sent to {member_name}: {message}")
        return message

    @staticmethod
    def sendDueDateReminder(member_name: str, book_title: str, days_left: int) -> str:
        """Send due date reminder (1.5)"""
        if days_left <= 5:
            message = f"Reminder: {book_title} due in {days_left} days"
            print(f"Reminder sent to {member_name}: {message}")
            return message
        return ""

    @staticmethod
    def sendReturnConfirmation(member_name: str, book_title: str) -> str:
        """Send return confirmation"""
        message = f"Return confirmed: {book_title}"
        print(f"Notification sent to {member_name}: {message}")
        return message