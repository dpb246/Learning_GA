'''
Class to hold all the data for each car
'''
import random
from ult import *

class wheel:
    def __init__(self, radius=0, x=0, y=0, motorSpeed=-30, frequencyHz=100, dampingRatio=0.7, friction=1, density=1):
        self.radius = radius
        self.pos = point(x, y)
        self.friction = friction
        self.density = density
        self.motorSpeed = motorSpeed
        self.frequencyHz = frequencyHz
        self.dampingRatio = dampingRatio
        self.number_of_genes = len(self.__dict__)
    #IDEA Wheel size limited such that the wheels don't hit?
    def randomize(self, box, what=None):
        if len(what) != self.number_of_genes: raise NotEnoughValues
        if what[0]: self.radius = clamp(0.1, random.random()*2, 2) #wheels between 0.1m and 3m
        if what[1]: self.friction = random.random() #friction is between 0 to 1
        if what[2]: self.density = random.random() #density is a value between 0 to 1
        if what[3]: self.motorSpeed = random.random()*40*-1 #Set from 0 to 40, flip so car travels in positive direction
        if what[4]: self.frequencyHz = random.random()*50 #Set from 0 to 50
        if what[5]: self.dampingRatio = clamp(0.5,random.random(), 1) #Set from 0 to 1
        if what[6]:
            x = random.random()*box[0]*2-box[0] #Double the size to full length, then subtract half the length to center it on 0
            y = random.random()*box[1]*2-box[1] #Double the size to full length, then subtract half the length to center it on 0
            self.pos = point(x, y)
    def __str__(self):
        output = "Position: " + str(self.pos) + "\n"
        output += "Radius: " + str(self.radius) + "\n"
        output += "Friction: " + str(self.friction) + "\n"
        output += "density: " + str(self.density) + "\n"
        output += "Speed: " + str(self.motorSpeed) + "\n"
        output += "frequencyHz: " + str(self.frequencyHz) + "\n"
        output += "dampingRatio: " + str(self.dampingRatio) + "\n"
        return output

class body:
    #Don't need to set a position of the body, since that is detrimined at spawn and everything else is relative to this
    def __init__(self, friction=0.2, density=1, box=(2.5, 1)):
        self.friction = friction
        self.density = density
        self.box = box
        self.number_of_genes = len(self.__dict__)
    def randomize(self, what=None):
        if what[0]: self.friction = random.random() #friction is between 0 to 1
        if what[1]: self.density = random.random() #density is a value between 0 to 1
        if what[2]:
            width = clamp(0.25, random.random()*4, 4)
            hieght = clamp(0.25, random.random()*3, 3)
            self.box = (width, hieght)
    def __str__(self):
        output = "Box: " + str(self.box) + "\n"
        output += "friction: " + str(self.friction) + "\n"
        output += "density: " + str(self.density) + "\n"
        return output
'''
Use relative positions
'''
class car_data:
    def __init__(self):
        self.wheel_count = 3
        self.wheels = [wheel() for i in range(self.wheel_count)]
        self.body = body()
        self.number_of_genes = self.body.number_of_genes + self.wheel_count*self.wheels[0].number_of_genes
    def randomize(self, change=None):
        if change==None: change = [True for i in range(self.number_of_genes)]
        self.body.randomize(what=change[0:self.body.number_of_genes])
        spot = self.body.number_of_genes
        for wheel in self.wheels:
            wheel.randomize(self.body.box, what=change[spot:(spot+wheel.number_of_genes)])
            spot += wheel.number_of_genes
    def __str__(self):
        output = ""
        for w in self.wheels:
            output += "Wheel:\n" + str(w) + "\n"
        output += "Body:\n"
        output += str(self.body)
        return output
