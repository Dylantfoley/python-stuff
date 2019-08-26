import pygame as py
import sys
import math
from time import sleep
py.init()

class Game:
    def __init__(self,screen,screenDimensions):
        self.fps = 30
        self.screenDimensions = screenDimensions
        self.frame = py.time.Clock()
        self.screen = screen
    def updateFrame(self):
        self.frame.tick(self.fps)
        py.display.flip()

class Background(Game):
    def __init__(self,screen,screenDimensions):
        Game.__init__(self,screen,screenDimensions)
        self.goalLeft = None
        self.goalMiddle = None
        self.goalRight = None
        self.adjust = 12
        self.grassImage = None
    def loadGrass(self,name):
        self.grassImage = py.image.load(name).convert()
        self.grassImage = py.transform.scale(self.grassImage, self.screenDimensions)

    def cropSurface(self, newWidth, newHeight, cropWidth, cropHeight, image):
        newSurf = py.Surface((newWidth, newHeight),
                             py.SRCALPHA, 32)  # SRCALPHA deals with transparancy, 32 is bit 32bit
        newSurf.blit(image, (0, 0), (cropWidth, cropHeight,
                                     newWidth, newHeight))
        return newSurf

    def loadGoalLeft(self,name):
        self.goalLeft = py.image.load(name).convert_alpha()
        self.goalLeft = py.transform.scale(self.goalLeft, (250, 270))
        goalLeftWidth = self.goalLeft.get_rect().width
        goalLeftHeight = self.goalLeft.get_rect().height
        self.goalLeft = self.cropSurface(goalLeftWidth / 2 + self.adjust,
                               goalLeftHeight / 2 + self.adjust,
                               goalLeftWidth / 2 - self.adjust,
                               goalLeftHeight / 2 - self.adjust,
                               self.goalLeft)
    def loadGoalMiddle(self,name):
        self.goalMiddle = py.image.load(name).convert_alpha()
        self.goalMiddle = py.transform.scale(self.goalMiddle, (250, 270))
        goalMiddleWidth = self.goalMiddle.get_rect().width
        goalMiddleHeight = self.goalMiddle.get_rect().height
        self.goalMiddle = self.cropSurface(goalMiddleWidth,
                                 goalMiddleHeight / 2 + self.adjust,
                                 0,
                                 goalMiddleHeight / 2 - self.adjust,
                                 self.goalMiddle)
    def loadGoalRight(self,name):
        self.goalRight = py.image.load(name).convert_alpha()
        self.goalRight = py.transform.scale(self.goalRight, (250, 270))
        goalRightWidth = self.goalRight.get_rect().width
        goalRightHeight = self.goalRight.get_rect().height
        self.goalRight = self.cropSurface(goalRightWidth / 2 + self.adjust,
                                goalRightHeight / 2 + self.adjust,
                                0,
                                goalRightHeight / 2 - self.adjust,
                                self.goalRight)
    def setStart(self):
        self.goalStart = (self.screenDimensions[0] - self.goalLeft.get_rect().width -
                     self.goalMiddle.get_rect().width -
                     self.goalRight.get_rect().width) / 2
    def blitBackground(self):
        self.screen.blit(self.grassImage,(0,0))
        self.screen.blit(self.goalLeft, (self.goalStart, 0))
        self.screen.blit(self.goalMiddle, (self.goalStart + self.goalLeft.get_rect().width, 0))
        self.screen.blit(self.goalRight, (self.goalStart + self.goalLeft.get_rect().width + self.goalMiddle.get_rect().width, 0))

class Ball(Game):
    def __init__(self,screen,screenDimensions):
        Game.__init__(self,screen,screenDimensions)
        self.ballX = self.screenDimensions[0]/2
        self.ballXOriginal = self.ballX
        self.ballY = 450
        self.ballYOriginal =self.ballY
        self.ball = None
    def resetBall(self):
        self.ballX = self.ballXOriginal
        self.ballY = self.ballYOriginal
    def loadBall(self,name,rescaleBall):
        self.ball = py.image.load(name).convert_alpha()
        ballWidth = self.ball.get_rect().width
        ballHeight = self.ball.get_rect().height
        self.ball = py.transform.scale(self.ball, (ballWidth * rescaleBall,
                                         ballHeight * rescaleBall))
    def blitBall(self):
        self.screen.blit(self.ball,(self.ballX - self.ball.get_rect().width/2,
                                    self.ballY - self.ball.get_rect().height/2))
    def setKickDirection(self,playerX,playerY):
        xMove = (playerX - self.ballX) / 10
        yMove = (playerY - self.ballY) / 10
        normMove = 1 / math.sqrt(xMove ** 2 + yMove ** 2)
        self.ballXDirection = xMove * normMove
        self.ballYDirection = yMove * normMove
    def kickBall(self,speed):
        self.ballX -= speed * self.ballXDirection
        self.ballY -= speed * self.ballYDirection

