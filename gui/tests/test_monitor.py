#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from .mvm_basics import *
from gui.monitor.monitor import Monitor
from gui.mainwindow import MainWindow
from PyQt5.QtCore import QCoreApplication

"""
TH13
"""
def test_monitorSizeMod(qtbot):
    '''
    Test the start of the PCV Mode, and then in PSV Mode
    '''

    assert qt_api.QApplication.instance() is not None

    esp32 = FakeESP32Serial(config)
    qtbot.addWidget(esp32)
    window = MainWindow(config, esp32)
    qtbot.addWidget(window)
    monitor = Monitor("Insp. Press.", config)
    qtbot.addWidget(monitor)

    assert monitor.configname == "Insp. Press."

    monitor.handle_resize(None)
    monitor.highlight()
    value = monitor.value
    monitor.update_value(10)

    assert monitor.value == 10
    monitor.value = value

