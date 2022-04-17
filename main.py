import random

from flask import Flask, render_template
from flask_apscheduler import APScheduler
from datetime import datetime
from git import Repo
import os

from factory import StockAnalysis, convert_fig_to_json
from keys.keys import Columns, AnalysisFunctions, PlotTypes
from configs import save_html

app = Flask(__name__, template_folder="templates/")
scheduler = APScheduler()


@app.route("/")
def index():
    t = "AAPL"
    test = StockAnalysis()
    analysis = AnalysisFunctions.MovingAverage()
    analysis.set_sample_size(24*4)
    x = test.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=t)
    g1 = convert_fig_to_json(x)

    settings = {
        'start': '2013-01-01',
        'end': datetime.now().strftime("%Y-%m-%d"),
        'interval': '1d'
    }
    test.download(**settings)
    analysis = AnalysisFunctions.MovingAverage()
    analysis.set_sample_size(10)
    x = test.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=t)
    g2 = convert_fig_to_json(x)

    return render_template(template_name_or_list="plot.html", g1=g1, g2=g2, title=t)


@app.route("/short")
def short():
    t = "AAPL"
    test = StockAnalysis()
    test.download(period='1mo', interval='30m')
    analysis = AnalysisFunctions.MovingAverage()
    analysis.set_sample_size(3)
    x = test.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=t)
    graph_json = convert_fig_to_json(x)
    return render_template(template_name_or_list="plot.html", graph1=graph_json, title=t)


def output_html():
    from flask import render_template
    t = "AAPL"
    test = StockAnalysis()
    test.download(period='6mo', interval='1d')
    analysis = AnalysisFunctions.MovingAverage()
    analysis.set_sample_size(3)
    x = test.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=t)
    graph_json = convert_fig_to_json(x)
    with app.app_context():
        temp = render_template(template_name_or_list="plot.html", graph1=graph_json, title=t)
        save_html(temp)

if __name__ == "__main__":
    # scheduler.add_job(id='Scheduled Task', func=output_html, trigger="interval", seconds=5)
    # scheduler.start()
    app.run(host="127.0.0.1", port=8080, debug=True)
