import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from math import sqrt


def index_SP_avec_risque(nom:str,periode:str,risk:int,fenetre:int):

    historique = yf.Ticker(nom).history(period=periode)
    n=len(historique.index)
    if n<fenetre+10:
        print("FENETRE TROP GRANDE")
    
    rendement=[0]*n#pour creer une liste de taille n avec que des 0
    vol=[0.1]*n
    rendement_ajuste=[0]*n
    prix_ajuste=[historique.Close[0]]*n

    #calcul du rendement
    for i in range(1,n):
        rendement[i]= (historique.Close[i]-historique.Close[i-1])/historique.Close[i-1]

    #calcul de la vol sur fenetre jours, les fenetre premières case de vol[] seront donc à 0.1
    for i in range(fenetre-1,n):
        rendement_moy=np.mean(rendement[i-fenetre+1:i+1])
        variance=0
        for j in range(fenetre):
            variance+=(rendement[i-j]-rendement_moy)**2
        variance/=(fenetre-1)
        vol[i]= sqrt(variance)*sqrt(252)#vol annuelle, il faut multiplier par le nombre de période

    #calcul du prix ajusté
    for i in range(n):#la vol est nulle avant fenetre
        if vol[i]!=0:
            rendement_ajuste[i]=rendement[i]*(risk/(100*vol[i]))
            prix_ajuste[i]=prix_ajuste[i-1]*(1+rendement_ajuste[i])

    #normalisation
    normalisation=historique.Close[0]/100
    for i in range(n):
        prix_ajuste[i]/=normalisation
        historique.Close[i]/=normalisation
    

    plt.figure(figsize=(10, 6))
    plt.plot(historique.index, historique.Close, label=nom)
    plt.plot(historique.index,prix_ajuste,label="prix ajuste du " + nom)

    plt.title("Historique de "+nom+" par rapport a celui d'un risque de "+ str(risk) +"%")
    plt.xlabel("Date")
    plt.ylabel("Prix de clôture")
    plt.legend()
    plt.show()
    return

index_SP_avec_risque("^GSPC","1y",5,30)
#index_SP_avec_risque("AAPL","1y",10,30)

