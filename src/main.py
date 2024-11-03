import numpy as np
import matplotlib.pyplot as plt
from algorithms.hill_climbing.steepest_ascent import steepest_ascent
from algorithms.hill_climbing.stochastic import stochastic_hill_climbing
from algorithms.hill_climbing.sideways_move import sideways_move
from algorithms.hill_climbing.random_restart import random_restart_hill_climbing
from algorithms.simulated_annealing.simulated_annealing import simulated_annealing
from algorithms.genetic.genetic_paralel import GeneticAlgorithm
from algorithms.genetic.plot_ga import plot_iteration_scores_GA
from utils import cube_plot as cp

def plot_scores(scores, algorithm_name):
    plt.plot(scores)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Function Value")
    plt.title(f"{algorithm_name} Progress")
    plt.show()

def run_algorithm(algorithm, cube, **kwargs):
    print("Running algorithm...")
    cp.main(cube)
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

    print(f"Final Objective Function Value: {score}")
    print(f"Search Duration: {duration:.2f} s")
    if algorithm.__name__ in ["steepest_ascent", "stochastic_hill_climbing", "sideways_move"]:
        print(f"Number of Iterations: {count_iteration}")
    elif algorithm.__name__ == "random_restart_hill_climbing":
        print(f"Number of Restarts: {count_restart}")
    elif algorithm.__name__ == "simulated_annealing":
        print(f"Number of Stuck Moves: {count_stuck}")

    cp.main(result)
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

def run_GA(crossover_func : str, population_size : int, iterations: int):
    print("Running algorithm...")
    genetic_solver = GeneticAlgorithm(crossover_func =crossover_func, population_size=population_size,iterations=iterations,shuffle=True)
    solution = genetic_solver.solve()
    best_final_state_config = solution['best_config']
    score = solution['best_score']
    duration = solution['elapsed_time']
    print(f"Final Objective Function Value: {score}")
    print(f"Search Duration: {duration:.2f} s")
    cp.main(best_final_state_config)
    plot_iteration_scores_GA(solution["iteration_scores"])

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
        iterations = int(input("Enter the number of iterations: "))
        run_algorithm(stochastic_hill_climbing, cube, iterations=iterations)
    elif choice == "3":
        max_sideways_moves = int(input("Enter the maximum number of sideways moves: "))
        run_algorithm(sideways_move, cube, max_sideways_moves=max_sideways_moves)
    elif choice == "4":
        iterations_per_restart = int(input("Enter the number of iterations per restart: "))
        max_restarts = int(input("Enter the maximum number of restarts: "))
        run_algorithm(random_restart_hill_climbing, cube, iterations=iterations_per_restart, max_restarts=max_restarts)
    elif choice == "5":
        initial_temp = float(input("Enter the initial temperature: "))
        cooling_rate = float(input("Enter the cooling rate: "))
        max_iter = int(input("Enter the maximum number of iterations: "))
        run_algorithm(simulated_annealing, cube, initial_temp=initial_temp, cooling_rate=cooling_rate, max_iter=max_iter)
    elif choice == "6":
        print("1. Probabilistic Crossover (allowing downhill in the middle iterations)")
        print("2. Non-probabilistic Crossover")

        while True:
            crossover_choice = input("Enter the number of your choice: ")
            if crossover_choice in ["1", "2"]:
                break
            else:
                print("Invalid choice. Please select 1 or 2.")

        population_size = int(input("Enter population size: "))
        iterations = int(input("Enter max iteration: "))
        run_GA(crossover_choice, population_size, iterations)
    else:
        print("Invalid choice. Please select a number between 1 and 6.")