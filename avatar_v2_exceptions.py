''' Module Name: "avatar_v2_exceptions.py"
    Module Description: This module houses custom exception classes, and function decorators that
    catches errors and are raised throughout the application.
'''
def catch_file_handling_exceptions(function):
    ''' A decorator function that catches errors on file handling methods/functions. '''
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except FileNotFoundError as error:
            print(f"FileNotFoundError occured in function {function.__name__}:")
            print("Attempting to access a file or directory that does not exist.")
            print(f"Error: {error}")
        except PermissionError as error:
            print(f"PermissionError occured in {function.__name__}:")
            print("Attempting to perform operations that does not meet user permissions.")
            print(f"Error: {error}")
        except NotADirectoryError as error:
            print(f"NotADirectoryError occured in {function.__name__}:")
            print("Attempting to do directory-only operations on a file.")
            print(f"Error: {error}")
        except IsADirectoryError as error:
            print(f"IsADirectoryError occured in {function.__name__}:")
            print("Attempting to do a file-only operations on a directory.")
            print(f"Error: {error}")
    return wrapper

class CustomExceptions(Exception):
    ''' Parent class / Template of custom exceptions. '''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Unable to run the program:\n{self.message}"

class ConfigurationExists(CustomExceptions):
    ''' Custom exception that is raised when attempting to save selected configurations that are
        already saved in the database. '''
    def __init__(self):
        super().__init__("This configuration you're trying to save already exists in the database.")

class ConfigurationEmpty(CustomExceptions):
    ''' Custom exception that is raised when attempting to save empty selected configurations. '''
    def __init__(self):
        super().__init__("Attempting to save empty configuration.")

class ResourcesDirectoryNotFound(CustomExceptions):
    ''' Custom exception that is raised when attempting to access directory "resources" but it is
        not found. '''
    def __init__(self):
        message_1 = "Directory 'resources' not found."
        message_2 = "Missing required files and/or directory for the application to run."
        super().__init__(message_1 + "\n" + message_2)
