''' Module Name: "avatar_v2_model.py"
    Module Description: This module primarily manages the state of the Avatars, validates input 
    data, handles the business logic, updates, creates, processes, reads, and writes the
    JSON data storage.
'''
import json
import random
from enum import Enum, auto
from pathlib import Path
from datetime import datetime
import avatar_v2_exceptions as e

BASE_DIR = Path(__file__).resolve().parent

class State(Enum):
    ''' State constants. '''
    EMPTY = auto()
    NOT_EMPTY = auto()

class Status(Enum):
    ''' Result status constants. '''
    DISTINCT_CONFIG = auto()
    DISTINCT_NAME = auto()
    SAVE_SUCCESS = auto()
    DELETE_SUCCESS = auto()
    UPDATE_SUCCESS = auto()
    RANDOMIZE_SUCCESS = auto()
    CLEAR_SUCCESS = auto()
    IDLE = auto()

    CONFIG_DUPLICATE = auto()
    NAME_DUPLICATE = auto()
    EMPTY_ERROR = auto()
    JSON_ERROR = auto()

class Model:
    ''' This class processes and validates data received. '''
    def __init__(self, database):
        self.status = StatusManagement().status
        self.state = StatusManagement().state
        self.database = database
        self.selected_assets = self.process_selected_assets()
        self.avatar_name = None

    def subscribe_status(self, callback):
        StatusManagement().subscribe_status(callback)

    def subscribe_preview(self, callback):
        StatusManagement().subscribe_preview(callback)

    def process_selected_assets(self, selected_input: dict = None) -> dict:
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

    def update_selected_assets(self, selected_input: dict = None) -> Status:
        ''' Receives raw selected input, calls method to process data in a specific order then
            sets the result to self.selected_assets. '''
        processed_dict = self.process_selected_assets(selected_input)
        self.selected_assets = processed_dict
        self.state = State.NOT_EMPTY
        self.status = Status.UPDATE_SUCCESS

    def select_random_assets(self, assets: dict) -> Status:
        ''' Receives dictionary of all assets, iterates through all categories, selects a
            random asset for each category, then sets it to the selected assets. '''
        randomize_dict = {}
        for category, item in assets.items():
            randomize_dict[category] = random.choice(list(item))
        processed_dict = self.process_selected_assets(randomize_dict)
        self.selected_assets = processed_dict
        self.state = State.NOT_EMPTY
        self.status = Status.RANDOMIZE_SUCCESS

    def clear_selected_assets(self) -> Status:
        ''' Sets the state of selected assets empty. '''
        self.selected_assets = self.process_selected_assets()
        self.state = State.EMPTY
        self.status = Status.IDLE

    def get_date_now(self):
        ''' Returns the str of the current data and time. '''
        return datetime.now().strftime("%b %d %Y | %I:%M %p")

    def set_avatar_name(self, avatar_name: str) -> Status:
        ''' Sets self.avatar_name if the received name is not yet used. '''
        self.is_name_already_used(avatar_name)
        if self.status is Status.DISTINCT_NAME:
            self.avatar_name = avatar_name
            self.status = Status.SAVE_SUCCESS
        else:
            self.status = Status.NAME_DUPLICATE

    def save_selected_assets(self) -> Status:
        ''' Receives a name of the avatar that is to be saved, then calls a method to check if the
            configuration is already saved, and if it's not, it will call a method to append the
            new data to the database. '''
        data = self.selected_assets.copy()
        date_saved = self.get_date_now()
        try:
            self.database.append_in_database(self.avatar_name, date_saved, data)
            self.status = Status.SAVE_SUCCESS
        except json.JSONDecodeError:
            self.status = Status.JSON_ERROR

    def delete_selected_avatar(self, avatar_name: str) -> Status:
        ''' Deletes selected avatar from database. '''
        saved_data = self.get_saved_data().copy()
        if avatar_name in saved_data:
            del saved_data[avatar_name]
            try:
                self.database.update_database(saved_data)
                self.status = Status.DELETE_SUCCESS
            except json.JSONDecodeError:
                self.status = Status.JSON_ERROR

    # validation methods:
    def is_name_already_used(self, name) -> Status:
        ''' Checks if the name is already used in the database. '''
        if any(item == name for item in self.get_saved_data()):
            self.status = Status.NAME_DUPLICATE
        self.status = Status.DISTINCT_NAME

    def is_config_already_saved(self) -> Status:
        ''' Checks if the configurations stored in self.selected_assets is already saved
            in the database and sets the self.status accordingly. '''
        if self.state is State.NOT_EMPTY:
            saved_avatars = [item['configuration'] for item in self.get_saved_data().values()]
            if self.selected_assets in saved_avatars:
                self.status = Status.CONFIG_DUPLICATE
            self.status = Status.DISTINCT_CONFIG
        self.status = Status.EMPTY_ERROR

    # getter methods:
    def get_saved_data(self) -> dict:
        ''' Returns self.saved_data from Database class '''
        return self.database.saved_data

class StatusManagement:
    ''' Handles management of states and status, to notify observers. '''
    def __init__(self):
        self.__preview_observers = []
        self.__status_observers = []
        self.__state = State.EMPTY
        self.__status = Status.IDLE

    def subscribe_preview(self, callback):
        ''' Adds callback to the list of subscribers to notify when avatar state has changed. '''
        self.__preview_observers.append(callback)

    def notify_preview(self):
        ''' Calls functions in self.__preview_observers to run or update. '''
        for callback in self.__preview_observers:
            callback()

    @property
    def state(self):
        ''' Returns self.__state '''
        return self.__state

    @state.setter
    def state(self, state):
        ''' When called, sets self.__state to the corresponding avatar state, and broadcasts to
            subscribers.'''
        self.__state = state
        self.notify_preview()

    def subscribe_status(self, callback):
        ''' Adds callback to the list of subscribers to notify when result status has chaanged.'''
        self.__status_observers.append(callback)

    def notify_status(self):
        ''' Calls functions in self.__status_observers to run or update. '''
        for callback in self.__status_observers:
            callback()

    @property
    def status(self):
        ''' Returns self.__status '''
        return self.__status

    @status.setter
    def status(self, status):
        ''' When called, sets self.__status to the corresponding result remark, and broadcasts to
            subscribers. '''
        self.__status = status
        self.notify_status()

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
    def append_in_database(self, avatar_name: str, date_saved: str, data: dict):
        ''' Receives credentials to be appended and saved in the JSON database.
            Calls a method to append the self.saved_data with the new dictionary contents. '''
        # data structure: avatar_name = {'date_saved' = date_saved, 'configuration' = data}
        old_content = self.saved_data.copy()
        old_content[avatar_name] = {}
        old_content[avatar_name]['date_saved'] = date_saved
        old_content[avatar_name]['configuration'] = data
        self.update_database(old_content)

    @e.catch_file_handling_exceptions
    def update_database(self, data: dict):
        ''' Receives a new dictionary to be saved in the JSON database, updates self.saved_data
            with the updates JSON file. '''
        with open(self.database_filepath, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        self.saved_data = self.read_database()
