''' Module Name: "avatar_v2_exceptions.py"
    Module Description: This module houses custom exception classes, and function decorators that
    catches errors and are raised throughout the application.
'''
def catch_file_handling_exceptions(function):
    ''' A decorator function that catches errors on file handling methods/functions. '''
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"FileNotFoundError occured in function {function.__name__}:\n{error}"
                ) from error
        except PermissionError as error:
            raise PermissionError(
                f"PermissionError occured in {function.__name__}:\n{error}"
            ) from error
        except NotADirectoryError as error:
            raise NotADirectoryError(
                f"NotADirectoryError occured in {function.__name__}:\n{error}"
            ) from error
        except IsADirectoryError as error:
            raise IsADirectoryError(
                f"IsADirectoryError occured in {function.__name__}:\n{error}"
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
