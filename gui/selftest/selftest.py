#!/usr/bin/env python3
'''
This module implements the self-test procedure and its user wizard.
'''

import os
from PyQt5 import QtWidgets, uic


class SelfTest(QtWidgets.QWidget):
    '''
    SelfTest widget. User guidance through the procedure.
    '''
    def __init__(self, *args):
        """
        Constructor. Initializes the SelfTest widget.
        """

        super(SelfTest, self).__init__(*args)
        uifile = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            "selftest.ui")

        uic.loadUi(uifile, self)

