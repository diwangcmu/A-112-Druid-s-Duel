# Di Wang + FF + andrewID: diw2

# animation structure adapted from 112 course notes
# tkinter used
# all tutorials copied or adapted from A Druid's Duel official game
# all images found on A Druid's Duel offical game website,
# image manipulation is done by code in images/images directory, adapted from Anthony's lecture notes
# castle background found on www.desktopwallpaperhd.net
# button image from www.clker.com
# white-blue buttons, tutorial text background, and papyrus background
# from www.dreamstime.com
# text box from forums.tigsource.com
# main page button from depositphotos.com
# bridge icon from thenounproject.com
# book button from steamtradingcards.wikia.com

from tkinter import *
from square import Square
from creatures import *
from player import Player
from Button import *
from Images import *
import math

# Splash Screen Mode

def init(data):
    data.mode = "splashScreen"
    data.isPlayInited = False
    data.isTutorialInited = False
    data.isChallengeInited = False
    data.ssButtons = []
    data.ssButtons.append(CampaignButton(300,200,300,100))
    data.ssButtons.append(TutorialButton(300,100,300,100))
    data.ssButtons.append(IndividualGameButton(300,300,300,100))
    data.ttPicture = PhotoImage(file="images/Druid.gif")
    data.ttTextBackground = PhotoImage(file="images/tutorialtextbackground.gif")
    data.campaignTextBackground = PhotoImage(file="images/papyrusbackground.gif")
    data.background = PhotoImage(file="images/images/druidbackground.gif")
    data.ttbuttonimage = PhotoImage(file="images/buttonimage.gif")
    data.button1image = PhotoImage(file="images/button1.gif")
    data.button2image = PhotoImage(file="images/button2.gif")
    data.mainpagebutton = PhotoImage(file="images/images/mainpagebuttons.gif")
    data.bookbutton = PhotoImage(file="images/bookbutton.gif")
    initializeImage(data)
    data.showPrologue = True
    data.chapter = 0
    data.ttPage = 0
    data.ttDemoPage = None
    data.challengePage = 0
    data.challengeChapter = None
    data.challengeMode = None

def mousePressed(event,data):
    if(data.mode == "splashScreen"): ssMousePressed(event,data)
    elif(data.mode == "play"): playMousePressed(event,data)
    elif(data.mode == "tutorial"): tutorialMousePressed(event,data)
    elif(data.mode == "challenge"): challengeMousePressed(event,data)

def timerFired(data):
    if(data.mode == "splashScreen"): ssTimerFired(data)
    elif(data.mode == "play"): playTimerFired(data)
    elif(data.mode == "tutorial"): tutorialTimerFired(data)
    elif(data.mode == "challenge"): challengeTimerFired(data)

def keyPressed(event,data):
    if(data.mode == "splashScreen"): ssKeyPressed(event,data)
    elif(data.mode == "play"): playKeyPressed(event,data)
    elif(data.mode == "tutorial"): tutorialKeyPressed(event,data)    
    elif(data.mode == "challenge"): challengeKeyPressed(event,data)

def redrawAll(canvas,data):
    if(data.mode == "splashScreen"): ssRedrawAll(canvas,data)
    elif(data.mode == "play"): playRedrawAll(canvas,data)
    elif(data.mode == "tutorial"): tutorialRedrawAll(canvas,data)
    elif(data.mode == "challenge"): challengeRedrawAll(canvas,data)

def ssMousePressed(event,data):
    for button in data.ssButtons:
        if button.contains(event.x,event.y):
            button.click(data)
            return

def ssTimerFired(data):
    pass

def ssKeyPressed(event,data):
    pass

def ssRedrawAll(canvas,data):
    canvas.create_image(data.width/2,data.height/2,image=data.background)
    canvas.create_text(data.width/2,50,text="A 112 Druid's Duel",
        font="ComicSansMS 40",fill="cyan")
    canvas.create_text(data.width/2,550,text="Di Wang 15112 Term Project",
        font="ComicSansMS 20")
    for button in data.ssButtons:
        button.draw(canvas,data)

def challengeInit(data):    
    data.challengePage = 0
    data.challengeChapter = None
    data.challengeMode = None
    data.challengeButtons = []
    data.challengeButtons.append(ChallengeButton(200,200,"Furious 5"))
    data.challengeButtons.append(ChallengeButton(450,200,"Tug of War"))   
    data.challengeButtons.append(ChallengeButton(700,200,"Ultimate Spells"))
    data.challengeButtons.append(ChallengeButton(200,400,"Chaotic Chaos"))
    data.challengeButtons.append(ChallengeButton(450,400,"Rebellion"))
    data.challengeButtons.append(ChallengeButton(700,400,"Peace"))
    data.challengeButtons.append(TTBackButton(400,550,100,50))
    data.challengeButtons2 = []
    data.challengeButtons2.append(ChallengeButton2(450,200,"Player vs Player"))
    data.challengeButtons2.append(ChallengeButton2(450,400,"Player vs AI"))
    data.challengeButtons2.append(ChallengeBackButton(400,550,100,50))

