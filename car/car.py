from ult import *
from car_data import *
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
from Box2D import * # The main library
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, staticBody, dynamicBody)
from copy import deepcopy
'''
Stores physical objects linked to car
'''
class car:
    def __init__(self, world):
        self.spawn = point(0, 4)
        self.world = world
        self.data = car_data()
        self.fitness = 0
        self.mutate_rate = 0.1
        self.make_car()
    def calc_fitness(self):
        self.fitness = (self.body.position.x - self.spawn.x)**2 #Squared distance travelled
        return self.fitness
    def __str__(self):
        return "Fitness: " + str(self.fitness) + "\n" + str(self.data)
    def __del__(self):
        self.world.DestroyBody(self.body)
        for c in self.wheels:
            self.world.DestroyBody(c)
    def randomize(self, change=None):
        self.data.randomize(change=change)
    def mutate(self):
        child = car(self.world)
        child.data = deepcopy(self.data)
        what = [random.random() < self.mutate_rate for i in range(child.data.number_of_genes)]
        child.randomize(change=what)
        return child
    def update_to_new_data(self):
        self.world.DestroyBody(self.body)
        for c in self.wheels:
            self.world.DestroyBody(c)
        self.make_car()
    def make_car(self):
        c = self.data
        # Create a car with 2 wheels
        self.body = self.world.CreateDynamicBody(
            position=self.spawn(),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=c.body.box),
                friction=c.body.friction,
                density=c.body.density,
                filter=b2Filter(
                    groupIndex=-1,
                    categoryBits=0x0002,
                    maskBits=0xFFFF^0x0002
                )
            )
        )
        self.wheels = []
        self.springs = []
        for w in c.wheels:
            wheel = self.world.CreateDynamicBody(
                position=(self.spawn+w.pos)(),
                fixtures=b2FixtureDef(
                    shape=b2CircleShape(radius=w.radius),
                    friction=w.friction,
                    density=w.density,
                    filter=b2Filter(
                        groupIndex=-1,
                        categoryBits=0x0002,
                        maskBits=0xFFFF
                    )
                )
            )
            self.wheels.append(wheel)
            spring = self.world.CreateWheelJoint(
                        bodyA=self.body,
                        bodyB=wheel,
                        anchor=wheel.position,
                        axis=(0.0, 1.0),
                        motorSpeed=w.motorSpeed,
                        maxMotorTorque=50,
                        enableMotor=True,
                        frequencyHz=w.frequencyHz,
                        dampingRatio=w.dampingRatio
                    )
            self.springs.append(spring)
        return [self.body, self.wheels, self.springs]
