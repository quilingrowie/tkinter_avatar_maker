''' Module Name: "avatar_v2_exceptions.py"
    Module Description: This module houses custom exception classes, and function decorators that
    catches errors and are raised throughout the application.
'''
from json.decoder import JSONDecodeError
def catch_file_handling_exceptions(function):
    ''' A decorator function that catches errors on file handling methods/functions. '''
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except OSError as error:
            raise DatabaseError(
                f"DatabaseError occured in {function.__name__}:\n{error}"
            ) from error
        except TypeError as error:
            raise DatabaseError(
                f"DatabaseError occured in {function.__name__}:\n{error}"
            ) from error
        except JSONDecodeError as error:
            raise DatabaseCorruptedError(
                f"DatabaseCorruptedError occured in {function.__name__}:\n{error}"
            ) from error
    return wrapper

class CustomExceptions(Exception):
    ''' Parent class / Template of custom exceptions. '''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f"Unable to run the program:\n{self.message}"

class ResourcesDirectoryNotFound(CustomExceptions):
    ''' Custom exception that is raised when attempting to access directory "resources" but it is
        not found. '''
    def __init__(self):
        message_1 = "Directory 'resources' not found."
        message_2 = "Missing required files and/or directory for the application to run."
        super().__init__(message_1 + "\n" + message_2)

class DatabaseError(CustomExceptions):
    ''' Custom exception raised when there is an error in Database (JSON).'''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DatabaseCorruptedError(DatabaseError):
    ''' A database error raised when the database file is corrupted. '''
    def __init__(self, message="Corrupted JSON file."):
        super().__init__(message)
