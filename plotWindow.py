import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII/classes')
from gi.repository import Gtk, Gdk, GdkPixbuf


class plotWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Online Plot")
        self.set_border_width(10)
        # Main box
        self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=20)
        self.add(self.mainBox)

        # Subboxes to place wdidgets
        self.topBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
        self.mainBox.add(self.topBox)

        self.middleBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
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
        self.plotBox = Gtk.Box(spacing = 12)
        self.middleBox.add(self.plotBox)

        self.plotButtonsBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 3)
        self.middleBox.add(self.plotButtonsBox)

        self.onlinePlot = Gtk.Image.new_from_file("figure_1.png")
        self.plotBox.add(self.onlinePlot)
        
        self.autoRangeButton = Gtk.Button(label = "Auto Range")
        self.plotButtonsBox.pack_start(self.autoRangeButton, True, True, 0)

        self.setRangeButton = Gtk.Button(label = "Set Range")
        self.plotButtonsBox.pack_start(self.setRangeButton, True, True, 0)
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
        setWindow.show_all()
        Gtk.main()
        
        

        
        

win = plotWindow()

#print(dir(win.infoLabel))

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()        
