from __future__ import annotations
from dataclasses import dataclass


@dataclass
class WaitingListItem:
    waiting_list_id: str
    book_id: str
    quantity: int

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self.waiting_list_id, str) or not self.waiting_list_id.strip():
            raise ValueError("waiting_list_id không được rỗng.")

        if not isinstance(self.book_id, str) or not self.book_id.strip():
            raise ValueError("book_id không được rỗng.")

        if not isinstance(self.quantity, int):
            raise TypeError("quantity phải là int.")

        if self.quantity <= 0:
            raise ValueError("quantity phải > 0.")
    def increase_quantity(self, amount: int = 1) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount phải là số nguyên dương.")
        self.quantity += amount

    def decrease_quantity(self, amount: int = 1) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount phải là số nguyên dương.")
        if self.quantity - amount <= 0:
            raise ValueError("Không thể giảm vì quantity phải luôn > 0.")
        self.quantity -= amount

    def set_quantity(self, new_quantity: int) -> None:
        if not isinstance(new_quantity, int):
            raise TypeError("new_quantity phải là int.")
        if new_quantity <= 0:
            raise ValueError("new_quantity phải > 0.")
        self.quantity = new_quantity

    def same_item(self, other: "WaitingListItem") -> bool:
        return (
            self.waiting_list_id == other.waiting_list_id
            and self.book_id == other.book_id
        )

    def to_dict(self) -> dict:
        return {
            "waiting_list_id": self.waiting_list_id,
            "book_id": self.book_id,
            "quantity": self.quantity
        }
