import os
import sys
import config
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QHBoxLayout, QWidget, QGroupBox, QVBoxLayout, QRadioButton, QButtonGroup, QFrame, QSlider, QStyle
from PyQt5.QtCore import Qt, QUrl

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
#from PyQt5.QtGui import QIcon #Windows icon (later)

#Main window class
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Driven Generation of Customized Publicity Content")
        self.setGeometry(0, 0, config.height, config.width)
        self.initUI()
        #self.setWindowIcon() #setWindowIcon

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
        download_b =QPushButton(config.download, self)
        download_b.setEnabled(False)
        return download_b

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

    #Validation
    def validate_input(self):
        error_flag = False
        self.resetError()
        desc = self.description_input.toPlainText()
        print(desc)

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

    #Reset error message
    def resetError(self):
        self.description_feeback.setText("")
        self.radio_button_feeback.setText("")
        self.resolution_button_feeback.setText("")

    #Reset form
    def resetForm(self):
        self.description_input.clear()
        
        self.vl_button_group.setExclusive(False)
        for b1 in self.vl_button_group.buttons():
            b1.setChecked(False)
        self.vl_button_group.setExclusive(True)

        self.resolution_button_group.setExclusive(False)
        for b2 in self.resolution_button_group.buttons():
            b2.setChecked(False)
        self.resolution_button_group.setExclusive(True)

    #Initialize user interface
    def initUI(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
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
        area1_layout = QVBoxLayout()
        area1_layout.addWidget(self.description_group_box)
        area1_layout.addWidget(self.description_feeback)
        area1_layout.addWidget(self.radio_group_box)
        area1_layout.addWidget(self.radio_button_feeback)
        area1_layout.addWidget(self.resolution_group_box)
        area1_layout.addWidget(self.resolution_button_feeback)
        area1_layout.addLayout(button_layout)
        
        #Area 2 layout
        #Create video widget
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        #need to change later
        video_path = os.path.join(script_dir, "../video/example.mp4")
        video_url = QUrl.fromLocalFile(video_path)
        self.media_player.setMedia(QMediaContent(video_url))
        
        #Play buttton
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        #Video Slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        pannel_layout = QHBoxLayout()
        pannel_layout.addWidget(self.download_button())
        pannel_layout.addWidget(self.play_button)
        pannel_layout.addWidget(self.position_slider)

        self.play_button.clicked.connect(self.play_video)
        self.media_player.stateChanged.connect(self.icon_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.position_slider.sliderMoved.connect(self.set_position)

        area2_layout =  QVBoxLayout()
        area2_layout.addWidget(self.video_widget)
        area2_layout.addLayout(pannel_layout)

        #Vertical line
        vline1 = QFrame()
        vline1.setFrameShape(QFrame.VLine)
        vline1.setFrameShadow(QFrame.Sunken)

        #Main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(area1_layout, 3)  # 3:7 ratio
        main_layout.addWidget(vline1)
        main_layout.addLayout(area2_layout,7)  # Placeholder for the second area

        central_widget.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()