import numpy as np

# modified distance matrix so best tour = 40
d = np.array([
    [0, 10, 10, 10, 10],
    [10, 0, 10, 10, 10],
    [10, 10, 0, 10, 10],
    [10, 10, 10, 0, 10],
    [10, 10, 10, 10, 0]
], dtype=float)

# parameters
iteration = 100
n_ants = 5
n_citys = 5
e = 0.5    # evaporation rate
alpha = 1  # pheromone factor
beta = 2   # heuristic factor

# visibility = 1 / distance (avoid div by zero)
visibility = np.zeros_like(d, dtype=float)
with np.errstate(divide="ignore"):
    visibility[d > 0] = 1.0 / d[d > 0]

# pheromone initialization
pheromone = 0.1 * np.ones((n_citys, n_citys))
np.fill_diagonal(pheromone, 0.0)

# best solution tracker
global_best_cost = np.inf
global_best_route = None

for ite in range(iteration):
    # each ant constructs a route
    all_routes = []
    all_costs = []

    for ant in range(n_ants):
        visited = [0]  # start from city 0
        current = 0

        for step in range(n_citys - 1):
            candidates = [c for c in range(n_citys) if c not in visited]

            tau = pheromone[current, candidates] ** alpha
            eta = visibility[current, candidates] ** beta
            desirability = tau * eta

            total = desirability.sum()
            if total == 0:
                probs = np.ones(len(candidates)) / len(candidates)
            else:
                probs = desirability / total

            next_city = np.random.choice(candidates, p=probs)
            visited.append(next_city)
            current = next_city

        # complete cycle
        visited.append(0)
        all_routes.append(visited)

        # calculate route cost
        cost = sum(d[visited[i], visited[i+1]] for i in range(n_citys))
        all_costs.append(cost)

    all_routes = np.array(all_routes)
    all_costs = np.array(all_costs)

    # find best ant this iteration
    best_idx = np.argmin(all_costs)
    best_cost = all_costs[best_idx]
    best_route = all_routes[best_idx]

    # update global best
    if best_cost < global_best_cost:
        global_best_cost = best_cost
        global_best_route = best_route.copy()

    # pheromone evaporation
    pheromone = (1 - e) * pheromone

    # pheromone deposit (iteration-best ant)
    tour_length = best_cost
    if tour_length > 0:
        deposit = 1.0 / tour_length
        for j in range(n_citys):
            a = best_route[j]
            b = best_route[j + 1]
            pheromone[a, b] += deposit
            pheromone[b, a] += deposit

    np.fill_diagonal(pheromone, 0.0)

# results
print("Best path found (1-based):", (global_best_route + 1).tolist())
print("Cost of the best path:", int(global_best_cost))
