# Projets Finance


Ces projets utilisent `python3`

Attention : Dans le projet 2, vous devez rentrer votre clé API pour utiliser Mistral donc choisissez les actions à la main si vous n'en avez pas.
# Projet 1: Construction de l'indice S&P 500 avec un risque journalier contrôlé à 5%

L'objectif est d'ajuster dynamiquement l'exposition au S&P 500 en fonction de la volatilité afin de maintenir un risque constant de 5%. J'utilise pour cela les données de l'API `yfinance` de Yahoo Finance.

## Description du Projet

Les étapes importantes de mon algorithme sont:

1. Récupération des données historiques avec yfinance
2. Calcul du rendement à la main
3. Calcul de la volatilité sur une fenêtre à définir, par exemple 20 jours, à la main
4. Calcul du rendement nécessaire pour ne pas dépasser un risque cible

## Détails du Projet

J'ai préféré calculer à la main le rendement et la volatilité afin de me familiariser avec les détails techniques, par exemple le problème de calcul de la volatilité sur les 20 premiers jours (je prends une fenêtre de 20 jours), puisqu'elle est calculée grâce à l'écart-type des 20 derniers rendements.
J'ai utilisé la formule:
Rendement modifié = rendement * (volatilité cible / volatilité actuelle)
sachant que (volatilité cible / volatilité actuelle) corresponds à l'effet de levier

## Présentation des résultats
Par rapport au [modèle de base](https://www.spglobal.com/spdji/en/indices/multi-asset/sp-500-daily-risk-control-5-index/#overview), on retrouve presque le même graphique, avec seulement un décalage d'environ 3% sur un an.



![image](https://github.com/user-attachments/assets/ab26c652-308f-4ba0-8276-50e3b983942c)
*Modèle utilisé comme référence*

![SP500_le_mien](https://github.com/user-attachments/assets/96cc1b53-a108-4230-ae73-cc5de319ec41)
*Mon modèle*


---


# Projet 2: Optimisation de Portefeuille avec le modèle de Markowitz et l'API Mistral

Ce projet met en œuvre l'optimisation de portefeuille selon le modèle de **Markowitz**. L'objectif est de construire un portefeuille efficient en maximisant le rendement tout en minimisant le risque, à l'aide de données financières provenant de Yahoo Finance. Plus précisement, je cherche à minimiser la fonction `risque/rendement`, ce qui est un choix personnel pour ne pas avoir de positions trop risquées, par rapport à `risque/(rendement**2)` par exemple. 


## Description du Projet

L'objectif est de trouver les pondérations optimales des actions dans un portefeuille. Le principe de mon code est le suivant :

1. Choix des actions du portefeuille par l'IA Mistral à partir d'un nombre d'actions et une période donnée
2. Calcul des rendements moyens de chaque action sur la période
3. Calcul de la covariance de chaque paire d'action sur la période
4. Calcul du risque et du rendement attendu du portefeuille en fonction des pondérations
5. Minimisation de la fonction mentionnée en introduction
6. Suppression des actions représentant une trop faible part du portefeuille ( <0.1% )
7. Génération d'un nombre donné de portefeuilles ayant les mêmes actions avec des proportions définit par une loi de probabilité uniforme sur [0;1] et dont la somme vaut 1
8. Affichage de tous les portefeuilles, y compris celui optimal, afin de comparer



## Présentation des résultats
On obtient avec 4 actions:

![p2_5a_puiss08](https://github.com/user-attachments/assets/23492b3a-4ac7-4681-8a03-375796ebb58b)

*On remarquera que les performances obtenues sur ce choix d'actions ne sont pas excellentes*

**En modifiant la fonction à minimiser, le portefeuille optimal se déplace sur la frontière d'efficience.**



![p2_5action_puissance01](https://github.com/user-attachments/assets/d3daf5f4-415f-40ca-a271-bc326b1c00ed)
*On a ici `risque/(rendement**0.1)`, ce qui privilégie les positions moins risquées*



**Avec un portefeuille plus varié, on obtient 15% de rendement pour 6,5% de risque, bien meilleur résultat.**



![Figure_1_projet2](https://github.com/user-attachments/assets/cc11c918-98fd-4b63-8c93-0d36efb651c8)

*Avec 15 actions, la frontière d'efficience est moins visible car le nombre de combinaisons possibles augmente mais le nombre de portefeuilles aléatoires est limité à cause du temps de calcul.*

**Sur les 15 actions, l'algorithme enlève les actions suivantes :**

`['TTE.PA', 'MSFT', 'NKE', 'V', 'UNH', 'JNJ', 'CVX', 'DIS']`

Il sélectionne celles restantes avec les proportions suivantes:


- AAPL, Poids: 0.4%
- GOOGL, Poids: 2.9%
- AMZN, Poids: 0.5%
- XOM, Poids: 12.2%
- PG, Poids: 15.8%
- KO, Poids: 48.4%
- NFLX, Poids: 19.8%


---


