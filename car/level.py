from Box2D import * # The main library
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, staticBody, dynamicBody)
import random
'''
Holds ground and related functions
'''
class level:
    def __init__(self, world=None):
        self.world = world
        # The ground -- create some terrain
        self.ground = world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, 0), (10, 0)])
        )
        self.blocker = world.CreateStaticBody( #Prevents cars from driving too far to the left
            position=(-18, 10),
            shapes=b2PolygonShape(box=(2,10))
        )
        self.x, self.y1, self.dx = 10, 0, 4
        self.vertices = [0.25, 1, 4, 0, 0, -1, -2, -2, -1.25, 0]
        self.add_ground()
    def reset(self):
        print("reseting world")
        self.world.DestroyBody(self.ground)
        self.world.DestroyBody(self.blocker)
        self.__init__(world = self.world)
    def add_ground_if_needed(self, farthest_dist):
        if self.x < farthest_dist+30:
            self.add_ground()
    def add_ground(self):
        for y2 in [i+random.random()+random.random() for i in self.vertices*2]:  # iterate through vertices multiple times
            self.ground.CreateEdgeFixture(
                vertices=[(self.x, self.y1), (self.x + self.dx, y2)],
                density=0,
                friction=0.1,
            )
            self.y1 = y2
            self.x += self.dx
