from car import car
from car_data import car_data
from ult import *
'''
Working car setups

car1.wheels[0].pos = point(1.25, -1)
car1.wheels[1].pos = point(-1.25, -1)
car1.wheels[0].radius = 1
car1.wheels[1].radius = 1


car2.wheels[0].pos = point(1.5, -1)
car2.wheels[1].pos = point(-1.5, -1)
car2.wheels[0].radius = 1.5
car2.wheels[1].radius = 1.5
'''
class pop:
    def __init__(self, physworld=None, size=10, spawn=point(0,4)):
        self.spawn = spawn
        self.size = size
        self.world = physworld
        self.cars = [car(physworld) for i in range(size)]
        for c in self.cars:
            c.randomize()
    #Updates physical models of the cars to the new data
    def make_cars(self):
        for c in self.cars:
            c.make_car(c.data)
    #Finds and returns the distance and index of the car that has travelled the farthest in the positive x direction
    def find_farthest(self):
        max_dis = 0
        index = 0
        for i in range(len(self.cars)):
            if self.cars[i].body.position.x > max_dis:
                max_dis = self.cars[i].body.position.x
                index = i
        return max_dis, index
