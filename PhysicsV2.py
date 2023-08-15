import pygame
import math
from pygame.locals import *
pygame.init()

#----------------------basic variables------------------
clock = pygame.time.Clock()
controls = False
addObjectMenu = False
recieveText = False
userText = ""
xVelocity = ""
yVelocity = ""
radius = ""
mass = ""
xVelocityBoxClicked = False
yVelocityBoxClicked = False
massBoxClicked = False
radiusBoxClicked = False
xVelocityDebounce = False
yVelocityDebounce = False
massDebounce = False
radiusDebounce = False
anyBoxClicked = False
createObject = False
objectNumber = 0
gravity = 0
noCollide = False
negx = False
negy = False
objectsColliding = False
objectsDoneColliding = False
selectMoveRight = False
selectMoveLeft = False
indexSelect = 0
applyLeftVelocity = False
applyRightVelocity = False
applyUpVelocity = False
applyDownVelocity = False
deleteObject = False
invertAddObjectX = False
invertAddObjectY = False
addObjectMenuPlacement = pygame.mouse.get_pos()
origin = (400, 400)
framesPassed = 0
pixelShift = 0
fillSurface = pygame.Rect(0,0,800,800)

#physics constants
frictionCoefficient = 0.5
impactDuration = 0.05

#colors
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
lime = (130,255,0)
gray = (50,50,50)
orange = (255,165,0)

#display setup
physicsBorder = pygame.Rect(25, 25, 750, 750)
displaySurf = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Pysics")

#stored object physics values
class screenObject:
    def __init__(self, xLocation, yLocation, xVelocity, yVelocity, mass, radius, selected, colliding, xMomentum, yMomentum, angle, angleVelocity, angleMomentum):
        self.xLocation = xLocation
        self.yLocation = yLocation
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.mass = mass
        self.radius = float(radius)
        self.selected = selected
        self.colliding = colliding
        self.xMomentum = xMomentum
        self.yMomentum = yMomentum
        self.angleVelocity = angleVelocity
        self.angleMomentum = angleMomentum
        self.angle = angle
        self.momentOfInertia = (1/2) * self.mass * (self.radius * self.radius)

#objects to be drawn on the screen
currentObjects = []

