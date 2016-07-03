# The square class which is a land in the game

from Images import Image

class Square(object):
    def __init__(self,row,col,color=None,landType="normal"):
        self.size = 50
        self.xMargin = 320
        self.yMargin = 60
        self.row = row
        self.col = col
        self.color = color
        self.landType = landType
        self.passable = True
        if(landType == "normal"):
            self.mana = 3
        elif(landType == "bridge"):
            self.mana = 0
        elif(landType == "obstacle"):
            self.mana = 0
            self.passable = False

    def __eq__(self,other):
        return (isinstance(other,Square) and self.row == other.row
                and self.col == other.col)

    def __hash__(self):
        return hash((self.row,self.col))

    def __repr__(self):
        return "(%d,%d)" % (self.row,self.col)

    def contains(self,x,y):
        x0 = self.col*self.size + self.xMargin
        y0 = self.row*self.size + self.yMargin
        x1 = x0+self.size
        y1 = y0+self.size
        if(x0 <= x <= x1 and y0 <= y <= y1):
            return True
        else:
            return False       

    def draw(self,canvas,data):
        x0 = self.col*self.size + self.xMargin
        y0 = self.row*self.size + self.yMargin
        x1 = x0+self.size
        y1 = y0+self.size
        if(self.landType == "normal"):
            image = data.landimage.form
            canvas.create_image((x0+x1)/2,(y0+y1)/2,image=image)
        elif(self.landType == "bridge"):
            image = data.bridgeimage.form
            canvas.create_image((x0+x1)/2,(y0+y1)/2,image=image)
            # canvas.create_line(x0,y0+(y1-y0)/3,x1,y0+(y1-y0)/3)
            # canvas.create_line(x0,y0+(y1-y0)*2/3,x1,y0+(y1-y0)*2/3)
        elif(self.landType == "obstacle"):
            image = data.obstacleimage.form
            canvas.create_image((x0+x1)/2,(y0+y1)/2,image=image)
            # canvas.create_line(x0,y0,x1,y1)
            # canvas.create_line(x0,y1,x1,y0)
        if(self.color != None):
            canvas.create_rectangle(x0+2,y0+2,x1-2,y1-2,
                outline=self.color,width=2)
