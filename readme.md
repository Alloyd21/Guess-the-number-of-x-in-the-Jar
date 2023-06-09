# Egg Packing Estimator

This script estimates the number of eggs that can fit inside a given container using Monte Carlo simulations. The user can choose between a cylindrical or rectangular container and input its dimensions. The script will then perform multiple iterations of the simulation and output the average number of eggs that can fit inside the specified container.

## Dependencies

To run this script, you will need the following Python packages:

- `math`
- `random`
- `matplotlib.pyplot`
- `numpy`
- `tqdm`
- `concurrent.futures`
- `functools`



## Installation

Before running the script, you need to install the required packages. If you do not have the packages installed, you can use the following command to install them:

```
bashCopy code
pip install matplotlib numpy tqdm
```

This command will install the `matplotlib`, `numpy`, and `tqdm` packages, as the other dependencies are part of Python's standard library.

## Running the Script

1. Open your terminal (Linux or macOS) or Command Prompt (Windows).
2. Navigate to the directory containing the script (e.g., `cd /path/to/your/script/folder`).
3. Run the script using the command: `python egg_packing_estimator.py`. Make sure to replace `egg_packing_estimator.py` with the name of the script file if it has a different name.

## Usage

1. Run the script in your terminal or IDE.
2. Input the container type you want to use (either `cylinder` or `rectangle`).
3. Enter the required dimensions for the chosen container type.
4. The script will then run the Monte Carlo simulation and output the estimated number of eggs that can fit inside the container.
5. Additionally, the script will display a scatter plot with the number of eggs found in each iteration.

## Functions

### `get_input()`

Prompts the user for the container type and its dimensions.

### `is_inside_rectangle(x, y, z, r, height, width, length)`

Checks if a given point is inside the rectangular container.

### `is_inside_cylinder(x, y, z, r, height, diameter)`

Checks if a given point is inside the cylindrical container.

### `check_overlap(x1, y1, z1, x2, y2, z2, min_distance)`

Checks if two points are within a minimum distance from each other.

### `monte_carlo_simulation(container_type, height, diameter, width, length, r, iterations)`

Performs the Monte Carlo simulation to estimate the number of eggs that can fit inside the container.

### `plot_egg_counts(egg_counts)`

Plots the number of eggs found in each iteration as a scatter plot.

### `worker(container_type, height, diameter, width, length, r, iterations_per_worker, pbar)`

A worker function that runs the Monte Carlo simulation for a specified number of iterations.

## Notes

- This script assumes an average egg width of 2.07 cm.
- The script uses a default of 20 iterations for the Monte Carlo simulation, and up to 10 worker threads for parallel processing.