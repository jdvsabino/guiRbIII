from matplotlib.patches import Rectangle

class drawRectangle:

    def __init__(self, up, down, left, right):

        self.ID = None
        
        self.x_start = left
        self.y_start = up

        self.x_end = right
        self.y_end = down

        self.width = self.x_end -self.x_start
        self.height = self.y_end - self.y_start
        


    def drawRectangle(self):
        raise NotImplementedError


class roiRectangle(drawRectangle):

    def __init__(self, up=0, down=0, left=0, right=0):
        drawRectangle.__init__(self, up, down, left, right)
        self.ID = 0 # Defines object's identity as a ROI recangle
    
    def drawRectangle(self):
        rectangle = Rectangle((self.x_start,self.y_end), self.width, self.height, facecolor = "green", alpha = 0.2)
        return rectangle


class rbcRectangle(drawRectangle):

    def __init__(self, up=0, down=0, left=0, right=0):
        drawRectangle.__init__(self, up, down, left, right)
        self.ID = 1 # Defines object's identity as a RBC recangle
    
    def drawRectangle(self):
        rectangle = Rectangle((self.x_start,self.y_end), self.width, self.height, facecolor = "green", alpha = 0.2)
        return rectangle


