''' Module Name: "avatar_v2_model.py"
    Module Description: This module primarily updates, creates, processes, reads, and writes the
    JSON data storage as well as .png resource files according to the program's controller's
    requests. 
'''
import json
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageTk
import avatar_v2_exceptions as e

BASE_DIR = Path(__file__).resolve().parent

class Model:
    ''' This class processes and validates data received. '''
    def __init__(self, database, resources):
        self.database = database
        self.resources = resources
        self.update_selected_assets()

    def set_selected_assets(self, selected_input: dict = None) -> dict:
        ''' Receives a dictionary of selected input, re-stores its values in a specific order in
            a new dictionary, and returns the new dictionary. '''
        processed_data = {
            "brows": "",
            "eyes": "",
            "mouth": "",
            "mood": "" }
        if selected_input is not None:
            selected_dict = selected_input.copy()
            for processed_key in processed_data:
                for selected_key, selected_value in selected_dict.items():
                    if processed_key == selected_key:
                        processed_data[processed_key] = selected_value
        return processed_data

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

    def update_selected_assets(self, selected_input: dict = None):
        ''' Lets self.selected_assets and self.loaded_assets update its contents in parallel. '''
        self.selected_assets = self.set_selected_assets(selected_input)
        self.loaded_assets = self.load_selected_assets()

    def save_configurations_to_database(self):
        ''' Calls a method to check if the configuration is already and appropriately raises an
            exception, otherwise calls the method that saves the configurations to the database. '''
        remark = self.is_configuration_already_saved()
        if remark is True:
            raise e.ConfigurationExists()
        if remark is None:
            raise e.ConfigurationEmpty()
        if remark is False:
            data = self.selected_assets.copy()
            date_saved = datetime.now()
            date_saved_str = date_saved.strftime("%b %d %Y | %I:%M %p")
            self.database.write_in_database(date_saved_str, data)

    def is_configuration_already_saved(self) -> bool:
        ''' Checks if the configurations stored in self.selected_assets is already saved
            in the database and returns boolean accordingly.'''
        if any(value != "" for value in self.selected_assets.values()):
            if self.selected_assets in self.database.saved_data.values():
                return True
            return False
        return None

    # getter methods:
    def get_saved_data(self) -> dict:
        ''' Returns self.saved_data from Database class '''
        return self.database.saved_data

    def get_icons(self) -> dict:
        ''' Returns self.icons from Resources class '''
        return self.resources.icons

    def get_backgrounds(self) -> dict:
        ''' Returns self.backgrounds from Resources class '''
        return self.resources.backgrounds

    def get_assets_images(self) -> dict:
        ''' Returns self.assets_images from Resources class '''
        return self.resources.assets_images

    def get_assets_icons(self) -> dict:
        ''' Returns self.assets_icons from Resources class '''
        return self.resources.assets_icons

class Database:
    ''' Handles writing and reading of JSON file. '''
    def __init__(self):
        self.database_dirpath = self.check_directories()
        self.database_filepath = self.check_database_filepath()
        self.saved_data = self.read_database()

    @e.catch_file_handling_exceptions
    def check_directories(self) -> Path:
        ''' Checks if directories "storage", and "database" exists, otherwise creates them. Returns
            database_dirpath to be stored in the constructor. '''
        # checks if "storage" directory exists within "storage" directory, otherwise creates them
        storage_dirpath = BASE_DIR / "storage"
        if not storage_dirpath.exists():
            storage_dirpath.mkdir(parents=True, exist_ok=True)

        # checks if "database" directory exists within "storage" directory, otherwise creates them
        database_dirpath = storage_dirpath / "database"
        if not database_dirpath.exists():
            database_dirpath.mkdir(parents=True, exist_ok=True)
        return database_dirpath

    @e.catch_file_handling_exceptions
    def check_database_filepath(self) -> Path:
        ''' Checks if file "saved_avatars.json" exists within the "database" directory, and
            otherwise creates it. Returns filepath of "saved_avatars.json".'''
        database_filepath = self.database_dirpath / "saved_avatars.json"
        if not database_filepath.exists():
            with open(database_filepath, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)
                # creates a file with an empty dictionary inside
        return database_filepath

    @e.catch_file_handling_exceptions
    def read_database(self) -> dict:
        ''' Reads the JSON file "saved_avatars.json" and returns its (dictionary) contents. '''
        with open(self.database_filepath, "r", encoding="utf-8") as file:
            saved_data = json.load(file)
            return saved_data

    @e.catch_file_handling_exceptions
    def write_in_database(self, date_saved: str, data: dict):
        ''' Receives string "date_saved" and dictionary "data", and creates a new key (saved_date)
            and value (data) to be appended and saved in the JSON database. Updates self.saved_data
            with the updated JSON file. '''
        old_content = self.saved_data.copy()
        old_content[date_saved] = data
        with open(self.database_filepath, 'w', encoding="utf-8") as file:
            json.dump(old_content, file, indent=4)
        self.saved_data = self.read_database()

class Resources:
    ''' Handles processing of ".png" files in "resources" directory into a PIL object, store them
        in dictionaries that will be used in the GUI '''
    def __init__(self):
        self.resources_dirpath = self.check_resources_dirpath()
        (self.icons, self.backgrounds,
         self.assets_images, self.assets_icons) = self.process_resources_dir()

    def check_resources_dirpath(self) -> Path:
        ''' Checks if "resources" folder exists within the "storage" directory, and returns its
            filepath, otherwise raises a custom exception. '''
        resources_dirpath = BASE_DIR / "storage" / "resources"
        if not resources_dirpath.exists():
            raise e.ResourcesDirectoryNotFound()
        return resources_dirpath

    def process_resources_dir(self) -> tuple[dict, dict, dict, dict]:
        ''' Processes the folders "icons", "backgrounds", "assets" within "resources" directory,
            otherwise raises a custom exception. '''
        icons_dict = self.process_dir_contents(self.resources_dirpath / "icons")
        background_dict = self.process_dir_contents(self.resources_dirpath / "backgrounds")
        asset_images_dict, asset_icons_dict = self.check_assets_dir()
        return icons_dict, background_dict, asset_images_dict, asset_icons_dict

    def process_dir_contents(self, this_dir: Path) -> dict:
        ''' Checks if the specified directory exists inside "resources" directory
            and processes its png files into PIL objects, stores them in a dictionary, and
            returns them. '''
        if not this_dir.exists():
            raise FileNotFoundError(
                "FileNotFoundError occured in function process_dir_contents():\n"+
                f"No folder {this_dir} found inside 'resources' directory."
            )
        processed_group = {}
        for folder in this_dir.iterdir():
            if folder.is_dir():
                processed_group[folder.name] = {}
                for item in folder.glob("*.png"):
                    png_item = Image.open(item)
                    png_obj = ImageTk.PhotoImage(png_item)
                    processed_group[folder.name][item.name] = png_obj
        return processed_group

    def check_assets_dir(self) -> tuple[dict, dict]:
        ''' Checks if "assets" folder exists within the resources directory, and calls a helper
            function to process their contents before returning it, otherwise raises
            FileNotFoundError. '''
        dir_path = self.resources_dirpath / "assets"
        if not dir_path.exists():
            raise FileNotFoundError(
                "FileNotFoundError occured in function check_assets_dir():\n"
                "'assets' directory not found."
            )
        images_dict = self.process_dir_contents(dir_path / "images")
        icons_dict = self.process_dir_contents(dir_path / "icons")
        return images_dict, icons_dict