def challengeMousePressed(event,data):
    if(data.challengePage == 0):
        for button in data.challengeButtons:
            if(button.contains(event.x,event.y)):
                button.click(data)
    elif(data.challengePage == 1):
        for button in data.challengeButtons2:
            if(button.contains(event.x,event.y)):
                button.click(data)

def challengeTimerFired(data):
    pass

def challengeKeyPressed(event,data):
    pass

def challengeRedrawAll(canvas,data):
    if(not data.isChallengeInited):
        challengeInit(data)
        data.isChallengeInited = True
    canvas.create_image(data.width/2,data.height/2,image=
        data.gameBackground.form)
    if(data.challengePage == 0):
        for button in data.challengeButtons:
            button.draw(canvas,data)
        canvas.create_text(data.width/2,50,text="Choose a challenge",
            font="ComicSansMS 30")
    elif(data.challengePage == 1):
        for button in data.challengeButtons2:
            button.draw(canvas,data)
        canvas.create_text(data.width/2,50,
            text="Are you playing with a friend\n or with the AI?",
            font="ComicSansMS 30")

def tutorialInit(data):
    data.ttPage = 0
    data.ttButtons = []
    data.ttButtons.append(TTForwardButton(600,550,100,50))
    data.ttButtons.append(TTBackwardButton(200,550,100,50))
    data.ttButtons.append(TTBackButton(400,550,100,50))
    data.ttButtons.append(TTTry(750,250,100,50))

def tutorialMousePressed(event,data):
    for button in data.ttButtons:
        if button.contains(event.x,event.y):
            button.click(data)

def tutorialTimerFired(data):
    pass

def tutorialKeyPressed(event,data):
    pass

