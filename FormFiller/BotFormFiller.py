from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys


game_url = "http://192.168.70.88:3000"
driver1 = webdriver.Chrome()
driver2 = webdriver.Chrome()
driver3 = webdriver.Chrome()
driver4 = webdriver.Chrome()
driver5 = webdriver.Chrome()
driverList = [driver1, driver2, driver3, driver4, driver5]
driver1.get(game_url)
driver2.get(game_url)
driver3.get(game_url)
driver4.get(game_url)
driver5.get(game_url)



def getGameCode(file): 
    FileGameCode = open(file, "r")
    gameCodeValue = FileGameCode.read()
    newGameCodeValue = str(int(gameCodeValue) + 1 )
    while len(newGameCodeValue) != 5 :
        newGameCodeValue = "0" + newGameCodeValue
    FileGameCode = open(file, "w")
    FileGameCode.write(newGameCodeValue)
    FileGameCode.close()
    return gameCodeValue

def fillParam(GameCodeValue, roundsValue, startStockValue, delayValue, typeDemandXpath, constValue):
    
    button = driver1.find_element("xpath", "//div[@class='tile_wrapper']//div[1]")
    button.click()
    gameCode = driver1.find_element("name", "GameCode")
    rounds = driver1.find_element("name", "Rounds")
    startStock = driver1.find_element("name", "StartStock")
    delay = driver1.find_element("name", "Délai")
    typeDemand = driver1.find_element("xpath", typeDemandXpath)
    const = driver1.find_element("name", "Enter value of constant...")
    gameCode.send_keys(GameCodeValue)
    rounds.send_keys(roundsValue)
    startStock.send_keys(startStockValue)
    delay.send_keys(delayValue)
    const.send_keys(constValue)
    typeDemand.click()
    submit = driver1.find_element("xpath","//button[normalize-space()='Créer un jeu']")
    submit.click()
    driver1.get(game_url)
    openMenu([driver1])
    
def openMenu (driverList):
    for i in driverList:
        button = i.find_element("xpath", "//a[@href='/game/create']//button")
        button.click()
        
        
def openRoom (driverList, GameCodeValue):
    for i in range(len(driverList)) :
        button = driverList[i].find_element("xpath", "//div[@class='game_select']//div[2]")
        button.click()
        room = driverList[i].find_element("xpath", "//input[@placeholder='GameCode']")
        room.send_keys(GameCodeValue)
        button = driverList[i].find_element("xpath", "//button[normalize-space()='Choisissez le rôle de jeu']")
        button.click()
        
def chooseRole(driverList):
    XpathRoleList = ["//div[@class='select_role']//div[1]", "//div[@class='select_role']//div[2]", "//div[@class='select_role']//div[3]", "//div[@class='select_role']//div[4]", "//div[@class='select_role']//div[5]"]
    for i in range(len(driverList)) :
        role = driverList[i].find_element("xpath", XpathRoleList[i])
        role.click()
        button = driverList[i].find_element("xpath", "//button[normalize-space()='Entrer dans le jeu']")
        button.click()

def estimateOrder():
    return 1 

def playGame(rounds, driverList):
    for i in range(rounds):
        for j in driverList :
            if j == driver5 :
                prod = j.find_element("name", "producerDelay")
                distrib = j.find_element("name", "distributorDelay")
                whole = j.find_element("name", "wholesalerDelay")
                retail = j.find_element("name", "retailerDelay")
                prod.send_keys(estimateOrder())
                distrib.send_keys(estimateOrder())
                whole.send_keys(estimateOrder())
                retail.send_keys(estimateOrder())
                button = j.find_element("xpath", "//button[normalize-space()='Commande']")
                button.click()
            else :
                order  = j.find_element("xpath", "//input[@placeholder='OrderQuantity']")
                order.send_keys(estimateOrder())
                button = j.find_element("xpath", "//button[normalize-space()='Commande']")
                button.click()
            print(j)
        print(i)


file = "Game_Code.txt"
roundsValue = 5
startStockValue = 3
delayValue = 1
typeDemandXpath = "//input[@id='{const}']"
constValue = 1

openMenu(driverList)
GameCodeValue = getGameCode(file)
fillParam(GameCodeValue, roundsValue, startStockValue, delayValue, typeDemandXpath, constValue)
openRoom(driverList, GameCodeValue)
chooseRole (driverList)
print("play")
sleep(2)
playGame(roundsValue+1, driverList)