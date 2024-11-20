# utils/file_types.py
from enum import Enum

class FileClasses(Enum):
    ECL_ECF = 1
    DMP_LOG = 2
    UNKNOWN = 3