def tutorialRedrawAll(canvas,data):
    # all tutorials text copied or adapted from A Druid's Duel official game
    if not data.isTutorialInited:
        tutorialInit(data)
        data.isTutorialInited = True
    canvas.create_image(data.width/2,data.height/2,image=data.background)
    for button in data.ttButtons:
        button.draw(canvas,data)
    canvas.create_text(data.width/2,30,text="Page %d/11" % (data.ttPage+1),
        font="Halvetica 40")
    canvas.create_image(800,100,image=data.ttPicture)
    size = 20
    canvas.create_image(370,320,image=data.ttTextBackground)
    if(data.ttPage == 0):
        text = """
Welcome, Druid! Our job here is to be the only color to own any land.
We gain mana every turn from the land we own. The more land we own,
the more mana we get.
Use mana to transform druids into animals to recruit more druids to
your circle. Remember, mana does not carry over to your next turn!
I'm going to explain the game in detail in the next few slides. It is
easy to get started, but there can be a lot of strategies!

In each of the tutorial pages, you can click on the "Try It Out!" 
button on the right, which directs you to a real game board, where
you can play against yourself to get familiar with the rules and 
strategies explained in the tutorial page. Click on it now to get a
feeling of what the game is like! Once there, you can go back by 
clicking a "back" button on the bottom-left corner.
"""
    elif(data.ttPage == 1):
        text = """
        How to Play
The objective of the game is to be the only player who owns any land.
The board is on the right of the screen, where the lands are.
Claim land by moving your druids onto open spaces. The druids will be 
introduced later.
Land spaces are marked with ownership squares of your color.
In this page's demo, there are two players, one purple, one green.
Each person has 2 lands which are marked by their own color.
        Gain Mana
Each piece of land you own will generate mana at the beginning
of your turn. Mana is your only resource and does not carry over
from turn to turn.
In the demo, see how the next turn's mana is projected in the pie 
chart.
(Continued Next Page)
"""
    elif(data.ttPage == 2):
        text = """
        Spend Mana
Use your mana each turn to cast one of the following spells:
1. Summon new druid's to the board on any land you already own.
2. Temporarily transform your druids into powerful animals.
3. Cast spells to alter the landscape of the board. (by a wizard)
To cast any of the above spells, go and click on a spell button
to the left of the board. All mana costs are labeled next to the 
button.
The leftmost button is the end turn button, which is explained in 
the next paragraph. To the right are 4 druid summoning buttons. 
Then to the right are (from top to down):
Druid Transform Button, Bridge Button, the three wizard spells.
When a button is not available, it will appear grey.
        End Turn
It is very important to end your turn after you cannot or don't
want to spend any of your mana and/or move any of your druids.
"""
    elif(data.ttPage == 3):
        text = """


There are three types of lands: normal land, bridge, and obstacle.
Each normal land, if occupied, would provide you with 3 mana each 
turn. It is indicated by a square of grassland.
Bridge is a land that cannot generate mana and thus cannot be 
controlled. It is shown by a bridge icon.
Obstacles block the space they occupy. They are marked by plants.

In this demo, there is one obstacle and one bridge.
Go to the demo board and check them out!
"""

    elif(data.ttPage == 4):
        text = """


You have four kinds of druids in your circle. Each one moves and
attackes differently. Each one can also transform into its animal
form, giving it additional ways to move and attack. 
Soldiers cost 5 mana to recruit, can transform into wolves.
Archers cost 10 mana to recruit, can transform into eagles.
Executors cost 15 mana to recruit, can transform into bears.
Wizards cost 20 mana to recruit, can transform into turtles.
The transform cost is 10 mana, but it gives the druid immense 
power.

Each creature and its corresponding animal transformation will be
explained in detail in the next few pages.
"""
    elif(data.ttPage == 5):
        text = """
The soldiers are protectors of your sacred land. While they are
simple servants, soldiers can be dangerous in groups.
Strategies: 
Soldiers can capture a lot of land quickly as a wolf. Use groups 
of soldiers to protect areas or units. Don't be afraid to sacrifice
them in order to force your opponent to move their druids.
Abilities (untransformed):
moves/attacks 1 adjacent space
Abilities (as a wolf):
moves up to 4 spaces
cannot attack

Go to the demo board to move your soldiers, recruit and transform
them when you can!
"""
    elif(data.ttPage == 6):
        text = """
The archers are brave scouts of and wondrous marksmen who attack
only from a safe distane. Thay can shoot over obstacles and other
druids but are vulnerable to close quarters.
Strategies: 
Eagles can help to expand behind enemy linds, reach disconnected
land masses or attack distant enemies. Sacrificing an archer/eagle
can be a good way to get rid of powerful foes.
Abilities (untransformed):
moves 1 adjacent space
attackes only 2 spaces away, cannot attack adjacent
Abilities (as an eagle):
fly up to 6 spaces to capture land or attack enemies
attacking ends turn, captures space
not attacking allows another normal action

Go to the demo board to move your archers, recruit and transform
them when you can!
"""
        size = 17
    elif(data.ttPage == 7):
        text = """
The executors are fierce fighters for your circle. Strength and 
endurance are combined with untamed ferocity in this one-druid
wrecking machine.
Strategies: 
Make use of this druid's extended movement range to capture land.
The bear can trample groups of foes if you can get him in range.
Abilities (untransformed):
moves 2 spaces each turn
1 of those moves can be an attack
attacking ends the executor's turn
Abilities (as a bear):
move and attack 3 spaces in a row
can attack turtles

Go to the demo board to move your executors, recruit and transform
them when you can!
"""
    elif(data.ttPage == 8):
        text = """
The wizard derives his powers from the primal force of mana.
He is at one with your land and uses ancient rites to bend it to
his will. Use his spells to master the landscape to the detriment
of your foes. 
Strategies: 
Every piece of land you destroy is less mana available to all
players. Beware of units on bridges, as you cannot destroy a bridge.
If you cannot gain a massive advantage this turn, try turning it
into a turtle.
(Continued next Page)
"""
    elif(data.ttPage == 9):
        text = """
Abilities (untransformed):
has 3 move or spells actions per turn
1st spell: add/destroy land (mana cost 3)
2nd spell: add/destroy obstacle (mana cost 2)
3rd spell: steal land (mana cost 3)
cannot attack
spells ranges are mostly 2 spaces
Abilities (as a turtle):
cannot move or attack or use spells
cannot be destroyed by normal attacks

Note that a spell button will be available only when you have selected
a wizard. 
Go to the demo board to move your wizards, cast spells, recruit and 
transform them when you can!
"""
    elif(data.ttPage == 10):
        text = """



Now you have known the basics for the game. Let's start playing!
The suggested starting place is the campaign, where you can enjoy a 
story while practicing playing against an AI.

If you want to play individual games with either a friend or the AI,
go back to the main menu and choose challenges. 
Warning: some challenges are hard!

Enjoy!
(Click on "Back to Main Page" to go back.)
"""
    canvas.create_text(50,50,anchor=NW,text=text,font="ComicSansMS %d"%(
        size),fill="black")

