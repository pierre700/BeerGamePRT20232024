# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:32:20 2024

@author: pierre
"""

import random

def partie (nbRounds, startStock, typeDemande, party):
    currentRound = 0
    if typeDemande == 1:
        dmdCli = calculDemande(1, startStock)
    prodData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, party, "a"]]
    distrData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, party, "b"]]
    wholeData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, party, "c"]]
    retailData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, party, "d"]]
    prodBuffer = []
    distrBuffer = []
    wholeBuffer = []
    retailBuffer = []
    listPlayer = ["prod", "distr", "whole", "retail", "prodDelay", "distrDelay", "wholeDelay", "retailDelay"]
    print("dmd", dmdCli)
    
    for a in range(nbRounds+1) :
        i = currentRound
        listInput=[]
        compt=0
        for j in listPlayer:
            if compt <= 3:
                listInput.append(random.randint(0, 2*startStock))
            else :
                listInput.append(calculDelay())
            compt = compt + 1
        #print("tour", currentRound)
        prodBuffer = fillBuffer(i, listInput[0], prodBuffer, listInput[4])
        distrBuffer = fillBuffer(i, listInput[1], distrBuffer, listInput[5])
        wholeBuffer = fillBuffer(i, listInput[2], wholeBuffer, listInput[6])
        retailBuffer = fillBuffer(i, listInput[3], retailBuffer, listInput[7])
        Data=[prodData, distrData, wholeData, retailData]
        Buffer=[prodBuffer, distrBuffer, wholeBuffer, retailBuffer]
        nextBuffer=[distrBuffer, wholeBuffer, retailBuffer, False]
        prevBuffer=[False, prodBuffer, distrBuffer, wholeBuffer]
        prevStock=[False, prodData[i-1][0], distrData[i-1][0], wholeData[i-1][0]]
        prevRetard=[None, prodData[i][1], distrData[i][1], wholeData[i][1]]
        Stock=[prodData[i][0], distrData[i][0], wholeData[i][0], retailData[i][0]]
        Retard=[prodData[i][1], distrData[i][1], wholeData[i][1], retailData[i][1]]
        ID=["a","b","c","d"]
        for k in range(4):
            Data[k].append(updateStock(Data[k], Buffer[k], nextBuffer[k], prevBuffer[k], prevStock[k], prevRetard[k], Stock[k], Retard[k], currentRound, dmdCli, i==3, typeDemande, ID[k], listInput[k], party, k))
            #distrData.append(updateStock(distrData, distrBuffer, wholeBuffer, prodBuffer, prodData[i-1][0], prodData[i][1], distrData[i][0], distrData[i][1], currentRound, dmdCli, False, typeDemande, "b", listInput[1], party))
            #wholeData.append(updateStock(wholeData, wholeBuffer, retailBuffer, distrBuffer, distrData[i-1][0], distrData[i][1], wholeData[i][0], wholeData[i][1], currentRound, dmdCli, False, typeDemande, "c", listInput[2], party))
            #retailData.append(updateStock(retailData, retailBuffer, False, wholeBuffer, wholeData[i-1][0], wholeData[i][1], retailData[i][0], retailData[i][1], currentRound, dmdCli, True, typeDemande, "d", listInput[3], party))
   
        #print('prod', prodData, prodBuffer)
        #print('distr', distrData, distrBuffer)
        #print('whole', wholeData, wholeBuffer)
        #print('retail', retailData, retailBuffer)
        currentRound = currentRound + 1
    prodData.pop()
    distrData.pop()
    wholeData.pop()
    retailData.pop()
    print('prod', prodData, prodBuffer)
    print('distr', distrData, distrBuffer)
    print('whole', wholeData, wholeBuffer)
    print('retail', retailData, retailBuffer)
    return [prodData, distrData, wholeData, retailData]



def calculDemande(typedemande, startStock):
    if typedemande == 1:
        return random.randint(int(startStock/10), int(startStock*(2/3)))
    
def calculDelay():
    a=random.random()
    if a<0.75:
        return 2
    elif a<0.9:
        return 1
    elif a<0.989:
        return 3
    else : 
        return 4
        
    
def fillBuffer(currentRound, order, buffer, delay): 
    cond = True
    if len(buffer)==0:
        buffer.append([delay+currentRound, order])
    else :
        for i in buffer : 
            if i[0] == delay+currentRound :
                i[1] = i[1] + order
                cond = False
        if cond : 
            buffer.append([delay+currentRound, order])
    return buffer
            

  
def updateStock(roleData, buffer, nextBuffer, prevBuffer, prevStock, prevRetard, Stock, Retard, currentRound, dmdCli, condRetailer, typeDemande, ID, orderRound, party, k):  
    orderList=[]
    for i in range(k):
        orderList.append(orderfct(buffer[i], currentRound))
    #if prevStock == 0 :
        #print("=0", order, prevStock)
    for i in range(k):
        if orderL > prevStock and prevStock is not False:
            if ID == "d":
                print(ID)
            print("=0", order, prevStock)
            print("order", "-", "prevStock", order, "-", prevStock)
            a = orderfct(prevBuffer, currentRound)
            diff = order - prevStock - a
            order = prevStock + a
            prevRetard = prevRetard + diff
    if nextBuffer != False : 
        nextOrder = orderfct(nextBuffer, currentRound)
        diff = order - nextOrder
        #print("diff", order, " - ", nextOrder, " = ", diff)
    if condRetailer :
        diff = order - dmdCli
    if diff > 0 :
        if Retard == 0 :
            Stock = Stock + diff
        elif diff >= Retard : 
            diff = diff - Retard
            Retard = 0
            Stock = Stock + diff
        elif Retard > diff :
            Retard = Retard - diff
    elif diff < 0 :
        if Stock >= abs(diff)  :
            Stock = Stock + diff
        elif abs(diff) > Stock :
            diff = abs(diff) - Stock
            Retard = Retard + diff
            Stock = 0 
    roleData[currentRound] = [Stock, Retard, currentRound, dmdCli, typeDemande, orderRound, party, ID]    
    return [Stock, Retard, currentRound+1, dmdCli, typeDemande, orderRound, party, ID]
    
        
def orderfct(buffer, currentRound):
    cond = True
    for i in buffer:
        #print("i", i)
        #print("i0", i[0], currentRound)
        #print("type", type(i[0]), type(currentRound))
        if i[0] == currentRound:
            order = i[1]
            cond = False
    if cond: 
        order = 0
    return order
    

def collectData(nbPartie, nbRounds, typeDemande): 
    fichierProd= open("Data_Set_Prod.txt", "w")
    fichierDistr= open("Data_Set_Distributor.txt", "w")
    fichierWhole= open("Data_Set_Wholesaler.txt", "w")
    fichierRetail= open("Data_Set_Retailer.txt", "w")
    fichierProd.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,partie_numero")
    fichierDistr.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,partie_numero")
    fichierWhole.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,partie_numero")
    fichierRetail.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,partie_numero")
    fichierProd= open("Data_Set_Prod.txt", "a")
    fichierDistr= open("Data_Set_Distributor.txt", "a")
    fichierWhole= open("Data_Set_Wholesaler.txt", "a")
    fichierRetail= open("Data_Set_Retailer.txt", "a")
    fichierProd.write("\n")
    fichierDistr.write("\n")
    fichierWhole.write("\n")
    fichierRetail.write("\n")
    for i in range(nbPartie) : 
        startStock = random.randint(10, 100)
        dataPartie = partie(nbRounds, startStock, typeDemande, i)
        for i in dataPartie : 
            for j in i : 
                dataTour = ""
                for k in j :
                    if k != j[-1]:
                        dataTour = dataTour + str(k)
                        dataTour = dataTour + ","
                if j[-1]=="a":
                    fichierProd.write(dataTour)
                    fichierProd.write("\n")
                if j[-1]=="b":
                    fichierDistr.write(dataTour)
                    fichierDistr.write("\n")
                if j[-1]=="c":
                    fichierWhole.write(dataTour)
                    fichierWhole.write("\n")
                if j[-1]=="d":
                    fichierRetail.write(dataTour)
                    fichierRetail.write("\n")

                    
            
collectData(1, 20, 1)


