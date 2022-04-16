import yfinance as yf
import json
import pandas as pd
from typing import Tuple
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from datetime import datetime

from configs import ticker_list
from keys.keys import Columns, AnalysisFunctions, PlotTypes


class StockAnalysis:
    def __init__(self):
        """
        valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        """
        self.data = {}
        self.download()

    def download(self, period="2y", interval="1h", group_by="ticker", threads=True):
        tickers_str = " ".join(ticker_list)
        cache = yf.download(tickers=tickers_str, period=period, interval=interval, group_by=group_by, threads=threads)
        if len(ticker_list) == 1:
            cache.sort_index()
            cache.reset_index(inplace=True)
            if "index" in cache:
                cache = cache.rename(columns={"index": "Date"})
            self.data = {ticker_list[0]: cache}
        else:
            for key in cache.keys():
                cache[key].sort_index()
                cache[key].reset_index(inplace=True)
                if "index" in cache:
                    cache[key] = cache[key].rename(columns={"index": "Date"})
            self.data = cache

    def get_graph(self, analysis, plot_type: PlotTypes, ticker: str):
        graph: go.Figure = go.Figure()

        if isinstance(analysis, AnalysisFunctions.MovingAverage):
            time, ma = calculate_moving_average(data=self.data[ticker], value_type=analysis.value_type,
                                                sample_size=analysis.sample_size)
            if plot_type == PlotTypes.TRACE:
                traces = []
                traces.append(get_scatter_graph(time, ma, f"MA:{ticker}:{analysis.value_type}"))
                if analysis.open_price:
                    traces.append(get_scatter_graph(time, self.data[ticker][Columns.Open.value], f":{ticker}:{Columns.Open.value}"))
                if analysis.close_price:
                    traces.append(get_scatter_graph(time, self.data[ticker][Columns.adj_close.value], f":{ticker}:{Columns.adj_close.value}"))
                graph = combine_traces(traces)
        graph.update_layout(
            width=1300,
            height=700,
        )
        return graph
    
    def populate_avgs(self):
        for key in self.data.keys():
            temp = []
            for idx, row in self.data[key].iterrows():
                avg = row[Columns.high.value]
                temp.append()


def convert_fig_to_json(fig) -> str:
    return json.dumps(fig, cls=PlotlyJSONEncoder)


def get_scatter_graph(*argv) -> go.Scatter:
    """
    :param argv list of tuples/lists representing list of times and series values, example; [['2022-10-05'],
    [10] "Name"]

    :return: Scatter Graph in PlotlyJSONEncoder Format
    """
    if len(argv) % 3 != 0:
        print("Invalid Number of Arguments")
        return None
    time, series, name = argv[0], argv[1], argv[2]
    return go.Scatter(y=series, x=time, name=name, showlegend=True)


def get_scatter_graph_animated(*argv) -> go.Scatter:
    """
    :param argv list of tuples/lists representing list of times and series values, example; [['2022-10-05'],
    [10] "Name"]

    :return: Scatter Graph in PlotlyJSONEncoder Format
    """
    if len(argv) % 3 != 0:
        print("Invalid Number of Arguments")
        return None
    time, series, name = argv[0], argv[1], argv[2]
    temp = [_ for _ in range(len(series))]
    return go.Scatter(y=series, x=temp, animation_frame=time, name=name, showlegend=True)


def calculate_moving_average(data: pd.DataFrame, value_type: str, sample_size: int = 12) -> Tuple[list, list]:
    """Returns Sorted Lists: Datetimes, Moving Average"""
    stack, ma = [], []
    for index, row in data.iterrows():
        stack.append(row[value_type])
        if len(stack) > sample_size:
            stack.pop(0)
        ma.append(sum(stack) / sample_size)
    return data[Columns.date.value].to_list(), ma


def combine_traces(traces: list) -> go.Figure:
    fig = go.Figure()
    for trace in traces:
        fig.add_trace(trace)
    return fig




# def get_scatter_subplots(*argv):
#     if len(argv) % 3 != 0:
#         print("Invalid Number of Arguments")
#         return None
#     fig = plotly.subplots.make_subplots(rows=len(argv) // 3, cols=1)
#     for i in range(0, len(argv), 3):
#         time, series, name = argv[i], argv[i + 1], argv[i + 2]
#         row = (i + 1) // 3 + 1
#         fig.add_scatter(y=series, x=time, name=name, row=row, col=1)
#     return fig
