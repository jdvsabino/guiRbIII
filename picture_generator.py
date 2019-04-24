import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

def gen_canvas(img, width = 5, height = 5, x_min=0, x_max=0, y_min=0, y_max=0, cbar = 0, title="", font=8):
    ''' 
    Generates a canvas object from a file picture. 

    filename:  the name of the original picture
    width: width of the figure to be generated
    height: height of the figure to be generated
    x/y_min/max: limits for plot axes
    cbar: flag for colorbar

    Returns: FigureCanvas 

    TODO: More options are to be added, for example, adding plots for integrated pics
    '''

    colormap = "RdYlBu_r"
    #img = mpimg.imread(filename)
    fig = Figure(figsize = (width, height), dpi = 100)
    
    ax = fig.add_subplot(111)
    ax.set_title(title, fontsize=font)
    ax.tick_params(labelsize=font)
    
    if (x_min != x_max and y_min != y_max):   
        ax.set_xlabel([x_min,x_max])
        ax.set_ylabel([y_min,y_max])    

    im = ax.imshow(img, cmap=colormap)

    if cbar == 1:
        fig.colorbar(im, ax = ax)
        
    canvas = FigureCanvas(fig)
    
    return canvas

def gen_canvas_zoomed(fig1, fig2, fig3, width = 5, height = 5, x_min=0, x_max=0, y_min=0, y_max=0, cbar = 0, font=8):
    ''' 
    Generates a canvas object for the zoomed picture.
    The picture can be loaded from a file or from an existing picture (so far a matrix). 

    filename:  the name of the original picture
    width: width of the figure to be generated
    height: height of the figure to be generated
    x/y_min/max: limits for plot axes
    cbar: flag for colorbar

    Returns: FigureCanvas 

    TODO: More options are to be added, for example, adding plots for integrated pics
    '''
    import matplotlib.gridspec as gridspec

    
    gs = gridspec.GridSpec(4, 4, hspace=0.2, wspace=0.2)#gridspec.GridSpec(3,3) #width_ratios=[3, 1], height_ratios=[3, 1])
    #img = mpimg.imread(filename)
    fig = Figure()#Figure(figsize = (width, height), dpi = 100)
    colormap = "RdYlBu_r"

    #--- Absorption picture
    ax1 =fig.add_subplot(gs[:-1, :-1])#(gs[:-1, 1:])# fig.add_subplot(gs[0:2,0:2])
    ax1.xaxis.set_alpha(0.)
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)    
    ax1.yaxis.set_alpha(0.)
    ax1.yaxis.set_ticks_position('right')
    ax1.tick_params(labelsize = font)

    #--- Right fit
#   ax2 =fig.add_subplot(gs[:-1, 0], xticklabels=[], sharey=ax1)# fig.add_subplot(gs[2,:2])
    ax2 =fig.add_subplot(gs[:-1, -1], xticklabels=[], sharey=ax1)# fig.add_subplot(gs[2,:2])
    ax2.yaxis.set_ticks_position('right')
    ax2.tick_params(labelsize = font)

    #--- Bottom fit
    ax3 =fig.add_subplot(gs[-1, :-1], yticklabels=[], sharex=ax1) # fig.add_subplot(gs[0:2,2])
    ax3.tick_params(labelsize = font)

    
    if (x_min != x_max and y_min != y_max):   
        ax1.set_xlabel([x_min,x_max])
        ax2.set_ylabel([y_min,y_max])    

    #--- Drawing the pictures    
    im1 = ax1.imshow(fig1, cmap=colormap, aspect="auto")
    # im2 = ax2.imshow(fig2.T, cmap=colormap, aspect="auto")
    # im3 = ax3.imshow(fig3, cmap=colormap,  aspect="auto")
    im2 = ax2.plot(fig2)#, cmap=colormap, aspect="auto")
    im3 = ax3.plot(fig3)#, cmap=colormap,  aspect="auto")
    #--- Setting colorbar
    if cbar == 1:
        cbaxes = fig.add_axes([0.02, 0.4, 0.02, 0.45])
        cbaxes.yaxis.set_ticks_position('left')
        cbar = fig.colorbar(im1, cax = cbaxes)

        # cb_max = np.max(fig1)
        # cb_min = np.min(fig1)
        # cb_step = 100
        # cbar.ax.set_yticklabels(np.arange(int(cb_min), int(cb_max+cb_step), int(cb_step)), fontsize=8)
        
    #canvas = FigureCanvas(fig)
    
    #return canvas
    return fig
    
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

