import gi
import sys, os
gi.require_version('Gtk', '3.0')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII')
sys.path.append('/home/colin/Desktop/Joao/GUI_RbIII/classes')
from gi.repository import Gtk, Gdk, GdkPixbuf

def replace_widget(old, new):
    parent = old.get_parent()

    props = {}
    for key in Gtk.ContainerClass.list_child_properties(type(parent)):
        props[key.name] = parent.child_get_property(old, key.name)

    parent.remove(old)
    parent.add(new)

    for name, value in props.iteritems():
        parent.child_set_property(new, name, value)


##### MATH FUNCTIONS #####

def gaussian_func(data, a, b, c):
    ''' 
    Returns the value of the function
       a*np.exp(-(x-b)**2/(2*c))
    '''
    return a*np.exp(-(x-b)*(x-b)/(2*c))
