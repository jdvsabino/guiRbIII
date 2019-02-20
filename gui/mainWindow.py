import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('../')
sys.path.append('./')
sys.path.append('./classes')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from gui.setRangeWindow import SetRangeWindow
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from numpy import sin, cos, pi, linspace, sqrt
from gui.plotWindow import *
from picture_generator import gen_canvas, gen_canvas_zoomed
from gui.classes.drawRectangle import *
from gui.classes.helpFunctions import *

class mainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Main Window")

        # Size settings
        self.width = 900
        self.height = 1000
        self.border = 10
        self.set_default_size(self.width, self.height)
        
        self.set_border_width(self.border)
        self.set_resizable(False)

        ### Main Box ###
        self.mainBoxSpacing = 20
        
        self.mainBox = Gtk.Box(spacing=self.mainBoxSpacing)
        self.add(self.mainBox)

        ### Sub Boxes - Left ###
        self.boxSpacing = 12
        self.buttonSpacing = 3
        self.leftBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.boxSpacing)
        self.mainBox.add(self.leftBox)
        
        self.buttonBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.buttonSpacing)
        self.leftBox.add(self.buttonBox)
        
        self.camSelectBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.buttonSpacing)
        self.leftBox.add(self.camSelectBox)

        self.regionsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.buttonSpacing)
        self.leftBox.add(self.regionsBox)

        self.infoBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.boxSpacing/2)
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

        self.chooseROI = Gtk.ToggleButton(label="Choose ROI")
        self.chooseROI.connect("toggled", self.set_ROI)
        self.regionsBox.pack_start(self.chooseROI, True, True, 0)

        self.chooseRBC = Gtk.ToggleButton(label="Choose Bkg.")
        self.chooseRBC.connect("toggled", self.set_RBC)
        self.regionsBox.pack_start(self.chooseRBC, True, True, 0)
        
        self.setManually = Gtk.Button(label="Set Manually")
        self.regionsBox.pack_start(self.setManually, True, True, 0)
        self.setManually.connect("clicked", self.on_setRegionButton_clicked)
        self.winControl = 0

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
        self.rightBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = self.boxSpacing)
        self.mainBox.add(self.rightBox)

        self.picZoomedBox = Gtk.Grid()#Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        # self.picZoomedBox.set_size_request(600, 300)
        self.rightBox.pack_start(self.picZoomedBox, True, True, 0)
        
        self.toolbarBox = Gtk.Box()
        self.rightBox.add(self.toolbarBox)

        self.picGrid = Gtk.Grid()
        self.picGrid.set_column_spacing(12)
        self.picGrid.set_row_spacing(12)
        self.rightBox.pack_end(self.picGrid, True, True, 0)
        #self.rightBox.set_center_widget(self.picGrid)



        self.picSize = [250, 160]
        self.first_time = 0



        ###---- Axes objects
        self.axes_abs       = []
        self.axes_abs_small = None
        self.axes_atoms     = None
        self.axes_no_atoms  = None
        self.axes_bkg       = None

        
        self.fig_abs       = Figure()
        self.fig_abs_small = Figure()
        self.fig_atoms     = Figure()
        self.fig_no_atoms  = Figure()        
        self.fig_bkg       = Figure()


        ###---- Canvas Objects
        self.canvasZoom      = FigureCanvas(self.fig_abs)
        self.canvasOriginal  = FigureCanvas(self.fig_abs_small)
        self.canvas_atoms    = FigureCanvas(self.fig_atoms)
        self.canvas_no_atoms = FigureCanvas(self.fig_no_atoms)
        self.canvas_bkg      = FigureCanvas(self.fig_bkg)


        ###--- Pack Canvas objects
        # Abs Pic
        self.canvasZoom.set_size_request(600, 500)
        self.picZoomedBox.attach(self.canvasZoom, 0,0,1,1)
        print(self.canvasZoom.get_child_visible())
        toolbar = NavigationToolbar(self.canvasZoom, self)            
        self.toolbarBox.pack_start(toolbar, False,False, 0)

        # Abs Pic small
        self.canvasOriginal.set_size_request(self.picSize[0], self.picSize[1])
        self.picGrid.attach(self.canvasOriginal, 1, 1, 1, 1)

        # Atom pic
        self.canvas_atoms.set_size_request(self.picSize[0], self.picSize[1])
        self.picGrid.attach(self.canvas_atoms, 0, 0, 1, 1)

        # No atom pic
        self.canvas_no_atoms.set_size_request(self.picSize[0], self.picSize[1])
        self.picGrid.attach(self.canvas_no_atoms, 1, 0, 1, 1)

        # Bkg pic
        self.canvas_bkg.set_size_request(self.picSize[0], self.picSize[1])
        self.picGrid.attach(self.canvas_bkg, 0, 1, 1, 1)

        # Rectangle for ROI and RBC
        self.rectangleROI = roiRectangle(1,1,1,1)
        self.rectangleRBC = rbcRectangle(1,1,2,2)
        self.regionControl = -1

        self.abs_pic = None
        
        # Plot Window
        self.plotWin = newPlotWindow()
        self.plotWin.show_all()


        self.update_pics_controll = 0
        GLib.timeout_add_seconds(0.5, self.update_pics)
        
        
        
        
        
    ### CALL BACK FUNCTIONS ###
    def on_setRegionButton_clicked(self, widget):
        from setRegionWindow import SetRegionWindow

        if self.winControl == 0:
            self.winControl = 1
            setWindow = SetRegionWindow()
            setWindow.connect("destroy", lambda x: Gtk.main_quit())
            setWindow.show_all()
            Gtk.main()
            self.winControl = 0
        

    def set_picZoomed(self, image = None, font=6, colormap="RdYlBu_r"):
        import matplotlib.gridspec as gridspec

    
        gs = gridspec.GridSpec(4, 4, hspace=0.2, wspace=0.2)
        img1 = image # mpimg.imread(filename)
        img2 = image[0] # self.abs_pic.integrate_x() # mpimg.imread("./atoms.tif")
        img3 = image[0] # self.abs_pic.integrate_y() # mpimg.imread("./noatoms.tif") 



            
        self.axes_abs = []
        self.axes_abs.append(self.fig_abs.add_subplot(gs[:-1, :-1]))
        self.axes_abs.append(self.fig_abs.add_subplot(gs[:-1, -1], xticklabels=[], sharey=self.axes_abs[0]))
        self.axes_abs.append(self.fig_abs.add_subplot(gs[-1, :-1], yticklabels=[], sharex=self.axes_abs[0]))

        self.axes_abs[0].imshow(img1, cmap=colormap, aspect="auto")
        self.axes_abs[0].xaxis.set_alpha(0.)
        self.axes_abs[0].xaxis.set_visible(False)
        self.axes_abs[0].yaxis.set_visible(False)    
        self.axes_abs[0].yaxis.set_alpha(0.)
        self.axes_abs[0].yaxis.set_ticks_position('right')
        self.axes_abs[0].tick_params(labelsize = font)

        ###---- COLORBAR: TODO
        # cbaxes = self.fig_abs.add_axes([0.02, 0.4, 0.02, 0.45])
        # cbaxes.yaxis.set_ticks_position('left')
        # cbar = self.fig_abs.colorbar(self.axes_abs[0], cax = cbaxes)
        self.axes_abs[1].set_yticklabels([])
        self.axes_abs[1].plot(img2)
        self.axes_abs[1].yaxis.set_ticks_position('right')
        self.axes_abs[1].xaxis.set_visible(False)
        #self.axes_abs[1].update()

        self.axes_abs[2].plot(img3)
        self.axes_abs[2].yaxis.set_visible(False)
        
        self.fig_abs.canvas.draw()
        self.canvasZoom.draw()

        
        
        
    def set_picAtoms(self, image = None, font = 6, colormap="RdYlBu_r", title="With atoms"):
        # self.picAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, self.picSize, self.picSize, False)
        # self.picAtoms = Gtk.Image.new_from_pixbuf(self.picAtoms)
        # self.picGrid.attach(self.picAtoms, 0, 0, 1, 1)
        #img = image # mpimg.imread(filename)
        #canvas = gen_canvas(img, title="With atoms",font=8)
        

        try:
            self.axes_atoms = self.fig_atoms.add_subplot(111)
            self.axes_atoms.cla()
            self.axes_atoms.imshow(self.abs_pic.atom_pic, cmap=colormap)
            
        except:
            print("INFO: Used argument as image.")
            self.axes_atoms = self.fig_atoms.add_subplot(111)
            self.axes_atoms.cla()
            self.axes_atoms.imshow(image, cmap=colormap)

        self.axes_atoms.set_title(title, fontsize=font)
        self.axes_atoms.tick_params(labelsize = font)
        self.fig_atoms.canvas.draw()
        self.canvas_atoms.draw()



    def set_picNoAtoms(self, image = None, font = 6, colormap="RdYlBu_r", title="Without atoms"):
        # self.picNoAtoms = GdkPixbuf.Pixbuf.new_from_file_at_scale(filename, self.picSize, self.picSize, False)
        # self.picNoAtoms = Gtk.Image.new_from_pixbuf(self.picNoAtoms)
        # self.picGrid.attach(self.picNoAtoms, 1, 0, 1, 1)
        # img = image # mpimg.imread(filename)
        # canvas = gen_canvas(img, title="Without Atoms",font=8)


        try:
            self.axes_no_atoms = self.fig_no_atoms.add_subplot(111)
            self.axes_no_atoms.imshow(self.abs_pic.no_atom_pic, cmap=colormap)
            
        except:
            print("INFO: Used argument as image.")
            self.axes_no_atoms = self.fig_no_atoms.add_subplot(111)
            self.axes_no_atoms.imshow(image, cmap=colormap)

        self.axes_no_atoms.set_title(title, fontsize=font)
        self.axes_no_atoms.tick_params(labelsize = font)
        self.fig_no_atoms.canvas.draw()
        self.canvas_no_atoms.draw()

        
    def set_picBkg(self, image = None, font = 6, colormap="RdYlBu_r", title = "Background"):
        #img = image # mpimg.imread(filename)
        #canvas = gen_canvas(img, title="Background", font=8)
        try:
            self.axes_bkg = self.fig_bkg.add_subplot(111)
            self.axes_bkg.imshow(self.abs_pic.bkg_pic, cmap=colormap)
            
        except:
            print("INFO: Used argument as image.")
            self.axes_bkg = self.fig_bkg.add_subplot(111)
            self.axes_bkg.imshow(image, cmap=colormap)

        self.axes_bkg.set_title(title, fontsize=font)
        self.axes_bkg.tick_params(labelsize = font)
        self.fig_bkg.canvas.draw()
        self.canvas_bkg.draw()

        

    def set_picOriginal(self, image = None, font = 6, colormap = "RdYlBu_r", title = "Abs. pic."):

        try:
            self.axes_abs_small = self.fig_abs_small.add_subplot(111)
            self.axes_abs_small.imshow(self.abs_pic.pic, cmap=colormap)
            
        except:
            print("INFO: Used argument as image.")
            self.axes_abs_small = self.fig_abs_small.add_subplot(111)
            self.axes_abs_small.imshow(image, cmap=colormap)

        self.axes_abs_small.set_title(title, fontsize=font)
        self.axes_abs_small.tick_params(labelsize = font)
        self.fig_abs_small.canvas.draw()
        self.canvasOriginal.draw()
        # self.canvasOriginal = gen_canvas(image, title="Absorption picture",font=8)
        

    def set_ROI(self, widget):
        # Here we make sure that the Toggle Buttons that set the ROI and RBC regions
        # are not activated at the same time.
        
        if self.chooseRBC.get_active() and self.chooseROI.get_active():
            self.chooseRBC.set_active(False)
            self.chooseROI.set_active(True)
            
        if self.chooseRBC.get_active() and not self.chooseROI.get_active():
            return 0

        if self.chooseROI.get_active():
            self.clearRegion(0)        
        
        
        motion_event_id = self.canvasOriginal.mpl_connect('motion_notify_event', self.updateCursorPosition)
        button_event_start_id = self.canvasOriginal.mpl_connect('button_press_event', self.zoomStart)
        button_event_end_id = self.canvasOriginal.mpl_connect('button_release_event', self.zoomEnd)
        
        if self.chooseROI.get_active():
            # Try to create a self.canvas
            print("Draw the ROI!")
            
        else:
            
            # replace_widget(self.picGrid.get_child_at(1,1), self.canvasOriginal)
            self.canvasOriginal.show()
            if motion_event_id != None:
                self.canvasOriginal.mpl_disconnect(motion_event_id)
            
            if button_event_start_id != None:
                self.canvasOriginal.mpl_disconnect(button_event_start_id)
            if button_event_end_id != None:
                self.canvasOriginal.mpl_disconnect(button_event_end_id)
        
    def set_RBC(self, widget):
        # Here we make sure that the Toggle Buttons that set the ROI and RBC regions
        # are not activated at the same time.

        if self.chooseROI.get_active() and self.chooseRBC.get_active():
            self.chooseROI.set_active(False)
            self.clearRegion(1)
            
        if self.chooseROI.get_active() and not self.chooseRBC.get_active():
            return 0

        if self.chooseRBC.get_active():
            self.clearRegion(1)

        
        motion_event_id = self.canvasOriginal.mpl_connect('motion_notify_event', self.updateCursorPosition)
        button_event_start_id = self.canvasOriginal.mpl_connect('button_press_event', self.zoomStart)
        button_event_end_id = self.canvasOriginal.mpl_connect('button_release_event', self.zoomEnd)

        if self.chooseRBC.get_active():
            # Try to create a self.canvas
            print("Draw the RBC!")
            
        else:
            # axes_temp = self.canvasOriginal.figure.axes[0]
            
            # rectangle = self.rectangleRBC.drawRectangle()
            # axes_temp.add_patch(rectangle)
            # print(rectangle)           
            # print("done! \n")
            
            # self.canvasOriginal.figure.axes[0] = axes_temp
            # self.canvasOriginal.flush_events()
            # self.canvasOriginal.draw_idle()
        
            # self.canvasOriginal.show()

            if motion_event_id != None:
                self.canvasOriginal.mpl_disconnect(motion_event_id)            
            if button_event_start_id != None:
                self.canvasOriginal.mpl_disconnect(button_event_start_id)
            if button_event_end_id != None:
                self.canvasOriginal.mpl_disconnect(button_event_end_id)
            
        
            
        
            
            
            


    def updateCursorPosition(self, event):
        '''When cursor inside plot, get position and print to statusbar'''

        
        if event.inaxes and self.rectangleROI.ID == -1:
            patches = self.canvasOriginal.figure.axes[0].patches
            if len(patches) > 5:
                patches = patches[-1:]
                self.canvasOriginal.figure.axes[0].patches = patches
            #self.rectangleROI.x_end = event.xdata
            #self.rectangleROI.y_end = event.ydata
            print("Coordinates:" + " x= " + str(round( event.xdata, 3)) + "  y= " + str(round( event.ydata, 3)))
            dx = event.xdata - self.rectangleROI.x_start
            dy = event.ydata - self.rectangleROI.y_start
            dist = sqrt(dx*dx + dy*dy)
            
            # #if dist >10:
            # self.rectangleROI.x_end = event.xdata
            # self.rectangleROI.y_end = event.ydata
            
            # self.rectangleROI.drawRectangle(alpha=0.1)
            # #print(self.canvasOriginal.figure.axes)
            # self.canvasOriginal.figure.axes[0].add_patch(self.rectangleROI.rectangle)
            # self.canvasOriginal.draw_idle()


            # self.canvasOriginal.figure.axes[0].patches = []
            # self.canvasOriginal.draw_idle()
            #print("Coordzoominates:" + " x= " + str(round( self.rectangleROI.x_end,3)) + "  y= " + str(round( self.rectangleROI.y_end,3)))
        
            # print("Left:  " + str(self.rectangleROI.x_start))
            # print("Up:    " + str(self.rectangleROI.y_start))
            # print("Down:  " + str(self.rectangleROI.x_end))
            # print("Right: " + str(self.rectangleROI.y_end))

    def updateRegion(self):

        if self.chooseROI.get_active() == True:
            axes = self.canvas.figure.axes[0]
            xlims = axes.get_xlim()
            ylims = axes.get_ylim()

            print(xlims)
            print(ylims)
            self.rectangleROI.x_start = xlims[0]
            self.rectangleROI.y_start = ylims[1]
            self.rectangleROI.x_end = xlims[1]
            self.rectangleROI.y_end = ylims[0]

            print("Left:  " + str(self.rectangleROI.x_start))
            print("Up:    " + str(self.rectangleROI.y_start))
            print("Down:  " + str(self.rectangleROI.y_end))
            print("Right: " + str(self.rectangleROI.x_end))
        
        
    def zoomStart(self, event):#, rectangle):
        '''When mouse is right-clicked on the canvas get the coordiantes and return them'''
        if event.button!=1: return
        if (event.xdata is None): return
        #x,y = event.xdata, event.ydata
        #self.canvasOriginal.fig.axes[0].clear()
        
        self.rectangleRBC.x_start = event.xdata
        self.rectangleRBC.y_start = event.ydata


        if self.chooseROI.get_active():
            self.rectangleROI.x_start = event.xdata
            self.rectangleROI.y_start = event.ydata
            self.rectangleROI.ID = -1
            print("Left:  " + str(self.rectangleROI.x_start))
            print("Up:    " + str(self.rectangleROI.y_start))
            print("Down:  " + str(self.rectangleROI.y_end))
            print("Right: " + str(self.rectangleROI.x_end))            
            print("ROI recangle drawn!")
            
            
        elif self.chooseRBC.get_active():
            self.rectangleRBC.x_end = event.xdata
            self.rectangleRBC.y_end = event.ydata
            self.rectangleRBC.ID = -1
            print("Left:  " + str(self.rectangleRBC.x_start))
            print("Up:    " + str(self.rectangleRBC.y_start))
            print("Down:  " + str(self.rectangleRBC.y_end))
            print("Right: " + str(self.rectangleRBC.x_end))
            print("RBC recangle drawn!")
            
        else:
            return False

        
    def zoomEnd(self, event):#, rectangle):
        '''When mouse is right-clicked on the canvas get the coordiantes and return them'''
        if event.button!=1: return
        if (event.xdata is None): return
        #x,y = event.xdata, event.ydata
