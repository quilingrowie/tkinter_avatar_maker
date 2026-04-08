'''
project name: tkinter avatar creator

description: allows users to create customizable avatar portrait by selecting
different visual elements such as hair, eyes, mouth, etc.

course: IT101-2L - Final Project
author: Rowie Belle J. Quiling
submission date: March 26 2026
'''
import tkinter as tk
from tkinter import messagebox
from tk_avatar_app import AvatarApp, DatabaseError

WINDOW_WIDTH = 413
WINDOW_HEIGHT = 736

def center_window(window):
    '''centralizes the window upon running'''
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight() # takes desktop's screen size

    x_axis = (screen_width - WINDOW_WIDTH) // 2 # gets x-axis position
    y_axis = (screen_height - WINDOW_HEIGHT) // 2 # gets y-axis position

    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_axis}+{y_axis}") # sets size and position
    window.resizable(False, False) # resize on window not allowed

def main_window():
    '''creates and configures the main tkinter window'''
    root = tk.Tk()
    center_window(root) # window size=413x736
    root.title("Tkinter Final Project | Avatar Portrait Creator")
    AvatarApp(root)

    return root

if __name__ == "__main__":
    try:
        main_window().mainloop()
    except AttributeError as e:
        messagebox.showerror(title="AttributeError raised",
                            message=f"An error occured:\n{e}")
    except TypeError as e:
        messagebox.showerror(title="TypeError raised",
                            message=f"An error occured:\n{e}")
    except NameError as e:
        messagebox.showerror(title="NameError raised",
                             message=f"An error occured:\n{e}")
    except DatabaseError as e:
        messagebox.showerror(title="DatabaseError",
                             message=f"{e}\nPlease delete both and restart the program.")
