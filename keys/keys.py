from enum import Enum


class Columns(Enum):
    Open = "Open"
    high = "High"
    low = "Low"
    close = "Close"
    adj_close = "Adj Close"
    volume = "Volume"
    date = "Date"


class AnalysisFunctions:
    class MovingAverage:
        value_type = "High"
        sample_size = 6

        def set_value_type(self, _input: str):
            cols = ["Open", "High", "Low", "Close"]
            if _input in cols:
                self.value_type = _input
            else:
                print(f"value_type can only be one of the following\n{cols}")

        def set_sample_size(self, _input: int):
            self.sample_size = _input

    class Fake:
        pass


class PlotTypes(Enum):
    SCATTER = "SCATTER"
    SCATTER_SUBPLOTS = "SCATTER SUB-PLOTS"
    TRACE = "TRACE"
    TRACE_SUBPLOTS = "TRACE SUB-PLOTS"
