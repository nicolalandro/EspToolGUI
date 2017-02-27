import os

import sys

from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog

import serial.tools.list_ports

absolute_path = os.path.dirname(os.path.abspath(__file__))
# print (absolute_path)


def erase(port):
    erase_string = "sudo python " + absolute_path + "/esptool.py --port " + port + " --baud 115200 erase_flash"
    # print(erase_string)
    os.system(erase_string)


def flash(port, firmware_path):
    flash_string = "sudo python " + absolute_path + "esptool.py --port " + port + " write_flash -fm dio -fs 32m 0x00000 " + firmware_path
    # print (flash_string)
    os.system(flash_string)


class MainWindow(QtGui.QMainWindow):
    def flash_firmware(self):
        port = str(self.portComboBox.currentText())
        firmware_path = str(self.pathTextEdit.toPlainText())
        erase(port)
        flash(port, firmware_path)

    def select_firmware(self):
        self.pathTextEdit.setText(QFileDialog.getOpenFileName())

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(500, 100)
        self.setWindowTitle('ESP Tool')

        c_widget = QtGui.QWidget(self)

        grid = QtGui.QGridLayout(c_widget)

        v_box_flashing = QtGui.QVBoxLayout()
        button_flashing = QtGui.QPushButton("Flash Firmware")
        button_flashing.clicked.connect(self.flash_firmware)
        v_box_flashing.addWidget(button_flashing)

        v_box_select_firmware = QtGui.QVBoxLayout()
        button_select_firmware = QtGui.QPushButton("Select Firmware")
        button_select_firmware.clicked.connect(self.select_firmware)
        v_box_select_firmware.addWidget(button_select_firmware)

        self.pathTextEdit = QtGui.QTextEdit(c_widget)
        self.pathTextEdit.setMaximumSize(500, 30)

        label = QtGui.QLabel("Select shield connected Port")
        self.portComboBox = QtGui.QComboBox()
        for p in serial.tools.list_ports.comports():
            self.portComboBox.addItem("/dev/" + p.name)

        grid.addWidget(label, 0, 0)
        grid.addWidget(self.portComboBox, 0, 1, 1, 2)
        grid.addWidget(self.pathTextEdit, 1, 0, 1, 2)
        grid.addLayout(v_box_select_firmware, 1, 2)
        grid.addLayout(v_box_flashing, 2, 0, 3, 0)

        c_widget.setLayout(grid)
        self.setCentralWidget(c_widget)


app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
