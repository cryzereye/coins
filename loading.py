import json

def updateATH(buy, sell):
    data = {'ath_buy'   : buy,
            'ath_sell'  : sell
           }
    try:
        jsonfile = open("ath.json", "w+")
        jsonfile.write(json.dumps(data))
        jsonfile.close()
    except Exception:
        pass

def getATH():
    try:
        data = json.load(open("ath.json"))
        return data
    except Exception:
        return []

def save_rates(rates):
    while True:
        try:
            jsonfile = open("rates.json", "w+")
            jsonfile.write(json.dumps(rates))
            jsonfile.close()
            break
        except Exception:
            pass

def get_rates():
    try:
        data = json.load(open("rates.json"))
        return data
    except Exception:
        return {}

def save_profile(lastAction, rate, fiat, crypto):
    data = {'action' : lastAction,
            'rate' : rate,
            'fiat' : fiat,
            'crypto' : crypto
           }
    while True:
        try:
            jsonfile = open("profile.json", "w+")
            jsonfile.write(json.dumps(data))
            jsonfile.close()
            break
        except Exception:
            pass

def get_profile():
    try:
        data = json.load(open("profile.json"))
        return data
    except Exception:
        print "profile.json not found!"
        return []