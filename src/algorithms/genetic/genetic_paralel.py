import numpy as np
import sys
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor

# Add the parent directory of 'algorithms' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import from utils
from utils.count_of_match import count_of_match
from utils.crossover import *
n = 5
magic_number = 315

# generating initial population
def generate_initial_population(size=100) -> list:
    population = []
    for _ in range(size):
        individual = np.random.permutation(n**3) + 1
        population.append(individual)
    return population

# count score of each individual in population
def count_score(population) -> list:
    scores = []
    for individual in population:
        scores.append(count_of_match(individual))
    return scores

# selection function from population to choice parent with weighted weights
def selection(population, scores, k=1) -> list:
    weights = scores if np.sum(scores) > 0 else None
    selected_population = random.choices(population, weights=weights, k=k)
    return selected_population[0]

# mutate function using random mutation
def mutate(individual):
    idx1, idx2 = random.sample(range(n**3), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Cycle Crossover (CX)
def cycle_crossover(parent1, parent2):
    child1 = [-1] * len(parent1)
    child2 = [-1] * len(parent2)
    
    def create_cycle(child, parent1, parent2):
        index = 0
        while index < len(child) and child[index] != -1:
            index += 1
        
        if index == len(child):
            return
        
        start = index
        while True:
            child[index] = parent1[index]
            index_array = np.where(parent1 == parent2[index])[0]
            if len(index_array) == 0:
                break
            index = index_array[0]
            if index == start:
                break

    create_cycle(child1, parent1, parent2)
    create_cycle(child2, parent2, parent1)

    for i in range(len(child1)):
        if child1[i] == -1:
            child1[i] = parent2[i]
        if child2[i] == -1:
            child2[i] = parent1[i]

    return child1, child2


import numpy as np


# genetic algorithm with parallel processing
def genetic_algorithm(fitness_fun, iterations=1000, population_size=100, shuffle = False):
    best_score = 0
    population = generate_initial_population(size=population_size)

    for iter in range(iterations):
        scores = count_score(population)
        individual_with_best_score = np.argmax(scores)
        best_score = scores[individual_with_best_score]
        if (iter+1)%10 ==0 :
            print(f"Best score in {iter+1}-iterations: {best_score} populasi ke: {individual_with_best_score}")
        
        new_population = []
        with ThreadPoolExecutor() as executor:
            # Generate children in parallel
            futures = [
                executor.submit(create_children, population, scores, fitness_fun,iter,iterations)
                for _ in range(population_size // 2)
            ]
            for future in futures:
                child1, child2 = future.result()
                new_population.extend([child1, child2])
        
        if shuffle == True:
            random.shuffle(new_population)
        population = new_population

    final_solution_index = np.argmax(scores)
    final_solution = population[final_solution_index]
    print("konfigurasi: ", final_solution)
    print("score akhir: ", best_score)
    return final_solution

def create_children(population, scores, fitness_fun,iter,total_iteration):
    parent1 = selection(population, scores)
    parent2 = selection(population, scores)
    child1, child2 = fitness_fun(parent1, parent2,iterations =total_iteration, current_iteration = iter)
    
    if random.random() < 0.15:
        child1 = mutate(child1)
    if random.random() < 0.15:
        child2 = mutate(child2)
    
    return child1, child2

start_time = time.time()

final_solution = genetic_algorithm(custom_probabilistic_randomized_segment_preserving_crossover, 8000, 400,shuffle=True)
end_time = time.time()
if(len(final_solution) == len(np.unique(final_solution))):
    print(len(final_solution))
    print("ARRAY UNIK")
else:
    print("Salah cok")

print("Elapsed time: {:.6f} seconds".format(end_time - start_time))

print(find_segments_with_magic_number(final_solution))