def drawPrologue(canvas,data):    
    canvas.create_image(800,100,image=data.ttPicture)
    canvas.create_image(350,350,image=data.campaignTextBackground)    
    canvas.create_text(450,570,text="Press space to continue",
        font="ComicSansMS 30 bold", fill="navy")
    size = 20
    if(data.chapter == 0):
        size = 16
        text = """
Welcome to A 112 Druid's Duel campaign! If you have not yet read the tutorials, 
please do so as that would maximize your playing experience here.
If yes, then let's begin our journey!

Once upon a time, there was a kingdom called 112 in the far occidental world. 
What was special about this kingdom is that every druid in the kingdom could 
use magical powers, except that everybody was differently gifted. The King was 
a capable druid ruler, and the people lived happily under his reign...
Until one day a group of barbarians invaded.

The barbarians are hostile people that are not quite intellectually gifted. 
They ruthlessly killed the druids without any obvious reason, and who was 
their leader also remained a mystery. The King lead his courageous army to 
fight back, but the barbarians seemed to have an advantage.

You are a young talented druid who wanted to save your kingdom from the barbarians 
by joining the royal army. Today you graduated from the training school and 
embarked on your way to the palace until a barbarian stopped you in a forest...

(Hint: Use the soldier to occupy more land and guard them!
Also don't forget to press the end turn button on the left once you're done!)
"""
    elif(data.chapter == 1):
        text = """


Good! You have just successfully driven the barbarian away. 
However, it seems that the barbarian has called other barbarians
during its retreat. 

This time, however, you noticed that the barbarians are able to fly. 
The good news is some druids who lived nearby heard the hustle and 
joined your side.

Can you defeat the flying barbarians?

(Hint: Take advantage of the archer's weak defensive power)
"""
    elif(data.chapter == 2):
        text ="""

After defeating the flying opponents, a druid named Yvetal studied 
the feathers left by the barbarians, and happily claimed that he 
had found the secret of the barbarians' flying power.

"All those archers have drunk a kind of magical potion which allows
them to fly temporarily at a cost of manas," said Yvetal. 

Then he decided to go back to his home to bring some for your team 
as well. While waiting for him, you expressed your ambition of 
saving the kingdom to your fellow druids. Most of them approved your 
valor, and some agreed to accompany you. One druid, named Zygarde, 
introduced himself as an "executor", and invited you to try out his 
power by having a friendly druid-against-druid battle. 

(Hint: Mind the power of the oppoenent's executor)
"""
    elif(data.chapter == 3):
        text ="""

"Executor is so powerful!" You exclaimed after a winning a very close 
battle.

"It sure is," said Zygarde, "that's why I am always the first to be 
attacked in a battle against the barbarians."

As you were engaged in a joyful conversation, Yvetal returned. 

"Now we can have flying abilities too! By the way, I myself is a 
wizard, which is why I am a master of so many spells."

Your team now resumed your way to the palace. However, the sky 
suddenly darkened and your team were torn apart by some evil, 
strong magical power. A group of barbarians just arrived!

(Hint: get rid of the opponent's wizards quickly! Also keep your wizard 
alive!)
"""
    elif(data.chapter == 4):
        text = """
It was a very close battle. You finally managed to drive the barbarians
away, but most of the druids on your side are severely wounded. One
thing that you do not quite understand is how the barbarians can 
pinpoint your position and master so many fearsome spells.

Yvetal suggested that most of the spells could be used by him, the wizard,
as well. It is just that you are not so familiar with how the power of
the wizard should be wielded to gain an advantage.

Therefore you began a training battle against Yvetal while the other 
druids are in recovery.
"""

    canvas.create_text(50,50,anchor=NW,text=text,
        font="ComicSansMS %d" % (size),fill="black")

### Game Body ###

def initializeButton(data):
    data.buttons = []
    data.buttons.append(EndTurnButton(50,400,25))
    data.buttons.append(CreatureButtons(150,300,30,"Soldier",5))
    data.buttons.append(CreatureButtons(150,375,30,"Archer",10))
    data.buttons.append(CreatureButtons(150,450,30,"Executor",15))
    data.buttons.append(CreatureButtons(150,525,30,"Wizard",20))
    data.buttons.append(TransformButton(250,280,30))
    data.buttons.append(BridgeButton(250,355,30))
    data.buttons.append(LandChangeButton(250,470,30))
    data.buttons.append(ObstacleRemoveButton(250,525,30))
    data.buttons.append(LandStealButton(250,580,30))
    data.buttons.append(TTBackButton(10,550,100,50))
    if(data.ttDemoPage == None):
        data.buttons.append(RestartButton(10,500,100,50))

def initializeImage(data):
    # all images found on A Druid's Duel offical game website,
    # game background found on Google
    # button image from www.clker.com
    data.gameBackground = Image("gamebackground")
    data.endturnbuttonimage = Image("endturnbutton")
    data.bridgebuttonimage = ButtonImage("bridgebutton")
    data.soldierbuttonimage = ButtonImage("soldierbutton")
    data.archerbuttonimage = ButtonImage("archerbutton")
    data.executorbuttonimage = ButtonImage("executorbutton")
    data.wizardbuttonimage = ButtonImage("wizardbutton")
    data.transformbuttonimage = ButtonImage("transformbutton")
    data.spell1image = ButtonImage("spell1")
    data.spell2image = ButtonImage("spell2")
    data.spell3image = ButtonImage("spell3")
    data.landimage = Image("land")
    data.bridgeimage = Image("bridge")
    data.obstacleimage = Image("obstacle")
    data.archerimage1 = CreatureImage("archer",1)
    data.archerimage2 = CreatureImage("archer",2)
    data.soldierimage1 = CreatureImage("soldier",1)
    data.soldierimage2 = CreatureImage("soldier",2)
    data.wizardimage1 = CreatureImage("wizard",1)
    data.wizardimage2 = CreatureImage("wizard",2)
    data.executorimage1 = CreatureImage("executor",1)
    data.executorimage2 = CreatureImage("executor",2)

def resetMana(data):
    data.unoccupiedMana = 0
    for player in data.playerList:
        player.mana = 0
    for row in range(10):
        for col in range(10):
            square = data.squares[row][col]
            if square != None:
                if square.color == None:
                    data.unoccupiedMana += square.mana
                else:
                    for player in data.playerList:
                        if square.color == player.color:
                            player.mana += square.mana
    for player in data.playerList:
        if player.mana == 0:
            data.playerList.remove(player)
    if len(data.playerList) == 1:
        data.isGameOver = True
        data.winner = data.playerList[0]

