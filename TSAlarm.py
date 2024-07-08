import sys
import sqlite3
import os
import platform
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from tell_time import tell_hour,tell_minute

database_filename = 'data.db'

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.connect_db()
        self.path_thai=[]
        self.path_eng=[]
        for i in range(1,25):
            if self.data[(i-1)]['sound'] is None or self.data[(i-1)]['sound'] == "":   
                self.path_thai.append("")
            else:
                self.path_thai.append(self.data[(i-1)]['sound'])
            
            if self.data[(i-1)]['sound_eng'] is None or self.data[(i-1)]['sound_eng'] == "":
                self.path_eng.append("")
            else:
                self.path_eng.append(self.data[(i-1)]['sound_eng'])

        self.setStyleSheet("background-color: white;")
        self.initialize_schedule()
        

        # Widgets
        self.button = QtWidgets.QPushButton(" บันทึก!")
        self.button.setIcon(QIcon("resource/save-save-file-svgrepo-com.svg"))
        self.button.setFixedHeight(40)
        self.button.setFixedWidth(100)
        self.button.setStyleSheet("background-color: #87cefa; color: black;")

        self.button_clear = QtWidgets.QPushButton(" ล้างข้อมูล!")
        self.button_clear.setIcon(QIcon("resource/bin-svgrepo-com.svg"))
        self.button_clear.setFixedHeight(40)
        self.button_clear.setFixedWidth(100)
        self.button_clear.setStyleSheet("background-color: #ff0800; color: white;")

        self.button_announcement = QtWidgets.QPushButton(" ประกาศ!")
        self.button_announcement.setIcon(QIcon("resource/announcement-svgrepo-com.svg"))
        self.button_announcement.setFixedHeight(40)
        self.button_announcement.setFixedWidth(100)
        self.button_announcement.setStyleSheet("background-color: #fadfad; color: black;")

        self.name_label = QtWidgets.QLabel("Name:")
        # self.name_label.setFixedWidth(50)
        self.head_label3 = QtWidgets.QLabel("ชั่วโมง")
        self.head_label4 = QtWidgets.QLabel("นาที")
        self.head_label5 = QtWidgets.QLabel("เสียง")
        self.head_label6 = QtWidgets.QLabel("ทดสอบ")
        self.head_label7 = QtWidgets.QLabel("เสียงอังกฤษ")
        self.head_label8 = QtWidgets.QLabel("ล้างข้อมูล")
        self.bottom_label_licence = QtWidgets.QLabel("*ไม่อนุญาตให้ใช้ในเชิงพาณิชย์")
        self.bottom_label_licence.setStyleSheet("color: #6495ed; font-size: 16px;")
        self.bottom_label_warning = QtWidgets.QLabel("**กดปุ่มบันทึกทุกครั้งที่มีการแก้ไขข้อมูล")
        self.bottom_label_warning.setStyleSheet("color: red; font-size: 16px;")
        self.head_checkbox = QtWidgets.QCheckBox("ทั้งหมด")
        self.head_checkbox_time = QtWidgets.QCheckBox("บอกเวลา")

        # Center-align the labels
        self.head_label3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.head_label4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.head_label5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.head_label6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.head_label7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.head_label8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
      

        # Layouts
        self.layout = QtWidgets.QVBoxLayout(self)

        # Grid layout for Name and Language
        self.form_grid_layout = QtWidgets.QGridLayout()
        self.checkboxes = []
        for i in range(1, 25):
            checkbox = QtWidgets.QCheckBox(str(i))
            if self.data[(i-1)]['status']==1:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
            checkbox.setFixedWidth(50)
            self.checkboxes.append(checkbox)
            self.form_grid_layout.addWidget(checkbox,i,0)

        self.checkboxes2 = []
        for i in range(1, 25):
            checkbox = QtWidgets.QCheckBox()
            if self.data[(i-1)]['tell_time']==1:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
            checkbox.setFixedWidth(50)
            self.checkboxes2.append(checkbox)
            self.form_grid_layout.addWidget(checkbox,i,1)

        self.combobox=[]
        self.hours = [str(i).zfill(2) for i in range(24)]
        self.minutes = [str(i).zfill(2) for i in range(60)]
        for i in range(1, 25):
            combo=QtWidgets.QComboBox()
            combo.setMinimumContentsLength(3)
            combo.setFixedWidth(50)
            combo.addItems(self.hours)
            hour_value = self.data[(i-1)]['hour']
            if hour_value is None or hour_value == '':
                combo.setCurrentIndex(-1)
            else:
                combo.setCurrentIndex(int(hour_value))
            self.combobox.append(combo)
            self.form_grid_layout.addWidget(combo,i,2)
        

        self.combobox_minutes=[]
        for i in range(1,25):
            combo=QtWidgets.QComboBox()
            combo.setMinimumContentsLength(3)
            combo.setFixedWidth(50)
            combo.addItems(self.minutes)
            minute_value = self.data[(i-1)]['minute']
            if minute_value is None or minute_value == '':
                combo.setCurrentIndex(-1)
            else:
                combo.setCurrentIndex(int(minute_value))
            self.combobox_minutes.append(combo)
            self.form_grid_layout.addWidget(combo,i,3)

        # Create a text box
        self.textbox_thai=[]
        for i in range(1,25):
            text_box = QtWidgets.QLineEdit()
            text_box.setReadOnly(True)
            text_box.setStyleSheet("background-color: lightgrey;")
            text_box.setText(os.path.basename(self.path_thai[(i-1)]))
            self.textbox_thai.append(text_box)
            self.form_grid_layout.addWidget(text_box,i,4)
        
        self.textbox_eng=[]
        for i in range(1,25):
            text_box = QtWidgets.QLineEdit()
            text_box.setReadOnly(True)
            text_box.setStyleSheet("background-color: lightgrey;")
            text_box.setText(os.path.basename(self.path_eng[(i-1)]))
            self.textbox_eng.append(text_box)
            self.form_grid_layout.addWidget(text_box,i,6)
        
        self.file_input_thai=[]
        for i in range(1,25):
            file_button = QtWidgets.QPushButton("เลือก")
            file_button.clicked.connect(lambda checked, index=i, target="file_input_thai": self.open_file_dialog(index,target))
            self.file_input_thai.append(file_button)
            self.form_grid_layout.addWidget(file_button,i,5)

        self.file_input_eng=[]
        for i in range(1,25):
            file_button = QtWidgets.QPushButton("เลือก")
            file_button.clicked.connect(lambda checked, index=i, target="file_input_eng": self.open_file_dialog(index,target))
            self.file_input_eng.append(file_button)
            self.form_grid_layout.addWidget(file_button,i,7)

        self.test=[]
        for i in range(1,25):
            play_button = QtWidgets.QPushButton()
            play_button.setIcon(QIcon("resource/play-circle-svgrepo-com.svg"))
            play_button.setStyleSheet("background-color: orange; color: white;")
            play_button.clicked.connect(lambda checked,index=i:self.play_action(index))
            self.test.append(play_button)
            self.form_grid_layout.addWidget(play_button,i,8)

        self.clear_data=[]
        for i in range(1,25):
            play_button = QtWidgets.QPushButton()
            play_button.setIcon(QIcon("resource/bin-svgrepo-com.svg"))
            play_button.setStyleSheet("background-color: #dc143c; color: white;")
            play_button.clicked.connect(lambda checked,index=i:self.clear_target_data(index))
            self.test.append(play_button)
            self.form_grid_layout.addWidget(play_button,i,9)

        self.form_grid_layout.addWidget(self.head_checkbox, 0,0)
        self.form_grid_layout.addWidget(self.head_checkbox_time, 0,1)
        self.form_grid_layout.addWidget(self.head_label3, 0,2)
        self.form_grid_layout.addWidget(self.head_label4, 0,3)
        self.form_grid_layout.addWidget(self.head_label5, 0,4)
        self.form_grid_layout.addWidget(self.head_label7, 0,6)
        self.form_grid_layout.addWidget(self.head_label6, 0,8)
        self.form_grid_layout.addWidget(self.head_label8, 0,9)

        self.create_system_layout()
        self.create_button_layout()

        # Adding grid layout to the main layout
        self.layout.addLayout(self.form_grid_layout)
        self.layout.addLayout(self.system_layout)
        self.layout.addLayout(self.button_layout)

        # Signals
        self.button.clicked.connect(self.save_data)
        self.button_announcement.clicked.connect(self.on_announcement)
        self.button_clear.clicked.connect(self.clear_all_data)
        self.head_checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        self.head_checkbox_time.stateChanged.connect(self.on_checkbox_time_state_changed)

    def create_button_layout(self):
        # Button layout 
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.bottom_label_licence)     
        self.button_layout.addWidget(self.bottom_label_warning)
        self.button_layout.addWidget(self.button_announcement)
        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.button_clear)      
        self.button_layout.setAlignment(QtCore.Qt.AlignRight)

    def create_system_layout(self):
        conn = sqlite3.connect(database_filename)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # system layout
        self.system_layout = QtWidgets.QHBoxLayout()
        self.bottom_grid_layout = QtWidgets.QGridLayout()
        self.startup_layout = QtWidgets.QHBoxLayout()
        self.shutdown_layout = QtWidgets.QHBoxLayout()
        self.bell_layout = QtWidgets.QHBoxLayout()

        self.checkbox_auto_startup = QtWidgets.QCheckBox("เริ่มโปรแกรมอัตโนมัติเมื่อเปิดเครื่อง")
        cursor.execute('SELECT * FROM utility where name="auto_startup" limit 1')
        auto_startup = cursor.fetchone()
        if auto_startup:
            auto_startup=dict(auto_startup)
            if auto_startup['value']=='1':
                self.checkbox_auto_startup.setChecked(True)

        self.label_bell = QtWidgets.QLabel("เสียงระฆัง: ")
        self.label_bell.setFixedWidth(60)
        self.combo_bell = QtWidgets.QComboBox()
        cursor.execute('SELECT * FROM bell')
        bell = cursor.fetchall()
        if bell:
            for i in bell:
                i=dict(i)
                bell_id = i['id']
                bell_name = i['name']
                self.combo_bell.addItem(bell_name, bell_id)
                if i['status']:
                    self.combo_bell.setCurrentIndex(self.combo_bell.findData(bell_id))

        current_time=QtCore.QTime.currentTime()
        time_string = "เวลาปัจจุบัน "+current_time.toString("hh:mm:ss")
        self.system_time_label = QtWidgets.QLabel(time_string)
        self.system_time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.system_time_label.setStyleSheet("font-size: 16px;font-weight:700;")

        self.bell_layout.addWidget(self.label_bell)
        self.bell_layout.addWidget(self.combo_bell)
        self.bell_layout.setContentsMargins(0, 0, 30, 0)

        self.bottom_grid_layout.addWidget(self.checkbox_auto_startup,0,0)
        self.bottom_grid_layout.addLayout(self.bell_layout,0,3)
        self.bottom_grid_layout.addWidget(self.system_time_label,0,4)
        self.system_layout.addLayout(self.bottom_grid_layout)

        conn.commit()
        conn.close()

    def on_announcement(self):
        self.play_action("announcement")

    def on_checkbox_state_changed(self, state):
        conn = sqlite3.connect(database_filename)
        cursor = conn.cursor()
        if state == 2:
            for checkbox in self.checkboxes:
                checkbox.setChecked(True)
            cursor.execute('''
            UPDATE schedule SET status = 1 Where status = 0
            ''')
        else:
            for checkbox in self.checkboxes:
                checkbox.setChecked(False)
            conn = sqlite3.connect(database_filename)
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE schedule SET status = 0 Where status = 1
            ''')
        conn.commit()
        conn.close()

    def on_checkbox_time_state_changed(self, state):
        conn = sqlite3.connect(database_filename)
        cursor = conn.cursor()
        if state == 2:
            for checkbox in self.checkboxes2:
                checkbox.setChecked(True)
            cursor.execute('''
            UPDATE schedule SET tell_time = 1 Where tell_time = 0
            ''')
        else:
            for checkbox in self.checkboxes2:
                checkbox.setChecked(False)
            cursor.execute('''
            UPDATE schedule SET tell_time = 0 Where tell_time = 1
            ''')
        conn.commit()
        conn.close()

    def connect_db(self):
        if not os.path.exists(database_filename):
            conn = sqlite3.connect(database_filename)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hour VARCHAR(5) DEFAULT NULL,
            minute VARCHAR(5) DEFAULT NULL,
            sound TEXT DEFAULT NULL,
            sound_eng TEXT DEFAULT NULL,
            status BOOLEAN DEFAULT 0,
            tell_time BOOLEAN DEFAULT 0)
            ''')

            cursor.execute('''CREATE TABLE bell (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200),
            first TEXT,
            last TEXT,
            status BOOLEAN DEFAULT 0)
            ''')

            cursor.execute('''CREATE TABLE utility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200),
            value VARCHAR(200))
            ''')

            cursor.execute('''
            CREATE INDEX idx_name ON utility (name)
            ''')

            cursor.execute('''
                    INSERT INTO bell (name,first,last,status)
                    VALUES ('เสียงเตือนที่ 1', 'audio/bell/sound1/First.wav','audio/bell/sound1/Last.wav',0),
                           ('เสียงเตือนที่ 2', 'audio/bell/sound2/First.wav','audio/bell/sound2/Last.wav',0),
                           ('เสียงเตือนที่ 3', 'audio/bell/sound3/First.wav','audio/bell/sound3/Last.wav',1)
                ''')

            for i in range(24):
                cursor.execute('''
                    INSERT INTO schedule (hour, minute, sound, sound_eng, status, tell_time)
                    VALUES (NULL, NULL, NULL, NULL, 0, 0)
                ''')
            conn.commit()
            conn.close()
            print(f"SQLite database '{database_filename}' created.")

        conn = sqlite3.connect(database_filename)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM schedule')
        rows = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        self.data=rows

    def open_file_dialog(self,index,target):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setNameFilter("Audio files (*.wav *.mp3 *.ogg *.flac *.aac)")
        default_directory = os.path.join(os.path.dirname(__file__), "audio")
        file_dialog.setDirectory(default_directory)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if target=="file_input_thai":
                self.path_thai[(index-1)]=selected_files[0]
                self.textbox_thai[(index-1)].setText(os.path.basename(selected_files[0]))
            elif target=="file_input_eng":
                self.path_eng[(index-1)]=selected_files[0]
                self.textbox_eng[(index-1)].setText(os.path.basename(selected_files[0]))

    def play_action(self,index):
        conn = sqlite3.connect(database_filename)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bell where status=1 limit 1')
        bell = cursor.fetchone()
        if bell:
            bell=dict(bell)
        else:
            return False

        self.audio_files=[]
        if index!="announcement":
            cursor.execute('SELECT * FROM schedule where id=? limit 1',(index,))
            schedule = cursor.fetchone()
            if schedule:
                schedule=dict(schedule)
            else:
                return False
            conn.commit()
            conn.close()
        
            if schedule['hour'] != "" or schedule['minute'] != "":
                if schedule['tell_time']:
                    self.audio_files.append(bell['first'])
                    self.audio_files.extend(tell_hour(schedule['hour']))
                    self.audio_files.extend(tell_minute(schedule['minute']))
                if schedule['sound']!="":
                    self.audio_files.append(schedule['sound'])
                if schedule['sound_eng']!="":
                    self.audio_files.append(schedule['sound_eng'])
                if schedule['tell_time']:
                    self.audio_files.append(bell['last'])
            else:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setIcon(QtWidgets.QMessageBox.Warning)
                msg_box.setWindowTitle('Alert')
                msg_box.setText('กรุณาเลือกชั่วโมงและนาทีก่อน!')
                msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg_box.exec()
        else:
            self.audio_files.append(bell['first'])

        self.current_index = 0
        self.play_audio()

    def play_audio(self):
        if self.audio_files and self.current_index < len(self.audio_files):
            audio_file = self.audio_files[self.current_index]

            self.initialize_player()

            # Set the new media source
            self.media_player.setSource(QUrl.fromLocalFile(audio_file))
            self.media_player.play()
    
    def initialize_player(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)

    def next_audio(self):
        self.current_index += 1
        if self.current_index < len(self.audio_files):
            self.play_audio()
   
    def on_media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next_audio()

    def initialize_schedule(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_schedule)
        self.timer.start(1000)
        self.last_played_minute = None
        self.load_schedule_from_database()
    
    def load_schedule_from_database(self):
        conn = sqlite3.connect(database_filename)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM schedule where status=1')
        self.schedule_list = cursor.fetchall()
        if self.schedule_list:
            self.schedule_list = [dict(row) for row in self.schedule_list]
        cursor.close()
        conn.commit()
        conn.close()
    
    def check_schedule(self):
        current_time_local = QtCore.QDateTime.currentDateTime()  # Fetch current local time
        
        # Extract hour, minute, and second components from current local time
        current_hour_local = current_time_local.time().hour()
        current_minute_local = current_time_local.time().minute()
        current_second_local = current_time_local.time().second()

        time_string = f"เวลาปัจจุบัน {current_hour_local:02}:{current_minute_local:02}:{current_second_local:02}"
        self.system_time_label.setText(time_string)

        if current_minute_local != self.last_played_minute:
            for schedule in self.schedule_list:
                hour = schedule['hour']
                minute = schedule['minute']
                if hour and minute:
                    scheduled_hour = int(hour)
                    scheduled_minute = int(minute)
                    if (current_hour_local == scheduled_hour and
                        current_minute_local == scheduled_minute):
                        # Perform action when scheduled time matches current time
                        print(f"Scheduled time matched: {scheduled_hour}:{scheduled_minute}")
                        self.play_action(schedule['id'])
                        # Example: Call a function to play sound based on the schedule
                        # self.play_sound(schedule['sound'])
                        
                        # Update any necessary flags or state variables
                        self.last_played_minute = current_minute_local
                        
                        break
         
    def clear_target_data(self,index):
        i=index-1
        self.checkboxes[i].setChecked(False)
        self.checkboxes2[i].setChecked(False)
        self.combobox[i].setCurrentIndex(-1)
        self.combobox_minutes[i].setCurrentIndex(-1)
        self.textbox_thai[i].setText("")
        self.textbox_eng[i].setText("")
        self.path_thai[i]=""
        self.path_eng[i]=""
    
    def clear_all_data(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "ยืนยันการล้างข้อมูล",
            "ต้องการล้างข้อมูลการตั้งค่าทั้งหมดหรือไม่?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            os.remove(database_filename)
            for i in range(1,25):
                self.clear_target_data(i)
            self.checkbox_auto_startup.setChecked(False)
            self.connect_db()
            print("Clear All!!")

    @QtCore.Slot()
    def save_data(self):
        print("Save !!")
        conn = sqlite3.connect(database_filename)
        cursor = conn.cursor()

        for i in range(24):
            hour=self.combobox[i].currentText()
            minute=self.combobox_minutes[i].currentText()
            sound=self.path_thai[i]
            sound_eng=self.path_eng[i]
            if self.checkboxes[i].isChecked():
                status=1
            else:
                status=0
            if self.checkboxes2[i].isChecked():
                tell_time=1
            else:
                tell_time=0
            cursor.execute('''
                UPDATE schedule
                SET hour = ?, minute = ?, sound = ?, sound_eng = ?, status = ?, tell_time = ?
                WHERE id = ?
            ''', (hour, minute, sound, sound_eng, status, tell_time, i+1))
        
        # Update bell
        bell_id=self.combo_bell.currentIndex()
        bell_id=bell_id+1
        cursor.execute('''UPDATE bell set status=0
                       ''')
        cursor.execute('UPDATE bell SET status = 1 WHERE id = ?', (bell_id,))
        
        auto_startup_status=self.checkbox_auto_startup.isChecked()
        cursor.execute('''SELECT * FROM utility where name="auto_startup"''')
        auto_startup = cursor.fetchone()
        if auto_startup_status:
            self.add_to_startup("add")
        else:
            self.add_to_startup("remove")
        if auto_startup:
            cursor.execute('''UPDATE utility SET value=? WHERE name="auto_startup"''', (int(auto_startup_status),))
        else:
            cursor.execute('''INSERT INTO utility (name, value) VALUES (?, ?)''', ("auto_startup", int(auto_startup_status)))
        

        conn.commit()
        conn.close()
        self.initialize_schedule()

    def add_to_startup(self,action):
        os_name = platform.system()
        
        if os_name == 'Windows':
            self.add_to_startup_windows(action)
        elif os_name == 'Linux':
            self.add_to_startup_linux(action)
        else:
            raise NotImplementedError(f"Unsupported OS: {os_name}")
        
    def add_to_startup_windows(self,action):
        try:
            from win32com.client import Dispatch
        except ImportError:
            print("pywin32 is required on Windows.")
            return

        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        script_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        shortcut_path = os.path.join(startup_dir, 'thai_school_alarm.lnk')
        
        if action == 'add':
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = script_path
            shortcut.WorkingDirectory = os.path.dirname(script_path)
            shortcut.save()
        elif action == 'remove':
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
            else:
                print("Startup shortcut does not exist.")

    def add_to_startup_linux(self, action):
        desktop_entry_name = 'thai_school_alarm.desktop'
        autostart_path = os.path.expanduser(f'~/.config/autostart/{desktop_entry_name}')
        executable_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        working_directory = os.path.dirname(executable_path)

        if action == 'add':
            desktop_entry_content = f"""
            [Desktop Entry]
            Type=Application
            Name=Thai School Alarm
            Exec="{executable_path}"
            Path="{working_directory}"
            X-GNOME-Autostart-enabled=true
            """
            try:
                os.makedirs(os.path.dirname(autostart_path), exist_ok=True)
                
                with open(autostart_path, 'w') as desktop_file:
                    desktop_file.write(desktop_entry_content)
                os.chmod(autostart_path, 0o755)  # Make the desktop entry executable
                print("Autostart entry added.")
            except Exception as e:
                print(f"Error adding autostart entry: {e}")
        elif action == 'remove':
            if os.path.exists(autostart_path):
                try:
                    os.remove(autostart_path)
                    print("Autostart entry removed.")
                except Exception as e:
                    print(f"Error removing autostart entry: {e}")
            else:
                print("Autostart entry does not exist.")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thai School Alarm by KruFame")
        
        self.setWindowIcon(QtGui.QIcon("icon.jpg"))

        self.main_widget = QtWidgets.QWidget()
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.widget = MyWidget()
        self.scroll.setWidget(self.widget)

        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.scroll)
        self.main_widget.setLayout(self.layout)

        self.setCentralWidget(self.main_widget)
        self.showMaximized()

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("icon.ico"))

        # Check if system tray is supported
        if QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QtWidgets.QSystemTrayIcon(self)
            self.tray_icon.setIcon(QtGui.QIcon("icon.ico"))

            tray_menu = QtWidgets.QMenu()
            restore_action = tray_menu.addAction("Restore")
            quit_action = tray_menu.addAction("Quit")

            restore_action.triggered.connect(self.show)
            quit_action.triggered.connect(QtWidgets.QApplication.instance().quit)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.on_tray_icon_activated)
            self.tray_icon.show()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                event.ignore()
                self.hide()
                self.tray_icon.showMessage(
                    "Application Minimized",
                    "The application is still running in the system tray.",
                    QtWidgets.QSystemTrayIcon.Information,
                    2000
                )
            else:
                super().changeEvent(event)

    def on_tray_icon_activated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon("icon.jpg")
    app.setWindowIcon(app_icon)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
