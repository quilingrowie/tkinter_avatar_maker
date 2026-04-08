'''
This module acts as the central controller for the Avatar Portrait Creator.
It manages the primary Tkinter root window, handles screen transitions
between the main menu, creator, and save screens, and persists user
configurations using JSON-based storage.
'''
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
from tk_create_avatar import CreateAvatar

directory_path = Path(__file__).resolve().parent
# takes the current directory path

class AvatarApp:
    ''' primary application controller that manages global state,
        resources, and sets up the primary frame containers for screen management.'''
    def __init__(self, root):
        self.root = root

        self.resources = self.load_resources()
        # loads image resources for labels and buttons

        self.main_frame = tk.Frame(self.root)
        self.create_frame = tk.Frame(self.root)
        self.save_frame = tk.Frame(self.root)
        # create frames

        self.saved_data = self.load_data()
        # loads saved avatar configurations from json file
        self.date_saved = self.load_date_saves()
        # paralles the json list and records the saved date and time for each configuration
        self.check_database()

        self.main_screen()
        self.create_screen = CreateAvatar(self.create_frame, self.resources, self)
        # loads static screens / UI of main screen and avatar screen

        self.show_screen(self.main_frame)
        # packs and loads main frame upon initialization

    # screen methods
    def main_screen(self):
        ''' constructs the landing page UI, including the background image
            and navigation buttons to enter the creator or view saves. '''
        screen_bg = tk.Label(self.main_frame,
                                image=self.resources["main_screen"]["main_bg.png"])
        screen_bg.pack()
        create_avatar_button = tk.Button(self.main_frame,
                                        relief="flat",
                                        highlightthickness=0,
                                        borderwidth=0,
                                        image=self.resources["main_screen"]["button_create.png"],
                                        command=lambda: self.show_screen(self.create_frame))
        create_avatar_button.place(relx=0.5, rely=0.64, anchor="center")

        load_save_button = tk.Button(self.main_frame,
                                    relief="flat",
                                    highlightthickness=0,
                                    borderwidth=0,
                                    image=self.resources["main_screen"]["button_save.png"],
                                    command=lambda: self.show_screen(self.save_frame))
        load_save_button.place(relx=0.5, rely=0.72, anchor="center")

        exit_button = tk.Button(self.main_frame,
                                relief="flat",
                                highlightthickness=0,
                                borderwidth=0,
                                image=self.resources["main_screen"]["button_exit.png"],
                                command=self.root.destroy)
        exit_button.place(relx=0.5, rely=0.80, anchor="center")

    def save_screen(self):
        ''' builds the save management interface. it reads the
            local JSON database to generate a scrollable grid of previously
            saved avatar and configurations. '''
        for widget in self.save_frame.winfo_children():
            widget.destroy()
            # since the buttons in this method depends on the saved json file,
            # the widgets here gets destroyed and reconstructed to "refresh" the screen
        container_canvas = tk.Canvas(self.save_frame, width=413, height=736,
                                    borderwidth=0, highlightthickness=0)
        container_canvas.pack()
        container_canvas.create_image(0, 0, anchor="nw",
                                image=self.resources["save_screen"]["save_bg.png"],
                                tags="save_screen_bg")
        container_canvas.tag_lower("save_screen_bg")
        container_canvas.create_image(206, 380, anchor="center",
                                image=self.resources["save_screen"]["inner_frame.png"])

        # creating scrollbar
        list_canvas = tk.Canvas(container_canvas, width=290, height=545,
                                bg="#fad8e4", highlightthickness=0)
                                # dedicated canvas for scrollable page
        container_canvas.create_window(206, 380, window=list_canvas, anchor="center")
        scrollbar = tk.Scrollbar(container_canvas, orient="vertical", command=list_canvas.yview)
        container_canvas.create_window(341, 380, window=scrollbar, anchor="center", height=545)
        list_canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = tk.Frame(list_canvas, borderwidth=0,
                                highlightthickness=0, background="#fad8e4")
        list_canvas.create_window((0, 0), anchor="nw", window=scrollable_frame)
        scrollable_frame.bind("<Configure>",
                            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))

        # creating buttons
        home_button = tk.Button(self.save_frame,
                        image=self.resources["save_screen"]["home_icon.png"],
                        command=lambda: self.show_screen(self.main_frame),
                        relief="flat",
                        borderwidth=0,
                        highlightthickness=0)
        container_canvas.create_window(350, 72, window=home_button)

        if len(self.saved_data) != 0:
            data_copy = self.saved_data.copy() # create workable copy of data
            dates = self.date_saved.copy()
            for i, items in enumerate(data_copy):
                # reads saved data from JSON file
                # creates a button and positions them in columns of 3 for each saved configuration
                base_row = (i // 3) * 2
                col = i % 3
                this_button = tk.Button(scrollable_frame,
                                        image=self.resources["save_screen"]["image_icon.png"],
                                        borderwidth=0, highlightthickness=0, relief="flat",
                                        command=lambda d=items: self.load_configurations(d))
                this_button.grid(row=base_row, column=col, padx=15, pady=(15, 0), sticky="s")
                label_string = dates[i]
                label_file = tk.Label(scrollable_frame,
                                    text=f"{label_string}", fg="#291925", bg="#fad8e4",
                                    font=("Tahoma", 7, "italic"))
                label_file.grid(row=base_row + 1, column=col, padx= 15, pady=(0, 15), sticky="n")
        else:
            info_label = tk.Label(scrollable_frame,
                                  text="No saved configurations yet.", fg="#291925", bg="#fad8e4",
                                  font=("Tahoma", 10, "italic"))
            info_label.pack(padx=20, pady=20)

    def show_screen(self, frame):
        ''' manages UI navigation by hiding all top-level frames and
            packing the requested frame into the window. '''
        for each_frame in (self.main_frame, self.create_frame, self.save_frame):
            each_frame.pack_forget()
        if frame == self.save_frame:
            self.save_screen()  # loads save_screen() if self.save_frame
                                # gets passed as the parameter
        frame.pack(fill="both", expand=True)

    # rendering methods
    def load_resources(self):
        ''' scans the 'resources' folder to load UI-specific images (buttons,
            backgrounds, icons) into a nested dictionary for global access. '''
        resources_images = {}
        resources_path = directory_path / "resources"

        for folder in resources_path.iterdir():
            if folder.is_dir():
                resources_images[folder.name] = {}
                for image in folder.glob("*.png"):
                    # converts .png files into PIL object
                    this_image = Image.open(image)
                    image_object = ImageTk.PhotoImage(this_image)

                    resources_images[folder.name][image.name] = image_object
        return resources_images

    def load_configurations(self, saved_avatar):
        ''' takes a specific configuration dictionary and passes it to
            the CreateAvatar instance to render a previously saved design '''
        for category, image_name in saved_avatar.items():
            self.create_screen.selected_assets[category] = image_name
            self.create_screen.layer_assets(category, image_name)
        self.show_screen(self.create_frame)

    def save_configuration(self, saved_avatar):
        ''' validates and persists a new avatar configuration to "saved_avatar_configuration.json".
            ensures duplicate configurations aren't saved and handles file
            creation if the database does not exist '''
        this_data = saved_avatar.copy()
        database = self.saved_data.copy()
        saved_date = self.date_saved.copy()
        # creates copy of each saved data to work with
        try:
            if this_data not in database:
                current_date = datetime.now()
                date_string = current_date.strftime("%b %d %Y:\n%I:%M %p")

                database.append(this_data)
                saved_date.append(date_string)

                database_path = directory_path / "saved_avatar_configuration.json"
                dates_path = directory_path / "dates.json"

                with open(database_path, "w", encoding="utf-8") as file:
                    json.dump(database, file, indent=4)
                with open(dates_path, "w", encoding="utf-8") as dates:
                    json.dump(saved_date, dates, indent=4)
                messagebox.showinfo(title=None, message="Saved!")
            else:
                messagebox.showinfo(title=None, message="Configuration already saved.")
        except json.JSONDecodeError as e:
            messagebox.showerror(title="JSONDecodeError raised",
                                message=f"An error occured:\n{e}")
        except FileNotFoundError as e:
            messagebox.showerror(title="FileNotFoundError raised",
                                message=f"An error occured:\n{e}")
        finally:
            self.saved_data = self.load_data()
            self.date_saved = self.load_date_saves()
            # after each save, the json file gets read and its new values
            # gets re-assigned to self.saved_data

    def load_data(self):
        ''' reads "saved_avatar_configuration.json" and returns the data as a list.
            returns an empty list and creates the file if it is missing. '''
        data_path = directory_path / "saved_avatar_configuration.json"
        try:
            if Path(data_path).is_file() is True:
                with open(data_path, "r", encoding="utf-8") as file:
                    returned_data = json.load(file)
                return returned_data
            else:
                with open(data_path, "w", encoding="utf-8") as file:
                    json.dump([], file, indent=4)
                    return []
        except json.JSONDecodeError as e:
            messagebox.showerror(title="JSONDecodeError raised",
                                 message=f"An error occured:\n{e}")
            return []
        except FileNotFoundError as e:
            messagebox.showerror(title="FileNotFoundError raised",
                                 message=f"An error occured:\n{e}")

    def load_date_saves(self):
        ''' reads "dates.json" and returns the data as a list.
            returns an empty list and creates the file if it is missing. '''
        data_path = directory_path / "dates.json"
        try:
            if Path(data_path).is_file() is True:
                with open(data_path, "r", encoding="utf-8") as file:
                    returned_data = json.load(file)
                return returned_data
            else:
                with open(data_path, "w", encoding="utf-8") as file:
                    json.dump([], file, indent=4)
                    return []
        except json.JSONDecodeError as e:
            messagebox.showerror(title="JSONDecodeError raised",
                                 message=f"An error occured:\n{e}")
            return []
        except FileNotFoundError as e:
            messagebox.showerror(title="FileNotFoundError raised",
                                 message=f"An error occured:\n{e}")

    def check_database (self):
        ''' checks if database files 'dates.json' and 'saved_avatar_configuration.json'
            are parallel to each other '''
        dates = self.date_saved.copy()
        database = self.saved_data.copy()
        if len(dates) != len(database):
            raise DatabaseError("'dates.json' and 'saved_avatar_configuration.json' are not parallel.")

class DatabaseError(Exception):
    ''' Exception raised for custom error: when 'dates.json' and
        'saved_avatar_configuration.json' are not parallel to each other. '''
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return self.message
