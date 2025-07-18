from enum import Enum


class CardStatus(int, Enum):
    ACTIVE = 1
    BLOCKED = 2
    EXPIRED = 3
