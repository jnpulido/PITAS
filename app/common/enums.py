from enum import Enum

class MovementType(str, Enum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"


class BatchStatus(str,Enum):
    PRODUCCTION = "production"
    COMPLETED = "completed"
    CANCELLED = "cancelled"