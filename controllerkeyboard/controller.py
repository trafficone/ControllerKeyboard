__author__ = 'trafficone'
import math
import autopy

def enum(**enums):
    return type('Enum', (), enums)

Buttons = enum(
    X = 0,
    Y = 1,
    B = 2,
    A = 3,
    START = 4,
    SELECT = 5,
    L1 = 6,
    R1 = 7,
    L3 = 8,
    R3 = 9,
    LEFTAXIS_X = 10,
    LEFTAXIS_Y = 11,
    RIGHTAXIS_X = 12,
    RIGHTAXIS_Y = 13,
    HAT = 14,
    TRIGGERAXIS = 15,
    LEFTANALOG = 16,
    RIGHTANALOG = 17)

Xbox360Buttons = {
    #Xbox360 Configuration
    'BUTTON_KEYS': ['Y','X','B','A','L1','R1','START','SELECT','L3','R3'],
    'BUTTONS' : dict(zip(['Y','X','B','A','L1','R1','START','SELECT','L3','R3'],
                         range(len(['Y','X','B','A','L1','R1','START','SELECT','L3','R3'])))),
    Buttons.LEFTAXIS_X : 0,
    Buttons.LEFTAXIS_Y : 1,
    Buttons.RIGHTAXIS_X : 4,
    Buttons.RIGHTAXIS_Y : 3,
    Buttons.HAT : 0,
    Buttons.TRIGGERAXIS : 2,
    Buttons.Y : 0,
    Buttons.X : 1,
    Buttons.B : 2,
    Buttons.A : 3,
    Buttons.L1: 4,
    Buttons.R1: 5,
    Buttons.START:6,
    Buttons.SELECT:7,
    Buttons.L3:8,
    Buttons.R3:9
    }

