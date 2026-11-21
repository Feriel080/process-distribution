# Répartition de tâches sur processeurs

Ce projet étudie l'affectation de tâches à des processeurs indépendants afin de
minimiser la durée totale d'exécution.

## Modèle

- `nP` : nombre de processeurs.
- `nT` : nombre de tâches.
- `D[p][t]` : durée d'exécution de la tâche `t` sur le processeur `p`.
- `S[t]` : indice du processeur affecté à la tâche `t` (`0` à `nP - 1`).

Chaque tâche est affectée à un seul processeur. Un processeur peut ne recevoir
aucune tâche.

La charge du processeur `p` est la somme des durées des tâches qui lui sont
affectées :

```text
C[p] = sum(D[p][t] for t where S[t] == p)
```

La fonction objectif minimise le makespan, c'est-à-dire la charge maximale :

```text
Cmax = max(C[p] for p in range(nP))
```

Le nombre d'affectations possibles est `nP ** nT`.

## Algorithmes et fichiers

- `helping_func.py` contient la génération d'instances et de solutions, le
  calcul du makespan, ainsi que les opérateurs de voisinage :
  - **move** : réaffecter une tâche à un autre processeur ;
  - **swap** : échanger les processeurs de deux tâches.
- `simulated_annealing.py` implémente le recuit simulé.
- `tabu_search.py` implémente la recherche tabou.
- `testing_sa.py` et `testing_ts.py` contiennent des scripts d'expérimentation.

Le recuit simulé et la recherche tabou sont des métaheuristiques : ils
explorent l'espace des affectations, mais ne garantissent pas de trouver
l'optimum global.

## Installation et exécution

Installez les dépendances depuis la racine du projet :

```bash
python -m pip install -r requirements.txt
```

Lancez les scripts d'expérimentation depuis cette même racine :

```bash
python testing_sa.py
python testing_ts.py
```
