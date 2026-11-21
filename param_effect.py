import random
import time
import json
import numpy as np
import pandas as pd
from helping_func import generer_instance, charge_processeurs, solution_initiale, voisin_move
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch

random.seed(42)

nP, nT = 5, 50
runs = 10
D = generer_instance(nP, nT)
S = solution_initiale(nP, nT)

json.dump({"D": D.tolist(), "S": S}, open(
    "instances/parameters_5-50.json", "w"), indent=2)

# Simulated annealing: alpha x T0
rows = []
for alpha in [0.90, 0.95, 0.99]:
    for T0 in [1, 10, 100, 1000]:
        SA = SimulatedAnnealing(charge_processeurs, voisin_move, initial_sol=S,
                                T_init=T0, T_min=1e-3, L=nT, n_stab=20, alpha=alpha)
        start = time.perf_counter()
        SA.run(nP, D)
        rows.append({"alpha": alpha, "T0": T0, "makespan": SA.best_cost,
                    "temps (s)": time.perf_counter() - start})

print("\nSimulated annealing")
print(pd.DataFrame(rows).round(2).to_string(index=False))

# Tabu search: k
rows = []
for k in [3, 7, 15]:
    TS = TabuSearch(charge_processeurs, tabu_size=k, initial_solution=S,
                    neighbor_opr=voisin_move, itermax=100)
    start = time.perf_counter()
    _, best, _ = TS.run(nP, D)
    rows.append({"k": k, "makespan": best,
                "temps (s)": time.perf_counter() - start})

print("\nTabu search")
print(pd.DataFrame(rows).round(2).to_string(index=False))
