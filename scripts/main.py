import os
import shutil 
import sys
from front_end import config
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel, QTextEdit, QPushButton, QHBoxLayout, QWidget, QGroupBox, QVBoxLayout, QRadioButton, QButtonGroup, QFrame, QSlider, QStyle, QSpacerItem, QSizePolicy, QAction, QMenu, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMovie

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
#from PyQt5.QtGui import QIcon #Windows icon (later)

#File
from front_end import config
from api import opensoraAPI

def exception_hook(exctype, value, traceback):
        print(f"🚨 Exception: {value}")
        import traceback
        traceback.print_exc()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"An error occurred:\n{value}")
        msg.setWindowTitle("Error")
        msg.exec_()

class CommandThread(QThread):
    command_finished = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, desc, video_length, resolution):
        super().__init__()
        self.desc = desc
        self.video_length = video_length
        self.resolution = resolution

    def run(self):
        try:
            opensoraAPI.runTerminalCommand(self.desc, self.video_length, self.resolution)
        except Exception as e:
            self.error_signal.emit(str(e))

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
        self.description_feeback = QLabel("", self)
        self.description_feeback.setStyleSheet("color: red;")

        self.description_group_box = QGroupBox(config.desc, self)
        self.description_layout = QVBoxLayout()
       
        self.description_layout.addWidget(self.description_input)
        self.description_group_box.setLayout(self.description_layout)

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
        self.radio_button_feeback.setStyleSheet("color: red;")
    
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
        self.resolution_button_feeback.setStyleSheet("color: red;")
    
    #Submit button
    def submit_button(self):
        self.submit_b = QPushButton(config.submit, self)
        self.submit_b.setStyleSheet(f"background-color: {config.submitColor}; color: white;")

    #Reset button
    def reset_button(self):
        self.reset_b = QPushButton(config.reset, self)
        self.reset_b.setStyleSheet(f"background-color: {config.resetColor}; color: white;")
    
    #Download button
    def download_button(self):
        self.download_b =QPushButton(config.download, self)
        self.download_b.setEnabled(False)

    # #Update download button status
    # def update_download_button_status(self, status):
    #     if status == QMediaPlayer.LoadedMedia:
    #         self.download_b.setEnabled(True)
    #     else:
    #         self.download_b.setEnabled(False)

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

        self.pannel_layout = QHBoxLayout()
        self.pannel_layout.addWidget(self.download_b)
        self.pannel_layout.addWidget(self.play_button)
        self.pannel_layout.addWidget(self.position_slider)

        self.play_button.clicked.connect(self.play_video)
        self.media_player.stateChanged.connect(self.icon_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.position_slider.sliderMoved.connect(self.set_position)

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

        src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/sample_0000.mp4")
        downloads_folder = "/mnt/c/Users/user/Downloads"
        #downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        des_file_path = os.path.join(downloads_folder, f"video.mp4")
        counter = 1

        while os.path.exists(des_file_path):
            des_file_path = os.path.join(downloads_folder, f"video_{counter}.mp4")
            counter += 1

        shutil.copy(src_path, des_file_path)
        self.show_information_alert(f"{config.download_success_title}", f"{config.download_success_message} {des_file_path}")


    #Validation
    def validate_input(self):
        error_flag = False
        self.resetError()
        desc = self.description_input.toPlainText()

        #description validation
        if len(desc) < 5:
            self.description_feeback.setText(config.Error_desc)
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
    
    def submit(self):
    
        #Get user inputs
        desc = self.description_input.toPlainText()
        video_length = self.vl_button_group.checkedButton().text()
        resolution = self.resolution_button_group.checkedButton().text()
        
        self.gif_label.setVisible(True)
        self.startGIF()

        self.thread = CommandThread(desc, video_length, resolution)
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

                video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../samples/samples/sample_0000.mp4")
                video_url = QUrl.fromLocalFile(video_path)
                self.media_player.setMedia(QMediaContent(video_url))
                
                self.download_b.setEnabled(True)

                self.video_widget.setVisible(True)
                self.media_player.play()
                
                self.download_b.setVisible(True)
                self.play_button.setVisible(True)
                self.position_slider.setVisible(True)
                break

    #Reset error message
    def resetError(self):
        self.description_feeback.setText("")
        self.radio_button_feeback.setText("")
        self.resolution_button_feeback.setText("")

    #Reset form
    def resetForm(self):
        self.resetError()
        self.description_input.clear()
        
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

    #Initialize user interface
    def newPage(self):

        page = QWidget()
        self.setCentralWidget(page)
        
        #Prompt
        self.description()
        
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
        self.area1_layout.addWidget(self.description_group_box)
        self.area1_layout.addWidget(self.description_feeback)
        self.area1_layout.addWidget(self.radio_group_box)
        self.area1_layout.addWidget(self.radio_button_feeback)
        self.area1_layout.addWidget(self.resolution_group_box)
        self.area1_layout.addWidget(self.resolution_button_feeback)
        self.area1_layout.addLayout(button_layout)

        #Loading scene
        self.gif_label = QLabel(self)
        GIF_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../image/loading3.gif")
        self.loading_scene = QMovie(GIF_path) 
        self.gif_label.setMovie(self.loading_scene)
        
        #Area 2 layout
        self.video_widget()
        self.area2_layout =  QVBoxLayout()
        self.area2_layout.addSpacerItem(QSpacerItem(850, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.area2_layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        self.area2_layout.addWidget(self.video_widget, alignment=Qt.AlignCenter)
        self.area2_layout.addSpacerItem(QSpacerItem(850, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.area2_layout.addLayout(self.pannel_layout)

        #Initial set visibility to False
        self.gif_label.setVisible(False)
        self.video_widget.setVisible(False)
        self.download_b.setVisible(False)
        self.play_button.setVisible(False)
        self.position_slider.setVisible(False)

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
        mainPage_layout = QVBoxLayout()

        mainPage_label = QLabel("Welcome to Philippe Sora", self)
        mainPage_label.setStyleSheet("font-size: 40px;")

        button = QPushButton("Start")
        button.clicked.connect(self.switch_to_new_page)
        button.setFixedSize(300, 50)

        mainPage_layout.addWidget(mainPage_label,alignment=Qt.AlignCenter)
        mainPage_layout.addWidget(button, alignment=Qt.AlignCenter)

        mainPage.setLayout(mainPage_layout)
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

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

def main():
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()