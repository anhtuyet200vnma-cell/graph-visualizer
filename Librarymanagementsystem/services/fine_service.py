class FineService:
    """
    FINE-RELATED CHECKS (1.4 & 1.5 trong đặc tả)
    """

    @staticmethod
    def checkPenaltyStatus(member) -> bool:
        """Check if member is under penalty (1.4)"""
        return member.penalty_status if hasattr(member, 'penalty_status') else False

    @staticmethod
    def calculateOverdueFine(days_overdue: int) -> float:
        """Calculate overdue fine (1.5)"""
        return days_overdue * 5000  # 5000 VND per day

    @staticmethod
    def calculateDamageFine(book_value: float) -> float:
        """Calculate damage fine (1.5)"""
        return book_value * 0.5  # 50% of book value