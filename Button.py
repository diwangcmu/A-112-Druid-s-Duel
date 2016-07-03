from creatures import *
from tkinter import *
from Images import Image

class Button(object):
    def __init__(self,x0,y0,width,height):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x0 + width
        self.y1 = y0 + height
        self.available = True
        self.selected = False

    def contains(self,x,y):
        if(self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1):
            return True
        else:
            return False

    def draw(self,canvas,data):
        canvas.create_rectangle(self.x0,self.y0,self.x1,self.y1)

class RoundButton(Button):
    def __init__(self,cx,cy,radius):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.available = True
        self.selected = False

    def contains(self,x,y):
        if(((self.cx-x)**2+(self.cy-y)**2)**0.5 <= self.radius):
            return True
        else:
            return False

    def draw(self,canvas,data):
        pass

class SquareButton(Button): pass

class MainPageButton(SquareButton): pass

class TutorialButton(SquareButton): pass

class CampaignButton(MainPageButton):
    def draw(self,canvas,data):
        super().draw(canvas,data)
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.mainpagebutton)
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Campaign",font="ComicSansMS 30 bold")

    def click(self,data):
        data.mode = "play"
        data.isPlayInited = False

class TutorialButton(MainPageButton):
    def draw(self,canvas,data):
        super().draw(canvas,data)
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.mainpagebutton)        
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Tutorial",font="ComicSansMS 30 bold")

    def click(self,data):
        data.mode = "tutorial"

class IndividualGameButton(MainPageButton):
    def draw(self,canvas,data):
        super().draw(canvas,data)
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.mainpagebutton)        
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Challenges",font="ComicSansMS 30 bold")

    def click(self,data):
        data.mode = "challenge"

class ChallengeButton(SquareButton):
    def __init__(self,cx,cy,text):
        self.width = 200
        self.height = 130
        self.cx = cx
        self.cy = cy
        super().__init__(cx-self.width/2,cy-self.height/2,self.width,self.height)
        self.text = text

    def click(self,data):
        data.challengeChapter = self.text
        data.challengePage = 1

    def draw(self,canvas,data):
        canvas.create_image(self.cx,self.cy,image=data.bookbutton)
        canvas.create_text(self.cx,self.cy,text=self.text,
            font="ComicSansMS 25 bold")

class ChallengeButton2(ChallengeButton):
    def click(self,data):
        data.challengeMode = self.text
        data.mode = "play"
        data.isPlayInited = False
        data.isChallengeInited = False

class ChallengeBackButton(SquareButton):
    def draw(self,canvas,data):
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.ttbuttonimage)
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Back to Last Page"
             ,font="ComicSansMS 10 bold")

    def click(self,data):
        data.challengePage = 0

class TTForwardButton(TutorialButton):
    def draw(self,canvas,data):
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.ttbuttonimage)
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Next Page",font="ComicSansMS 10 bold")

    def click(self,data):
        if data.ttPage < 10:
            data.ttPage += 1        

class TTBackwardButton(TutorialButton):
    def draw(self,canvas,data):
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.ttbuttonimage)
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Previous Page",font="ComicSansMS 10 bold")

    def click(self,data):
        if data.ttPage > 0:
            data.ttPage -= 1

class TTBackButton(TutorialButton):
    def draw(self,canvas,data):
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.ttbuttonimage)
        if(data.ttDemoPage == None):
            text = "Back to Main Page"
        else:
            text = "Back to Tutorial"
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text=text,font="ComicSansMS 10 bold")

    def click(self,data):
        if(data.ttDemoPage != None):
            data.mode = "tutorial"
            data.isPlayInited = False
            data.ttDemoPage = None
        else:
            data.mode = "splashScreen"
            data.isTutorialInited = False
            data.isPlayInited = False
            data.isChallengeInited = False
            data.challengeChapter = None
            data.challengeMode = None

class TTTry(TutorialButton):
    def draw(self,canvas,data):
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.ttbuttonimage)
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Try it out!",font="ComicSansMS 10 bold")

    def click(self,data):
        data.mode = "play"
        data.ttDemoPage = data.ttPage

