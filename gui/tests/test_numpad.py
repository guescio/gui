#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from mainwindow import MainWindow
from gui.numpad.numpad import NumPad
from PyQt5.QtCore import QCoreApplication

def test_createNumPad(qtbot):
    '''
    Test the creation of the NumPad instance
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    pad = NumPad(window)

    assert pad is not None


def checkCode():
    assert True


def test_codeNumPad(qtbot):
    '''
    Test the assignment and the comparison of the code
    '''

    assert qt_api.QApplication.instance() is not None
    esp32 = FakeESP32Serial(config)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)

    pad = NumPad(window)
    pad.assign_code("1234", checkCode())

    # Check that the code is correctly set
    assert pad.code == [1,2,3,4]

    # Try to set the code
    pad.input_number(4)
    pad.input_number(3)
    pad.input_number(2)
    pad.input_number(1)