# Four creatures + token creatures + token bridges

from square import Square
from tkinter import *

class Creature(object):
    def __init__(self,row,col,color=None,summonSickness=False):
        self.size = 50
        self.xMargin = 320
        self.yMargin = 60
        self.color = color
        self.selected = False
        self.movablePlaces = []
        self.row = row
        self.col = col
        self.transformed = False
        self.offensive = True
        self.trample = False
        self.moveRange = 1
        self.turns = None
        self.summonSickness = summonSickness

    def move(self,row,col,data):
        if(not self.summonSickness):
            if(self.turns != 0):
                data.creatures[self.row][self.col] = None
                self.row = row
                self.col = col
                if(not self.trample and data.creatures[row][col] != None
                    and data.creatures[row][col].color != self.color):
                    self.turns = 0
                else:
                    self.turns -= 1
                if(data.squares[row][col].landType != "bridge"):
                    data.squares[row][col].color = self.color
                data.creatures[row][col] = self

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
        if(self.turns == 0 or self.summonSickness):
            if(not self.transformed):
                canvas.create_image((x0+x1)/2,(y0+y1)/2,
                    image=self.image.shadedform)
            else:
                canvas.create_image((x0+x1)/2,(y0+y1)/2,
                    image=self.image.shadedformT)
        elif(self.selected):
            if(not self.transformed):
                canvas.create_image((x0+x1)/2,(y0+y1)/2,
                                image=self.image.selectedform)
            else:
                canvas.create_image((x0+x1)/2,(y0+y1)/2,
                                image=self.image.selectedformT)
            for pos in self.getAvailableMoves(data):
                (row,col) = pos
                x0 = col*self.size + self.xMargin
                y0 = row*self.size + self.yMargin
                x1 = x0+self.size
                y1 = y0+self.size
                canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,
                            fill="#%02x%02x%02x" % (20, 20, 20))
        else:
            if(not self.transformed):
                canvas.create_image((x0+x1)/2,(y0+y1)/2,image=self.image.form)
            else:
                canvas.create_image((x0+x1)/2,(y0+y1)/2,image=self.image.formT)

    def getAvailableMoves(self,data): # excluding archer
        answer = []
        for drow in range(-1,2):
            for dcol in range(-1,2):
                newRow = self.row + drow
                newCol = self.col + dcol
                if(0<=newRow<=9 and 0<=newCol<= 9 and
                    data.squares[newRow][newCol] != None and 
                    data.squares[newRow][newCol].passable):
                    if(data.creatures[newRow][newCol] == None):
                        answer.append((newRow,newCol))
                    elif(data.creatures[newRow][newCol].color != self.color
                        and self.offensive):
                        answer.append((newRow,newCol))
        self.movablePlaces = answer
        return answer

    def isSelectionAllowed(self):
        if(self.summonSickness or self.turns == 0):
            return False
        else:
            return True

    def __eq__(self,other):
        return (isinstance(other,Creature) and self.row == other.row
            and self.col == other.col)

    def __hash__(self):
        return hash((self.row,self.col))

class Archer(Creature):
    def __init__(self,row,col,color,data,sm=False):
        super().__init__(row,col,color,sm)
        self.kind = "archer"
        self.maxTurns = 1
        self.turns = 1
        if(self.color == data.player1.color):
            self.image = data.archerimage1
        elif(self.color == data.player2.color):
            self.image = data.archerimage2

    def transform(self):
        self.transformed = True
        self.maxTurns = 2
        self.turns = 2

    def detransform(self):
        self.transformed = False
        self.maxTurns = 1
        self.turns = 1

    def getAvailableMoves(self,data):
        answer = []
        if(not self.transformed or (self.transformed and self.turns==1)):
            for drow in range(-1,2):
                for dcol in range(-1,2):
                    newRow = self.row + drow
                    newCol = self.col + dcol
                    if(0<= newRow <= 9 and 0 <= newCol <= 9 and
                        data.squares[newRow][newCol] != None and 
                            data.squares[newRow][newCol].passable):
                        if(data.creatures[newRow][newCol] == None):
                            answer.append((newRow,newCol))
            for drow in range(-2,3):
                for dcol in range(-2,3):
                    if (abs(drow) == 2 or abs(dcol) == 2):
                        newRow = self.row + drow
                        newCol = self.col + dcol
                        if(0<=newRow<=9 and 0<=newCol<=9 and
                            data.squares[newRow][newCol] != None and 
                            data.squares[newRow][newCol].passable and
                            data.creatures[newRow][newCol] != None and
                            data.creatures[newRow][newCol].color != self.color):
                            answer.append((newRow,newCol))
        else:
            for drow in range(-6,7):
                for dcol in range(-6,7):
                    if(drow != 0 or dcol != 0):
                        newRow = self.row + drow
                        newCol = self.col + dcol
                        if(0<=newRow<=9 and 0<=newCol<=9 and
                            data.squares[newRow][newCol] != None and 
                            data.squares[newRow][newCol].passable and
                            (data.creatures[newRow][newCol] == None or
                            data.creatures[newRow][newCol].color !=self.color)):
                            answer.append((newRow,newCol))
        self.movablePlaces = answer
        return answer

    def move(self,row,col,data):
        if(self.turns != 0 and not self.summonSickness):
            if(not self.transformed or (self.transformed and self.turns == 1)):
                if(abs(row-self.row) == 2 or abs(col-self.col) == 2):
                    data.creatures[row][col] = None
                    self.turns -= 1
                elif(abs(row-self.row) == 1 or abs(col-self.col) == 1):
                    data.creatures[self.row][self.col] = None
                    self.row = row
                    self.col = col
                    if(data.squares[row][col].landType != "bridge"):
                        data.squares[row][col].color = self.color
                    data.creatures[row][col] = self
                    self.turns -= 1
            elif(self.transformed):
                data.creatures[self.row][self.col] = None
                self.row = row
                self.col = col
                if(not self.trample and data.creatures[row][col] != None
                    and data.creatures[row][col].color != self.color):
                    self.turns = 0
                else:
                    self.turns -= 1
                if(data.squares[row][col].landType != "bridge"):
                    data.squares[row][col].color = self.color
                data.creatures[row][col] = self

