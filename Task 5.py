import numpy as np
from numpy import inf

# Distance matrix
d = np.array([[0,10,12,11,14],
              [10,0,13,15,8],
              [12,13,0,9,14],
              [11,15,9,0,16],
              [14,8,14,16,0]])

iteration = 100
n_ants = 5
n_citys = 5
m = n_ants
n = n_citys
e = 0.5  # evaporation rate
alpha = 1
beta = 2

# Visibility matrix (1/distance), no division by zero
visibility = 1 / d
visibility[visibility == inf] = 0

# Initialize pheromone matrix
pheromone = 0.1 * np.ones((n, n))

# Initialize variables to store the best path and cost across all iterations
best_path = None
best_cost = float('inf')

for ite in range(iteration):
    # Initialize routes matrix for this iteration
    rute = np.ones((m, n), dtype=int)
    rute[:, 0] = 0  # All ants start at city 0
    
    for i in range(m):
        visited = {0}
        for j in range(1, n):
            cur_loc = rute[i, j-1]
            unvisited = [c for c in range(n) if c not in visited]
            if not unvisited:
                break
                
            probabilities = np.zeros(n)
            total = 0.0
            for city in unvisited:
                p_val = (pheromone[cur_loc, city] ** beta) * (visibility[cur_loc, city] ** alpha)
                probabilities[city] = p_val
                total += p_val
            
            if total > 0:
                probabilities /= total
            else:
                probabilities[unvisited] = 1.0 / len(unvisited)
            
            next_city = np.random.choice(range(n), p=probabilities)
            rute[i, j] = next_city
            visited.add(next_city)

    # Calculate distance costs
    dist_cost = np.zeros(m)
    for i in range(m):
        total_dist = 0
        for j in range(n-1):
            total_dist += d[rute[i, j], rute[i, j+1]]
        total_dist += d[rute[i, n-1], rute[i, 0]]
        dist_cost[i] = total_dist

    # Find best route in this iteration
    current_min_loc = np.argmin(dist_cost)
    current_min_cost = dist_cost[current_min_loc]
    current_best_route = rute[current_min_loc, :].copy()

    # Update overall best path and cost
    if current_min_cost < best_cost:
        best_cost = current_min_cost
        best_path = current_best_route

    # Evaporate pheromone
    pheromone *= (1 - e)

    # Update pheromone based on ants' routes
    for i in range(m):
        # Add pheromone for each edge in the route
        for j in range(n-1):
            city_from = rute[i, j]
            city_to = rute[i, j+1]
            pheromone[city_from, city_to] += 1.0 / dist_cost[i]
        # Add pheromone for return to start
        city_from = rute[i, n-1]
        city_to = rute[i, 0]
        pheromone[city_from, city_to] += 1.0 / dist_cost[i]

# Convert best_path to 1-indexed for output
best_path_1_indexed = best_path + 1

print('Best path (1-indexed):', best_path_1_indexed)
print('Cost of the best path:', int(best_cost))
