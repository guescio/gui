#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from gui.data_handler import DataHandler
from PyQt5.QtCore import QCoreApplication

def test_objectCreation(qtbot):
    '''
    Test the creation of the DataHandler instance with name and units
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    handler = DataHandler(config, esp32, None, None)

    assert handler is not None


def test_communicationErrors(qtbot):
    '''
    Test the communication error
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    handler = DataHandler(config, esp32, None, None)

    def handle_dialog():
        handler.open_comm_error("Test")
        messagebox = window.findChild(QtWidgets.QMessageBox)
        qtbot.addWidget(messagebox)
        assert "Test" in messagebox.text
        button = messagebox.button(QtWidgets.QMessageBox.Abort)
        qtbot.mouseClick(button, QtCore.Qt.LeftButton, delay=1)

    QtCore.QTimer.singleShot(100, handle_dialog)

    assert handler is not None
