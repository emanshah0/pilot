import os
import json
import pandas as pd
from collections import defaultdict


class Buffer:
    """
    Caches Data For Active Sessions, Saves and Reports to Calls
    """

    def __init__(self) -> None:
        # data
        self.ma: list = []
        self.time_series: list = []
        self.buy_time_series: list = []
        self.sell_time_series: list = []
        self.section: str = ""

        # directory
        self.root = "cache/"

    def cache(self, ts=None, buy_ts=None, sell_ts=None, section=None, ma=None):
        if ts:
            self.time_series = ts
        if buy_ts:
            self.buy_time_series = buy_ts
        if sell_ts:
            self.sell_time_series = sell_ts
        if section:
            self.section = section
        if ma:
            self.ma = ma

    def save(self):
        if self.ma:
            pass
        pass
