''' Module Name: "avatar_v2_controller.py"
    Module Description: This module acts as the central coordinator between the GUI and the
    program's model.
'''
from avatar_v2_constants import State, Status, Page

class Controller:
    ''' This class handles the coordination between the view/GUI and model. '''
    def __init__(self, view, model):
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.set_subscribers()

    def set_subscribers(self):
        ''' sets observers in model '''
        self.model.subscribe_status(self.view.save_success_message)
        self.model.subscribe_status(self.view.delete_success_message)
        self.model.subscribe_status(self.view.config_duplicate_message)
        self.model.subscribe_status(self.view.name_duplicate_message)
        self.model.subscribe_status(self.view.empty_error_message)
        self.model.subscribe_status(self.view.json_write_error)
        self.model.subscribe_status(self.view.json_read_error)

        self.model.subscribe_preview(self.view.preview_selected_assets)

    def go_to_page(self, page):
        ''' Tells the GUI to hide all frame before displaying the specified frame / page. '''
        self.view.hide_frames()
        if page is Page.CREATE:
            while True:
                category, asset = self.view.create()
                if category.upper() not in ['SAVE', 'RANDOM', 'CLEAR', 'HOME']:
                    self.view.selected_assets[category] = asset
                    self.update_selected_assets()
                if category.upper() == 'SAVE':
                    self.command_save()
                if category.upper() == 'RANDOM':
                    self.command_random()
                if category.upper() == 'CLEAR':
                    self.command_clear()
                if category.upper() == 'HOME':
                    self.command_home()
                    break
        elif page is Page.SAVES:
            if self.model.has_data_saved():
                user_input = self.view.show_saved_avatars(self.model.get_saved_data())
                self.get_selected_avatar(user_input)
            else:
                self.view.show_empty_saves()
        elif page is Page.HOME:
            self.view.home()

    def get_selected_avatar(self, user_input: str):
        ''' Processes user_input from 'Saves' page and update the selected assets in View and
            Model. '''
        get_saved_data = self.model.get_saved_data()
        if len(get_saved_data) != 0:
            saved_data = get_saved_data.copy()
            saved_list = list(saved_data.keys())
            selected_index = int(user_input) - 1
            selected_avatar = saved_list[selected_index]
            self.view.selected_assets = saved_data[selected_avatar]['configuration']
            self.update_selected_assets()

    def update_selected_assets(self):
        ''' Syncs selected assets in View and Model. '''
        selected_input = self.view.selected_assets.copy()
        self.model.update_selected_assets(selected_input)

    def command_home(self):
        ''' "Home" button command flow. '''
        if self.model.state is State.NOT_EMPTY:
            remark = self.view.lose_progress()
            if remark.upper() == "OK":
                self.view.clear_widgets()
                self.command_clear()
                self.go_to_page(Page.HOME)
        else:
            self.view.clear_widgets()
            self.command_clear()
            self.go_to_page(Page.HOME)

    def command_clear(self):
        ''' "Clear" button command flow. '''
        self.model.clear_selected_assets()
        self.view.selected_assets = self.view.set_empty_select()

    def command_random(self):
        ''' "Random" button command flow. '''
        if self.model.state is State.NOT_EMPTY:
            self.model.clear_selected_assets()
        self.model.select_random_assets(self.view.resources.assets_images)

    def command_save(self):
        ''' "Save" button command flow. '''
        self.model.is_config_already_saved()
        if self.model.status in [Status.CONFIG_DUPLICATE, Status.EMPTY_ERROR]:
            return
        avatar_name = self.view.set_avatar_name()
        self.model.set_avatar_name(avatar_name)
        if self.model.status is Status.NAME_DUPLICATE:
            return
        self.model.save_selected_assets()
        if self.model.status is Status.JSON_WRITE_ERROR:
            return

    def command_delete(self, delete_avatar):
        ''' "Delete" button command flow. '''
        self.model.delete_selected_avatar(delete_avatar)

    def command_edit(self, edit_avatar):
        ''' "Edit" button command flow. '''
        self.model.update_selected_assets(edit_avatar)
        if self.model.status is Status.UPDATE_SUCCESS:
            self.go_to_page(Page.CREATE)

    def command_exit(self):
        ''' "Exit" button command flow. '''
        self.view.exit_program()
