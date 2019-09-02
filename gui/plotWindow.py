import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('../')
sys.path.append('./classes/')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
from gui.setRangeWindow import SetRangeWindow
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from numpy import sin, cos, pi, linspace
import datetime

class plotWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Online Plot")
        # Size settings
        self.set_default_size(700, 400)
        print(self.get_size())
        self.set_border_width(10)
        #self.set_resizable(True)
        self.set_border_width(10)

        # Main box
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=20)
        self.add(self.mainBox)

        # Subboxes to place wdidgets
        self.topBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
        self.mainBox.add(self.topBox)

        self.middleBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        self.mainBox.add(self.middleBox)

        self.bottomBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
        self.mainBox.add(self.bottomBox)


        # Top Widgets and boxes
        self.averageLabel = Gtk.Label("Average over")
        self.topBox.pack_start(self.averageLabel, True, True, 0)
        
        self.av3_Button = Gtk.RadioButton.new_with_label_from_widget(None, "3 runs")
        self.topBox.pack_start(self.av3_Button, True, True, 0)

        self.avN_Button = Gtk.RadioButton.new_from_widget(self.av3_Button)
        self.avN_Button.set_label("N runs")
        self.topBox.pack_start(self.avN_Button, True, True, 0)

        self.entryN_Runs = Gtk.Entry(text = "")
        self.topBox.pack_start(self.entryN_Runs, True, True, 0)

        self.meanLabel = Gtk.Label("Mean: 0.0")
        self.topBox.pack_start(self.meanLabel, True, True, 0)

        self.stdLabel = Gtk.Label("Std.: 0.0")
        self.topBox.pack_start(self.stdLabel, True, True, 0)
        
        
        # Middle Widgets and Boxes
        self.plotBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        self.middleBox.add(self.plotBox)

        self.plotButtonsBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        self.middleBox.add(self.plotButtonsBox)

        self.onlinePlot = Gtk.Image.new_from_file("figure_1.png")
        #self.plotBox.add(self.onlinePlot)

        ### Plot with matplotlib
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        #self.ax.plot()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(600,400)
        self.plotBox.pack_start(self.canvas, True, True, 0)
        #self.toolbar = NavigationToolbar(self.canvas, self)

        self.autoRangeButton = Gtk.Button(label = "Auto Range")
        self.plotButtonsBox.pack_start(self.autoRangeButton, True, True, 0)

        self.setRangeButton = Gtk.Button(label = "Set Range")
        self.plotButtonsBox.pack_start(self.setRangeButton, True, True, 0)
        #self.setRangeButton.connect("clicked", self.on_setRangeButton_clicked, self.setRangeWin)
        self.setRangeButton.connect("clicked", self.on_setRangeButton_clicked)

        self.saveDataButton = Gtk.Button(label = "Save Data")
        self.plotButtonsBox.pack_start(self.saveDataButton, True, True, 0)

        # Bottom Widgets and boxes
        self.varGrid = Gtk.Grid()
        self.varGrid.set_column_spacing(3)
        self.varGrid.set_row_spacing(9)
        self.bottomBox.add(self.varGrid)

        self.leftVarBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.varGrid.attach(self.leftVarBox, 0, 1, 1, 4)

        self.rightVarBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.varGrid.attach(self.rightVarBox, 1, 1, 1, 4)
    
        self.varLabel = Gtk.Label("Data Varables")
        self.varGrid.attach(self.varLabel, 0, 0, 2, 1)

        # Here we add the boxes and labels for each entry
        # starting with the left box and then the right one.

        # Var 1
        self.var1Label = Gtk.Label("Var1")
        self.leftVarBox.pack_start(self.var1Label, True, True, 0)
        self.var1Entry = Gtk.Entry()
        self.leftVarBox.pack_start(self.var1Entry, True, True, 0)

        # Var 2
        self.var2Label = Gtk.Label("Var2")
        self.leftVarBox.pack_start(self.var2Label, True, True, 0)
        self.var2Entry = Gtk.Entry()
        self.leftVarBox.pack_start(self.var2Entry, True, True, 0)

        # Var 3
        self.var3Label = Gtk.Label("Var3")
        self.leftVarBox.pack_start(self.var3Label, True, True, 0)
        self.var3Entry = Gtk.Entry()
        self.leftVarBox.pack_start(self.var3Entry, True, True, 0)

        # Var 4
        self.var4Label = Gtk.Label("Var4")
        self.leftVarBox.pack_start(self.var4Label, True, True, 0)
        self.var4Entry = Gtk.Entry()
        self.leftVarBox.pack_start(self.var4Entry, True, True, 0)

        # Var 5
        self.var5Label = Gtk.Label("Var5")
        self.rightVarBox.pack_start(self.var5Label, True, True, 0)
        self.var5Entry = Gtk.Entry()
        self.rightVarBox.pack_start(self.var5Entry, True, True, 0)

        # Var 6
        self.var6Label = Gtk.Label("Var6")
        self.rightVarBox.pack_start(self.var6Label, True, True, 0)
        self.var6Entry = Gtk.Entry()
        self.rightVarBox.pack_start(self.var6Entry, True, True, 0)

        # Var 7
        self.var7Label = Gtk.Label("Var7")
        self.rightVarBox.pack_start(self.var7Label, True, True, 0)
        self.var7Entry = Gtk.Entry()
        self.rightVarBox.pack_start(self.var7Entry, True, True, 0)

        # Var 8
        self.var8Label = Gtk.Label("Var8")
        self.rightVarBox.pack_start(self.var8Label, True, True, 0)
        self.var8Entry = Gtk.Entry()
        self.rightVarBox.pack_start(self.var8Entry, True, True, 0)        


    ### CALL BACK FUNCTIONS ###
    def on_setRangeButton_clicked(self, widget):
        from setRangeWindow import SetRangeWindow
        setWindow = SetRangeWindow()
        setWindow.connect("destroy", lambda x: Gtk.main_quit())
        setWindow.show_all()
        Gtk.main()


class newPlotWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Nice Plot")
        self.set_border_width(10)
        #self.set_default_size(700, 400)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 12)
        self.add(self.box)

        self.pbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 12)
        self.pbox.set_size_request(680, 300)
        self.box.pack_start(self.pbox, True, True, 0)
        

        
        self.middleBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
        self.box.add(self.middleBox)

        self.autoRangeButton = Gtk.Button(label = "Auto Range")
        self.autoRangeButton.connect("clicked", self.set_range_auto)
        self.middleBox.pack_start(self.autoRangeButton, True, True, 0)

        self.setRangeButton = Gtk.Button(label = "Set Range")
        self.middleBox.pack_start(self.setRangeButton, True, True, 0)
        #self.setRangeButton.connect("clicked", self.on_setRangeButton_clicked, self.setRangeWin)
        self.setRangeButton.connect("clicked", self.on_setRangeButton_clicked)
        self.winControl = 0

        self.saveDataButton = Gtk.Button(label = "Save Data")
        self.middleBox.pack_start(self.saveDataButton, True, True, 0)


        # Top Widgets and boxes
        self.plotSettingsBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
        self.box.add(self.plotSettingsBox)
        
        self.averageLabel = Gtk.Label("Average over")
        self.plotSettingsBox.pack_start(self.averageLabel, True, True, 0)
        self.averge_control = 0
        
        self.av3_Button = Gtk.RadioButton.new_with_label_from_widget(None, "3 runs")
        self.plotSettingsBox.pack_start(self.av3_Button, True, True, 0)
        self.av3_Button.connect("clicked", self.set_average)

        self.avN_Button = Gtk.RadioButton.new_from_widget(self.av3_Button)
        self.avN_Button.set_label("N runs")
        self.plotSettingsBox.pack_start(self.avN_Button, True, True, 0)
        self.avN_Button.connect("clicked", self.set_average)
        
        self.entryN_Runs = Gtk.Entry(text = "Insert no. runs")
        self.plotSettingsBox.pack_start(self.entryN_Runs, True, True, 0)

        self.meanLabel = Gtk.Label("Mean: 0.0")
        self.plotSettingsBox.pack_start(self.meanLabel, True, True, 0)

        self.stdLabel = Gtk.Label("Std.: 0.0")
        self.plotSettingsBox.pack_start(self.stdLabel, True, True, 0)


        # Values and variable boxes
        # Bottom Widgets and boxes
        self.varGrid = Gtk.Grid()
        self.varGrid.set_column_spacing(20)
        self.varGrid.set_row_spacing(9)
        self.box.pack_start(self.varGrid, True, True, 0)

        self.infoLabelBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.varGrid.attach(self.infoLabelBox, 0, 0, 1,4)

        self.leftVarBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.varGrid.attach(self.leftVarBox, 1, 1, 1, 4)

        self.rightVarBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.varGrid.attach(self.rightVarBox, 2, 1, 1, 4)
    
        self.varLabel = Gtk.Label("Data Variables")
        self.varGrid.attach(self.varLabel, 1, 0, 2, 1)

        # Here we add the boxes and labels for each entry
        # starting with the left box and then the right one.

        # Info labels
        self.label1 = Gtk.Label("System Info")
        self.infoLabelBox.add(self.label1)


        # Set environment for variables
        self.var_num   = 8
        self.variables = {}
        self.var_boxes = []
        
        self.index_label          = 0
        self.index_label_val      = 1
        self.index_chk_button     = 2
        
        for i in range(0, self.var_num):
            
            temp_name       = "Var" + str(i+1) 
            temp_label      = Gtk.Label(temp_name)
            temp_label_val  = Gtk.Label("empty")
            temp_chk_button = Gtk.CheckButton()

            if i == 0:
                temp_chk_button.set_active(True)

            self.variables[temp_name] = [temp_label, temp_label_val, temp_chk_button]
            self.var_boxes.append(Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3))
            

            if i < 4:
                self.leftVarBox.pack_start(self.variables[temp_name][self.index_label], True, True, 0)
                self.leftVarBox.pack_start(self.var_boxes[i], True, True, 0)
                self.var_boxes[i].pack_start(self.variables[temp_name][self.index_chk_button], False, False, 0)
                self.var_boxes[i].pack_start(self.variables[temp_name][self.index_label_val], False, False, 0)
            else:
                self.rightVarBox.pack_start(self.variables[temp_name][self.index_label], True, True, 0)
                self.rightVarBox.pack_start(self.var_boxes[i], True, True, 0)
                self.var_boxes[i].pack_start(self.variables[temp_name][self.index_chk_button], False, False, 0)
                self.var_boxes[i].pack_start(self.variables[temp_name][self.index_label_val], False, False, 0)
        # # Var 1
        # self.var1Label = Gtk.Label("Var1")
        # self.leftVarBox.pack_start(self.var1Label, True, True, 0)
        # self.var1_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.leftVarBox.pack_start(self.var1_box, True, True, 0)        
        # self.chk_button_1 = Gtk.CheckButton()
        # self.var1_box.pack_start(self.chk_button_1, False, False, 0)
        # self.var1Entry = Gtk.Label("empty")
        # self.var1_box.pack_start(self.var1Entry, False, False, 0)


        # # Var 2
        # self.var2Label = Gtk.Label("Var2")
        # self.leftVarBox.pack_start(self.var2Label, True, True, 0)
        # self.var2_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.leftVarBox.pack_start(self.var2_box, True, True, 0)        
        # self.chk_button_2 = Gtk.CheckButton()
        # self.var2_box.pack_start(self.chk_button_2, False, False, 0)
        # self.var2Entry = Gtk.Label("empty")
        # self.var2_box.pack_start(self.var2Entry, False, False, 0)
        

        # # Var 3
        # self.var3Label = Gtk.Label("Var3")
        # self.leftVarBox.pack_start(self.var3Label, True, True, 0)
        # self.var3_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.leftVarBox.pack_start(self.var3_box, True, True, 0)        
        # self.chk_button_3 = Gtk.CheckButton()
        # self.var3_box.pack_start(self.chk_button_3, False, False, 0)
        # self.var3Entry = Gtk.Label("empty")
        # self.var3_box.pack_start(self.var3Entry, False, False, 0)


        # # Var 4
        # self.var4Label = Gtk.Label("Var4")
        # self.leftVarBox.pack_start(self.var4Label, True, True, 0)
        # self.var4_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.leftVarBox.pack_start(self.var4_box, True, True, 0)        
        # self.chk_button_4 = Gtk.CheckButton()
        # self.var4_box.pack_start(self.chk_button_4, False, False, 0)
        # self.var4Entry = Gtk.Label("empty")
        # self.var4_box.pack_start(self.var4Entry, False, False, 0)


        # # Var 5
        # self.var5Label = Gtk.Label("Var5")
        # self.rightVarBox.pack_start(self.var5Label, True, True, 0)
        # self.var5_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.rightVarBox.pack_start(self.var5_box, True, True, 0)        
        # self.chk_button_5 = Gtk.CheckButton()
        # self.var5_box.pack_start(self.chk_button_5, False, False, 0)
        # self.var5Entry = Gtk.Label("empty")
        # self.var5_box.pack_start(self.var5Entry, False, False, 0)

        
        # # Var 6
        # self.var6Label = Gtk.Label("Var6")
        # self.rightVarBox.pack_start(self.var6Label, True, True, 0)
        # self.var6_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.rightVarBox.pack_start(self.var6_box, True, True, 0)        
        # self.chk_button_6 = Gtk.CheckButton()
        # self.var6_box.pack_start(self.chk_button_6, False, False, 0)
        # self.var6Entry = Gtk.Label("empty")
        # self.var6_box.pack_start(self.var6Entry, False, False, 0)


        # # Var 7
        # self.var7Label = Gtk.Label("Var7")
        # self.rightVarBox.pack_start(self.var7Label, True, True, 0)
        # self.var7_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.rightVarBox.pack_start(self.var7_box, True, True, 0)        
        # self.chk_button_7 = Gtk.CheckButton()
        # self.var7_box.pack_start(self.chk_button_7, False, False, 0)
        # self.var7Entry = Gtk.Label("empty")
        # self.var7_box.pack_start(self.var7Entry, False, False, 0)

        
        # # Var 8
        # self.var8Label = Gtk.Label("Var8")
        # self.rightVarBox.pack_start(self.var8Label, True, True, 0)
        # self.var8_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 3)
        # self.rightVarBox.pack_start(self.var8_box, True, True, 0)        
        # self.chk_button_8 = Gtk.CheckButton()
        # self.var8_box.pack_start(self.chk_button_8, False, False, 0)
        # self.var8Entry = Gtk.Label("empty")
        # self.var8_box.pack_start(self.var8Entry, False, False, 0)


        ### Plot objects
        self.axes   = None
        self.fig    = Figure()
        self.canvas = FigureCanvas(self.fig)

        self.plot_min = 0
        self.plot_max = 0
        
        self.pbox.pack_start(self.canvas, True, True, 0)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.pbox.pack_start(self.toolbar, False, True, 0)        
        
        self.gen_plot()


        self.set_range_window = SetRangeWindow()
        self.set_range_window.connect("delete-event", self.on_destroy_range_window)
        self.set_range_window.hide()
        self.set_range_window.setButton.connect("clicked", self.set_range)

        ''' TODO
        Make the plot in plotWindow run faster
        '''
        # self.info_from_main = None
        # GLib.timeout_add_seconds(0.5, self.gen_plot, self.info_from_main)

    ### CALL BACK FUNCTIONS ###
    def on_setRangeButton_clicked(self, *data):
        if not self.set_range_window.props.visible:
            self.set_range_window.show_all()
        return True
    
    def on_destroy_range_window(self, *data):
        if self.set_range_window.props.visible:
            self.set_range_window.hide()

        return True

    def set_range(self, *data):

        min_value = 0
        max = 0
        
        try:
            min = float(self.set_range_window.minEntry.get_text())
            max = float(self.set_range_window.maxEntry.get_text())

            if min > max:
                print("Swapped min and max values!")
                temp = min
                min = max
                max = temp

            print("Min: " +str(min))
            print("Max: " +str(max))
            self.plot_min = min
            self.plot_max = max
            self.axes.set_ylim([self.plot_min, self.plot_max])
            self.fig.canvas.draw()
            self.canvas.draw()
            
        except Exception as e:
            print("Found the following exception after trying ro set min and max values for plot:")
            print("EXCP: " + str(e) + "\n")
            print("Leaving axes unchanged.")
            return False

        return True

    def set_range_auto(self, *data):
        self.axes.autoscale()
        min, max = self.axes.get_ylim()

        print("min: ", str(min))
        print("max: ", str(max))
        self.plot_min = min
        self.plot_max = max

        self.set_range_window.minEntry.set_text(str(min))
        self.set_range_window.maxEntry.set_text(str(max))

        self.fig.canvas.draw()
        self.canvas.draw()
        return True

        
    # def gen_plot(self, x=[1,2,3], y = [4,5,6]):

        
    #     try:
    #         self.axes.remove()
    #     except:
    #         print("Couldn't remove axis!")

    #     self.axes = self.fig.add_subplot(111)

    #     if not (self.plot_min == 0 and self.plot_max == 0):
    #         self.axes.set_ylim([self.plot_min, self.plot_max])
            
    #     self.axes.plot(x, y, '--o')


    #     self.fig.tight_layout()# canvas = FigureCanvas(fig)
    #     #self.canvas = FigureCanvas(self.fig)
    #     self.fig.canvas.draw()
    #     self.canvas.draw()


    def gen_plot(self, data=dict()):

        
        try:
            self.axes.remove()
        except:
            print("Couldn't remove axis!")

        self.axes = self.fig.add_subplot(111)

        if not (self.plot_min == 0 and self.plot_max == 0):
            self.axes.set_ylim([self.plot_min, self.plot_max])
            
        try:
            for key in list(self.variables.keys()):
                if self.variables[key][self.index_chk_button].get_active():
                    self.axes.plot(data[key], '--o')
        except Exception as e:
            print("Failed plot generation with Error: " + str(e))


        self.fig.tight_layout()# canvas = FigureCanvas(fig)
        #self.canvas = FigureCanvas(self.fig)
        self.fig.canvas.draw()
        self.canvas.draw()

    def set_average(self, *data):

        if self.av3_Button.get_active():
            self.averge_control = 0
            print("Avereging over 3 runs")

        elif self.avN_Button.get_active():
            self.averge_control = 1
            print("Avereging over N runs")
