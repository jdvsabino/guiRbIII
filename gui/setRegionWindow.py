import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('../')
sys.path.append('./classes')
from gi.repository import Gtk, Gdk, GdkPixbuf
from classes.settingWindow import *


class SetRegionWindow(SettingWindow):
    '''
       Sets the definitions for the window that pops up
       when the user chooses the limits of ROI and RBC
       manually.
    '''
    def __init__(self):

        SettingWindow.__init__(self, "Set Region")

        # Here we choose the position of the label "Up" and set everything
        # relatively to it. 
        posUpLabel_col = 0
        posUpLabel_row = 1

        # We create and position the labels
        # Label Creation
        self.upLabel = Gtk.Label("Up")
        self.downLabel = Gtk.Label("Down")
        self.leftLabel = Gtk.Label("Left")
        self.rightLabel = Gtk.Label("Right")
        self.roiLabel = Gtk.Label("ROI")
        self.rbcLabel = Gtk.Label("RBC")

        self.mainGrid.attach(self.upLabel, posUpLabel_col, posUpLabel_row, 1 ,1)
        self.mainGrid.attach(self.downLabel, posUpLabel_col, posUpLabel_row + 1, 1 ,1)
        self.mainGrid.attach(self.leftLabel, posUpLabel_col, posUpLabel_row + 2, 1 ,1)
        self.mainGrid.attach(self.rightLabel, posUpLabel_col, posUpLabel_row + 3, 1 ,1)
        self.mainGrid.attach(self.roiLabel, posUpLabel_col + 1, posUpLabel_row -1, 1 ,1)
        self.mainGrid.attach(self.rbcLabel, posUpLabel_col + 2, posUpLabel_row -1, 1 ,1)

        # Now the entries are created and positioned
        # For ROI
        self.upEntry_roi = Gtk.Entry()
        self.downEntry_roi = Gtk.Entry()
        self.leftEntry_roi = Gtk.Entry()
        self.rightEntry_roi = Gtk.Entry()
        
        self.mainGrid.attach(self.upEntry_roi, posUpLabel_col + 1, posUpLabel_row, 1 ,1)
        self.mainGrid.attach(self.downEntry_roi, posUpLabel_col + 1, posUpLabel_row + 1, 1 ,1)
        self.mainGrid.attach(self.leftEntry_roi, posUpLabel_col + 1, posUpLabel_row + 2, 1 ,1)
        self.mainGrid.attach(self.rightEntry_roi, posUpLabel_col + 1, posUpLabel_row + 3, 1 ,1)

        # For RBC
        self.upEntry_rbc = Gtk.Entry()
        self.downEntry_rbc = Gtk.Entry()
        self.leftEntry_rbc = Gtk.Entry()
        self.rightEntry_rbc = Gtk.Entry()
        
        self.mainGrid.attach(self.upEntry_rbc, posUpLabel_col + 2, posUpLabel_row, 1 ,1)
        self.mainGrid.attach(self.downEntry_rbc, posUpLabel_col + 2, posUpLabel_row + 1, 1 ,1)
        self.mainGrid.attach(self.leftEntry_rbc, posUpLabel_col + 2, posUpLabel_row + 2, 1 ,1)
        self.mainGrid.attach(self.rightEntry_rbc, posUpLabel_col + 2, posUpLabel_row + 3, 1 ,1)
