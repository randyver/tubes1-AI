# Local Search Algorithm | Diagonal Magic Cube
Tugas Besar 1 IF3170 Artificial Intelligence 2024/2025

<div align="center">
    <img src="/diagonal-magic-cube.png" alt="Diagonal Magic Cube">
</div>

## 1. Description
This project implements various local search algorithms for solving Diagonal Magic Cube, such as Steepest Ascent Hill Climbing, Stochastic Hill Climbing, Sideways Move Hill Climbing, Random Restart Hill Climbing, Simulated Annealing, and Genetic Algorithm.

## 2. Features
- 🔼 **Steepest Ascent Hill Climbing**: A local search algorithm that moves in the direction of the steepest increase in objective function.
- 🎲 **Stochastic Hill Climbing**: A variant of hill climbing where random neighbors are chosen.
- ↔️ **Sideways Move Hill Climbing**: Allows sideways moves to escape plateaus.
- 🔁 **Random Restart Hill Climbing**: Runs multiple hill climbing searches from different starting points.
- ❄️ **Simulated Annealing**: A probabilistic technique to escape local optima.
- 🧬 **Genetic Algorithm**: Uses crossover and mutation to explore the solution space.
- 🧊 **Visualization**: Visualize the performance and results of each algorithm using various graphs and 3D visualizations of the initial and result cubes.

## 3. Requirements
- Python
- Numpy
- Plotly
- Matplotlib

### 4. How to set up
1. Clone the repository
```
git clone https://github.com/randyver/tubes1-AI.git
```
2. Navigate to the project directory
```
cd tubes1-AI
```
3. Install the required libraries
```
pip install numpy plotly matplotlib
```

### 5. How to run
1. Run the main program
```
python main.py
```
2. Follow the prompts to select an algorithm and input parameters if required

### 6. Task distribution
| NIM |  Name  | Task |
|-----|--------|------|
| 13522067   | Randy Verdian | Steepest Ascent HC, Stochastic HC, Sideways Move HC, Random Restart HC |
| 13522079  |  Emery Fathan Zwageri  |   Genetic Algorithm |
| 13522092 | Sa'ad Abdul Hakim |    Simulated Annealing |
| 13522097 | Ellijah Darrellshane S. | Visualisasi|