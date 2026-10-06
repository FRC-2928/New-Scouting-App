import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import Toplevel

import customtkinter as ctk

import data_management

style = {
    "background_color": "#F9ECE5",
    "accent_background_color": "#9C220B",
    "textcolor": "#36362E"
}

# create the different pages 
def build_matches_page(parent_frame):
    page=Frame(parent_frame, bg=style.get("background_color"))
    Label(page, text="Matches View",font=("Helvetica", 12, "bold"), fg=style["textcolor"], bg=style["background_color"]).pack(pady=30)
    return page

def build_general_settings_page(parent_frame):
    page=Frame(parent_frame, bg=style.get("background_color"))
    
    Label(page, text="General Settings",font=("Helvetica", 12, "bold"), fg=style["textcolor"], bg=style["background_color"]).pack(pady=30)

    return page

def build_help_page(parent_frame):
    page=Frame(parent_frame, bg=style.get("background_color"))
    
    Label(page, text="Help",font=("Helvetica", 12, "bold"), fg=style["textcolor"], bg=style["background_color"]).pack(pady=30)

    return page



def build_team_page(parent_frame):

    page = Frame(parent_frame)
    load_data_cards(page)
    
    return page

def open_specific_team_page(team_id, team_data, root):
    # FIX: Open as an independent pop-up modal window
    detail_window = Toplevel(root)
    detail_window.title(f"Team {team_id} Details")
    detail_window.geometry("400x500") # Set an initial crisp window size
    detail_window.configure(bg=style.get("background_color"))

    header = Label(detail_window, text=f"TEAM {team_id} ANALYTICS", font=("Helvetica", 16, "bold"), bg=style["background_color"], fg=style["textcolor"], pady=10)
    header.pack(fill="x", pady=(0, 15))

    metrics = [
        ("Avg Auto Scoring:", team_data["avg_auto"]),
        ("Avg Defense Rating:", team_data["avg_defense"]),
        ("Avg Overall Scoring:", team_data["avg_scoring"])
    ]

    for label_text, val in metrics:
        # Internal frames can use whatever layout you prefer safely
        row = Frame(detail_window, bg="#ffffff")
        row.pack(fill="x", padx=20, pady=5)
        
        lbl = Label(row, text=label_text, font=("Helvetica", 11, "bold"), bg=style["background_color"], fg=style["textcolor"])
        lbl.pack(side="left")
        
        lbl_val = Label(row, text=str(val), font=("Helvetica", 11), bg=style["background_color"], fg=style["textcolor"])
        lbl_val.pack(side="right")


def load_data_cards(page):

    canvas = Canvas(page, bg=style["background_color"], highlightthickness=0)
    scrollbar = Scrollbar(page, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=style["background_color"])

    # 1. Keeps scrollbar accuracy intact when items inside change size
    scrollable_frame.bind(
        "<Configure>", 
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # 2. Store the window item reference ID
    canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 3. FIX: Safe resize function to prevent the "shrinking feedback loop"
    def configure_canvas_width(event):
        # Only stretch the inner frame if the canvas has actually rendered a real width
        if event.width > 1:
            canvas.itemconfig(canvas_frame_id, width=event.width)

    # Bind the safe configuration updater
    canvas.bind("<Configure>", configure_canvas_width)
    
    # 4. Pack layouts cleanly
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #load the data
    dataset = data_management.import_json_data("current.json")

    team_dashboard_data = data_management.parse_and_average_json() 

    for team_id, data in team_dashboard_data.items():
        card = ctk.CTkFrame(
            scrollable_frame, 
            corner_radius=12,     
            fg_color=style["background_color"],     
            border_color=style["accent_background_color"],  
            border_width=2
        )
        card.pack(side="top", fill="x", padx=15, pady=10, expand=True)
        
        # 2. Card Title (The Team Name placed at the top-left)
        title_lbl = ctk.CTkLabel(
            card, 
            text=f"Team  {team_id}", 
            font=("Helvetica", 13, "bold"),
            text_color=style["textcolor"]
        )
        # Pack it to anchor northwest (top-left) with explicit internal spacing
        title_lbl.pack(side="top", anchor="nw", padx=15, pady=(10, 5))
        
        # Internal layout frame to separate statistics from the button
        content_row = ctk.CTkFrame(card, fg_color="transparent")
        content_row.pack(side="top", fill="x", padx=15, pady=(0, 10))
        
        # 3. Add Inline Statistical Metrics Info Labels
        stats_summary = (
            f"Avg Scoring: {data['avg_scoring']}  |  "
            f"Avg Defense: {data['avg_defense']}  |  "
            f"Avg Auto: {data['avg_auto']}"
        )
        info_lbl = ctk.CTkLabel(
            content_row, 
            text=stats_summary, 
            font=("Helvetica", 11), 
            text_color=style["textcolor"]
        )
        info_lbl.pack(side="left", anchor="w")
        
        # 4. Click Event Interface Component (Rounded Button Element)
        view_btn = ctk.CTkLabel(
            content_row, 
            text="View Details →", 
            font=("Helvetica", 10, "bold"),
            fg_color=style["accent_background_color"], 
            text_color=style["background_color"],
            corner_radius=6,
            padx=12,                   
            pady=5                    
        )
        view_btn.pack(side="right", anchor="e")
        
        # Secure the lambda event handler context
        view_btn.bind(
            "<Button-1>", 
            lambda event, t_id=team_id, t_data=data, current_page=page: 
                open_specific_team_page(t_id, t_data, current_page)
        )


