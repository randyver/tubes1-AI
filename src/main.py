import numpy as np
from algorithms.hill_climbing.stochastic import stochastic_hill_climbing
from algorithms.hill_climbing.steepest_ascent import steepest_ascent

if __name__ == "__main__":
    cube = np.random.choice(range(1,126),size=125,replace=False)

    # result, score = steepest_ascent(cube)
    result, score = stochastic_hill_climbing(cube)
    print(result)
    print("score (out of 109):", score)