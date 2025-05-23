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


from settings import *
from datetime import datetime, timedelta

class GameTime:
    def __init__(self, time_scale=180):
        # time_scale determines how many real seconds equal one game hour
        # default: 60 seconds real time = 1 hour game time
        self.time_scale = time_scale
        self.running = True
        # Start at 6:00 AM on 1. September by default (first day of school)
        self.game_time = datetime(2025, 9, 1, 6, 0) # year, month, day, seconds, milliseconds
        self.last_update = pygame.time.get_ticks()
        
        #test
        self.paused_time = 0
        #####
        
        # Time events storage
        self.time_events = {
            "morning": {"time": "06:00", "triggered": False},
            "noon": {"time": "12:00", "triggered": False},
            "evening": {"time": "18:00", "triggered": False},
            "night": {"time": "22:00", "triggered": False}
        }
    
    def update(self):
        current_time = pygame.time.get_ticks() - self.paused_time                                                       # get current ticks and subtract time when game was paused (e.g: during player is in Menu)
        elapsed = (current_time - self.last_update)                                                                     # calculate how much time has passed since the last update
        
        # Convert milliseconds to hours in game time
        game_hours = (elapsed / 1000) * (1 / self.time_scale)                                                           # count/get in-game hours
        
        if game_hours > 0:
            self.game_time += timedelta(hours=game_hours)
            self.last_update = current_time
            
            # Reset to next day if we pass midnight
            if self.game_time.hour >= 24:
                self.game_time = datetime(
                    self.game_time.year,
                    self.game_time.month,
                    self.game_time.day + 1,
                    0, 0
                )
            
            # Check time events
            self._check_time_events()

    def pause_game_time(self, dt):
        self.running = False
        self.paused_time += dt * 1000

    def _check_time_events(self):
        current_time_str = self.get_time_str()
        
        for event_name, event_data in self.time_events.items():
            if current_time_str == event_data["time"] and not event_data["triggered"]:
                self._trigger_time_event(event_name)
                event_data["triggered"] = True
            # Reset trigger if time has passed
            elif current_time_str != event_data["time"]:
                event_data["triggered"] = False
    
    def _trigger_time_event(self, event_name):
        """Handle different time-of-day events"""
        events = {
            "morning": self._morning_event,
            "noon": self._noon_event,
            "evening": self._evening_event,
            "night": self._night_event
        }
        if event_name in events:
            events[event_name]()
    
    def _morning_event(self):
        # Implement morning specific logic
        pass
    
    def _noon_event(self):
        # Implement noon specific logic
        pass
    
    def _evening_event(self):
        # Implement evening specific logic
        pass
    
    def _night_event(self):
        # Implement night specific logic
        pass
    
    def get_time_str(self):
        """Returns time as string in 24-hour format (HH:MM)"""
        return self.game_time.strftime("%H:%M")
    
    def get_time_12hr(self):
        """Returns time as string in 12-hour format with AM/PM"""
        return self.game_time.strftime("%I:%M %p")
    
    def get_day_phase(self):
        """Returns the current phase of the day"""
        hour = self.game_time.hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"
