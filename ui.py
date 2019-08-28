import sys
import random
import sqlite3
import time, datetime
import Xlib
import Xlib.display
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QListWidget, QScrollArea)
from PySide2.QtCore import Slot, Qt
from PySide2 import QtGui
import PySide2

import appthread

MACHINE = 'XPS13'


class TrackApp(QWidget):

    entries = []

    def __init__(self):

        self.thread = None

        QWidget.__init__(self)

        self.main_layout = QVBoxLayout()

        scroll_layout = QWidget()

        scroll = QScrollArea()
        scroll.setWidget(scroll_layout)
        scroll_container = QVBoxLayout()
        scroll_container.addWidget(scroll)
        # scroll.setWidgetResizable(True)

        tracking_layout = QVBoxLayout()

        tracking_button = QPushButton("Start Tracking")
        tracking_button.clicked.connect(self.start_track)
        
        tracking_text = QLabel("Hello World")
        tracking_text.setAlignment(Qt.AlignCenter)
        
        tracking_layout.addWidget(tracking_text)
        tracking_layout.addWidget(tracking_button)

        # self.main_layout.addChildLayout(scroll_container)
        self.main_layout.addWidget(tracking_text)
        self.main_layout.addWidget(tracking_button)
        self.setLayout(self.main_layout)
        self.setWindowTitle("UniTrack")
        

        

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
            self.button.setText('Start Tracking')
        else:
            self.thread = appthread.AppDetectThread(self.text, self.list)
            self.thread.start()
            self.button.setText('Stop Tracking')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = TrackApp()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
