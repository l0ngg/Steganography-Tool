from PyQt6.QtWidgets import (
    QLineEdit ,QApplication, QWidget, QTextEdit, QPushButton, QGridLayout, QMessageBox, QFileDialog, QLabel
)
from functions.LSB import encode_lsb
import sys

class Window(QWidget):
    def __init__(self):
        self.path = ''
        
        super().__init__()
        self.setWindowTitle("Image LSB Encoder")
 
        layout = QGridLayout()
        self.setLayout(layout)

        file_button = QPushButton("Select image")
        file_button.setFixedSize(80,30)
        file_button.clicked.connect(self.open_file)
        
        self.input_display = QLabel('No file selected')
        self.input_display.setWordWrap(True)
        
        input_indicator = QLabel('Enter the message you want to hide:')
        input_indicator.setFixedHeight(25)

        self.input_box = QTextEdit()
        # input_box.setFixedSize(300,200)

        name_indicator = QLabel('Enter the resulting filename (with extension):')

        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(175)
 
        encode_button = QPushButton("Encode")
        encode_button.setFixedSize(80,30)
        encode_button.clicked.connect(self.show_popup)
        
        layout.addWidget(file_button, 0, 1)
        layout.addWidget(self.input_display, 0, 0)
        layout.addWidget(input_indicator, 1, 0)
        layout.addWidget(self.input_box, 2, 0)
        layout.addWidget(name_indicator, 3, 0)
        layout.addWidget(self.name_input, 4, 0)
        layout.addWidget(encode_button, 4, 1)
        
        self.setMinimumSize(self.sizeHint())
    
    def show_popup(self):
        print(self.name_input.text())
        msg = QMessageBox(parent=self, text="No file was selected")
        msg.setWindowTitle('Result')
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        if self.path != '':
            if self.input_box.toPlainText() == '':
                msg.setText("No message was entered")
            
            elif (self.name_input.text() == '') or ('.' not in self.name_input.text()):
                msg.setText("You need to enter the name of the new resulting image (with extension)")
            
            else:
                encode_lsb(self.path[0], self.input_box.toPlainText(), self.name_input.text())
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("The message was encoded into " + self.name_input.text())
        # msg.setInformativeText("This is some random text:")

        ret = msg.exec()
    
    def open_file(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '','Images(*.png)')
        self.input_display.setText( 'Selected: ' + self.path[0].split('/')[-1])

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())