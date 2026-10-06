import json
from collections import defaultdict

current_file_open = "none"

def import_default_json():
    with open("default.json", "r") as file:
        default = json.load(file)
        return default
    
def import_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return data
    
def clear_current():
    with open("current.json", "w") as file:
        json.dump(import_default_json, file)

#def write_to_current():

#def save_file_as():

def save_file():
    if not current_file_open == "none":
        with open(current_file_open, "w") as file:
            json.dump(import_json_data("current.json"), file)

def parse_and_average_json():
    """
    Parses your specific nested list JSON format.
    Aggregates stats across all occurrences to calculate global averages per team.
    """
    try:
        with open('current.json', 'r') as file:
            raw_data = json.load(file)
    except FileNotFoundError:
        # Stand-in example layout matching your precise format definition
        raw_data = [
            [254, 
             {"team1ID": 254, "team1_alliance": "blue", "team1_scoring_In_Auto": 4, "team1_quality_of_auto":5, "team1_quality_of_scoring": 5, "team1_overall_scoring": 12, "team1_quality_of_defense": 2},
             {"team2ID": 1323, "team2_alliance": "blue", "team2_scoring_In_Auto": 3, "team2_quality_of_auto":4, "team2_quality_of_scoring": 4, "team2_overall_scoring": 10, "team2_quality_of_defense": 4},
             {"team3ID": 1678, "team3_alliance": "blue", "team3_scoring_In_Auto": 5, "team3_quality_of_auto":5, "team3_quality_of_scoring": 4, "team3_overall_scoring": 11, "team3_quality_of_defense": 1},
             {"team4ID": 118, "team4_alliance": "red", "team4_scoring_In_Auto": 2, "team4_quality_of_auto":3, "team4_quality_of_scoring": 3, "team4_overall_scoring": 8, "team4_quality_of_defense": 5},
             {"team5ID": 148, "team5_alliance": "red", "team5_scoring_In_Auto": 3, "team5_quality_of_auto":4, "team5_quality_of_scoring": 5, "team5_overall_scoring": 9, "team5_quality_of_defense": 3},
             {"team6ID": 254, "team6_alliance": "red", "team6_scoring_In_Auto": 6, "team6_quality_of_auto":5, "team6_quality_of_scoring": 5, "team6_overall_scoring": 14, "team6_quality_of_defense": 3},
             "qualification" 
            ]
        ]

    # --- ADD THIS LOGIC TO FIX THE KEYERROR ---
    # Temporary storage to tally totals and matches played
    team_totals = defaultdict(lambda: {"auto": 0, "defense": 0, "scoring": 0, "count": 0})

    for match in raw_data:
        # Loop indices 1 through 6 map to team1 through team6 dictionaries
        for i in range(1, 7):
            team_dict = match[i]
            
            # Extract data using dynamic keys matching your JSON format
            t_id = team_dict[f"team{i}ID"]
            auto_score = team_dict[f"team{i}_scoring_In_Auto"]
            defense_rating = team_dict[f"team{i}_quality_of_defense"]
            overall_scoring = team_dict[f"team{i}_overall_scoring"]
            
            # Accumulate values
            team_totals[t_id]["auto"] += auto_score
            team_totals[t_id]["defense"] += defense_rating
            team_totals[t_id]["scoring"] += overall_scoring
            team_totals[t_id]["count"] += 1

    # Convert overall totals into final averages
    processed_teams = {}
    for t_id, stats in team_totals.items():
        count = stats["count"]
        processed_teams[t_id] = {
            "avg_auto": round(stats["auto"] / count, 2),
            "avg_defense": round(stats["defense"] / count, 2),
            "avg_scoring": round(stats["scoring"] / count, 2)
        }
        
    return processed_teams
