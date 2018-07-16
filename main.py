import pygame, sys
from engine import *
from individual import *
from time import sleep
import population
import physics
# initialize the pygame module
pygame.init()
#Settings
max_steps = 300
goal = (600, 600)
screen_size = (720,720)
# create a surface on screen
screen = pygame.display.set_mode(screen_size)
engine = Render_Engine(screen, goal, screen_size)
physics = physics.physics(goal, engine)
pop = population.population([30, 30], population_size=1000, steps=max_steps)
walls = [[500, 300, 10, 300]]


for step in range(max_steps):
    # event handling, gets all event from the eventqueue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            pygame.quit()
            sys.exit()

    engine.frame(pop.get_positions(), walls)
    print("+++++++++STEP+++++++++++++++", step)
    pop.move(step)
    physics.check(pop.individuals, walls)

print(pop.best_person(goal))
