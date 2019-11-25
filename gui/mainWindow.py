import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('../')
sys.path.append('../network')
sys.path.append('./')
sys.path.append('./classes')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from numpy import sin, cos, pi, linspace, sqrt, zeros, int32, array, sum
from gui.plotWindow import *
from gui.setRangeWindow import SetRangeWindow
from gui.setRegionWindow import SetRegionWindow
from picture_generator import gen_canvas, gen_canvas_zoomed
from gui.classes.drawRectangle import *
from gui.classes.helpFunctions import *
from gui.classes.ticker_locator import MyLocator
from network.data_collection import data_collector as dc
from analysis.infoManager import InfoManager
import copy
import csv

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

        ###---- Parameters for data saving
        self.save_path = "./info/"
        self.save_file = "/data"
        
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
        self.camSelect.set_active(3)
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

        self.online_plot = Gtk.Button(label="Online Plot")
        self.online_plot.connect("clicked", self.on_plot_window_clicked)
        self.online_plot.set_size_request(80,80)
        self.leftBox.pack_end(self.online_plot, False, False, 0)

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


        self.picSize    = [250, 160]
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

        # Set Region Window
        self.set_region_window = SetRegionWindow()
        self.set_region_window.connect('delete-event', self.on_destroy_region_window)
        self.set_region_window.setButton.connect('clicked', self.set_region_manual)
        # self.set_region_window.show_all()
        # self.set_region_window.hide()

        # Regions for cameras
        # Index order:
        #      0 - TAndor
        #      1 - LAndor
        #      2 - Vandor
        self.cam_regions = [dict(), dict(), dict()]
        
        with open("./gui/regions_info.txt") as f:
            print("HERE WE GO!!!!!!")
            for line in f.readlines():

                print(line)
                if line[0] == "#" or line[0] == "\n":
                    pass
                else:
                    line_temp = line.split(":")
                    separator = " "
                    if   line_temp[0] == "TANDOR":
                        self.cam_regions[0]["ROI"] = [int(s) for s in line_temp[1].split(separator)]
                        self.cam_regions[0]["RBC"] = [int(s) for s in line_temp[2].split(separator)]                        

                    elif line_temp[0] == "LANDOR":
                        self.cam_regions[1]["ROI"] = [int(s) for s in line_temp[1].split(separator)]
                        self.cam_regions[1]["RBC"] = [int(s) for s in line_temp[2].split(separator)]                                                

                    elif line_temp[0] == "VANDOR":
                        self.cam_regions[2]["ROI"] = [int(s) for s in line_temp[1].split(separator)]
                        self.cam_regions[2]["RBC"] = [int(s) for s in line_temp[2].split(separator)]                                

            print(self.cam_regions)
        self.im = InfoManager()
        self.update_pics_controll = 0

        


        # Plot Window
        self.plotWin = newPlotWindow()
        self.plotWin.connect("delete-event", self.on_destroy_plot_window)
        self.plotWin.saveDataButton.connect("clicked", self.on_save_clicked)
        self.plotWin.show_all()

        try:
            
            for i in range(0, len(self.im.variables)):
                index_name = 0
                temp_name  = "Var" + str(i+1)
               

                self.plotWin.variables[temp_name][index_name].set_label(self.im.variables[i])
                self.plotWin.variables[self.im.variables[i]] = self.plotWin.variables[temp_name] 
                del self.plotWin.variables[temp_name]
        except Exception as e:
            print("Error: Assiging variables names to variables entries went wrong.")
            print("Probably the number is not the same!")
        
        
        GLib.timeout_add_seconds(2., self.update_functions)
        
        
        
    ### CALL BACK FUNCTIONS ###
    def on_destroy_region_window(self, *data):
        if self.set_region_window.props.visible:        
            self.set_region_window.hide()
        return True


    def on_destroy_plot_window(self, *data):
        if self.plotWin.props.visible:
            self.plotWin.hide()
        return True

    def on_setRegionButton_clicked(self, *data):
        if not self.set_region_window.props.visible:        
            self.set_region_window.show_all()
        return True
        
    def on_plot_window_clicked(self, *data):
        if not self.plotWin.props.visible:
            self.plotWin.show_all()
        return True
        

    def set_picZoomed(self, image = None, font=6, colormap="RdYlBu_r"):
        import matplotlib.gridspec as gridspec

        
        gs = gridspec.GridSpec(4, 4, hspace=0.2, wspace=0.2)


        try:

            up    = int(self.im.abs_pic.ROI[0])
            down  = int(self.im.abs_pic.ROI[1])
            left  = int(self.im.abs_pic.ROI[2])
            right = int(self.im.abs_pic.ROI[3])
            
            print("ROI: "   + str(self.im.abs_pic.ROI))
            print("Up: "    + str(up))
            print("Down: "  + str(down))
            print("Left: "  + str(left))
            print("Right: " + str(right))
            
            print("**** SETTING ZOOM PIC ****")
            img1 = self.im.abs_pic.pic[up:down, left:right]
            print("Passou!")            
            img2 = self.im.abs_pic.integrate_y()
            img3 = self.im.abs_pic.integrate_x()
            print("Passou!")            
            self.im.abs_pic.fit_integrated_x("x")#plot=1)
            print("Passou!")
            self.im.abs_pic.fit_integrated_x("y")
            print("Passou!")
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
        self.axes_abs.append(self.fig_abs.add_subplot(gs[:-1, -1]))#, xticklabels=[]))#, sharey=self.axes_abs[0]))
        self.axes_abs.append(self.fig_abs.add_subplot(gs[-1, :-1]))#, yticklabels=[]))#, sharex=self.axes_abs[0]))


        cset = self.axes_abs[0].imshow(img1, cmap=colormap)
        self.axes_abs[0].xaxis.set_alpha(0.)
        self.axes_abs[0].yaxis.set_alpha(0.)
        self.axes_abs[0].xaxis.set_visible(False)
        self.axes_abs[0].yaxis.set_visible(False)    
        self.axes_abs[0].yaxis.set_ticks_position('right')
        self.axes_abs[0].tick_params(labelsize = font)
        self.axes_abs[0].set_aspect(aspect="equal", adjustable="box", anchor="C", share=True)
        aspect_ratio = self.axes_abs[0].get_data_ratio()

        ###---- COLORBAR
        # TODO:
        #      - Correct colorbar scale
        #
        self.cbaxes = self.fig_abs.add_axes([0.02, 0.4, 0.02, 0.45])
        self.cbaxes.yaxis.set_ticks_position('left')
        cbar = self.fig_abs.colorbar(cset, cax=self.cbaxes)
        cbar.set_clim(0,1)


        ###---- AXES
        # TODO:
        #      - Adjust size properly
        #
        #pos_ref = self.axes_abs[0].get_position()
        #asp = np.diff(self.axes_abs[].get_xlim())[0] / np.diff(ax2.get_ylim())[0]
        try:
            # self.axes_abs[1].set_yticklabels([])
            print("Dims pic:"  + str(img2.shape))
            print("Dims axis:" + str(img2.shape))
            tick_axis = linspace(0, img2.shape[0], img2.shape[0], dtype=int32)*self.im.abs_pic.cam.pixel2um
            print("\n\n\n\n\n x_axis:")
            print(tick_axis)
            print("\n\n\n\n\n")
            self.axes_abs[1].invert_xaxis()
            self.axes_abs[1].plot(img2[::-1].T, tick_axis, 'b', linewidth=1.2)
            self.axes_abs[1].plot(self.im.abs_pic.fit_y[::-1].T, tick_axis, '--r', linewidth=0.7)
            #self.axes_abs[1].yticks(ticks=x_axis)
            #self.axes_abs[1].yaxis.set_ticks_position('right')
            # self.axes_abs[1].selfet_aspect("equal")

        

            # left   = self.axes_abs[1].get_position().bounds[0]
            # right  = self.axes_abs[1].get_position().bounds[1]
            # width  = self.axes_abs[0].get_position().height
            # height = self.axes_abs[1].get_position().height        
            # self.axes_abs[1].set_position(Bbox(array([[left, right], [width, height]])))
            self.axes_abs[1].yaxis.set_ticks_position('right')
            #self.axes_abs[1].xaxis.set_visible(False)
            self.axes_abs[1].set_aspect(aspect=aspect_ratio, adjustable="box", anchor="C")
            
            #self.axes_abs[2].set_major_locator(ML)
            #aspect_ratio = position.width/self.picSize[0]/4
        except Exception as e:
            print("ERROR:" + str(e))
            print("Setting right plot failed!")

        
        try:

            tick_axis = linspace(0, img3.shape[0], img3.shape[0], dtype=int32)*self.im.abs_pic.cam.pixel2um*3
            self.axes_abs[2].plot(tick_axis, img3,'b', linewidth=1.2)
            #        self.axes_abs[2].set_aspect("equal", adjustable="box", anchor="C")        
            # left   = self.axes_abs[2].get_position().bounds[0]
            # right  = self.axes_abs[2].get_position().bounds[1]
            # width  = self.axes_abs[0]self.get_position().width
            # height = self.axes_abs[2].get_position().height                
            # self.axes_abs[2].set_position(Bbox(array([[left, right], [width, height]])))
            #        self.axes_abs[2].yaxis.set_visible(True)
            print("SHAPADA")
            try:
                print(img3.shape)
                print(self.im.abs_pic.fit_x.shape)
            except:# e as Exception:
                #print(e)
                print("morreu")
            self.axes_abs[2].plot(tick_axis, self.im.abs_pic.fit_x, '--r', linewidth=0.7)
            self.axes_abs[2].set_aspect(aspect=aspect_ratio, adjustable="box", anchor="C")

        except Exception as e:
            print("ERROR: " + str(e))
            print("Setting bottom plot failed")


        self.fig_abs.canvas.draw()
        self.canvasZoom.draw()

        
        
        
    def set_picAtoms(self, image = None, font = 6, colormap="RdYlBu_r", title="With atoms"):        

        try:
            self.axes_atoms = self.fig_atoms.add_subplot(111)
            self.axes_atoms.cla()
            self.axes_atoms.imshow(self.im.atom_pic.pic, cmap=colormap)
            
        except:
            print("INFO: Used argument as image.")
            self.axes_atoms = self.fig_atoms.add_subplot(111)
            self.axes_atoms.cla()
            self.axes_atoms.imshow(zeros((256, 256)), cmap=colormap)

        self.axes_atoms.set_title(title, fontsize=font)
        self.axes_atoms.tick_params(labelsize = font)
        self.fig_atoms.canvas.draw()
        self.canvas_atoms.draw()



    def set_picNoAtoms(self, image = None, font = 6, colormap="RdYlBu_r", title="Without atoms"):

        try:
            self.axes_no_atoms = self.fig_no_atoms.add_subplot(111)
            self.axes_no_atoms.imshow(self.im.no_atom_pic.pic, cmap=colormap)
            
        except Exception as e:
            print(e)
            print("INFO: Used argument as image.")
            self.axes_no_atoms = self.fig_no_atoms.add_subplot(111)
            self.axes_no_atoms.imshow(zeros((256, 256)), cmap=colormap)

        self.axes_no_atoms.set_title(title, fontsize=font)
        self.axes_no_atoms.tick_params(labelsize = font)
        self.fig_no_atoms.canvas.draw()
        self.canvas_no_atoms.draw()

        
    def set_picBkg(self, image = None, font = 6, colormap="RdYlBu_r", title = "Background"):
        try:
            self.axes_bkg = self.fig_bkg.add_subplot(111)
            self.axes_bkg.imshow(self.im.abs_pic.bkg_pic, cmap=colormap)
            

        except:
            print("INFO: Used argument as image.")
            image = zeros((256, 256)) ### TESTING
            self.axes_bkg = self.fig_bkg.add_subplot(111)
            self.axes_bkg.imshow(zeros((256, 256)), cmap=colormap)

        self.axes_bkg.set_title(title, fontsize=font)
        self.axes_bkg.tick_params(labelsize = font)
        self.fig_bkg.canvas.draw()
        self.canvas_bkg.draw()

        
    def set_picOriginal(self, image = None, font = 6, colormap = "RdYlBu_r", title = "Abs. pic."):

        try:
            self.axes_abs_small = self.fig_abs_small.add_subplot(111)
            self.axes_abs_small.imshow(self.im.abs_pic.pic, cmap=colormap)
        
        except:
            print("INFO: Used argument as image.")
            self.axes_abs_small = self.fig_abs_small.add_subplot(111)
            self.axes_abs_small.imshow(zeros((256, 256)), cmap=colormap)
        
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
    
    def set_region_cam(self, cam_id, *data):
        if self.regionControl != -1:
            try:
                self.canvasOriginal.figure.axes[0].patches = []
                self.canvasOriginal.figure.axes[1].patches = []
            except:
                print("Probably there's no roi area to clean!")

        up_roi    = self.cam_regions[cam_id]["ROI"][0]
        down_roi  = self.cam_regions[cam_id]["ROI"][1]
        left_roi  = self.cam_regions[cam_id]["ROI"][2]
        right_roi = self.cam_regions[cam_id]["ROI"][3]

        up_rbc    = self.cam_regions[cam_id]["RBC"][0]
        down_rbc  = self.cam_regions[cam_id]["RBC"][1]
        left_rbc  = self.cam_regions[cam_id]["RBC"][2]
        right_rbc = self.cam_regions[cam_id]["RBC"][3]

        ###---- Get data for ROI and RBC
        self.rectangleROI.x_start = left_roi
        self.rectangleROI.x_end   = right_roi
        self.rectangleROI.y_start = up_roi
        self.rectangleROI.y_end   = down_roi

        self.rectangleRBC.x_start = left_rbc
        self.rectangleRBC.x_end   = right_rbc
        self.rectangleRBC.y_start = up_rbc
        self.rectangleRBC.y_end   = down_rbc


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
        self.im.abs_pic.set_ROI(rectangle = self.rectangleROI)



        self.rectangleRBC.drawRectangle()

        self.canvasOriginal.figure.axes[0].add_patch(self.rectangleRBC.rectangle)
        print(self.canvasOriginal.figure.axes[0].patches)
        
        print("done! \n")
            
        #self.canvasOriginal.figure.axes[0] = axes_temp
        self.canvasOriginal.show_all()
        self.canvasOriginal.draw_idle()
        self.regionControl = 1
            
        self.im.abs_pic.set_RBC(rectangle = self.rectangleRBC)
        
        ###--- plot the ROI
        up    = int(self.rectangleROI.y_start)
        down  = int(self.rectangleROI.y_end)
        left  = int(self.rectangleROI.x_start)
        right = int(self.rectangleROI.x_end)
        self.set_picZoomed(self.im.abs_pic.pic[up:down, left:right])

        # self.regionControl = -1


    def set_region_manual(self, *data):

        if self.regionControl != -1:
            try:
                self.canvasOriginal.figure.axes[0].patches = []
                self.canvasOriginal.figure.axes[1].patches = []
            except:
                print("Probably there's no roi area to clean!")
        # self.clearRegion(0)
        # self.clearRegion(1)

        left_roi  = int(self.set_region_window.leftEntry_roi.get_text())
        right_roi = int(self.set_region_window.rightEntry_roi.get_text())
        up_roi    = int(self.set_region_window.upEntry_roi.get_text())
        down_roi  = int(self.set_region_window.downEntry_roi.get_text())

        left_rbc  = int(self.set_region_window.leftEntry_rbc.get_text())
        right_rbc = int(self.set_region_window.rightEntry_rbc.get_text())
        up_rbc    = int(self.set_region_window.upEntry_rbc.get_text())
        down_rbc  = int(self.set_region_window.downEntry_rbc.get_text())
        
        ###---- Get data for ROI and RBC
        self.rectangleROI.x_start = left_roi
        self.rectangleROI.x_end   = right_roi
        self.rectangleROI.y_start = up_roi
        self.rectangleROI.y_end   = down_roi

        self.rectangleRBC.x_start = left_rbc
        self.rectangleRBC.x_end   = right_rbc
        self.rectangleRBC.y_start = up_rbc
        self.rectangleRBC.y_end   = down_rbc


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
        self.im.abs_pic.set_ROI(rectangle = self.rectangleROI)



        self.rectangleRBC.drawRectangle()

        self.canvasOriginal.figure.axes[0].add_patch(self.rectangleRBC.rectangle)
        print(self.canvasOriginal.figure.axes[0].patches)
        
        print("done! \n")
            
        #self.canvasOriginal.figure.axes[0] = axes_temp
        self.canvasOriginal.show_all()
        self.canvasOriginal.draw_idle()
        self.regionControl = 1
            
        self.im.abs_pic.set_RBC(rectangle = self.rectangleRBC)
        
        ###--- plot the ROI
        up    = int(self.rectangleROI.y_start)
        down  = int(self.rectangleROI.y_end)
        left  = int(self.rectangleROI.x_start)
        right = int(self.rectangleROI.x_end)
        self.set_picZoomed(self.im.abs_pic.pic[up:down, left:right])

        # self.regionControl = -1
        
        
    def updateCursorPosition(self, event):
        '''
        When cursor inside plot, get position and print to statusbar
        '''
    
        if event.inaxes and self.rectangleROI.ID == -1:
            patches = self.canvasOriginal.figure.axes[0].patches
            if len(patches) > 5:
                patches = patches[-1:]
                self.canvasOriginal.figure.axes[0].patches = patches
            
            # print("Coordinates:" + " x= " + str(round( event.xdata, 3)) + "  y= " + str(round( event.ydata, 3)))
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
            # print("Left:  " + str(self.rectangleROI.x_start))
            # print("Up:    " + str(self.rectangleROI.y_start))
            # print("Down:  " + str(self.rectangleROI.y_end))
            # print("Right: " + str(self.rectangleROI.x_end))            
            # print("ROI recangle drawn!")

            self.set_region_window.leftEntry_roi.set_text(str(int(self.rectangleROI.x_start)))
            self.set_region_window.upEntry_roi.set_text(str(int(self.rectangleROI.y_start)))
            
            
        elif self.chooseRBC.get_active():
            self.rectangleRBC.x_end = event.xdata
            self.rectangleRBC.y_end = event.ydata
            self.rectangleRBC.ID = -1
            # print("Left:  " + str(self.rectangleRBC.x_start))
            # print("Up:    " + str(self.rectangleRBC.y_start))
            # print("Down:  " + str(self.rectangleRBC.y_end))
            # print("Right: " + str(self.rectangleRBC.x_end))
            # print("RBC recangle drawn!")

            self.set_region_window.leftEntry_rbc.set_text(str(int(self.rectangleRBC.x_start)))
            self.set_region_window.upEntry_rbc.set_text(str(int(self.rectangleRBC.y_start)))

            
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
            # print("Left:  " + str(self.rectangleROI.x_start))
            # print("Up:    " + str(self.rectangleROI.y_start))
            # print("Down:  " + str(self.rectangleROI.y_end))
            # print("Right: " + str(self.rectangleROI.x_end))


            # Makes sure that the rectangle is set correctly
            if self.rectangleROI.x_start > self.rectangleROI.x_end:
                temp = self.rectangleROI.x_start
                self.rectangleROI.x_start = self.rectangleROI.x_end
                self.rectangleROI.x_end = temp

            if self.rectangleROI.y_start > self.rectangleROI.y_end:
                temp = self.rectangleROI.y_start
                self.rectangleROI.y_start = self.rectangleROI.y_end
                self.rectangleROI.y_end = temp            

            self.set_region_window.rightEntry_roi.set_text(str(int(self.rectangleROI.x_end)))
            self.set_region_window.downEntry_roi.set_text( str(int(self.rectangleROI.y_end)))

            
            
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
            self.im.abs_pic.set_ROI(rectangle = self.rectangleROI)

            ###--- plot the ROI
            up    = int(self.rectangleROI.y_start)
            down  = int(self.rectangleROI.y_end)
            left  = int(self.rectangleROI.x_start)
            right = int(self.rectangleROI.x_end)
            self.set_picZoomed(self.im.abs_pic.pic[up:down, left:right])

            # self.im.abs_pic.fit_integrated_x()#plot=1)
            # self.im.abs_pic.fit_integrated_y()
            
            print("ROI recangle drawn!")
            self.chooseROI.set_active(False)
            
        elif self.chooseRBC.get_active():
            self.rectangleRBC.ID = 1
            self.rectangleRBC.x_end = event.xdata
            self.rectangleRBC.y_end = event.ydata
            # print("Left:  " + str(self.rectangleRBC.x_start))
            # print("Up:    " + str(self.rectangleRBC.y_start))
            # print("Down:  " + str(self.rectangleRBC.y_end))
            # print("Right: " + str(self.rectangleRBC.x_end))

            self.set_region_window.rightEntry_rbc.set_text(str(int(self.rectangleRBC.x_end)))
            self.set_region_window.downEntry_rbc.set_text(str(int(self.rectangleRBC.y_end)))

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

            self.im.abs_pic.set_RBC(rectangle = self.rectangleRBC)

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

    def update_plot_window(self):
        n_runs = 3
        var    = "Atom Number" 
        try:

            n_runs = int(self.plotWin.entryN_Runs.get_text())
            
            if n_runs > len(self.im.history[var]):
                n_runs = len(self.im.history[var])
            
            if not self.plotWin.averge_control:
                n_runs = 3

        except Exception as e:
            print("FAILED WITH ERROR: " + str(e))

        
        mean = sum(self.im.history["Atom Number"][-n_runs:])/n_runs
        self.plotWin.meanLabel.set_text("Mean: " + str('%.2f' % mean))

        # self.plotWin.info_from_main = self.im.history
        self.plotWin.gen_plot(self.im.history)

    def on_save_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        dialog.set_filename(self.save_path)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            now = str(datetime.datetime.now())
            now = now[:-7]
            now = now.replace(" ", "_")
            now = now.replace(":", ".")
            self.save_file = "/data_" + now + ".csv"
            self.save_path = dialog.get_filename()
            final = self.save_path + self.save_file

            f = csv.writer(open(final, "w"))
            for key, val in self.im.history.items():
                    f.writerow([key, val])
            
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    
    def update_functions(self):
        print("Funny stuff")
        try:
            import numpy as np

            # if dc.glob == self.im.dc.glob:
            #     return True
            read_data = dc.receiving_flag != 1 and dc.glob != self.im.dc.glob
            print("READ DATA: " +  str(read_data))
            if read_data:
                self.im.update_data_buffer()
                self.im.update_info(self)
                # self.plotWin.gen_plot(np.linspace(1,self.im.dc.glob,len(self.im.history[self.im.variables[0]])), self.im.history[self.im.variables[0]])
                self.update_plot_window()
                
                
                for var in self.im.variables:
                    index_label_val = 1
                    print("TO LABEL: " + str(self.im.status[var]))
                    try:    
                        self.plotWin.variables[var][index_label_val].set_label(str(round(self.im.status[var], 2)))
                    except:
                        
                        self.plotWin.variables[var][index_label_val].set_label(str(self.im.status[var]))
            
                print("Badum")
                self.update_pics()
                print("Tss...")
                self.update_status()
        except Exception as e:
            print("FAILED WITH ERROR: " +str(e)) 
            

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
            
        elif widget.get_active_text() == "TAndor":
            self.set_region_cam(0)

        elif widget.get_active_text() == "LAndor":
            self.set_region_cam(1)
            
        elif widget.get_active_text() == "VAndor":
            self.set_region_cam(2)
        
        print(widget.get_active_text() + " is active!")
