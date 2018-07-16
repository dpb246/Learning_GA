'''
Based on java code found: https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3
Used to learn basic structure of genetic algorithm
'''
import random as rn

length_of_genes = 5
population_size = 10

class individual:
    def __init__(self, number_of_genes):
        self.fitness = 0
        self.genes = [rn.randint(0,1) for i in range(number_of_genes)]
    def calc_fitness(self):
        self.fitness = 0
        for gene in self.genes:
            if gene == 1:
                self.fitness += 1

class population:
    def __init__(self, population_size):
        self.individuals = [individual(length_of_genes) for i in range(population_size)]
        self.fittest = 0
    def get_fittest(self):
        max_fit = -1
        index_max_fit = 0
        for index, thing in enumerate(self.individuals):
            if thing.fitness > max_fit:
                max_fit = thing.fitness
                index_max_fit = index
        self.fittest = self.individuals[index_max_fit].fitness
        return self.individuals[index_max_fit]
    def get_second_fittest(self):
        max_fit = 0
        second_fittest = 0
        for index in range(len(self.individuals)):
            if self.individuals[index].fitness > self.individuals[max_fit].fitness:
                second_fittest = max_fit
                max_fit = index
            elif self.individuals[index].fitness > self.individuals[second_fittest].fitness:
                second_fittest = index
        return self.individuals[second_fittest]
    def get_least_fit(self):
        least_fit_index = 0
        for index in range(len(self.individuals)):
            if self.individuals[index].fitness < self.individuals[least_fit_index].fitness:
                least_fit_index = index
        return index
    def calc_fitness(self):
        for thing in self.individuals:
            thing.calc_fitness()
        self.get_fittest()
def get_fittest_individual(in1, in2):
    if in1.fitness > in2.fitness:
        return in1
    return in2
def main():
    opposite = {
        0: 1,
        1: 0
    }
    gen_count = 0
    pop = population(10)
    pop.calc_fitness()
    print("Gen:", gen_count, "Fittest:", pop.fittest)
    while(pop.fittest < length_of_genes):
        gen_count += 1
        #Selection
        fittest = pop.get_fittest()
        second_fittest = pop.get_second_fittest()
        #cross_over
        for i in range(rn.randint(0, length_of_genes-1)):
            temp = fittest.genes[i]
            fittest.genes[i] = second_fittest.genes[i]
            second_fittest.genes[i] = temp
        if rn.randint(0,7) < 5:
            #Mutation
            mutation_point = rn.randint(0, length_of_genes-1)
            fittest.genes[mutation_point] = opposite[fittest.genes[mutation_point]]
            mutation_point = rn.randint(0, length_of_genes-1)
            second_fittest.genes[mutation_point] = opposite[second_fittest.genes[mutation_point]]
        #add_fittest_offspring
        fittest.calc_fitness()
        second_fittest.calc_fitness()
        pop.individuals[pop.get_least_fit()] = get_fittest_individual(fittest, second_fittest)

        pop.calc_fitness()
        print("Gene:", gen_count, "Fittest:", pop.fittest)

    print("Solved")
    print("Took {} generations".format(gen_count))
    print(pop.get_fittest().genes)
main()
