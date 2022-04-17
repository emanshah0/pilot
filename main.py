from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

from factory import StockAnalysis, convert_fig_to_json
from keys.keys import Columns, AnalysisFunctions, PlotTypes
from configs import save_html, ticker_list

app = Flask(__name__, template_folder="templates/")
scheduler = APScheduler()


@app.route("/", methods=["GET", "POST"])
def index():
    index_template = render_template(template_name_or_list="index.html")
    return index_template


@app.route("/test", methods=["GET", "POST"])
def test():
    index_template = render_template(template_name_or_list="index.html")
    if request.method == 'POST':
        if request.form['submit_ticker'] == 'Submit Ticker':
            if request.form['user_ticker'] != '':
                ticker = request.form.get("user_ticker").upper()
                data_dump = StockAnalysis()

                current_time = datetime.now()
                start_time = (current_time - relativedelta(months=12)).strftime("%Y-%m-%d")
                current_time = current_time.strftime("%Y-%m-%d")
                settings = {
                    'tickers': ticker,
                    'start': start_time,
                    'end': current_time,
                    'threads': True,
                    'interval': '1h'
                }
                if not data_dump.download(settings):
                    return index_template + "<br> NO DATA FOR PROVIDED TICKER: " + ticker

                analysis = AnalysisFunctions.MovingAverage()
                analysis.set_sample_size(24 * 1)
                temp_graph = data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=ticker)
                g1 = convert_fig_to_json(temp_graph)

                settings = {
                    'tickers': ticker,
                    'period': "2y",
                    'interval': "1h",
                    'group_by': "ticker",
                    'threads': True,
                }
                if not data_dump.download(settings):
                    return index_template + "<br> NO DATA FOR PROVIDED TICKER: " + ticker

                analysis = AnalysisFunctions.MovingAverage()
                analysis.set_sample_size(3 * 33)
                temp_graph = data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=ticker)
                g2 = convert_fig_to_json(temp_graph)

                index_template = render_template(template_name_or_list="index.html", graph=g1, title=ticker)
                graph_1 = render_template(template_name_or_list="plot.html", graph=g1, id="Short")
                graph_2 = render_template(template_name_or_list="plot.html", graph=g2, id="Long")
                return index_template + graph_1 + graph_2
            else:
                return index_template + "<br> ENTER TICKER ABOVE"
        elif request.method == 'GET':
            return index_template
    return index_template


def output_html():
    from flask import render_template
    t = "AAPL"
    data_dump = StockAnalysis()
    data_dump.download(period='6mo', interval='1d')
    analysis = AnalysisFunctions.MovingAverage()
    analysis.set_sample_size(3)
    temp_graph = data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=t)
    graph_json = convert_fig_to_json(temp_graph)
    with app.app_context():
        temp = render_template(template_name_or_list="plot.html", graph1=graph_json, title=t)
        save_html(temp)


if __name__ == "__main__":
    # scheduler.add_job(id='Scheduled Task', func=output_html, trigger="interval", seconds=5)
    # scheduler.start()
    app.run(host="localhost", port=5000, debug=True)
