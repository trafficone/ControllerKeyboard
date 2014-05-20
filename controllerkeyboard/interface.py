__author__ = 'trafficone'
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def pront(self, screen, textString):
        nextString = ''
        if '\n' in textString:
            nextString = textString[textString.index('\n')+1:]
            textString = textString[:textString.index('\n')]
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        if nextString != '':
            self.pront(screen,nextString)

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
