import json
import numpy as np
from helping_func import charge_processeurs, voisin_move
from tabu_search import TabuSearch

D = np.array([[6, 9, 4, 7, 8, 5, 10, 3],
              [8, 5, 7, 4, 6, 9, 6, 7],
              [5, 8, 6, 9, 3, 7, 8, 4],
              [9, 6, 5, 5, 7, 4, 7, 6]])
nP, nT = 4, 8

# use the same solutions of simulated annealing
initial_solutions = [run["initial_solution"] for run in json.load(open("instances/sa_results.json", "r"))["runs"]]
results = []

for r, solution in enumerate(initial_solutions):
    S = solution
    TS = TabuSearch(charge_processeurs, tabu_size=0, initial_solution=S, neighbor_opr=voisin_move)
    best_solution, best_cost, _ = TS.run(nP, D)
    
    results.append({
        "run": r + 1,
        "initial_solution": S,
        "best_solution": best_solution,
        "best_cost": float(best_cost),
    })
    
    with open("instances/ts_results.json", "w") as f:
        json.dump({"processors": nP,
        "tasks": nT,
        "runs": results,
    }, f, indent=2)
        
    print(f"""Solution {r + 1}:
{S}
Best solution:
{best_solution}
Cmax = {best_cost}
""")
