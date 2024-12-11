# Projets Finance 


Ces projets utilisent `python3`

Attention : Dans le projet 2, vous devez rentrer votre clé API pour utiliser l'IA Mistral. Si vous n'avez pas de clé API, des actions sont choisies aléatoirement parmi une liste modifiable.
# Projet 1: Construction de l'indice S&P 500 avec un risque journalier contrôlé à 5%

L'objectif est d'ajuster dynamiquement l'exposition d'un portefeuille représentant le S&P 500 en fonction de sa volatilité afin de maintenir un risque maximum de 5%. J'utilise pour cela les données de l'API `yfinance` de Yahoo Finance.

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

Ce projet met en œuvre l'optimisation de portefeuille selon le modèle de **Markowitz**. L'objectif est de construire un portefeuille efficient en maximisant le rendement tout en minimisant le risque, à l'aide de données financières provenant de Yahoo Finance. Plus précisément, je cherche à maximiser le ratio de Sharpe `(rendement - taux sans risque)/risque`, ce qui est un choix personnel pour ne pas avoir de positions trop risquées, par rapport à `(rendement - taux sans risque)**2/risque` par exemple. 


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


**On obtient d'encore meilleurs résultats avec 55 actions de secteurs variés : 40% de rendement pour 8,5% de risque**

![55_40_8_100k](https://github.com/user-attachments/assets/c2d744f2-ee99-4a92-aba5-d08e944eecdd)

*Malgré 100 000 portefeuilles générés aléatoirement, il est impossible de visualiser la frontière efficiente. Par ailleurs le rendement semble très élevé, c'est pourquoi un programme de backtesting est en développement.*



Proportions correspondantes :

- GOOGL, Poids: 0.6%
- ORCL, Poids: 3.6%
- PG, Poids: 5.8%
- KO, Poids: 8.3%
- WMT, Poids: 17.0%
- COST, Poids: 5.5%
- SO, Poids: 9.3%
- XOM, Poids: 4.5%
- GE, Poids: 11.8%
- LMT, Poids: 17.7%
- NFLX, Poids: 8.7%
- T, Poids: 7.4%


Une majeure partie des entreprises n'ont pas été retenues dans cet exemple :

`['AAPL', 'MSFT', 'IBM', 'JNJ', 'PFE', 'MRK', 'UNH', 'ABT', 'JPM', 'BAC', 'GS', 'C', 'MS', 'TSLA', 'AMZN', 'HD', 'NKE', 'MCD', 'PEP', 'NEE', 'DUK', 'AEP', 'EXC', 'CVX', 'COP', 'BP', 'SLB', 'BHP', 'RIO', 'DD', 'VALE', 'FCX', 'SPG', 'PLD', 'AMT', 'PSA', 'CBRE', 'BA', 'CAT', 'DE', 'DIS', 'VZ', 'CHTR']`

## Améliorations possible

**Meilleure génération des portefeuilles aléatoire :**

Les portefeuilles sont générés avec des proportions aléatoires qui suivent une loi de probabilité uniforme, grâce à la fonction np.random.random. Lorsqu'on se base sur un grand nombre d'actions, ces portefeuilles aléatoires ne représentent pas les meilleurs portefeuilles puisque les meilleures solutions nécessitent d'exclure un grand nombre d'actions (43 actions à supprimer pour la solution optimale du dernier exemple). Il faudrait donc remplacer `np.random.random` par `np.random.normal` pour avoir une loi gaussienne, qui peut favoriser les valeurs proches de 0 et ainsi filtrer les actions. Malheureusement le coût de calcul est trop important pour mon ordinateur.

**Backtesting**



---


