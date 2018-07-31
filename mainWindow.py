import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class mainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Main Window")

        ### Main Box ###
        self.mainBox = Gtk.Box(spacing=20)
        self.add(self.mainBox)

        ### Sub Boxes - Left ###
        self.leftBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        self.mainBox.add(self.leftBox)
        
        self.startButtonBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.startButtonBox)
        
        self.camSelectBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.camSelectBox)

        self.regionsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.regionsBox)

        self.infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.infoBox)

        

        self.button1 = Gtk.Button(label="START / STOP")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.startButtonBox.pack_start(self.button1, True, True, 0)
        
        self.camSelect = Gtk.Button(label="Cam Select")
        self.camSelectBox.pack_start(self.camSelect, True, True, 0)

        self.chooseROI = Gtk.Button(label="Choose ROI")
        self.regionsBox.pack_start(self.chooseROI, True, True, 0)

        self.chooseBkg = Gtk.Button(label="Choose Bkg.")
        self.regionsBox.pack_start(self.chooseBkg, True, True, 0)

        self.button2 = Gtk.Button(label="Stuff")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.mainBox.pack_start(self.button2, True, True, 0)

        

##############################
###         Buttons        ###
##############################

### Left Box ###
    def on_button1_clicked(self, widget):
        print("Hello")

    def on_button2_clicked(self, widget):
        print("Goodbye")

win = mainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
