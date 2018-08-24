class drawRectangle:

    def __init__(self, up, down, left, right):

        self.x = left
        self.y = up

        self.width = right - left
        self.height = up - down

    def rectangleROI():
        rectangle = Rectangle(self.x,self.y, self.width, self.height, facecolor = "green", alpha = 0.2)
        return rectangle

    def rectangleRBC():
        rectangle = Rectangle(self.x,self.y, self.width, self.height, facecolor = "white", alpha = 0.2)
        return rectangle    
