from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QFileDialog, QLabel
)
from functions.LSB import decode_lsb
import sys
from itsdangerous import base64_decode, base64_encode

class Window(QWidget):
    def __init__(self):
        self.path = ''
        
        super().__init__()
        self.setWindowTitle("Image LSB Decoder")
 
        layout = QGridLayout()
        self.setLayout(layout)

        file_button = QPushButton("Select image")
        file_button.setFixedSize(80,30)
        file_button.clicked.connect(self.open_file)
        
        self.input_display = QLabel('No file selected')
        self.input_display.setFixedWidth(250)
        self.input_display.setWordWrap(True)
 
        decode_button = QPushButton("Decode")
        decode_button.setFixedSize(80,30)
        decode_button.clicked.connect(self.show_popup)
        
        layout.addWidget(self.input_display, 0, 0, 1 , 1)
        layout.addWidget(file_button, 0, 2)
        layout.addWidget(decode_button, 1, 2)

    def show_popup(self):
        if self.path != '':
            message = decode_lsb(self.path[0])
            msg = QMessageBox(parent=self, text="No file was selected")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("The decoded message is:\n" + message)
            print( base64_decode(message) )
        else:
            msg = QMessageBox(parent=self, text="No file was selected")
            msg.setWindowTitle('Result')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        # msg.setInformativeText("This is some random text:")

        ret = msg.exec()
    
    def open_file(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '','Images (*.png)')
        self.input_display.setText( 'Selected: ' + self.path[0].split('/')[-1])

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())