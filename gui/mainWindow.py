import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('../')
sys.path.append('../network')
sys.path.append('./')
sys.path.append('./classes')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from gui.setRangeWindow import SetRangeWindow
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from numpy import sin, cos, pi, linspace, sqrt, zeros, int32, array
from gui.plotWindow import *
from picture_generator import gen_canvas, gen_canvas_zoomed
from gui.classes.drawRectangle import *
from gui.classes.helpFunctions import *
from gui.classes.ticker_locator import MyLocator
from network.data_collection import data_collector as dc
import copy

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

        self.label_network = "Network v0.0"
        self.infoNetwork   = Gtk.Label(self.label_network)
        self.infoBox.add(self.infoNetwork)

        self.label_status = "Adwin Status\n"
        self.infoStatus   = Gtk.Label(self.label_status)
        self.infoBox.add(self.infoStatus)

        self.label_global = "Global\n counts: "
        self.infoGlobalCounts = Gtk.Label(self.label_global)
        self.infoBox.add(self.infoGlobalCounts)

        self.label_picnum = "Picture number: "
        self.infoPicNum = Gtk.Label(self.label_picnum)
        self.infoBox.add(self.infoPicNum)        

        self.label_scan = "Scan\n number: "
        self.infoScanNum = Gtk.Label(self.label_scan)
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
        self.cbaxes         = None 

        ###---- Figure Objects
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


        try:

            up    = int(self.abs_pic.ROI[0])
            down  = int(self.abs_pic.ROI[1])
            left  = int(self.abs_pic.ROI[2])
            right = int(self.abs_pic.ROI[3])
            
            print("**** SETTING ZOOM PIC ****")
            print("ROI: " + str(self.abs_pic.ROI))
            
            img1 = self.abs_pic.pic[up:down, left:right]
            img2 = self.abs_pic.integrate_y()
            img3 = self.abs_pic.integrate_x()


            ###---- Cleans axes
            for ax in self.axes_abs:
                ax.remove()

            try:
                self.cbaxes.remove()
            except:
                print("Non-existent colorbar!")
            
            print("**** DONE ****")
            
        except Exception as e:
            print("Didn't work:")
            print(e)
            img1 = image 
            img2 = image[0]
            img3 = image[0]

        
        self.axes_abs = []
        self.axes_abs.append(self.fig_abs.add_subplot(gs[:-1, :-1]))
        self.axes_abs.append(self.fig_abs.add_subplot(gs[:-1, -1], xticklabels=[], sharey=self.axes_abs[0]))
        self.axes_abs.append(self.fig_abs.add_subplot(gs[-1, :-1], yticklabels=[], sharex=self.axes_abs[0]))


        cset = self.axes_abs[0].imshow(img1, cmap=colormap)#, aspect="auto")
        self.axes_abs[0].xaxis.set_alpha(0.)
        self.axes_abs[0].xaxis.set_visible(False)
        self.axes_abs[0].yaxis.set_visible(False)    
        self.axes_abs[0].yaxis.set_alpha(0.)
        self.axes_abs[0].yaxis.set_ticks_position('right')
        self.axes_abs[0].tick_params(labelsize = font)


        ###---- COLORBAR
        # TODO:
        #      - Correct colorbar scale
        #
        self.cbaxes = self.fig_abs.add_axes([0.02, 0.4, 0.02, 0.45])
        self.cbaxes.yaxis.set_ticks_position('left')
        cbar = self.fig_abs.colorbar(cset, cax=self.cbaxes)


        ###---- AXES
        # TODO:
        #      - Adjust size properly
        #
        pos_ref = self.axes_abs[0].get_position()
        #aspect_ratio = self.picSize[0]/4/position.height

        self.axes_abs[1].set_yticklabels([])
        self.axes_abs[1].invert_xaxis()
        self.axes_abs[1].plot(img2.T, linspace(0, len(img2)-1, len(img2), dtype=int32), 'r', linewidth=1.)
        self.axes_abs[1].set_aspect("equal")

        # left   = self.axes_abs[1].get_position().bounds[0]
        # right  = self.axes_abs[1].get_position().bounds[1]
        # width  = self.axes_abs[0].get_position().height
        # height = self.axes_abs[1].get_position().height        
        # self.axes_abs[1].set_position(Bbox(array([[left, right], [width, height]])))
        self.axes_abs[1].yaxis.set_ticks_position('right')
        self.axes_abs[1].xaxis.set_visible(False)
        self.axes_abs[1].set_aspect("equal", adjustable="box", anchor="C")                

        #self.axes_abs[2].set_major_locator(ML)
        #aspect_ratio = position.width/self.picSize[0]/4

        self.axes_abs[2].plot(img3,'r', linewidth=1.)
        self.axes_abs[2].set_aspect("equal", adjustable="box", anchor="C")        
        # left   = self.axes_abs[2].get_position().bounds[0]
        # right  = self.axes_abs[2].get_position().bounds[1]
        # width  = self.axes_abs[0].get_position().width
        # height = self.axes_abs[2].get_position().height                
        # self.axes_abs[2].set_position(Bbox(array([[left, right], [width, height]])))
        self.axes_abs[2].yaxis.set_visible(False)


        self.fig_abs.canvas.draw()
        self.canvasZoom.draw()

        
        
        
    def set_picAtoms(self, image = None, font = 6, colormap="RdYlBu_r", title="With atoms"):        

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

        try:
            self.axes_bkg = self.fig_bkg.add_subplot(111)
            self.axes_bkg.imshow(self.abs_pic.bkg_pic, cmap=colormap)
            
        except:
            print("INFO: Used argument as image.")
            image = zeros((256, 256)) ### TESTING
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
    
    
    def set_ROI(self, widget):
        # IS THIS FUNTION NECESSARY?
        ###---- ROI and RBC buttons are not used at the same time
        if self.chooseRBC.get_active() and self.chooseROI.get_active():
            self.chooseRBC.set_active(False)
            self.chooseROI.set_active(True)
            
        if self.chooseRBC.get_active() and not self.chooseROI.get_active():
            return 0

        if self.chooseROI.get_active():
            self.clearRegion(0)        
        

        ###---- Events are connected to the plot object
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
            
            if motion_event_id != None:
                self.canvasOriginal.mpl_disconnect(motion_event_id)            
            if button_event_start_id != None:
                self.canvasOriginal.mpl_disconnect(button_event_start_id)
            if button_event_end_id != None:
                self.canvasOriginal.mpl_disconnect(button_event_end_id)
    

    def updateCursorPosition(self, event):
        '''
        When cursor inside plot, get position and print to statusbar
        '''
    
        if event.inaxes and self.rectangleROI.ID == -1:
            patches = self.canvasOriginal.figure.axes[0].patches
            if len(patches) > 5:
                patches = patches[-1:]
                self.canvasOriginal.figure.axes[0].patches = patches
            
            print("Coordinates:" + " x= " + str(round( event.xdata, 3)) + "  y= " + str(round( event.ydata, 3)))
            dx = event.xdata - self.rectangleROI.x_start
            dy = event.ydata - self.rectangleROI.y_start
            dist = sqrt(dx*dx + dy*dy)


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


        if self.chooseROI.get_active():
            self.rectangleROI.ID = 0
            self.rectangleROI.x_end = event.xdata
            self.rectangleROI.y_end = event.ydata
            print("Left:  " + str(self.rectangleROI.x_start))
            print("Up:    " + str(self.rectangleROI.y_start))
            print("Down:  " + str(self.rectangleROI.y_end))
            print("Right: " + str(self.rectangleROI.x_end))


            # Makes sure that the rectangle is set correctly
            if self.rectangleROI.x_start > self.rectangleROI.x_end:
                temp = self.rectangleROI.x_start
                self.rectangleROI.x_start = self.rectangleROI.x_end
                self.rectangleROI.x_end = temp

            if self.rectangleROI.y_start > self.rectangleROI.y_end:
                temp = self.rectangleROI.y_start
                self.rectangleROI.y_start = self.rectangleROI.y_end
                self.rectangleROI.y_end = temp            

            
            
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
            up    = int(self.rectangleROI.y_start)
            down  = int(self.rectangleROI.y_end)
            left  = int(self.rectangleROI.x_start)
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


            # Makes sure that the rectangle is set correctly
            if self.rectangleRBC.x_start > self.rectangleRBC.x_end:
                temp = self.rectangleRBC.x_start
                self.rectangleRBC.x_start = self.rectangleRBC.x_end
                self.rectangleRBC.x_end = temp

            if self.rectangleRBC.y_start > self.rectangleRBC.y_end:
                temp = self.rectangleRBC.y_start
                self.rectangleRBC.y_start = self.rectangleRBC.y_end
                self.rectangleRBC.y_end = temp            


            
            self.rectangleRBC.drawRectangle()

            self.canvasOriginal.figure.axes[0].add_patch(self.rectangleRBC.rectangle)
            print(self.canvasOriginal.figure.axes[0].patches)

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

    def update_status(self):
        '''
        Updates the status of adwin, indicating
        'Receiving' or 'Waiting'
        TODO
        '''

        temp = self.label_status + str(dc.status)

        self.infoStatus.set_label(temp)
        
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
