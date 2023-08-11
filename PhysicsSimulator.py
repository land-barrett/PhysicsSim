import pygame
from pygame.locals import *
pygame.init()

#basic variables
clock = pygame.time.Clock()
red = (255,0,0)
blue = (0,255,0)
green = (0,0,255)

#pre loop stuff
displaySurf = pygame.display.set_mode((800,800))
pygame.display.set_caption("Pysics")

#stored object physics values
circleValues = {
    "xLocation": 400,
    "yLocation": 400,
    "xVelocity": 8,
    "yVelocity": 8
}

#-------------main loop-------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #framerate
    clock.tick(60)

    #screen drawer
    pygame.draw.circle(displaySurf, red, (circleValues["xLocation"],circleValues["yLocation"]), 4)
    pygame.display.update()
    displaySurf.fill((0,0,0))

    #----------physics calculations----------

    #movement from velocity values
    if circleValues["xVelocity"] != 0:
        circleValues["xLocation"] = circleValues["xLocation"] + (circleValues["xVelocity"])
        if circleValues["xLocation"] > 800:
            circleValues["xLocation"] = 800
        if circleValues["xLocation"] < 0:
            circleValues["xLocation"] = 0

    if circleValues["yVelocity"] != 0:
        circleValues["yLocation"] = circleValues["yLocation"] - (circleValues["yVelocity"])
        if circleValues["yLocation"] > 800:
            circleValues["yLocation"] = 800
        if circleValues["yLocation"] < 0:
            circleValues["yLocation"] = 0

    #wall collisions
    if circleValues["xLocation"] == 800 or circleValues["xLocation"] == 0:
        circleValues["xVelocity"] = -circleValues["xVelocity"]

    if circleValues["yLocation"] == 800 or circleValues["yLocation"] == 0:
        circleValues["yVelocity"] = -circleValues["yVelocity"]
    

    #-----------vector drawing-------------
    
    #velocity vector
    vectorStart = (circleValues["xLocation"], circleValues["yLocation"])
    vectorEnd = (circleValues["xLocation"] + (circleValues["xVelocity"] * 5), circleValues["yLocation"] - (circleValues["yVelocity"] * 5))

    if circleValues["xVelocity"] or circleValues["yVelocity"] != 0:
        pygame.draw.line(displaySurf, blue, vectorStart, vectorEnd)