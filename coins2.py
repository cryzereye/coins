# coins v1.1
# lots of refactor
import json
import urllib2
import time
import datetime
from threading import Thread
import csv
import playsound
import loading
import kb



def main():
    """
    main function to start it all
    """
    inputs = get_userinput()
    rates = loading.get_rates()
    flags = {}

    # computation variables
    rates['last'] = int(inputs['rate'])
    rates['fiat'] = float(inputs['fiat'])
    rates['btc'] = float(inputs['crypto'])
    rates['prev_buy'] = int(inputs['rate'])
    rates['prev_sell'] = int(inputs['rate'])
    rates['buy_max'] = int(0)
    rates['buy_min'] = int(0)
    rates['sell_max'] = int(0)
    rates['sell_min'] = int(0)
    

    # flags
    flags['last_buy'] = bool(inputs['action'])
    flags['buy'] = False
    flags['sell'] = False
    flags['spread_beaten'] = False
    flags['ath'] = False
    flags['dip'] = False

    print " BUY   |  SELL  |  RATE  |       PROFIT       |   DO   | DELTA  |"
    t = Thread(target=livethread, args=(rates, flags))
    t.start()

def play_notif(flags):
    if flags['ath']:
        playsound.playsound('mario.mp3', True)
    elif flags['dip']:
        playsound.playsound('wololo.mp3', True)
    if flags['buy'] or flags['sell']:
        playsound.playsound('buy.mp3', True)

def print_stuff(rates, flags, delta, buy, sell):
    """
    do all dynamic prints
    """
    buying = not flags['last_buy']
    buy_div = " | "
    sell_div = " | "
    printstring = ""
    if bool(flags['buy']): buy_div = " < "
    if bool(flags['sell']): sell_div = " > "

    print (str(buy) + buy_div + str(sell) + sell_div + str(rates['last']) + " |"),

    # PROFIT column
    if buying:
        profit = rates['fiat']/buy - rates['fiat']/rates['last']
        printstring = str("BTC %.8f" % profit)
    elif not buying:
        profit = sell * rates['btc'] - rates['last'] * rates['btc']
        printstring = str("PHP %.2f" % profit)
    print (str(printstring.ljust(18, ' ')) + " |"),

    # DO column
    if flags['buy']:
        print ("BUY    |"),
    elif flags['sell']:
        print ("SELL   |"),
    else:
        print ("...... |"),

    # DELTA column
    delta_ave = (delta['buy'] + delta['sell'])/2
    if delta_ave > 0:
        if delta_ave/1000 > 0:
            print ("+" * int(delta_ave/1000)),
        else:
            print ("+"),
    elif delta_ave < 0:
        if delta_ave/1000 < 0:
            print ("-" * int(delta_ave/1000 * -1)),
        else:
            print ("-"),
    print ""

def comparison(rates, flags, buy, sell):
    """
    where all computation and flag setting will happen
    """
    buying = not flags['last_buy']
    delta = {}
    spread = buy - sell
    # update peaks and trenches
    if buy > rates['buy_max']: rates['buy_max'] = buy
    if buy < rates['buy_min']: rates['buy_min'] = buy
    if sell > rates['sell_max']: rates['sell_max'] = sell
    if sell < rates['sell_min']: rates['sell_min'] = sell

    # compute delta
    delta['buy'] = buy - rates['prev_buy']
    delta['sell'] = sell - rates['prev_sell']
    delta['buy_from_sell'] = rates['sell_max'] - buy
    delta['sell_from_buy'] = rates['buy_min'] - sell
    delta['buy_from_last'] = rates['last'] - buy
    delta['sell_from_last'] = rates['last'] - sell

    # flag setting
    flags['buy'] = bool(buying and rates['last'] > buy)
    flags['sell'] = bool(not buying and rates['last'] < sell)
    flags['spread_beaten'] = bool(buying and buy + spread < rates['sell_max']) or bool(not buying and sell - spread > rates['buy_min'])
    flags['ath'] = bool(not buying and delta['sell_from_last']/2000 < 0)
    flags['dip'] = bool(buying and delta['buy_from_last']/2000 > 0)

    # update prev rates
    rates['prev_buy'] = buy
    rates['prev_sell'] = sell

    print_stuff(rates, flags, delta, buy, sell)
    play_notif(flags)

def livethread(rates, flags):
    """
        1 thread function to load the rates then call the necessary print functions
    """
    validTime = 0
    new_rates = []

    while True:
        try:
            # get rates from api
            new_rates = json.load(urllib2.urlopen("https://quote.coins.ph/v1/markets/BTC-PHP"))
            buyRate = new_rates['market']['ask']
            sellRate = new_rates['market']['bid']
            validTime = new_rates['market']['expires_in_seconds']
            rate_row = [datetime.datetime.now(), buyRate, sellRate]
            with open(r'history.csv','ab') as f:
                writer = csv.writer(f)
                writer.writerow(rate_row)
        except Exception:
            print "API failed us"
            next

        if int(validTime) > 0:
            comparison(rates, flags, int(buyRate), int(sellRate))
        loading.save_rates(rates)
        time.sleep(validTime)

def get_userinput():
    """
    gets user inputs. if user wants to use their recent profile,
    user can enter Y in the first question. Else, user will have to enter new ones.
    """
    data = {}
    isLastBuy = False
    lastRate = int(0)
    lastMoney = float(0)
    lastbtc = float(0)
    while True:
        try:
            useLast = str(raw_input("Do you want to use your previous inputs? [Y/N]: "))
            if useLast == 'y' or useLast == 'Y':
                try:
                    data = loading.get_profile()
                    return data
                except Exception:
                    print 'Unable to load previous profile. Please enter new inputs.'
            elif useLast == 'n' or useLast == 'N':
                break
        except Exception:
            print 'Error in previous inputs'

    while True:
        try:
            isLastBuy = str(raw_input("Last action ([B]uy or [S]ell): "))
            if isLastBuy == 'B': isLastBuy = bool(True)
            elif isLastBuy == 'S': isLastBuy = bool(False)
            else: next
            break
        except Exception:
            pass
    while True:
        try:
            lastRate = int(raw_input("Last rate in history: "))
            break
        except Exception:
            print 'Invalid input'
            pass
    while True:
        try:
            lastMoney = float(raw_input("Money you have now: "))
            break
        except Exception:
            print 'Invalid input'
            pass
    while True:
        try:
            lastbtc = float(raw_input("BTC you have now: "))
            break
        except Exception:
            print 'Invalid input'
            pass
    loading.save_profile(isLastBuy, lastRate, lastMoney, lastbtc)

    data['action'] = isLastBuy
    data['rate'] = lastRate
    data['fiat'] = lastMoney
    data['crypto'] = lastbtc
    return data

if __name__ == '__main__':
    main()
    kb.read_stop()
