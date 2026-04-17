'''A practice CLI terminal for I/O.'''
# from avatar_v2_media import Resources
from avatar_v2_constants import Page, Status

class View:
    ''' I/O terminal to test the program's Controller and Model. '''
    def __init__(self, model, resources):
        self.resources = resources
        self.model = model
        self.controller = None
        self.status = self.model.status
        self.selected_assets = self.set_empty_select()

    def set_empty_select(self):
        '''docstring'''
        empty_dict = { "brows": "",
                        "eyes": "",
                        "mouth": "",
                        "hair": "",
                        "mood": "" }
        return empty_dict

    def set_controller(self, control = None):
        '''docstring'''
        self.controller = control

    def home(self):
        ''' User interface for Home. '''
        while True:
            print("----- HOME -----")
            print("Select activity:")
            print("1. Create Avatar")
            print("2. Saved Avatars")
            print("3. Exit Program")
            user_input = input("> ")
            page = ""
            if user_input == "1":
                page = Page.CREATE
            elif user_input == "2":
                page = Page.SAVES
            elif user_input == "3":
                break
            print()
            self.controller.go_to_page(page)

    def hide_frames(self):
        '''doctstring'''
        print("Hiding frames...")
        print()

    def create(self) -> tuple[str, str]:
        '''docstring'''
        print("----- CREATE -----")
        category = self.show_categories()
        asset = ""
        if category.upper() not in ['SAVE', 'RANDOM', 'CLEAR', 'HOME']:
            asset = self.show_assets(category)
        return category, asset

    def show_categories(self) -> str:
        '''docstring'''
        for i, category in enumerate(self.resources.assets_images, 1):
            print(f"{i:02d}. {category}")
        user_input = input("> ")
        if user_input.upper() not in ['SAVE', 'RANDOM', 'CLEAR', 'HOME']:
            selected_index = int(user_input) - 1
            category_list = list(self.resources.assets_images.keys())
            selected_category = category_list[selected_index]
            return selected_category
        return user_input

    def show_assets(self, category) -> str:
        '''docstring'''
        for i, asset in enumerate(self.resources.assets_images[category], 1):
            print(f"{i:02d}. {asset}")
        user_input = input("> ")
        selected_index = int(user_input) - 1
        asset_list = list(self.resources.assets_images[category].keys())
        selected_asset = asset_list[selected_index]
        return selected_asset

    def clear_widgets(self):
        '''docstring'''
        print("Clearing widgets...")

    def lose_progress(self):
        '''docstring'''
        print("If you go home without saving, you will lose progress.")
        print("Continue? [OK] [CANCEL]")
        user_input = input("> ")
        return user_input

    def show_empty_saves(self):
        '''docstring'''
        print("----- SAVES -----")
        print("No configurations saved.")
        print()

    def show_saved_avatars(self, saved_avatars: dict) -> str:
        '''docstring'''
        print("----- SAVES -----")
        for i, avatar in enumerate(saved_avatars, 1):
            print(f"{i:02d}. {avatar}")
        print("------------------")
        user_input = input("> ")
        return user_input

    def preview_selected_assets(self):
        '''docstring'''
        print("----- CREATE -----")
        selected_assets = self.model.selected_assets
        for key, value in selected_assets.items():
            if value != '':
                print(f"{key} category: '{value}' = {self.resources.assets_images[key][value]}")
            else:
                continue
        print()

    def set_avatar_name(self) -> str:
        '''docstring'''
        name = input("Enter avatar name: ")
        return name

    def save_success_message(self):
        '''docstring'''
        if self.model.status is Status.SAVE_SUCCESS:
            print("Save success.")

    def delete_success_message(self):
        '''docstring'''
        if self.model.status is Status.DELETE_SUCCESS:
            print("Delete success.")

    def config_duplicate_message(self):
        '''docstring'''
        if self.model.status is Status.CONFIG_DUPLICATE:
            print("Config already saved.")

    def name_duplicate_message(self):
        '''docstring'''
        if self.model.status is Status.NAME_DUPLICATE:
            print("Name already used.")

    def empty_error_message(self):
        '''docstring'''
        if self.model.status is Status.EMPTY_ERROR:
            print("Can't be saved. Configuration is empty.")

    def json_write_error(self):
        '''docstring'''
        if self.model.status is Status.JSON_WRITE_ERROR:
            print("An error occured while writing JSON file.")

    def json_read_error(self):
        '''docstring'''
        if self.model.status is Status.JSON_READ_ERROR:
            print("An error occured while reading JSON file.")
