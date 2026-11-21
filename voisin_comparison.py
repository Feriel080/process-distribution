import time
import numpy as np
import pandas as pd
from helping_func import (generer_instance, charge_processeurs, solution_initiale,
                          voisin_move, voisin_swap)
from simulated_annealing import SimulatedAnnealing

nP, nT = 5, 50
runs = 10

rows = []
for name, operator in [("move", voisin_move), ("swap", voisin_swap)]:
    costs, times = [], []
    for seed in range(1, runs + 1):
        D = generer_instance(nP, nT)
        S = solution_initiale(nP, nT)

        SA = SimulatedAnnealing(charge_processeurs, operator, initial_sol=S,
                                T_init=100, T_min=1e-3, L=nT, n_stab=50, alpha=0.9)
        start = time.perf_counter()
        SA.run(nP, D)
        times.append(time.perf_counter() - start)
        costs.append(SA.best_cost)

    rows.append({"operateur": name, "meilleur": min(costs),
                 "moyen": np.mean(costs), "ecart-type": np.std(costs),
                 "temps (s)": np.mean(times)})

results = pd.DataFrame(rows).round(4)
results.to_csv("instances/operateur_comparison.csv")
