#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from gui.settings.mvmtoggle import MVMToggle


"""
TH07
"""
def test_paintEvent(qtbot):
    '''
    Test the method paintEvent of the class MVMToggle
    '''

    toggle = MVMToggle()
    toggle.setEnabled(False)
    toggle.setChecked(False)
    toggle.paintEvent(None)

    assert toggle.value() == 0
