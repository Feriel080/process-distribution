import random
from helping_func import generer_instance, charge_processeurs, solution_initiale, voisin_move, voisin_swap

random.seed(42)

nP = 4
nT = 10

D = generer_instance(nP, nT)
S = solution_initiale(nP, nT)
voisinM = voisin_move(S, nP)
voisinS = voisin_swap(S)
makespanSI = charge_processeurs(S, D)
makespanVM = charge_processeurs(voisinM, D)
makespanVS = charge_processeurs(voisinS, D)

print(f"""Matrice D:\n{D}\n
Solution initiale:\n{S}
makespan: {makespanSI}\n
Voisin avec l'opération Move:\n{voisinM}
makespane: {makespanVM}
Voisin avec l'opération Swap:\n{voisinS}
makespan: {makespanVS}""")
