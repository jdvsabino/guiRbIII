import gi
gi.require_version('Gtk', '3.0')
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

        self.saveDataButton = Gtk.Button(label = "Save Data")
        self.plotButtonsBox.pack_start(self.saveDataButton, True, True, 0)

        
        

win = plotWindow()

#print(dir(win.infoLabel))

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()        
