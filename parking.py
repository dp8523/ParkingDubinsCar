import random

from control import Control
import constants
import genetic_solver
from individual import Individual


def main():
    population = []
    for i in range(constants.population_size):
        current_individual = Individual()
        for j in range(constants.num_optimization_parameters):
            random_gamma_decimal = random.randint(0, 2**constants.chromosome_length - 1)
            random_beta_decimal = random.randint(0, 2**constants.chromosome_length - 1)

            random_gamma_gray = Control.get_gray(random_gamma_decimal)
            random_beta_gray = Control.get_gray(random_beta_decimal)

            current_control = Control(random_gamma_gray, random_beta_gray)
            current_individual.add_control(current_control)
        population.append(current_individual)

    best_individual = genetic_solver.genetic_algorithm(population)

    print()
    best_individual.print_final_state()
    best_individual.plot_control_history()
    best_individual.plot_state_history()


if __name__ == '__main__':
    main()
