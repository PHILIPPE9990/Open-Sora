import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu Bar Example")
        self.setGeometry(100, 100, 600, 400)

        # Create the menu bar
        menu_bar = self.menuBar()

        # Add a "File" menu
        file_menu = menu_bar.addMenu("File")

        # Add actions to the "File" menu
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Add a separator
        file_menu.addAction(exit_action)

        # Add a "Help" menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Connect actions to methods
        exit_action.triggered.connect(self.close)  # Close the application
        about_action.triggered.connect(self.show_about)

    def show_about(self):
        print("This is a simple PyQt application with a menu bar.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
