import os

import sys

from PyQt4 import QtGui
from PyQt4.QtGui import QFileDialog

import serial.tools.list_ports

from PyQt4.QtGui import QMessageBox

absolute_path = os.path.dirname(os.path.abspath(__file__))
bound_rate_array = [115200, 9600, 57600, 230400, 460800, 921600]


# print (absolute_path)


def erase(port, bound_rate):
    erase_string = "sudo python " + absolute_path + "/esptool.py --port " + port + " --baud " + bound_rate + " erase_flash"
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
        bound_rate = str(self.boundRateComboBox.currentText())

        if len(port) > 0 and len(firmware_path) > 0:
            erase(port, bound_rate)
            flash(port, firmware_path)
        else:
            message_box = QtGui.QMessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setText("Some field are unselected")
            message_box.setWindowTitle("Error")
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()

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

        labelPort = QtGui.QLabel("Select shield connected Port")
        self.portComboBox = QtGui.QComboBox()
        for p in serial.tools.list_ports.comports():
            self.portComboBox.addItem("/dev/" + p.name)

        labelBoundRate = QtGui.QLabel("Select shield Bound Rate")  # TODO usare nella creazione della stringa
        self.boundRateComboBox = QtGui.QComboBox()
        for brate in bound_rate_array:
            self.boundRateComboBox.addItem(str(brate))

        grid.addWidget(labelPort, 0, 0)
        grid.addWidget(self.portComboBox, 0, 1, 1, 2)
        grid.addWidget(labelBoundRate, 1, 0)
        grid.addWidget(self.boundRateComboBox, 1, 1, 1, 2)
        grid.addWidget(self.pathTextEdit, 2, 0, 1, 2)
        grid.addLayout(v_box_select_firmware, 2, 2)
        grid.addLayout(v_box_flashing, 3, 0, 3, 0)

        c_widget.setLayout(grid)
        self.setCentralWidget(c_widget)


app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
