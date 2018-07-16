from individual import *
import time
class population:
    def __init__(self, spawn_point, population_size=10, steps=100):
        self.individuals = [person(spawn_point, steps) for i in range(population_size)]
        self.positions = []
        self.fitness_scores = []
        self.fittest = 100000000
    def move(self, step):
        self.positions = []
        for i in range(len(self.individuals)):
            self.individuals[i].move(step)
            self.positions.append(self.individuals[i].get_pos())
    def get_positions(self):
        return self.positions
    def calc_fitness_scores(self, goal):
        self.fitness_scores = [p.get_fitness(goal) for p in self.individuals]
        return self.fitness_scores
    def best_person(self, goal):
        self.calc_fitness_scores(goal)
        best_index= 0
        best_score = 10000000000 #Smaller score means closer and better
        for index, score in enumerate(self.fitness_scores):
            if score < best_score:
                best_score = score
                best_index = index
        self.fittest = best_score
        return self.individuals[best_index]
