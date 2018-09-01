'''
Class to hold all the data for each car
'''
import random

#Clamp value between min and max
def clamp(min, value, max):
    return sorted([min, value, max])[1]

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __call__(self):
        return (x,y)
    def __str__(self):
        return "x: " + str(x) + " y: " + str(y)

class wheel:
    def __init__(self, radius=0, x=0, y=0, motorSpeed=-30, frequencyHz=10, dampingRatio=0.7, friction=1, density=1):
        self.radius = radius
        self.pos = point(x, y)
        self.friction = friction
        self.density = density
        self.motorSpeed = motorSpeed
        self.frequencyHz = frequencyHz
        self.dampingRatio = dampingRatio
    #TODO Need to set a relative pos that is within the body
    def randomize(self):
        self.radius = clamp(0.1, random.random()*3, 3) #wheels between 0.1m and 3m
        self.friction = random.random() #friction is between 0 to 1
        self.density = random.random() #density is a value between 0 to 1
        self.motorSpeed = random.random()*40 #Set from 0 to 40
        self.frequencyHz = random.random()*50 #Set from 0 to 50
        self.dampingRatio = random.random()
        pass

class body:
    def __init__(self, x=0, y=0, friction=0.2, density=1, box=(2.5, 1)):
        self.pos = point(x, y)
        self.friction = friction
        self.density = density
        self.box = box
    def randomize(self):
        pass
'''
Use relative positions
'''
class car:
    def __init__(self):
        self.wheel_count = 2
        self.wheels = [wheel() for i in range(self.wheel_count)]
        self.body = body()
    def randomize(self):
        self.body.randomize()
        for wheel in self.wheels:
            wheel.randomize()
