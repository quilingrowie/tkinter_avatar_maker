'''
This module handles the 'Creator' interface where users can customize
their portraits. It manages canvas layering, loading of asset from
local directories, and the UI logic for asset selection.
'''
import random
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

directory_path = Path(__file__).resolve().parent
# takes current directory path

class CreateAvatar:
    ''' handles real-time rendering of layered png assets and manages
        the selection interface '''
    def __init__(self, frame, resources, app):
        self.create_frame = frame
        self.app = app # accesses the running instance of AvatarApp

        self.resources = resources
        self.assets = self.load_assets()
        self.asset_icons = self.load_asset_icons()
        # contains rendered images used throughout the application

        self.selected_assets = {}
        # stores the selected configurations of the avatar

        self.screen_ui()
        # creates frames and displays canvas

    # frame and display methods
    def screen_ui (self):
        ''' defines the layout of the creator screen, including the primary 
            rendering canvas, the category sidebar, and the asset selection area. '''
        # creates container canvas for all widgets to be created
        container_canvas = tk.Canvas( self.create_frame, width=413, height=736,
                            bg="lightblue", borderwidth=0, highlightthickness=0)
        container_canvas.pack()
        container_canvas.create_image(0, 0, anchor="nw",
                                    image=self.resources["create_screen"]["create_bg.png"],
                                    tags="bg_image")
        container_canvas.tag_lower("bg_image")

        # creates rendering canvas that outputs configured avatars
        canvas = tk.Canvas(self.create_frame,
                        bg='white',
                        highlightbackground="#422b3e",
                        highlightcolor="#422b3e",
                        borderwidth=3,
                        height=290, width=290)
        container_canvas.create_window(227, 246, window=canvas, anchor="center")
        canvas.create_image((290 / 2), (290 / 2),
                            image=self.resources["canvas"]["base_avatar.png"],
                            anchor='center', tags="base")
        canvas.tag_lower("base")
        self.canvas = canvas

        # buttons at the top row of the screen
        home_button = tk.Button(self.create_frame,
                        image=self.resources["create_screen"]["home_button.png"],
                        command=self.go_home,
                        relief="flat",
                        borderwidth=0,
                        highlightthickness=0)
        save_button = tk.Button(self.create_frame,
                                image=self.resources["create_screen"]["save_button.png"],
                                relief="flat",
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.save_instance)
        clear_button = tk.Button(self.create_frame,
                                image=self.resources["create_screen"]["clear_button.png"],
                                relief="flat",
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.clear_widgets)
        random_button = tk.Button(self.create_frame,
                                image=self.resources["create_screen"]["random_button.png"],
                                relief="flat",
                                borderwidth=0,
                                highlightthickness=0,
                                command=self.random_configuration)
        container_canvas.create_window(350, 70, window=home_button)
        container_canvas.create_window(62, 75, window=save_button, anchor="center")
        container_canvas.create_window(125, 75, window=clear_button, anchor="center")
        container_canvas.create_window(197, 75, window=random_button, anchor="center")

        # creates sidebar and displaying its category buttons
        sidebar = tk.Frame(self.create_frame,
                        highlightthickness=2,
                        highlightbackground="#422b3e",
                        highlightcolor="#422b3e",
                        bg="#fad8e4",
                        height=300,
                        width=44)
        sidebar.pack_propagate(False)
        container_canvas.create_window(57, 246, window=sidebar, anchor="center")
        self.sidebar = sidebar
        self.category_buttons()

        # creates scrollbar and asset selection frame
        list_canvas = tk.Canvas(container_canvas, width=300, height=240,
                                bg="#af3164", highlightthickness=0)
                                # dedicated canvas for scrollable page
        scrollbar = tk.Scrollbar(container_canvas, orient="vertical",
                                 command=list_canvas.yview)
        container_canvas.create_window(200, 565, window=list_canvas, anchor="center")
        container_canvas.create_window(349, 565, window=scrollbar, anchor="center", height=240)
        list_canvas.configure(yscrollcommand=scrollbar.set)

        selection_frame = tk.Frame( list_canvas, borderwidth=0, relief="flat",
                                    bg="#af3164", height=240, width=250) # scrollable frame
        list_canvas.create_window((0, 0), window=selection_frame, anchor="nw")
        self.selection_frame = selection_frame
        selection_frame.bind("<Configure>",
                            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))

        starting_display = list(self.assets.keys())
        # creates copy of list of key names (categories)
        self.asset_buttons(starting_display[0])
        # displays the asset selection of the first category as the starting display

    def layer_assets(self, category, png_name):
        ''' renders the avatar on the canvas by layering .png assets.
            it maintains a dictionary of selected items and redraws the canvas accordingly '''
        selected_item = self.selected_assets.copy()
        self.clear_widgets()
        selected_item[category] = png_name
        # assigns the specific selected item to its category in selected_item list

        for key, value in selected_item.items():
            self.canvas.create_image((290 / 2), (290 / 2),
                                    anchor='center',
                                    image=self.assets[key][value],
                                    tags="this_asset")
            self.canvas.tag_raise("this_asset")
        self.selected_assets = selected_item

    # loading methods
    def load_assets(self):
        ''' creates and returns a dictionary that serves as storage for each categories 
            in 'assets' folder and their corresponding PIL image '''
        assets_path = directory_path / "assets"
        assets_dict = {}
        for folder in assets_path.iterdir():
            if folder.is_dir():
                assets_dict[folder.name] = {}
                for image in folder.glob("*.png"):
                    this_image = Image.open(image)
                    resize_image = this_image.resize((290, 290), Image.Resampling.LANCZOS)
                    # resizes image to 290x290 (size of the canvas)
                    asset_image = ImageTk.PhotoImage(resize_image)

                    assets_dict[folder.name][image.name] = asset_image
        return assets_dict

    def load_asset_icons(self):
        ''' loads smaller, thumbnail versions of assets to be used as preview buttons
            in the selection grid '''
        icons_path = directory_path / "asset_icons"
        dict_name = {}
        for folder in icons_path.iterdir():
            if folder.is_dir():
                dict_name[folder.name] = {}
                for image in folder.glob("*.png"):
                    pil_image = Image.open(image)
                    asset_image = ImageTk.PhotoImage(pil_image)
                    dict_name[folder.name][image.name] = asset_image
        return dict_name

    # creating button methods
    def category_buttons(self):
        ''' creates the buttons in sidebar for every asset category.
            these buttons allows user to toggle between different 
            customization menus like "hair", "eyes", etc. '''
        assets_dict = self.assets.copy()
        for category in assets_dict:
            this_button = tk.Button(self.sidebar,
                                    image=self.resources["create_screen"][f"{category}.png"],
                                    relief="flat",
                                    borderwidth=0,
                                    highlightthickness=0,
                                    command=lambda this_item=category:
                                        self.asset_buttons(this_item))
            this_button.pack(padx=5, pady=5)

    def asset_buttons(self, category):
        ''' displays selection frame with a grid of clickable icons based on the
            currently selected category '''
        this_frame = self.selection_frame.winfo_children()
        for widget in this_frame:
            widget.destroy()
            # destroys pre-existing buttons in self.selection frame
            # before reconstructing the new buttons to be displayed

        assets_dict = list(self.assets[category]).copy()
        # creates a copy of the list of asset filenames of the specified category
        buttons = []
        for i, asset in enumerate(assets_dict):
            if len(assets_dict) != 0:
                this_button = tk.Button(self.selection_frame,
                                        image=self.asset_icons[category][asset],
                                        relief="flat",
                                        borderwidth=0,
                                        highlightthickness=0,
                                        command=lambda index=i:
                                        self.layer_assets(category, assets_dict[index]))
                                        # asset_dict[index] accesses the filename of the
                                        # asset button selected
                buttons.append(this_button)
            else:
                continue
                # skips the iteration if folder is empty and no filenames are found
        for i, button in enumerate(buttons):
            button.grid(row=i // 3, column=i % 3, padx=18, pady=18, sticky="s")
            # displays buttons in three columns and indefinite number of rows

    # on-click command references
    def go_home(self):
        ''' triggers a confirmation dialogue before clearing current unsaved changes
            and returning to the main menu'''
        selected_items = self.selected_assets.copy()

        if self.app.saved_data is not None:
            saved_data = self.app.saved_data.copy()
        else:
            saved_data = []
        # creates copy of self.saved_data from AvatarApp if the data is not empty,
        # else creates an empty list
        if selected_items in saved_data or len(selected_items) == 0:
            self.app.show_screen(self.app.main_frame)
            self.clear_widgets()
            self.selected_assets = {}
        else:
            msg_string = "Exiting to home without saving\nLeave anyway?"
            to_return = messagebox.askokcancel(title="Exit to Home", message=msg_string)
            if to_return is True:
                self.app.show_screen(self.app.main_frame)
                self.clear_widgets()
                self.selected_assets = {}
                # clears all images in rendered canvas and emptying self.selected_assets
                # so going back once more to create screen from menu will be a clean slate

    def clear_widgets(self):
        ''' flushes all rendered image objects from the canvas to prepare for
            a new render cycle or screen transition '''
        canvas_items = self.canvas.find_withtag("this_asset")
        for items in canvas_items:
            self.canvas.delete(items)
        self.selected_assets = {}
        # emptying self.selected_assets after clearing widgets syncs
        # the display (render canvas) with the memory (self.selected_assets)

    def save_instance(self):
        ''' sends the current dictionary of selected assets to the AvatarApp
            to be validated and written to the JSON database'''
        if len(self.selected_assets) != 0:
            self.app.save_configuration(self.selected_assets)

    def random_configuration(self):
        ''' iterates through all categories and selects a random asset for each
            providing a quick start design for the user '''
        self.clear_widgets() # clears out previously selected assets

        random_select = {}
        assets_dict = self.assets.copy()
        for category, assets in assets_dict.items():
            random_select[category] = random.choice(list(assets))
        for category, image in random_select.items():
            if len(image) != 0:
                self.layer_assets(category, image)
            else:
                continue
