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
    prodData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, 0, party, "a"]]
    distrData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, 0, party, "b"]]
    wholeData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, 0, party, "c"]]
    retailData = [[startStock, 0, currentRound, dmdCli, typeDemande, 0, 0, party, "d"]]
    prodBuffer = []
    distrBuffer = []
    wholeBuffer = []
    retailBuffer = []
    listPlayer = ["prod", "distr", "whole", "retail", "prodDelay", "distrDelay", "wholeDelay", "retailDelay"]
    print("dmd", dmdCli)
    
    for a in range(nbRounds+1) :
        listInput=[]
        compt=0
        for j in listPlayer:
            if compt <= 3:
                listInput.append(random.randint(0, int(1.5*startStock)))
            else :
                listInput.append(calculDelay())
            compt = compt + 1
        #print("tour", currentRound)
        prodBuffer = fillBuffer(a, listInput[0], prodBuffer, listInput[4])
        distrBuffer = fillBuffer(a, listInput[1], distrBuffer, listInput[5])
        wholeBuffer = fillBuffer(a, listInput[2], wholeBuffer, listInput[6])
        retailBuffer = fillBuffer(a, listInput[3], retailBuffer, listInput[7])
        
        print(startStock, listInput)
        commandeRecueProd = orderfct(prodBuffer, a)
        
        prodData.append(updateStock(commandeRecueProd, prodData, orderfct(distrBuffer, a), a, dmdCli, typeDemande, party, "a", prodBuffer))
        distrData.append(updateStock(prodData[a+1][6], distrData, orderfct(wholeBuffer, a), a, dmdCli, typeDemande, party, "b", distrBuffer))
        wholeData.append(updateStock(distrData[a+1][6], wholeData, orderfct(retailBuffer, a), a, dmdCli, typeDemande, party, "c", wholeBuffer))
        retailData.append(updateStock(wholeData[a+1][6], retailData, int(random.uniform(0.5, 2)*dmdCli), a, dmdCli, typeDemande, party, "d", retailBuffer, cond=False))
        #print('prod', prodData, prodBuffer)
        #print('distr', distrData, distrBuffer)
        #print('whole', wholeData, wholeBuffer)
        #print('retail', retailData, retailBuffer)
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
        return random.randint(int(startStock/5), int(startStock*(2/3)))
    
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
            

  
def updateStock(commandeRecue, roleData, demande, currentRound, dmdCli, typeDemande, party, ID, buffer, cond=True): 
    precRetard = 0
    if cond :
        precRetard = roleData[currentRound][1]
    somme = roleData[currentRound][0] + commandeRecue - precRetard - demande
    if cond is not True:
        print("somme= stock + recue - retard - demande", roleData[currentRound][0], commandeRecue, precRetard, demande)
    if somme >= 0 : 
        dispo = precRetard + demande
        stock = somme
        retard = 0
    else : 
        dispo = roleData[currentRound][0] + commandeRecue
        stock = 0
        retard = 0 - somme
    if cond:
        roleData[currentRound]=[stock, retard, currentRound, dmdCli, typeDemande, orderfct(buffer,currentRound), dispo, party, ID]
        return [stock, retard, currentRound, dmdCli, typeDemande, orderfct(buffer,currentRound), dispo, party, ID]
    else :
        roleData[currentRound]=[stock, retard, currentRound, dmdCli, typeDemande, orderfct(buffer,currentRound), dispo, party, ID]
        return [stock, 0, currentRound, dmdCli, typeDemande, orderfct(buffer,currentRound), dispo, party, ID]

        
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
    fichierProd.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,qt_envoye,partie_numero")
    fichierDistr.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,qt_envoye,partie_numero")
    fichierWhole.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,qt_envoye,partie_numero")
    fichierRetail.write("Stock,Retard,Round,Demande_Client,typeDemande,OrderRound,qt_envoye,partie_numero")
    fichierProd= open("Data_Set_Prod.txt", "a")
    fichierDistr= open("Data_Set_Distributor.txt", "a")
    fichierWhole= open("Data_Set_Wholesaler.txt", "a")
    fichierRetail= open("Data_Set_Retailer.txt", "a")
    fichierProd.write("\n")
    fichierDistr.write("\n")
    fichierWhole.write("\n")
    fichierRetail.write("\n")
    for i in range(nbPartie) : 
        startStock = random.randint(100, 1000)
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

                    
            
collectData(1, 100, 1)
