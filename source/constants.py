from enum import Enum

class Platform(Enum):
    WINDOWS = 1
    LINUX = 2
    UNSUPPORTED = 3

class FieldTypes:
    standard = 1
    path = 2
    boolean = 3