import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

def gen_canvas(filename, width = 5, height = 5, x_min=0, x_max=0, y_min=0, y_max=0):


    img = mpimg.imread(filename)
    fig = Figure(figsize = (width, height), dpi = 100)
    ax = fig.add_subplot(111)

    if (x_min != x_max and y_min != y_max):   
        ax.set_xlabel([x_min,x_max])
        ax.set_ylabel([y_min,y_max])    

    ax.imshow(img)
    canvas = FigureCanvas(fig)
    
    return canvas


    
def rescale_pic(pic, factor=1, title=""):
    '''
    filename: the name of the file to be imported
    factor: rescaling factor
    title: title to be shown with the picture
    Returns: Gtk.Image
    
    A image file is imported with picbuf, it is manipulated
    and then transformed into a Gtk.Image object. The main 
    purpose is to generate pictures of plots, so the matplotlib
    is used to set the kind of plot as well as axis and title.
    '''

    

    ### TODO
    #read pic
    #load picbuf
    #rescale
    #generate Gtk.Image
    #
    

# def generate_pixbuf(pic):
#     '''
#     Converts a Gtk.Image Object into a pixbuf.

#     Returns: GdkPixbuf Object

#     '''

#     pixbuf = pic.get_pixbuf()    
#     return pixbuf

# def generate_pixbuf_from_file(filename):
#     '''
#     Generates pixbuf from file by generating a Gtk.Image
#     object and using 'generate_pixbuf' function (above)
#     to create a pixbuf object.
    
#     Returns: GdkPixbuf object

#     TODO
#     Improvements: Let user choose with browser window
#     '''
    
#     pic_gtk = Gtk.Image.new_from_file(filename)
#     pixbuf = generate_pixbuf(pic_gtk)
#     return pixbuf
    
def generate_plot(pic, title, xlabel, ylabel):
    '''
    Returns a plot ready to be shown in the GUI.

    Returns: Gtk.Image

    '''

    return None

