from dydx3 import Client
from web3 import Web3
from dydx3.constants import MARKET_BTC_USD, ORDER_SIDE_BUY
from dydx3.constants import ORDER_SIDE_SELL
from dydx3.constants import ORDER_TYPE_LIMIT
from dydx3.constants import TIME_IN_FORCE_GTT
import requests
from requests import Request
from time import time
import json
import config
from datetime import datetime



def makeBuy(amount, price, pair, _client):
    client = _client
    client.private.create_order(
    position_id=1, # required for creating the order signature
    market=pair,
    side=ORDER_SIDE_BUY,
    order_type=ORDER_TYPE_LIMIT,
    post_only=False,
    size=amount,
    price=price,
    expiration_epoch_seconds=1613988637,
    time_in_force=TIME_IN_FORCE_GTT
)

def makeSell(amount, price, pair, _client):
    client = _client
    client.private.create_order(
    position_id=1, # required for creating the order signature
    market=pair,
    side=ORDER_SIDE_SELL,
    order_type=ORDER_TYPE_LIMIT,
    post_only=False,
    size=amount,
    price=price,
    expiration_epoch_seconds=1613988637,
    time_in_force=TIME_IN_FORCE_GTT
)

def get_spread(max_spread):
    orderbook = requests.get(config.API_ENDPOINT+"/v3/orderbook/BTC-USD")
    r = orderbook.json()
    market_price = requests.get(config.API_ENDPOINT+"/v3/markets")
    market = float(market_price.json()["markets"]["BTC-USD"]["indexPrice"])

    total_spread = 0
    trades = []
    while (total_spread <= max_spread):  
        pares = len(trades)
        spread = float(r["asks"][pares]["price"]) - float(r["bids"][pares]["price"])
        spread_percent = spread/market
        askSize=r["asks"][pares]["size"]
        askPrice=r["asks"][pares]["price"]
        bidSize=r["bids"][pares]["size"]
        bidPrice=r["bids"][pares]["price"]
        consolePrints = []
        if (total_spread + spread) <= max_spread:
            total_spread = total_spread + spread
            #print("ask" + str(r["asks"][i]) + " | bid " + str(r["bids"][i]) + " | spread: " + str(spread) + " | spread %: " + str(spread_percent) + " | total Spread: " + str(total_spread))
            consolePrint = f"ask: {askSize}, {askPrice} | bid: {bidSize}, {bidPrice} | spread: {spread} | spread %: {spread_percent} | total Spread: {total_spread}"
            consolePrints.append(consolePrint)
            trade = [askSize, askPrice, bidSize, bidPrice]
            trades.append(trade)
        else:
            return (trades, total_spread, pares, consolePrints) #[0: ask size][1: ask price][2: bid size][3: bid price][4: Spread total del ciclo][5: Cantidad de pares encontrados][6: console print]
            
        
from time import time
def count_elapsed_time(f):
    """
    Decorator.
    Execute the function and calculate the elapsed time.
    Print the result to the standard output.
    """
    def wrapper():
        # Start counting.
        start_time = time()
        # Take the original function's return value.
        ret = f()
        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        print("Elapsed time: %0.10f seconds." % elapsed_time)
        return ret
    
    return wrapper

def bot(max_spread):
  start = datetime.now()
  _total_spread = 0
  _total_orders = 0
  ciclo = 1

  while True:
        trades = get_spread(max_spread)[0]    
        for trade in trades:
            if trade[0] < trade[2]:
              size_value = float(trade[0])
            elif trade[2] < trade[0]:
                size_value = float(trade[2])
            else:
                size_value = trade[0]

        
#count_elapsed_time(bot(10))

bot(10)
