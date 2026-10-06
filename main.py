import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


import os

import data_management
import pages
import json


# Creates the root for the window
root = Tk()
root.title("Scouting App")
root.geometry("620x480")
root.minsize(320, 240)
root.configure(bg="#FFFFFF") #fixes auto styling on macos

#Styling 
style = {
    "background_color": "#F9ECE5",
    "accent_background_color": "#9C220B",
    "textcolor": "#36362E"
}

def run_loading_screen(main_root, display_duration_ms=2500):
    main_root.withdraw() #hides the main window

    splash = Toplevel(main_root)
    splash.overrideredirect(True)

    width, height = 620, 340
    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    center_x = int((screen_w / 2) - (width / 2))
    center_y = int((screen_h / 2) - (height / 2))
    splash.geometry(f"{width}x{height}+{center_x}+{center_y}")
    splash.configure(bg=style["accent_background_color"])

    #add text
    Label(splash, text="Team 2928 Viking Robotics", font=("Helvetica", 14, "bold"),
          fg=style["background_color"], bg=style["accent_background_color"])
    Label(splash, text="Team 2928 Viking Robotics", font=("Helvetica", 18, "bold"),
          fg=style["background_color"], bg=style["accent_background_color"]).pack(pady=5)
    Label(splash, text="Scouting Software", font=("Helvetica", 10, "italic"),
          fg=style["background_color"], bg=style["accent_background_color"]).pack(pady=(15, 0))
    
    #add the box for the loading bar
    track_w, track_h = 300, 12
    bar_canvas = Canvas(splash, width=track_w, height=track_h, bg="#FFFFFF", highlightthickness=1, highlightbackground="#BDC3C7")
    bar_canvas.pack(pady=20)

    #create the progress bar
    progress_bar = bar_canvas.create_rectangle(0, 0, 0, track_h, fill=style["accent_background_color"], width=0)
    
    def animate_progress(current_width=0):
        if current_width <=track_w:
            bar_canvas.coords(progress_bar, 0, 0, current_width, track_h)
            splash.after(15, lambda: animate_progress(current_width + 3))

        else:
            splash.destroy()
            main_root.deiconify()
    
    animate_progress()


class FlatDropDown:
    def __init__(self, parent, root_window, title, options, bgcolor=style.get("background_color"), hover_color="#EAEAEA") -> None:
        self.options = options
        self.bg_color = bgcolor
        self.hover_color = hover_color
        self.is_open = False
        self.selected_value = None


        self.container = Frame(parent, bg=parent["bg"])

        self.button = Label(
            self.container,
            text=f"{title}",
            font=("Helvetica", 15, "bold"),
            bg=self.bg_color,
            fg="white",
            padx=15,
            pady=15,
            
        )

        self.button.pack(side="top", anchor="w")
        self.button.bind("<Button-1>", self.toggle)

        self.options_frame = Frame(root_window, bg="#FFFFFF", bd=1, relief="solid")

        self.item_labels = []
        
        #adds each item row
        for item in self.options:
            item_label = Label(
                self.options_frame,
                text=item,
                font=("Helvetica", 10),
                bg=style.get("background_color"),
                fg=style.get("textcolor"),
                anchor="w",
                padx=15,
                pady=6,
                width=18,
            )
            self.item_labels.append(item_label)

            #hover states
            item_label.bind("<Enter>", lambda e, lbl=item_label, dropdown=self: lbl.config(bg=dropdown.hover_color))
            item_label.bind("<Leave>", lambda e, lbl=item_label: lbl.config(bg="#FFFFFF"))

            #selection event execution
            item_label.bind("<Button-1>", lambda e, choice=item, dropdown=self: dropdown.select(choice))

    def toggle(self, event):
        if self.is_open:
            self.options_frame.place_forget()
            for lbl in self.item_labels:
                lbl.pack_forget()
            self.is_open = False

        else:
            for lbl in self.item_labels:
                lbl.pack(side="top", fill="x")

            current_x = self.container.winfo_x()

            self.options_frame.place(x=current_x, y=55)
            self.options_frame.lift()
            self.options_frame.update_idletasks()
            self.is_open = True


    def select(self, choice):
        self.selected_value = choice
        self.options_frame.place_forget()

        for lbl in self.item_labels:
            lbl.pack_forget()
        self.is_open = False

        clean_choice = choice.strip()

        callbacks_dict = getattr(self, "callbacks", getattr(self, "callback", {}))
        
        if callbacks_dict and clean_choice in callbacks_dict:
            callbacks_dict[clean_choice]()

    def get(self):
        return self.selected_value
            



