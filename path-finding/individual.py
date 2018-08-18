from math import sqrt
import random
from copy import deepcopy
from brain import *
'''
A circle with a position and velocity, each has a brain that contains the accel vectors
'''
class person(object):
    def __init__(self, starting_pos, steps=100, max_speed=10):
        self.pos = deepcopy(starting_pos)
        self.starting_pos = starting_pos
        self.velocity = [0,0]
        self.brain = brain(steps)
        self.is_dead = False #Stores if it should be updated
        self.max_speed = max_speed
        self.win = False
        self.fitness = 0
        self.steps = steps
    def get_fitness(self, goal): #Returns distance to goal
        if self.win:
            self.fitness = (self.brain.number_of_steps - self.brain.counter)**2
        else:
            self.fitness = 1/((self.pos[0]-goal[0])**2 + (self.pos[1]-goal[1])**2)
        return self.fitness
    def kill(self):
        self.is_dead = True
        #print("killed")
    def win_game(self):
        self.win = True
        #print("win game")
    def reset(self):
        self.brain.reset()
        self.is_dead = False
        self.win = False
    def active(self):
        return self.is_dead or self.win
    def get_pos(self):
        return [int(i) for i in self.pos]
    def child(self):
        child = person(self.starting_pos, self.steps, self.max_speed)
        child.brain = deepcopy(self.brain)
        return child
    def move(self):
        if self.is_dead or self.win: return False #Skip if dead
        step = self.brain.get_next()
        if step == None:
            self.is_dead = True
            return False
        for i in range(2):
            #Add accel
            self.velocity[i] += step[i]
            #Cap velocity
            if self.velocity[i] > self.max_speed:
                self.velocity[i] = self.max_speed
                #print("MAX SPEED", id)
            if self.velocity[i] < -self.max_speed:
                self.velocity[i] = -self.max_speed
                #print("MAX SPEED", id)
            #Change pos
            self.pos[i] += self.velocity[i]
