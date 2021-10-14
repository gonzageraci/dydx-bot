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
import datetime

publicClient = Client(
    host=config.API_ENDPOINT
)


privateClient = Client(
    host=config.API_ENDPOINT,
    api_key_credentials={'key': '686405d0-598a-9f0a-1ba5-4598ed5099da', 'secret': 'Klqmh2rhuHrOPqfEhBnn4BhKyc_4hxUGSCzkPFt6', 'passphrase': 'BOeRJv0-yQOkk_Lu9jrS'},
    #eth_private_key=config.eth_private_key,
    stark_private_key=config.StarkPrivateKey,
    #default_ethereum_address=config.eth_address,
    #web3=Web3(Web3.HTTPProvider(config.API_ENDPOINT)),
)


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
    expiration_epoch_seconds= time() + 80,
    limit_fee="10",
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
    expiration_epoch_seconds= time() + 80,
    limit_fee="10",
)

def get_spread(max_spread,_market):
    orderbook = requests.get(config.API_ENDPOINT+"/v3/orderbook/"+_market)
    r = orderbook.json()
    market_price = requests.get(config.API_ENDPOINT+"/v3/markets")
    market = float(market_price.json()["markets"][_market]["indexPrice"])

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


