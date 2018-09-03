'''
Holds various methods and classes used in multiple files
'''
#Clamp value between a min and max
def clamp(min, value, max):
    return sorted([min, value, max])[1]

#Checks if a point is within a box
#Uses 0,0 as center of the box
#Box is a tuple of half widths: (length, hieght)
def within(pos, box):
    if abs(pos.x) > box[0]:
        return False #just abs to check since pos is relative to the middle of the box
    if abs(pos.y) > box[1]:
        return False
    return True

#X, Y point
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        x = self.x+other.x
        y = self.y+other.y
        return point(x, y)
    def __sub__(self, other):
        x = self.x-other.x
        y = self.y-other.y
        return point(x, y)
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y
    def __ne__(self, other):
        return self.x!=other.x or self.y!=other.y
    def __call__(self):
        return (self.x,self.y)
    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)
    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)
    def __gt__(self, other):
        return self.x > other and self.y > other
    def __lt__(self, other):
        return self.x < other and self.y < other
    def __abs__(self):
        return point(abs(self.x), abs(self.y))
