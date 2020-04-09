#!/usr/bin/env python3
from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui, QtCore

def clickable(widget):
    class Filter(QtCore.QObject):
        clicked = QtCore.pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class Alarms(QtWidgets.QWidget):
    def __init__(self, *args):
        """
        Initialize the Alarms widget.

        Grabs child widgets.
        """
        super(Alarms, self).__init__(*args)
        uic.loadUi("alarms/alarms.ui", self)

        self.layout          = self.findChild(QtWidgets.QGridLayout, "monitors_layout")

        self.slider_alarmmin = self.findChild(QtWidgets.QScrollBar,  "slider_alarmmin")
        self.alarmmin_min    = self.findChild(QtWidgets.QLabel,      "alarmmin_min")
        self.alarmmin_value  = self.findChild(QtWidgets.QLabel,      "alarmmin_value")
        self.alarmmin_max    = self.findChild(QtWidgets.QLabel,      "alarmmin_max")

        self.slider_alarmmax = self.findChild(QtWidgets.QScrollBar,  "slider_alarmmax")
        self.alarmmax_min    = self.findChild(QtWidgets.QLabel,      "alarmmax_min")
        self.alarmmax_value  = self.findChild(QtWidgets.QLabel,      "alarmmax_value")
        self.alarmmax_max    = self.findChild(QtWidgets.QLabel,      "alarmmax_max")

    def connect_monitors_and_plots(self, mainparent):
        self.mainparent = mainparent
        self.monitors = mainparent.monitors
        self.monitor_slots = mainparent.monitor_slots
        self.plots = mainparent.plots
        self.plot_slots = mainparent.plot_slots
        self.plot_hidden_slots = mainparent.plot_hidden_slots

        # connect monitors to selection and alarm clearing slots
        for name in self.monitors:
            monitor = self.monitors[name]
            clickable(monitor).connect(lambda n=name: self.select_monitor(n))

    def select_monitor(self, selected):
        for name in self.monitors:
            monitor = self.monitors[name]
            if name == selected:
                self.selected = name
                monitor.clear_alarm()
                # Show configuration and highlight monitor
                if monitor.config_mode:
                    monitor.highlight()
                    self.show_settings(name)
            elif monitor.config_mode:
                monitor.unhighlight()

    def unhighlight_monitors(self):
        for name in self.monitors:
            self.monitors[name].unhighlight()

    def set_slider_range(self, slider, monitor):
        slider.setMinimum(0)
        slider.setMaximum((monitor.maximum - monitor.minimum) / monitor.step)
        slider.setSingleStep(monitor.step)

    def do_alarmmin_moved(self, slidervalue, monitor):
        value = slidervalue * monitor.step + monitor.minimum
        self.alarmmin_value.setText("Alarm min: " + str(value))

    def do_alarmmax_moved(self, slidervalue, monitor):
        value = slidervalue * monitor.step + monitor.minimum
        self.alarmmax_value.setText("Alarm max: " + str(value))

    def show_settings(self, name):
        monitor = self.monitors[name]

        self.alarmmin_min.setText(str(monitor.minimum))
        self.alarmmin_max.setText(str(monitor.maximum))
        self.set_slider_range(self.slider_alarmmin, monitor)
        self.slider_alarmmin.valueChanged.connect(lambda value:
                self.do_alarmmin_moved(value, monitor))
        sliderpos = int((monitor.set_minimum - monitor.minimum) / monitor.step)
        self.slider_alarmmin.setSliderPosition(sliderpos)

        self.alarmmax_min.setText(str(monitor.minimum))
        self.alarmmax_max.setText(str(monitor.maximum))
        self.set_slider_range(self.slider_alarmmax, monitor)
        self.slider_alarmmax.valueChanged.connect(lambda value:
                self.do_alarmmax_moved(value, monitor))
        sliderpos = int((monitor.set_maximum - monitor.minimum) / monitor.step)
        self.slider_alarmmax.setSliderPosition(sliderpos)

    def apply_selected(self):
        print(self.selected)

    def reset_selected(self):
        self.show_settings(self.selected)

    def display_selected(self, slotname):
        print(self.selected + " to " + slotname)
        self.populate_monitors_and_plots()

    def populate_monitors_and_plots(self):
        # Get all active plots and monitors and put the remaining monitors on the alarms page
        self.active_plots = []
        self.active_monitors = []
        for (i, name) in enumerate(self.monitors):
            monitor = self.monitors[name]
            plot = self.plots[name]
            self.layout.addWidget(monitor, int(i % 3), 10-int(i / 3)) 
            self.plot_hidden_slots.addWidget(plot, i)
            for (mon_slotname, plot_slotname) in zip(self.monitor_slots, self.plot_slots):
                monitor_slot = self.monitor_slots[mon_slotname]
                if monitor.location == mon_slotname:
                    self.monitor_slots[mon_slotname].addWidget(monitor, 0, 0)
                    self.plot_slots[plot_slotname].addWidget(plot, 0, 0)
                    self.active_monitors.append(monitor)
                    self.active_plots.append(plot)
                    break

        return (self.active_monitors, self.active_plots)

    def config_monitors(self):
        for name in self.monitors:
            self.monitors[name].config_mode = True
            self.selected = name
        self.select_monitor(self.selected)

    def deconfig_monitors(self):
        for name in self.monitors:
            self.monitors[name].config_mode = False


