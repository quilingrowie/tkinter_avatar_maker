''' Project Description: Refactored, 2nd version of "Tkinter Avatar Maker" project. This program
    allows user to create a customizeable avatar; created in Python, using Tkinter for its GUI and
    JSON data storage to save instances of each saved avatar.

    Module Name: "avatar_v2_controller.py"
    
    Module Description: This module acts as the central coordinator between the GUI and the
    program's model. It manages screen transitions, user actions, and manages loading and saving
    of avatar configurations from JSON storage.
    
    Project start date: April 09, 2026
    Project finish date: stc
    Author: Rowie Quiling
'''
from avatar_v2_model import Model
class Controller:
    ''' This class handles the coordination between the view/GUI and model. '''
    def __init__(self):
        self.view = ""
        self.model = Model()

try:
    Controller()
except SyntaxError as e:
    print("SyntaxError has occured: Incorrect code syntax was encountered.")
    print(f"Error: {e}")
except IndexError as e:
    print("IndexError has occured: Attempting to access a sequence with an")
    print("index that is out of its range.")
    print(f"Error: {e}")
except KeyError as e:
    print("KeyError has occured: A dictionary was accessed using a key that does not exist.")
    print(f"Error: {e}")
except AttributeError as e:
    print("AttributeError has occured: An attribute or method has been accessed that")
    print("does not exist for the particular object.")
    print(f"Error: {e}")
except NameError as e:
    print("NameError has occured: A local or global name (variable or function) is attempted")
    print("to be accessed but not found.")
    print(f"Error: {e}")
