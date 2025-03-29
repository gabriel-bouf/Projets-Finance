# Projets Finance 

Ces projets utilisent `Python`.

---
## Projet 3 : Skew of volatility

The idea is to use the historical time series of the excess return index assuming interest rates are equal to fed fund to imply what 
implied volatility would on average over the period made the P&L of a delta hedged call option equal to zero.

### Delta Hedging

The first step in this project is to simulate delta hedging. I used the `yfinance` library to retrieve Apple stock prices from January 1, 2024, to August 1, 2024, to simulate a delta hedging strategy. By plotting the P&L of the hedging strategy as a function of the strike price and the volatility used in the Black-Scholes model, it is interesting to observe that the P&L cannot be positive if the strike price is too low (deep in the money). In the following example, the initial spot price was $184, and the spot price at maturity was $221. We can see that below K=150, the P&L remains negative, meaning the Break-Even Volatility does not exist.

The simulation was run with the following parameters:
- **Commission rate:** 0.03%
- **Bid-ask spread:** 0.02%
- **Risk-free rate:** 4.3% (Fed Funds rate assumption)
- **Borrowing interest rate:** 4.3%
- **Delta hedging frequency:** Daily

![skeww 3d k150](https://github.com/user-attachments/assets/4208010f-38e7-4b74-9812-c0b6880470c9)

After finding the break-even volatility based on the P&L simulation, I have obtained the following BEV surface :
![bev4](https://github.com/user-attachments/assets/0f867512-6fd6-439f-8e83-7829a44f0235)


Based on the provided BEV (Break-Even Volatility) surface, we can observe the following:

- Low strikes lead to higher BEV.
- The BEV is near 0 for 450-480 days maturity and for deep OTM options.



---

## Projet 2 : Optimisation de Portefeuille avec le modèle de Markowitz et l'API Mistral

Ce projet implémente l'optimisation de portefeuille selon le modèle de **Markowitz**. L'objectif est de construire un portefeuille maximisant le rendement tout en minimisant le risque, en s'appuyant sur des données financières issues de Yahoo Finance. Plus précisément, nous cherchons à maximiser le ratio de Sharpe `(rendement - taux sans risque)/risque`, un choix pertinent pour éviter des positions excessivement risquées, contrairement à `(rendement - taux sans risque)**2/risque` par exemple. 

> **Remarque** : Une clé API est nécessaire pour utiliser l'IA Mistral. Si vous n'avez pas de clé, des actions sont choisies aléatoirement à partir d'une liste modifiable.

### Description du projet

Voici les étapes principales du projet :  
1. **Sélection des actions du portefeuille** par l'IA Mistral en fonction d'un nombre d'actions et d'une période définie.  
2. **Calcul des rendements moyens et de la covariance**.  
3. **Évaluation du risque et du rendement attendu** du portefeuille en fonction des pondérations.  
4. **Optimisation du ratio de Sharpe**.  
5. **Suppression des actions marginales** (<0.1% du portefeuille) et génération de portefeuilles aléatoires pour comparaison.  
6. **Visualisation et backtest** pour analyser la pertinence des résultats.

### Résultats

Avec 3 actions :  
![p2_5a_puiss08](https://github.com/user-attachments/assets/23492b3a-4ac7-4681-8a03-375796ebb58b)  
*Les performances obtenues sur ce choix d'actions restent modestes.*

En modifiant la fonction d'optimisation, le portefeuille se déplace sur la frontière efficiente :  
![p2_5action_puissance01](https://github.com/user-attachments/assets/d3daf5f4-415f-40ca-a271-bc326b1c00ed)  
*Cette variante privilégie des positions moins risquées.*

Un portefeuille plus diversifié affiche 15% de rendement pour 6.5% de risque :  
![Figure_1_projet2](https://github.com/user-attachments/assets/cc11c918-98fd-4b63-8c93-0d36efb651c8)

### Mistral & Backtest

L'IA Mistral est utilisée pour sélectionner les tickers. Par exemple, avec 5 actions :  
```plaintext
Mistral proposition :
['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']

Optimal set :
[('AAPL', 0.303), ('GOOGL', 0.139), ('NVDA', 0.557)]

Deleted tickers :
['MSFT', 'AMZN']

This portfolio is supposed to have a daily return of 0.44% and a daily risk of 2.1867% based on 2024-01-01 to 2024-08-01.

Return of the portfolio on the tested period :
 17.295 %
Expected return of the portfolio over the period : 45.233 %
```

![backt3](https://github.com/user-attachments/assets/07167c7a-105a-4e9d-812c-fdfd21c1ab86)  
*La courbe du portefeuille est en noir.*

On peut modifier le prompting et demander aussi la présence de cryptomonnaies, ainsi qu'une centaine d'actions, ce qui permetterait de trouver une combinaison optimale en sachant qu'on arrondie les poids à 3 chiffres significatifs, ce qui supprime les valeurs proches de 0. Malheureusement, Mistral invente un trop grand nombre d'actions dans ce cas et seulement une vingtaine est retenue en général.

Après modification du prompt pour inclure des cryptomonnaies, on obtient pour 15 actions:

```
Mistral proposition :
 ['MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'V', 'BABA', 'BNP.PA', 'NKE', 'UNH', 'JNJ', 'PG', 'KO', 'VZ', 'BTC-USD']

Optimal set :
 [('MSFT', 0.003), ('AMZN', 0.014), ('NVDA', 0.035), ('V', 0.038), ('BABA', 0.579), ('UNH', 0.157), ('JNJ', 0.004), ('KO', 0.069), ('BTC-USD', 0.102)]

 Deleted tickers :
 ['GOOGL', 'TSLA', 'BNP.PA', 'NKE', 'PG', 'VZ']
This portfolio is supposed to have a daily return of 0.1922% and a daily risk of 0.6308% based on 2024-01-01 to 2024-08-01.

Return of the portfolio on the tested period : 
 4.834 %
Expected return of the portfolio over the period : 26.39 %
```


![back4](https://github.com/user-attachments/assets/16130d77-e207-4040-9588-70c072856db7)


Les paliers qu'on peut voir sur les courbes correspondent à la différence de fuseaux horaires des bourses puisque le prix est constant lorsqu'elles sont fermées ainsi que les cryptomonnaies, qui varient continuement.

---

## Projet 1 : Construction de l'indice S&P 500 avec un risque journalier contrôlé à 5%

L'objectif est d'ajuster dynamiquement l'exposition d'un portefeuille représentant le S&P 500 afin de maintenir un risque maximum de 5%. Ce projet utilise les données fournies par l'API `yfinance` de Yahoo Finance.

### Description du projet

Les étapes importantes de l'algorithme :  
1. **Récupération des données historiques** avec `yfinance`.  
2. **Calcul des rendements et de la volatilité** sur une fenêtre définie (par exemple 20 jours).
3. **Ajustement du rendement** pour respecter le risque cible, avec la formule :  
   $`
   \text{Rendement modifié} = \text{Rendement} \times \left(\frac{\text{Volatilité cible}}{\text{Volatilité actuelle}}\right)
   `$

### Résultats

Par rapport au [modèle de base](https://www.spglobal.com/spdji/en/indices/multi-asset/sp-500-daily-risk-control-5-index/#overview), mon modèle montre un décalage d'environ 3% sur un an.  

**Modèle de référence :**  
![image](https://github.com/user-attachments/assets/ab26c652-308f-4ba0-8276-50e3b983942c)  

**Mon modèle :**  
![SP500_le_mien](https://github.com/user-attachments/assets/96cc1b53-a108-4230-ae73-cc5de319ec41)

---

## Améliorations en cours

1. **Projet 2 : Ajout de contraintes supplémentaires :**  
   - Limiter la part maximale d'une action pour éviter une concentration excessive sur une seule performance historique.
2. **Projet 2 : Génération améliorée des portefeuilles aléatoires :**  
   - Remplacer `np.random.random` par `np.random.normal` pour privilégier des poids proches de 0, tout en réduisant le coût de calcul.
3. **Projet 1 : Paramètres supplémentaires de contrôle**  
   - Prise en compte du **Lag rebalancing**, poids exponentiel aux données dans le calcul de l'écart-type pour prendre plus en compte les données récentes **(EWA)**
