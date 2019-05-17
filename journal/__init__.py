"A logging utility"

from enum import Enum

class Level(Enum):
    """Level at which a Journal should log"""
    STUDY   = 0
    TEST    = 0
    DEBUG   = 1
    DEVELOP = 2
    INFO    = 3
    PROD    = 4

from .message import *
