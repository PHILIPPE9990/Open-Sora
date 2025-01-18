import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtGui import QMovie 
from PyQt5.QtCore import Qt 


class LoadingGif(object): 

	def mainUI(self, FrontWindow): 
		FrontWindow.setObjectName("FTwindow") 
		FrontWindow.resize(700, 700) 
		self.centralwidget = QtWidgets.QWidget(FrontWindow) 
		self.centralwidget.setObjectName("main-widget") 

		# Label Create 
		self.label = QtWidgets.QLabel(self.centralwidget) 
		# self.label.setGeometry(QtCore.QRect(25, 25, 200, 200)) 
		# self.label.setMinimumSize(QtCore.QSize(250, 250)) 
		# self.label.setMaximumSize(QtCore.QSize(250, 250)) 
		self.label.setObjectName("lb1") 
		
		FrontWindow.setCentralWidget(self.centralwidget) 

		# Loading the GIF 
        #need to change later
		script_dir = os.path.dirname(os.path.abspath(__file__))
		image_path = os.path.join(script_dir, "../image/game_loading.gif")

		self.movie = QMovie(image_path) 
		self.label.setMovie(self.movie) 

		self.startAnimation() 
		self.watcher = QtCore.QFileSystemWatcher()
		self.watcher.addPath(os.path.join(script_dir, "../samples/samples/"))
		self.watcher.directoryChanged.connect(self.check_for_completed)


	# Start Animation 
	def startAnimation(self): 
		self.movie.start() 

	# Stop Animation(According to need) 
	def stopAnimation(self): 
		self.movie.stop()
		self.label.hide()
		
	def check_for_completed(self, path):

		for file_name in os.listdir(path):
			if file_name.endswith('.mp4'):
				self.stopAnimation()
				break


app = QtWidgets.QApplication(sys.argv) 
window = QtWidgets.QMainWindow() 
demo = LoadingGif() 
demo.mainUI(window) 
window.show() 
sys.exit(app.exec_()) 
