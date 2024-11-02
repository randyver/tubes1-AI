import numpy as np
import matplotlib.pyplot as plt
from algorithms.hill_climbing.steepest_ascent import steepest_ascent
from algorithms.hill_climbing.stochastic import stochastic_hill_climbing
from algorithms.hill_climbing.sideways_move import sideways_move
from algorithms.hill_climbing.random_restart import random_restart_hill_climbing
from algorithms.simulated_annealing.simulated_annealing import simulated_annealing

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
        count_iteration, count_restart, result, score, scores, duration = result
    elif algorithm.__name__ == "simulated_annealing":
        algorithm_name = "Simulated Annealing"
        count_iteration, result, score, scores, probabilities, count_stuck, duration = result
        count_restart = 0

    print(f"Final Cube: {result}")
    print(f"Final Objective Function Value: {score}")
    print(f"Search Duration: {duration:.2f} s")
    print(f"Number of Iterations: {count_iteration}")
    if algorithm.__name__ == "random_restart_hill_climbing":
        print(f"Number of Restarts: {count_restart}")
    elif algorithm.__name__ == "simulated_annealing":
        print(f"Number of Stuck Moves: {count_stuck}")

    plot_scores(scores, algorithm_name)
    # if algorithm.__name__ == "simulated_annealing":
    #     unique_probabilities, count_unique_probabilities = np.unique(probabilities, return_counts=True)

    #     plt.plot(count_unique_probabilities, unique_probabilities)
    #     plt.xlabel("Probability")
    #     plt.ylabel("Count")
    #     plt.title("Probability Progress (Line Plot)")
    #     plt.grid(True)
    #     plt.show()
    if algorithm.__name__ == "simulated_annealing":
        subsampled_probabilities = probabilities[::2000]
        subsampled_iterations = np.arange(len(subsampled_probabilities)) * 2000

        plt.plot(subsampled_iterations, subsampled_probabilities)
        plt.xlabel("Iteration")
        plt.ylabel("Probability")
        plt.title("Smoothed Probability Progress")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    cube = np.random.permutation(125) + 1
    
    print("Choose the algorithm:")
    print("1: Steepest Ascent")
    print("2: Stochastic Hill Climbing")
    print("3: Sideways Move")
    print("4: Random Restart Hill Climbing")
    print("5: Simulated Annealing")
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
    else:
        print("Invalid choice. Please select a number between 1 and 5.")