class Controller:
    THRESH = .5
    SENSITIVITY = 50
    DEADZONE = .2
    def __init__(self,joystick):

        self.joystick = joystick
        self.joystick.init()
        self.debounce = 0
        self.hdebounce = 0

        self.keyboard = Keyboard()
        self.mouse = Mouse()

        self.myButtons = Xbox360Buttons
        self.myButtons[Buttons.LEFTANALOG] = [self.myButtons[Buttons.LEFTAXIS_X],self.myButtons[Buttons.LEFTAXIS_Y]]
        self.myButtons[Buttons.RIGHTANALOG] = [self.myButtons[Buttons.RIGHTAXIS_X],self.myButtons[Buttons.RIGHTAXIS_Y]]

        self.validate_buttons(self.myButtons)


    def validate_buttons(self,buttonDict):
        for i in range(18):
            try:
                buttonDict[i]
            except:
                raise Exception("Button Specification is invalid - required buttons are missing")

    def reinit(self):
        self.joystick.init()
        self.update_mouse()
        self.process_hat()
        if self.debounce > 0:
            self.debounce -= 1
        if self.hdebounce > 0:
            self.hdebounce -= 1

    def process_button(self):
        for butts in range(4):
            i = self.myButtons['BUTTONS'][self.myButtons['BUTTON_KEYS'][butts]]
            axis = self.get_analog_stick(Buttons.LEFTANALOG)
            if self.joystick.get_button(i) == 1 and (
                        axis[0] ** 2 + axis[1] ** 2) ** .5 >= self.THRESH:
                #ABXY - enter char
                self.keyboard.type_letter(
                    self.keyboard.get_letters(axis[0],
                                                axis[1],
                                                self.get_triggers())[3 - butts])
            else:
                #I keep finding myself doing this
                #self.m1.click()
                pass
        if self.joystick.get_button(self.myButtons[Buttons.L1]) == 1 and self.debounce == 0:
            self.debounce = 3
            self.keyboard.type_letter(autopy.key.K_BACKSPACE)
        if self.joystick.get_button(self.myButtons[Buttons.R1]) == 1 and self.debounce == 0: #RBump - space
            self.debounce = 3
            self.keyboard.type_letter(' ')
        if self.joystick.get_button(self.myButtons[Buttons.START]) == 1: #Start - unmapped
            pass
        if self.joystick.get_button(self.myButtons[Buttons.SELECT]) == 1: #Select - unmapped
            pass
        if self.joystick.get_button(self.myButtons[Buttons.L3]) == 1: #Lstick - enter
            self.keyboard.type_letter(autopy.key.K_RETURN)
        if self.joystick.get_button(self.myButtons[Buttons.R3]) == 1 and self.debounce == 0: #Rstick - click (LTrigger = right-click, RTrigger = Middle-click)
            self.debounce = 10
            triggers = self.get_triggers()
            if triggers > self.DEADZONE:
                self.mouse.click(autopy.mouse.RIGHT_BUTTON)
            elif triggers < -self.DEADZONE:
                self.mouse.click(autopy.mouse.CENTER_BUTTON)
            else:
                self.mouse.click(autopy.mouse.LEFT_BUTTON)

    def process_hat(self):
        if self.joystick.get_hat(0) != (0, 0) and self.hdebounce == 0:
            self.hdebounce = 5
            if self.joystick.get_hat(0)[1] == 1:
                self.keyboard.type_letter(self.key.K_UP)
            if self.joystick.get_hat(0)[1] == -1:
                self.keyboard.type_letter(self.key.K_DOWN)
            if self.joystick.get_hat(0)[0] == -1:
                self.keyboard.type_letter(self.key.K_LEFT)
            if self.joystick.get_hat(0)[0] == 1:
                self.keyboard.type_letter(self.key.K_RIGHT)

    def get_analog_stick(self,stick_choice):
        if stick_choice not in [Buttons.LEFTANALOG,Buttons.RIGHTANALOG]:
            raise Exception("Invalid analog stick")
        else:
            stick = self.myButtons[stick_choice]
            return (self.joystick.get_axis(stick[0]),self.joystick.get_axis(stick[1]))

    def get_triggers(self):
        return self.joystick.get_axis(self.myButtons[Buttons.TRIGGERAXIS])

    def update_mouse(self):
        axis = self.get_analog_stick(Buttons.RIGHTANALOG)
        oldloc = [self.loc[0], self.loc[1]]
        if abs(axis[0]) > self.DEADZONE or abs(axis[1]) > self.DEADZONE:
            self.mouse.move(map(lambda x:x ** 5 * self.SENSITIVITY,axis))

        if oldloc != self.loc:


class Mouse:
    def __init__(self):
        import autopy
        from pymouse import PyMouse

        self.m1 = autopy.mouse
        self.loc = [self.m1.get_pos()[0],self.m1.get_pos()[1]]
        self.m = PyMouse()
        self.m.move(self.loc[0], self.loc[1])

    def move(self,direction):
        #Move mouse
        self.loc[0] += direction[0]
        self.loc[1] += direction[1] ** 5 * self.SENSITIVITY
        #FIXME: Support multiple displays
        #Check horizontal bounds
        self.loc[0] = min(self.loc[0],3600)#self.m.screen_size()[0])
        self.loc[0] = max(self.loc[0],0)
        #Check vertical bounds
        self.loc[1] = min(self.loc[1],self.m.screen_size()[1])
        self.loc[1] = max(self.loc[1],0)
        self.m.move(int(self.loc[0]), int(self.loc[1]))

    def click(self,button):
        self.m1.click(button)


class Keyboard:
    def __init__(self):
        self.key = autopy.key

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

    def type_letter(self,keyval,shift=False):
        mods = 0
        if type(keyval) == str:
            if keyval in '~!@#$%^&*(){}"<>PYFGCRL?+|AOEUIDHTNS_:QJKXBMWVZ' and len(keyval) == 1:
                mods |= self.key.MOD_SHIFT
            if keyval[0] == '^' and len(keyval) == 2:
                mods |= self.key.MOD_CONTROL
                keyval = keyval[1]
        self.key.tap(keyval, mods)