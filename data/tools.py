import os
import json
import pandas as pd
from collections import defaultdict
import shutil


class Buffer:
    """
    Caches Data For Active Sessions, Saves and Reports to Calls
    """

    def __init__(self) -> None:
        # data
        self.ma: list = []
        self.time_series: list = []
        self.buy_peaks: list = []
        self.buy_time_series: list = []
        self.sell_peaks: list = []
        self.sell_time_series: list = []
        self.section: str = ""
        self.sample_size: str = ""

    def cache(self, ts=None, buy_ts=None, sell_ts=None, section=None, ma=None, buy_pk=None, sell_pk=None,
              sample_size=None):
        if ts:
            self.time_series = ts
        if buy_ts:
            self.buy_time_series = buy_ts
        if buy_pk:
            self.buy_peaks = buy_ts
        if sell_pk:
            self.sell_peaks = sell_ts
        if sell_ts:
            self.sell_time_series = sell_ts
        if section:
            self.section = section
        if sample_size:
            self.sample_size = sample_size
        if ma:
            self.ma = ma

    def save(self):
        ma_route = f"cache/{self.section}/{self.sample_size}/ma.csv"
        ts_route = f"cache/{self.section}/{self.sample_size}/ts.csv"
        bts_route = f"cache/{self.section}/{self.sample_size}/bts.csv"
        bpk_route = f"cache/{self.section}/{self.sample_size}/bpk.csv"
        sts_route = f"cache/{self.section}/{self.sample_size}/sts.csv"
        spk_route = f"cache/{self.section}/{self.sample_size}/spk.csv"
        try:
            os.makedirs(f"cache/long")
        except:
            pass
        try:
            os.makedirs(f"cache/short")
        except:
            pass
        try:
            os.makedirs(f"cache/{self.section}/{self.sample_size}")
        except:
            pass
        if os.path.isfile(ma_route):
            os.remove(ma_route)
        if os.path.isfile(ts_route):
            os.remove(ts_route)
        if os.path.isfile(bts_route):
            os.remove(bts_route)
        if os.path.isfile(bpk_route):
            os.remove(bpk_route)
        if os.path.isfile(sts_route):
            os.remove(sts_route)
        if os.path.isfile(spk_route):
            os.remove(spk_route)
        if self.ma:
            save_dataframe({'ma': self.ma}, ma_route)
        if self.time_series:
            save_dataframe({'ts': self.time_series}, ts_route)
        if self.buy_time_series and self.buy_peaks:
            save_dataframe({'bts': self.buy_time_series}, bts_route)
            save_dataframe({'bpk': self.buy_peaks}, bpk_route)
        if self.sell_time_series and self.sell_peaks:
            save_dataframe({'sts': self.sell_time_series}, sts_route)
            save_dataframe({'spk': self.sell_peaks}, spk_route)

    def load(self, section: str, sample_size: str):
        self.time_series, self.ma, self.buy_time_series, self.buy_peaks, self.sell_time_series, self.sell_peaks = \
            load_dataframe(section, sample_size)

    def clear_buffer(self):
        self.ma = []
        self.time_series = []
        self.buy_peaks = []
        self.buy_time_series = []
        self.sell_peaks = []
        self.sell_time_series = []
        self.section = ""
        self.sample_size = ""

    @staticmethod
    def clear_cache():
        try:
            shutil.rmtree("cache/short/")
            shutil.rmtree("cache/long/")
        except IOError as err:
            print(f"{err}\nError clearing cache")

    def graph_exists(self):
        if len(self.ma) > 0 and len(self.time_series) > 0:
            return True
        else:
            return False

    def get_ma(self):
        return self.ma

    def get_time_series(self):
        return self.time_series

    def get_buy_peaks(self):
        return self.buy_peaks

    def get_buy_series(self):
        return self.buy_time_series

    def get_sell_peaks(self):
        return self.sell_peaks

    def get_sell_series(self):
        return self.sell_time_series

    def get_section(self):
        return self.section

    def get_sample_size(self):
        return self.sample_size


def save_dataframe(data: dict, fp: str):
    try:
        pd.DataFrame(data).to_csv(fp)
    except IOError as err:
        print(f"{err}\nError Saving Results")


def load_dataframe(section, sample_size):
    ma_route = f"cache/{section}/{str(sample_size)}/ma.csv"
    ts_route = f"cache/{section}/{str(sample_size)}/ts.csv"
    bts_route = f"cache/{section}/{str(sample_size)}/bts.csv"
    bpk_route = f"cache/{section}/{str(sample_size)}/bpk.csv"
    sts_route = f"cache/{section}/{str(sample_size)}/sts.csv"
    spk_route = f"cache/{section}/{str(sample_size)}/spk.csv"

    ma, ts, bts, bpk, sts, spk = [], [], [], [], [], []
    if os.path.isfile(ma_route):
        ma = pd.read_csv(ma_route)
    if os.path.isfile(ts_route):
        ts = pd.read_csv(ts_route)
    if os.path.isfile(bts_route) and os.path.isfile(bpk_route):
        bts = pd.read_csv(bts_route)
        bpk = pd.read_csv(bpk_route)
    if os.path.isfile(sts_route) and os.path.isfile(spk_route):
        sts = pd.read_csv(sts_route)
        spk = pd.read_csv(spk_route)

    return ts, ma, bts, bpk, sts, spk
