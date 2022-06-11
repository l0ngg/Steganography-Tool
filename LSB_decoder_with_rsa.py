from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QFileDialog, QLabel, QLineEdit
)
from itsdangerous import base64_decode
from functions.LSB import decode_lsb
import sys
import base64
from functions.encryptor import decrypt_message

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
        
        key_indicator = QLabel('Enter the private key for RSA decryption:')

        self.key_input = QLineEdit()
        self.key_input.setFixedWidth(175)
 
        decode_button = QPushButton("Decode")
        decode_button.setFixedSize(80,30)
        decode_button.clicked.connect(self.show_popup)
        
        layout.addWidget(self.input_display, 0, 0, 1 , 1)
        layout.addWidget(file_button, 0, 2)
        layout.addWidget(key_indicator, 1, 0)
        layout.addWidget(self.key_input, 2, 0)
        layout.addWidget(decode_button, 3, 2)

    def show_popup(self):
        if self.path != '':
            message = base64_decode( decode_lsb(self.path[0]) )
            # print(message)
            # print(self.key_input.text())
            message = decrypt_message( message, self.key_input.text() ) 
            # print(message)
            msg = QMessageBox(parent=self, text="No file was selected")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("The decoded message is:\n" + message)
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