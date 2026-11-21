import json
import numpy as np
from helping_func import charge_processeurs, solution_initiale, voisin_move
from simulated_annealing import SimulatedAnnealing

runs = 10
D = np.array([[6, 9, 4, 7, 8, 5, 10, 3],
              [8, 5, 7, 4, 6, 9, 6, 7],
              [5, 8, 6, 9, 3, 7, 8, 4],
              [9, 6, 5, 5, 7, 4, 7, 6]])
nP, nT = 4, 8
results = []
# S = [2, 3, 0, 3, 2, 3, 1, 2]

for r in range(runs):
    S = solution_initiale(nP, nT)
    SA = SimulatedAnnealing(charge_processeurs, voisin_move, initial_sol=S,
                            T_min=1e-3, alpha=0.99, L=nT, n_stab=20, r=0.9)
    SA.run(nP, D)
    
    results.append({
        "run": r + 1,
        "initial_solution": S,
        "best_solution": SA.best_solution,
        "best_cost": float(SA.best_cost),
        "moves": SA.n_movement,
    })
    
    with open("instances/sa_results_solInitFixe.json", "w") as f:
        json.dump({"processors": nP,
        "tasks": nT,
        "execution_times": D.tolist(),
        "runs": results,
    }, f, indent=2)
        
    print(f"""Solution {r + 1}:
{S}
Best solution:
{SA.best_solution}
Cmax = {SA.best_cost}
movement: {SA.n_movement}
""")
