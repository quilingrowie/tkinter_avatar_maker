''' Module Name: "avatar_v2_media.py"
    Module Description: This handles reading and loading different media resources needed  in the
    GUI of the application.
'''
from pathlib import Path
from PIL import Image, ImageTk
from avatar_v2_model import BASE_DIR
from avatar_v2_exceptions import ResourcesDirectoryNotFound
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
            raise ResourcesDirectoryNotFound()
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
                    png_object = ImageTk.PhotoImage(png_item)
                    processed_group[folder.name][item.name] = png_object
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
