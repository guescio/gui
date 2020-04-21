#!/usr/bin/env python3

# from pytestqt import qt_compat
import pytest
import time
#from PyQt5.QtCore import QCoreApplication
import sys
import os
import os.path

import yaml

from communication.esp32serial import ESP32Serial
from communication.fake_esp32serial import FakeESP32Serial
from monitor.monitor import Monitor

from alarms.guialarms import GuiAlarms
from copy import copy

class NullSerial:
    pass


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    settings_file = os.path.join(base_dir, 'default_settings.yaml')
    with open(settings_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    #print('Config:', yaml.dump(config), sep='\n')
    nullserial = NullSerial
    monitor = Monitor("monitor",config,None)
    alarms = GuiAlarms(config,nullserial,monitor)
    
    #obs = copy(config["alarms"])
    #print('obs:', obs, sep='\n')

    
    observable = "battery_charge" 
    
    alarms.update_thresholds(observable, 10, 20)
    
    print(alarms._obs[observable]["setmin"])
    
