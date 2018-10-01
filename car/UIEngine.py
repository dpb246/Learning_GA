import pygame

#COLOURS
BLACK     = (0, 0, 0, 0)
WHITE     = (255, 255, 255, 0)
RED       = (255, 0, 0, 0)
BLUE      = (0, 0, 255, 0)
GREEN     = (0, 255, 0, 0)
DARKGRAY  = ( 64,  64,  64, 0)
GRAY      = (128, 128, 128, 0)
LIGHTGRAY = (212, 208, 200, 0)

#Simple displayable text object
class textObj:
    def __init__(self, location, font, text, textcolour = WHITE, bgcolour = BLACK):
        self._font = font
        self._check_coll = False
        self._text = " " + str(text) + " " #Yes, it is hard coded to pad it using spaces :)
        self._location = location
        self._textcolour = textcolour
        self._bgcolour = bgcolour
        if font != None and text != None:
            self._surface = self._font.render(self._text, True, self._textcolour, self._bgcolour)
            self._surface = self._surface.convert_alpha()
        else:
            self._surface = None #failed to init right
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        self._text = str(self._text)
        if self._text[0] != " ":
            self._text = " " + str(self._text) + " "#Assume padding
        self._surface = self._font.render(self._text, True, self._textcolour, self._bgcolour)
        self._surface = self._surface.convert_alpha()
        self._boundingbox = pygame.Rect(self._location, self._font.size(self._text))
    def remove(self):
        self._surface = None #Set to be deleted next draw cycle

#Expands on text object to add click functionality
class buttonObj(textObj):
    def __init__(self, location, font=None, text=None, size=None, onClick=None, textcolour = WHITE, bgcolour = BLACK):
        super().__init__(location, font, text, textcolour, bgcolour)
        self._onClick = onClick
        self._size = size
        self._check_coll = True
        if self._size != None and self._surface != None:
            self._boundingbox = pygame.Rect(self._location, self._size)
            self._surface = pygame.transform.smoothscale(self._surface, self._size) #Stretch surface to fit size of button
        else: #if there is no hardcoded size for the clickable area, use the entire size of the text/surface
            self._boundingbox = pygame.Rect(self._location, self._font.size(self._text))
    def update(self, **kwargs):
        super().update(**kwargs)
        if self._size != None and self._surface != None:
            self._boundingbox = pygame.Rect(self._location, self._size)
            self._surface = pygame.transform.smoothscale(self._surface, self._size)
    def click(self): #Just calls onClick method that user gave it
        if self._onClick != None:
            self._onClick()

#Holds a collection of buttonObj and textObj that can be drawn/checked for clicks together
class UIScreen:
    def __init__(self):
        self._obj = []
    def draw(self, screen):
        for i, obj in enumerate(self._obj):
            if obj._surface != None:
                screen.blit(obj._surface, obj._location)
            else:
                del self._obj[i] #If there is no surface delete it to save on preformance
    def clicks(self, mouse_pos): #call during MOUSEDOWN event
        for i, obj in enumerate(self._obj):
            if obj._check_coll:
                if obj._boundingbox.collidepoint(mouse_pos):
                    obj.click()
    def add_text(self, location, font, text, textcolour = WHITE, bgcolour = BLACK):
        self._obj.append(textObj(location, font, text, textcolour, bgcolour))
        return self._obj[-1]
    def add_button(self, location, font = None, text = None, size = None, onClick=None, textcolour = WHITE, bgcolour = LIGHTGRAY):
        self._obj.append(buttonObj(location, font, text, size, onClick, textcolour, bgcolour))
        return self._obj[-1]
