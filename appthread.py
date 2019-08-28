import time
import threading
import time, datetime, sqlite3
import Xlib
import Xlib.display
from threading import Thread

MACHINE = 'XPS13'

class AppDetectThread(Thread):
    def __init__(self, text_box):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.text = text_box
        self.online = True

        self.setup_db()
        self.setup()


    def setup(self):
        self.sqlite_insert_with_param = """INSERT INTO 'tracks'('date', 'machine', 'application') VALUES (?, ?, ?);"""
        self.disp = Xlib.display.Display()
        self.root = self.disp.screen().root

        self.last_entry = None

        self.NET_WM_NAME = self.disp.intern_atom('_NET_WM_NAME')
        self.NET_ACTIVE_WINDOW = self.disp.intern_atom('_NET_ACTIVE_WINDOW')

    def setup_db(self):
        self.db_conn = sqlite3.connect('tracker.db')
        self.db_cursor = self.db_conn.cursor()

        # Create table
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS tracks
                            (date timestamp, machine text, application text)''')
        self.db_conn.commit()
 
    def get_app_constant(self):
        self.root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
        try:
            window_id = self.root.get_full_property(
                self.NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
            window = self.disp.create_resource_object('window', window_id)
            window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
            window_name = window.get_full_property(self.NET_WM_NAME, 0).value
        except Xlib.error.XError:  # simplify dealing with BadWindow
            window_name = None
        print(window_name, self.last_entry)
        if window_name != self.last_entry and self.last_entry is not None and self.last_entry is not 'Tracker':
            data_tuple = (datetime.datetime.now(), MACHINE, str(window_name))
            self.db_cursor.execute(self.sqlite_insert_with_param, data_tuple)
            self.db_conn.commit()
        last_entry = window_name
        event = self.disp.next_event()
        return window_name
 
    def run(self):
        i = 0
        while self.online:
            window_name = self.get_app_constant()
            self.text.setText("{}".format(window_name))
            i += 2
            time.sleep(5)

