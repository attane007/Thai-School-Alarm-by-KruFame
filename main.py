import sys
import sqlite3
import os
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from scheduler import SoundScheduler
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

        self.setWindowTitle("Thai School Alarm by KruFame")
        self.setStyleSheet("background-color: white;")
        

        # Widgets
        self.button = QtWidgets.QPushButton("Save!")
        self.name_label = QtWidgets.QLabel("Name:")
        # self.name_label.setFixedWidth(50)
        self.head_label3 = QtWidgets.QLabel("ชั่วโมง")
        self.head_label4 = QtWidgets.QLabel("นาที")
        self.head_label5 = QtWidgets.QLabel("เสียง")
        self.head_label6 = QtWidgets.QLabel("ทดสอบ")
        self.head_label7 = QtWidgets.QLabel("เสียงอังกฤษ")
        self.head_label8 = QtWidgets.QLabel("ล้างข้อมูล")
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
            play_button.setIcon(QIcon("resource/play-circle-svgrepo-com.svg"))
            play_button.setStyleSheet("background-color: #dc143c; color: white;")
            play_button.clicked.connect(lambda checked,index=i:self.play_action(index))
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


        # Adding grid layout to the main layout
        self.layout.addLayout(self.form_grid_layout)
        self.layout.addWidget(self.button)

        # Signals
        self.button.clicked.connect(self.save_data)
        self.head_checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        self.head_checkbox_time.stateChanged.connect(self.on_checkbox_time_state_changed)


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
            status BOOLEAN DEFAULT 0)
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
        file_dialog.setNameFilter("Audio files (*.wav *.mp3)")
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

    @QtCore.Slot()
    def save_data(self):
        print("save !!")
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
        conn.commit()
        conn.close()

    def play_action(self,index):
        conn = sqlite3.connect(database_filename)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bell where status=1 limit 1')
        bell = cursor.fetchone()
        if bell:
            bell=dict(bell)

        cursor.execute('SELECT * FROM schedule where id=? limit 1',(index,))
        schedule = cursor.fetchone()
        if schedule:
            schedule=dict(schedule)
        conn.commit()
        conn.close()
    
        self.audio_files=[]
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


            
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()

    widget.showMaximized()
    sys.exit(app.exec())