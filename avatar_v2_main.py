''' Project Description: Refactored, 2nd version of "Tkinter Avatar Maker" project. This program
    allows user to create a customizeable avatar; created in Python, using Tkinter for its GUI and
    JSON data storage to save instances of each saved avatar.
    
    Module Name: "avatar_v2_main.py"
    Module Description: This module serves as the entry point of the program.
    
    Project start date: April 09, 2026
    Project finish date: stc
    Author: Rowie Quiling
'''
from avatar_v2_controller import Controller
if __name__ == "__main__":
    try:
        Controller()
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
