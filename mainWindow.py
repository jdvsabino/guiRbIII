import gi
import sys
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from plotWindow import *

class mainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Main Window")

        # Size settings
        self.set_default_size(750, 1000)
        print(self.get_size())
        self.set_border_width(10)
        #self.set_resizable(False)
        ### Main Box ###
        self.mainBox = Gtk.Box(spacing=20)
        self.add(self.mainBox)

        ### Sub Boxes - Left ###
        self.leftBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        self.mainBox.add(self.leftBox)
        
        self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.buttonBox)
        
        self.camSelectBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.camSelectBox)

        self.regionsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.leftBox.add(self.regionsBox)

        self.infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        self.leftBox.add(self.infoBox)

        
        ### Buttons, labels and boxes - Left ###
        self.startButton = Gtk.ToggleButton(label="START")
        self.startButton.connect("toggled", self.on_startButton_clicked)
        self.buttonBox.pack_start(self.startButton, True, True, 0)
        
        self.camSelect = Gtk.ComboBoxText()
        self.camSelect.set_entry_text_column(0)
        self.camSelect.connect("changed", self.on_camSelect_changed)
        self.camSelect.append_text("TAndor")
        self.camSelect.append_text("LAndor")
        self.camSelect.append_text("VAndor")
        self.camSelect.append_text("Auto")
        self.camSelectBox.pack_start(self.camSelect, True, True, 0)

        self.chooseROI = Gtk.Button(label="Choose ROI")
        self.regionsBox.pack_start(self.chooseROI, True, True, 0)

        self.chooseBkg = Gtk.Button(label="Choose Bkg.")
        self.regionsBox.pack_start(self.chooseBkg, True, True, 0)
        
        self.setManually = Gtk.Button(label="Set Manually")
        self.regionsBox.pack_start(self.setManually, True, True, 0)
        self.setManually.connect("clicked", self.on_setRegionButton_clicked)

        self.infoNetwork = Gtk.Label("Network v0.0")
        self.infoBox.add(self.infoNetwork)

        self.infoStatus = Gtk.Label("Adwin Status\n")
        self.infoBox.add(self.infoStatus)
        
        self.infoGlobalCounts = Gtk.Label("Global counts: ")
        self.infoBox.add(self.infoGlobalCounts)

        self.infoPicNum = Gtk.Label("Picture number: ")
        self.infoBox.add(self.infoPicNum)        

        self.infoScanNum = Gtk.Label("Scan number: ")
        self.infoBox.add(self.infoScanNum)        


        ### Sub Boxes - Right ###
        self.rightBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        self.mainBox.add(self.rightBox)

        self.picZoomedBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        self.rightBox.add(self.picZoomedBox)

        self.picGrid = Gtk.Grid()
        self.picGrid.set_column_spacing(3)
        self.picGrid.set_row_spacing(3)
        self.rightBox.add(self.picGrid)

        #pixbuf = GdkPixbuf.gdk_pixbuf_new_from_file("figure_1.png")

        self.piczoom = GdkPixbuf.Pixbuf.new_from_file("figure_2.tif")
        self.piczoom2 = self.piczoom.scale_simple(100, 100, GdkPixbuf.InterpType.BILINEAR)
        self.picZoomed = Gtk.Image.new_from_pixbuf(self.piczoom2)#Gtk.Image.new_from_file("figure_1.tif")
        self.picZoomedBox.add(self.picZoomed)

        self.picAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale("figure_2.tif", 300, 300, False)
        self.picAtoms = Gtk.Image.new_from_pixbuf(self.picAtoms)
        self.picGrid.attach(self.picAtoms, 0, 0, 1, 1)

        self.picNoAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale("figure_3.tif",300,300, False)
        self.picNoAtoms = Gtk.Image.new_from_pixbuf(self.picNoAtoms)
        self.picGrid.attach(self.picNoAtoms, 1, 0, 1, 1)

        self.picBkg = GdkPixbuf.Pixbuf.new_from_file_at_scale("figure_4.tif",300,300, False)
        self.picBkg = Gtk.Image.new_from_pixbuf(self.picBkg)
        self.picGrid.attach(self.picBkg, 0, 1, 1, 1)

        self.picOriginal = GdkPixbuf.Pixbuf.new_from_file_at_scale("figure_5.tif",300,300, False)
        self.picOriginal = Gtk.Image.new_from_pixbuf(self.picOriginal)
        self.picGrid.attach(self.picOriginal, 1, 1, 1, 1)  


        # Plot Window
        self.plotWin = plotWindow()
        self.plotWin.show_all()
    ### CALL BACK FUNCTIONS ###
    def on_setRegionButton_clicked(self, widget):
        from setRegionWindow import SetRegionWindow
        setWindow = SetRegionWindow()
        setWindow.connect("destroy", lambda x: Gtk.main_quit())
        setWindow.show_all()
        Gtk.main()
        
    def set_picAtoms(self, filename):
        self.picAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, 300, 300, True)
        self.picAtoms = Gtk.Image.new_from_pixbuf(self.picAtoms)
        self.picGrid.attach(self.picAtoms, 0, 0, 1, 1)

##############################
###         Buttons        ###
##############################

### Left Box ###
    def on_startButton_clicked(self, widget):
        print(self.startButton.get_active())
        if self.startButton.get_active():
            self.startButton.set_label("STOP")
        else:
            self.startButton.set_label("START")
        print("Hello")

    def on_camSelect_changed(self, widget):

        if widget.get_active_text is "Auto":
            print("Camera will be selected automatically.")
        else:
            print(widget.get_active_text() + " is active!")

win = mainWindow()

#print(dir(win.infoLabel))

win.connect("destroy", Gtk.main_quit)
#win.set_resizable(False)
win.show_all()
Gtk.main()
