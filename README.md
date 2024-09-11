# Projets Finance


Ces projets utilisent `python3`
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

![Graphe de mon code ](path/to/frontiere_efficiente_image.png)  
*Exemple de frontière efficiente : chaque point représente une combinaison rendement/risque, et le point rouge correspond au portefeuille optimal.*

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
6. Génération d'un nombre donné de portefeuilles ayant les mêmes actions avec des proportions définit par une loi de probabilité uniforme sur [0;1] et dont la somme vaut 1
7. Affichage de tous les portefeuilles, y compris celui optimal, afin de comparer



## Présentation des résultats

1. **Téléchargement des données financières** : Récupération des données de prix historiques des actions via l'API Yahoo Finance avec `yfinance`.
2. **Calcul du risque et du rendement** : Le risque est basé sur la volatilité, et le rendement attendu est calculé à partir des moyennes historiques des rendements.
3. **Optimisation des pondérations** : Utilisation de la méthode SLSQP pour minimiser une fonction de performance basée sur le ratio rendement/risque.
4. **Frontière efficiente** : Visualisation de toutes les combinaisons possibles de portefeuilles et identification du portefeuille optimal.

![Exemple de Frontière Efficiente](path/to/frontiere_efficiente_image.png)  
*Exemple de frontière efficiente : chaque point représente une combinaison rendement/risque, et le point rouge correspond au portefeuille optimal.*

---

## Frontière Efficiente

La frontière efficiente montre les portefeuilles avec le meilleur compromis entre risque et rendement. Dans notre projet, nous générons plusieurs portefeuilles aléatoires et identifions celui qui offre le meilleur ratio rendement/risque.

