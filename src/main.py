import numpy as np
import matplotlib.pyplot as plt
from algorithms.hill_climbing.steepest_ascent import steepest_ascent
from algorithms.hill_climbing.stochastic import stochastic_hill_climbing
from algorithms.hill_climbing.sideways_move import sideways_move
from algorithms.hill_climbing.random_restart import random_restart_hill_climbing
from algorithms.simulated_annealing.simulated_annealing import simulated_annealing
from utils import cube_plot as cp

from algorithms.genetic.genetic_paralel import GeneticAlgorithm
from algorithms.genetic.plot_ga import plot_iteration_scores_GA

def plot_scores(scores, algorithm_name):
    plt.plot(scores)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Function Value")
    plt.title(f"{algorithm_name} Progress")
    plt.show()

def run_algorithm(algorithm, cube, **kwargs):
    result = algorithm(cube, **kwargs)
    
    if algorithm.__name__ in ["steepest_ascent", "stochastic_hill_climbing", "sideways_move"]:
        if algorithm.__name__ == "steepest_ascent":
            algorithm_name = "Steepest Ascent"
        elif algorithm.__name__ == "stochastic_hill_climbing":
            algorithm_name = "Stochastic Hill Climbing"
        elif algorithm.__name__ == "sideways_move":
            algorithm_name = "Sideways Move"
        count_iteration, result, score, scores, duration = result
        count_restart = 0
    elif algorithm.__name__ == "random_restart_hill_climbing":
        algorithm_name = "Random Restart Hill Climbing"
        count_restart, result, score, scores, duration = result
    elif algorithm.__name__ == "simulated_annealing":
        algorithm_name = "Simulated Annealing"
        count_iteration, result, score, scores, probabilities, count_stuck, duration = result
        count_restart = 0

    print(f"Initial Cube: {cube}")
    print(f"Final Cube: {result}")
    print(f"Final Objective Function Value: {score}")
    print(f"Search Duration: {duration:.2f} s")
    if algorithm.__name__ in ["steepest_ascent", "stochastic_hill_climbing", "sideways_move"]:
        print(f"Number of Iterations: {count_iteration}")
    elif algorithm.__name__ == "random_restart_hill_climbing":
        print(f"Number of Restarts: {count_restart}")
    elif algorithm.__name__ == "simulated_annealing":
        print(f"Number of Stuck Moves: {count_stuck}")

    plot_scores(scores, algorithm_name)

    if algorithm.__name__ == "simulated_annealing":
        subsampled_probabilities = probabilities[::2000]
        subsampled_iterations = np.arange(len(subsampled_probabilities)) * 2000

        plt.plot(subsampled_iterations, subsampled_probabilities)
        plt.xlabel("Iteration")
        plt.ylabel("Probability")
        plt.title("Smoothed Probability Progress")
        plt.grid(True)
        plt.show()

    cp.main(result)

def run_GA(crossover_func : str, population_size : int, iterations: int):
    genetic_solver = GeneticAlgorithm(crossover_func =crossover_func, population_size=population_size,iterations=iterations,shuffle=True)
    solution = genetic_solver.solve()
    elapsed_time = solution['elapsed_time']
    best_initial_state = solution['best_initial_state']
    best_final_state_index = solution['best_index']
    best_final_state_config = solution['best_config']
    matched_segment_list = solution['matched_list']
    print("State awal:", best_initial_state)
    print(f"State solusi: populasi ke-{best_final_state_index}, konfigurasi:", best_final_state_config)
    print("Daftar segment matched-315:", matched_segment_list)
    print("Score(obj value):", str(solution["best_score"])+"/109")
    print("Waktu:", elapsed_time, "sec")
    plot_iteration_scores_GA(solution["iteration_scores"])

    cp.main(best_final_state_config)

if __name__ == "__main__":
    cube = np.random.permutation(125) + 1
    
    print("Choose the algorithm:")
    print("1: Steepest Ascent")
    print("2: Stochastic Hill Climbing")
    print("3: Sideways Move")
    print("4: Random Restart Hill Climbing")
    print("5: Simulated Annealing")
    print("6: Genetic Algorithm")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        run_algorithm(steepest_ascent, cube)
    elif choice == "2":
        run_algorithm(stochastic_hill_climbing, cube, iterations=123456)
    elif choice == "3":
        run_algorithm(sideways_move, cube, max_sideways_moves=1000)
    elif choice == "4":
        run_algorithm(random_restart_hill_climbing, cube, iterations=1000, max_restarts=500)
    elif choice == "5":
        run_algorithm(simulated_annealing, cube, initial_temp=100, cooling_rate=0.8, max_iter=121000)
    elif choice == "6":
        print("1. Probabilistic Crossover (allowing downhill in the middle iterations)")
        print("2. Non-probabilistic Crossover")
        crossover_choice = input("Enter the number of your choice: ")
        if crossover_choice == 1:
            crossover = "Probabilistic"
        else:
            crossover = "Randomized"
        population_size = int(input("Enter population size: "))
        iterations = int(input("Enter max iteration: "))
        run_GA(crossover_choice, population_size, iterations)
    else:
        print("Invalid choice. Please select a number between 1 and 6.")