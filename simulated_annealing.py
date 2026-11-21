import math
import random

class SimulatedAnnealing:
    def __init__(self, obj_func, neighbor_opr, T_init = 100.0, T_min = 0.0, r = None,
                 alpha = 0.4, initial_sol = None, L = 5,
                 n_stab = 5):
        self.temperature = T_init
        self.T_min = T_min
        self.r = r if r is not None else random.randint(0, 1)
        if alpha < 0 or alpha > 1:
            raise ValueError("alpha must be in ]0, 1[")
        
        self.alpha = alpha 
        self.initial_sol = initial_sol
        self.L = L 
        self.obj_func = obj_func
        self.Nstab = n_stab
        self.best_solution = None
        self.best_cost = 0
        self.n_movement = 0
        self.neighbor_opr = neighbor_opr

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
        
        iteration = 0
        stable = 0
        while self.temperature > self.T_min and stable < self.Nstab:
            improved = False
           
            Sv = self.neighbor_opr(current_sol, nP)
            if Sv == current_sol:
                break # the best solution is the current solution
            
            Sv_cost = self.obj_func(Sv, D)
            De = Sv_cost - current_cost
            
            if De <= 0 or self.r < self.probability(De):
                current_solution, current_cost = Sv, Sv_cost
                self.n_movement += 1
                
                if self.best_cost > current_cost: # We need to minimize the makespan
                    self.best_solution, self.best_cost = current_solution, current_cost
                    improved = True
            
            iteration += 1
            if (iteration + 1) % self.L == 0:
                self.temperature *= self.alpha
                iteration = 0
                
            stable = 0 if improved else stable + 1
        print(f"{"Solution stable."if stable < self.Nstab else "The temperature became so small."}")