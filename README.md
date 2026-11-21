# process-distribution

3 processeurs.

execution des programmes.

optimization des taches selon les processus.

ordonnancement multi-processeur.

une machine acev plusieurs processeur.  de p1 au pN.

et plusieurs taches.

chaque processeur est independant d'autre processeur.

probleme d'ordonnoncement.: ex: p1 = t1, p2 = t3, p3 = t2

solution: vecteur d'affectation.

Ti,j: temp de processeur i pour faire la tache j.

fonction objectif: minimiser le temp d'execution. -> avoir le min calendrier des taches.

contrainte: la tache doit être executer dans un seul processeur.

taille d'espace de rechrche:

n: nombre de taches, m: nombre de processeurs. Alors; m ^ n affectation possible.

variable de decision: matrices tel que : les lignes sont les processeurs, les colonnes sont les taches, et la valeur et binaire 0 si processeur n'execute pas la tache, 1 sinon.

rechrche tabu ne garanti pas de trouver le minimum global.

recuit simulé garanti en cas de choisir les bonnes parametre.



# 2eme presentaiton

peut etre un vecteur: taille = nombre de taches. , les valeurs sont des entiers tq, l'entier represente le nombre de processeur.


# Dans la rechrche Tabou

swap:
