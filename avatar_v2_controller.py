''' Module Name: "avatar_v2_controller.py"
    Module Description: This module acts as the central coordinator between the GUI and the
    program's model.
'''
from avatar_v2_model import Model, Database
class Controller:
    ''' This class handles the coordination between the view/GUI and model. '''
    def __init__(self):
        self.view = ""
        self.model = Model(Database)
