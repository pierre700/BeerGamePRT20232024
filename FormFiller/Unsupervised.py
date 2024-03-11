# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:59:30 2024

@author: pierre
"""

import pandas as pd
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

myDataProd = pd.read_csv("Data_Set_Prod.csv", sep=";")
myDataDistr = pd.read_csv("Data_Set_Distributor.csv", sep=";")
myDataWhole = pd.read_csv("Data_Set_Wholesaler.csv", sep=";")
myDataRetail = pd.read_csv("Data_Set_Retailer.csv", sep=";")

dfProd = pd.DataFrame(myDataProd).head(100)
dfDistr = pd.DataFrame(myDataDistr).head(100)
dfWhole = pd.DataFrame(myDataWhole).head(100)
dfRetail = pd.DataFrame(myDataRetail).head(100)

#print(df.info())
#print(df.corr())

#x²dfProd.groupby("partie_numero")["Stock"].plot(title='Stock', color="b")
dfDistr.groupby("partie_numero")["Stock"].plot(title='Stock', color="g")
dfWhole.groupby("partie_numero")["Stock"].plot(title='Stock', color="r")
dfRetail.groupby("partie_numero")["Stock"].plot(title='Stock', color="y")
plt.legend()
a = dfProd.groupby("partie_numero")["Stock"]
print(a)