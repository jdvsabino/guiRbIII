import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from .settingWindow import SettingWindow



class SetRangeWindow(settingWindow):

    def __init__(self):

        settingWindow.__init__(self, "Set Range")

        self.maxLabel = Gtk.Label("Max.")
        self.mainGrid.attach(self.mainLabel, 0, 0, 1 ,1)
        self.maxEntry = Gtk.Entry()
        self.mainGrid.attach(self.maxEntry, 1, 0, 1 ,1)

        
        self.minLabel = Gtk.Label("Min.")
        self.mainGrid.attach(self.minLabel, 0, 1, 1 ,1)
        self.minEntry = Gtk.Entry()
        self.mainGrid.attach(self.minEntry, 1, 0, 1 ,1)
        

win = setRangeWindow()

#print(dir(win.infoLabel))

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
        
