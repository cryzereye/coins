import json
import urllib2
import time
import playsound
from threading import Thread

# profile
isLastBuy = True                     # buy/sell BTC
amountUsed = int(2000)               # last amount used in buy/sell
lastRate =  int(596450)              # last rate used in buy/sell
lastBTC = float(0.00335317)          # last BTC gain/sold

def printing(buyRate, sellRate):
    if isLastBuy:
        if int(sellRate) > lastRate:
            print buyRate + "       " + sellRate + " >>>> " + str(lastRate) + "      SEEEEELL NOW"
        else:
            print buyRate + "       " + sellRate + "      " + str(lastRate) + "      HODL"
    else:
        if int(buyRate) < lastRate:
            print buyRate + " <<<<  " + sellRate + "      " + str(lastRate) + "      BUUUUUY NOW"
        else:
            print buyRate + "       " + sellRate + "      " + str(lastRate) + "      ..."

def rateComp(buy, sell):
    # if selling , if buying
    return isLastBuy and sell > lastRate or not isLastBuy and buy < lastRate

def livethread():
    validTime = 0
    while True:
        # get rates from api
        rates = json.load(urllib2.urlopen("https://quote.coins.ph/v1/markets/BTC-PHP"))

        buyRate = rates['market']['ask']
        sellRate = rates['market']['bid']

        printing(buyRate, sellRate)        

        if rateComp(int(buyRate), int(sellRate)):
            playsound.playsound('buy.mp3', True)

        validTime = rates['market']['expires_in_seconds']
        time.sleep(validTime)


#####   MAIN   #####
print "BUY          SELL        LAST RATE   WHAT TO DO"
t = Thread(target=livethread, args=())
t.start()
