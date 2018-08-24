import pygame, sys
from engine import *
from individual import *
from time import sleep
import population
import physics
from food import food
# initialize the pygame module
pygame.init()
#Settings
max_steps = 1000
goal = (900, 600) #(x, y)
screen_size = (1000,720) #(x, y)
spawn_point = [30, 30] #Spawn point for circles
# create a surface on screen
screen = pygame.display.set_mode(screen_size)
engine = Render_Engine(screen, goal, screen_size)
physics = physics.physics(goal, engine)
food = food(*screen_size, goal)
food.upfood()
pop = population.population(spawn_point, food, population_size=300, steps=max_steps)
walls = [[500, 300, 10, 600], [600, 0, 10, 400], [800, 500, 10, 200]] #Walls: format [x, y, x_size, y_size], [400, 0, 10, 300]
gen = 0
frame_num = 0
while True:
    # Closes program when red[x] button in corner is pressed
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            pygame.quit()
            sys.exit()
    if pop.everyone_dead():
        #Everyone died reset and advance to next generation
        print("Gen:", gen)
        engine.frame(pop.get_positions(), walls)
        #pop.calc_fitness_scores(goal)
        best = pop.best_person(goal)
        print(best.fitness)
        print(pop.individuals[10].fitness)
        if best.win:
            print("Took the fastest {} steps".format(best.brain.counter))
        pop.selection(goal)
        pop.reset()
        gen += 1
        frame_num = 0
        food.upfood()
    else:
        #Continue moving and updating
        engine.frame(pop.get_positions(), walls)
        pop.move()
        physics.check(pop.individuals, walls)
        #if frame_num%10 == 0:
        #    food.upfood()
        pop.update_fitness()
        frame_num += 1
