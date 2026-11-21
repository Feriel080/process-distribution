import numpy as np
import random
 
def generer_instance(nP, nT):
    """Génération d'une matrice de temps d'exécution entiers positives aléatoires entre 1 et 100.

    Args:
        nP (int): Nombre de processeurs.
        nT (int): Nombre de tâches.

    Returns:
        D: Matrice de temps d'éxecution nP x nT
    """
    D = np.zeros((nP, nT))
    D = [[random.randint(1, 100) for _ in range(nT)] for _ in range(nP)]
    
    return np.array(D)

def solution_initiale(nP, nT):
    """Affectation aléatoire des nT tâches aux nP processeurs.

    Args:
        nP (int): Number of processors
        nT (int): Number of tasks
    
    Returns:
        S: Solution initiale, où S[j] indique l'indice du processeur.
        `exemple:` S = [1, 2, 3, 1] -
            * La tâche 0 est exécutée sur le processeur 1
            * La tâche 1 est exécutée sur le processeur 2
            * La tâche 2 est exécutée sur le processeur 3
            * La tâche 3 est exécutée sur le processeur 1
    """
    return [random.randrange(nP) for _ in range(nT)]

def realizable_solution(nT, nP, S):
    """Vérifier si la solution respecte les contraintes ou non.
    
    Les contrainte:
        * Chaque tâche est exécutée sur un seul processeur. (toujours vérifié, car contrôlé par les indices.)
        * Chaque processeur peut exécuter une ou plusieurs tâches.
        * Toutes les tâches et tous les processeurs sont présents.

    Args:
        nP (int): Nombre de processeurs.
        nT (int): Nombre de tâches.
        S (List[int]): Affectation des tâches. 
    
    Returns:
        Boolean: `True` si la solution est réalizable, `False` si non.
    """
    if nT != len(S):
        return False
    
    if nP != max(S) + 1:
        return False
        
    return True

def charge_processeurs(S, D):
    """Calcule la charge maximal (durée d'ordonnancement).
    C_max = max(C_1, ..., C_nP)
    C_i = Σ d_ij
    
    Args:
        S (List[int]): Ordonnancement des tâches.
        D (np.array): Matrice de temps d'exécution.

    Returns:
        makespan: La charge maximal.
    """
    nP = max(S)
    C = []
    
    for p in range(nP + 1):
        taches = [i for i, processeur in enumerate(S) if processeur == p]
        Ci = np.sum(D[p, taches])
        C.append(Ci)
        
    makespan = max(C)
    return makespan