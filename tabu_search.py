import math
import os
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme('paper')


class TabuSearch:
    """Tabu Search with the move operator (process distribution).
    First call run(nP, D) where:
        nP : number of processors.
        D : duration matrix.

    To plot the convergence, call convergence().
    """

    def __init__(self, obj_func, tabu_size, initial_solution, neighbor_opr, itermax=100):
        self.obj_func = obj_func
        self.tabu_size = tabu_size              # k
        self.initial_solution = initial_solution
        self.itermax = itermax
        self.neighbor_opr = neighbor_opr
        # oldest move leaves when full
        self.tabu_list = deque(maxlen=tabu_size)
        self.best_solution = None
        self.best_cost = None
        self.history = []                       # best cost at each iteration

    def neighbors(self, current_sol, nP, D):
        n_samples = len(current_sol) * (nP - 1)
        best_task, best_move_cost, best_sol = None, math.inf, None
        seen = set()
        
        for _ in range(n_samples):
            Sv = self.neighbor_opr(current_sol, nP)
            
            task = next(i for i in range(len(Sv)) if Sv[i] != current_sol[i])
            move = (task, Sv[task])
            if move in seen:                      # already evaluated
                continue
            seen.add(move)

            cost = self.obj_func(Sv, D)
            if move in self.tabu_list and cost >= self.best_cost:
                continue                   
            if cost < best_move_cost:
                best_task, best_move_cost, best_sol = task, cost, Sv

        return best_task, best_move_cost, best_sol

    def run(self, nP, D):
        if nP <= 0:
            raise ValueError(
                "I've never seen a negative number of processors before.")

        current_sol = self.initial_solution.copy()
        self.best_solution = current_sol.copy()
        self.best_cost = self.obj_func(current_sol, D)
        self.tabu_list.clear()
        self.history = []

        for _ in range(self.itermax):
            task, cost, Sv = self.neighbors(current_sol, nP, D)
            if Sv is None:                    # every neighbor is tabu
                break
            old_proc = current_sol[task]
            current_sol = Sv
            self.tabu_list.append((task, old_proc))

            if cost < self.best_cost:
                self.best_solution = current_sol.copy()
                self.best_cost = cost
            self.history.append(self.best_cost)

        return self.best_solution, self.best_cost, self.history

    def convergence(self):
        if not self.history:
            raise ValueError("History is empty, call run() first.")
        plt.figure(figsize=(7, 4))
        plt.plot(range(1, len(self.history) + 1), self.history)
        plt.xlabel("Iteration")
        plt.ylabel("Best cost (makespan)")
        plt.title("Tabu search convergence")
        plt.grid(True)
        os.makedirs("plots", exist_ok=True)
        plt.savefig("plots/convergence_tabu.png", dpi=600)
        plt.close()
