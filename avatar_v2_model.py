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

class Model:
    ''' This class processes and validates data received. '''
    def __init__(self, database):
        self.database = database
        self.selected_assets = self.set_selected_assets()

    def set_selected_assets(self, selected_input: dict = None) -> dict:
        ''' Receives a dictionary to be stored in self.selected_assets, processes them in a new
            dictionary storage which arranges them in a specific order, and returns the new
            dictionary to be stored in self.selected_assets. '''
        processed_data = {}
        if selected_input is not None:
            selected_dict = selected_input.copy()
            processed_data = {
                "brows": "",
                "eyes": "",
                "mouth": "",
                "mood": "" }
            for processed_key in processed_data:
                for selected_key, selected_value in selected_dict.items():
                    if processed_key == selected_key:
                        processed_key[processed_data] = selected_value
        return processed_data

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
        # creates workable copy of data
        selected_assets = self.selected_assets.copy()
        saved_data = self.database.saved_data.copy()

        if len(selected_assets) != 0:
            if selected_assets in saved_data:
                return True
            return False
        return None

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
        directory_path = Path(__file__).resolve().parent

        # checks if "storage" directory exists
        storage_dirpath = directory_path / "storage"
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
            and value (data) to be appended and saved in the JSON database. '''
        old_content = self.read_database()
        old_content[date_saved] = data
        with open(self.database_filepath, 'w', encoding="utf-8") as file:
            json.dump(old_content, file, indent=4)

class Resources:
    ''' Handles processing of ".png" files in "resources" directory into a PIL object, store them
        in dictionaries that will be used in the GUI '''
    def __init__(self):
        self.icons = self.check_resources_dir()

    def check_resources_dir(self):
        ''' Checks if "resources" folder exists within the "storage" directory, and processes
            the folders within it, otherwise raises a custom exception. '''
        recourses_dirpath = Path(__file__).resolve().parent / "storage" / "resources"
        if recourses_dirpath.exists():
            try:
                for folder in recourses_dirpath.iterdir():
                    if folder.is_dir():
                        if folder.name == "icons":
                            icons_dict = self.check_icons_dir()
                            # calls method that processes icons
                        if folder.name == "backgrounds":
                            self.check_backgrounds_dir()
                            # calls method that processes backgrounds
                        if folder.name == "assets":
                            self.check_assets_dir()
                            # calls method that processes assets
            except FileNotFoundError as error:
                message_1 = "FileNotFoundError occured in function check_resources_dir():"
                message_2 = "No folders found inside 'resources' directory."
                raise FileNotFoundError( message_1 + "\n" + message_2 ) from error
            except PermissionError as error:
                message_1 = "PermissionError occured in function check_resources_dir:"
                message_2 = "Attempting to access protected folder."
                raise PermissionError( message_1 + "\n" + message_2 ) from error
        else:
            raise e.ResourcesDirectoryNotFound()
        return icons_dict

    def check_icons_dir(self):
        ''' Checks if "icons" folder exists within the resources directory, and prcoesses its
            contents before returning it, otherwise raises FileNotFoundError. '''
        dir_path = Path(__file__).resolve().parent / "storage" / "resources" / "icons"
        icons_dict = {}
        if dir_path.exists():
            try:
                for folder in dir_path.iterdir():
                    if folder.is_dir():
                        icons_dict[folder.name] = {}
                        for image in folder.glob("*.png"):
                            this_image = Image.open(image)
                            image_obj = ImageTk.PhotoImage(this_image)
                            icons_dict[folder.name][image.name] = image_obj
            except FileNotFoundError as error:
                message_1 = "FileNotFoundError occured in function check_icons_dir():"
                message_2 = "No folders found inside 'icons' directory. "
                raise FileNotFoundError(message_1 + "\n" + message_2) from error
        else:
            message_1 = "FileNotFoundError occured in function check_icons_dir():"
            message_2 = "'icons' directory not found."
            raise FileNotFoundError(message_1 + "\n" + message_2)
        return icons_dict

    def check_backgrounds_dir(self):
        ''' Checks if "backgrounds" folder exists within the resources directory, and prcoesses its
            contents before returning it, otherwise raises FileNotFoundError. '''
        dir_path = Path(__file__).resolve().parent / "storage" / "resources" / "backgrounds"
        backgrounds_dict = {}
        if dir_path.exists():
            try:
                for folder in dir_path.iterdir():
                    if folder.is_dir():
                        backgrounds_dict[folder.name] = {}
                        for image in folder.glob("*.png"):
                            this_image = Image.open(image)
                            image_obj = ImageTk.PhotoImage(this_image)
                            backgrounds_dict[folder.name][image.name] = image_obj
            except FileNotFoundError as error:
                message_1 = "FileNotFoundError occured in function check_backgrounds_dir():"
                message_2 = "No folders found inside 'backgrounds' directory. "
                raise FileNotFoundError(message_1 + "\n" + message_2) from error
        else:
            message_1 = "FileNotFoundError occured in function check_backgrounds_dir():"
            message_2 = "'backgrounds' directory not found."
            raise FileNotFoundError(message_1 + "\n" + message_2)
        return backgrounds_dict

    def check_assets_dir(self):
        ''' Checks if "assets" folder exists within the resources directory, and prcoesses its
            contents before returning it, otherwise raises FileNotFoundError. '''
        dir_path = Path(__file__).resolve().parent / "storage" / "resources" / "assets"
        images_dict = {}
        icons_dict = {}
        if dir_path.exists():
            try:
                for folder in dir_path.iterdir():
                    if folder.is_dir() and folder.name == "images":
                        for inner_folder in folder.iterdir():
                            if inner_folder.is_dir():
                                images_dict[inner_folder.name] = {}
                                for image in inner_folder.glob("*.png"):
                                    this_image = Image.open(image)
                                    image_obj = ImageTk.PhotoImage(this_image)
                                    images_dict[inner_folder.name][image.name] = image_obj
                    if folder.is_dir() and folder.name == "icons":
                        for inner_folder in folder.iterdir():
                            if inner_folder.is_dir():
                                icons_dict[inner_folder.name] = {}
                                for image in inner_folder.glob("*.png"):
                                    this_image = Image.open(image)
                                    image_obj = ImageTk.PhotoImage(this_image)
                                    icons_dict[inner_folder.name][image.name] = image_obj
            except FileNotFoundError as error:
                message_1 = "FileNotFoundError occured in function check_assets_dir():"
                message_2 = "No folders / specific folder found inside 'assets' directory."
                raise FileNotFoundError(message_1 + "\n" + message_2) from error
        else:
            message_1 = "FileNotFoundError occured in function check_assets_dir():"
            message_2 = "'icons' directory not found."
            raise FileNotFoundError(message_1 + "\n" + message_2)
        return images_dict, icons_dict
    # ^ too many nested blocks, will refactor later
