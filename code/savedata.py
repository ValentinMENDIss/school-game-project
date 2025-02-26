import json
import os

# Default player data
DEFAULT_PLAYER_DATA = {
    'health': 100,
    'stamina': 50,
    'damage': 10,
    'defence': 5
}

# Path to the save file
SAVE_FILE = 'savedata.json'

# Function to load saved data from JSON file (if it exists)
def load_saved_data():
    # Check if the saved data file exists
    if os.path.exists(SAVE_FILE):
        try:
            # Load the saved data from the file
            with open(SAVE_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error loading saved data. Using default values.")
            return DEFAULT_PLAYER_DATA
    else:
        print("No saved data found. Using default values.")
        save_data(DEFAULT_PLAYER_DATA)
        return DEFAULT_PLAYER_DATA

# Function to save player data to the JSON file
def save_data(player_data):
    # Save the current player data to the JSON file
    with open(SAVE_FILE, 'w') as file:
        json.dump(player_data, file, indent=4)

# Function to change an attribute
def change_attribute(attribute, value, player_data):
    if attribute in player_data:
        player_data[attribute] = value
        save_data(player_data)  # Persist changes to the file
    else:
        print(f"Invalid attribute: {attribute}")
