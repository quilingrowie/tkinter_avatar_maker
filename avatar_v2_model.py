''' Module Name: "avatar_v2_model.py"
    Module Description: This module primarily updates, creates, processes, and reads the JSON
    data storage as well as .png resource files according to the program's controller's requests. 
'''
import json
from pathlib import Path

def catch_file_handling_exceptions(function):
    ''' A decorator function that catches errors on file handling methods/functions. '''
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"FileNotFoundError occured in function {function.__name__}:")
            print("Attempting to access a file or directory that does not exist.")
            print(f"Error: {e}")
        except PermissionError as e:
            print(f"PermissionError occured in {function.__name__}:")
            print("Attempting to perform operations that does not meet user permissions.")
            print(f"Error: {e}")
        except NotADirectoryError as e:
            print(f"NotADirectoryError occured in {function.__name__}:")
            print("Attempting to do directory-only operations on a file.")
            print(f"Error: {e}")
        except IsADirectoryError as e:
            print(f"IsADirectoryError occured in {function.__name__}:")
            print("Attempting to do a file-only operations on a directory.")
            print(f"Error: {e}")
    return wrapper

class Model:
    ''' Processes data -- '''
    def __init__(self):
        self.database = Database()
        self.selected_assets = self.set_selected_assets()

    def set_selected_assets(self, selected_assets: dict = None):
        ''' Receives a dictionary to be stored in self.selected_assets, processes them in a new
            dictionary storage which arranges them in a specific order, and returns the new
            dictionary to be stored in self.selected_assets. '''
        asset_dict = {}
        if selected_dict is not None:
            selected_dict = selected_assets.copy()
            asset_dict = {
                "brows": "",
                "eyes": "",
                "mouth": "",
                "mood": "" }
            for asset_key in asset_dict:
                for selected_key, selected_value in selected_dict.items():
                    if asset_key == selected_key:
                        asset_dict[asset_key] = selected_value
        return asset_dict

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

    @catch_file_handling_exceptions
    def check_directories(self) -> Path:
        ''' Checks if directories "storage", "database", and "resources" exists, otherwise creates
            them or raises and exception. Returns database_dirpath to be stored in the
            constructor. '''
        directory_path = Path(__file__).resolve().parent

        # checks if "storage" directory exists
        storage_dirpath = directory_path / "storage"
        if not storage_dirpath.exists():
            storage_dirpath.mkdir(parents=True, exist_ok=True)

        # checks if "database" directory exists within "storage" directory, otherwise creates them
        database_dirpath = storage_dirpath / "database"
        if not database_dirpath.exists():
            database_dirpath.mkdir(parents=True, exist_ok=True)

        # checks if "resources" directory exists, otherwise raises FileNotFoundError
        recourses_dirpath = storage_dirpath / "resources"
        if not recourses_dirpath.exists():
            message_1 = "Directory 'resources' not found."
            message_2 = "Missing required files for the application to run."
            error_message = f"{message_1}\n{message_2}"
            raise FileNotFoundError(error_message)

        return database_dirpath

    @catch_file_handling_exceptions
    def check_database_filepath(self) -> Path:
        ''' Checks if file "saved_avatars.json" exists within the "database" directory, and
            otherwise creates it. Returns filepath of "saved_avatars.json".'''
        database_filepath = self.database_dirpath / "saved_avatars.json"
        if not database_filepath.exists():
            with open(database_filepath, "w", encoding="utf-8") as file:
                json.dump(file, {}, indent=4)
                # creates a file with an empty dictionary inside
        return database_filepath

    @catch_file_handling_exceptions
    def read_database(self) -> dict:
        ''' Reads the JSON file "saved_avatars.json" and returns its (dictionary) contents. '''
        with open(self.database_filepath, "r", encoding="utf-8") as file:
            saved_data = json.load(file)
            return saved_data
