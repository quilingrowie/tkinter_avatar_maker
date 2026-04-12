''' Module Name: "avatar_v2_view.py"
    Module Description: This module handles GUI of the application. It creates the Tkinter root
    window, creation, destroying of widgets, and displays the PhotoImages saved in the program.
'''
import tkinter as tk
def get_screen_size():
    ''' Takes the screensize of the device where the program is executed and determines the
        window size of the application, then returns its values. '''
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width - (screen_width * 0.2))
    window_height = int(screen_height - (screen_height * 0.2))
    root.destroy()

    return screen_width, screen_height, window_width, window_height

SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT= get_screen_size()
MINIMUM_SCALE = 1.5

class Window:
    ''' Creation class of the root window and main frames displayed in the window. '''
    def __init__(self, resources):
        self.root = self.root_window()
        self.resources = resources
        self.selected_assets = self.select_asset()
        self.root.mainloop()

    def root_window(self):
        ''' Creates Tk window and places the window at the center of the screen upon running.
            Returns the root window.'''
        root = tk.Tk()
        root.title("Anime Avatar Portrait Maker v2")
        x_axis = (SCREEN_WIDTH - WINDOW_WIDTH) // 2
        y_axis = (SCREEN_HEIGHT - WINDOW_HEIGHT) // 2
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_axis}+{y_axis}")
        root.minsize(width=int(WINDOW_WIDTH // MINIMUM_SCALE),
                     height=int(WINDOW_HEIGHT // MINIMUM_SCALE))

        return root

    def select_asset(self, selected_input: dict = None):
        ''' Takes dictionary input of selected asset items and returns them. '''
        # edit method later
        return selected_input

    def load_selected_assets(self) -> dict:
        ''' Reads self.selected_assets and accesses its corresponding PIL object. Stores selected
            assets with its PIL objects in a dictionary and returns it. '''
        selected_dict = self.selected_assets.copy()
        loaded_group = {}
        for key, value in selected_dict.items():
            if value == "":
                loaded_group[key] = ""
            else:
                loaded_obj = self.resources.assets_images[key][value]
                loaded_group[key] = loaded_obj
        return loaded_group
# will update when design is complete
