import math
import random
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import concurrent.futures
from functools import partial

# Function to get user input for container type and dimensions
def get_input():
    container_type = input(
        "Enter container type (cylinder/rectangle): ").lower()
    if container_type not in ['cylinder', 'rectangle']:
        print("Invalid input. Please choose either 'cylinder' or 'rectangle'.")
        return get_input()
    if container_type == 'cylinder':
        height = float(input("Enter the height of the cylinder (in cm): "))
        diameter = float(input("Enter the diameter of the cylinder (in cm): "))
        return container_type, height, diameter, None, None
    elif container_type == 'rectangle':
        height = float(input("Enter the height of the rectangle (in cm): "))
        width = float(input("Enter the width of the rectangle (in cm): "))
        length = float(input("Enter the length of the rectangle (in cm): "))
        return container_type, height, None, width, length

# Function to check if a given point is inside a rectangular container
def is_inside_rectangle(x, y, z, r, height, width, length):
    return (
        -width / 2 + r <= x <= width / 2 - r
        and -length / 2 + r <= y <= length / 2 - r
        and 0 + r <= z <= height - r
    )

# Function to check if a given point is inside a cylindrical container
def is_inside_cylinder(x, y, z, r, height, diameter):
    return z >= 0 and z <= height and x ** 2 + y ** 2 <= (diameter / 2) ** 2

# Function to check if two points are within a minimum distance from each other
def check_overlap(x1, y1, z1, x2, y2, z2, min_distance):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) < min_distance ** 2

# Function to perform the Monte Carlo simulation
def monte_carlo_simulation(container_type, height, diameter, width, length, r, iterations):
    if container_type == 'cylinder':
        max_eggs = int(math.pi * (diameter / 2) ** 2 *
                       height / (4 / 3 * math.pi * r ** 3))
    elif container_type == 'rectangle':
        max_eggs = int((width * length * height) / (4 / 3 * math.pi * r ** 3))

    egg_counts = []

    for i in tqdm(range(iterations), desc="Processing"):
        egg_positions = []
        egg_count = 0
        z = 0

        while z <= height:
            for _ in range(max_eggs):
                x, y = (
                    random.uniform(-diameter / 2 + r, diameter / 2 -
                                   r) if container_type == 'cylinder' else random.uniform(width / 2 - r),
                    random.uniform(-diameter / 2 + r, diameter / 2 -
                                   r) if container_type == 'cylinder' else random.uniform(-length / 2 + r, length / 2 - r)
                )
                if container_type == 'cylinder':
                    is_inside = is_inside_cylinder(
                        x, y, z, r, height, diameter)
                elif container_type == 'rectangle':
                    is_inside = is_inside_rectangle(x, y, z, r, height, width, length)
                if not is_inside:
                    continue
                overlap = False
                for pos in egg_positions:
                    if check_overlap(x, y, z, pos[0], pos[1], pos[2], 2 * r):
                        overlap = True
                        break
                if not overlap:
                    egg_positions.append((x, y, z))
                    egg_count += 1
            z += 2 * r
        egg_counts.append(egg_count)
    return egg_counts

# Function to plot the number of eggs found in each iteration
def plot_egg_counts(egg_counts):
    plt.figure()
    iterations = range(1, len(egg_counts) + 1)
    # Scatter plot without lines joining the dots
    plt.scatter(iterations, egg_counts, marker='o', label='Egg counts')
    # Trend line
    z = np.polyfit(iterations, egg_counts, 1)
    p = np.poly1d(z)
    plt.plot(iterations, p(iterations), 'r--')
    plt.xlabel('Iteration')
    plt.ylabel('Number of eggs')
    plt.legend()
    plt.show()

# Worker function to run Monte Carlo simulation for a specified number of iterations
def worker(container_type, height, diameter, width, length, r, iterations_per_worker, pbar):
    result = monte_carlo_simulation(
        container_type, height, diameter, width, length, r, iterations_per_worker)
    pbar.update(iterations_per_worker)
    return result

if __name__ == "__main__":
    container_type, height, diameter, width, length = get_input()
    r = 2.07 / 2  # Egg width in cm divided by 2 for radius
    total_iterations = 20
    # Number of workers (threads) and iterations per worker
    num_workers = min(10, total_iterations)  # Use up to 8 workers
    iterations_per_worker = total_iterations // num_workers

    # Run Monte Carlo simulations in parallel
    with concurrent.futures.ThreadPoolExecutor(num_workers) as executor:
        worker_partial = partial(
            worker, container_type, height, diameter, width, length, r)
        with tqdm(total=total_iterations, desc="Processing") as pbar:
            results = list(executor.map(worker_partial, [
                           iterations_per_worker] * num_workers, [pbar] * num_workers))

    # Combine the results from all workers
    egg_counts = [egg_count for sublist in results for egg_count in sublist]
    avg_eggs = sum(egg_counts) / len(egg_counts)

    print('\n')
    print('\n')
    print('\n')
    print(f"Approximately {int(avg_eggs)} eggs can fit into the {container_type} container using Monte Carlo simulation.")

    volume = (4 / 3) * math.pi * r ** 3
    print(f"The volume of the egg is approximately {volume:.2f} cubic centimeters.")

    plot_egg_counts(egg_counts)

