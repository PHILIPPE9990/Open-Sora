import os
import shutil 
import sys
import re
from front_end import config
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QTextEdit, QPushButton, QHBoxLayout, QWidget, QGroupBox, QVBoxLayout, QRadioButton, QButtonGroup, QFrame, QSlider, QStyle, QSpacerItem, QSizePolicy, QAction, QMenu, QMessageBox, QDialog, QComboBox, QCheckBox
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMovie, QPixmap, QPalette, QBrush, QColor, QLinearGradient

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
#from PyQt5.QtGui import QIcon #Windows icon (later)

#File
from front_end import config
from back_end import llama, videoProcessing
from api import opensoraAPI

def exception_hook(exctype, value, traceback):
        print(f"🚨 Exception: {value}")
        import traceback
        traceback.print_exc()

        msg = QMessageBox()
        msg.setStyleSheet(config.global_style)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"An error occurred:\n{value}")
        msg.setWindowTitle("Error")

        msg.move(500, 250)
        msg.exec_()

class CommandThread(QThread):
    command_finished = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, desc, video_length, resolution, model, seed):
        super().__init__()
        self.desc = desc
        self.video_length = video_length
        self.resolution = resolution
        self.model = model
        self.seed = seed

    def run(self):
        try:
            #print("Hello world")
            #print(self.desc, self.video_length, self.resolution, self.model, self.seed)
            opensoraAPI.runTerminalCommand(self.desc, self.video_length, self.resolution, self.model, self.seed)
        except Exception as e:
            self.error_signal.emit(str(e))

class RefinementDialog(QDialog):

    def __init__(self, original_prompt, parent=None):
        super().__init__(parent)
        self.setWindowTitle(config.prompt)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(600, 400)

        if parent:
            self.move(parent.x() + 500, parent.y() + 150)
        
        self.original_prompt = original_prompt
        self.selected_prompt = None
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()

        # Original Prompt Display
        original_group = QGroupBox(config.og_prompt)
        original_layout = QVBoxLayout() 

        self.original_input = QTextEdit()
        self.original_input.setPlainText(self.original_prompt)
        self.original_input.setStyleSheet(config.original_style)
        self.original_input.setFixedHeight(40)
        self.og_feedback = QLabel("", self)
        self.og_feedback.setStyleSheet("color: #ff0033;background: #383838;")

        original_layout.addWidget(self.original_input)
        original_layout.addWidget(self.og_feedback)
        original_group.setLayout(original_layout)
        
        # Refined Suggestion
        refined_group = QGroupBox(config.re_prompt)
        refined_group.setStyleSheet(config.label_style)
        refined_layout = QVBoxLayout()

        self.refined_input = QTextEdit()
        self.refined_input.setStyleSheet(config.original_style)

        refined_layout.addWidget(self.refined_input)
        refined_group.setLayout(refined_layout)
        
        # Button Row
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton(config.regenerate)
        #self.refresh_button.setStyleSheet("background-color: #f39c12; color: white;")
        
        self.use_button = QPushButton(config.select)
        #self.use_button.setStyleSheet("background-color: #2ecc71; color: white;")
        
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.use_button)
        
        # Assemble main layout
        layout.addWidget(original_group)
        layout.addWidget(refined_group)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Connect signals
        self.use_button.clicked.connect(self.accept_selection)
        self.refresh_button.clicked.connect(self.generate_new_suggestions)
    
    # def enable_use_button(self):
    #     self.use_button.setEnabled(len(self.suggestion_list.selectedItems()) > 0)
    
    def accept_selection(self):
        self.selected_prompt = self.refined_input.toPlainText()
        self.accept()

    def generate_new_suggestions(self):
        if not self.original_input.toPlainText().strip():
            #QMessageBox.warning(self, "Empty Input", "Please enter a subject!")
            self.og_feedback.setText("Please enter a subject!")
            return
        self.refined_input.setText(config.dia_load)
        QApplication.processEvents()
        text = self.original_input.toPlainText()
        retext=llama.generate_scene(text)
        self.refined_input.setText(retext)

