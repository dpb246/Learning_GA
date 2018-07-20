from individual import *
import time
import random
from copy import deepcopy
'''
Population of individuals, contains all the evolutionary logic
'''
class population:
    def __init__(self, spawn_point, population_size=10, steps=100):
        self.individuals = [person(spawn_point, steps) for i in range(population_size)]
        self.positions = []
        self.fitness_scores = []
        self.fittest = 0
        self.min_steps = 10000
        self.spawn_point = spawn_point
        self.population_size = population_size
        self.steps = steps
    def move(self):
        self.positions = []
        for i in range(len(self.individuals)):
            self.individuals[i].move()
            self.positions.append(self.individuals[i].get_pos())
    def get_positions(self):
        return self.positions
    def calc_fitness_scores(self, goal):
        self.fitness_scores = [p.get_fitness(goal) for p in self.individuals]
        self.best_person(goal)
        return self.fitness_scores
    def everyone_dead(self):
        for person in self.individuals:
            if not person.is_dead and not person.win:
                return False
        return True
    def best_person(self, goal):
        best_index= 0
        best_score = 0 #Smaller score means closer and better
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
            if running_sum > random_number:
                return i
        return None
    def create_child(self, individual1, individual2):
        child = person(individual1.starting_pos, individual1.steps, individual1.max_speed)
        for i in range(individual1.steps):
            if (100 * random.random() < 50):
                child.brain.steps[i] = individual1.brain.steps[i]
            else:
                child.brain.steps[i] = individual2.brain.steps[i]
        child.brain.mutate()
        return deepcopy(child) #randomly select each allel from the two parents
    def select_breeders(self, population_sorted):
        result = []
        best_individuals = self.population_size / 5
        lucky_few = self.population_size / 5
        for i in range(int(best_individuals)):
            result.append(population_sorted[i])
        for i in range(int(lucky_few)):
            result.append(random.choice(population_sorted))
        random.shuffle(result)
        return result
    def selection(self, goal):
        self.next_gen = []
        self.calc_fitness_scores(goal)
        best_person = self.best_person(goal)
        self.next_gen.append(best_person.child())
        for i in range(1, self.population_size-3, 2):
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            for j in range(2):
                self.next_gen.append(self.create_child(parent1, parent2))
                self.next_gen[-1].brain.mutate()
        for j in range(2):
            self.next_gen.append(best_person.child())
            self.next_gen[-1].brain.special_mutate()
        self.individuals = deepcopy(self.next_gen)
    def reset(self):
        for i in self.individuals:
            i.reset()
