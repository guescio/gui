#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
from mvm_basics import *
from PyQt5.QtCore import QCoreApplication

def test_basics(qtbot):
    '''
    Basic test that works more like a sanity check 
    to ensure we are setting up a QApplication properly
    '''
    assert qt_api.QApplication.instance() is not None

    widget = qt_api.QWidget()
    qtbot.addWidget(widget)
    widget.setWindowTitle("W1")
    widget.show()

    assert widget.isVisible()
    assert widget.windowTitle() == "W1"

from mainwindow import MainWindow

def test_menu(qtbot):
    '''
    Tests that the menu opens
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)

    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    assert window.bottombar.currentWidget() == window.menu

@pytest.mark.parametrize("code,expected", [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16), (5, 32), (6, 64), (7, 128), (31, 2147483648)])
def test_single_alarm(qtbot, code, expected):
    '''
    Tests that when there is an alarm, it is revealed by the get_alarms function
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)
    
    code = (1 << code)
    
    esp32.alarms_checkboxes[code].setChecked(True)
    esp32._compute_and_raise_alarms()
    
    assert esp32.get_alarms().number == expected
    
    assert QtWidgets.QApplication.activeWindow() != ""
    
    esp32.alarms_checkboxes[code].setChecked(False)
       
       
def test_not_alarm(qtbot):
    '''
    Tests the absence of alarms
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    qtbot.mouseClick(window.button_menu, QtCore.Qt.LeftButton)

    esp32._compute_and_raise_alarms()
    
    assert esp32.get_alarms().number == 0











