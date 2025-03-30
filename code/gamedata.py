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


######### IMPORT ##############

from settings import *

######### DATA ##############

## ENTITY DATA ##
NPC_INTERACT_DATA = ["Oh... also try to get near these Items and to press E. See what happens :3",
                     "OMG, I CAN SPEAK!!! Thank you developers :3",
                     "Hello, how are you?",
                     ":3",
                     "I am so glad that developers made me able to speak. That's so cool :).",
                     "What are those items? Perhaps you can do something with them?",
                     "What is your favourite game?",
                     "It's so nice to see you",
                     "Try to explore the world",
                     "YIPPEE!",
                     "My life is so exciting, I get to see everyday people like you and that's cool!\nWhat about you?",
                     "Try to find items near this area!",
                     "I've heard that you can find items in this area. Maybe it's just a legend...",
                     "This school looks awesome :)"]

NPC_DIALOG_1 = ["Hello...", 
                "I love watermelons",
                "So, I am capybara :3",
                "...",
                "Okay, bye :)"]

NPC_ENEMY_INTERACT_DATA = ["Is it all you can do?",
                           "Well done...",
                           "Write your exam faster",
                           "I see that Peace was never an option...",
                           "That was quite exciting, but have you seen my power?",
                           "Good move :)",
                           "Look what I've got!",
                           "Continue Fighting!",
                           "You will not be able to do this. Surrender!",
                           "I like silly things, oh I've forgot, we are fighting, anyways...",
                           "Do you really think that you can beat me?",
                           "No one has ever defeated me, so good luck!",
                           "Are you scared?",
                           "Maybe you want to stop?",
                           "Look, behind you!",
                           "Uh, it hurts!",
                           "Peace?",
                           "Violence?",
                           "...",
                           "... And now see my power!"]

NPC_ENEMY_DEFEATED_INTERACT_DATA = ["You have already defeated me...",
                                    "You can't fight with me anymore, sadly...",
                                    "I don't want to fight with you anymore",
                                    "Why are you still here?",
                                    "Do you really want me to show you my full potential?",
                                    "I am not in the mood to fight anymore..."]

NPC_ENEMY_WON_INTERACT_DATA = ["Do you really want me to fight with you second time?",
                               "Stop asking me to fight with you again.\nI've already defeated you. That's enough for me",
                               "Have you forgotten? I defeated you"]

## ITEM DATA ##
ITEM_RARITY_DATA_RARE = {"health_mul": 1.2,
                         "stamina_mul": 1.2,
                         "damage_mul": 1.2,
                         "defence_mul": 1.2}

ITEM_RARITY_DATA_EPIC = {"health_mul": 1.3,
                         "stamina_mul": 1.3,
                         "damage_mul": 1.3,
                         "defence_mul": 1.3}

ITEM_RARITY_DATA_MYTHIC = {"health_mul": 1.4,
                           "stamina_mul": 1.4,
                           "damage_mul": 1.4,
                           "defence_mul": 1.4}

ITEM_RARITY_DATA_LEGENDARY = {"health_mul": 1.5,
                              "stamina_mul": 1.5,
                              "damage_mul": 1.5,
                              "defence_mul": 1.5}

## SIDE QUESTS ##
SIDE_QUESTS = {                                                                 # perhaps NPCs should have own name, which will work as an ID to discover which NPC is which, and which side-quests can be triggered for them
    "player-mother": {
        "get-item": {
            "info-text": "Get a random item and you will get a reward.",
            "reward": 0.99,
        },
        "interact_npc": {
            "info-text": "Try to interact with someone and you will get a reward.",
            "reward": 1.25,
        }
    } 
}