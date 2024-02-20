# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 13:32:20 2024

@author: pierre
"""

import random

def partie (nbRounds, startStock, typeDemande):
    currentRound = 0
    if typeDemande == 1:
        dmdCli = calculDemande(1, startStock)
    prodData = [[startStock, 0, currentRound, dmdCli]]
    distrData = [[startStock, 0, currentRound, dmdCli]]
    wholeData = [[startStock, 0, currentRound, dmdCli]]
    retailData = [[startStock, 0, currentRound, dmdCli]]
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
        print("tour", currentRound)
        prodBuffer = fillBuffer(i, listInput[0], prodBuffer, listInput[4])
        distrBuffer = fillBuffer(i, listInput[1], distrBuffer, listInput[5])
        wholeBuffer = fillBuffer(i, listInput[2], wholeBuffer, listInput[6])
        retailBuffer = fillBuffer(i, listInput[3], retailBuffer, listInput[7])
        #print("stock", prodData[i][0], " i ", i)
        #print(prodData)
        prodData.append(updateStock(prodData, prodBuffer, distrBuffer, prodData[i][0], prodData[i][1], currentRound, dmdCli, False))
        distrData.append(updateStock(distrData, distrBuffer, wholeBuffer, distrData[i][0], distrData[i][1], currentRound, dmdCli, False))
        wholeData.append(updateStock(wholeData, wholeBuffer, retailBuffer, wholeData[i][0], wholeData[i][1], currentRound, dmdCli, False))
        retailData.append(updateStock(retailData, retailBuffer, False, retailData[i][0], retailData[i][1], currentRound, dmdCli, True))
   
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
            

  
def updateStock(roleData, buffer, nextBuffer, Stock, Retard, currentRound, dmdCli, condRetailer):  
    order = orderfct(buffer, currentRound)
    if nextBuffer != False : 
        nextOrder = orderfct(nextBuffer, currentRound)
        diff = order - nextOrder
        print("diff", order, " - ", nextOrder, " = ", diff)
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
    roleData[currentRound] = [Stock, Retard, currentRound, dmdCli]    
    return [Stock, Retard, currentRound+1, dmdCli]
    
        
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
                
partie(5, 30, 1)