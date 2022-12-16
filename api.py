from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from yahoo_fin import stock_info as si
from decimal import Decimal
import pandas as pd
import random
import bcrypt
#import time

appFlask = Flask(__name__)
CORS(appFlask, supports_credentials=True)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="",
    password="",
    hostname="",
    databasename="",
)
appFlask.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
appFlask.config["SQLALCHEMY_POOL_RECYCLE"] = 299
appFlask.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(appFlask)

users = []

stock_picks = []

# ('alex', 'alex@gmail.com', 'test5678', 'qwqq', 'apple')


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


    if(len(stock_dict["ticker"]) > 4):
        #print("starting to get nums ------")
        #print(current_p)
        # fix Mitch's price -- XLNX turned into 1.7234 shares of AMD
        current_p[4] = round(current_p[4] * 1.7234, 2)
        percent_c[4] = round((((current_p[4]-stock_dict["initial"][4])/stock_dict["initial"][4])*100),2)
        #print(f"Mitch's is {current_p[4]} and {percent_c[4]}")
    

    stock_dict["current"] = current_p
    stock_dict["percent"] = percent_c

def get_spy_data():
    stonk = {}
    stonk["ticker"] = ["SPY"]
    stonk["initial"] = [474.96]
    get_current_prices(stonk)
    get_current_prices
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
    #updateUsers()
    #print(len(users))
    #print(users[0])
    updateStockPicks("Alex", "$POOP")
    results = db.session.execute("SELECT * from stock_picks;")
    print(results.fetchall())
    """  results = db.session.execute("DELETE from users where username=\"john\";")
    results = db.session.execute("SELECT * from users;")
    print(results.fetchall())
    results = db.session.execute("SELECT * from users where username=\"presley\";")
    results = db.session.execute("SELECT * from users;")
    print(results.fetchall())
    user="testdummy"
    email="test@gmail.com"
    password= bytes("password22", "utf-8")
    salt= bcrypt.gensalt()
    password = bcrypt.hashpw(password, salt)
    name="test man"
    results = db.session.execute(f"insert into users values(\"{user}\", \"{email}\", \"{password.decode('utf-8')}\", \"{salt.decode('utf-8')}\", \"{name}\");")
    results = db.session.execute("SELECT * from users;")
    print(results.fetchall())
    checkUserPassword("testdummy", "password22") """
    return "This site is no longer valid and is only used for API purposes. Please visit www.pres.dev/stonks"


def updateUsers():
    results = db.session.execute("SELECT * from users;")
    users = []
    for user in results:
        users.append(user)
    print(users[0])


def updatePassword(user, password):
    print("update")
    salt= bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(bytes(password, "utf-8"), salt)
    results = db.session.execute(f"UPDATE users SET password = \"{hashed_pwd.decode('utf-8')}\", salt = \"{salt.decode('utf-8')}\" WHERE username =\"{user}\";")
    db.session.commit()


@appFlask.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def tryLogin():
    print("trying to login")
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        print(json)
        user = json['username']
        password = json['password']
        if(checkUserPassword(user,password)):
            return jsonify("this-is-secure")
    return jsonify("deny")


def updateStockPicks(user, newpick):
    results = db.session.execute("SELECT * from stock_picks;").fetchall()
    picks = []
    for current in results:
        picks.append(current)
    notPicked = True
    for pick in picks:
        if pick[1] == newpick:
            notPicked = False
    
    if(notPicked):
        # update
        results = db.session.execute(f"UPDATE stock_picks SET stock= \"{newpick}\" WHERE user=\"{user}\";")
        db.session.commit()
        # TODO: return some kind of json response
        return
    # TODO: return negative json response
    print("cannot update stock because it was already picked")
    return


def pickStock(user, stock_pick):
    results = db.session.execute("SELECT * from stock_picks;").fetchall()
    picks = []
    for current in results:
        picks.append(current)
    notPicked = True
    for pick in picks:
        if pick[1] == stock_pick:
            notPicked = False
    
    if(notPicked):
        # update
        print("inserting!")
        results = db.session.execute(f"insert into stock_picks values(\"{user}\", \"{stock_pick}\", \"Pending\");")
        db.session.commit()
        # TODO: return some kind of json response
        return
    # TODO: return negative json response
    print("Stock was already picked by a user")
    return






def checkUserPassword(username, password):
    results = db.session.execute("SELECT * from users;").fetchall()
    users = []
    for result in results:
        users.append(result)
    for user in users:
        #results = list(db.session.execute(f"SELECT * from users where username=\"{user}\";").fetchall())
        #print(results)
        print(f"user = {user[0]} and username = {username}")
        if(user[0] == username):
            current_pwd = user[2]
            bpassword= bytes(password, "utf-8")
            print("salt= "+user[3])
            hashed_pwd = bcrypt.hashpw(bpassword, bytes(user[3], "utf-8"))
            print(f"current = {current_pwd} and hash = {hashed_pwd.decode('utf-8')}")
            if(current_pwd == hashed_pwd.decode('utf-8')):
                print('access granted')
                return True
        #if(users[0] == user):
        #    print("user found.. checking password")
        #    if()
    return False

@appFlask.route('/api/SPY', methods=['GET', 'POST'])
def get_spy():
    stonk = {}
    stonk["ticker"] = ["SPY"]
    stonk["initial"] = [474.96]
    get_current_prices(stonk)
    #print(stonk)
    #get_current_prices(stonk)
    return "SPY"

@appFlask.route('/api/playground', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_pwd():
    print("helloooooooo")
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        print(json)
        if json['password'] == 'eagles':
            return jsonify("valid")
    return jsonify("deny")

@appFlask.route('/api/stonks', methods=['GET', 'POST'])
def stonk_api():
    #start = time.time()
    stonk_data = {}
    stonk_data["names"] = ['David', 'Jack', 'Jawsh', 'Mark', 'Mitch', 'Poles', 'Presley', 'Rex', 'Sean']
    stonk_data["ticker"] = ['SMRT', 'AI', 'DIS', 'SE', 'AMD', 'ROKU', 'AAPL', 'NVDA', 'IBM'] # Mitch is now AMD -- XLNX acquired
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

@appFlask.route('/api/random', methods=['GET', 'POST'])
def random_spy():
    rand_num = random.randrange(1,506)
    data = open("data/spy_stocks.txt")
    data = pd.read_csv('data/spy_stocks.txt', header=None)
    name = data.iloc[rand_num][0]
    ticker = si.get_company_info(name)
    print(ticker)
    for key in ticker:
        print("???")
        print(ticker['Value']['zip'])
        print(ticker['Value']['zip'])
        print(ticker['Value']['zip'])
        print(ticker['Value']['zip'])

    return str(ticker)


if __name__ == "__main__":
    #from waitress import serve
    appFlask.run(debug=True)
    #serve(appFlask, host="0.0.0.0", port=8080)
