''' Module name: avatar_v2_constants.py
    Module descrption: Compiles the enum constants used throughout the applciation. '''
from enum import Enum, auto

class Page(Enum):
    ''' Serves as constant for page strings'''
    HOME = auto()
    CREATE = auto()
    SAVES = auto()
    EXIT = auto()

class State(Enum):
    ''' State constants. '''
    EMPTY = auto()
    NOT_EMPTY = auto()

class Status(Enum):
    ''' Result status constants. '''
    DISTINCT_CONFIG = auto()
    DISTINCT_NAME = auto()
    SAVE_SUCCESS = auto()
    DELETE_SUCCESS = auto()
    UPDATE_SUCCESS = auto()
    RANDOMIZE_SUCCESS = auto()
    CLEAR_SUCCESS = auto()
    IDLE = auto()

    CONFIG_DUPLICATE = auto()
    NAME_DUPLICATE = auto()
    EMPTY_ERROR = auto()
    JSON_WRITE_ERROR = auto()
    JSON_READ_ERROR = auto()

class ObserverType(Enum):
    ''' Constants for obervation type in the Model. '''
    PREVIEW = auto()
    STATUS = auto()
    DATABASE = auto()
