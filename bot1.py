from bot_tools import get_spread, makeBuy, makeSell, publicClient, privateClient
from config import API_ENDPOINT, eth_address
from datetime import datetime

from dydx3.dydx_client import Client

client = privateClient

"""stark_private_key = client.onboarding.derive_stark_key()
print(stark_private_key)
client.stark_private_key = stark_private_key"""

def bot(max_spread, pair):
  start = datetime.now()
  _total_spread = 0
  _total_orders = 0
  ciclo = 1

  while True:
        trades = get_spread(max_spread)[0]    
        for trade in trades:
            if float(trade[0]) < float(trade[2]):
              size_value = float(trade[0])
            elif float(trade[2]) < float(trade[0]):
                size_value = float(trade[2])
            else:
                size_value = trade[0]
            
            makeBuy(str(size_value), str(trade[1]), pair,  client)
            makeSell(str(size_value), str(trade[3]), pair,  client)

#print(client.api_keys.create_api_key(ethereum_address= "0xb6eDcE2198cC2063906169fD4339B0F15EC558ea"))

#print(client.private.get_registration())

#print(client.private.get_api_keys())

#bot(10)

def test(max_spread, max_ciclos, pair):
  #start = datetime.now()
  _total_spread = 0
  _total_orders = 0
  ciclo = 1

  while ciclo <= max_ciclos:
        trades = get_spread(max_spread,pair)[0]    
        for trade in trades:
            if float(trade[0]) < float(trade[2]):
              size_value = float(trade[0])
            elif float(trade[2]) < float(trade[0]):
                size_value = float(trade[2])
            else:
                size_value = trade[0]
            
            makeBuy(str(size_value), str(trade[1]), pair, client)
            makeSell(str(size_value), str(trade[3]), pair, client)
            print(f"|{size_value} | {trade[1]} | {trade[3]} | {(float(trade[1])-float(trade[3]))*float(size_value)}")
        print("Fin ciclo: "+ str(ciclo))
        ciclo += 1

print(test(10, 10, "ETH-USD"))
#print(makeBuy("0.01", "3400", "ETH-USD", client))
"""
import time
print(time.time())"""