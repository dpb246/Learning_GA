from math import sqrt
import random
from copy import deepcopy
class person(object):
    def __init__(self, starting_pos, steps=100, max_speed=10):
        self.pos = deepcopy(starting_pos)
        self.velocity = [0,0]
        self.steps = [[random.random()*random.randrange(-1, 2, 2)/4 for i in range(2)] for i in range(steps)] #Random steps
        self.is_dead = False #Stores if it should be updated
        self.max_speed = max_speed
        self.win = False
    def get_fitness(self, goal): #Returns distance to goal
        return int(sqrt((self.pos[0]-goal[0])**2 + (self.pos[1]-goal[1])**2))
    def kill(self):
        self.is_dead = True
    def win_game(self):
        self.win = True
        print("win game")
    def active(self):
        return self.is_dead or self.win
    def get_pos(self):
        return [int(i) for i in self.pos]
    def move(self, step):
        if self.is_dead or self.win: return False #Skip if dead
        for i in range(2):
            #Add accel
            self.velocity[i] += self.steps[step][i]
            #Cap velocity
            if self.velocity[i] > self.max_speed:
                self.velocity[i] = self.max_speed
                print("MAX SPEED", id)
            if self.velocity[i] < -self.max_speed:
                self.velocity[i] = -self.max_speed
                print("MAX SPEED", id)
            #Change pos
            self.pos[i] += self.velocity[i]