def initializeGame(data):    
    data.selectedCreature = None
    data.selectedSpell = None
    if(data.ttDemoPage != None):
        for row in range(3,7):
            for col in range(3,7):
                data.squares[row][col] = Square(row,col)
        for row in range(4,5):
            for col in range(4,6):
                data.squares[row][col] = Square(row,col,data.player1.color)
        for row in range(6,7):
            for col in range(5,7):
                data.squares[row][col] = Square(row,col,data.player2.color)
        if(data.ttDemoPage == 3):
            data.squares[3][3] = Square(3,3,None,"bridge")
            data.squares[3][6] = Square(3,6,None,"obstacle")
        elif(data.ttDemoPage == 5):
            data.creatures[4][5] = Soldier(4,5,data.player1.color,data)
            data.creatures[4][4] = Soldier(4,4,data.player1.color,data)
            data.creatures[6][6] = Soldier(6,6,data.player2.color,data)   
            data.creatures[6][5] = Soldier(6,5,data.player2.color,data) 
        elif(data.ttDemoPage == 6):
            data.creatures[4][5] = Archer(4,5,data.player1.color,data)
            data.creatures[4][4] = Archer(4,4,data.player1.color,data)
            data.creatures[6][6] = Archer(6,6,data.player2.color,data)   
            data.creatures[6][5] = Archer(6,5,data.player2.color,data)
        elif(data.ttDemoPage == 7):
            data.creatures[4][5] = Executor(4,5,data.player1.color,data)
            data.creatures[4][4] = Executor(4,4,data.player1.color,data)
            data.creatures[6][6] = Executor(6,6,data.player2.color,data)   
            data.creatures[6][5] = Executor(6,5,data.player2.color,data)
        elif(data.ttDemoPage == 8 or data.ttDemoPage == 9):
            data.creatures[4][5] = Wizard(4,5,data.player1.color,data)
            data.creatures[4][4] = Wizard(4,4,data.player1.color,data)
            data.creatures[6][6] = Wizard(6,6,data.player2.color,data)   
            data.creatures[6][5] = Wizard(6,5,data.player2.color,data)
    elif(data.challengeChapter != None):
        if(data.challengeChapter == "Furious 5"):
            for row in range(1,9):
                for col in range(1,9):
                    data.squares[row][col] = Square(row,col)
            for col in range(1,6):
                data.squares[8][col] = Square(8,col,data.player1.color)
                data.creatures[8][col] = Soldier(8,col,data.player1.color,data)
            for col in range(4,9):
                data.squares[1][col] = Square(1,col,data.player2.color)
                data.creatures[1][col] = Soldier(1,col,data.player2.color,data)
            data.creatures[8][5] = Executor(8,5,data.player1.color,data)
            data.creatures[1][8] = Wizard(1,8,data.player2.color,data)
        elif(data.challengeChapter == "Tug of War"):
            for row in range(3,7):
                for col in range(0,2):
                    data.squares[row][col] = Square(row,col)
                for col in range(8,10):
                    if(col == 9):
                        data.squares[row][col] = Square(row,col,data.player2.color)
                    else:
                        data.squares[row][col] = Square(row,col)
            data.squares[3][0] = Square(3,0,data.player1.color)
            data.squares[6][0] = Square(6,0,data.player1.color)
            for row in [2,7]:
                for col in range(4,6):
                    if(col == 4):
                        data.squares[row][col] = Square(row,col,data.player1.color)
                    else:
                        data.squares[row][col] = Square(row,col,data.player2.color)
            for row in range(4,6):
                for col in range(3,7):
                    if(col == 3):
                        data.squares[row][col] = Square(row,col,data.player1.color)
                        data.creatures[row][col] = Soldier(row,col,data.player1.color,data)
                    elif(col == 5):
                        data.squares[row][col] = Square(row,col,data.player2.color)
                        data.creatures[row][col] = Soldier(row,col,data.player2.color,data)
                    elif(col == 6):
                        data.squares[row][col] = Square(row,col,data.player2.color)
                    else:
                        data.squares[row][col] = Square(row,col)
        elif(data.challengeChapter == "Ultimate Spells"):
            data.squares[0][4] = Square(0,4,data.player1.color)
            data.squares[7][0] = Square(7,0,data.player1.color)
            data.squares[7][9] = Square(7,9,data.player1.color)
            data.squares[9][4] = Square(9,4,data.player2.color)
            data.squares[2][0] = Square(2,0,data.player2.color)
            data.squares[2][9] = Square(2,9,data.player2.color)
            data.creatures[0][4] = Wizard(0,4,data.player1.color,data)
            data.creatures[7][0] = Wizard(7,0,data.player1.color,data)
            data.creatures[9][4] = Wizard(9,4,data.player2.color,data)
            data.creatures[2][0] = Wizard(2,0,data.player2.color,data)
            data.creatures[2][9] = Wizard(2,9,data.player2.color,data)
            if(data.challengeMode == "Player vs AI"):
                data.squares[4][4] = Square(4,4,data.player2.color)
                data.creatures[4][4] = Wizard(4,4,data.player2.color,data)
        elif(data.challengeChapter == "Chaotic Chaos"):
            for row in range(1,9):
                for col in range(1,9):
                    if((row+col)%2 == 0):
                        data.squares[row][col] = Square(row,col,data.player2.color)
                    else:
                        data.squares[row][col] = Square(row,col,data.player1.color)
            for (row,col) in [(1,8),(8,1),(4,5),(5,4)]:
                data.squares[row][col] = Square(row,col,data.player2.color)
        elif(data.challengeChapter == "Rebellion"):
            for row in range(10):
                if(row == 0 or row == 9):
                    color = data.player2.color
                else:
                    color = None
                data.squares[row][5] = Square(row,5,color)
                data.squares[row][0] = Square(row,0)
                data.squares[row][9] = Square(row,9)
            for col in range(10):
                if(col == 0 or col == 9):
                    color = data.player2.color
                elif(col == 5):
                    color = data.player1.color
                else:
                    color = None
                data.squares[4][col] = Square(4,col,color)
            data.creatures[4][5] = Wizard(4,5,data.player1.color,data)
            data.squares[0][0] = Square(0,0,data.player1.color)
            data.squares[9][9] = Square(9,9,data.player1.color)
            data.squares[0][9] = Square(0,9,data.player1.color)
            data.squares[9][0] = Square(9,0,data.player1.color)
            data.creatures[4][0] = Executor(4,0,data.player2.color,data)
            data.creatures[4][9] = Executor(4,9,data.player2.color,data)
            data.creatures[0][5] = Executor(0,5,data.player2.color,data)
            data.creatures[9][5] = Executor(9,5,data.player2.color,data)
        elif(data.challengeChapter == "Peace"):
            for row in range(4,6):
                for col in [0,1]:
                    data.squares[row][col] = Square(row,col,data.player1.color)
                for col in [8,9]:
                    data.squares[row][col] = Square(row,col,data.player2.color)
            if(data.challengeMode == "Player vs AI"):
                data.creatures[5][9] = Wizard(5,9,data.player2.color,data)
    elif(data.chapter == 0):
        for row in range(3,7):
            for col in range(3,7):
                data.squares[row][col] = Square(row,col)
        for row in range(4,5):
            for col in range(4,6):
                data.squares[row][col] = Square(row,col,data.player1.color)
        for row in range(6,7):
            for col in range(5,7):
                data.squares[row][col] = Square(row,col,data.player2.color)
        data.creatures[4][5] = Soldier(4,5,data.player1.color,data)
        data.creatures[6][6] = Soldier(6,6,data.player2.color,data)
    elif(data.chapter == 1):
        for row in range(2,8):
            for col in range(2,8):
                data.squares[row][col] = Square(row,col)
        for row in range(4,5):
            for col in range(5,7):
                data.squares[row][col] = Square(row,col,data.player1.color)
        for row in range(6,7):
            for col in range(5,8):
                data.squares[row][col] = Square(row,col,data.player2.color)
        data.creatures[4][5] = Soldier(4,5,data.player1.color,data)
        data.creatures[4][6] = Soldier(4,6,data.player1.color,data)
        data.creatures[6][7] = Archer(6,7,data.player2.color,data)
        data.creatures[6][6] = Archer(6,6,data.player2.color,data)
    elif(data.chapter == 2):
        for row in range(3,8):
            for col in range(3,8):
                data.squares[row][col] = Square(row,col)
        for row in range(3,5):
            for col in range(5,7):
                data.squares[row][col] = Square(row,col,data.player1.color)
        for row in range(6,8):
            for col in range(4,6):
                data.squares[row][col] = Square(row,col,data.player2.color)
        data.creatures[4][5] = Soldier(4,5,data.player1.color,data)
        data.creatures[4][6] = Soldier(4,6,data.player1.color,data)
        data.creatures[6][4] = Soldier(6,4,data.player2.color,data)
        data.creatures[6][5] = Executor(6,5,data.player2.color,data)        
    elif(data.chapter == 3):
        for row in range(3,7):
            for col in range(3,7):
                data.squares[row][col] = Square(row,col)
        for row in range(2,3):
            for col in range(1,3):
                data.squares[row][col] = Square(row,col,data.player1.color)
        for row in range(7,8):
            for col in range(7,9):
                data.squares[row][col] = Square(row,col,data.player1.color)        
        for row in range(3,5):
            for col in range(5,7):
                data.squares[row][col] = Square(row,col,data.player2.color)
        data.creatures[2][2] = Archer(2,2,data.player1.color,data)
        data.creatures[2][1] = Archer(2,1,data.player1.color,data)
        data.creatures[7][7] = Executor(7,7,data.player1.color,data)
        data.creatures[7][8] = Wizard(7,8,data.player1.color,data)
        data.creatures[3][5] = Wizard(3,5,data.player2.color,data)
        data.creatures[3][6] = Archer(3,6,data.player2.color,data)
        data.creatures[4][5] = Soldier(4,5,data.player2.color,data) 
        data.creatures[4][6] = Wizard(4,6,data.player2.color,data)  
    elif(data.chapter == 4):
        for row in range(2,8):
            for col in range(2,8):
                data.squares[row][col] = Square(row,col)
        data.squares[0][0] = Square(0,0,data.player1.color)
        data.squares[9][9] = Square(9,9,data.player2.color)
        data.squares[2][2] = Square(2,2,data.player1.color)
        data.squares[7][7] = Square(7,7,data.player2.color)
        data.creatures[2][2] = Wizard(2,2,data.player1.color,data)
        data.creatures[7][7] = Wizard(7,7,data.player2.color,data)

