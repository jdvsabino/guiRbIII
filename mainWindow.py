import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf


class mainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Main Window")
        self.set_border_width(10)
        
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
        
        self.picZoomed = Gtk.Image.new_from_file("figure_1.png")
        self.picZoomedBox.add(self.picZoomed)

        self.picAtoms = Gtk.Image.new_from_file("figure_2.png")
        self.picGrid.attach(self.picAtoms, 0, 0, 1, 1)

        self.picNoAtoms = Gtk.Image.new_from_file("figure_3.png")
        self.picGrid.attach(self.picNoAtoms, 1, 0, 1, 1)

        self.picBkg = Gtk.Image.new_from_file("figure_4.png")
        self.picGrid.attach(self.picBkg, 0, 1, 1, 1)

        self.picOriginal = Gtk.Image.new_from_file("figure_5.png")
        self.picGrid.attach(self.picOriginal, 1, 1, 1, 1)  
        
    ### CALL BACK FUNCTIONS ###
    def on_setRegionButton_clicked(self, widget):
        from setRegionWindow import SetRegionWindow
        setWindow = SetRegionWindow()
        setWindow.show_all()
        Gtk.main()
        
        

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
win.show_all()
Gtk.main()
