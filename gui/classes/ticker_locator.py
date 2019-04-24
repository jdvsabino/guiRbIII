""" 
This class generates an object which will update the axes of the pictures correctly.
"""
from matplotlib import ticker

class MyLocator(ticker.LinearLocator):
   def tick_values(self, vmin, vmax):
       "vmin and vmax are the axis limits, return the tick locations here"
       return [vmin, 0.5 * (vmin + vmax), vmax]