def resetSelection(data):
    for row in range(10):
        for col in range(10):
            if data.creatures[row][col] != None:
                data.creatures[row][col].selected = False
                data.creatures[row][col].movablePlaces = []
    data.selectedCreature = None
    for button in data.buttons:
        button.selected = False
    data.selectedSpell = None

def resetButtonAvailability(data):
    for button in data.buttons:
        if(isinstance(button,CreatureButtons) or
            isinstance(button,BridgeButton)):
            if button.cost > data.curMana:
                button.available = False
            else:
                button.available = True
        elif(isinstance(button,TransformButton)):
            if (button.cost > data.curMana or 
                data.selectedCreature == None or 
                isinstance(data.selectedCreature,Tokens) or
                data.selectedCreature.transformed or
                data.selectedCreature.turns != data.selectedCreature.maxTurns):
                button.available = False
            else:
                button.available = True
        elif(isinstance(button,SpellButton)):
            if (data.selectedCreature != None
                and isinstance(data.selectedCreature,Wizard)
                and button.cost <= data.curMana
                and data.selectedCreature.turns > 0):
                button.available = True
            else:
                button.available = False

def doesEmptySquareContain(row,col,x,y):
    size = 50
    xMargin = 320
    yMargin = 60
    x0 = col*size + xMargin
    y0 = row*size + yMargin
    x1 = x0+size
    y1 = y0+size
    if(x0 <= x <= x1 and y0 <= y <= y1):
        return True
    else:
        return False  

