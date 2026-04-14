''' Module Name: "avatar_v2_controller.py"
    Module Description: This module acts as the central coordinator between the GUI and the
    program's model.
'''
from avatar_v2_model import State, Status
class Controller:
    ''' This class handles the coordination between the view/GUI and model. '''
    def __init__(self, view, model):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def go_to_page(self, page: str):
        ''' Tells the GUI to hide all frame before displaying the specified frame / page. '''
        if page != "EXIT":
            self.view.hide_frames()
            self.view.pack_frame(page)
        # else:
        #     self.command_exit()

    def update_selected_assets(self):
        ''' Syncs selected assets in View and Model. '''
        selected_input = self.view.selected_assets.copy()
        self.model.update_selected_assets(selected_input)

    def command_home(self):
        ''' "Home" button command flow. '''
        if self.model.state is State.EMPTY:
            self.view.clear_widgets()
            self.go_to_page("HOME")

    def command_clear(self):
        ''' "Clear" button command flow. '''
        self.model.clear_selected_assets()

    def command_random(self):
        ''' "Random" button command flow. '''
        if self.model.state is State.NOT_EMPTY:
            self.model.clear_selected_assets()
        self.model.select_random_assets()

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
        if self.model.status is Status.JSON_ERROR:
            return

    def command_delete(self, delete_avatar):
        ''' "Delete" button command flow. '''
        self.model.deleted_selected_avatar(delete_avatar)

    def command_edit(self, edit_avatar):
        ''' "Edit" button command flow. '''
        self.model.update_selected_assets(edit_avatar)
        if self.model.status is Status.UPDATE_SUCCESS:
            self.go_to_page("CREATE")

    def command_exit(self):
        ''' "Exit" button command flow. '''
        self.view.exit_program()
