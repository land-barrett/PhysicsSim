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
gravity = 0.0
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

origin = (400, 400)

#colors
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
lime = (130,255,0)
gray = (50,50,50)

#display setup
physicsBorder = pygame.Rect(25, 25, 750, 750)
addObjectBorder = pygame.Rect(790, 450, 400, 300)
xVelocityTextBox = pygame.Rect(975, 490, 40, 25)
yVelocityTextBox = pygame.Rect(975, 520, 40, 25)
massTextBox = pygame.Rect(975, 550, 40, 25)
radiusTextBox = pygame.Rect(975, 580, 40, 25)
displaySurf = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Pysics")

#stored object physics values
class screenObject:
    def __init__(self, xLocation, yLocation, xVelocity, yVelocity, mass, radius, selected, colliding, xMomentum, yMomentum):
        self.xLocation = xLocation
        self.yLocation = yLocation
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.mass = mass
        self.radius = radius
        self.selected = selected
        self.colliding = colliding
        self.xMomentum = xMomentum
        self.yMomentum = yMomentum

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
            elif 1050 <= mouse[0] <= 1175 and 75 <= mouse[1] <= 100 and controls:
                controls = False
        
            #check text boxes on add object menu
            if 975 <= mouse[0] <= 1005 and 490 <= mouse[1] <= 515 and not anyBoxClicked:
                xVelocityBoxClicked = True
                recieveText = True
                userText = ""
            if 975 <= mouse[0] <= 1005 and 520 <= mouse[1] <= 545 and not anyBoxClicked:
                yVelocityBoxClicked = True
                recieveText = True
                userText = ""
            if 975 <= mouse[0] <= 1005 and 550 <= mouse[1] <= 575 and not anyBoxClicked:
                massBoxClicked = True
                recieveText = True
                userText = ""
            if 975 <= mouse[0] <= 1005 and 580 <= mouse[1] <= 605 and not anyBoxClicked:
                radiusBoxClicked = True
                recieveText = True
                userText = ""
            if 965 <= mouse[0] <= 1015 and 650 <= mouse[1] <= 680 and not anyBoxClicked:
                createObject = True
                objectNumber += 1
            
 
        #add object
        if event.type == pygame.KEYDOWN:
            #add object menu
            if event.key == pygame.K_a and not recieveText:
                addObjectMenu = True
            if event.key == pygame.K_RETURN:
                xVelocityBoxClicked = False
                recieveText = False
                yVelocityBoxClicked = False
                massBoxClicked = False
                radiusBoxClicked = False
            
            #gravity change
            if event.key == pygame.K_EQUALS:
                gravity += 0.1
            if event.key == pygame.K_MINUS:
                gravity -= 0.1
            
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
       
    #redraw screen ever loop
    displaySurf.fill(black) 
    pygame.draw.rect(displaySurf, white, physicsBorder, 1)
    titleFont = pygame.font.SysFont("Arial",20)
    titleText = titleFont.render("Pysics: A Python Based Physics Simulator", False, lime, black)
    displaySurf.blit(titleText, (800,25))

    #framerate
    clock.tick(600)

    mouse = pygame.mouse.get_pos()

    #controls menu
    if controls:
        controlButton = titleFont.render("Close Controls", False, black, white)
        displaySurf.blit(controlButton, (1050, 75))
        controlTitleText = titleFont.render("Controls", False, white, black)
        displaySurf.blit(controlTitleText, (950, 100))
        controlLine1 = titleFont.render("Click an object to select the object", False, white, black)
        displaySurf.blit(controlLine1, (790, 150))
        controlLine2 = titleFont.render("A - create a new object", False, white, black)
        displaySurf.blit(controlLine2, (790, 175))
        controlLine3 = titleFont.render("D - delete selected object", False, white, black)
        displaySurf.blit(controlLine3, (790, 200))
        controlLine4 = titleFont.render("right arrow - apply positive velocity on x axis", False, white, black)
        displaySurf.blit(controlLine4, (790, 225))
        controlLine5 = titleFont.render("left arrow - apply negative velocity on x axis", False, white, black)
        displaySurf.blit(controlLine5, (790, 250))
        controlLine6 = titleFont.render("up arrow - apply positive velocity on y axis", False, white, black)
        displaySurf.blit(controlLine6, (790, 275))
        controlLine7 = titleFont.render("down arrow - apply negative velocity on y axis", False, white, black)
        displaySurf.blit(controlLine7, (790, 300))
        controlLine8 = titleFont.render("plus/equals - increase gravity", False, white, black)
        displaySurf.blit(controlLine8, (790, 325))
        controlLine9 = titleFont.render("minus/dash - decrease gravity", False, white, black)
        displaySurf.blit(controlLine9, (790, 350))
        controlLine10 = titleFont.render("comma/< - scroll left on object selection", False, white, black)
        displaySurf.blit(controlLine10, (790, 375))
        controlLine11 = titleFont.render("period/> - scroll right on object selection", False, white, black)
        displaySurf.blit(controlLine11, (790, 400))
    else:
        controlButton = titleFont.render("Controls", False, black, white)
        displaySurf.blit(controlButton, (1100, 75))
    
    #add object menu
    if addObjectMenu:
        #title
        pygame.draw.rect(displaySurf, red, addObjectBorder, 2)
        addObjectTitle = titleFont.render("Add an Object", False, white, black)
        displaySurf.blit(addObjectTitle, (925, 460))

        #x velocity label
        addObjectXVelocityLabel = titleFont.render("Initial X Velocity:", False, white, black)
        displaySurf.blit(addObjectXVelocityLabel, (800, 490))
        if not xVelocityDebounce and not xVelocityBoxClicked:
            pygame.draw.rect(displaySurf, gray, xVelocityTextBox)
        elif xVelocityDebounce and not xVelocityBoxClicked:
            xVelocityText = titleFont.render(xVelocity, False, green, gray)
            displaySurf.blit(xVelocityText, (975, 490))
        if xVelocityBoxClicked:
            xVelocityDebounce = True
            xVelocityText = titleFont.render(userText, False, white, gray)
            displaySurf.blit(xVelocityText, (975, 490))
            xVelocity = userText

        #y velocity label
        addObjectYVelocityLabel = titleFont.render("Initial Y Velocity:", False, white, black)
        displaySurf.blit(addObjectYVelocityLabel, (800, 520))
        if not yVelocityDebounce and not yVelocityBoxClicked:
            pygame.draw.rect(displaySurf, gray, yVelocityTextBox)
        elif yVelocityDebounce and not yVelocityBoxClicked:
            yVelocityText = titleFont.render(yVelocity, False, green, gray)
            displaySurf.blit(yVelocityText, (975, 520))
        if yVelocityBoxClicked:
            yVelocityDebounce = True
            yVelocityText = titleFont.render(userText, False, white, gray)
            displaySurf.blit(yVelocityText, (975, 520))
            yVelocity = userText

        #mass label
        addObjectMassLabel = titleFont.render("Object Mass:", False, white, black)
        displaySurf.blit(addObjectMassLabel, (800, 550))
        if not massDebounce and not massBoxClicked:
            pygame.draw.rect(displaySurf, gray, massTextBox)
        elif massDebounce and not massBoxClicked:
            massText = titleFont.render(mass, False, green, gray)
            displaySurf.blit(massText, (975, 550))
        if massBoxClicked:
            massDebounce = True
            massText = titleFont.render(userText, False, white, gray)
            displaySurf.blit(massText, (975, 550))
            mass = userText

        #radius label
        addObjectRadiusLabel = titleFont.render("Object Radius:", False, white, black)
        displaySurf.blit(addObjectRadiusLabel, (800, 580))
        if not radiusDebounce and not radiusBoxClicked:
            pygame.draw.rect(displaySurf, gray, radiusTextBox)
        elif radiusDebounce and not radiusBoxClicked:
            radiusText = titleFont.render(radius, False, green, gray)
            displaySurf.blit(radiusText, (975, 580))
        if radiusBoxClicked:
            radiusDebounce = True
            radiusText = titleFont.render(userText, False, white, gray)
            displaySurf.blit(radiusText, (975, 580))
            radius = userText

        #create button
        createButtonText = titleFont.render("Create", False, white, red)
        displaySurf.blit(createButtonText, (965, 650))
        if createObject:
            pygame.draw.circle(displaySurf, red, origin, 3)
            currentObjects.append(screenObject(400, 400, float(xVelocity), float(yVelocity), float(mass), float(radius), False, -1, float(mass)*float(xVelocity), float(mass)*float(yVelocity)))
            createObject = False
            addObjectMenu = False
        
    #gravity label
    gravityLabelText = titleFont.render("Gravity:" + str('%.1f'%(gravity)), False, white, blue)
    displaySurf.blit(gravityLabelText, (825, 75))


    #physics calculations
    for object in currentObjects:        

        #calculate momentum for possible later use
        object.xMomentum = object.mass * object.xVelocity
        object.yMomentum = object.mass * object.yVelocity

        #object selection
        currentIndex = -1
        for x in currentObjects:
            currentIndex += 1
            print(indexSelect, selectMoveLeft, selectMoveRight)
            if selectMoveLeft and indexSelect != 0:
                indexSelect -= 1
                selectMoveLeft = False
            else:
                selectMoveLeft = False
            if selectMoveRight and indexSelect != (len(currentObjects) - 1):
                indexSelect += 1
                selectMoveRight = False
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

                    #calculate velocity
                    object.xVelocity = object.xMomentum / object.mass
                    object.yVelocity = object.yMomentum / object.mass
                    x.xVelocity = x.xMomentum / x.mass
                    x.yVelocity = x.yMomentum / x.mass

                    object.colliding = -1
                    currentIndex = -1

        #calculate movement based on velocity
        if object.xVelocity != 0:
            object.xLocation = object.xLocation + (object.xVelocity / 10)
        if object.yVelocity != 0:
            object.yLocation = object.yLocation - (object.yVelocity / 10)
        #make sure objects can't go past border
        if object.xLocation > 775 - object.radius:
            object.xLocation = 775 - object.radius
        if object.yLocation > 775 - object.radius:
            object.yLocation = 775 - object.radius
        if object.xLocation < 25 + object.radius:
            object.xLocation = 25 + object.radius
        if object.yLocation < 25 + object.radius:
            object.yLocation = 25 + object.radius
        
        #wall collisions
        if object.xLocation == (775 - object.radius) or object.xLocation == (25 + object.radius):
            object.xVelocity = -object.xVelocity
        if object.yLocation == (775 - object.radius) or object.yLocation == (25 + object.radius):
            object.yVelocity = -object.yVelocity
        
        #gravity
        object.yVelocity = object.yVelocity - gravity
            
        #vector drawing
        pygame.draw.line(displaySurf, blue, (object.xLocation, object.yLocation), (object.xLocation + object.xVelocity * 2 , object.yLocation - object.yVelocity * 2))
        if not object.selected:
            pygame.draw.circle(displaySurf, red, (object.xLocation, object.yLocation), object.radius)
        elif object.selected:
            pygame.draw.circle(displaySurf, blue, (object.xLocation, object.yLocation), object.radius)
    #update the display
    pygame.display.update()