def playInit(data):
    if(data.ttDemoPage != None or data.challengeMode == "Player vs Player"):
        data.player1 = Player("purple","Player1")
        data.player2 = Player("SeaGreen2","Player2")
    else:
        data.player2 = Player("SeaGreen2","Player2(AI)",True)
        data.player1 = Player("purple","Player1(You)")
    data.playerList = [data.player1,data.player2]
    data.squareSize = 50
    data.creatures = [[None for i in range(10)] for j in range(10)]
    data.squares = [[None for i in range(10)] for j in range(10)]
    initializeGame(data)
    initializeButton(data)    
    resetMana(data)
    data.curPlayer = data.player1
    data.curMana = data.curPlayer.mana
    resetButtonAvailability(data)
    data.isGameOver = False
    data.winner = None
    if(data.ttDemoPage != None or data.challengeChapter != None):
        data.showPrologue = False
    else:
        data.showPrologue = True

def getMouseClicked(event,data):
    for row in range(10):
        for col in range(10):
            square = data.squares[row][col]
            if square == None:
                if doesEmptySquareContain(row,col,event.x,event.y):
                    return [None, row, col]
            elif(square.contains(event.x,event.y)):
                return (row,col)
    return False

def playMousePressed(event, data):
    if(not data.isGameOver and not data.curPlayer.isAI):
        pos = getMouseClicked(event,data)
        if(type(pos) == tuple): # in the board, square exists
            (row,col) = pos
            creature = data.creatures[row][col]
            square = data.squares[row][col]
            if data.selectedCreature == None:
                if creature != None:
                    if creature.color == data.curPlayer.color:
                        if creature.contains(event.x,event.y):
                            if(creature.isSelectionAllowed()):
                                creature.selected = True
                                data.selectedCreature = creature
            else:
                if (square != None and square.contains(event.x, event.y) and 
                    (row,col) in data.selectedCreature.movablePlaces):
                    data.selectedCreature.move(row,col,data)
                    resetMana(data)
                resetSelection(data)
        elif(type(pos) == list and pos[0] == None): # square does not exist
            (row,col) = (pos[1],pos[2])
            if (data.selectedCreature != None and 
                isinstance(data.selectedCreature,TokenBridge)
                and (row,col) in data.selectedCreature.movablePlaces):
                data.selectedCreature.move(row,col,data)
                resetMana(data)
            elif (data.selectedSpell != None and 
                        isinstance(data.selectedCreature,Wizard) and
                        isinstance(data.selectedSpell,LandChangeSpell) and
                        (row,col) in data.selectedCreature.movablePlaces):
                data.selectedCreature.move(row,col,data)
                resetMana(data)
            resetSelection(data)
        elif(pos == False):
            buttonClick = False
            for button in data.buttons:
                if button.contains(event.x,event.y):
                    if(isinstance(button,EndTurnButton)):
                        resetSelection(data)
                        button.click(data)
                        buttonClick = True
                    else:
                        if((not isinstance(button,SpellButton) or 
                            (data.selectedCreature != None and not 
                            isinstance(data.selectedCreature,Wizard)))
                            and not isinstance(button,TransformButton)):
                            resetSelection(data)
                        if(button.available): # must be available to be clicked
                            isButtonSelected = False # if different button clicked,
                            for testButton in data.buttons: # reset selection.
                                if(testButton.selected):
                                    isButtonSelected = True
                            if(isButtonSelected):
                                resetSelection(data)
                            else:
                                button.click(data)
                                buttonClick = True
            if(not buttonClick):
                resetSelection(data) # reset if button not clicked
        resetButtonAvailability(data)

