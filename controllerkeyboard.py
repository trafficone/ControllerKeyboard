from pymouse import PyMouse
import autopy
import pygame
import math


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
THRESH = .5
SENSITIVITY = 50
DEADZONE = .2


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def pront(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

    def draw_chars(self, screen, location, chars):
        """ Draw chars at location in the format: A
                                                 B C
                                                  D
        """
        textChar0 = self.font.render(chars[0], True, BLACK)
        textChar1 = self.font.render('%c   %c' % (chars[1], chars[2]), True, BLACK)
        textChar2 = self.font.render(chars[3], True, BLACK)
        screen.blit(textChar0, [location[0], location[1] - self.line_height])
        screen.blit(textChar1, [location[0] - 10, location[1]])
        screen.blit(textChar2, [location[0], location[1] + self.line_height])


class TypeWriter:
    def __init__(self):
        #self.reset()
        self.lchars = map(chr, range(ord('a'), ord('z') + 1))
        self.lchars.extend([',', '.', '!', '?', '-', "'"])
        self.uchars = map(chr, range(ord('A'), ord('Z') + 1))
        self.uchars.extend([',', '.', '!', '?', '-', "'"])
        self.schars = list('@#$%' +
                           '^&*=' +
                           '()<>' +
                           '"+_/' +
                           '\\123' +
                           '4567' +
                           '890')
        self.schars.extend([';', ':', '~', '`', '-'])

    def get_angle(self, xAxis, yAxis):
        if yAxis == 0:
            angle = math.pi / 2
        else:
            angle = math.atan(xAxis / -yAxis) #angle in radians, 0 at top, clockwise
        if -yAxis < 0:
            angle += math.pi
        elif xAxis < 0:
            angle += 2 * math.pi
        segment_size = 2 * math.pi / 8
        offset = segment_size / 2
        angle += offset
        if angle > 2 * math.pi:
            angle -= 2 * math.pi
        return angle

    def get_letters(self, xAxis, yAxis, zAxis):
        angle = self.get_angle(xAxis, yAxis)
        segment_size = 2 * math.pi / 8
        segment = int(angle / segment_size)
        if abs(zAxis) < .1:
            return self.lchars[4 * segment:4 * segment + 4]
        elif zAxis > 0:
            return self.uchars[4 * segment:4 * segment + 4]
        else:
            return self.schars[4 * segment:4 * segment + 4]

#initialize pygame
pygame.init()
size = [400, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Controller General Interface")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Initialize the mouse
m1 = autopy.mouse
loc = [m1.get_pos()[0],m1.get_pos()[1]]
m = PyMouse()
m.move(loc[0], loc[1])

#Initialize the keyboard
key = autopy.key


testphrase = ""



# Initialize the joysticks
joystick = None
try:
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
except Exception, e:
    testphrase = "Joystick not attached. Please attach joystick & Restart."
    print 'joystick not found'

textPrint = TextPrint()
typewriter = TypeWriter()

debounce = 0
hdebounce = 0

# -------- Main Program Loop -----------
while done == False:
    if joystick != None:
      joystick.init()
    # EVENT PROCESSING STEP
    if debounce > 0:
        debounce -= 1
    if hdebounce > 0:
        hdebounce -= 1
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.JOYBUTTONDOWN:
            # button 9 = right stick
            # button 8 = left stick
            # button 7 = select
            # button 6 = start
            # button 5 = Right bumper
            # button 4 = Left bumper
            # button 3 = A
            # button 2 = B
            # button 1 = X
            # button 0 = Y
            # Hat = D-pad
            for i in range(4):
                if joystick.get_button(i) == 1 and (
                            joystick.get_axis(0) ** 2 + joystick.get_axis(1) ** 2) ** .5 >= THRESH:
                #ABXY - enter char
                    outchar = typewriter.get_letters(joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2))[
                        3 - i]
                    key.tap(outchar)
            if joystick.get_button(4) == 1 and debounce == 0: #LBump - backspace
                debounce = 3
                key.tap(key.K_BACKSPACE)
            if joystick.get_button(5) == 1 and debounce == 0: #RBump - space
                debounce = 3
                key.tap(' ')
            if joystick.get_button(6) == 1: #Start - unmapped
                pass
            if joystick.get_button(7) == 1: #Select - unmapped
                pass
            if joystick.get_button(8) == 1: #Lstick - enter
                key.tap(key.K_RETURN)
            if joystick.get_button(9) == 1 and debounce == 0: #Rstick - click (LTrigger = right-click, RTrigger = Middle-click)
                debounce = 10
                #button = 1
                button = m1.LEFT_BUTTON
                if joystick.get_axis(2) > DEADZONE:
                    #button = 2
                    button = m1.RIGHT_BUTTON
                if joystick.get_axis(2) < -DEADZONE:
                    #button = 3
                    button = m1.CENTER_BUTTON
                m1.click(button)
    if joystick != None and joystick.get_hat(0) != (0, 0) and hdebounce == 0:
        hdebounce = 5
        if joystick.get_hat(0)[1] == 1:
            key.tap(key.K_UP)
        if joystick.get_hat(0)[1] == -1:
            key.tap(key.K_DOWN)
        if joystick.get_hat(0)[0] == -1:
            key.tap(key.K_LEFT)
        if joystick.get_hat(0)[0] == 1:
            key.tap(key.K_RIGHT)
    #DRAWING STEP
    screen.fill(WHITE)
    textPrint.reset()
    textPrint.pront(screen, testphrase)
    if joystick != None:
        if (joystick.get_axis(0) ** 2 + joystick.get_axis(1) ** 2)**.5 >= THRESH:
            textPrint.draw_chars(screen,
                                 (200+joystick.get_axis(0) * 100,
                                  200 + joystick.get_axis(1) * 100),
                                  typewriter.get_letters(joystick.get_axis(0), joystick.get_axis(1),
                                                        joystick.get_axis(2)))
        pygame.draw.line(screen, pygame.Color(255, 0, 0), (200, 200),
                         (200+joystick.get_axis(4) * 50, 200 + joystick.get_axis(3) * 50))
        pygame.draw.circle(screen, pygame.Color(0,0,0),(200,200),int(DEADZONE*50),0)
        pygame.draw.circle(screen, pygame.Color(0,0,0),(200,200),int(THRESH*100),1)
        oldloc = [loc[0], loc[1]]
        if abs(joystick.get_axis(4)) > DEADZONE: # implementing DEAD ZONE
            loc[0] += joystick.get_axis(4) ** 5 * SENSITIVITY
        if abs(joystick.get_axis(3)) > DEADZONE: # implementing DEAD ZONE
            loc[1] += joystick.get_axis(3) ** 5 * SENSITIVITY
        if oldloc != loc:
            m.move(int(loc[0]), int(loc[1]))

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
pygame.quit ()