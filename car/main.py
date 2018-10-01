'''
KNOWN ISSUES:
random generation
Camera will teleport around, # IDEA: Add smooth transition to new car, somewhat fixed with

TODO:
Add more random terrain rather than scripted
Add all genetic functionality
Move main loop into genetic loop
'''
from ult import *
from car_data import *
import pygame
import time
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)
import random
from Box2D import * # The main library
from Box2D.b2 import (world, polygonShape, circleShape, edgeShape, staticBody, dynamicBody)
import UIEngine
import car
from population import pop
from level import level
import graphics
from graphics import s #Holds a bunch of global screen variables

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
TARGET_FPS = 240
MAX_TIME = 10.0
TIME_STEP = 1.0 / 60
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
s.XOFFSET = 0
s.YOFFSET = SCREEN_HEIGHT

# --- pygame setup ---
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('TESTS')
clock = pygame.time.Clock()

#UI
UI = UIEngine.UIScreen()
font = pygame.font.SysFont('Arial', 30)
UI.add_text((10, 10), font, "DEMO")
count_down = UI.add_text((580, 10), font, MAX_TIME)

# Create the world
world = world(gravity=(0, -10), doSleep=True)

#Ground/World cars drive on
stage = level(world=world)

#all the cars
population = pop(physworld=world)
population.make_cars()
cars = population.cars

#Config drawing
s.screen = screen
polygonShape.draw = graphics._draw_polygon
circleShape.draw = graphics._draw_circle
edgeShape.draw = graphics._draw_edge

# --- main loop ---
running = True
start_time = current_time()
last_pos = point(0, 0)
while current_time()-start_time < MAX_TIME*1000 and running:
    # Check the event queue
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # The user closed the window or pressed escape
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            UI.clicks(pygame.mouse.get_pos()) #Check if any of the buttons were pressed
    screen.fill((0, 0, 0, 0))

    count_down.update(_text="{0:0.1f}".format((MAX_TIME*1000-(current_time()-start_time))/1000))

    UI.draw(screen)
    # Draw the world
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)
    # Make Box2D simulate the physics of our world for one step.
    world.Step(TIME_STEP, 10, 10)

    #Find the car that has travelled the farthest in the x+ direction
    farthest_dist, index = population.find_farthest()
    #Have screen follow the car
    s.XOFFSET = (-farthest_dist) * s.PPM + SCREEN_WIDTH // 2
    s.YOFFSET = (cars[index].body.position[1]) * s.PPM + SCREEN_HEIGHT // 2

    #Check if car is about to run out of ground to drive on
    stage.add_ground_if_needed(farthest_dist)
    # Flip the screen and try to keep at the target FPS
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')
