import os
import pickle
import time
import numpy as np
import pandas as pd
from helping_func import generer_instance, charge_processeurs, solution_initiale, voisin_move
from simulated_annealing import SimulatedAnnealing
from tabu_search import TabuSearch


class Counter:
    def __init__(self, func):
        self.func = func
        self.n = 0

    def __call__(self, S, D):
        self.n += 1
        return self.func(S, D)


pairs = [(3, 10), (5, 50), (10, 200)]
runs = 10
rows = []
saved = []

for (nP, nT) in pairs:
    sa_costs, sa_times, ts_costs, ts_times = [], [], [], []
    sa_evals, ts_evals = [], []

    for run in range(1, runs + 1):
        D = generer_instance(nP, nT)
        S = solution_initiale(nP, nT)
        saved.append((D, S.copy()))

        # Simulated annealing
        f_sa = Counter(charge_processeurs)
        SA = SimulatedAnnealing(f_sa, voisin_move, initial_sol=S, T_init=100,
                                T_min=1e-3, L=nT, n_stab=50, alpha=0.9)
        start = time.perf_counter()
        SA.run(nP, D)
        sa_times.append(time.perf_counter() - start)
        sa_costs.append(SA.best_cost)
        sa_evals.append(f_sa.n)

        # Tabu search with a comparable budget:
        # one iteration costs at most nT * (nP - 1) evaluations
        itermax = max(1, f_sa.n // (nT * (nP - 1)))
        f_ts = Counter(charge_processeurs)
        TS = TabuSearch(f_ts, tabu_size=5, initial_solution=S,
                        neighbor_opr=voisin_move, itermax=itermax)
        start = time.perf_counter()
        _, ts_best, _ = TS.run(nP, D)
        ts_times.append(time.perf_counter() - start)
        ts_costs.append(ts_best)
        ts_evals.append(f_ts.n)
        
    with open(f"instances/instances_{nP}_{nT}.pkl", "wb") as f:
        pickle.dump(saved, f)
        
    rows.append({
        "(nP, nT)": (nP, nT),
        "SA meilleur": min(sa_costs),
        "SA moyen": np.mean(sa_costs),
        "Temps SA (s)": np.mean(sa_times),
        "RT meilleur": min(ts_costs),
        "RT moyen": np.mean(ts_costs),
        "Temps RT (s)": np.mean(ts_times),
        "Evals SA": np.mean(sa_evals),
        "Evals RT": np.mean(ts_evals),
    })

df = pd.DataFrame(rows).round(2)
df.to_csv("instances/comparaison.csv")
