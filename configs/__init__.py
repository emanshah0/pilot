import json

configs = {}

try:
    with open("configs/configs.json", "r") as js:
        configs = json.load(js)
except IOError as err:
    print("Error Loading configs.json")

ticker_list = configs.get("tickers", [])