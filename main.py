from flask import Flask, render_template
import os

from factory import StockAnalysis, convert_fig_to_json
from keys.keys import Columns, AnalysisFunctions, PlotTypes

os.system("cls")
app = Flask(__name__, template_folder="templates/")


@app.route("/")
def index():
    test = StockAnalysis()
    analysis = AnalysisFunctions.MovingAverage()
    x = test.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker="AAPL")
    graph_json = convert_fig_to_json(x)
    return render_template(template_name_or_list="plot.html", graphJSON=graph_json)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
