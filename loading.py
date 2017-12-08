import json

def jsonload():
    # for loading recent history
    try:
        data = json.load("hist.json")
        return data
    except Exception:
        return []

def jsonsave(data):
    # for saving the recently accumulated data, will overwrite all
    save = {}
    for d in data:
        jsondata = {'datetime' : d[0],
                    'buy'      : d[1],
                    'sell'     : d[2]
                   }
        save.update(jsondata)
    try:
        jsonfile = open("hist.json", "w+")
        jsonfile.write(json.dumps(save))
        jsonfile.close()
        return True
    except Exception:
        return False

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