#        self.canvasOriginal.figure.axes[0]        
        # else:
        if self.chooseROI.get_active():
            self.rectangleROI.ID = 0
            self.rectangleROI.x_end = event.xdata
            self.rectangleROI.y_end = event.ydata
            print("Left:  " + str(self.rectangleROI.x_start))
            print("Up:    " + str(self.rectangleROI.y_start))
            print("Down:  " + str(self.rectangleROI.y_end))
            print("Right: " + str(self.rectangleROI.x_end))
            #rect = self.rectangleROI.drawRectangle()
            #self.canvasOriginal.figure.axes[0].add_artist(rect)
            #self.canvasOriginal.figure.axes[0].draw_artist(rect)
            
            self.rectangleROI.drawRectangle()
            #print(self.canvasOriginal.figure.axes)
            self.canvasOriginal.figure.axes[0].add_patch(self.rectangleROI.rectangle)
            print(self.canvasOriginal.figure.axes[0].patches)
            #self.canvasOriginal.draw_idle()
            print("done! \n")
            
            #self.canvasOriginal.figure.axes[0] = axes_temp
            self.canvasOriginal.show_all()
            self.canvasOriginal.draw_idle()
            
            #self.canvasOriginal.draw()
            self.regionControl = 0

            self.abs_pic.set_ROI(rectangle = self.rectangleROI)

            ###--- plot the ROI
            up = int(self.rectangleROI.y_start)
            down = int(self.rectangleROI.y_end)
            left = int(self.rectangleROI.x_start)
            right = int(self.rectangleROI.x_end)
            self.set_picZoomed(self.abs_pic.pic[up:down, left:right])

            
            print("ROI recangle drawn!")
            self.chooseROI.set_active(False)
            
        elif self.chooseRBC.get_active():
            self.rectangleRBC.ID = 1
            self.rectangleRBC.x_end = event.xdata
            self.rectangleRBC.y_end = event.ydata
            print("Left:  " + str(self.rectangleRBC.x_start))
            print("Up:    " + str(self.rectangleRBC.y_start))
            print("Down:  " + str(self.rectangleRBC.y_end))
            print("Right: " + str(self.rectangleRBC.x_end))

            self.rectangleRBC.drawRectangle()
            #print(self.canvasOriginal.figure.axes)
            self.canvasOriginal.figure.axes[0].add_patch(self.rectangleRBC.rectangle)
            print(self.canvasOriginal.figure.axes[0].patches)
            #self.canvasOriginal.draw_idle()
            print("done! \n")
            
            #self.canvasOriginal.figure.axes[0] = axes_temp
            self.canvasOriginal.show_all()
            self.canvasOriginal.draw_idle()
            self.regionControl = 1

            self.abs_pic.set_RBC(rectangle = self.rectangleRBC)

            print("RBC recangle drawn!")
            self.chooseRBC.set_active(False)
        else:
            return False
    
    def clearRegion(self, region):
        
        if self.regionControl == -1:
            print("Nothing to clear.")
            return -1

        patches = self.canvasOriginal.figure.axes[0].patches

        
        if len(self.canvasOriginal.figure.axes[0].patches) == 1:
            if self.regionControl==region:
                patches = []
                self.regionControl = -1
                print("Emptied patches!")
        elif self.regionControl != region:
            del  patches[0]
            print("Cleared First!")
        else:
            del patches[1]
            print("Cleared second!")

        self.canvasOriginal.figure.axes[0].patches = patches
        self.canvasOriginal.draw_idle()

    def update_pics(self):
        if self.update_pics_controll:
            self.set_picOriginal()
            self.set_picAtoms()
            self.set_picNoAtoms()
            self.set_picBkg()
            self.update_pics_controll = 0
            return True
            
        else:
            return True
            

        

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



        
#win = mainWindow()

#print(dir(win.infoLabel))

# win.connect("destroy", Gtk.main_quit)

# win.set_picZoomed("/home/colin/Dropbox/GUI_RbIII/manos_na_neve.png")
# win.set_picAtoms("./atoms.tif")
# win.set_picNoAtoms("./noatoms.tif")
# win.set_picBkg("./atoms.tif")
# win.set_picOriginal("./noatoms.tif")


# picpic = win.picGrid.get_child_at(1,1)
# picpic.mpl_connect('motion_notify_event', win.updateCursorPosition)
# picpic.mpl_connect('button_press_event', win.updateZoom)
# win.set_resizable(False)


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

#win.show_all()
#Gtk.main()

