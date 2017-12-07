import json
import urllib2
import time
import playsound
from threading import Thread

# profile: change every transaction made then rerun script
isLastBuy = True                     # buy/sell BTC
lastRate =  int(705722)              # last rate used in buy/sell

highestSellRate = lastRate
highestBuyRate = lastRate
lowestBuyRate = lastRate
    
def printing(buyRate, sellRate):
    global highestSellRate
    global lowestBuyRate
    global highestBuyRate

    if isLastBuy:
        if int(sellRate) > lastRate:
            print (buyRate + "       " + sellRate + " >>>> " + str(lastRate) + "      SELL NOW"),
        else:
            print (buyRate + "       " + sellRate + "      " + str(lastRate) + "      HODL"),
    else:
        if int(buyRate) < lastRate:
            print (buyRate + " <<<<  " + sellRate + "      " + str(lastRate) + "      BUY NOW"),
        else:
            print (buyRate + "       " + sellRate + "      " + str(lastRate) + "      ..."),
    if highestSellRate < sellRate:
        highestSellRate = sellRate
        print ("         ATH"),
        playsound.playsound('mario.mp3', True)
    if lowestBuyRate > buyRate: lowestBuyRate = buyRate
    if highestBuyRate < buyRate: highestBuyRate = buyRate

    # dip detection, for PHP only
    isDip = (int(highestBuyRate) - int(buyRate))/1000
    if isDip > 0:
        print ("         D"),
        print ("I") * isDip,
        print ("P"),
        if isDip > 5:
            playsound.playsound('wololo.mp3', True)
    print ""
    
def rateComp(buy, sell):
    # if selling , if buying
    return isLastBuy and sell > lastRate or not isLastBuy and buy < lastRate

def livethread():
    validTime = 0

    while True:
        try:
            # get rates from api
            rates = json.load(urllib2.urlopen("https://quote.coins.ph/v1/markets/BTC-PHP"))
        except Exception:
            print "API failed us"
            next

        buyRate = rates['market']['ask']
        sellRate = rates['market']['bid']
        validTime = rates['market']['expires_in_seconds']

        if int(validTime) > 0:
            printing(buyRate, sellRate)        

        if rateComp(int(buyRate), int(sellRate)):
            playsound.playsound('buy.mp3', True)

        time.sleep(validTime)


#####   MAIN   #####
print "BUY          SELL        LAST RATE   WHAT TO DO"
t = Thread(target=livethread, args=())
t.start()
