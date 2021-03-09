from keys import coinbase_api_key, coinbase_api_secret
from coinbase.wallet.client import Client

client = Client(coinbase_api_key, coinbase_api_secret)

accounts = client.get_accounts()
#print(accounts)

eth_id = "9f829e6b-fcdb-5179-a77f-641803e9208e"
eth_transactions = client.get_transactions(eth_id)
eth_buys = client.get_buys(eth_id)

total_usd_subtotal = 0
eth_balance = 0
eth_price = 0

# Finds the length of the eth_buys
def buys_length():
    length = len(eth_buys.data)
    return length

# Total eth balance in account (int)
def total_eth_balance():
    global eth_balance
    #eth_balance = 0
    for balance in accounts.data:
        if balance["currency"] == "ETH":
            value = str(balance["balance"]).replace("ETH ", "")
            eth_balance += float(value)
    return(eth_balance)

# Returns the current eth price (int)
def current_eth_price():
    global eth_price
    #eth_price = 0
    price = client.get_spot_price(currency_pair = "ETH-USD")
    eth_price = float(price.amount)
    return(eth_price)

# Adds all of the USD subtotals per transaction (excluding fee) (returns total initial investments) (ints)
def total_usd_subtotals():
    global total_usd_subtotal
    #total_usd_subtotal = 0
    i = 0
    for i in range(buys_length()):
        value = str(eth_buys[i]["subtotal"]).replace("USD", "")
        total_usd_subtotal += float(value)
        i += 1
    return(total_usd_subtotal)

# Prints your total profit
def profit():
    profit = 0
    percent = 0
    current_eth_price()
    total_eth_balance()
    total_usd_subtotals()
    profit = (eth_price * eth_balance) - total_usd_subtotal
    percent = (profit/total_usd_subtotal) * 100
    print("Total ETH profit: " + "$" + str(profit) + " (%" + str(percent) + ")")


profit()