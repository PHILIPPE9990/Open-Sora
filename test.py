from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QLabel, QPushButton, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimum Length Validation")

        # Create widgets
        self.label = QLabel("Please enter at least 5 characters:", self)
        self.input = QLineEdit(self)
        self.feedback = QLabel("", self)
        self.feedback.setStyleSheet("color: red;")  # Set feedback text color

        # Button to trigger validation
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.validate_input)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.feedback)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def validate_input(self):
        text = self.input.text()
        if len(text) < 5:
            self.feedback.setText("Error: Input must be at least 5 characters!")
        else:
            self.feedback.setText("Success: Valid input!")
            self.feedback.setStyleSheet("color: green;")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