class Player(Game):
    def __init__(self,screen,screenDimensions):
        Game.__init__(self,screen,screenDimensions)
        self.player = None
        self.playerStart = self.player
        self.foot = None
        self.footStart = self.foot
        self.playerX = self.screenDimensions[0]/2
        self.playerY = 530
        self.playerXOriginal = self.playerX
        self.playerYOriginal = self.playerY
        self.footX = None
        self.footY = None
        self.currentRotation = 0
        self.radius = 80
        self.deltaTheta = int(90/(self.radius/5))
        self.font = py.font.SysFont("Arial",25)
        self.score = 0
        self.scoreText = self.font.render(" Score: "+str(self.score),True,(255,255,255))
        self.username = None
    def setName(self,username):
        self.username = username
        self.scoreText = self.font.render(self.username+ " Score: " + str(self.score), True, (255, 255, 255))

    def scored(self):
        self.score +=1
        self.scoreText = self.font.render(self.username+ " Score: "+str(self.score),True,(255,255,255))

    def blitScore(self):
        self.screen.blit(self.scoreText,(800-self.scoreText.get_width()/2,50-self.scoreText.get_height()/2))

    def resetPlayer(self):
        self.playerX = self.playerXOriginal
        self.playerY = self.playerYOriginal
        self.currentRotation = 0
        self.rotatePlayer(self.currentRotation)
    def loadPlayer(self,name, rescale):
        self.player = py.image.load(name).convert_alpha()
        playerWidth = self.player.get_rect().width
        playerHeight = self.player.get_rect().height
        self.player = py.transform.scale(self.player,
                                         (playerWidth*rescale,
                                         playerHeight*rescale))
        self.player = py.transform.rotate(self.player,90)
        self.playerStart = self.player
    def loadFoot(self,name,rescale):
        self.foot = py.image.load(name).convert_alpha()
        footWidth = self.foot.get_rect().width
        footHeight = self.foot.get_rect().height
        self.foot = py.transform.scale(self.foot,
                                       (footWidth*rescale,
                                       footHeight*rescale))
        self.foot = py.transform.rotate(self.foot, 90)
        self.footStart = self.foot
    def rotatePlayer(self,angle):
        self.player = py.transform.rotate(self.playerStart,angle)
    def rotateFoot(self,angle):
        self.foot = py.transform.rotate(self.footStart,angle)
    def movePlayer(self,direction):
        if direction == "Left":
            self.deltaTheta *= -1
        finalRot = (self.currentRotation + self.deltaTheta) * math.pi / 180
        hypotenuse = self.radius * math.sin(finalRot) / \
                     ((math.sin((math.pi - finalRot) / 2)))
        changeX = hypotenuse * math.cos(math.pi / 2 - (math.pi - finalRot) / 2)
        changeY = hypotenuse * math.sin(math.pi / 2 - (math.pi - finalRot) / 2)

        self.currentRotation =self.currentRotation +self.deltaTheta
        self.player = py.transform.rotate(self.playerStart, self.currentRotation)
        self.playerX = self.playerXOriginal + changeX
        self.playerY = self.playerYOriginal - changeY

        if direction == "Left": #revert
            self.deltaTheta*=-1
    def blitPlayer(self):
        self.screen.blit(self.player,(self.playerX-self.player.get_rect().width/2,
                                      self.playerY-self.player.get_rect().height/2))
    def blitFoot(self):
        self.screen.blit(self.foot,(self.footX-self.foot.get_rect().width/2,
                                    self.footY-self.foot.get_rect().height/2))
    def playerShoot(self,ballX,ballY):
        xMove = (self.playerX-ballX)/10
        yMove = (self.playerY-ballY)/10
        self.playerX -= xMove
        self.playerY -= yMove

    def positionFoot(self,ballX,ballY):
        xMove = (self.playerX-ballX)/10
        yMove = (self.playerY-ballY)/10
        normMove = 1/math.sqrt(xMove**2+yMove**2)
        distanceToShoulder = 20
        shoulderAngle = self.currentRotation*math.pi/180
        self.footX = (self.playerX+
                      distanceToShoulder*math.cos(shoulderAngle)-
                      20*xMove*normMove)
        self.footY = (self.playerY -
                      distanceToShoulder*math.sin(shoulderAngle)-
                      20*yMove*normMove)
        self.foot = py.transform.rotate(self.footStart,self.currentRotation)

