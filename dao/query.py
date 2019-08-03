from enum import Enum


class ComparisonOperator(Enum):
    EQ = "="
    LT = "<"
    GT = ">"


class SortOrder(Enum):
    ASC = 'asc'
    DESC = 'desc'


class Operation(Enum):
    SET = "set"
    SET_DATE = "set_date"
    INC = "inc"
    MIN = "min"
    MAX = "max"
    MUL = "mul"
    RENAME = "rename"
    SET_ON_INSERT = "set_on_insert"
    UNSET = "unset"
