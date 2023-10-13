import random

import constants

from control import Control
from individual import Individual


def proportionate_selection(population):
    fitness_sum = 0
    fitnesses = []
    for individual in population:
        fitness = individual.get_fitness()
        fitness_sum += fitness
        fitnesses.append(fitness)
    fitness_ratios = [fitness / fitness_sum for fitness in fitnesses]

    result = random.choices(population, weights=fitness_ratios, k=2)
    while result[0] == result[1]:
        result = random.choices(population, weights=fitness_ratios, k=2)

    return result


def reproduce(parent1, parent2):
    child1 = Individual()
    child2 = Individual()
    for i in range(len(parent1.controls)):
        c1 = random.randint(0, 6)
        c2 = random.randint(0, 6)

        gamma1 = parent1.controls[i].gamma[:c1] + parent2.controls[i].gamma[c1:]
        gamma2 = parent2.controls[i].gamma[:c1] + parent1.controls[i].gamma[c1:]

        beta1 = parent1.controls[i].beta[:c2] + parent2.controls[i].beta[c2:]
        beta2 = parent2.controls[i].beta[:c2] + parent1.controls[i].beta[c2:]

        child1.add_control(Control(gamma1, beta1))
        child2.add_control(Control(gamma2, beta2))

    return child1, child2


def mutate(individual):
    mutated = Individual()
    for control in individual.controls:
        new_gamma = ''
        new_beta = ''
        for i in range(constants.chromosome_length):
            if random.random() < constants.mutation_rate:
                if control.gamma[i] == '0':
                    new_gamma += '1'
                else:
                    new_gamma += '0'
            else:
                new_gamma += control.gamma[i]

        for i in range(constants.chromosome_length):
            if random.random() < constants.mutation_rate:
                if control.beta[i] == '0':
                    new_beta += '1'
                else:
                    new_beta += '0'
            else:
                new_beta += control.beta[i]

        mutated.add_control(Control(new_gamma, new_beta))

    return mutated


def genetic_algorithm(init_population):
    population = init_population
    gen_count = 0
    population.sort(key=lambda x: x.get_fitness(), reverse=True)
    fittest_cost = population[0].get_cost()
    print('Generation', gen_count, ': J =', fittest_cost)
    while fittest_cost > 0.1:
        next_generation = []
        for i in range(10):
            next_generation.append(population[i])
        for i in range(len(population) // 2 - 5):
            parent1, parent2 = proportionate_selection(population)
            child1, child2 = reproduce(parent1, parent2)
            mutated1 = mutate(child1)
            mutated2 = mutate(child2)
            next_generation.append(mutated1)
            next_generation.append(mutated2)
        population = next_generation
        population.sort(key=lambda x: x.get_fitness(), reverse=True)
        fittest_cost = population[0].get_cost()
        gen_count += 1
        print('Generation', gen_count, ': J =', fittest_cost)
    return population[0]
