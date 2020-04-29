#!/usr/bin/env python3

# from pytestqt import qt_compat
from pytestqt.qt_compat import qt_api
import pytest
import time
from communication.peep import PEEP


"""
TH11
"""
def test_peepReset(qtbot):
    '''
    Test the reset of the Peep
    '''

    p = PEEP()

    # Set a negative value for the t5 parameter, so the time t is obiously greater than t5
    t5 = p.phase_start["restart"]
    p.phase_start["restart"] = -1
    t0 = p.t_cycle_start

    # Force the flow
    p.flow()

    assert p.t_cycle_start != t0

    p.phase_start["restart"] = phase_start["restart"]