def playKeyPressed(event, data):
    if(event.char == "a"):
        data.isGameOver = True
        data.winner = data.player1
    elif(data.isGameOver and event.char == "r" and not data.showPrologue
        and data.ttDemoPage == None and data.challengeChapter == None):
        if(data.winner == data.player1):
            data.chapter += 1
            if(data.chapter >= 5):
                init(data)
            data.showPrologue = True
        else:
            playInit(data)
    elif(data.isGameOver and event.char == "r" and not data.showPrologue
        and data.challengeChapter != None):
        data.mode = "splashScreen"
        data.isPlayInited = False
        data.isChallengeInited = False
    elif(data.isGameOver and event.char == "r" and not data.showPrologue
        and data.ttDemoPage != None):
        data.mode = "tutorial"
        data.isPlayInited = False
        data.ttDemoPage = None
    elif(data.showPrologue and event.keysym == "space"):
        playInit(data)
        data.showPrologue = False

def playTimerFired(data):
    if(not data.isGameOver and data.curPlayer.isAI):
        data.curPlayer.AIMove(data)
        resetMana(data)
        resetButtonAvailability(data)

def drawManaPie(canvas,data):
    (x0,y0) = (170,150)
    (x1,y1) = (270,250)
    book = dict()
    book["white"] = data.unoccupiedMana
    for player in data.playerList:
        book[player.color] = player.mana
    totalMana = sum(book.values())
    i = 0
    lastStart = 0
    while i < len(data.playerList):
        player = data.playerList[i]
        canvas.create_arc(x0,y0,x1,y1,fill=player.color,start=lastStart,
            extent=player.mana/totalMana*360)
        if(player.mana/totalMana == 1):
            canvas.create_oval(x0,y0,x1,y1,fill=player.color)
        lastStart = lastStart+player.mana/totalMana*360
        canvas.create_text(20,150+i*30,text="%s: %d" % (player,player.mana),
            fill=player.color, font="Halvetica 20", anchor=NW)
        i += 1
    canvas.create_arc(x0,y0,x1,y1,fill="white",start=lastStart,
        extent=360-lastStart)
    canvas.create_text(20,150+i*30,text="Unoccupied:%d"%(data.unoccupiedMana)
        ,fill="white",font="Halvetica 20", anchor=NW)
    canvas.create_text(50,135,text="Predicted Mana Next Turn"
        ,fill="white",font="Times 20",anchor=W)

def playRedrawAll(canvas, data):
    if(not data.isPlayInited):
        playInit(data)
        data.isPlayInited = True
    canvas.create_image(data.width/2,data.height/2,image=
        data.gameBackground.form)    
    canvas.create_image(450,30,image=data.button1image)
    if(data.ttDemoPage != None):
        canvas.create_text(450,30,text="Tutorial Demo %d" % (data.ttDemoPage+1),
            font="ComicSansMS 15")
    elif(data.challengeChapter != None):
        canvas.create_text(450,30,text=data.challengeChapter,
            font="ComicSansMS 15")
    else:        
        canvas.create_text(450,30,text="Chapter %d" % (data.chapter+1),
            font="ComicSansMS 15")
    if(data.showPrologue):
        drawPrologue(canvas,data)
        return
    for row in range(10):
        for col in range(10):
            if(data.squares[row][col] != None):
                data.squares[row][col].draw(canvas,data)
    if(data.selectedCreature != None):
        data.selectedCreature.draw(canvas,data)
    for row in range(10):
        for col in range(10):                
            if(data.creatures[row][col] != None):
                if(data.selectedCreature == None or
                    data.creatures[row][col] != data.selectedCreature):
                    data.creatures[row][col].draw(canvas,data)
    canvas.create_image(130,90,image=data.button2image)
    canvas.create_text(130,90,text="%s's turn\nYour mana: %d"%
        (data.curPlayer,data.curMana),
        font="Halvetica 19",fill=data.curPlayer.color)
    drawManaPie(canvas,data)
    for button in data.buttons:
        button.draw(canvas,data)
    if(data.isGameOver and data.winner == data.player1):
        canvas.create_text(data.width/2,data.height/2,
            text="You win! \nPress r to continue",
            font="ComicSansMS 50")
    elif(data.isGameOver and data.winner != data.player1):
        canvas.create_text(data.width/2,data.height/2,
            text="You lose! \nPress r to restart",
            font="ComicSansMS 50")
    elif(data.curPlayer.isAI):
        canvas.create_text(data.width/2,data.height/2-200,
            text="AI's Turn",font="ComicSansMS 50")      

####################################
# use the run function as-is (Copied from 112 Course notes)
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        # canvas.coords()
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # create the root and the canvas
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(900, 600)