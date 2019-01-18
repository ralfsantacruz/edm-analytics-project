from flask import Flask, render_template, request, Markup
# from graph_gen import generate_plot
# from map_gen import generate_scattermap, utc_to_pst
# from ETL import menu_items
# import os 
# from datetime import datetime
# from pytz import timezone
# import pytz
# from timefunc import pst_to_12hr
# from sqlalchemy import create_engine
from hip_hop_graph import plot_gen, top_10_rappers, make_top_rapper_chart
import pandas as pd

app = Flask(__name__)

@app.route("/")
def intro():
    plot = plot_gen()
    plot2 = top_10_rappers()
    plot3 = make_top_rapper_chart()
    return render_template("index.html", plot=plot,plot2=plot2,plot3=plot3)

if __name__ == "__main__":
    app.run(debug=True,threaded=True)