import json
import os

configs = {}

try:
    with open("configs/configs.json", "r") as js:
        configs = json.load(js)
except IOError as err:
    print("Error Loading configs.json")

ticker_list = configs.get("tickers", [])
html_output_dir = configs.get("output html", "/")
local_html = configs.get("local html", "/")


def save_html(html: str, filepath: str = html_output_dir):
    try:
        with open(filepath + "index.html", 'w') as fp:
            fp.write(html)
            fp.close()
        # os.replace(filepath, html_output_dir + "index.html")
    except Exception as err:
        print(f"{err}")
