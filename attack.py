from PIL import Image
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QFileDialog, QLabel, QTabWidget
)

from sympy import Q
from functions.LSB import decode_lsb
from functions.Partity import steganalyse
from functions.pillowqt import pil2pixmap
import sys

class Window(QWidget):
    def __init__(self):
        self.path = ''
        
        super().__init__()
        self.setWindowTitle("Simple scan attacker")
 
        layout = QGridLayout()
        self.setLayout(layout)

        file_button = QPushButton("Select image")
        file_button.setFixedSize(80,30)
        file_button.clicked.connect(self.open_file)
        
        self.input_display = QLabel('No file selected')
        self.input_display.setFixedWidth(250)
        self.input_display.setWordWrap(True)
 
        decode_button = QPushButton("Analyse")
        decode_button.setFixedSize(80,30)
        decode_button.clicked.connect(self.show_popup)
        
        self.tab_list = QTabWidget()
        # im = Image.open(r"D:\github repos\Steganography-Tool\result.png")
        # self.imagebox.setPixmap( pil2pixmap(steganalyse(im) ))
        
        layout.addWidget(self.input_display, 0, 0, 1 , 1)
        layout.addWidget(file_button, 0, 2)
        layout.addWidget(decode_button, 1, 2)
        layout.addWidget(self.tab_list, 2, 0)

    def show_popup(self):
        if self.path != '':
            im = Image.open(self.path[0])
            imagebox = QLabel()
            imagebox.setPixmap( pil2pixmap(steganalyse(im) ))
            self.tab_list.addTab(imagebox, self.path[0].split('/')[-1])
            imagebox.adjustSize()
            self.input_display.setText('No file selected')
            self.path = ''
        else:
            msg = QMessageBox(parent=self, text="No file was selected")
            msg.setWindowTitle('Result')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        # msg.setInformativeText("This is some random text:")
    
    def open_file(self):
        self.path = QFileDialog.getOpenFileName(self, 'Open a file', '','Images (*.png)')
        self.input_display.setText( 'Selected: ' + self.path[0].split('/')[-1])

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())