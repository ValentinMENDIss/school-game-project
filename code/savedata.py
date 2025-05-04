#    School-Game-Project - Adventure style school game
#    Copyright (C) 2025 Valentin Virstiuc <valentin.vir@proton.me>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import os

# Default player data
DEFAULT_PLAYER_DATA = {
    'health': 100,
    'stamina': 50,
    'damage': 10,
    'defence': 5,
    'cutsceneOrder': 0
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
        save_player_data(DEFAULT_PLAYER_DATA)
        return DEFAULT_PLAYER_DATA

def default_data():
    save_player_data(DEFAULT_PLAYER_DATA)

# Function to save player data to the JSON file
def save_player_data(player_data):
    # Save the current player data to the JSON file
    with open(SAVE_FILE, 'w') as file:
        json.dump(player_data, file, indent=4)

def save_data(game):
    with open(SAVE_FILE, 'w') as file:
        DEFAULT_PLAYER_DATA['cutsceneOrder'] = game.cutscene_order
        json.dump(DEFAULT_PLAYER_DATA, file, indent=5)

def change_player_data(health=None, stamina=None, damage=None, defence=None):
    if health:
        DEFAULT_PLAYER_DATA['health'] = health
    if stamina:
        DEFAULT_PLAYER_DATA['stamina'] = stamina
    if damage:
        DEFAULT_PLAYER_DATA['damage'] = damage
    if defence:
        DEFAULT_PLAYER_DATA['defence'] = defence
    save_player_data(DEFAULT_PLAYER_DATA)

# Function to change an attribute
def change_attribute(attribute, value, player_data):
    if attribute in player_data:
        player_data[attribute] = value
        save_player_data(player_data)  # Persist changes to the file
    else:
        print(f"Invalid attribute: {attribute}")
