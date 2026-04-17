''' Module Name: "avatar_v2_model.py"
    Module Description: This module primarily manages the state of the Avatars, validates input 
    data, handles the business logic, updates, creates, processes, reads, and writes the
    JSON data storage.
'''
from json.decoder import JSONDecodeError
import random
from datetime import datetime
from avatar_v2_constants import State, Status, ObserverType

class Model:
    ''' This class processes and validates data received. '''
    def __init__(self, database):
        self.status_management = StatusManagement()
        self.database = database
        self.selected_assets = self.process_selected_assets()
        self.avatar_name = None

    @property
    def status(self):
        ''' Returns self.status from StatusManagement class. '''
        return self.status_management.status

    @property
    def state(self):
        ''' Returns self.state from StatusManagement class. '''
        return self.status_management.state

    @status.setter
    def status(self, value):
        self.status_management.status = value

    @state.setter
    def state(self, value):
        self.status_management.state = value

    def subscribe_status(self, callback):
        ''' Receives a list of subscribers and sets it to StatusManagement(). '''
        self.status_management.set_subscribers(ObserverType.STATUS, callback)

    def subscribe_preview(self, callback):
        ''' Receives a list of subscribers and sets it to StatusManagement(). '''
        self.status_management.set_subscribers(ObserverType.PREVIEW, callback)

    def process_selected_assets(self, selected_input: dict = None) -> dict:
        ''' Receives a dictionary of selected input, re-stores its values in a specific order in
            a new dictionary, and returns the new dictionary. '''
        processed_data = {
            "brows": "",
            "eyes": "",
            "mouth": "",
            "hair": "",
            "mood": "" }
        if selected_input is not None:
            selected_dict = selected_input.copy()
            for processed_key in processed_data:
                for selected_key, selected_value in selected_dict.items():
                    if processed_key == selected_key:
                        processed_data[processed_key] = selected_value
        return processed_data

    def update_selected_assets(self, selected_input: dict = None):
        ''' Receives raw selected input, calls method to process data in a specific order then
            sets the result to self.selected_assets. '''
        processed_dict = self.process_selected_assets(selected_input)
        self.selected_assets = processed_dict
        self.state = State.NOT_EMPTY
        self.status = Status.UPDATE_SUCCESS

    def select_random_assets(self, assets: dict):
        ''' Receives dictionary of all assets, iterates through all categories, selects a
            random asset for each category, then sets it to the selected assets. '''
        randomize_dict = {}
        for category, item in assets.items():
            randomize_dict[category] = random.choice(list(item))
        processed_dict = self.process_selected_assets(randomize_dict)
        self.selected_assets = processed_dict
        self.state = State.NOT_EMPTY
        self.status = Status.RANDOMIZE_SUCCESS

    def clear_selected_assets(self):
        ''' Sets the state of selected assets empty. '''
        self.selected_assets = self.process_selected_assets()
        self.state = State.EMPTY
        self.status = Status.IDLE

    def get_date_now(self):
        ''' Returns the str of the current data and time. '''
        return datetime.now().strftime("%b %d %Y | %I:%M %p")

    def set_avatar_name(self, avatar_name: str):
        ''' Sets self.avatar_name if the received name is not yet used. '''
        self.is_name_already_used(avatar_name)
        if self.status is Status.DISTINCT_NAME:
            self.avatar_name = avatar_name
            self.status = Status.SAVE_SUCCESS
        else:
            self.status = Status.NAME_DUPLICATE

    def save_selected_assets(self):
        ''' Receives a name of the avatar that is to be saved, then calls a method to check if the
            configuration is already saved, and if it's not, it will call a method to append the
            new data to the database. '''
        data = self.selected_assets.copy()
        date_saved = self.get_date_now()
        try:
            self.database.append_in_database(self.avatar_name, date_saved, data)
            self.status = Status.SAVE_SUCCESS
        except JSONDecodeError:
            self.status = Status.JSON_WRITE_ERROR

    def delete_selected_avatar(self, avatar_name: str):
        ''' Deletes selected avatar from database. '''
        saved_data = {}
        get_data = self.get_saved_data()
        if get_data is not None:
            saved_data = get_data.copy()
        else:
            self.status = Status.JSON_READ_ERROR
        if avatar_name in saved_data:
            del saved_data[avatar_name]
            try:
                self.database.update_database(saved_data)
                self.status = Status.DELETE_SUCCESS
            except JSONDecodeError:
                self.status = Status.JSON_WRITE_ERROR

    # validation methods:
    def is_name_already_used(self, name):
        ''' Checks if the name is already used in the database. '''
        if any(item == name for item in self.get_saved_data()):
            self.status = Status.NAME_DUPLICATE
        else:
            self.status = Status.DISTINCT_NAME

    def is_config_already_saved(self):
        ''' Checks if the configurations stored in self.selected_assets is already saved
            in the database and sets the self.status accordingly. '''
        if self.state is State.NOT_EMPTY:
            saved_avatars = [item['configuration'] for item in self.get_saved_data().values()]
            if self.selected_assets in saved_avatars:
                self.status = Status.CONFIG_DUPLICATE
            else:
                self.status = Status.DISTINCT_CONFIG
        else:
            self.status = Status.EMPTY_ERROR

    def has_data_saved(self) -> bool:
        ''' Checks if there's are configurations saved in the database and returns boolean.  '''
        return bool(len(self.get_saved_data()) != 0)

    # getter methods:
    def get_saved_data(self) -> dict:
        ''' Returns self.saved_data from Database class '''
        return self.database.saved_data

class StatusManagement:
    ''' Handles management of states and status, to notify observers. '''
    def __init__(self):
        self.__state = State.EMPTY
        self.__status = Status.IDLE
        self.preview_observer = []
        self.status_observer = []

    def set_subscribers(self, observer_type: ObserverType, callback):
        ''' Receives observer type constant / enum and callback to be appended to the list of
            subscribers to notify when states or status has been changed. '''
        if observer_type is ObserverType.PREVIEW:
            self.preview_observer.append(callback)
        elif observer_type is ObserverType.STATUS:
            self.status_observer.append(callback)

    def notify_subscribers(self, observer_type: ObserverType):
        ''' Receives observer type to be called to notify of its subscribers. '''
        observer_list = []
        if observer_type is ObserverType.PREVIEW:
            observer_list = self.preview_observer
        elif observer_type is ObserverType.STATUS:
            observer_list = self.status_observer

        for callback in observer_list:
            callback()

    @property
    def state(self) -> State:
        ''' Returns self.__state '''
        return self.__state

    @state.setter
    def state(self, state: State):
        ''' When called, sets self.__state to the corresponding avatar state, and broadcasts to
            subscribers.'''
        self.__state = state
        self.notify_subscribers(ObserverType.PREVIEW)

    @property
    def status(self) -> Status:
        ''' Returns self.__status '''
        return self.__status

    @status.setter
    def status(self, status: Status):
        ''' When called, sets self.__status to the corresponding result remark, and broadcasts to
            subscribers. '''
        self.__status = status
        self.notify_subscribers(ObserverType.STATUS)
