from car import car
from car_data import car_data
from ult import *
import random
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
            c.update_to_new_data()
    #Updates physical models of the cars to the new data
    def update_cars(self):
        for c in self.cars:
            c.update_to_new_data()
    def activate_motors(self):
        for c in self.cars:
            for s in c.springs:
                s.enableMotor = True
    #Finds and returns the distance and index of the car that has travelled the farthest in the positive x direction
    def find_farthest(self):
        max_dis = 0
        index = 0
        for i in range(len(self.cars)):
            if self.cars[i].body.position.x > max_dis:
                max_dis = self.cars[i].body.position.x
                index = i
        return max_dis, index
    def calculate_fitness(self):
        self.max_fitness = 0
        self.sum_of_fitness = 0
        for c in self.cars:
            fitness = c.calc_fitness()
            self.sum_of_fitness += fitness
            if fitness > self.max_fitness:
                self.max_fitness = fitness
        return self.max_fitness
    def pick_parent(self):
        number = random.random() * self.sum_of_fitness
        for c in self.cars:
            number -= c.fitness
            if number <= 0: break
        return c
    def next_gen(self):
        next_gen = [self.pick_parent().mutate() for i in range(self.size)]
        next_gen[0] = self.cars[self.find_farthest()[1]]
        del self.cars
        self.cars = next_gen
        for c in self.cars:
            c.update_to_new_data()
