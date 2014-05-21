
__author__ = 'trafficone'
from controllerkeyboard.interface import TextPrint
from controllerkeyboard.controller import Controller
from controllerkeyboard.controller import Buttons
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#initialize pygame
pygame.init()
size = [400, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Controller General Interface")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

testphrase = ""

# Initialize the joysticks
controller = None
try:
    pygame.joystick.init()
    controller = Controller(pygame.joystick.Joystick(0))
except Exception, e:
    testphrase = e.message + '\n'
    testphrase += "Controller not attached. Please attach joystick & Restart."
    print 'Controller not found, or could not be initialized'

textPrint = TextPrint()

# -------- Main Program Loop -----------
while done == False:
    if controller != None:
      controller.reinit()
    # EVENT PROCESSING STEP

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.JOYBUTTONDOWN:
            controller.process_button()

    #DRAWING STEP
    screen.fill(WHITE)
    textPrint.reset()
    textPrint.pront(screen, testphrase)
    if controller != None:
        axis = controller.get_analog_stick(Buttons.LEFTANALOG)
        if (axis[0] ** 2 + axis[1] ** 2)**.5 >= controller.THRESH:
            textPrint.draw_chars(screen,
                             (200+axis[0] * 100,
                              200 + axis[1] * 100),
                              controller.typewriter.get_letters(axis[0], axis[1],
                                                    controller.get_triggers()))
        axis = controller.get_analog_stick(Buttons.RIGHTANALOG)
        pygame.draw.line(screen, pygame.Color(255, 0, 0), (200, 200),
                         (200+axis[0] * 50, 200 + axis[1] * 50))
        pygame.draw.circle(screen, pygame.Color(0,0,0),(200,200),int(controller.DEADZONE*50),0)
        pygame.draw.circle(screen, pygame.Color(0,0,0),(200,200),int(controller.THRESH*100),1)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
pygame.quit ()