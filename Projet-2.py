import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from math import sqrt
from scipy.optimize import minimize
import requests
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import json


def contrainte(poids):
    return np.sum(poids)-1 #contrainte=0 dans minimise; ici on veut 100% du portefeuille en actions

def calcul_rendement_portefeuille(poids, rendements_moyens):
    return np.dot(poids, rendements_moyens)*252

def calcul_risque_portefeuille(poids, matrice_cov):
    return sqrt(np.dot(poids, np.dot(matrice_cov, poids))*252)

def perfomance_portefeuille(poids:list,rendements: pd.DataFrame):
    #note la performance du portefeuille selon une fonction (ici le ratio risque/rendement)
    matrice_cov= rendements.cov()
    rendements_moyens=rendements.mean()
    rendement_attendu_portfolio=calcul_rendement_portefeuille(poids,rendements_moyens)
    portfolio_risk=calcul_risque_portefeuille(poids, matrice_cov)
    #ici mettre la fonction qu'on veut, en fonction de comment on aime le risque
    #du plus au moins risqué: risque/rendement**2 , risque/rendement ,  risque, etc
    return portfolio_risk/(rendement_attendu_portfolio)

def meilleure_combinaison(actions:list,start:str, end:str):
    #trouve la meilleure combinaison d'actions pour un portefeuille
    historiques=[]
    m=len(actions)
    for i in range(m):
        historiques.append(yf.Ticker(actions[i]).history(start=start, end=end).Close)#récolte des historiques des actions à la fermeture
    df_histo=pd.DataFrame(historiques).T #pour transposer
    df_histo.columns=actions
    rendements= df_histo.pct_change().dropna()#calcul des rendements
    bounds = [(0, 1) for k in range(m)]#proportion de chaque action entre 0 et 1
    ci=[1/m for k in range(m)]#poids initial de chaque action égaux

    contraintes={'type': 'eq', 'fun': contrainte}
    meilleure_combi =minimize(perfomance_portefeuille,ci,args=(rendements), method='SLSQP', bounds=bounds, constraints=contraintes)
    return meilleure_combi.x, rendements

def generer_portefeuilles(rendements, nombre_portefeuilles):
    nombre_actions = rendements.shape[1]
    rendements_moyens = rendements.mean()
    matrice_cov = rendements.cov()
    couples_rendement_risque = []

    for _ in range(nombre_portefeuilles):
        #poids totalisent 1
        poids = np.random.random(nombre_actions)
        poids /= np.sum(poids)

        rendement = calcul_rendement_portefeuille(poids, rendements_moyens)
        risque = calcul_risque_portefeuille(poids, matrice_cov)
        couples_rendement_risque.append((rendement, risque))
    return couples_rendement_risque

def afficher_portefeuilles(couples_rendement_risque,meilleur_couple):
    rendements, risques = zip(*couples_rendement_risque)#* pour décompresser
    rendements = np.array(rendements)
    risques = np.array(risques)
    plt.figure(figsize=(10, 10))
    # Scatter plot avec le ratio rendement/risque
    plt.scatter(risques, rendements, c=rendements/risques, marker='o',s=5)
    plt.scatter(meilleur_couple[1], meilleur_couple[0], color='red', marker='o', s=30)
    #meilleur_couple[1] = risque
    plt.title('Frontière efficiente des portefeuilles\nie toutes les performances possibles des portefeuilles pour les actions choisies\nLe point rouge est le portefeuille optimal')
    plt.xlabel('Risque')
    plt.ylabel('Rendement attendu')
    plt.colorbar(label='Rendement/Risque')
    plt.show()

def tickers_mistral(n,start,end):
    #demande à l'API Mistral n tickers d'entreprises de secteurs variés ayant performé entre start et end
    prefixe="Il faut que tu varie tes réponse. Si tu choisi de mettre l'un ou plusieurs d'entre eux, met juste le bon ticker : change 'FB' par 'META', change 'BNP' par 'BNP.PA',change 'TOT' par 'TTE.PA',change 'BT' par 'BT-A.L'. Ne porpose pas 'BNSF' ni 'TWTR'. N'ajoute aucuns détails ou explication, n'invente aucun ticker. Ne met pas de retour à la ligne dans la liste."
    
    api_key = "a remplir"
    
    model ="open-mistral-nemo-2407"
    client=MistralClient(api_key=api_key)
    request="donne moi au format JSON un objet qui contient uniquement une liste de "+ str(n) +" tickers valide sur Yahoo Finance, d'entreprises françaises et internationales dans des secteurs d'activité varié, qui ont performées entre " + start + " et " + end
    resp=client.chat(model=model,messages=[ChatMessage(role="system",content=prefixe),ChatMessage(role="user",content=request),])
    
    actions_str=resp.choices[0].message.content
    #actions = json.loads(actions_str) parfois actions_str est déjà une liste, souvent un dict
    actions_dict = json.loads(actions_str)
    actions = actions_dict['tickers']
    if (type(actions))!=list:
        print("Erreur lors de la récupération des tickers")
        return Error
    return actions

def affichage_meilleure_partition(actions,start,end,nombre_portefeuilles):
    meilleure_partition,rendements=meilleure_combinaison(actions,start,end)
    meilleure_partition = [round(x,3) for x in meilleure_partition]#arrondie a 3 chiffres apres la virgule
    actions_a_garder = [(actions[i], meilleure_partition[i]) for i in range(len(meilleure_partition)) if meilleure_partition[i] > 0]
    action_a_jetee = [actions[i] for i in range(len(meilleure_partition)) if meilleure_partition[i] == 0]
    for action, poids in actions_a_garder:
        print(f'Action: {action}, Poids: {poids*100}%')

    print(actions_a_garder)

    meilleur_couple=[calcul_rendement_portefeuille(meilleure_partition,rendements.mean()),calcul_risque_portefeuille(meilleure_partition,rendements.cov())]
    print("Avec un rendement de",meilleur_couple[0],"et un risque de",meilleur_couple[1])
    print("Actions à enlever:",action_a_jetee)
    couples = generer_portefeuilles(rendements, nombre_portefeuilles)
    afficher_portefeuilles(couples,meilleur_couple)
    return

start = '2024-01-01'#yyyy-mm-dd
end = '2024-08-07'
n=10
nombre_portefeuilles=10000

actions = tickers_mistral(n,start,end)
affichage_meilleure_partition(actions,start,end,nombre_portefeuilles)