class RestartButton(TutorialButton):
    def draw(self,canvas,data):
        canvas.create_image((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,image=data.ttbuttonimage)
        canvas.create_text((self.x0+self.x1)/2,
            (self.y0+self.y1)/2,text="Restart this chapter",font=
                 "ComicSansMS 10 bold")   
            
    def click(self,data):
        data.isPlayInited = False


class EndTurnButton(RoundButton):
    def draw(self,canvas,data):
        super().draw(canvas,data)
        self.selected = False
        image = data.endturnbuttonimage.form
        canvas.create_image(self.cx,self.cy,image=image)
        # canvas.create_text(self.cx,self.cy,
        #     text="End Turn",font="Times 10 bold")

    def click(self,data):
        nextPlayer = data.playerList[(data.playerList.index(data.curPlayer) 
            + 1) % len(data.playerList)]
        for row in range(10):
            for col in range(10):
                creature = data.creatures[row][col]
                if creature != None:
                    if creature.color == data.curPlayer.color:
                        creature.summonSickness = False
                        creature.turns = creature.maxTurns
                    elif creature.color == nextPlayer.color:
                        creature.detransform()
                        creature.summonSickness = False             
                        creature.turns = creature.maxTurns                        
        data.curPlayer = nextPlayer
        data.curMana = data.curPlayer.mana
        
class CreatureButtons(RoundButton):
    def __init__(self,cx,cy,radius,letter,cost):
        super().__init__(cx,cy,radius)
        self.letter = letter
        self.cost = cost
        self.selected = False

    def draw(self,canvas,data):        
        super().draw(canvas,data)
        if(self.letter == "Soldier"):
            image = data.soldierbuttonimage
        elif(self.letter == "Archer"):
            image = data.archerbuttonimage
        elif(self.letter == "Executor"):
            image = data.executorbuttonimage
        elif(self.letter == "Wizard"):
            image = data.wizardbuttonimage
        if(not self.available):
            image = image.shadedform
        elif(self.selected):
            image = image.selectedform
        else:
            image = image.form
        canvas.create_image(self.cx,self.cy,image=image)               
        # canvas.create_text(self.cx,self.cy,
        #     text="%s\nCost:%d" % (self.letter,self.cost),
        #     font="ComicSansMS 10 bold")

    def click(self,data):
        if(self.available):
            data.selectedCreature = TokenCreature(
                self.letter,data.curPlayer.color)
            self.selected = True

class TransformButton(RoundButton):
    def __init__(self,cx,cy,radius):
        super().__init__(cx,cy,radius)
        self.cost = 10

    def draw(self,canvas,data):
        super().draw(canvas,data)
        image = data.transformbuttonimage
        if(not self.available):
            image = image.shadedform
        elif(self.selected):
            image = image.selectedform
        else:
            image = image.form
        canvas.create_image(self.cx,self.cy,image=image)

    def click(self,data):
        if(self.available):
            data.selectedCreature.transform()
            data.curMana -= self.cost
            self.selected = True

class BridgeButton(RoundButton):
    def __init__(self,cx,cy,radius):
        super().__init__(cx,cy,radius)
        self.cost = 5

    def draw(self,canvas,data):
        super().draw(canvas,data)
        image = data.bridgebuttonimage
        if(not self.available):
            image = image.shadedform
        elif(self.selected):
            image = image.selectedform
        else:
            image = image.form
        canvas.create_image(self.cx,self.cy,image=image)

    def click(self,data):
        if(self.available):
            self.selected = True
            data.selectedCreature = TokenBridge()

class SpellButton(RoundButton): pass

class LandChangeButton(SpellButton):
    def __init__(self,cx,cy,radius):
        super().__init__(cx,cy,radius)
        self.cost = 3

    def draw(self,canvas,data):
        super().draw(canvas,data)
        image = data.spell1image
        if(not self.available):
            image = image.shadedform
        elif(self.selected):
            image = image.selectedform
        else:
            image = image.form
        canvas.create_image(self.cx,self.cy,image=image)
        # canvas.create_text(self.cx,self.cy,
        #     text="Land\nChange",font="ComicSansMS 10 bold") 

    def click(self,data):
        if(self.available):
            self.selected = True
            data.selectedSpell = LandChangeSpell(data.selectedCreature)
            
class ObstacleRemoveButton(SpellButton):
    def __init__(self,cx,cy,radius):
        super().__init__(cx,cy,radius)
        self.cost = 2

    def draw(self,canvas,data):
        super().draw(canvas,data)
        image = data.spell2image
        if(not self.available):
            image = image.shadedform
        elif(self.selected):
            image = image.selectedform
        else:
            image = image.form
        canvas.create_image(self.cx,self.cy,image=image)
        # canvas.create_text(self.cx,self.cy,
        #     text="Obstacle\nRemove",font="ComicSansMS 10 bold") 

    def click(self,data):
        if(self.available):
            self.selected = True
            data.selectedSpell = ObstacleRemoveSpell(data.selectedCreature)

class LandStealButton(SpellButton):
    def __init__(self,cx,cy,radius):
        super().__init__(cx,cy,radius)
        self.cost = 3

    def draw(self,canvas,data):
        super().draw(canvas,data)
        image = data.spell3image
        if(not self.available):
            image = image.shadedform
        elif(self.selected):
            image = image.selectedform
        else:
            image = image.form
        canvas.create_image(self.cx,self.cy,image=image)
        # canvas.create_text(self.cx,self.cy,
        #     text="Land\nSteal",font="ComicSansMS 10 bold") 

    def click(self,data):
        if(self.available):
            self.selected = True 
            data.selectedSpell = LandStealSpell(data.selectedCreature)