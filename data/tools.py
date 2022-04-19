import os
import json
import pandas as pd
from collections import defaultdict

class Buffer:
    """Caches Data For Active Sessions, Saves and Reports to Calls"""
    def __init__(self) -> None:
        # data
        self.time_series: list = None
        self.buy_time_series: list = None
        self.sell_time_series: list = None
        self.ma_map: dict = {}
        self.section: str = ""

        # directory
        self.root = "cache/"


    def cache(self, ts: list, mp: dict):
        self.ma_map = mp
        self.time_series = ts

    def save(self):
        if self.ma_map:
            for sample_id, packet in self.ma_map.items():
                pass

