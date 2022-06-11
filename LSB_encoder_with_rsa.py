from PyQt6.QtWidgets import (
    QLineEdit ,QApplication, QWidget, QTextEdit, QPushButton, QGridLayout, QMessageBox, QFileDialog, QLabel
)
from itsdangerous import base64_decode, base64_encode
from functions.LSB import encode_lsb
from functions.encryptor import encrypt_message, generate_keys
import sys
import base64

class Window(QWidget):
    def __init__(self):
        self.path = ''
        
        super().__init__()
        self.setWindowTitle("Image LSB Encoder")
 
        layout = QGridLayout()
        self.setLayout(layout)

        self.keygen = QLabel('Click to generate random pair of keys')
        genbutton = QPushButton("Generate")
        genbutton.setFixedSize(80,30)
        genbutton.clicked.connect(self.gener_key)

        file_button = QPushButton("Select image")
        file_button.setFixedSize(80,30)
        file_button.clicked.connect(self.open_file)
        
        self.input_display = QLabel('No file selected')
        self.input_display.setWordWrap(True)
        
        input_indicator = QLabel('Enter the message you want to hide:')
        input_indicator.setFixedHeight(25)

        self.input_box = QTextEdit()
        # input_box.setFixedSize(300,200)

        key_indicator = QLabel('Enter the public key for RSA encryption:')

        self.key_input = QLineEdit()
        self.key_input.setFixedWidth(175)

        name_indicator = QLabel('Enter the resulting filename (with extension):')

        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(175)
 
        encode_button = QPushButton("Encode")
        encode_button.setFixedSize(80,30)
        encode_button.clicked.connect(self.show_popup)
        
        layout.addWidget(self.keygen, 0, 0)
        layout.addWidget(genbutton, 0, 1)
        
        layout.addWidget(file_button, 1, 1)
        layout.addWidget(self.input_display, 1, 0)
        
        layout.addWidget(input_indicator, 2, 0)
        
        layout.addWidget(self.input_box, 3, 0)
        
        layout.addWidget(key_indicator, 4, 0)
        layout.addWidget(self.key_input, 5, 0)
        
        layout.addWidget(name_indicator, 6, 0)
        layout.addWidget(self.name_input, 7, 0)
        layout.addWidget(encode_button, 7, 1)
        
        self.setMinimumSize(self.sizeHint())
    
    def show_popup(self):
        msg = QMessageBox(parent=self, text="No file was selected")
        msg.setWindowTitle('Result')
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        if self.path != '':
            if self.input_box.toPlainText() == '':
                msg.setText("No message was entered")
            
            elif (self.name_input.text() == '') or ('.' not in self.name_input.text()):
                msg.setText("You need to enter the name of the new resulting image (with extension)")
            
            elif (self.key_input.text() == ''):
                msg.setText("You need to enter the public key")
            else:
                encrypted = encrypt_message(self.input_box.toPlainText(), self.key_input.text())
                print(encrypted)
                encrypted = base64_encode(encrypted)
                print(encrypted)
                encrypted = encrypted.decode('utf-8')
                print(encrypted)
                encode_lsb(self.path[0], encrypted, self.name_input.text())
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("The message was encrypted and encoded into " + self.name_input.text())
        # msg.setInformativeText("This is some random text:")

        msg.exec()
    
    def open_file(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '','Images(*.png)')
        self.input_display.setText( 'Selected: ' + self.path[0].split('/')[-1])

    def gener_key(self):
        pub_key, priv_key = generate_keys()
        with open('keys.txt', 'w', encoding='utf-8') as fil:
            fil.write( str(pub_key) + "\n" + str(priv_key))
        msg2 = QMessageBox(parent = self, text = "Public key is: \n" + str(pub_key) + "\n Private key is: \n" + str(priv_key) + "\n The keys are written into key.txt text file")
        msg2.setWindowTitle("Keys generated")
        msg2.setIcon(QMessageBox.Icon.Information)
        msg2.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg2.exec()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())