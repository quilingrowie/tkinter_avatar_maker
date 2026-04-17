''' Module Name: avatar_v2_database.py
    Module Description: This module reads data from JSON data storage, and handles writing inputs
    from the model. '''
import json
from pathlib import Path
import avatar_v2_exceptions as err

BASE_DIR = Path(__file__).resolve().parent

class Database:
    ''' Handles writing and reading of JSON file. '''
    def __init__(self):
        self.database_dirpath = self.check_directories()
        self.database_filepath = self.check_database_filepath()
        self.saved_data = self.read_database()

    @err.catch_file_handling_exceptions
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

    @err.catch_file_handling_exceptions
    def check_database_filepath(self) -> Path:
        ''' Checks if file "saved_avatars.json" exists within the "database" directory, and
            otherwise creates it. Returns filepath of "saved_avatars.json".'''
        database_filepath = self.database_dirpath / "saved_avatars.json"
        if not database_filepath.exists():
            with open(database_filepath, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)
                # creates a file with an empty dictionary inside
        return database_filepath

    @err.catch_file_handling_exceptions
    def read_database(self) -> dict:
        ''' Reads the JSON file "saved_avatars.json" and returns its (dictionary) contents. '''
        with open(self.database_filepath, "r", encoding="utf-8") as file:
            saved_data = json.load(file)
            return saved_data

    @err.catch_file_handling_exceptions
    def append_in_database(self, avatar_name: str, date_saved: str, data: dict):
        ''' Receives credentials to be appended and saved in the JSON database.
            Calls a method to append the self.saved_data with the new dictionary contents. '''
        # data structure: avatar_name = {'date_saved' = date_saved, 'configuration' = data}
        old_content = self.saved_data.copy()
        old_content[avatar_name] = {}
        old_content[avatar_name]['date_saved'] = date_saved
        old_content[avatar_name]['configuration'] = data
        self.update_database(old_content)

    @err.catch_file_handling_exceptions
    def update_database(self, data: dict):
        ''' Receives a new dictionary to be saved in the JSON database, updates self.saved_data
            with the updates JSON file. '''
        with open(self.database_filepath, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        self.saved_data = self.read_database()
