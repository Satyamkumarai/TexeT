from enum import IntEnum
class FileStatus(IntEnum):
    uploaded = 0
    processing = 1
    success = 2
    error = -1