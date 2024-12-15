import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from math import sqrt

def index_SP_avec_risque(ticker:str,periode:str,risk:int,fenetre:int,lag:int,EWA:int,plot:bool):
    stock=yf.Ticker(ticker)
    history=stock.history(periode)
    returns=history.pct_change()["Close"]
    returns=returns.to_frame(name="Returns")
    volatility=returns.rolling(fenetre).std().ffill() # si fenetre=30 rolling calcul avec la 30ieme pour le j30
    returns.insert(0,"Close",history["Close"])
    returns.insert(2,"Volatility",volatility)
    #returns.insert(3,"Annualized returns",(1+returns["Returns"])**252-1)
    returns.insert(3,"Annualized std",returns["Volatility"]*sqrt(252))
    returns.insert(4,"Controled returns",returns["Close"])

    returns["Controled returns"]=returns.apply(lambda row: row["Returns"]*((risk*0.01)/row["Annualized std"]) if row["Annualized std"]>(risk*0.01) else row["Returns"],axis=1)
    returns.insert(5,"Controled returns STD",sqrt(252)*returns["Controled returns"].rolling(fenetre).std().ffill())
    if plot:
        returns.insert(5,"Strike",100*((1+returns["Returns"].fillna(0)).cumprod()))
        returns.insert(6,"Controled Strike",100*((1+returns["Controled returns"].fillna(0)).cumprod()))
        returns["Strike"].plot()
        returns["Controled Strike"].plot()
        plt.show()
    else:
        print(returns)

index_SP_avec_risque("^GSPC","1y",10,5,1,10,plot=True)