#-------------main loop-------------
running = True
while running:
    #checks status of text boxes
    if not xVelocityBoxClicked and not yVelocityBoxClicked and not massBoxClicked and not  radiusBoxClicked:
        anyBoxClicked = False
    else:
        anyBoxClicked = True

    #framerate
    clock.tick(600)

    #get mouse position
    mouse = pygame.mouse.get_pos()

    #event handler
    for event in pygame.event.get():
        #close window
        if event.type == pygame.QUIT:
            running = False

        #mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            #check controls button
            if 1050 <= mouse[0] <= 1175 and 75 <= mouse[1] <= 100 and not controls:
                controls = True
                displaySurf.fill(black)
            elif 1050 <= mouse[0] <= 1175 and 75 <= mouse[1] <= 100 and controls:
                controls = False
                displaySurf.fill(black)

            #check add object text boxes
            if not invertAddObjectX and not invertAddObjectY:
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] + 45 <= mouse[1] <= addObjectMenuPlacement[1] + 70 and not anyBoxClicked and event.button == 1:
                    xVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] + 75 <= mouse[1] <= addObjectMenuPlacement[1] + 100 and not anyBoxClicked and event.button == 1:
                    yVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] + 105 <= mouse[1] <= addObjectMenuPlacement[1] + 130 and not anyBoxClicked and event.button == 1:
                    massBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] + 135 <= mouse[1] <= addObjectMenuPlacement[1] + 160 and not anyBoxClicked and event.button == 1:
                    radiusBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 150 <= mouse[0] <= addObjectMenuPlacement[0] + 200 and addObjectMenuPlacement[1] + 165 <= mouse[1] <= addObjectMenuPlacement[1] + 195 and not anyBoxClicked and event.button == 1:
                    createObject = True
                    objectNumber += 1
            
            elif invertAddObjectX and not invertAddObjectY:
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] + 45 <= mouse[1] <= addObjectMenuPlacement[1] + 70 and not anyBoxClicked and event.button == 1:
                    xVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] + 75 <= mouse[1] <= addObjectMenuPlacement[1] + 100 and not anyBoxClicked and event.button == 1:
                    yVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] + 105 <= mouse[1] <= addObjectMenuPlacement[1] + 130 and not anyBoxClicked and event.button == 1:
                    massBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] + 135 <= mouse[1] <= addObjectMenuPlacement[1] + 160 and not anyBoxClicked and event.button == 1:
                    radiusBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 150 <= mouse[0] <= addObjectMenuPlacement[0] - 100 and addObjectMenuPlacement[1] + 165 <= mouse[1] <= addObjectMenuPlacement[1] + 195 and not anyBoxClicked and event.button == 1:
                    createObject = True
                    objectNumber += 1
            
            elif not invertAddObjectX and invertAddObjectY:
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] - 155 <= mouse[1] <= addObjectMenuPlacement[1] - 130 and not anyBoxClicked and event.button == 1:
                    xVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] - 125 <= mouse[1] <= addObjectMenuPlacement[1] - 100 and not anyBoxClicked and event.button == 1:
                    yVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] - 95 <= mouse[1] <= addObjectMenuPlacement[1] - 70 and not anyBoxClicked and event.button == 1:
                    massBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 160 <= mouse[0] <= addObjectMenuPlacement[0] + 190 and addObjectMenuPlacement[1] - 65 <= mouse[1] <= addObjectMenuPlacement[1] - 40 and not anyBoxClicked and event.button == 1:
                    radiusBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] + 150 <= mouse[0] <= addObjectMenuPlacement[0] + 200 and addObjectMenuPlacement[1] - 35 <= mouse[1] <= addObjectMenuPlacement[1] - 5 and not anyBoxClicked and event.button == 1:
                    createObject = True
                    objectNumber += 1

            elif invertAddObjectX and invertAddObjectY:
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] - 155 <= mouse[1] <= addObjectMenuPlacement[1] - 130 and not anyBoxClicked and event.button == 1:
                    xVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] - 125 <= mouse[1] <= addObjectMenuPlacement[1] - 100 and not anyBoxClicked and event.button == 1:
                    yVelocityBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] - 95 <= mouse[1] <= addObjectMenuPlacement[1] - 70 and not anyBoxClicked and event.button == 1:
                    massBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 140 <= mouse[0] <= addObjectMenuPlacement[0] - 110 and addObjectMenuPlacement[1] - 65 <= mouse[1] <= addObjectMenuPlacement[1] - 40 and not anyBoxClicked and event.button == 1:
                    radiusBoxClicked = True
                    recieveText = True
                    userText = ""
                if addObjectMenuPlacement[0] - 150 <= mouse[0] <= addObjectMenuPlacement[0] - 100 and addObjectMenuPlacement[1] - 35 <= mouse[1] <= addObjectMenuPlacement[1] - 5 and not anyBoxClicked and event.button == 1:
                    createObject = True
                    objectNumber += 1

            #add object right click menu
            if event.button == 3:
                if 25 < mouse[0] and 25 < mouse[1] and not recieveText:
                    if mouse[0] > 475:
                        #invert x orientation of menu
                        invertAddObjectX = True
                    else:
                        invertAddObjectX = False
                    if mouse[1] > 575:
                        #invert y orientation of menu
                        invertAddObjectY = True
                    else:
                        invertAddObjectY = False
                    if mouse[0] > 475 and mouse[1] > 575:
                        invertAddObjectX = True
                        invertAddObjectY = True
                    #gets position of mouse and does not change it every frame
                    #required to keep menus in place
                    #may need multiple later to make sure menus dont overlap
                    addObjectMenuPlacement = pygame.mouse.get_pos()

                    addObjectMenu = True

        #add object enter to quit typing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                xVelocityBoxClicked = False
                recieveText = False
                yVelocityBoxClicked = False
                massBoxClicked = False
                radiusBoxClicked = False
            
            #gravity change
            if event.key == pygame.K_EQUALS:
                gravity += 1
            if event.key == pygame.K_MINUS:
                gravity -= 1
            
            #ball selection
            if event.key == pygame.K_COMMA:
                selectMoveLeft = True
            if event.key == pygame.K_PERIOD:
                selectMoveRight = True
            if event.key == pygame.K_UP:
                applyUpVelocity = True
            if event.key == pygame.K_DOWN:
                applyDownVelocity = True
            if event.key == pygame.K_LEFT:
                applyLeftVelocity = True
            if event.key == pygame.K_RIGHT:
                applyRightVelocity = True
                
            #delete function
            if event.key == pygame.K_d:
                deleteObject = True
            
            #typing
            if recieveText:
                if event.key == pygame.K_BACKSPACE:
                    userText = userText[:-1]
                else:
                    userText += event.unicode
       
    #mouse dependent menus
    addObjectBorder = pygame.Rect(addObjectMenuPlacement[0], addObjectMenuPlacement[1], 300, 200)
    xVelocityTextBox = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 45, 40, 25)
    yVelocityTextBox = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 75, 40, 25)
    massTextBox = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 105, 40, 25)
    radiusTextBox = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 135, 40, 25)

    addObjectBorderInvertX = pygame.Rect(addObjectMenuPlacement[0] - 300, addObjectMenuPlacement[1], 300, 200)
    xVelocityTextBoxInvertX = pygame.Rect(addObjectMenuPlacement[0] -140, addObjectMenuPlacement[1] + 45, 40, 25)
    yVelocityTextBoxInvertX = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 75, 40, 25)
    massTextBoxInvertX = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 105, 40, 25)
    radiusTextBoxInvertX = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 135, 40, 25)

    addObjectBorderInvertY = pygame.Rect(addObjectMenuPlacement[0], addObjectMenuPlacement[1] - 200, 300, 200)
    xVelocityTextBoxInvertY = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 155, 40, 25)
    yVelocityTextBoxInvertY = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 125, 40, 25)
    massTextBoxInvertY = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 95, 40, 25)
    radiusTextBoxInvertY = pygame.Rect(addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 65, 40, 25)

    addObjectBorderInvert = pygame.Rect(addObjectMenuPlacement[0] - 300, addObjectMenuPlacement[1] - 200, 300, 200)
    xVelocityTextBoxInvert = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 155, 40, 25)
    yVelocityTextBoxInvert = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 125, 40, 25)
    massTextBoxInvert = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 95, 40, 25)
    radiusTextBoxInvert = pygame.Rect(addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 65, 40, 25)
    
    #redraw screen ever loop
    displaySurf.fill(black, fillSurface)
    pygame.draw.rect(displaySurf, white, physicsBorder, 1)
    titleFont = pygame.font.SysFont("Arial",20)
    titleText = titleFont.render("Pysics: A Python Based Physics Simulator", False, lime, black)
    displaySurf.blit(titleText, (800,25))

    #controls menu
    if controls:
        controlButton = titleFont.render("Close Controls", False, black, white)
        displaySurf.blit(controlButton, (1050, 75))
        controlTitleText = titleFont.render("Controls", False, white, black)
        displaySurf.blit(controlTitleText, (950, 100))
        controlLine2 = titleFont.render("Right click inside box to create a new object", False, white, black)
        displaySurf.blit(controlLine2, (790, 150))
        controlLine3 = titleFont.render("D - delete selected object", False, white, black)
        displaySurf.blit(controlLine3, (790, 175))
        controlLine4 = titleFont.render("right arrow - apply positive velocity on x axis", False, white, black)
        displaySurf.blit(controlLine4, (790, 200))
        controlLine5 = titleFont.render("left arrow - apply negative velocity on x axis", False, white, black)
        displaySurf.blit(controlLine5, (790, 225))
        controlLine6 = titleFont.render("up arrow - apply positive velocity on y axis", False, white, black)
        displaySurf.blit(controlLine6, (790, 250))
        controlLine7 = titleFont.render("down arrow - apply negative velocity on y axis", False, white, black)
        displaySurf.blit(controlLine7, (790, 275))
        controlLine8 = titleFont.render("plus/equals - increase gravity", False, white, black)
        displaySurf.blit(controlLine8, (790, 300))
        controlLine9 = titleFont.render("minus/dash - decrease gravity", False, white, black)
        displaySurf.blit(controlLine9, (790, 325))
        controlLine10 = titleFont.render("comma/< - scroll left on object selection", False, white, black)
        displaySurf.blit(controlLine10, (790, 350))
        controlLine11 = titleFont.render("period/> - scroll right on object selection", False, white, black)
        displaySurf.blit(controlLine11, (790, 375))
    else:
        controlButton = titleFont.render("Controls", False, black, white)
        displaySurf.blit(controlButton, (1100, 75))
    
    #add object menu
    if addObjectMenu:
        if invertAddObjectX and not invertAddObjectY:
            #draw inverted x axis orientaion
            #title inverted x
            pygame.draw.rect(displaySurf, red, addObjectBorderInvertX, 2)
            addObjectTitle = titleFont.render("Add an Object", False, white, black)
            displaySurf.blit(addObjectTitle, (addObjectMenuPlacement[0] - 210, addObjectMenuPlacement[1] + 10))

            #x velocity label inverted x
            addObjectXVelocityLabel = titleFont.render("Initial X Velocity:", False, white, black)
            displaySurf.blit(addObjectXVelocityLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] + 45))
            if not xVelocityDebounce and not xVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, xVelocityTextBoxInvertX)
            elif xVelocityDebounce and not xVelocityBoxClicked:
                xVelocityText = titleFont.render(xVelocity, False, green, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 45))
            if xVelocityBoxClicked:
                xVelocityDebounce = True
                xVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 45))
                xVelocity = userText

            #y velocity label inverted x
            addObjectYVelocityLabel = titleFont.render("Initial Y Velocity:", False, white, black)
            displaySurf.blit(addObjectYVelocityLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] + 75))
            if not yVelocityDebounce and not yVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, yVelocityTextBoxInvertX)
            elif yVelocityDebounce and not yVelocityBoxClicked:
                yVelocityText = titleFont.render(yVelocity, False, green, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 75))
            if yVelocityBoxClicked:
                yVelocityDebounce = True
                yVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 75))
                yVelocity = userText

            #mass label inverted x
            addObjectMassLabel = titleFont.render("Object Mass:", False, white, black)
            displaySurf.blit(addObjectMassLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] + 105))
            if not massDebounce and not massBoxClicked:
                pygame.draw.rect(displaySurf, gray, massTextBoxInvertX)
            elif massDebounce and not massBoxClicked:
                massText = titleFont.render(mass, False, green, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 105))
            if massBoxClicked:
                massDebounce = True
                massText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 105))
                mass = userText

            #radius label inverted x
            addObjectRadiusLabel = titleFont.render("Object Radius:", False, white, black)
            displaySurf.blit(addObjectRadiusLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] + 135))
            if not radiusDebounce and not radiusBoxClicked:
                pygame.draw.rect(displaySurf, gray, radiusTextBoxInvertX)
            elif radiusDebounce and not radiusBoxClicked:
                radiusText = titleFont.render(radius, False, green, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 135))
            if radiusBoxClicked:
                radiusDebounce = True
                radiusText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] + 135))
                radius = userText

            #create button inverted x
            createButtonText = titleFont.render("Create", False, white, red)
            displaySurf.blit(createButtonText, (addObjectMenuPlacement[0] - 150, addObjectMenuPlacement[1] + 165))
            if createObject:
                pygame.draw.circle(displaySurf, red, addObjectMenuPlacement, 3)
                currentObjects.append(screenObject(addObjectMenuPlacement[0], addObjectMenuPlacement[1], float(xVelocity), float(yVelocity), float(mass), radius, False, -1, float(mass)*float(xVelocity), float(mass)*float(yVelocity), 0, 0, 0))
                createObject = False
                addObjectMenu = False
                invertAddObjectX = False
        
        elif invertAddObjectY and not invertAddObjectX:
            #draw inverted y add object menu orientation
            #title
            pygame.draw.rect(displaySurf, red, addObjectBorderInvertY, 2)
            addObjectTitle = titleFont.render("Add an Object", False, white, black)
            displaySurf.blit(addObjectTitle, (addObjectMenuPlacement[0] + 90, addObjectMenuPlacement[1] - 190))

            #x velocity label invert y
            addObjectXVelocityLabel = titleFont.render("Initial X Velocity:", False, white, black)
            displaySurf.blit(addObjectXVelocityLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] - 155))
            if not xVelocityDebounce and not xVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, xVelocityTextBoxInvertY)
            elif xVelocityDebounce and not xVelocityBoxClicked:
                xVelocityText = titleFont.render(xVelocity, False, green, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 155))
            if xVelocityBoxClicked:
                xVelocityDebounce = True
                xVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 155))
                xVelocity = userText

            #y velocity label invert y
            addObjectYVelocityLabel = titleFont.render("Initial Y Velocity:", False, white, black)
            displaySurf.blit(addObjectYVelocityLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] - 125))
            if not yVelocityDebounce and not yVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, yVelocityTextBoxInvertY)
            elif yVelocityDebounce and not yVelocityBoxClicked:
                yVelocityText = titleFont.render(yVelocity, False, green, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 125))
            if yVelocityBoxClicked:
                yVelocityDebounce = True
                yVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 125))
                yVelocity = userText

            #mass label invert y
            addObjectMassLabel = titleFont.render("Object Mass:", False, white, black)
            displaySurf.blit(addObjectMassLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] - 95))
            if not massDebounce and not massBoxClicked:
                pygame.draw.rect(displaySurf, gray, massTextBoxInvertY)
            elif massDebounce and not massBoxClicked:
                massText = titleFont.render(mass, False, green, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 95))
            if massBoxClicked:
                massDebounce = True
                massText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 95))
                mass = userText

            #radius label invert y
            addObjectRadiusLabel = titleFont.render("Object Radius:", False, white, black)
            displaySurf.blit(addObjectRadiusLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] - 65))
            if not radiusDebounce and not radiusBoxClicked:
                pygame.draw.rect(displaySurf, gray, radiusTextBoxInvertY)
            elif radiusDebounce and not radiusBoxClicked:
                radiusText = titleFont.render(radius, False, green, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 65))
            if radiusBoxClicked:
                radiusDebounce = True
                radiusText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] - 65))
                radius = userText
    
            #create button invert y
            createButtonText = titleFont.render("Create", False, white, red)
            displaySurf.blit(createButtonText, (addObjectMenuPlacement[0] + 150, addObjectMenuPlacement[1] - 35))
            if createObject:
                pygame.draw.circle(displaySurf, red, addObjectMenuPlacement, 3)
                currentObjects.append(screenObject(addObjectMenuPlacement[0], addObjectMenuPlacement[1], float(xVelocity), float(yVelocity), float(mass), radius, False, -1, float(mass)*float(xVelocity), float(mass)*float(yVelocity), 0, 0, 0))
                createObject = False
                addObjectMenu = False

        elif invertAddObjectX and invertAddObjectY:
            #draw both axis inverted orientation
            #title
            pygame.draw.rect(displaySurf, red, addObjectBorderInvert, 2)
            addObjectTitle = titleFont.render("Add an Object", False, white, black)
            displaySurf.blit(addObjectTitle, (addObjectMenuPlacement[0] - 210, addObjectMenuPlacement[1] - 190))

            #x velocity label invert both
            addObjectXVelocityLabel = titleFont.render("Initial X Velocity:", False, white, black)
            displaySurf.blit(addObjectXVelocityLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] - 155))
            if not xVelocityDebounce and not xVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, xVelocityTextBoxInvert)
            elif xVelocityDebounce and not xVelocityBoxClicked:
                xVelocityText = titleFont.render(xVelocity, False, green, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 155))
            if xVelocityBoxClicked:
                xVelocityDebounce = True
                xVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 155))
                xVelocity = userText

            #y velocity label invert both
            addObjectYVelocityLabel = titleFont.render("Initial Y Velocity:", False, white, black)
            displaySurf.blit(addObjectYVelocityLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] - 125))
            if not yVelocityDebounce and not yVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, yVelocityTextBoxInvert)
            elif yVelocityDebounce and not yVelocityBoxClicked:
                yVelocityText = titleFont.render(yVelocity, False, green, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 125))
            if yVelocityBoxClicked:
                yVelocityDebounce = True
                yVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 125))
                yVelocity = userText

            #mass label invert both
            addObjectMassLabel = titleFont.render("Object Mass:", False, white, black)
            displaySurf.blit(addObjectMassLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] - 95))
            if not massDebounce and not massBoxClicked:
                pygame.draw.rect(displaySurf, gray, massTextBoxInvert)
            elif massDebounce and not massBoxClicked:
                massText = titleFont.render(mass, False, green, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 95))
            if massBoxClicked:
                massDebounce = True
                massText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 95))
                mass = userText

            #radius label invert both
            addObjectRadiusLabel = titleFont.render("Object Radius:", False, white, black)
            displaySurf.blit(addObjectRadiusLabel, (addObjectMenuPlacement[0] - 290, addObjectMenuPlacement[1] - 65))
            if not radiusDebounce and not radiusBoxClicked:
                pygame.draw.rect(displaySurf, gray, radiusTextBoxInvert)
            elif radiusDebounce and not radiusBoxClicked:
                radiusText = titleFont.render(radius, False, green, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 65))
            if radiusBoxClicked:
                radiusDebounce = True
                radiusText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] - 140, addObjectMenuPlacement[1] - 65))
                radius = userText
        
            #create button
            createButtonText = titleFont.render("Create", False, white, red)
            displaySurf.blit(createButtonText, (addObjectMenuPlacement[0] - 150, addObjectMenuPlacement[1] - 35))
            if createObject:
                pygame.draw.circle(displaySurf, red, addObjectMenuPlacement, 3)
                currentObjects.append(screenObject(addObjectMenuPlacement[0], addObjectMenuPlacement[1], float(xVelocity), float(yVelocity), float(mass), radius, False, -1, float(mass)*float(xVelocity), float(mass)*float(yVelocity), 0, 0, 0))
                createObject = False
                addObjectMenu = False
        else:
            #draw regular orientation
            #title
            pygame.draw.rect(displaySurf, red, addObjectBorder, 2)
            addObjectTitle = titleFont.render("Add an Object", False, white, black)
            displaySurf.blit(addObjectTitle, (addObjectMenuPlacement[0] + 90, addObjectMenuPlacement[1] + 10))

            #x velocity label
            addObjectXVelocityLabel = titleFont.render("Initial X Velocity:", False, white, black)
            displaySurf.blit(addObjectXVelocityLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] + 45))
            if not xVelocityDebounce and not xVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, xVelocityTextBox)
            elif xVelocityDebounce and not xVelocityBoxClicked:
                xVelocityText = titleFont.render(xVelocity, False, green, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 45))
            if xVelocityBoxClicked:
                xVelocityDebounce = True
                xVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(xVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 45))
                xVelocity = userText

            #y velocity label
            addObjectYVelocityLabel = titleFont.render("Initial Y Velocity:", False, white, black)
            displaySurf.blit(addObjectYVelocityLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] + 75))
            if not yVelocityDebounce and not yVelocityBoxClicked:
                pygame.draw.rect(displaySurf, gray, yVelocityTextBox)
            elif yVelocityDebounce and not yVelocityBoxClicked:
                yVelocityText = titleFont.render(yVelocity, False, green, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 75))
            if yVelocityBoxClicked:
                yVelocityDebounce = True
                yVelocityText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(yVelocityText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 75))
                yVelocity = userText

            #mass label
            addObjectMassLabel = titleFont.render("Object Mass:", False, white, black)
            displaySurf.blit(addObjectMassLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] + 105))
            if not massDebounce and not massBoxClicked:
                pygame.draw.rect(displaySurf, gray, massTextBox)
            elif massDebounce and not massBoxClicked:
                massText = titleFont.render(mass, False, green, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 105))
            if massBoxClicked:
                massDebounce = True
                massText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(massText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 105))
                mass = userText

            #radius label
            addObjectRadiusLabel = titleFont.render("Object Radius:", False, white, black)
            displaySurf.blit(addObjectRadiusLabel, (addObjectMenuPlacement[0] + 10, addObjectMenuPlacement[1] + 135))
            if not radiusDebounce and not radiusBoxClicked:
                pygame.draw.rect(displaySurf, gray, radiusTextBox)
            elif radiusDebounce and not radiusBoxClicked:
                radiusText = titleFont.render(radius, False, green, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 135))
            if radiusBoxClicked:
                radiusDebounce = True
                radiusText = titleFont.render(userText, False, white, gray)
                displaySurf.blit(radiusText, (addObjectMenuPlacement[0] + 160, addObjectMenuPlacement[1] + 135))
                radius = userText
        
            #create button
            createButtonText = titleFont.render("Create", False, white, red)
            displaySurf.blit(createButtonText, (addObjectMenuPlacement[0] + 150, addObjectMenuPlacement[1] + 165))
            if createObject:
                pygame.draw.circle(displaySurf, red, addObjectMenuPlacement, 3)
                if xVelocity == "":
                    xVelocity = 0
                if yVelocity == "":
                    yVelocity = 0
                if mass == "":
                    mass = 1
                if radius == "":
                    radius = 3
                currentObjects.append(screenObject(addObjectMenuPlacement[0], addObjectMenuPlacement[1], float(xVelocity), float(yVelocity), float(mass), radius, False, -1, float(mass)*float(xVelocity), float(mass)*float(yVelocity), 0, 0, 0))
                createObject = False
                addObjectMenu = False

        
        
    #gravity label
    gravityString = str(gravity)
    negativeGravityString = str(-gravity)
    if gravity >= 10:
        gravityLabelText = titleFont.render("Gravity:" + gravityString[0] + "." + gravityString[1], False, white, blue)
    elif gravity < 0:
        gravityLabelText = titleFont.render("Gravity:" + "-0." + negativeGravityString[0] , False, white, blue)
    else:
        gravityLabelText = titleFont.render("Gravity:" + "0." + gravityString[0] , False, white, blue)
    displaySurf.blit(gravityLabelText, (825, 75))


    #physics calculations
    for object in currentObjects:        

        #calculate momentum for possible later use
        object.xMomentum = object.mass * object.xVelocity
        object.yMomentum = object.mass * object.yVelocity
        
        object.angleMomentum = object.angleVelocity * object.momentOfInertia

        #object selection
        currentIndex = -1
        for x in currentObjects:
            currentIndex += 1
            if selectMoveLeft and indexSelect != 0:
                indexSelect -= 1
                selectMoveLeft = False
                framesPassed = 0
                displaySurf.fill(black)
            else:
                selectMoveLeft = False
            if selectMoveRight and indexSelect != (len(currentObjects) - 1):
                indexSelect += 1
                selectMoveRight = False
                framesPassed = 0
                displaySurf.fill(black)
            else: 
                selectMoveRight = False
            if currentIndex == indexSelect:
                x.selected = True
            else:
                x.selected = False
            
            #velocity change
            if applyLeftVelocity and x.selected:
                x.xVelocity -= 1
                applyLeftVelocity = False
            if applyRightVelocity and x.selected:
                x.xVelocity += 1
                applyRightVelocity = False
            if applyUpVelocity and x.selected:
                x.yVelocity += 1
                applyUpVelocity = False
            if applyDownVelocity and x.selected:
                x.yVelocity -= 1
                applyDownVelocity = False

            #delete object function
            if deleteObject and x.selected:
                currentObjects.pop(indexSelect)
                deleteObject = False

        #collision detector
        currentIndex = -1
        objectsColliding = False
        for x in currentObjects:
            currentIndex += 1
            if object.xLocation == x.xLocation and object.yLocation == x.yLocation:
                noCollide = True
            else:
                noCollide = False
            if not noCollide:
                    #use correct object radius to prevent overlapping
                    if object.xLocation < x.xLocation + x.radius + object.radius and object.xLocation > x.xLocation - x.radius - object.radius:
                        if object.yLocation < x.yLocation + x.radius + object.radius and object.yLocation > x.yLocation - x.radius - object.radius:
                            object.colliding = currentIndex
                            objectsColliding = True

        #collision calculator
        if objectsDoneColliding:
            objectsDoneColliding = False
            object.colliding = -1
        if objectsColliding:
            indexValue = -1
            for x in currentObjects:
                indexValue += 1
                #only check values of colliding object index location
                if indexValue == currentIndex and not objectsDoneColliding:
                    #debounce
                    objectsDoneColliding = True

                    #swap momentum in both axis
                    tempx = object.xMomentum
                    object.xMomentum = x.xMomentum
                    x.xMomentum = tempx

                    tempy = object.yMomentum
                    object.yMomentum = x.yMomentum
                    x.yMomentum = tempy

                    #swap angular momentum
                    temp = object.angleMomentum
                    object.angleMomentum = x.angleMomentum
                    x.angleMomentum = temp

                    #calculate velocity
                    object.xVelocity = object.xMomentum / object.mass
                    object.yVelocity = object.yMomentum / object.mass
                    x.xVelocity = x.xMomentum / x.mass
                    x.yVelocity = x.yMomentum / x.mass

                    #calculate angle velocity
                    object.angleVelocity = object.angleMomentum / object.momentOfInertia
                    x.angleVelocity = x.angleMomentum / x.momentOfInertia

                    object.colliding = -1
                    currentIndex = -1

        #calculate movement based on velocity
        if object.xVelocity != 0:
            object.xLocation = object.xLocation + (object.xVelocity / 10)
        if object.yVelocity != 0:
            object.yLocation = object.yLocation - (object.yVelocity / 10)

        #calculate rotation based on angular velocity
        if object.angleVelocity != 0:
            object.angle = object.angle + (object.angleVelocity / 10)

        #objects collide with border
        xImpactForce = object.mass * ((2 * object.xVelocity) / impactDuration)
        xFrictionForce = frictionCoefficient * xImpactForce
        xAngularAcceleration = xFrictionForce / object.mass

        yImpactForce = object.mass * ((2 * object.yVelocity) / impactDuration)
        yFrictionForce = frictionCoefficient * yImpactForce
        yAngularAcceleration = yFrictionForce / object.mass
        
        if object.xLocation >= 775 - object.radius:
            object.xLocation = 775 - object.radius

            if object.yVelocity > 0:
                object.angleVelocity = object.angleVelocity + (xAngularAcceleration * impactDuration)
            if object.yVelocity < 0:
                object.angleVelocity = object.angleVelocity - (xAngularAcceleration * impactDuration)

        if object.yLocation >= 775 - object.radius:
            object.yLocation = 775 - object.radius
            
            if object.xVelocity > 0:
                object.angleVelocity = object.angleVelocity - (yAngularAcceleration * impactDuration)
            if object.xVelocity < 0:
                object.angleVelocity = object.angleVelocity + (yAngularAcceleration * impactDuration)
        
        if object.xLocation <= 25 + object.radius:
            object.xLocation = 25 + object.radius
            
            if object.yVelocity > 0:
                object.angleVelocity = object.angleVelocity + (xAngularAcceleration * impactDuration)
            if object.yVelocity < 0:
                object.angleVelocity = object.angleVelocity - (xAngularAcceleration * impactDuration)
        
        if object.yLocation <= 25 + object.radius:
            object.yLocation = 25 + object.radius
            
            if object.xVelocity > 0:
                object.angleVelocity = object.angleVelocity - (yAngularAcceleration * impactDuration)        
            if object.xVelocity < 0:
                object.angleVelocity = object.angleVelocity + (yAngularAcceleration * impactDuration)
                
                
        
        #wall collisions
        if object.xLocation == (775 - object.radius) or object.xLocation == (25 + object.radius):
            object.xVelocity = -object.xVelocity
        if object.yLocation == (775 - object.radius) or object.yLocation == (25 + object.radius):
            object.yVelocity = -object.yVelocity
        
        #gravity
        object.yVelocity = object.yVelocity - (gravity / 100)
            
        #vector drawing
        pygame.draw.line(displaySurf, blue, (object.xLocation, object.yLocation), (object.xLocation + object.xVelocity * 2 , object.yLocation - object.yVelocity * 2))
        if not object.selected:
            pygame.draw.circle(displaySurf, red, (object.xLocation, object.yLocation), object.radius)
        elif object.selected:
            pygame.draw.circle(displaySurf, blue, (object.xLocation, object.yLocation), object.radius)

        #angle line drawing
        #find line end point coordinates
        angleRadians = float(object.angle) * (math.pi/180)
        angleLineX = object.radius * math.cos(angleRadians)
        angleLineY = object.radius * math.sin(angleRadians)

        pygame.draw.line(displaySurf, orange, (object.xLocation, object.yLocation), (object.xLocation + angleLineX, object.yLocation + angleLineY), 1)

        #graph drawing    
        if not controls and object.selected:
            #x velocity graph
            pygame.draw.line(displaySurf, white, (800, 150), (800, 300))
            pygame.draw.line(displaySurf, white, (800, 225), (950, 225))
            xVelocityGraphTitle = titleFont.render("X Velocity", False, white, black)
            displaySurf.blit(xVelocityGraphTitle, (845, 315))

            pixelShift = round(framesPassed / 50)

            xGraphDotYLocation = 225 - (object.xVelocity * 2)
            xGraphDotXLocation = 800 + pixelShift
            
            #if the dot off the graph dont draw the dot
            if 150 < xGraphDotYLocation < 300:
                pygame.draw.circle(displaySurf, blue, (xGraphDotXLocation, xGraphDotYLocation), 1)
            
            #y velocity graph
            pygame.draw.line(displaySurf, white, (1000, 150), (1000, 300))
            pygame.draw.line(displaySurf, white, (1000, 225), (1150, 225))
            yVelocityGraphTitle = titleFont.render("Y Velocity", False, white, black)
            displaySurf.blit(yVelocityGraphTitle, (1040, 315))

            yGraphDotYLocation = 225 - (object.yVelocity * 2)
            yGraphDotXLocation = 1001 + pixelShift

            #if the dot off the graph dont draw the dot
            if 150 < yGraphDotYLocation < 300:
                pygame.draw.circle(displaySurf, blue, (yGraphDotXLocation, yGraphDotYLocation), 1)
            
            #speed graph
            pygame.draw.line(displaySurf, white, (800, 350), (800, 500))
            pygame.draw.line(displaySurf, white, (800, 500), (950, 500))
            speedGraphTitle = titleFont.render("Speed", False, white, black)
            displaySurf.blit(speedGraphTitle, (845, 530))

            speed = math.sqrt((object.xVelocity * object.xVelocity) + (object.yVelocity * object.yVelocity))

            speedGraphDotYLocation = 500 - (speed * 2)
            speedGraphDotXLocation = 800 + pixelShift
    
            if 350 < speedGraphDotYLocation < 500:
                pygame.draw.circle(displaySurf, green, (speedGraphDotXLocation, speedGraphDotYLocation), 1)

            #angular velocity graph
            pygame.draw.line(displaySurf, white, (1000, 350), (1000, 500))
            pygame.draw.line(displaySurf, white, (1000, 425), (1150, 425))
            angularVelocityGraphTitle = titleFont.render("Angular Velocity", False, white, black)
            displaySurf.blit(angularVelocityGraphTitle, (1010, 530))

            angularVelocityGraphDotYLocation = 425 - (object.angleVelocity * 2)
            angularVelocityGraphDotXLocation = 1001 + pixelShift
            
            if 350 < angularVelocityGraphDotYLocation < 500:
                pygame.draw.circle(displaySurf, orange, (angularVelocityGraphDotXLocation, angularVelocityGraphDotYLocation), 1)
            #if dot reaches end of graph clear graph and start at beginning
            if pixelShift == 150:
                framesPassed = 0
                displaySurf.fill(black)
        if controls:
            framesPassed = 0

    #check if objects exist before frames start counting
    #makes sure graphs start at x = 0
    if not(len(currentObjects) < 1):
        framesPassed += 1

    #update the display
    pygame.display.update()