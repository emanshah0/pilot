import json

import plotly.utils
from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import plotly.graph_objects as go
import pyautogui

from factory import StockAnalysis, convert_fig_to_json, get_scatter_graph, combine_graphs
from keys.keys import Columns, AnalysisFunctions, PlotTypes
from configs import save_html, ticker_list
from data.tools import Buffer

app = Flask(__name__, template_folder="templates/")
scheduler = APScheduler()
buffer = Buffer()
buffer.clear_cache()


@app.route("/", methods=["GET", "POST"])
def index():
    index_template = render_template(template_name_or_list="index.html")
    return index_template


@app.route("/MA", methods=["GET", "POST"])
def ma():
    index_template = render_template(template_name_or_list="index.html")
    if request.method == 'POST':
        if request.form['submit_ticker'] == 'Submit Ticker':
            if request.form['user_ticker'] != '':
                min_ma, max_ma = 20, 100
                ticker = request.form.get("user_ticker").upper()
                data_dump = StockAnalysis(buffer)

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
                for i in range(min_ma, max_ma, 10):
                    analysis.set_sample_size(i)
                    buffer.cache(section="short")
                    data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=ticker)
                buffer.cache(section="short")
                analysis.set_sample_size(25)
                temp_graph = data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=ticker)
                g1 = convert_fig_to_json(temp_graph)
                graph_1 = render_template(template_name_or_list="plot.html", graph=g1, id="Short", slider_id="short")

                data_dump = StockAnalysis(buffer)
                settings = {
                    'tickers': ticker,
                    'period': "2y",
                    'interval': "1h",
                    'group_by': "ticker",
                    'threads': True,
                }
                if not data_dump.download(settings):
                    return index_template + graph_1 + "<br> NO DATA FOR LONG TERM CONFIGURATION " + ticker

                analysis = AnalysisFunctions.MovingAverage()
                for i in range(min_ma, max_ma, 5):
                    analysis.set_sample_size(i)
                    buffer.cache(section="long")
                    data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=ticker)
                buffer.cache(section="long")
                analysis.set_sample_size(100)
                temp_graph = data_dump.get_graph(analysis=analysis, plot_type=PlotTypes.TRACE, ticker=ticker)
                g2 = convert_fig_to_json(temp_graph)

                index_template = render_template(template_name_or_list="index.html", title=ticker)
                graph_2 = render_template(template_name_or_list="plot.html", graph=g2, id="Long", slider_id="long")
                full_html = index_template + graph_1 + graph_2
                with app.app_context():
                    save_html(full_html)
                return full_html
            else:
                return index_template + "<br> ENTER TICKER ABOVE"
        elif request.method == 'GET':
            return index_template
    return index_template


@app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():
    if request.method == "POST":
        if request.form:
            new_sample_size = request.form['ss']
            this_id = request.form['id']

            buffer.load(section=this_id, sample_size=new_sample_size)
            if buffer.graph_exists():
                ts = buffer.get_time_series()
                ma = buffer.get_ma()
                bts = buffer.get_buy_series()
                bpk = buffer.get_buy_peaks()
                sts = buffer.get_sell_series()
                spk = buffer.get_sell_peaks()
                cp = buffer.get_close_price()
                traces = [get_scatter_graph(**{'x': ts,
                                               'y': ma,
                                               'name': f"MA:{new_sample_size}"}),
                          get_scatter_graph(**{'x': ts,
                                               'y': cp,
                                               'name': "Close Price",
                                               'opacity': 0.6,
                                               'marker': dict(
                                                   color='#ff8000', )}),
                          get_scatter_graph(**{'x': sts,
                                               'y': spk,
                                               'name': "SELL",
                                               'mode': 'markers',
                                               'marker': dict(
                                                   size=8,
                                                   color='red',
                                                   symbol='arrow-bar-down'
                                               ), }),
                          get_scatter_graph(**{'x': bts,
                                               'y': bpk,
                                               'name': "BUY",
                                               'mode': 'markers',
                                               'marker': dict(
                                                   size=8,
                                                   color='green',
                                                   symbol='arrow-bar-up'
                                               ), })
                          ]
                graph = combine_graphs(traces, PlotTypes.TRACE)
                width, height = pyautogui.size()
                rgb = 220
                margins = 30
                op = 0.8
                graph.update_layout(
                    width=int(width * 0.98),
                    height=int(height * 0.6),
                    margin=dict(l=margins, r=margins, t=margins, b=margins),
                    paper_bgcolor=f"rgba({rgb},{rgb},{rgb},{op})",
                    plot_bgcolor=f"rgba({rgb},{rgb},{rgb}, {op})"
                )
                graph = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
                gid = "Long" if this_id.lower() == "long" else "Short"
                return {'gp': graph, 'gid': gid}
        else:
            print("no data")


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
    # app.run(host="localhost", port=5000, debug=True)
    app.run(host="127.0.0.1", port=5000, debug=True)
