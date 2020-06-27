from enum import Enum

class PLATFORMS(Enum):
    WINDOWS = 1
    LINUX = 2
    MACOSX = 3

class FieldTypes:
    standard = 1
    path = 2
    boolean = 3