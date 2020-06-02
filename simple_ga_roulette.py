#demo python program for the use of GA in finding out maxima of a function x^2+y^2 subj to -5<=x,y<=5
#The program is a modification of code found in https://hackernoon.com/genetic-algorithms-explained-a-python-implementation-sd4w374i for learning purposes


import random
import math




#below function is used to generate the initial population and use that to form parent and offsprings
def initial_population(size,x_limit,y_limit):
    lower_x_limit, upper_x_limit = x_limit
    lower_y_limit, upper_y_limit = y_limit
    population = []
    for i in range(size):
        individual = {
        "x": random.uniform(lower_x_limit, upper_x_limit),
        "y": random.uniform(lower_y_limit, upper_y_limit),
        }
        population.append(individual)
    return population

#if initial population is already available , then just load into population array

#fitness function to identify which are the best parents
def fitness_function(individual):
    x = individual["x"]
    y = individual["y"]
    fitness = math.sqrt(x ** 2 + y ** 2)
    return fitness

def sorted_population(population):
    return sorted(population, key = fitness_function)

def roulette_selection(sorted_population,fitness_sum):
    offset = 0
    normalized_fitness = fitness_sum

    lowest_fitness = fitness_function(sorted_population[0])
    if lowest_fitness<0:
        offset = lowest_fitness
        normalized_fitness += offset*len(sorted_population)

    draw = random.uniform(0,1)

    accumulated = 0
    for individual in sorted_population:
        fitness = fitness_function(individual) + offset
        probability_selection = fitness/fitness_sum
        accumulated += probability_selection

        if draw <=accumulated:
            return individual

def crossover(individual_1,individual_2):
    x1 = individual_1["x"]
    y1 = individual_1["y"]

    x2 = individual_2["x"]
    y2 = individual_2["y"]

    return {"x" : (x1+x2)/2, "y" : (y1+y2)/2}

def mutation(individual):
    next_x = individual["x"] + random.uniform(-0.05, 0.05)
    next_y = individual["y"] + random.uniform(-0.05, 0.05)

    lower_boundary, upper_boundary = (-4, 4)

    # Guarantee we keep inside boundaries
    next_x = min(max(next_x, lower_boundary), upper_boundary)
    next_y = min(max(next_y, lower_boundary), upper_boundary)

    return {"x": next_x, "y": next_y}

def make_next_generation(previous_population):
    next_generation = []
    sorted_by_fitness_population = sorted_population(previous_population)
    population_size = len(previous_population)
    fitness_sum = sum(fitness_function(individual) for individual in population)

    for i in range(population_size):
        first_choice = roulette_selection(sorted_by_fitness_population, fitness_sum)
        second_choice = roulette_selection(sorted_by_fitness_population, fitness_sum)

        individual = crossover(first_choice, second_choice)
        individual = mutation(individual)
        next_generation.append(individual)

    return next_generation

if __name__ == '__main__':
    population = initial_population(size = 20, x_limit = (-5,5), y_limit = (-5,5))
    print(population)
    no_generation = 1000
    i = 1
    while True:
        print(f" Generation {i}")
        for individual in population:
            print(individual, fitness_function(individual))
        if i == no_generation:
            break
        i = i+1
        population = make_next_generation(population)

best_individual = sorted_population(population)[-1]
print("\n FINAL RESULT")
print(best_individual, fitness_function(best_individual))