class Executor(Creature):
    def __init__(self,row,col,color,data,sm=False):
        super().__init__(row,col,color,sm)
        self.kind = "executor"
        self.turns = 2
        self.maxTurns = 2
        if(self.color == data.player1.color):
            self.image = data.executorimage1
        elif(self.color == data.player2.color):
            self.image = data.executorimage2

    def transform(self):
        self.transformed = True
        self.trample = True
        self.maxTurns = 3
        self.turns = 3

    def detransform(self):
        self.transformed = False
        self.trample = False
        self.maxTurns = self.turns = 2

class Wizard(Creature):
    def __init__(self,row,col,color,data,sm=False):
        super().__init__(row,col,color,sm)
        self.kind = "wizard"
        self.maxTurns = 3
        self.turns = 3
        self.offensive = False
        if(self.color == data.player1.color):
            self.image = data.wizardimage1
        elif(self.color == data.player2.color):
            self.image = data.wizardimage2

    def transform(self):
        self.transformed = True
        self.maxTurns = 0
        self.turns = 0

    def detransform(self):
        self.transformed = False
        self.maxTurns = 3
        self.turns = 3

    def move(self,row,col,data):
        if(data.selectedSpell == None or data.selectedSpell.wizard != self):
            super().move(row,col,data)
        else:
            data.selectedSpell.move(row,col,data)
            self.turns -= 1
            data.curMana -= data.selectedSpell.cost

    def getAvailableMoves(self,data):
        if(data.selectedSpell == None or data.selectedSpell.wizard != self):
            super().getAvailableMoves(data)
            return self.movablePlaces
        else:
            self.movablePlaces = data.selectedSpell.getAvailableMoves(data)
            return self.movablePlaces 

class Soldier(Creature):
    def __init__(self,row,col,color,data,sm=False):
        super().__init__(row,col,color,sm)
        self.kind = "soldier"
        self.maxTurns = 1
        self.turns = 1
        if(self.color == data.player1.color):
            self.image = data.soldierimage1
        elif(self.color == data.player2.color):
            self.image = data.soldierimage2

    def transform(self):
        self.transformed = True
        self.maxTurns = 4
        self.turns = 4
        self.offensive = False

    def detransform(self):
        self.transformed = False
        self.maxTurns = self.turns = 1
        self.offensive = True

class Tokens(object): pass

class TokenCreature(Tokens):
    def __init__(self,cType,color):
        self.cType = cType
        self.color = color
        self.movablePlaces = []
        self.size = 50
        self.xMargin = 320
        self.yMargin = 60

    def move(self,row,col,data):
        if(self.cType == "Soldier"):
            data.creatures[row][col]=Soldier(row,col,self.color,data,True)
            cost = 5
        elif(self.cType == "Archer"):
            data.creatures[row][col]=Archer(row,col,self.color,data,True)
            cost = 10
        elif(self.cType == "Executor"):
            data.creatures[row][col]=Executor(row,col,self.color,data,True)
            cost = 15
        elif(self.cType == "Wizard"):
            data.creatures[row][col]=Wizard(row,col,self.color,data,True)
            cost = 20
        data.curMana -= cost

    def draw(self,canvas,data):
        for pos in self.getAvailableMoves(data):
            (row,col) = pos
            x0 = col*self.size + self.xMargin
            y0 = row*self.size + self.yMargin
            x1 = x0+self.size
            y1 = y0+self.size
            canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,
                        fill="#%02x%02x%02x" % (20, 20, 20))

    def getAvailableMoves(self,data):
        answer = []
        for row in range(10):
            for col in range(10):
                if(data.squares[row][col]!=None):
                    if(data.squares[row][col].color == self.color
                        and data.creatures[row][col] == None):
                        answer.append((row,col))
        self.movablePlaces = answer
        return answer

