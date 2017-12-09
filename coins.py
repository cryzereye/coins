import sys
import json
import urllib2
import time
import playsound
import loading
import kb
from threading import Thread

# globals
isLastBuy = True
lastRate = int(0)
highestSellRate = int(0)
highestBuyRate = int(0)
lowestBuyRate = int(0)
ath_buy = int(0)
ath_sell = int(0)
    
def printing(buyRate, sellRate):
    global highestSellRate
    global highestBuyRate
    global lowestBuyRate
    global ath_buy
    global ath_sell
    spread = int(buyRate) - int(sellRate)
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
    
    if highestBuyRate < buyRate:
        highestBuyRate = buyRate
        if highestBuyRate > ath_buy:
            ath_buy = highestBuyRate
            loading.updateATH(int(ath_buy), int(ath_sell))

    isDip = (int(highestBuyRate) - int(buyRate))/2000
    isAth = (int(sellRate) - int(lastRate))/2000
    # dip detection, for PHP only
    if highestSellRate < sellRate and sellRate > lastRate:
        highestSellRate = sellRate
        ath_sell = sellRate
        loading.updateATH(int(ath_buy), int(ath_sell))
        if isAth > 0:
            print ("       "),
            print ("A") * isAth,
            print ("TH"),
            if isAth > spread/2000:
                playsound.playsound('nice.mp3', True)
            else:
                playsound.playsound('mario.mp3', True)
    elif isDip > 0:
        print ("         D"),
        print ("I") * isDip,
        print ("P"),
        if isDip > spread/2000:
            playsound.playsound('wololo.mp3', True)
    print ""
    
def rateComp(buy, sell):
    # if selling , if buying
    return isLastBuy and sell > lastRate or not isLastBuy and buy < lastRate

def livethread():
    """
        1 thread function to load the rates then call the necessary print functions
    """
    validTime = 0
    rates = []

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
def main():
    """
    This is just for starting the whole script in a cleaner way
    """
    global ath_buy
    global ath_sell
    ath = loading.getATH()
    ath_buy = ath['ath_buy']
    ath_sell = ath['ath_sell']

    global isLastBuy
    global lastRate

    while True:
        try:
            isLastBuy = str(raw_input("Last action ([B]uy or [S]ell): "))
            if isLastBuy == 'B': isLastBuy = bool(True)
            elif isLastBuy == 'S': isLastBuy = bool(False)
            else: next
            break
        except Exception:
            next
    while True:
        try:
            lastRate = int(raw_input("Last rate in history: "))
            break
        except Exception:
            next
    global highestSellRate
    global highestBuyRate
    global lowestBuyRate
    highestSellRate = lastRate
    highestBuyRate = lastRate
    lowestBuyRate = lastRate

    print "BUY          SELL        LAST RATE   WHAT TO DO"
    t = Thread(target=livethread, args=())
    t.start()

if __name__ == '__main__':
    main()
    kb.read_stop()