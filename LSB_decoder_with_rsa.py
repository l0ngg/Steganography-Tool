from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QFileDialog, QLabel, QLineEdit
)
from itsdangerous import base64_decode
from functions.LSB import decode_lsb
import sys
import base64
from functions.encryptor import decrypt_message
from functions.rsa import decrypt_dome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Window(QWidget):
    def __init__(self):
        self.path = ''
        self.key_path = ''
        
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
        
        self.key_indicator = QLabel('Select the the private key for RSA decryption:')
        key_select = QPushButton("Select key")
        key_select.setFixedSize(80,30)
        key_select.clicked.connect(self.open_key)
 
        decode_button = QPushButton("Decode")
        decode_button.setFixedSize(80,30)
        decode_button.clicked.connect(self.show_popup)
        
        layout.addWidget(self.input_display, 0, 0, 1 , 1)
        layout.addWidget(file_button, 0, 2)
        layout.addWidget(self.key_indicator, 1, 0)
        layout.addWidget(key_select, 1, 2)
        # layout.addWidget(key_indicator, 1, 0)
        # layout.addWidget(self.key_input, 2, 0)
        layout.addWidget(decode_button, 3, 2)

    def show_popup(self):
        if self.key_path == '':
            msg = QMessageBox(parent=self, text="No key was selected")
            msg.setWindowTitle('Result')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        elif self.path != '':
            message = base64_decode( decode_lsb(self.path[0]) )
            print(message)
            # print(self.key_input.text())
            print(self.key_path[0])
            # message = decrypt_message( message, self.key_input.text() )
            private_key = RSA.import_key(open(self.key_path[0]).read())
            print('key obtained')
            decryptor = PKCS1_OAEP.new(private_key)
            message = decryptor.decrypt(message)
            # message = decrypt_dome( message , private_key)
            # print(2)
            message = message.decode('utf-8')
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
        
    def open_key(self):
        self.key_path = QFileDialog.getOpenFileName(self, 'Open a file', '','Keys(*.pem)')
        print(self.key_path)
        self.key_indicator.setText( 'Key selected: ' + self.key_path[0].split('/')[-1])

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())