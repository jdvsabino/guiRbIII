import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII/classes')
from gi.repository import Gtk, Gdk, GdkPixbuf
from classes.settingWindow import *


class SetRangeWindow(SettingWindow):
    '''
	Sets the definition for the window that pops up
	when the user sets the limits of the on-line plot.
    '''

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

        self.connect("destroy", self.on_destroy)

        self.show_all()

    def on_destroy(self, widget):
        widget.hide()