class VideoProcessingDialog(QDialog):
    
    def __init__(self, parent=None):

        super().__init__(parent)
        self.setWindowTitle(config.video_processing_heading)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(400, 250)
        
        if parent:
            self.move(parent.x() + 500, parent.y() + 150)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(config.video_processing_title)
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        
        # Options
        options_group = QGroupBox(config.video_processing_opton)
        options_layout = QVBoxLayout()
        
        self.anti_aliasing_check = QCheckBox(config.video_processing_anti_aliasing)
        self.anti_aliasing_check.setChecked(True)
        self.anti_aliasing_check.setToolTip(config.video_processing_anti_aliasing_tip)
        
        self.sharpening_check = QCheckBox(config.video_processing_sharpening)
        self.sharpening_check.setChecked(True)
        self.sharpening_check.setToolTip(config.video_processing_sharpening_tip)
        
        self.resize_check = QCheckBox(config.video_processing_resize)
        self.resize_check.setChecked(True)
        self.resize_check.setToolTip(config.video_processing_resize_tip)
        
        options_layout.addWidget(self.anti_aliasing_check)
        options_layout.addWidget(self.sharpening_check)
        options_layout.addWidget(self.resize_check)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Note
        note = QLabel(config.video_processing_note)
        note.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(note)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.process_button = QPushButton("Enhance Video")
        self.cancel_button = QPushButton("Cancel")
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.process_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def get_options(self):
        return (
            self.anti_aliasing_check.isChecked(),
            self.sharpening_check.isChecked(),
            self.resize_check.isChecked()
        )

