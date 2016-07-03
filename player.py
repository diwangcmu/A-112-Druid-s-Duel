# the class player has attributes mana, creatures, land etc.

import random
from creatures import *
from Button import *

class Player(object):
    def __init__(self,color,name=None,AI=False):
        self.color = color
        self.mana = 0
        self.manaLeft = 0
        self.name = name
        self.isAI = AI

    def __repr__(self):
        return self.name

    def AIMove(self,data):
        assert(data.curPlayer == self)
        # data.curMana
        # first move creatures 
            # move wizard
                # use landchange if enemy in sight
                # move to opponent's / blank space 
            # move executor
                # if two or more enemies can be killed, transform, kill
                # if 1 enemy in sight, kill
                # move to opponent's / blank space
            # move archer
                # if transform can kill wizard/executor, transform and kill
                # kill 
                # move
            # move soldier
                # if path has 4 lands and last move not adjacent to opponent's,
                # transform and move
                # kill
                # move
        # add creatures
            # close to own creatures
            # away from enemies creatures
            # creature created randomly
        (creatures,enemyCreatures,enemyLand,
            availableLand,allLands) = self.getCreatures(data)
        if(data.selectedCreature == None):
            # if(self.mana >= data.player1.mana+15 and data.curMana >= 5):
            #     pos = self.toHelpIslandsPresent(data,allLands)
            #     if(pos != None):
            #         (row,col) = pos
            #         data.squares[row][col] = Square(row,col,None,"bridge")
            #         data.curMana -= 5
            #         return 
            if(len(creatures["wizard"]) != 0):
                self.selectCreature(data,random.choice(creatures["wizard"]))
            elif(len(creatures["archer"]) != 0):
                self.selectCreature(data,random.choice(creatures["archer"]))
            elif(len(creatures["executor"]) != 0):
                self.selectCreature(data,random.choice(creatures["executor"]))
            elif(len(creatures["soldier"]) != 0):
                self.selectCreature(data,random.choice(creatures["soldier"]))
            else:
                if(data.curMana >= 5 and len(availableLand) != 0): # choose recruitment
                    (row,col) = random.choice(availableLand)
                    if(self.mana >= data.player1.mana + 15 and data.curMana >= 10):
                        data.creatures[row][col]=Archer(row,col,self.color,data,True)
                        data.curMana -= 10
                    elif(data.curMana < 10):
                        data.creatures[row][col]=Soldier(row,col,self.color,data,True)
                        data.curMana -= 5
                    elif(data.curMana < 15):
                        if(random.randint(0,10) < 6):
                            data.creatures[row][col]=Archer(row,col,self.color,data,True)
                            data.curMana -= 10
                        else:
                            data.creatures[row][col]=Soldier(row,col,self.color,data,True)
                            data.curMana -= 5
                    elif(data.curMana < 20):
                        if(random.randint(0,10) < 5):
                            data.creatures[row][col]=Soldier(row,col,self.color,data,True)
                            data.curMana -= 5
                        else:
                            data.creatures[row][col]=Executor(row,col,self.color,data,True)
                            data.curMana -= 15
                    else:
                        if(random.randint(0,10) < 5):
                            data.creatures[row][col] = Wizard(row,col,self.color,data,True)
                            data.curMana -= 20
                        else:
                            data.creatures[row][col]=Soldier(row,col,self.color,data,True)
                            data.curMana -= 5
                else:
                    for button in data.buttons:
                        if(isinstance(button,EndTurnButton)):
                            button.click(data)
                # recruitment
        elif(isinstance(data.selectedCreature,Creature)):
            if(data.selectedCreature.turns==0):
                data.selectedCreature.movablePlaces = []
                data.selectedCreature.selected = False
                data.selectedCreature = None
            elif(data.selectedCreature.kind=="wizard"): # move this wizard
                if(data.curMana >= 3):
                    enemiesInTwo = self.enemyInTwo(data)
                    if (len(enemiesInTwo) != 0): # make land change spell here
                        enemyPos = random.choice(enemiesInTwo)
                        (row,col) = enemyPos
                        data.squares[row][col] = None
                        data.creatures[row][col] = None
                        data.curMana -= 3
                        data.selectedCreature.turns -= 1
                    elif(random.randint(0,10) < 8):
                        emptySquares = self.getEmptySquares(data)
                        if(len(emptySquares) != 0):
                            (row,col) = random.choice(emptySquares)
                            data.squares[row][col] = Square(row,col)
                            data.curMana -= 3
                            data.selectedCreature.turns -= 1
                        else:
                            self.normalMove(data)
                    else:
                        self.normalMove(data)
                else:
                    self.normalMove(data)
            elif(data.selectedCreature.kind=="executor"):
                if(data.curMana >= 10 and not data.selectedCreature.transformed
                    and data.selectedCreature.turns == 2):
                    enemiesInThree = self.canKillThree(data)
                    if(enemiesInThree != None):
                        (row,col) = enemiesInThree[0]
                        data.selectedCreature.transform()
                        data.curMana -= 10
                        self.normalKillOrMove(data,row,col)
                    else:
                        self.normalKillOrMove(data)
                else:
                    self.normalKillOrMove(data)
            elif(data.selectedCreature.kind=="archer"):
                if(data.curMana >= 10 and not data.selectedCreature.transformed):
                    if(len(enemyCreatures["wizard"])!=0 or len(enemyCreatures["executor"])!=0):
                        enemies = enemyCreatures["wizard"]+enemyCreatures["executor"]
                        for enemy in enemies:
                            if(abs(enemy.row-data.selectedCreature.row)<=6 and
                                abs(enemy.col-data.selectedCreature.col)<=6):
                                data.selectedCreature.transform()
                                data.curMana -= 10
                                self.normalKillOrMove(data,enemy.row,enemy.col)
                                return
                    elif(self.mana >= data.player1.mana+15):
                        pos = random.choice(enemyLand)
                        (row,col) = pos
                        data.selectedCreature.transform()
                        data.curMana -= 10
                        self.normalKillOrMove(data,row,col)
                        return
                self.archerKillOrMove(data)
            elif(data.selectedCreature.kind=="soldier"): # to be edited 
                if(data.curMana >= 10 and not data.selectedCreature.transformed):
                    path = self.areTwoSpaceInRow(data)
                    if(path!=None):
                        data.selectedCreature.transform()
                        data.curMana -= 10
                if(data.selectedCreature.transformed):
                    self.normalMove(data)
                else:
                    self.normalKillOrMove(data)
    # following are an alternative way to find the islands, which does not 
    # work as well as the current way

    # def isIsland(self,data,row,col):
    #     if(data.squares[row][col].color == self.color):
    #         return False
    #     for checkRow in range(row-1,row+2):
    #         for checkCol in range(col-1,col+2):
    #             if(0<= checkRow <= 9 and 0<= checkCol <= 9 and
    #                 (checkRow != row or checkCol != col) and
    #                 data.squares[checkRow][checkCol] != None and
    #                 data.squares[checkRow][checkCol].color == self.color):
    #                 return False
    #     return True      

    # def calculateDistance(self,data,row1,col1,row2,col2):
    #     return max(abs(row1-row2),abs(col1-col2))

    # def toHelpIslandsPresent(self,data,allLands):
    #     answerRow = answerCol = None
    #     for pos in allLands:
    #         (row,col) = pos
    #         if self.isIsland(data,row,col):
    #             (answerRow,answerCol) = (row,col)
    #             break
    #     if(answerRow != None):
    #         lowestDistance = None
    #         nearestRow = nearestCol = None
    #         for pos in allLands:
    #             (row,col) = pos
    #             if(data.squares[row][col].color != self.color):
    #                 break
    #             distance = self.calculateDistance(data,row,col,answerRow,answerCol)      
    #             if(distance != 0):
    #                 if(distance == 2):
    #                     (nearestRow,nearestCol) = (row,col)
    #                     break
    #                 elif(lowestDistance == None or distance < lowestDistance):
    #                     lowestDistance = distance
    #                     (nearestRow,nearestCol) = (row,col)
    #     else:
    #         return None
    #     resultRow = nearestRow-1 if nearestRow > answerRow else nearestRow +1
    #     resultCol = nearestCol-1 if nearestCol > answerCol else nearestCol +1
    #     return (resultRow,resultCol)

    def getCreatures(self,data):
        result = {
        "wizard": [],
        "executor": [],
        "archer": [],
        "soldier": []
        }
        enemyResult = {
        "wizard": [],
        "executor": [],
        "archer": [],
        "soldier": []
        }
        availableLand = []
        allLands = []
        enemyLand = []
        for row in range(10):
            for col in range(10):
                creature = data.creatures[row][col]
                land = data.squares[row][col]
                if(land != None and land.landType != "obstacle"):
                    allLands.append((row,col))
                if(land != None and land.color != None and 
                        land.color != self.color):
                    enemyLand.append((row,col))
                if(land != None and creature == None and land.color == self.color):
                    availableLand.append((row,col))
                elif (creature != None and creature.color == self.color
                    and (creature.turns != 0 and not creature.summonSickness)):
                    result[creature.kind].append(creature)
                elif (creature != None and creature.color != self.color):
                    enemyResult[creature.kind].append(creature)
        return (result,enemyResult,enemyLand,availableLand,allLands)

    def enemyInTwo(self,data): # wizards only
        result = []
        row = data.selectedCreature.row
        col = data.selectedCreature.col
        for checkRow in range(row-2,row+3):
            for checkCol in range(col-2,col+3):
                if (0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                    (abs(checkRow-row) == 2 or abs(checkCol-col) == 2)):
                    if (data.squares[checkRow][checkCol] != None and
                        data.creatures[checkRow][checkCol] != None and 
                        data.creatures[checkRow][checkCol].color != self.color):
                        result.append((checkRow,checkCol))
        return result

    def getEmptySquares(self,data): #wizards only
        result = []
        row = data.selectedCreature.row
        col = data.selectedCreature.col
        for checkRow in range(row-1,row+2):
            for checkCol in range(col-1,col+2):
                if (0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                    data.squares[checkRow][checkCol] == None):
                    result.append((checkRow,checkCol))
        return result

    def canKillThree(self,data): # executor only
        row = data.selectedCreature.row
        col = data.selectedCreature.col
        for checkRow in range(row-1,row+2):
            for checkCol in range(col-1,col+2):
                if(0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                    data.squares[checkRow][checkCol] != None and
                    data.creatures[checkRow][checkCol] != None and 
                    data.creatures[checkRow][checkCol].color != self.color):
                    for check2Row in range(checkRow-1,checkRow+2):
                        for check2Col in range(checkCol-1,checkCol+2):
                            if(0<= check2Row <= 9 and 0 <= check2Col <= 9 and 
                                data.creatures[check2Row][check2Col]!=None and
                                data.creatures[check2Row][check2Col].color != self.color):
                                return [(checkRow,checkCol),(check2Row,check2Col)]

    def areTwoSpaceInRow(self,data): # soldier only
        row = data.selectedCreature.row
        col = data.selectedCreature.col
        for checkRow in range(row-1,row+2):
            for checkCol in range(col-1,col+2):
                if(0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                    data.squares[checkRow][checkCol] != None and
                    data.creatures[checkRow][checkCol] == None and 
                    data.squares[checkRow][checkCol].color != self.color):
                    for check2Row in range(checkRow-1,checkRow+2):
                        for check2Col in range(checkCol-1,checkCol+2):
                            if(0<= check2Row <= 9 and 0 <= check2Col <= 9 and 
                                data.squares[check2Row][check2Col] != None and
                                data.creatures[check2Row][check2Col] == None and 
                                data.squares[check2Row][check2Col].color != self.color):
                                    return (checkRow,checkCol)

    def archerKillOrMove(self,data): # archer only
        row = data.selectedCreature.row
        col = data.selectedCreature.col
        for checkRow in range(row-2,row+3):
            for checkCol in range(col-2,col+3):
                if(0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                    (abs(checkRow-row) == 2 or abs(checkCol-col) == 2)):
                    if(data.creatures[checkRow][checkCol] != None and 
                        data.creatures[checkRow][checkCol].color != self.color):
                        data.selectedCreature.move(checkRow,checkCol,data)
                        return
        self.normalMove(data)

    def selectCreature(self,data,creature):
        data.selectedCreature = creature
        creature.selected = True

    def normalKillOrMove(self,data,row=None,col=None): 
        # normal move possibly killing
        if(row != None):
            data.selectedCreature.move(row,col,data)
        else:
            result = []
            row = data.selectedCreature.row
            col = data.selectedCreature.col
            for checkRow in range(row-1,row+2):
                for checkCol in range(col-1,col+2):
                    if(0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                        data.creatures[checkRow][checkCol]!=None and 
                        data.creatures[checkRow][checkCol].color != self.color):
                        result.append((checkRow,checkCol))
            if(len(result)!=0): # kill first then move 
                (row,col) = random.choice(result)
                data.selectedCreature.move(row,col,data)
            else:
                self.normalMove(data)

    def normalMove(self,data): # normal move without killing
        possibilities = []
        row = data.selectedCreature.row
        col = data.selectedCreature.col
        for checkRow in range(row-1,row+2):
            for checkCol in range(col-1,col+2):
                if (0<= checkRow <= 9 and 0 <= checkCol <= 9 and 
                    (checkRow != row or checkCol != col)):
                    if(data.squares[checkRow][checkCol] != None and 
                        data.squares[checkRow][checkCol].landType != "obstacle"
                        and data.creatures[checkRow][checkCol] == None):
                        possibilities.append((checkRow,checkCol))
        superGoodMoves = []
        goodMoves = []
        badMoves = []
        superBadMoves = []
        normalMoves = []
        if(len(possibilities) != 0):
            for position in possibilities:
                if(self.goodPosition(data,position)):
                    superGoodMoves.append(position)
                elif(self.normalPosition(data,position)):
                    goodMoves.append(position)
                elif(self.isDangerousSquare(data,position)):
                    if(data.selectedCreature.kind == "wizard" or
                            data.selectedCreature.kind == "archer"):
                        superBadMoves.append(position)
                    else:
                        badMoves.append(position)
                elif(self.uselessSquare(data,position)):
                    if(data.selectedCreature.kind == "executor" or
                        data.selectedCreature.kind == "soldier"):     
                        superBadMoves.append(position)
                    else:
                        badMoves.append(position)
                else:
                    normalMoves.append(position)
        else:
            data.selectedCreature.turns = 0
            return
        random.shuffle(goodMoves)
        random.shuffle(badMoves)
        random.shuffle(normalMoves)
        random.shuffle(superBadMoves)
        random.shuffle(superGoodMoves)
        possibilities = (superGoodMoves + goodMoves + 
                        normalMoves + badMoves + superBadMoves)
        (drow, dcol) = possibilities[0]
        data.selectedCreature.move(drow,dcol,data)

    def uselessSquare(self,data,position):
        (row,col) = position
        if(data.squares[row][col].color == self.color):
            return True
        return False

    def isDangerousSquare(self,data,position): # one included
        (row,col) = position
        for checkRow in range(row-1,row+2):
            for checkCol in range(col-1,col+2):
                if (checkRow != row or checkCol != col):
                    if(0<= checkRow <= 9 and 0 <= checkCol <= 9 and
                        data.creatures[checkRow][checkCol] != None and 
                        data.creatures[checkRow][checkCol].color != self.color):
                        return True
        return False

    def goodPosition(self,data,position):
        (row,col) = position
        if(data.squares[row][col].landType != "bridge" and
            data.squares[row][col].color != None and
            data.squares[row][col].color != self.color):
            return True
        return False

    def normalPosition(self,data,position):
        (row,col) = position
        if(data.squares[row][col].landType != "bridge" and
            data.squares[row][col].color == None):
            return True
        return False

