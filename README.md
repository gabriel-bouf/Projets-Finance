# Projets Finance 


Ces projets utilisent `python`

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

Ce projet met en œuvre l'optimisation de portefeuille selon le modèle de **Markowitz**. L'objectif est de construire un portefeuille qui maximise le rendement tout en minimisant le risque, à l'aide de données financières provenant de Yahoo Finance. Plus précisément, on cherche à maximiser le ratio de Sharpe `(rendement - taux sans risque)/risque`, ce qui est un choix personnel pour ne pas avoir de positions trop risquées, par rapport à `(rendement - taux sans risque)**2/risque` par exemple. 

Attention : Vous devez utiliser une clé API pour utiliser l'IA Mistral. Si vous n'avez pas de clé API, des actions sont choisies aléatoirement parmi une liste modifiable.


## Description du Projet

On cherche les pondérations optimales des actions dans le portefeuille. Le principe du code est le suivant :

1. Choix des actions du portefeuille par l'IA Mistral à partir d'un nombre d'actions et une période donnée
2. Calcul des rendements moyens, de la covariance
3. Calcul du risque et du rendement attendu du portefeuille en fonction des pondérations
4. Maximisation du ratio de Sharpe
5. Suppression des actions représentant une trop faible part du portefeuille ( <0.1% ) et générations de portefeuilles aléatoires des mêmes actions pour comparer
6. Affichage de tous les portefeuilles et backtest pour analyser la pertinence du code

## Présentation des résultats

On obtient avec 3 actions:

![p2_5a_puiss08](https://github.com/user-attachments/assets/23492b3a-4ac7-4681-8a03-375796ebb58b)
*On remarquera que les performances obtenues sur ce choix d'actions ne sont pas excellentes*


**En modifiant la fonction à maximiser, le portefeuille optimal se déplace sur la frontière d'efficience, tout va bien**


![p2_5action_puissance01](https://github.com/user-attachments/assets/d3daf5f4-415f-40ca-a271-bc326b1c00ed)
*On a remplacé le ratio de Sharpe par `(rendement-taux sans risque)**0.1/risque`, ce qui privilégie les positions moins risquées*

**Avec un portefeuille plus varié, on obtient 15% de rendement pour 6,5% de risque, bien meilleur résultat.**



![Figure_1_projet2](https://github.com/user-attachments/assets/cc11c918-98fd-4b63-8c93-0d36efb651c8)

## Mistral & backtest

Au lieu de sélectionner soit même les tickers, on demande à l'API de MistralAI, via un prompting, sa sélection d'actions qui lui semblent pertinentes. En souhaitant 5 actions on obtient par exemple :

![front3](https://github.com/user-attachments/assets/5f6bda48-b238-4073-ba73-29a74f4878cb)

```
Mistral proposition :
 ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']

Optimal set :
 [('AAPL', 0.303), ('GOOGL', 0.139), ('NVDA', 0.557)]

 Deleted tickers :
 ['MSFT', 'AMZN']
 
This portfolio is supposed to have a daily return of 0.44% and a daily risk of 2.1867% based on 2024-01-01 to 2024-08-01

Return of the portfolio on the tested period :
 17.295 %
Expected return of the portfolio over the period : 45.233 %
```
*The portfolio curve is in black*

![backt3](https://github.com/user-attachments/assets/07167c7a-105a-4e9d-812c-fdfd21c1ab86)

On peut modifier le prompting et demander aussi la présence de cryptomonnaies, ainsi qu'une centaine d'actions, ce qui permetterait de trouver une combinaison optimale en sachant qu'on arrondie les poids à 3 chiffres significatifs, ce qui supprime les valeurs proches de 0. Malheureusement, Mistral invente un trop grand nombre d'actions dans ce cas et seulement une vingtaine est retenue en général.

Après modification du prompt, on obtient pour 15 actions:
```
Mistral proposition :
 ['MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'V', 'BABA', 'BNP.PA', 'NKE', 'UNH', 'JNJ', 'PG', 'KO', 'VZ', 'BTC-USD']

Optimal set :
 [('MSFT', 0.003), ('AMZN', 0.014), ('NVDA', 0.035), ('V', 0.038), ('BABA', 0.579), ('UNH', 0.157), ('JNJ', 0.004), ('KO', 0.069), ('BTC-USD', 0.102)]

 Deleted tickers :
 ['GOOGL', 'TSLA', 'BNP.PA', 'NKE', 'PG', 'VZ']
This portfolio is supposed to have a daily return of 0.1922% and a daily risk of 0.6308% based on 2024-01-01 to 2024-08-01

Return of the portfolio on the tested period : 
 4.834 %
Expected return of the portfolio over the period : 26.39 %
```
![back4](https://github.com/user-attachments/assets/16130d77-e207-4040-9588-70c072856db7)

# Améliorations en cours

**Mise en place de contraintes supplémentaire**

Pour éviter d'avoir 80% du portefeuille dans une seule action qui a eu des perfomances sur la période historique analysée qui soient trompeuses.

**Meilleure génération des portefeuilles aléatoire :**

Les portefeuilles sont générés avec des proportions aléatoires qui suivent une loi de probabilité uniforme, grâce à la fonction np.random.random. Lorsqu'on se base sur un grand nombre d'actions, ces portefeuilles aléatoires ne représentent pas les meilleurs portefeuilles puisque les meilleures solutions nécessitent d'exclure un grand nombre d'actions (43 actions à supprimer pour la solution optimale du dernier exemple). Il faudrait donc remplacer `np.random.random` par `np.random.normal` pour avoir une loi gaussienne, qui peut favoriser les valeurs proches de 0 et ainsi filtrer les actions. Malheureusement le coût de calcul est trop important pour mon ordinateur.





---


