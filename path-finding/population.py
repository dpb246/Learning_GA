from individual import *
import time
import random
from copy import deepcopy
from food import food
'''
Population of individuals, contains all the evolutionary logic
'''
class population:
    def __init__(self, spawn_point, food, population_size=10, steps=100):
        self.individuals = [person(spawn_point, steps) for i in range(population_size)]
        self.positions = []
        self.fitness_scores = []
        self.fittest = 0
        self.min_steps = 10000
        self.spawn_point = spawn_point
        self.population_size = population_size
        self.steps = steps
        self.food = food
    def move(self):
        self.positions = []
        for i in range(len(self.individuals)):
            self.individuals[i].move()
            self.positions.append(self.individuals[i].get_pos())
    def get_positions(self):
        return self.positions
    def calc_fitness_scores(self, goal):
        print("called bad")
        self.fitness_scores = [p.get_fitness(goal) for p in self.individuals]
        self.best_person(goal)
        return self.fitness_scores
    def update_fitness(self):
        self.fitness_scores = [i.eat(self.food.get_food(i.pos)) for i in self.individuals]
        return self.fitness_scores
    def everyone_dead(self):
        for person in self.individuals:
            if not person.is_dead and not person.win:
                return False
        return True
    def best_person(self, goal):
        best_index= 0
        best_score = 0 #bigger score means closer and better
        for index, score in enumerate(self.fitness_scores):
            if score > best_score:
                best_score = score
                best_index = index
        self.fittest = best_score
        if self.individuals[best_index].win:
            self.min_steps = self.individuals[best_index].brain.counter
            #print("steps: {}".format(self.min_steps))
        return self.individuals[best_index]
    def select_parent(self):
        random_number = random.random()*sum(self.fitness_scores)
        running_sum = 0
        for i in self.individuals:
            running_sum += i.fitness
            if running_sum >= random_number:
                return i
        return None
    def selection(self, goal):
        self.next_gen = [person(self.spawn_point, self.steps) for i in range(self.population_size)]
        #self.calc_fitness_scores(goal)
        best_person = self.best_person(goal)
        self.next_gen[0] = best_person.child()
        for i in range(1, len(self.next_gen)):
            parent = self.select_parent()
            self.next_gen[i] = parent.child()
            self.next_gen[i].brain.mutate(parent.fitness)
        self.individuals = deepcopy(self.next_gen)
    def reset(self):
        for i in self.individuals:
            i.reset()
