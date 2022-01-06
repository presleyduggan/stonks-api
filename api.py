from flask import Flask, jsonify
from flask_cors import CORS
from yahoo_fin import stock_info as si
from decimal import Decimal
#import time

appFlask = Flask(__name__)
CORS(appFlask)

def get_initial_prices(stock_dict):
    list_o_prices = []
    for i in range(0, len(stock_dict["ticker"])):
        prices = round(si.get_data(stock_dict["ticker"][i] , start_date = '12/31/2021'), 2)
        list_o_prices.append(prices['close'][0])

    # print 
    for i in range(0, len(list_o_prices)):
        ticker = stock_dict["ticker"][i]
        print(f"For ticker ${ticker} the close price on 12/31 was {list_o_prices[i]}")

def get_current_prices(stock_dict):
    current_p = []
    percent_c = []
    for i in range(0,len(stock_dict["ticker"])):
        current_p.append(round(si.get_live_price(stock_dict["ticker"][i]),2))
        percent_c.append(round((((current_p[i]-stock_dict["initial"][i])/stock_dict["initial"][i])*100),2))

    stock_dict["current"] = current_p
    stock_dict["percent"] = percent_c

def get_spy_data():
    stonk = {}
    stonk["ticker"] = ["SPY"]
    stonk["initial"] = [474.96]
    get_current_prices(stonk)
    #print(stonk)
    return stonk

@appFlask.route('/api', methods=['GET', 'POST'])
def home2():
    names = ["adam", "ben", "charlie", "dave"]
    data = [1,2,3,4]
    price = [10, 20, 30, 40]
    dict_list = []
    for i in range(0, 4):
        new_dict = {}
        new_dict["Name"] = names[i]
        new_dict["Tag"] = data[i]
        new_dict["Cost"] = price[i]
        dict_list.append(new_dict)
    send = jsonify(dict_list)
    print(send)
    return send

@appFlask.route('/', methods=['GET'])
def home():
    return "This site is no longer valid and is only used for API purposes. Please visit www.pres.dev/stonks"


@appFlask.route('/api/SPY', methods=['GET', 'POST'])
def get_spy():
    stonk = {}
    stonk["ticker"] = ["SPY"]
    stonk["initial"] = [474.96]
    get_current_prices(stonk)
    #print(stonk)
    #get_current_prices(stonk)
    return "SPY"

@appFlask.route('/api/stonks', methods=['GET', 'POST'])
def stonk_api():
    #start = time.time()
    stonk_data = {}
    stonk_data["names"] = ['David', 'Jack', 'Jawsh', 'Mark', 'Mitch', 'Poles', 'Presley', 'Rex', 'Sean']
    stonk_data["ticker"] = ['SMRT', 'AI', 'DIS', 'SE', 'XLNX', 'ROKU', 'AAPL', 'NVDA', 'IBM']
    stonk_data["initial"] = [9.68, 31.25, 154.89, 223.71, 212.03, 228.2, 177.57, 294.11, 133.66]
    stonk_data["current"] = {}
    stonk_data["percent"] = {}
    get_current_prices(stonk_data)
    #end = time.time()
    # get max
    max_stonker = max(range(len(stonk_data["percent"])), key=lambda index: stonk_data['percent'][index])
    #print(stonk_data["names"][max_stonker])
    #print(end-start)
    send_arr = []
    for i in range(0, len(stonk_data["names"])):
        new_dict = {}
        new_dict["name"] = stonk_data["names"][i]
        new_dict["ticker"] = stonk_data["ticker"][i]
        new_dict["initial"] = stonk_data["initial"][i]
        new_dict["current"] = stonk_data["current"][i]
        new_dict["percent"] = stonk_data["percent"][i]
        send_arr.append(new_dict)

    spy = {}
    spy = get_spy_data()
    names = stonk_data["names"]
    percent_change = stonk_data["percent"]

    send = jsonify(stonkers=send_arr, king=stonk_data["names"][max_stonker], spy=spy["percent"], names=names, percent_change=percent_change)


    #test initial price
    #from1999 = get_data('msft' , start_date = '01/01/1999')
    return send


if __name__ == "__main__":
    #from waitress import serve
    appFlask.run(debug=False)
    #serve(appFlask, host="0.0.0.0", port=8080)
