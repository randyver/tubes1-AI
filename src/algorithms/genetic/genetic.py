import numpy as np
import sys
import os
import time
import random
# Add the parent directory of 'algorithms' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import from utils
from utils.count_of_match import count_of_match

n = 5
magic_number = 315
# generating initial population
def generate_initial_population(size = 100) -> list:
    population = []
    for _ in range(size):
        individual = np.random.permutation(n**3)+1
        population.append(individual)
    
    return population

init = generate_initial_population(3)
# count score of the each individual in population
def count_score(population) -> list:
    scores = []
    for individual in population:
        scores.append(count_of_match(individual))
    
    return scores
# selection function from population to choice parent with weighted weights. weights is None if total weigth is zero
def selection(population, scores, k=1) -> list:
    weights = scores if np.sum(scores) > 0 else None
    selected_population = random.choices(population, weights=weights,k=k)
    return selected_population[0]

# mutate function. use random mutation
def mutate(individual):
    idx1, idx2 = random.sample(range(n*3),2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Crossover functions

# Order Crossover (OX)
def order_crossover(parent1, parent2):
    # Menentukan dua titik potong secara acak
    idx1, idx2 = sorted(random.sample(range(len(parent1)), 2))
    # Membuat anak dengan mengisi segmen di antara titik potong dari parent1
    child1 = [-1] * len(parent1)
    child2 = [-1] * len(parent2)
    # Salin bagian dari parent1 ke child1 dan parent2 ke child2 di antara dua titik potong
    child1[idx1:idx2] = parent1[idx1:idx2]
    child2[idx1:idx2] = parent2[idx1:idx2]
    # Mendapatkan elemen yang belum ada dalam anak dari parent lain, sesuai urutan
    def fill_remaining(child, parent, idx1, idx2):
        current_pos = idx2
        for i in range(len(parent)):
            elem = parent[(i + idx2) % len(parent)]
            if elem not in child:
                child[current_pos % len(child)] = elem
                current_pos += 1
    # Mengisi elemen yang tersisa dari parent lain
    fill_remaining(child1, parent2, idx1, idx2)
    fill_remaining(child2, parent1, idx1, idx2)

    return child1, child2

# Partially Mapped Crossover (PMX) dengan pengecekan untuk menghindari error
def pmx_crossover(parent1, parent2):
    # Tentukan dua titik potong secara acak
    idx1, idx2 = sorted(random.sample(range(len(parent1)), 2))
    
    # Membuat salinan dari parent untuk child
    child1, child2 = parent1.copy(), parent2.copy()
    
    # Tukar segmen di antara titik potong
    child1[idx1:idx2], child2[idx1:idx2] = parent2[idx1:idx2], parent1[idx1:idx2]
    
    # Pemetaan elemen untuk child1
    for i in range(idx1, idx2):
        elem1, elem2 = parent1[i], parent2[i]
        # Lakukan pemetaan elemen agar tidak ada duplikasi
        if elem1 != elem2:
            # Cek apakah elem2 ada di child1 dan elem1 ada di child1
            pos1 = np.where(child1 == elem2)[0]
            pos2 = np.where(child1 == elem1)[0]
            if len(pos1) > 0 and len(pos2) > 0:
                pos1, pos2 = pos1[0], pos2[0]
                child1[pos1], child1[pos2] = child1[pos2], child1[pos1]

    # Pemetaan elemen untuk child2
    for i in range(idx1, idx2):
        elem1, elem2 = parent1[i], parent2[i]
        if elem1 != elem2:
            # Cek apakah elem2 ada di child2 dan elem1 ada di child2
            pos1 = np.where(child2 == elem2)[0]
            pos2 = np.where(child2 == elem1)[0]
            if len(pos1) > 0 and len(pos2) > 0:
                pos1, pos2 = pos1[0], pos2[0]
                child2[pos1], child2[pos2] = child2[pos2], child2[pos1]

    return child1, child2

import numpy as np

def cycle_crossover(parent1, parent2):
    # Buat dua anak dengan panjang yang sama dengan induk dan inisialisasi dengan nilai -1
    child1 = [-1] * len(parent1)
    child2 = [-1] * len(parent2)
    
    # Fungsi untuk membentuk siklus dan menukarkan elemen sesuai siklus
    def create_cycle(child, parent1, parent2):
        # Mulai dari indeks pertama yang belum diisi
        index = 0
        while index < len(child) and child[index] != -1:
            index += 1
        
        if index == len(child):  # Semua elemen telah diproses
            return
        
        start = index
        while True:
            # Set elemen parent1 ke child
            child[index] = parent1[index]
            # Cari indeks elemen yang sama di parent2 menggunakan np.where
            index_array = np.where(parent1 == parent2[index])[0]
            if len(index_array) == 0:
                break
            index = index_array[0]
            if index == start:
                break

    # Bentuk siklus pada child1 menggunakan parent1 dan parent2
    create_cycle(child1, parent1, parent2)
    # Bentuk siklus pada child2 menggunakan parent2 dan parent1
    create_cycle(child2, parent2, parent1)

    # Lengkapi child1 dan child2 dengan elemen dari parent yang tidak ada dalam siklus
    for i in range(len(child1)):
        if child1[i] == -1:
            child1[i] = parent2[i]
        if child2[i] == -1:
            child2[i] = parent1[i]

    return child1, child2


# genetic algorithm
def genetic_algorithm(fitness_fun ,iterations = 1000, population_size = 100 ):
    best_score = 0
    population = generate_initial_population(size = population_size)
    for iter in range(iterations):
        scores = count_score(population)
        individual_with_best_score = np.argmax(scores)
        best_score = scores[individual_with_best_score]
        print(f"Best score in {iter+1}-iterations: {best_score} populasi ke: {individual_with_best_score}")
        
        new_population = []
        for _ in range(population_size//2):
            parent1 = selection(population,scores)
            parent2 = selection(population,scores)
            child1, child2 = fitness_fun(parent1,parent2)
            if random.random() < 0.2:
                child1 = mutate(child1)
            if random.random() < 0.2:
                child2 = mutate(child2)
            new_population.extend([child1,child2])
        population = new_population

    final_solution_index = np.argmax(scores)
    final_solution = population[final_solution_index]
    print("konfigurasi: ",np.array(final_solution).reshape(5,5,5))
    print("score akhir: ", best_score)

start_time = time.time()
genetic_algorithm(cycle_crossover, 100, 1000)
end_time = time.time()

# Menampilkan waktu dalam detik dengan 6 desimal
print("Elapsed time: {:.6f} seconds".format(end_time - start_time))

# scores = count_score(init)
# selected_parent = selection(init,scores,len(init))
# for i in init:
#     print (i[:10])
# for initial, parent in zip(init,selected_parent):
#     print(f"initial: {initial[:10]}")
#     print(f"selected: {parent[:10]}")



# for i in init:
    
#     if(len(np.unique(i)) == len(i)):
#        print(f"{i}:\n unik ") 
#     else:
#         print(f"{i} tidak unik")

