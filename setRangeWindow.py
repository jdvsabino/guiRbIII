import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII/classes')
# if __name__ == "__main__" and __package__ is None:
#     __package__ = "classes.settingWindow"

from gi.repository import Gtk, Gdk, GdkPixbuf
from classes.settingWindow import *


class SetRangeWindow(SettingWindow):

    def __init__(self):

        SettingWindow.__init__(self, "Set Range")

        self.maxLabel = Gtk.Label("Max.")
        self.mainGrid.attach(self.maxLabel, 0, 0, 1 ,1)
        self.maxEntry = Gtk.Entry()
        self.mainGrid.attach(self.maxEntry, 1, 0, 1 ,1)

        
        self.minLabel = Gtk.Label("Min.")
        self.mainGrid.attach(self.minLabel, 0, 1, 1 ,1)
        self.minEntry = Gtk.Entry()
        self.mainGrid.attach(self.minEntry, 1, 1, 1 ,1)
        

# win = SetRangeWindow()

# #print(dir(win.infoLabel))

# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()