class TokenBridge(Tokens):
    def __init__(self):
        self.cost = 5
        self.movablePlaces = []
        self.size = 50
        self.xMargin = 320
        self.yMargin = 60

    def move(self,row,col,data):
        data.squares[row][col] = Square(row,col,None,"bridge")
        data.curMana -= 5

    def draw(self,canvas,data):
        for pos in self.getAvailableMoves(data):
            (row,col) = pos
            x0 = col*self.size + self.xMargin
            y0 = row*self.size + self.yMargin
            x1 = x0+self.size
            y1 = y0+self.size
            canvas.create_rectangle(x0+4,y0+4,x1-4,y1-4,
                        fill="#%02x%02x%02x" % (20, 20, 20))

    def getAvailableMoves(self,data):
        answer = []
        for row in range(10):
            for col in range(10):
                if(data.squares[row][col]==None):
                    for checkRow in range(row-1,row+2):
                        for checkCol in range(col-1,col+2):
                            if(0 <=checkRow<=9 and 0<=checkCol<=9):
                                if(data.squares[checkRow][checkCol] != None):
                                    answer.append((row,col))
        answer = list(set(answer))
        self.movablePlaces = answer
        return answer

class Spells(object):
    def __init__(self,wizard):
        self.wizard = wizard
        self.size = 50
        self.xMargin = 320
        self.yMargin = 60
        # isInstance(wizard,Wizard)
        pass

class LandChangeSpell(Spells):
    def __init__(self,wizard):
        super().__init__(wizard)
        self.cost = 3
        self.movablePlaces = []

    def move(self,row,col,data):
        if data.squares[row][col] == None:
            data.squares[row][col] = Square(row,col)
        else:
            data.squares[row][col] = None
            data.creatures[row][col] = None

    def getAvailableMoves(self,data):
        answer = []
        wRow = self.wizard.row
        wCol = self.wizard.col
        for row in range(wRow-2,wRow+3):
            for col in range(wCol-2,wCol+3):
                if (0<=row<=9 and 0<=col<=9 and
                    (row != wRow or col != wCol)):
                    if ((abs(row-wRow) == 2 or abs(col-wCol) == 2) and
                            data.squares[row][col]!=None and 
                            data.squares[row][col].landType!="bridge"):
                        answer.append((row,col))
                    elif(data.squares[row][col]==None):
                        answer.append((row,col))
        self.movablePlaces = answer
        return answer

class ObstacleRemoveSpell(Spells):
    def __init__(self,wizard):
        super().__init__(wizard)
        self.cost = 2
        self.movablePlaces = []

    def move(self,row,col,data):
        if data.squares[row][col].landType != "obstacle":
            data.squares[row][col] = Square(row,col,None,"obstacle")
        else:
            data.squares[row][col] = Square(row,col)

    def getAvailableMoves(self,data):
        answer = []
        wRow = self.wizard.row
        wCol = self.wizard.col
        for row in range(wRow-2,wRow+3):
            for col in range(wCol-2,wCol+3):
                if (0<=row<=9 and 0<=col<=9 and
                    (row != wRow or col != wCol) and 
                    (abs(row-wRow) == 2 or abs(col-wCol) == 2) and
                    data.squares[row][col] != None and 
                    data.creatures[row][col] == None):
                    answer.append((row,col))
        self.movablePlaces = answer
        return answer

class LandStealSpell(Spells): # !!!!!!copied from land change for now
    def __init__(self,wizard):
        super().__init__(wizard)
        self.cost = 3
        self.movablePlaces = []

    def move(self,row,col,data):
        data.squares[row][col].color = data.curPlayer.color

    def getAvailableMoves(self,data):
        answer = []
        wRow = self.wizard.row
        wCol = self.wizard.col
        for row in range(wRow-2,wRow+3):
            for col in range(wCol-2,wCol+3):
                if (0<=row<=9 and 0<=col<=9 and
                    (row != wRow or col != wCol) and 
                    data.squares[row][col] != None and
                    data.squares[row][col].color != data.curPlayer.color and
                    data.creatures[row][col] == None and
                    data.squares[row][col].landType != "obstacle" and
                    data.squares[row][col].landType != "bridge"):
                    answer.append((row,col))
        self.movablePlaces = answer
        return answer
