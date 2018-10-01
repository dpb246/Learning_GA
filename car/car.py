from ult import *
from car_data import *
import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
from Box2D import * # The main library
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, staticBody, dynamicBody)
'''
Stores physical objects linked to car
'''
class car:
    def __init__(self, world):
        self.spawn = point(0, 4)
        self.world = world
    def make_car(self, c):
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
