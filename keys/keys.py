from enum import Enum


class Columns(Enum):
    Open = "Open"
    high = "High"
    low = "Low"
    close = "Close"
    adj_close = "Adj Close"
    volume = "Volume"
    date = "Date"
    ma = "MA"


class AnalysisFunctions:
    class MovingAverage:
        value_type = Columns.high.value
        sample_size = 6
        open_price = False
        close_price = True
        sell_indicators = True
        buy_indicators = True

        def set_value_type(self, _input: str):
            cols = ["Open", "High", "Low", "Close", "Adj Close"]
            if _input in cols:
                self.value_type = _input
            else:
                print(f"value_type can only be one of the following\n{cols}")

        def set_sample_size(self, _input: int):
            self.sample_size = _input

    class Fake:
        pass


class PlotTypes(Enum):
    SUBPLOTS = "SUB-PLOTS"
    TRACE = "TRACE"
