import os

import sys
from PyQt4 import QtGui

from PyQt4.QtGui import QFileDialog


class MainWindow(QtGui.QMainWindow):
    def flash_firmware(self):
        erase1 = "sudo python esptool.py --port "
        erase2 = " --baud 115200 erase_flash"
        erase = erase1 + str(self.portTextEdit.toPlainText()) + erase2
        # print(erase)
        os.system(erase)

        flash1 = "sudo python esptool.py --port"
        flash2 = " write_flash -fm dio -fs 32m 0x00000 "
        flash = flash1 + str(self.portTextEdit.toPlainText()) + flash2 + str(self.pathTextEdit.toPlainText())
        #print (flash)
        os.system(flash)

    def select_firmware(self):
        self.pathTextEdit.setText(QFileDialog.getOpenFileName())

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(500, 100)
        self.setWindowTitle('ESP Tool')

        cWidget = QtGui.QWidget(self)

        grid = QtGui.QGridLayout(cWidget)

        vBoxFlashing = QtGui.QVBoxLayout()
        buttonFlashing = QtGui.QPushButton("Flash Firmware")
        buttonFlashing.clicked.connect(self.flash_firmware)
        vBoxFlashing.addWidget(buttonFlashing)

        vBoxSelectFirmware = QtGui.QVBoxLayout()
        buttonSelectFirmware = QtGui.QPushButton("Select Firmware")
        buttonSelectFirmware.clicked.connect(self.select_firmware)
        vBoxSelectFirmware.addWidget(buttonSelectFirmware)

        self.pathTextEdit = QtGui.QTextEdit(cWidget)
        self.pathTextEdit.setMaximumSize(500, 30)

        label = QtGui.QLabel("Write Shield Port")
        self.portTextEdit = QtGui.QTextEdit(cWidget)
        self.portTextEdit.setMaximumSize(500, 30)
        self.portTextEdit.setText("/dev/ttyUSB0")

        grid.addWidget(label, 0, 0)
        grid.addWidget(self.portTextEdit, 0, 1)
        grid.addWidget(self.pathTextEdit, 1, 0, 1, 2)
        grid.addLayout(vBoxSelectFirmware, 1, 2)
        grid.addLayout(vBoxFlashing, 2, 0, 3, 0)

        cWidget.setLayout(grid)
        self.setCentralWidget(cWidget)


app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
