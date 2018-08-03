import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII/classes')
from gi.repository import Gtk, Gdk, GdkPixbuf
from setRangeWindow import SetRangeWindow
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from numpy import sin, cos, pi, linspace
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

        self.picSize = 200
        self.piczoom = GdkPixbuf.Pixbuf.new_from_file("figure_2.tif")
        self.piczoom2 = self.piczoom.scale_simple(100, 100, GdkPixbuf.InterpType.BILINEAR)
        self.picZoomed = Gtk.Image.new_from_pixbuf(self.piczoom2)#Gtk.Image.new_from_file("figure_1.tif")
        self.picZoomedBox.add(self.picZoomed)

        # Plot Window
        self.plotWin = newPlotWindow()
        self.plotWin.show_all()

        # Zoom stuff ???
        self.picOriginal = Gtk.Image()
        self.zoom = Gtk.GestureDrag.new(self.picOriginal)
        self.zoom.connect("begin", self.zoomEvent)
        
        
        
        
        
    ### CALL BACK FUNCTIONS ###
    def on_setRegionButton_clicked(self, widget):
        from setRegionWindow import SetRegionWindow
        setWindow = SetRegionWindow()
        setWindow.connect("destroy", lambda x: Gtk.main_quit())
        setWindow.show_all()
        Gtk.main()
        
    def set_picAtoms(self, filename):
        self.picAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, self.picSize, self.picSize, False)
        self.picAtoms = Gtk.Image.new_from_pixbuf(self.picAtoms)
        self.picGrid.attach(self.picAtoms, 0, 0, 1, 1)


    def set_picNoAtoms(self, filename):
        self.picNoAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, self.picSize, self.picSize, False)
        self.picNoAtoms = Gtk.Image.new_from_pixbuf(self.picNoAtoms)
        self.picGrid.attach(self.picNoAtoms, 1, 0, 1, 1)

    def set_picBkg(self, filename):
        self.picBkg = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, self.picSize, self.picSize, False)
        self.picBkg = Gtk.Image.new_from_pixbuf(self.picBkg)
        self.picGrid.attach(self.picBkg, 0, 1, 1, 1)

    def set_picOriginal(self, filename):
        self.picOriginal = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, self.picSize, self.picSize, False)
        self.picOriginal = Gtk.Image.new_from_pixbuf(self.picOriginal)
        self.picGrid.attach(self.picOriginal, 1, 1, 1, 1)
        self.zoom = Gtk.GestureLongPress.new(self.picOriginal)
        self.zoom.connect("pressed", self.zoomEvent)

    def zoomEvent(self, widget):
        print("Yaaaay")    
        



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
# win.set_picAtoms("figure_2.tif")
# win.set_picNoAtoms("figure_3.tif")
# win.set_picBkg("figure_4.tif")
# win.set_picOriginal("figure_5.tif")

win.set_picAtoms("manos_na_neve.png")
win.set_picNoAtoms("manos_na_neve.png")
win.set_picBkg("manos_na_neve.png")
win.set_picOriginal("manos_na_neve.png")
#win.set_resizable(False)


# n = 1000
# xsin = linspace(-pi, pi, n, endpoint=True)
# xcos = linspace(-pi, pi, n, endpoint=True)
# ysin = sin(xsin)
# ycos = cos(xcos)

# sinwave = win.plotWin.ax.plot(xsin, ysin, color='black', label='sin(x)')
# coswave = win.plotWin.ax.plot(xcos, ycos, color='black', label='cos(x)', linestyle='--')

# win.plotWin.ax.set_xlim(-pi,pi)
# win.plotWin.ax.set_ylim(-1.2,1.2)

# win.plotWin.ax.fill_between(xsin, 0, ysin, (ysin - 1) > -1, color='blue', alpha=.3)
# win.plotWin.ax.fill_between(xsin, 0, ysin, (ysin - 1) < -1, color='red',  alpha=.3)
# win.plotWin.ax.fill_between(xcos, 0, ycos, (ycos - 1) > -1, color='blue', alpha=.3)
# win.plotWin.ax.fill_between(xcos, 0, ycos, (ycos - 1) < -1, color='red',  alpha=.3)

# win.plotWin.ax.legend(loc='upper left')

# win.plotWin.ax = win.plotWin.fig.gca()
# win.plotWin.ax.spines['right'].set_color('none')
# win.plotWin.ax.spines['top'].set_color('none')
# win.plotWin.ax.xaxis.set_ticks_position('bottom')
# win.plotWin.ax.spines['bottom'].set_position(('data',0))
# win.plotWin.ax.yaxis.set_ticks_position('left')
# win.plotWin.ax.spines['left'].set_position(('data',0))
# win.plotWin.fig.tight_layout()

# win.plotWin.canvas = FigureCanvas(win.plotWin.fig)
# toolbar = NavigationToolbar(win.plotWin.canvas, win.plotWin)
# win.plotWin.plotBox.pack_start(toolbar, False, False, 0)

win.show_all()
Gtk.main()