class InformationAlert(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(400, 200)
        
        if parent:
            self.move(parent.x() + 500, parent.y() + 150)
        
        self.setup_ui(message)
        
    def setup_ui(self, message):
        layout = QVBoxLayout()
        
        # Message label
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        
        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        
        # Layout
        layout.addWidget(self.message_label)
        layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
#Main window class
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Driven Generation of Customized Publicity Content")
        self.setGeometry(0, 0, config.height, config.width)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.mainPage())
        self.stacked_widget.addWidget(self.newPage())
        self.stacked_widget.currentChanged.connect(self.updateMenuBar)

        self.setCentralWidget(self.stacked_widget)

        #Menu bar
        self.menu_bar = self.menuBar()
        self.action_menu = QMenu(config.action_menu_label, self)
        self.return_mainpage = QAction(config.action_menu_action_return, self)
        self.return_mainpage.triggered.connect(self.switch_to_main_page)

        #self.setWindowIcon() #setWindowIcon

    #Update menu bar
    def updateMenuBar(self, index):
        self.menu_bar.clear()
        if index == 1:
            self.menu_bar.addMenu(self.action_menu)
            self.action_menu.addAction(self.return_mainpage)
    
    #Description
    def description(self):
    
        self.description_input = QTextEdit(self)
        self.description_feeback1 = QLabel("", self)
        self.description_feeback1.setStyleSheet("color: #ff0033;")

        self.description_feeback2 = QLabel("", self)
        self.description_feeback2.setStyleSheet("color: #ff0033;")

        self.description_group_box = QGroupBox(config.desc, self)
        self.description_layout = QVBoxLayout()
       
        self.description_layout.addWidget(self.description_input)
        self.description_group_box.setLayout(self.description_layout)

    def seed_selection(self):
        self.seed_group_box = QGroupBox("Random Seed", self)
        self.seed_layout = QVBoxLayout()
        
        # Create slider
        self.seed_slider = QSlider(Qt.Horizontal)
        self.seed_slider.setRange(0, 1024)  # Adjust range as needed
        self.seed_slider.setValue(42)       # Default seed
        self.seed_slider.setTickInterval(100)
        self.seed_slider.setTickPosition(QSlider.TicksBelow)
        
        # Create display label
        self.seed_value_label = QLabel("Seed: 42")
        
        # Connect signal
        self.seed_slider.valueChanged.connect(self.update_seed_label)
        
        self.seed_layout.addWidget(self.seed_slider)
        self.seed_layout.addWidget(self.seed_value_label)
        self.seed_group_box.setLayout(self.seed_layout)

    def update_seed_label(self, value):
        self.seed_value_label.setText(f"Seed: {value}")

    #Duration
    def video_length(self):
        self.rb_2s = QRadioButton(config.two_second, self)
        self.rb_4s = QRadioButton(config.four_second, self)
        self.rb_8s = QRadioButton(config.eight_second, self)
        self.rb_16s = QRadioButton(config.sixteen_second, self)

        self.rb_2s.setChecked(True)

        self.vl_button_group = QButtonGroup(self)
        self.vl_button_group.addButton(self.rb_2s)
        self.vl_button_group.addButton(self.rb_4s)
        self.vl_button_group.addButton(self.rb_8s)
        self.vl_button_group.addButton(self.rb_16s)

        self.radio_group_box = QGroupBox(config.video_length, self)
        self.radio_layout = QHBoxLayout()
        self.radio_layout.addWidget(self.rb_2s)
        self.radio_layout.addWidget(self.rb_4s)
        self.radio_layout.addWidget(self.rb_8s)
        self.radio_layout.addWidget(self.rb_16s)
        self.radio_group_box.setLayout(self.radio_layout)

        self.radio_button_feeback = QLabel("", self)
        self.radio_button_feeback.setStyleSheet("color: #ff0033;")
    
    #Resolution
    def resolution(self):
        self.rb_144p = QRadioButton(config._144p, self)
        self.rb_240p = QRadioButton(config._240p, self)
        self.rb_360p = QRadioButton(config._360p, self)
        self.rb_480p = QRadioButton(config._480p, self)
        self.rb_720p = QRadioButton(config._720p, self)

        self.rb_144p.setChecked(True)

        self.resolution_button_group = QButtonGroup(self)
        self.resolution_button_group.addButton(self.rb_144p)
        self.resolution_button_group.addButton(self.rb_240p)
        self.resolution_button_group.addButton(self.rb_360p)
        self.resolution_button_group.addButton(self.rb_480p)
        self.resolution_button_group.addButton(self.rb_720p)

        self.resolution_group_box = QGroupBox(config.resolution)
        self.resolution_layout = QHBoxLayout()
        self.resolution_layout.addWidget(self.rb_144p)
        self.resolution_layout.addWidget(self.rb_240p)
        self.resolution_layout.addWidget(self.rb_360p)
        self.resolution_layout.addWidget(self.rb_480p)
        self.resolution_layout.addWidget(self.rb_720p)
        self.resolution_group_box.setLayout(self.resolution_layout)

        self.resolution_button_feeback = QLabel("", self)
        self.resolution_button_feeback.setStyleSheet("color: #ff0033;")
    
    #Submit button
    def submit_button(self):
        self.submit_b = QPushButton(config.submit, self)
        #self.submit_b.setStyleSheet(f"background-color: {config.submitColor}; color: white;")

    #Reset button
    def reset_button(self):
        self.reset_b = QPushButton(config.reset, self)
        #self.reset_b.setStyleSheet(f"background-color: {config.resetColor}; color: white;")
    
    #Download button
    def download_button(self):
        self.download_b =QPushButton(config.download, self)
        self.download_b.setEnabled(False)

    #Refine prompt button
    def refine_prompt_button(self):
        self.refine_prompt_b = QPushButton(config.prompt, self)
        self.refine_prompt_b.setStyleSheet(f"{config.prompt_style}") 
        self.refine_prompt_b.clicked.connect(self.show_refinement_dialog)

    # #Update download button status
    # def update_download_button_status(self, status):
    #     if status == QMediaPlayer.LoadedMedia:
    #         self.download_b.setEnabled(True)
    #     else:
    #         self.download_b.setEnabled(False)
    def show_refinement_dialog(self):
        current_prompt = self.description_input.toPlainText()
        # if not current_prompt.strip():
        #     self.show_information_alert("Empty Prompt", "Please enter a prompt to refine")
        #     return

        dialog = RefinementDialog(current_prompt, self)
        dialog.setStyleSheet(config.global_style)
        if dialog.exec_() == QDialog.Accepted:
            self.description_input.setPlainText(dialog.selected_prompt)

    def model_selection(self):
        self.model_group_box = QGroupBox("Select Model", self)
        self.model_layout = QVBoxLayout()
        
        self.model_combo = QComboBox()
        for model_name, model_value in config.models.items():
            self.model_combo.addItem(model_name, model_value)
        
        # Set default model
        default_index = list(config.models.keys()).index(config.default_model)
        self.model_combo.setCurrentIndex(default_index)
        
        self.model_layout.addWidget(self.model_combo)
        self.model_group_box.setLayout(self.model_layout)

    #Video widget
    def video_widget(self):
        #Create video widget
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        self.video_widget.setFixedSize(800, 600) 

        #need to change later
        # video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/sample_0000.mp4")
        # video_url = QUrl.fromLocalFile(video_path)
        # self.media_player.setMedia(QMediaContent(video_url))

        self.process_button = QPushButton("Enhance Video")
        self.reset_button_video = QPushButton("Reset to Original")
        
        #Play buttton
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        #Video Slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        #Download button
        self.download_button()
        self.download_b.clicked.connect(self.download)

        self.video_processing_layout = QHBoxLayout()
        self.video_processing_layout.addWidget(self.process_button)
        self.video_processing_layout.addWidget(self.reset_button_video)

        self.pannel_layout = QHBoxLayout()
        self.pannel_layout.addWidget(self.download_b)
        self.pannel_layout.addWidget(self.play_button)
        self.pannel_layout.addWidget(self.position_slider)

        self.play_button.clicked.connect(self.play_video)
        self.media_player.stateChanged.connect(self.icon_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.process_button.clicked.connect(self.show_processing_dialog)
        self.reset_button_video.clicked.connect(self.reset_to_original)

    #Slider poistion change when playing video
    def set_position(self, position):
        self.media_player.setPosition(position)

    #Slider --> video position
    def position_changed(self, position): 
        self.position_slider.setValue(position)
    
    #Vary depends on video duration
    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    #Play/Pause video
    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
    
    #Icon change (pause/ play)
    def icon_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    #download
    def download(self):

        #src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/sample_0000.mp4")
        src_path = self.current_video_path
        downloads_folder = "/mnt/c/Users/user/Downloads"
        #downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        des_file_path = os.path.join(downloads_folder, f"video.mp4")
        counter = 1

        while os.path.exists(des_file_path):
            des_file_path = os.path.join(downloads_folder, f"video_{counter}.mp4")
            counter += 1

        shutil.copy(src_path, des_file_path)
        self.show_information_alert(f"{config.download_success_title}", f"{config.download_success_message} {des_file_path}")


    def count_words(self, s):
        return len(s.split())
    
    def check_length(self, n):
        return 3 <= n <= 100
    
    # Allows letters, numbers, whitespace, and common special characters
    def check_wordings(self, s):
        if not re.match(r'^[\w\s\-,.!?;:\'"()@#$%&*+/<=>\\^_`{|}~]*$', s):
            return False
        else:
            return True

    #Validation
    def validate_input(self):
        error_flag = False
        self.resetError()
        desc = self.description_input.toPlainText()

        #description validation
        if(not self.check_wordings(desc)):
            self.description_feeback1.setText(config.Error_desc1)
            error_flag = True

        if(self.check_wordings(desc) and not self.check_length(self.count_words(desc))):
            self.description_feeback2.setText(config.Error_desc2)
            error_flag = True

        #video length validation
        if(not self.vl_button_group.checkedButton()):
            self.radio_button_feeback.setText(config.Error_option)
            error_flag = True

        #resolution validation
        if(not self.resolution_button_group.checkedButton()):
            self.resolution_button_feeback.setText(config.Error_option)
            error_flag = True
        
        if(error_flag == False):
           self.submit()
        else:
            raise ValueError(config.Error_prompt)
    
    def submit(self):
    
        #Get user inputs
        desc = self.description_input.toPlainText()
        video_length = self.vl_button_group.checkedButton().text()
        resolution = self.resolution_button_group.checkedButton().text()
        model = self.model_combo.currentData()
        seed = self.seed_slider.value()
        
        self.gif_label.setVisible(True)
        self.startGIF()

        self.thread = CommandThread(desc, video_length, resolution, model, seed)
        self.thread.error_signal.connect(self.error_thread)
        #self.thread.command_finished.connect(self.check_for_completed)
        self.thread.start()

        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.addPath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/"))
        self.watcher.directoryChanged.connect(self.check_for_completed)

    def error_thread(self, msg):
        self.resetForm()
        QMessageBox.critical(self, "Video Generation Error: ", msg)
    
    def check_for_completed(self, path):
        for file_name in os.listdir(path):
            if file_name.endswith('.mp4'):
                
                self.stopGIF()
                self.gif_label.setVisible(False)

                self.show_information_alert(f"{config.Generated_success_title}", f"{config.Generated_success_message}")

                video_path = os.path.join(path, file_name)
                self.current_video_path = video_path  # Store the initial video path
                self.load_video(video_path)

                # video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/sample_0000.mp4")
                # self.current_video_path = video_path
                # video_url = QUrl.fromLocalFile(video_path)
                # self.media_player.setMedia(QMediaContent(video_url))
                
                self.download_b.setEnabled(True)

                self.video_widget.setVisible(True)
                self.media_player.play()
                
                self.download_b.setVisible(True)
                self.play_button.setVisible(True)
                self.position_slider.setVisible(True)
                self.process_button.setVisible(True)
                self.reset_button_video.setVisible(True)
                break

    #Reset error message
    def resetError(self):
        self.description_feeback1.setText("")
        self.description_feeback2.setText("")
        self.radio_button_feeback.setText("")
        self.resolution_button_feeback.setText("")

    #Reset form
    def resetForm(self):
        self.resetError()
        self.description_input.clear()

        self.seed_slider.setValue(42)
        
        self.vl_button_group.setExclusive(False)
        for b1 in self.vl_button_group.buttons():
            b1.setChecked(False)
        self.vl_button_group.setExclusive(True)

        self.resolution_button_group.setExclusive(False)
        for b2 in self.resolution_button_group.buttons():
            b2.setChecked(False)
        self.resolution_button_group.setExclusive(True)

        self.download_b.setEnabled(False)

        self.stopGIF()
        self.gif_label.setVisible(False)
        self.video_widget.setVisible(False)
        self.download_b.setVisible(False)
        self.play_button.setVisible(False)
        self.position_slider.setVisible(False)

        self.deleteSample()

    def deleteSample(self):
        
        folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
    
            if os.path.isfile(file_path):
                os.remove(file_path) 

        folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/enhanced")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
    
            if os.path.isfile(file_path):
                os.remove(file_path) 

    #Initialize user interface
    def newPage(self):

        page = QWidget()
        page.setStyleSheet(config.global_style)
        self.setCentralWidget(page)

        #Model selection
        self.model_selection()

        #Prompt
        self.description()

        #Prompt Refine
        self.refine_prompt_button()
        #self.refine_prompt_b.clicked.connect()

        #Seed selection
        self.seed_selection()
        
        #Redio button
        self.video_length()

        #Resolution
        self.resolution()

        #Submit button
        self.submit_button()
        self.submit_b.clicked.connect(self.validate_input)

        #Reset button
        self.reset_button()
        self.reset_b.clicked.connect(self.resetForm)

        #Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.reset_b)
        button_layout.addWidget(self.submit_b)

        #Area 1 layout
        self.area1_layout = QVBoxLayout()
        self.area1_layout.addWidget(self.model_group_box) 
        self.area1_layout.addWidget(self.description_group_box)
        self.area1_layout.addWidget(self.refine_prompt_b)
        self.area1_layout.addWidget(self.description_feeback1)
        self.area1_layout.addWidget(self.description_feeback2)
        self.area1_layout.addWidget(self.seed_group_box)
        self.area1_layout.addWidget(self.radio_group_box)
        self.area1_layout.addWidget(self.radio_button_feeback)
        self.area1_layout.addWidget(self.resolution_group_box)
        self.area1_layout.addWidget(self.resolution_button_feeback)
        self.area1_layout.addLayout(button_layout)

        #Loading scene
        self.gif_label = QLabel(self)
        GIF_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../image/loading4.gif")
        self.loading_scene = QMovie(GIF_path) 
        self.gif_label.setMovie(self.loading_scene)
        
        #Area 2 layout
        self.video_widget()
        self.area2_layout =  QVBoxLayout()
        self.area2_layout.addSpacerItem(QSpacerItem(850, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.area2_layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        self.area2_layout.addWidget(self.video_widget, alignment=Qt.AlignCenter)
        self.area2_layout.addSpacerItem(QSpacerItem(650, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.area2_layout.addLayout(self.video_processing_layout)
        self.area2_layout.addLayout(self.pannel_layout)

        #Initial set visibility to False
        self.gif_label.setVisible(False)
        self.video_widget.setVisible(False)
        self.download_b.setVisible(False)
        self.play_button.setVisible(False)
        self.position_slider.setVisible(False)
        self.process_button.setVisible(False)
        self.reset_button_video.setVisible(False)

        #Vertical line
        vline1 = QFrame()
        vline1.setFrameShape(QFrame.VLine)
        vline1.setFrameShadow(QFrame.Sunken)

        #Main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(self.area1_layout,3)  # 3:7 ratio
        main_layout.addWidget(vline1)
        main_layout.addLayout(self.area2_layout,7)  # Placeholder for the second area

        page.setLayout(main_layout)
        return page
    
    def mainPage(self):
        mainPage = QWidget()
        mainPage_layout = QVBoxLayout(mainPage)
        
        # Set background
        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../image/bg.jpg")
        if os.path.exists(bg_path):
            palette = mainPage.palette()
            palette.setBrush(QPalette.Window, QBrush(QPixmap(bg_path).scaled(
                self.size(), 
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )))
            mainPage.setPalette(palette)
            mainPage.setAutoFillBackground(True)

        # Overlay widget - key changes here
        overlay = QWidget(mainPage)
        overlay.setStyleSheet("""
            background-color: rgba(30, 30, 30, 0.8);  
            border-radius: 4px ;
        """)
        overlay.setFixedSize(500, 300)
        
        # Critical: Add a layout to the overlay
        overlay_layout = QVBoxLayout(overlay)
        overlay_layout.setContentsMargins(0, 0, 0, 0)  # Remove default margins
        
        # Content widget - now fills the overlay
        content = QWidget(overlay)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)  # Add internal padding
        
        # Label and button
        mainPage_label = QLabel(config.dia_label)
        mainPage_label.setStyleSheet(config.dialog_label)
        mainPage_label.setAlignment(Qt.AlignCenter)  # Directly set alignment
        
        button = QPushButton(config.dia_button)
        button.setStyleSheet(config.dialog_button)
        button.setFixedSize(300, 50)
        button.clicked.connect(self.switch_to_new_page)
        
        # Add widgets to content layout
        content_layout.addWidget(mainPage_label, 0, Qt.AlignCenter)
        content_layout.addWidget(button, 0, Qt.AlignCenter)
        
        # Add stretch to push content to vertical center
        content_layout.addStretch(1)
        
        # Add content to overlay
        overlay_layout.addWidget(content, 0, Qt.AlignCenter) 
        
        # Center overlay in main page
        mainPage_layout.addWidget(overlay, 0, Qt.AlignCenter)
        
        return mainPage
    
    def startGIF(self):
        self.loading_scene.start()
    
    def stopGIF(self):
        self.loading_scene.stop()
    
    def switch_to_main_page(self):
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_new_page(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_information_alert(self, title, message):
        dialog = InformationAlert(title, message, self)
        dialog.setStyleSheet(config.global_style)
        dialog.exec_()
    
    def show_processing_dialog(self):
        dialog = VideoProcessingDialog(self)
        dialog.setStyleSheet(config.global_style)
        
        if dialog.exec_() == QDialog.Accepted:
            anti_aliasing, sharpening, resize = dialog.get_options()
            
            processing_msg = InformationAlert("Processing", "Your video is being processed...", self)
            processing_msg.setStyleSheet(config.global_style)
            processing_msg.show()
            QApplication.processEvents()
            

            # Process the video
            input_path = "sample_0000.mp4"
            output_path = videoProcessing.video_processing(input_path, anti_aliasing, resize, sharpening)
            
            # Load the processed video
            output_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/enhanced/"), output_path)
            self.current_video_path = output_path 
            self.load_video(output_path)
              
            processing_msg.close()
            self.show_information_alert("Success", "Video processed successfully!")

            # processing_msg.close()
            # QMessageBox.warning(self, "Processing Error", f"Could not process video: {str(e)}")

    def reset_to_original(self):
        original_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/sample_0000.mp4")
        self.load_video(original_path)
        self.current_video_path = original_path
        self.show_information_alert("Reset", "Video reset to original version")

    def load_video(self, video_path):
        video_url = QUrl.fromLocalFile(video_path)
        self.media_player.setMedia(QMediaContent(video_url))
        self.media_player.play()

def main():
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    #app.setStyleSheet(config.global_style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()