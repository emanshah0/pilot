import plotly
import plotly.graph_objects as go
import yfinance as yf
import json
import pandas as pd
from typing import Tuple
from plotly.utils import PlotlyJSONEncoder

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
        cache.sort_index()
        cache.reset_index(inplace=True)
        if "index" in cache:
            cache = cache.rename(columns={"index": "Date"})
        if len(ticker_list) == 1:
            self.data = {ticker_list[0]: cache}
        else:
            self.data = cache

    def get_graph(self, analysis, plot_type: PlotTypes, ticker: str):
        graph: go.Figure = go.Figure()

        if isinstance(analysis, AnalysisFunctions.MovingAverage):
            args = []
            time, ma = calculate_moving_average(data=self.data[ticker], value_type=analysis.value_type,
                                                sample_size=analysis.sample_size)
            args.append(time)
            args.append(ma)
            args.append(f"MA:{ticker}:{analysis.value_type}")
            if plot_type == PlotTypes.TRACE:
                graph = get_scatter_graph(*args)
            temp = get_scatter_graph(time, self.data[ticker][Columns.high.value], f"Highs:{ticker}")
            combine_traces([graph, temp])
        graph.update_layout(
            width=1500,
            height=700,
        )
        return graph


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
#     """
#     argv[0] = list of datetimes
#
#     argv[1] = list of values
#
#     argv[2] = str : Name of series
#
#     :return: Scatter Graph in PlotlyJSONEncoder Format
#     """
#     if len(argv) % 3 != 0:
#         print("Invalid Number of Arguments")
#         return None
#     fig = plotly.subplots.make_subplots(rows=len(argv) // 3, cols=1)
#     for i in range(0, len(argv), 3):
#         time, series, name = argv[i], argv[i + 1], argv[i + 2]
#         row = (i + 1) // 3 + 1
#         fig.add_scatter(y=series, x=time, name=name, row=row, col=1)
#     return fig
