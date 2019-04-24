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

        self.rectangle = None
        


    def drawRectangle(self):
        raise NotImplementedError


class roiRectangle(drawRectangle):

    def __init__(self, up=0, down=0, left=0, right=0):
        drawRectangle.__init__(self, up, down, left, right)
        self.ID = 0 # Defines object's identity as a ROI recangle
    
    def drawRectangle(self, alpha=-1):
        self.width = self.x_end -self.x_start
        self.height = self.y_end - self.y_start

        if alpha != -1:
            self.rectangle = Rectangle((self.x_start,self.y_start), self.width, self.height, facecolor = "red", alpha=alpha)#'none', linewidth=1, edgecolor='b', alpha=alpha)
            #return self.rectangle
            
        else:
            self.rectangle = Rectangle((self.x_start,self.y_start), self.width, self.height, facecolor = 'none', linewidth=1, edgecolor='r')
        #return self.rectangle


class rbcRectangle(drawRectangle):

    def __init__(self, up=0, down=0, left=0, right=0):
        drawRectangle.__init__(self, up, down, left, right)
        self.ID = 1 # Defines object's identity as a RBC recangle
    
    def drawRectangle(self, alpha=-1):
        self.width = self.x_end -self.x_start
        self.height = self.y_end - self.y_start

        if alpha != -1:
            self.rectangle = Rectangle((self.x_start,self.y_start), self.width, self.height, facecolor = 'none', linewidth=1, edgecolor='k', alpha=alpha)
            #return self.rectangle
        else:
            self.rectangle = Rectangle((self.x_start,self.y_start), self.width, self.height, facecolor = 'none', linewidth=1, edgecolor='k')
        #return self.rectangle
