import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class SettingWindow(Gtk.Window):

    def __init__(self, ownTitle):

        Gtk.Window.__init__(self, title = ownTitle)
        self.connect("destroy", lambda x: Gtk.main_quit())

        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.add(self.mainBox)
        
        self.mainGrid = Gtk.Grid()
        self.mainBox.pack_start(self.mainGrid, True, True, 0)

        self.setButton = Gtk.Button(label = "Set Values")
        self.mainBox.pack_start(self.setButton, True, True, 0)


