from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM


class MovementType(str, Enum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"



class MovementTypeCost(str, Enum):
    RAW_MATERIAL = "raw_material"
    LABOR = "labor"
    PACKAGING = "packaging"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    OTHER = "other"


movement_type_enum = ENUM(
    MovementType,
    name="movement_type",
    create_type=False,
)



movement_type_cost_enum = ENUM(
    MovementTypeCost,
    name="movement_type_cost",
    create_type=False,
)