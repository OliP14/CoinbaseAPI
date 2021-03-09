from keys import coinbase_api_key, coinbase_api_secret
from coinbase.wallet.client import Client

client = Client(coinbase_api_key, coinbase_api_secret)

accounts = client.get_accounts()
#print(accounts)

btc_id = "2205fa25-b8e3-5a35-a110-d5106c6234b9"
btc_transactions = client.get_transactions(btc_id)
btc_buys = client.get_buys(btc_id)

total_usd_subtotal = 0
btc_balance = 0
btc_price = 0

# Finds the length of the btc_buys
def buys_length():
    length = len(btc_buys.data)
    return length

# Total BTC balance in account (int)
def total_btc_balance():
    global btc_balance
    #btc_balance = 0
    for balance in accounts.data:
        if balance["currency"] == "BTC":
            value = str(balance["balance"]).replace("BTC ", "")
            btc_balance += float(value)
    return(btc_balance)

# Returns the current BTC price (int)
def current_btc_price():
    global btc_price
    #btc_price = 0
    price = client.get_spot_price(currency_pair = "BTC-USD")
    btc_price = float(price.amount)
    return(btc_price)

# Adds all of the USD subtotals per transaction (excluding fee) (returns total initial investments) (ints)
def total_usd_subtotals():
    global total_usd_subtotal
    #total_usd_subtotal = 0
    i = 0
    for i in range(buys_length()):
        value = str(btc_buys[i]["subtotal"]).replace("USD", "")
        total_usd_subtotal += float(value)
        i += 1
    return(total_usd_subtotal)

# Prints your total profit
def profit():
    profit = 0
    percent = 0
    current_btc_price()
    total_btc_balance()
    total_usd_subtotals()
    profit = (btc_price * btc_balance) - total_usd_subtotal
    percent = (profit/total_usd_subtotal) * 100
    print("Total BTC profit: " + "$" + str(profit) + " (%" + str(percent) + ")")


profit()