class Target(Game):
    def __init__(self,screen,screenDimensions,start,goalHeight,goalEnd):
        Game.__init__(self,screen,screenDimensions)
        self.targetX = start
        self.targetY = goalHeight
        self.target = None
        self.xDirection = 1
        self.goalEnd = goalEnd
        self.start = start
    def loadTarget(self,name):
        self.target = py.image.load(name).convert_alpha()
        self.target = py.transform.scale(self.target,(50,50))
        self.targetWidth = self.target.get_rect().width
        self.targetHeight = self.target.get_rect().height
    def blitTarget(self):
        self.screen.blit(self.target,(self.targetX,
                                      self.targetY-self.targetHeight/2))
    def moveTarget(self,speed):
        self.targetX +=self.xDirection*speed
        if self.targetX + self.targetWidth >= self.goalEnd -10:
            self.xDirection = -1
        elif self.targetX <= self.start+10:
            self.xDirection = 1
    def checkTargetHit(self,ballXLeft,ballWidth,ballYTop,ballHeight):
        ballBoxX = (ballXLeft, ballXLeft+ballWidth)
        ballBoxY = (ballYTop, ballYTop+ballHeight)
        targetBoxX = (self.targetX, self.targetX+self.targetWidth)
        targetBoxY = (self.targetY-self.targetHeight/2, self.targetY+self.targetHeight/2)
        if ballBoxX[0] >= targetBoxX[0] and ballBoxX[0] <= targetBoxX[1]:
            if ballBoxY[0] >= targetBoxY[0] and ballBoxY[0] <= targetBoxY[1]:
                return True
            if ballBoxY[1] >= targetBoxY[0] and ballBoxY[1] <= targetBoxY[1]:
                return True
        elif ballBoxX[1] >= targetBoxX[0] and ballBoxX[1] <= targetBoxX[1]:
            if ballBoxY[0] >= targetBoxY[0] and ballBoxY[0] <= targetBoxY[1]:
                return True
            if ballBoxY[1] >= targetBoxY[0] and ballBoxY[1] <= targetBoxY[1]:
                return True
        return False

def updateFrameImages(showFoot = False):
    global background,newPlayer,newBall,blitFoot
    background.blitBackground()
    newPlayer.blitScore()
    if showFoot:
        newPlayer.blitFoot()
    target.blitTarget()
    newPlayer.blitPlayer()
    newBall.blitBall()

width = 900
height = 700
screenDim = (width, height)

screen = py.display.set_mode(screenDim) #display is a class not function or variable
py.display.set_caption("First Game")

game = Game(screen,screenDim)
newPlayer = Player(screen,screenDim)
newBall = Ball(screen,screenDim)
background = Background(screen,screenDim)

background.loadGrass("Grass_11.png")

rescale = 3

newPlayer.loadPlayer("PNG/Blue/characterBlue (4).png",rescale)

newPlayer.loadFoot("PNG/Blue/characterBlue (14).png",rescale)

rescaleBall = 2
newBall.loadBall("ball_soccer2.png",rescaleBall)

background.loadGoalLeft("Goal left.png")
goalHeight = background.goalLeft.get_rect().height
background.loadGoalMiddle("goalMiddle.png")
background.loadGoalRight("goal Right.png")
background.setStart()
goalEnd = (background.goalStart+background.goalLeft.get_rect().width+
           background.goalMiddle.get_rect().width+
           background.goalRight.get_rect().width)
target = Target(screen,screenDim,background.goalStart,goalHeight,goalEnd)
target.loadTarget("Target.png")

background.blitBackground()
newPlayer.blitScore()
target.blitTarget()
newPlayer.blitPlayer()
newBall.blitBall()

username = input("What is you name")
newPlayer.setName(username)
print(username)

finished = False
hitTarget = False
while finished == False: #processes the events
    for event in py.event.get(): #goes through each of the events
        if event.type == py.QUIT:
            finished = True
            py.quit()
            sys.exit()

    pressedKeys = py.key.get_pressed() #array to know which keys are pressed
    if pressedKeys[py.K_LEFT] == 1: #left key has been pressed so move left
        if newPlayer.currentRotation > -90:
            newPlayer.movePlayer("Left")
    elif pressedKeys[py.K_RIGHT]==1:
        if newPlayer.currentRotation < 90:
            newPlayer.movePlayer("Right")

    elif pressedKeys[py.K_SPACE]==1: #Shoot the ball
        for i in range(3):
            target.moveTarget(5)
            newPlayer.playerShoot(newBall.ballX,newBall.ballY)
            updateFrameImages()
            game.updateFrame()

        newPlayer.positionFoot(newBall.ballX,newBall.ballY)
        updateFrameImages(True)
        game.updateFrame()

        newBall.setKickDirection(newPlayer.playerX,newPlayer.playerY)
        ballspeed = 15
        while newBall.ballY >= goalHeight:
            target.moveTarget(5)
            newBall.kickBall(ballspeed)

            ballWidth = newBall.ball.get_rect().width
            ballXLeft = newBall.ballX - ballWidth/2
            ballHeight = newBall.ball.get_rect().height
            ballYTop = newBall.ballY - ballHeight/2
            hitTarget =  target.checkTargetHit(ballXLeft,ballWidth,
                                               ballYTop,ballHeight)
            updateFrameImages()
            game.updateFrame()
        if hitTarget:
            newPlayer.scored()
            updateFrameImages()
            game.updateFrame()
            print("HIT!")
        newPlayer.resetPlayer()
        newBall.resetBall()
        sleep(1)
    target.moveTarget(5)
    updateFrameImages()
    game.updateFrame()






























