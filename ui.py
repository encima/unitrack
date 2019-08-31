import sys
import random
import sqlite3
import time, datetime
import Xlib
import Xlib.display
from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QListWidget, QScrollArea)
from PySide2.QtCore import Slot, Qt
import PySide2

import appthread

MACHINE = 'XPS13'


class TrackApp(QWidget):

    entries = []

    def __init__(self):

        super(TrackApp, self).__init__()

        self.initUI()
        self.thread = None

    def initUI(self):

        appLbl = QtWidgets.QLabel('App')
        durationLbl = QtWidgets.QLabel('Duration')
        actionLbl = QtWidgets.QLabel('Action')

        self.appEdit = QtWidgets.QLabel()
        durationEdit = QtWidgets.QLabel()
        actionEdit = QtWidgets.QTextEdit()

        self.trackBtn = QtWidgets.QPushButton("Start Tracking")
        self.trackBtn.clicked.connect(self.start_track)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(appLbl, 1, 0)
        self.grid.addWidget(self.appEdit,1,1)

        self.grid.addWidget(durationLbl,2,0)
        self.grid.addWidget(durationEdit,2,1)

        self.grid.addWidget(actionLbl,3,0)
        self.grid.addWidget(actionEdit,3,1)

        self.grid.addWidget(self.trackBtn,4,0)

        self.setLayout(self.grid)
        self.setGeometry(800,500, 400, 400)
        self.setWindowTitle('UniTrack')
        self.show()

    @Slot()
    def get_app(self):
        disp = Xlib.display.Display()
        NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')
        NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
        root = disp.screen().root
        root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
        try:
            window_id = root.get_full_property(
                NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
            window = disp.create_resource_object('window', window_id)
            window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
            window_name = window.get_full_property(NET_WM_NAME, 0).value
            self.text.setText(window_name)
        except Xlib.error.XError:  # simplify dealing with BadWindow
            window_name = None
            self.text.setText("No Window Found")

    @Slot()
    def start_track(self):
        if self.thread:
            self.thread.online = False
            self.thread = None
            self.trackBtn.setText('Start Tracking')
        else:
            self.thread = appthread.AppDetectThread(self.appEdit, self.entries)
            self.thread.start()
            self.trackBtn.setText('Stop Tracking')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TrackApp()
    sys.exit(app.exec_())
