import tkinter
from tkinter import *
from tkinter import ttk

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


def load_data_cards(page):
    canvas = Canvas(page, bg=style["background_color"], highlightthickness=0)
    scrollbar = Scrollbar(page, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg=style["background_color"])

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    #pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    #load the data
    dataset = data_management.import_json_data("current.json")

    team_dashboard_data = data_management.parse_and_average_json()

    for team_id, data in team_dashboard_data.items():
        # 1. Base Structure Frame for the Card
        card = LabelFrame(
            scrollable_frame, 
            text=f" Team  {team_id}", 
            font=("Helvetica", 12, "bold"),
            bg="#ffffff", 
            fg="#1a237e",
            bd=2, 
            relief="solid"
        )
        card.pack(fill="x", padx=15, pady=10, ipady=8)
        
        # 2. Add Inline Statistical Metrics Info Labels
        stats_summary = (
            f"Avg Scoring: {data['avg_scoring'], 0}  |  "
            f"Avg Defense: {data['avg_defense'], 0}  |  "
            f"Avg Auto: {data['avg_auto'], 0}"
        )
        info_lbl = Label(
            card, 
            text=stats_summary, 
            font=("Helvetica", 10), 
            bg="#ffffff", 
            fg="#444444"
        )
        info_lbl.pack(side="left", anchor="w", padx=15, pady=5)
        
        # 3. Click Event Interface Component (Button)
        # CRITICAL: team_id=team_id binds the loop context state directly to the callback instance
        view_btn = Button(
            card, 
            text="View Details →", 
            font=("Helvetica", 9, "bold"),
            bg="#1a237e", 
            fg="#ffffff",
            activebackground="#303f9f",
            activeforeground="#ffffff",
            relief="flat",
            command=lambda t_id=team_id, t_data=data: open_specific_team_page(t_id, t_data, page)
        )
        view_btn.pack(side="right", anchor="e", padx=15, pady=5)


def open_specific_team_page(team_id, team_data, root):
    detail_window = Frame(root, bg=style.get("background_color"))

    header = Label(detail_window, text=f"TEAM {team_id} ANALYTICS", font=("Helvetica", 16, "bold"), bg=style["background_color"], fg=style["textcolor"], pady=10)
    header.pack(fill="x", pady=(0, 15))

    metrics = [
        ("Avg Auto Scoring:", team_data["avg_auto"]),
        ("Avg Defense Rating:", team_data["avg_defense"]),
        ("Avg Overall Scoring:", team_data["avg_scoring"])
    ]

    for label_text, val in metrics:
        row = Frame(detail_window, bg="#ffffff")
        row.pack(fill="x", padx=20, pady=5)
        
        lbl = Label(row, text=label_text, font=("Helvetica", 11, "bold"), bg=style["background_color"], fg=style["textcolor"])
        lbl.pack(side="left")
        
        lbl_val = Label(row, text=str(val), font=("Helvetica", 11), bg=style["background_color"], fg=style["textcolor"])
        lbl_val.pack(side="right")
