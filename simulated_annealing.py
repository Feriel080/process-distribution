import math
import random
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme('paper')

class SimulatedAnnealing:
    """Simulated Annealing algorithm,
    applied only for this case (process distribution).
    First call run(nP, D) where:
        nP : number of processors.
        D : Duration matrix (how much time each processor take to finish a specific task).
    
    If you want to plot the convergence call convergence()
    """
    def __init__(self, obj_func, neighbor_opr, T_init = 100.0, T_min = 0.0, r = None,
                 alpha = 0.4, initial_sol = None, L = 5,
                 n_stab = 5):
        self.temperature = T_init
        self.T_min = T_min
        self.r = r if r is not None else random.random()
        self.alpha = alpha 
        self.initial_sol = initial_sol
        self.L = L 
        self.obj_func = obj_func
        self.Nstab = n_stab
        self.best_solution = None
        self.best_cost = 0
        self.n_movement = 0
        self.neighbor_opr = neighbor_opr
        self.history = []

    def probability(self, delta):
        if self.temperature <= 0:
            return 0.0
        return math.exp(-delta / self.temperature)

    def run(self, nP, D):
        if self.initial_sol is None:
            raise ValueError("Go provide initial_sol first.")
        if nP <= 0:
            raise ValueError("I've never seen a negative number of processors before.")
        
        current_sol = self.initial_sol.copy()
        current_cost = self.obj_func(current_sol, D)
        self.best_solution = current_sol.copy()
        self.best_cost = current_cost
        self.history = []
        
        stable = 0
        while self.temperature > self.T_min and stable < self.Nstab:
            best_before = self.best_cost
            
            for _ in range(self.L):
                Sv = self.neighbor_opr(current_sol, nP)
                Sv_cost = self.obj_func(Sv, D)
                De = Sv_cost - current_cost
                
                if De <= 0 or self.r < self.probability(De):
                    current_sol, current_cost = Sv, Sv_cost
                    self.n_movement += 1
                    
                    if self.best_cost > current_cost: # We need to minimize the makespan
                        self.best_solution, self.best_cost = current_sol.copy(), current_cost
                
                self.temperature *= self.alpha
                self.history.append(self.best_cost)
                stable = 0 if self.best_cost < best_before else stable + 1
                
        print(f"{"Solution stable."if stable >= self.Nstab else "The temperature became so small."}")
    
    def convergence(self):
        if not self.history:
            raise ValueError("You didn't even find the optimum solution, what are you expecting to plot?")
        paliers = range(1, len(self.history) + 1)
        plt.figure(figsize=(7, 4))
        plt.plot(paliers, self.history, marker="o")
        plt.xlabel("Palier")
        plt.ylabel("Best cost (makespan)")
        plt.title("Simulated annealing convergence")
        plt.tight_layout()
        plt.savefig("plots/convergence_sa.png", dpi=600)
        plt.close()