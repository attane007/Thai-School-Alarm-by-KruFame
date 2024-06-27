import sqlite3
from PySide6 import QtCore

class SoundScheduler(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_schedule)
        self.timer.start(1000)  # Check every second
        
        # self.load_schedule_from_database()
        self.last_played_minute = None

    def load_schedule_from_database(self):
        # Connect to SQLite database
        database_filename = 'your_database.db'  # Replace with your database filename
        conn = sqlite3.connect(database_filename)
        cursor = conn.cursor()
        
        # Fetch schedule data from database
        cursor.execute('SELECT hour, minute, sound_path FROM schedule')
        self.schedule_list = cursor.fetchall()
        
        conn.close()

    def start(self):
        self.timer.start(1000)  # Start the timer when the scheduler starts

    def stop(self):
        self.timer.stop()  # Stop the timer when the scheduler stops

    def check_schedule(self):
        current_time_local = QtCore.QDateTime.currentDateTime()  # Fetch current local time
        
        # Extract hour, minute, and second components from current local time
        current_hour_local = current_time_local.time().hour()
        current_minute_local = current_time_local.time().minute()
        current_second_local = current_time_local.time().second()
        
        print(f"Local Time: {current_hour_local}:{current_minute_local}:{current_second_local}")

        # if current_minute_local != self.last_played_minute:
        #     # Check if current time matches any scheduled time
        #     for hour, minute, sound_path in self.schedule_list:
        #         if current_time_local.time().hour() == hour and current_time_local.time().minute() == minute:
        #             # Play sound function (replace with your sound playing logic)
        #             self.play_sound(sound_path)
        #             self.last_played_minute = current_minute_local
        #             break

    def play_sound(self, sound_path):
        print(f"Playing sound: {sound_path}")
        # Implement your sound playing logic here