#Creates the top bar 
top_bar = Frame (root,height=50,bg=style.get("accent_background_color"),bd=1,relief="flat")
top_bar.pack(side="top", fill="x")
top_bar.pack_propagate(False)


title_label = FlatDropDown(top_bar, root, "2928 Scouting Dashboard", ["New", "Open File", "Save", "Save As..."], bgcolor=style.get("accent_background_color"))

view_label = FlatDropDown(top_bar, root, "View", ["Team", "Match", "Leaderboard"], bgcolor=style.get("accent_background_color"))

collect_label = FlatDropDown(top_bar, root, "Data", ["Collect", "Edit"], bgcolor=style.get("accent_background_color"))

settings_label = FlatDropDown(top_bar, root, "Settings", ["General", "Help"], bgcolor=style.get("accent_background_color"))


#pack the labels for the top bar
title_label.container.pack(side="left", padx=10, anchor="n")
view_label.container.pack(side="left", padx=10, anchor="n")
collect_label.container.pack(side="left", padx=10, anchor="n")
settings_label.container.pack(side="left", padx=10, anchor="n")

body = Frame(root,bg=style.get("background_color"),relief="groove")
body.pack(fill="both", expand="true")
body.pack_propagate(False)

settings_general_page = pages.build_general_settings_page(body)
team_page = pages.build_team_page(body)
matches_page = pages.build_matches_page(body)
help_page = pages.build_help_page(body)

for page in (settings_general_page, team_page, matches_page, help_page):
    page.grid(row=0, column=0, sticky="nsew")

body.rowconfigure(0, weight=1)
body.columnconfigure(0, weight=1)

def open_file_explorer():
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    target_folder = os.path.join(script_dir, "data")

    file_path = filedialog.askopenfilename(
        initialdir=target_folder,
        title="Select A File To Open",
        filetypes=[("Text Files", "*.json"), ("All Files", "*.*")]
    )

    if file_path:
        print(f"user selected {file_path}")

        with open(file_path, 'r') as file:
            print(file.read())

def create_new_file():
    if not data_management.import_default_json:
        data_management.clear_current()
        

def save_new_file():
    file_path = filedialog.asksaveasfilename(
        title="Create New Scouting File",
        defaultextension=".json", # Automatically adds .txt if the user forgets
        filetypes=[("Text Files", "*.json")]
    )

    if file_path:
        print(f"Creating new file at: {file_path}")
        
        # Open in 'w' (write) mode to physically create an empty file
        with open(file_path, 'w') as file:
            file.write("") # Starts it off empty, ready for scouting data

def save_file():
    data_management.savefile()


def show_gen_settings():
    settings_general_page.tkraise()

def show_team():
    team_page.tkraise()

def show_matches():
    matches_page.tkraise()

def show_help():
    help_page.tkraise()

show_team()
view_label.callbacks = {
    "Team": show_team,
    "Match": show_matches
}

settings_label.callbacks = {
    "General": show_gen_settings,
    "Help": show_help
}

title_label.callback = {
    "Open File": open_file_explorer,
    "New": create_new_file,
    "Save As...": save_new_file,
    "Save": save_file
}

run_loading_screen(root)


root.mainloop()