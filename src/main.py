import numpy as np
import matplotlib.pyplot as plt
from algorithms.hill_climbing.steepest_ascent import steepest_ascent
from algorithms.hill_climbing.stochastic import stochastic_hill_climbing
from algorithms.hill_climbing.sideways_move import sideways_move
from algorithms.hill_climbing.random_restart import random_restart_hill_climbing

def plot_scores(scores, algorithm_name):
    plt.plot(scores)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Function Value")
    plt.title(f"{algorithm_name} Progress")
    plt.show()

def run_algorithm(algorithm, cube, **kwargs):
    result, score, scores, duration = algorithm(cube, **kwargs)
    print("Final configuration:", result)
    print(f"Final score (out of 109): {score}")
    print(f"Search duration: {duration:.2f} s")
    plot_scores(scores, algorithm.__name__)

if __name__ == "__main__":
    cube = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                     11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                     21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                     31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                     41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                     51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                     61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
                     71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
                     81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                     91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                     101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                     111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                     121, 122, 123, 124, 125])

    print("Choose the algorithm:")
    print("1: Steepest Ascent")
    print("2: Stochastic Hill Climbing")
    print("3: Sideways Move")
    print("4: Random Restart Hill Climbing")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        run_algorithm(steepest_ascent, cube)
    elif choice == "2":
        run_algorithm(stochastic_hill_climbing, cube, iterations=123456)
    elif choice == "3":
        run_algorithm(sideways_move, cube, max_sideways_moves=1000)
    elif choice == "4":
        run_algorithm(random_restart_hill_climbing, cube, iterations=1000, restarts=500)
    else:
        print("Invalid choice. Please select a number between 1 and 4.")