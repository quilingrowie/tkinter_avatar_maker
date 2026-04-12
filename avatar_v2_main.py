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
from avatar_v2_model import Model, Database
from avatar_v2_media import Resources
from avatar_v2_view import Window

if __name__ == "__main__":
    database = Database()
    resources = Resources()
    model = Model(database)
    view = Window(resources)

    Controller(view, model)
